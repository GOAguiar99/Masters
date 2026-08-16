# Evaluation: VO protection under hotspot load (hypothesis → method → confirmation)

**Date:** 2026-08-16
**Status:** Hypothesis confirmed by simulation campaign (heavy, post-fix measurements)
**Scope of this note:** Why VO protection modes (stable/guarded/emergency) showed no
VO advantage in the uniform-load campaign, the causal hypothesis that follows, and
the hotspot (S1) campaign designed to falsify it. Supersedes any pre-fix VO-policy
claims; see `EVAL_MEASUREMENT_REVIEW.md` for the measurement audit that made this
question necessary.

**Sources:** `veins_qos` apps + `V2xHcf` MAC, `kpi_dashboard` parser
`rust-kpi-dashboard-0.2.1`, branch `fix/measurement-poisson-vo-clock`
(commits `5b0f584` fix, `ee243dc` nits, `9a92dc1`+`6189876` predictive A/B added
and reverted, `abf1922`+`c4467cf`+`0cbc984` hotspot configs).

## 1. Hypothesis

> Emergency-style protection (suppress/drop neighboring BE around crash VO bursts)
> cannot measurably improve VO delay or delivery when BE arrivals are uniformly
> random, because VO loss is then dominated by receiver-side collision corruption
> from ~100 equiprobable low-duty-cycle senders — not by identifiable hot BE
> neighbors. Each node accounts for ~1/N of near-crash collision opportunities;
> node-local blocking removes ~1% of ambient airtime for tens of ms at a time and
> only after a *decodable* first copy, so the marginal benefit is below
> measurement noise. VO delay is additionally floored by burst self-queueing at
> the single source. When offered airtime is instead concentrated in a few
> senders, protection acquires a target and VO gains should reappear.

Two falsifiable predictions were made:

- **P1 (reappearance):** with a few high-rate neighbors near the crash, emergency
  protection must show a measurable VO advantage over plain/EDCA.
- **P2 (invariance):** under uniform Poisson load, no policy separates from plain
  on VO mean/P95/delivery at any density or load.

## 2. Method

### 2.1 Measurement basis

All numbers below use the corrected measurement (`5b0f584`): per-packet
`volatile` Poisson draws for BE, and Voice delay stamped with the logical burst
time (alert age of the first received copy), plus the crash-sender BE slice
`beEndToEndDelayFromCrash`. Parser `rust-kpi-dashboard-0.2.1`. Pre-fix caches and
raws were discarded; pre-fix values quoted here were recovered from the 18:58 SVG
export of `fig_01` (bar-pixel decoding), not from raw traces.

### 2.2 P2 — uniform-load invariance campaign (ruling out alternatives)

- Matrices: light (10 veh) × {high, stress}; heavy (100 veh) × {low, medium, high,
  stress=exp(25ms)/420B}; 5 policies × 3 seeds each — 96 runs total.
- Predictive protection (`predictiveBlocking`): learn per-source cadence and
  pre-block BE before predicted bursts (code added as `9a92dc1`).
- Result: VO mean/P95/delivery were policy-invariant in all cells (delivery
  identical to the 3rd decimal; delay spread ≤ noise ≈ ±3%); predictive blocking
  moved nothing and regressed guarded (+11% mean) → reverted (`6189876`).
- Loss attribution in every cell: VO `retryLimit` = 0, `queueOverflow` = 0; all VO
  MAC drops are RX-side `incorrectlyReceived`.

### 2.3 P1 — hotspot (S1) design

`[Config _hotspot3]` (heavy ini): nodes 1–3 (which enter the highway immediately
after the crash node) run `CritPacketSender` at `exponential(4ms)` / 1200 B for
the whole run ≈ 2.4 Mb/s offered each, on top of the normal netload profile.
Effect: ~3× channel capacity of offered airtime concentrated in three senders.
Runnable configs: `{plain, edca_only, edca_v2x_vo_{stable,guarded,emergency}}_hotspot_{low,medium,high}`,
5 seeds-worth, 3 seeds per config (recognizable pitfall fixed in `c4467cf`:
`_hotspot3` must precede `_netload_*` in `extends` — first matching assignment wins).

## 3. Results

### 3.1 Confirmation, heavy hotspot_high (3 policies, 3 seeds each)

| config | VO mean (ms) | VO P95 (ms) | VO incorrectRx | delivery (rx/alert) | BE-from-crash mean (ms) |
|---|---|---|---|---|---|
| plain_hotspot_high | 4.54 | 18.45 | (not classified) | 9.67 | 1.5 |
| edca_only_hotspot_high | 4.45 | 19.96 | 25.2k | 9.62 | 1453 (AC_BE starvation) |
| **edca_v2x_vo_emergency_hotspot_high** | **2.78 (−39%)** | **14.56 (−21%)** | **17.8k (−30%)** | 9.83 | 3.3 |

(Values reconciled 2026-08-16 against `context/eval-kpis/highway_heavy_hotspot/`;
the archived summary is authoritative wherever this note's prose differs.)

Per-seed consistency (VO P95, ms): plain [16.1, 19.4, 19.9], edca [20.5, 20.7,
18.7], emergency [11.8, 16.0, 15.9] — emergency wins in every seed.
Sanity: hotspot nodes each transmitted ≈17.1k packets; total BE TX ≈71.7k
(vs ≈22.2k without hotspot); VO logical alerts = 1500 per run.

### 3.2 Full hotspot campaign (5 policies x 3 netloads x 3 seeds; 45 runs)

3-seed means; VOirx = VO incorrectlyReceived (decode-under-collision loss);
BEdropBlk / BEgrantSup = emergency preemption counters; BEc = BE-from-crash delay.

#### hotspot_high (headline)

| policy | VO mean (ms) | VO P95 (ms) | VO rx/alert | VOirx | BEc mean (ms) | BEdropBlk | BEgrantSup |
|---|---|---|---|---|---|---|---|
| plain | 4.540 | 18.45 | 9.670 | (unclassified) | 1.548 | 0 | 0 |
| edca | 4.448 | 19.96 | 9.624 | 25.2k | 1453 | 0 | 0 |
| stable | 4.608 | 21.04 | 9.636 | 25.4k | 1386 | 0 | 0 |
| guarded | 4.439 | 20.04 | 9.689 | 25.1k | 981 | 0 | 0 |
| **emergency** | **2.781** | **14.56** | **9.835** | **17.8k** | **3.335** | 16.1k | 998 |

Per-seed VO P95 (ms): plain [16.1, 19.4, 19.9]; edca [20.5, 20.7, 18.7];
stable [21.5, 22.8, 18.8]; guarded [19.8, 19.9, 20.4]; emergency [11.8, 16.0, 15.9].

#### Dose-response: emergency vs plain by netload (3-seed means)

| netload | VO burst profile | VO mean gain | VO P95 gain |
|---|---|---|---|
| high | 20 ms x 8 copies (quasi-continuous) | **-39%** | **-21%** |
| medium | 75 ms x 4 copies | +10% | +5% |
| low | 120 ms x 3 copies | +16% | +0% |

The gain exists only when the alert stream is dense enough that protection
stays armed for most of the crash window: emergency blocks are re-armed on
every decoded copy, and at a 20 ms burst period the blocked duty cycle is
near-continuous (16.1k BE frames dropped/suppressed), so hotspot queues never
re-flood the arena. At 75/120 ms periods the block duty cycle falls to a
third or less, hot CBR traffic refills the gaps, and VO delay is again set by
collision physics, not by policy. BEc starvation under edca/stable/guarded
(1.0-1.5 s mean for packets that eventually leave) vs 3.3 ms under emergency
shows the same duty-cycle effect from the BE side.

Natural-high control, same seeds without hotspot (policy-invariant as in P2):
VO mean 0.952-0.998 ms and VO rx/alert 9.954 for all five policies.

## 4. Interpretation

1. The uniform-load invariance (P2) held in every cell tested, including past
   channel-collapse load.
2. The reappearance prediction (P1) is **confirmed**: under hotspot load the
   emergency mode recovers ~40% of VO mean delay and ~23% of VO P95, and cuts
   collision losses (incorrectRx) by ~30% — with results consistent per seed.
3. VO delivery remains range-limited (~9.6–9.8 copies per alert of ~10 in-range
   neighbors): protection recovers *latency and integrity*, not reach.
4. Side finding worth citing: under pure EDCA + hotspot, crash-node BE suffers
   AC_BE queueing starvation (mean ≈ 1.4 s for delivered packets); emergency's
   drop-while-blocked keeps delivered-BE delay at ≈ 3.3 ms — a robustness
   argument for emergency under extreme contention, beyond VO itself.
5. Cost ladder is preserved under hotspot: the more aggressive the protection,
   the more BE is suppressed/dropped (blocked-drop counters in raw scalars).

### What this does *not* show

- That protection helps VO under uniform load (it does not — P2 stands);
- That emergency is free: its VO gain is bought with blocked/dropped BE;
- Statistical significance beyond ±few % (n=3 seeds per cell); the hotspots
  were placed by spawn order (nodes 1–3), not by RSS map.

## 5. Reproducibility

- Scenario: `veins_qos/simulations/veins_inet_highway_heavy` (100 vehicles),
  70 s limit, crash window 30–60 s, multicast 224.0.0.1, 802.11p 5.9 GHz 10 MHz.
- Commands: `./run -u Cmdenv -c <config> -r 0-2 --repeat=3` from that directory,
  with `veins_launchd` on port 9999; branch + commits listed above.
- Raw traces: `veins_inet_highway_heavy/results/*hotspot*.sca/.vec` (this machine);
  natural matrices: rest of `results/`.
- Dashboard (live): `http://localhost:8050` (light+heavy), 8051 (stress).
