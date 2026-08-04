# System Model chapter plan (`chapters/3-chapter.tex`, prints as Chapter 4)

**Goal:** replace the legacy DQ-WiFi / AP-centric / worst-case-analysis draft with a crash-aware System Model that defines the decentralized highway multicast setting, two-class BE/VO traffic, five MAC policies, three-mode adaptive controller, crash timeline, assumptions, and tool-agnostic model parameters.

**Status of this file:** implemented in `chapters/3-chapter.tex` (August 2026); reviewed against [`scientific-paper-structure.md`](scientific-paper-structure.md) to strip Implementation/Evaluation leakage.

**Separation authority:** always apply [`scientific-paper-structure.md`](scientific-paper-structure.md). SBESC merges System Model + Implementation; the dissertation must **not**.

---

## Current state (legacy — remove)

[`chapters/3-chapter.tex`](../chapters/3-chapter.tex) is the DQ-WiFi draft:

- AP / DQC / beacon-driven coordination, bandwidth reservation
- Old FSM: ACTIVE / LISTENING / BLOCKED with cycle phases
- Worst-case delay analysis (`vardakas2007end`, cycle misalignment bounds)
- Legacy figures: `Topology.png`, `fsm_simple.pdf`, `delay.png`
- Static, infrastructure-centric assumptions (clock sync, no mobility)

**Primary port source:** SBESC §III-A/B (`../SBESC-2026-Paper/text.tex`) — network/traffic/event prose + MAC policy / three-mode controller detail (**not** §III-C Implementation).

**Secondary expansion:** ETFA §System Model (`../ETFA-2026---Paper/text.tex`) — separate Network / Traffic / QoS / Event / Assumptions subsections; architecture + stack-path figures.

**Technical truth for parameter values:** `../veins-inet-qos/veins_qos/` + [`code-overview.md`](code-overview.md). Prefer code for knobs; do not name modules in Ch3.

**Scope boundary (strict):** System Model only — *what* the system is. Defer to Implementation: OMNeT++/INET/Veins/SUMO, module/class names, config naming, artifact cite. Defer to Evaluation: seeds, CIs, KPIs, results.

---

## Citation requirements

- Every substantive paragraph should normally contain one or more citations from the inventory below, or an explicit cross-ref to Background / Related Work.
- Prefer Background cross-refs for DiffServ/DCF/EDCA mechanics already taught; do not re-teach them.
- Use dissertation keys (map paper aliases per [`bibliography-guide.md`](bibliography-guide.md)).
- Never invent KPIs, analytical delay bounds, or features absent from `veins_qos/`.

### Must cite (System Model)

`jiang2008ieee80211p`, `IEEE80211`, `IEEE80211e_2005`, `RFC8325_WiFi_QoS`, `RFC3246_EF_PHB`, `RFC9119_Multicast_IEEE802_Wireless`, `etsi_dcc_2018`

### Optional light cross-cites

`RFC2474_DSField`, `RFC2475_DiffServ_Architecture`, `RFC4594_DiffServ_Service_Classes`, `mangold2003QoS`, `kong2004EDCA`, `kosekszott2012What`, `bianchi2000DCF`, `Continuous_Backoff_Freezing_Li`, `etsi_en_302663`

### Do **not** cite in System Model (belong elsewhere)

| Key | Belongs in |
|-----|------------|
| `aguiar2026_veins_qos`, `varga2008omnetpp`, `inet_framework`, `veins_sommer2011`, `lopez2018sumo`, `inet_ideal_obstacle_loss` | Implementation |
| `ts22186` | Evaluation / Discussion |
| `vardakas2007end`, `veins_inet_qos_2026`, `IEEE_80211p_Survey` | Deprecated / legacy |
| TSNCtl, PRP-MAC, CFC-MAC, NR-V2X, SkipCCH, adaptive EDCF, TSN/OFDMA, `11288825` | Related Work |

---

## Section architecture

Keep stable label `\label{chap:sysmodel}`.

### Opening (~0.5 page)

- Restate the residual gap from Related Work: local, event-triggered BE suppression with explicit DSCP 46→Voice on 802.11p OCB, no sync/infra/TSN.
- Emphasize tool-agnostic System Model; forward-ref Implementation and Evaluation (**no** artifact/simulator cite).
- Chapter roadmap: Network → Traffic → QoS/policies → Event → Assumptions → Model parameters.

### 4.1 Network Model (`sec:sys:network`)

- Decentralized VANET; no AP/RSU/central coordinator (`jiang2008ieee80211p`).
- Shared IEEE 802.11p OCB; one-hop multicast (`RFC9119_Multicast_IEEE802_Wireless`).
- PHY fixed across policies → isolate queueing/contention (`IEEE80211`).
- Figure: `Figs/system_model_architecture.pdf`.

### 4.2 Traffic Model (`sec:sys:traffic`)

- Synthetic two-class abstraction (not CAM/DENM / full ITS).
- All vehicles: periodic BE, DSCP 0.
- One crash source: DSCP 46 overlay; keeps generating BE during alerts (`RFC3246_EF_PHB`).
- Load profiles referenced forward to params table.

### 4.3 QoS Model and MAC Policies (`sec:sys:qos`)

- Two classes only; DSCP 46 → Voice UP (`RFC8325_WiFi_QoS`); cross-ref `sec:bg:dscp`.
- Stack-path figure (tabular layers).
- Five policies with full knobs (plain / edca_only / stable / guarded / emergency).
- Three-mode controller: *listening* / *blocking* / *sending*.
- stable/guarded defer BE; emergency may drop BE; no channel reservation (`IEEE80211e_2005`, `kosekszott2012What`).
- Controller FSM figure (tabular).

### 4.4 Event Model (`sec:sys:event`)

- Three phases: normal → crash window (t=30 s, 30 s, designated node stops) → recovery.
- Lingering adaptive protection until window + guard expire.
- Figure: `Figs/event_timeline_cropped.pdf`.

### 4.5 Assumptions and Scope (`sec:sys:scope`)

- Minimal: one crash source; two-class; no infra/TSN gating.
- DCC not part of the model (`etsi_dcc_2018`).
- Free-space + binary obstruction + static SNIR; no fading/shadowing (**no** class name `IdealObstacleLoss`).
- No deterministic / worst-case latency claims.

### 4.6 Model Parameters (`sec:sys:params`)

- Tool-agnostic parameter table (topology, radio, densities, load profiles, MAC knobs).
- **Exclude:** simulator/toolchain, seeds, config naming (`netload_*` as code identifiers), artifact cite.
- Bridge sentence to Implementation / Evaluation only.

---

## Figures and tables

| Float | Source | Notes |
|-------|--------|-------|
| Architecture | `Figs/system_model_architecture.pdf` | Real figure |
| Event timeline | `Figs/event_timeline_cropped.pdf` | Real figure |
| Stack path | Tabular in chapter | App→Net/QoS→MAC→PHY |
| Controller FSM | Tabular in chapter | listening↔blocking↔sending |
| Params table | Abstract model parameters | ABNT caption/`\fonte`; no simulator rows |

Legacy figures (`Topology.png`, `fsm_simple.pdf`, `delay.png`) are no longer referenced after rewrite.

---

## Policy knobs (must match exactly)

| Policy | Block / max cont. / guard / thr | Notes |
|--------|----------------------------------|-------|
| `plain` | — | Single DCF queue 128; no classifier |
| `edca_only` | — | DSCP 46→AC_VO; queues 128/128/64/32; AIFSN 7/3/2/2; cwMin 15/15/7/3; cwMax 1023/1023/15/7 |
| `stable` | 15 / 80 / 5 ms, thr 2 | Sustained protection |
| `guarded` | 4 / 20 / 4 ms, thr 3 | Bounded suppression |
| `emergency` | 10 / 60 / 5 ms, thr 1 | Emergency preemption; may drop BE |

---

## Remove list

- All DQ-WiFi / DQC / reservation / beacon scheduling prose
- Old ACTIVE/LISTENING/BLOCKED cycle semantics
- Entire worst-case delay analysis section and equations
- Citations to `vardakas2007end` from this chapter
- Cross-refs to deleted `sec:fsm`, `sec:analysis`, `sec:listening`, `sec:topology`, `sec:assumptions` (legacy labels)
- Simulator / framework / module / artifact / seed leakage (see [`scientific-paper-structure.md`](scientific-paper-structure.md) checklist)
