# Evaluation measurement review

**Date:** 2026-08-15 (audit); campaign replaced 2026-08-15 (`5b0f584`)  
**Status:** Addressed. The dissertation Evaluation chapter and `context/eval-kpis/` now use only the measurement-fix traces (Poisson redraw, logical Voice clock, crash-node BE slice). The 38 GB pre-fix `results/` trees were deleted.

**Scope of this note:** How Chapter 6 KPIs used to be produced, and where those measurements misled — especially Voice vs Best Effort delay under `plain` DCF. Kept as a record of why the campaign was rerun.  
**Sources:** `veins_qos` apps + MAC, `kpi_dashboard` parser (`rust-kpi-dashboard-0.2.1`), archived rows in `context/eval-kpis/`.

---

## 1. Pipeline (what is actually timed)

```text
app[0] CritPacketSender  ── DSCP 0 periodic BE ──► UDP/IP ──► IEEE 802.11p MAC
app[1] CrashBurstApp     ── DSCP 46 crash VO  ──► UDP destPort 9001 (same socket as BE RX)
                              │
                              ▼
                    receivers' app[0] processPacket()
                              │
                    emit beE2eDelay / voE2eDelay
                              ▼
                    OMNeT .vec / .sca
                              ▼
                    kpi_dashboard parse → run_rows.json → thesis tables
```

- Every vehicle has both apps. Only `app[1]` with `targetNodeIndex` (default **0**) emits Voice.
- Voice is received and timestamped on **`app[0]`**, not on `CrashBurstApp` (`processPacket` there is a no-op).
- Delay is **creation → successful UDP delivery** at a *different* vehicle. Loopback multicast to the sender is dropped (`src == selfAddress`).
- Failed receptions (collision, out of range, queue drop before TX) **never enter the delay sample**.

Under `plain`, `qosStation` stays off: one DCF FIFO, no `QosClassifier`. DSCP is still on the packet, so the KPI pipeline can still split “VO” vs “BE” at the application. That split is **not** a MAC access-category split.

---

## 2. How each printed KPI is built

### 2.1 End-to-end delay

| Step | BE | Voice |
|------|----|--------|
| Clock start | `CreationTimeTag` at `sendOne()` (packet handed to the stack) | Same, but stamped at **physical repeat** send (`simTime()` in `CrashBurstApp::sendOne`), **not** `logicalCreationTime` |
| Clock end | First `CreationTimeTag` on RX in `CritPacketSender::processPacket` | Same |
| Extra filter | None | If `voDedupWindow > 0` (ini: `200ms`), keep only the **first** RX of `(src, sequence)` **for the whole run**. The map is never expired (NED comment). Sequence is the **logical burst id**, shared by all repeats. |
| Mean (tables) | Weighted mean of per-`app[0]` scalar `:mean` using `:count` as weights | Same |
| P95 (tables) | 95th percentile of **all** `beEndToEndDelay:vector` samples pooled across receivers, then **mean of those per-run P95s** across seeds | Same with `voEndToEndDelay:vector` |
| Min/max | Min of per-module mins / max of per-module maxes | Same |

Parser only reads `Scenario.node[*].app[0]` for delay vectors (`is_node_app(module, 0)`). That is correct given where signals are emitted.

**What this is:** delay of packets that were decoded by at least one neighbor, weighted by how many neighbors decoded them (one TX with nine RX copies → nine P95 samples).

**What this is not:** MAC service time of a typical queued frame; delay of dropped frames; time from *logical* crash sequence to first useful copy; per-sender delay.

### 2.2 Jitter

Mean absolute difference between **consecutive samples on the same OMNeT vector** (one vector per receiver). Not RFC 3550 jitter, not inter-sender, not aligned in simulation time.

### 2.3 Reach

| Printed name | Formula | After dedup? |
|--------------|---------|----------------|
| Voice RX/alert (`vo_rx_per_tx`) | `voRxPackets` / `voLogicalTxPackets` (falls back to physical TX if logical count is 0) | Yes: `voRxPackets` is incremented only for the first copy of each sequence |
| BE RX/TX | `beRxPackets` / `beTxPackets` | No |

So Voice reach is roughly “vehicles that got **at least one** copy of a logical alert.” BE reach is “received copies per physical packet.” They are not the same denominator. Voice physical TX at high load is 8× logical TX (`repeatCount = 8`).

### 2.4 MAC drops

- Aggregate `packetDrop:count` is summed over **every node MAC**, including **receive-side** “incorrectly received” discards. One collision can increment many receivers, so `mac_drop_per_tx` can exceed 1.
- Per-AC counters exist only when EDCA + classifier are on. Under `plain` they are unclassified / `n.a.`
- If attributed BE+VO+unclassified ≈ **2×** aggregate, the parser halves attributed counts (documented double-count guard).

### 2.5 Controller counters

Summed from `mac.hcf` statistics (`vo_protection_activation`, `be_dropped_while_blocked`, `be_grant_suppressed`). Zero / absent under `plain` and `edca_only`.

---

## 3. What might be wrong (ranked)

### P1 — Best Effort `exponential(125ms)` is not a per-packet Poisson process

**Code.** `CritPacketSender` reads `par("sendInterval")` **once** in `startApplication()` and reuses that interval forever. The NED parameter is not `volatile`. In the ini, `sendInterval = exponential(125ms)` is therefore **one draw per vehicle**, then a **periodic** CBR source at that period.

**Thesis.** Chapter 4 / 6 describe “exponential inter-arrivals with mean 125 ms” and “approaching 800 packets/s fleet-wide.” That is the Poisson reading.

**Why it matters.** An exponential draw has a heavy left tail. A handful of vehicles can freeze a 1–5 ms period and become greedy BE sources. That matches the archived heavy `plain_netload_high` TX counts:

| Seed | BE TX | Queue overflow | BE P95 | VO P95 | VO max |
|------|------:|---------------:|-------:|-------:|-------:|
| `#0` | 55 053 | 0 | 0.678 ms | 0.676 ms | 1.64 ms |
| `#1` | 359 358 | 172 423 | 73.7 ms | 0.678 ms | 1.41 ms |
| `#2` | 187 715 | 37 110 | 97.8 ms | 2.52 ms | 4.83 ms |

Seed `#0` is ~100 × 70 s / 0.125 s ≈ 56 k, i.e. typical periods. Seeds `#1`/`#2` are 3–6× that load. The 57 ms **mean** BE P95 is mostly “did this seed draw a near-greedy BE period,” not a stable high-load operating point.

This also feeds DCF unfairness: always-backlogged nodes re-contend immediately and keep their own FIFO short while others overflow.

### P2 — Voice vs BE delay under `plain` is not a same-MAC, same-sender comparison

Under `plain`, MAC treatment is identical. The two columns still differ because:

1. **Different senders.** Voice is one stopped crash node. BE P95 is 100 queues, dominated by the worst.
2. **Different time windows.** Voice exists only in the 30 s alert (`crashAt=30s`, `resumeAfter=30s`). BE is the whole 70 s, including SUMO insertion.
3. **Different offered load at the crash node.** During the alert, node 0 injects ~400 physical Voice packets/s (8 repeats / 20 ms) plus its BE. That node is a greedy DCF source; its FIFO can stay short while other BE nodes overflow. Seed `#1`: all ~12 000 Voice frames were sent, Voice overflow 0, Voice **max** 1.4 ms, while the fleet overflowed 172 k frames.
4. **Payload / airtime.** 260 B vs 420 B (~0.03 ms at low load). Harmless next to 70 ms.

**Prediction if DCF is class-blind:** crash-node BE delay **during the alert** should sit next to Voice. That slice is **not recorded**. Until it is, a 100× Voice/BE P95 gap under `plain` should not be read as “DCF prefers Voice.” Seed `#0` (0.676 vs 0.678 ms) is the only seed that actually tests “same MAC ⇒ same delay.”

### P3 — Voice delay is first-copy-of-burst, clocked from the physical repeat, not from the logical alert

`CrashBurstApp` computes `logicalCreationTime` and then **ignores it** for `CreationTimeTag` (stamps `simTime()` at each repeat). Combined with run-long dedup on logical sequence:

- Recorded Voice delay ≈ MAC/air delay of the **first successful repeat**, not waiting time from the crash sequence.
- If repeat 0 is lost and repeat 5 flies immediately, the sample is ~airtime even though the alert is already ~25 ms old.
- Dedup **cannot** turn a 74 ms sender FIFO into 0.7 ms (the first successful copy would still have waited). It *can* hide later, slower copies and the logical age of the burst.
- `voDedupWindow = 200ms` does not expire; it is an on/off switch for run-long uniqueness.

BE has no analogue: every received copy is a delay sample.

### P4 — Delay P95 conditions on success and over-weights well-connected receivers

Multicast + no ACK: collisions and uncovered neighbors disappear. A packet received by nine close vehicles contributes nine small samples; a packet that only one far vehicle gets contributes one. P95 is not “95 % of transmissions met this latency.”

### P5 — Reach ratios are not comparable across classes

Voice RX/alert ≈ 9.07 (`plain` high) vs BE RX/TX ≈ 6.15 is largely **counting rules** (logical vs physical, dedup vs not), plus geometry (stopped crash node vs fleet average, early sparse BE). It is not evidence that DCF delivers Voice farther than BE.

### P6 — MAC drop totals mix TX drops and RX discards, all nodes

Useful as a congestion intensity signal; easy to misread as “lost application packets.” `mac_drop_per_tx > 1` is expected when many receivers mark a frame incorrect. Per-AC overflow is `n.a.` under `plain`; using `0` in that column would be wrong (already fixed in the thesis).

### P7 — Mean and P95 are not the same population aggregator

Mean delay = weighted scalar means. P95 = pooled vectors. Jitter = successive in-vector deltas. Fine if documented; dangerous if someone treats jitter as a tail metric.

### P8 — Seed budget vs seed-dependent load

Heavy *n* = 3. After P1, two of three `plain` high seeds are in a different load regime than the third. Averaging them into 57 ms BE P95 hides that bimodality. Ranges on the tables help; *t*-intervals would not.

---

## 4. What is probably fine

- Class split at RX uses DSCP on the packet (app-tagged), not a phantom EDCA classifier under `plain`.
- Self-RX is excluded.
- Voice TX counts: 1500 logical × 8 repeats ≈ 12 000 physical, stable across seeds — the crash app is not dropping at the source.
- Parser `app[0]` / `app[1]` split matches where signals live.
- Double-count guard on AC drops is explicit.
- Cross-**policy** Voice P95 (plain → EDCA → emergency) is still the least-bad comparison: same crash app, same parser, same dedup. It does **not** prove how much of the 0.90 → 0.46 ms move is MAC prioritization vs change in who is backlogged.

---

## 5. Checks that would settle P2/P3 (no new campaign required if vectors exist)

From existing `plain_netload_high` `.vec` files, per seed:

1. **Crash-node BE delay** (`node[0].app[0]` BE samples) vs **Voice**, restricted to *t* ∈ [30 s, 60 s]. If they match, P2 is confirmed and the table gap is other nodes.
2. Histogram of **per-node BE `sendInterval`** (or BE TX count per node). If a few nodes account for the 55 k → 359 k jump, P1 is confirmed.
3. Voice delay with **logical** creation time (needs a code stamp) vs current physical stamp — only if (1) still looks suspicious.

A correct BE load for a future campaign: `volatile` `sendInterval`, re-read `par("sendInterval")` on every send, so each packet is Exp(mean) rather than one CBR period per car.

---

## 6. Implications for the printed Evaluation

Keep: within-class, cross-policy Voice tails; emergency vs EDCA as a **mechanism** check; seed ranges; `n.a.` for `plain` AC drops.

Do not lean on: `plain` Voice P95 ≪ `plain` BE P95 as proof of anything about DCF; 57 ms as a typical BE cost of “high load”; Voice RX/alert vs BE RX/TX as a fan-out gap; “exponential 125 ms” as a Poisson fleet unless the sender is fixed.

The discussion subsection on plain DCF is pointing at a real issue (two processes, not two ACs). The missing sentence is that the crash **node** is also a different *offered-load and queueing* process, and that BE load is seed-unstable because intervals are frozen exponential draws.
