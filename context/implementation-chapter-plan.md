# Implementation chapter plan (`chapters/4-chapter.tex`, prints as Chapter 5)

**Goal:** replace the legacy DQ-WiFi Implementation (and the DQ-WiFi Preliminary Results glued into the same file) with a crash-aware Implementation chapter that answers *how* the System Model was realized in OMNeT++/INET/Veins software—without Evaluation leakage.

**Status of this file:** implemented in `chapters/4-chapter.tex` (August 2026); expanded to dissertation depth from `veins-inet-qos/` module/NED/ini truth (host compounds, packet path, per-module parameters, policy wiring, scenario packages, instrumentation). Reviewed against [`scientific-paper-structure.md`](scientific-paper-structure.md) to keep System Model / Implementation / Evaluation separated.

**Separation authority:** always apply [`scientific-paper-structure.md`](scientific-paper-structure.md). SBESC merges System Model + Implementation in §III; the dissertation must **not**.

---

## Current state (legacy — remove)

[`chapters/4-chapter.tex`](../chapters/4-chapter.tex) is the DQ-WiFi draft:

- `UdpCritApp` / `UdpCollisionApp` (four criticality levels; not in `veins_qos/`)
- `EdcaFsmController` with ACTIVE / LISTENING / BLOCKED and bandwidth reservation (`activePeriod` / `listenPeriod` / `BEAperiodic`)
- Legacy figures: `classifier.png`, `upperframe.png`, `lowerframe.png`, `mymodel.png`
- A second chapter, Preliminary Results, with NOQOS / CRASH_QOS* profiles and invented delay tables

**Primary port source:** SBESC §III-C *Implementation and Scope* (`../SBESC-2026-Paper/text.tex`) — toolchain, artifact mapping table, instrumentation, scope.

**Secondary expansion:** ETFA Implementation (same modules); module truth from [`code-overview.md`](code-overview.md) + [`code-references.md`](code-references.md). Prefer code names/behavior over paper shorthand if they disagree.

**Already covered elsewhere — do not re-teach:**
- Toolchain motivation: Background `sec:bg:sim` (OMNeT++/INET/Veins/SUMO)
- Architecture, policies, FSM semantics, crash timeline, tool-agnostic params: System Model (`chapters/3-chapter.tex`)
- Cross-ref those; Implementation names modules, versions, configs, and integration hooks

**Scope boundary (strict):** Implementation only — *how* the system was built. Defer to Evaluation: seeds, CIs, KPI result tables, CDFs, discussion. Do not re-derive System Model algorithms.

---

## Citation requirements

- Every substantive paragraph should normally contain one or more citations from the inventory below, or an explicit cross-ref to Background / System Model.
- Prefer Background cross-refs for simulator motivation already taught; do not re-teach them.
- Use dissertation keys (map paper aliases per [`bibliography-guide.md`](bibliography-guide.md)).
- Never invent modules, hooks, or features absent from `veins_qos/`.

### Must cite (Implementation)

`aguiar2026_veins_qos`, `varga2008omnetpp`, `inet_framework`, `veins_sommer2011`, `lopez2018sumo`, `inet_ideal_obstacle_loss`, `RFC8325_WiFi_QoS`, `RFC3246_EF_PHB`, `IEEE80211e_2005`

### Optional light cross-cites

`IEEE80211`, `jiang2008ieee80211p`, `varga2010omnetpp`

### Do **not** cite in Implementation (belong elsewhere)

| Key / content | Belongs in |
|---------------|------------|
| `ts22186`, seed counts, CIs, KPI result tables, CDFs | Evaluation |
| Policy *semantics* re-derivation, crash timeline, abstract architecture | System Model (cross-ref) |
| TSNCtl, PRP-MAC, adaptive EDCA surveys | Related Work |
| `vardakas2007end`, `UdpCritApp`, reservation FSM, DQ-WiFi | Deprecated |

---

## Section architecture

Keep stable label `\label{chap:implementation}`.

### Opening

- Map Ch3 onto the Veins/INET artifact; version pins; roadmap; forward-ref Evaluation.

### Toolchain and repository (`sec:impl:toolchain`)

- Versions; directory layout table; attribution (Sommer; Bigge unused TransparentMobility).

### Host and scenario compounds (`sec:impl:host`)

- `VeinsInetCar`, `VeinsInetApplicationBase`, `Scenario` NED + TraCI manager.

### End-to-end packet path (`sec:impl:path`)

- App → UDP/IP → classifier → MAC/HCF → PHY → Crit RX KPIs; stack tabular figure.

### Application layer (`sec:impl:apps`)

- `CritPacketSender` / `CrashBurstApp` parameter and statistic tables; TraCI stop; ports 9001/9002.

### QoS classifier (`sec:impl:classifier`)

- `QosClassifier` + exact `.ini` binding.

### MAC (`sec:impl:mac`)

- `V2xIeee80211Mac` drop instrumentation; `V2xHcf` + FSM parameters and hooks tables.

### Policy wiring (`sec:impl:policies`)

- Exact `plain` / `edca_only` / adaptive `.ini` composition and knob table.

### Scenarios and matrix (`sec:impl:scenarios`)

- Light/heavy packages; SUMO; radio baseline; load overlays; 15 configs/package; build/run notes.

### Instrumentation (`sec:impl:instrumentation`)

- Signal table; `kpi_dashboard/` as analysis surface (no results).

### Scope (`sec:impl:scope`)

- Deliberate omissions; legacy packages; bridge to Evaluation.

---

## Figures and tables

| Float | Source | Notes |
|-------|--------|-------|
| Artifact mapping table | Port SBESC `tab:impl_map` | Required; ABNT caption/`\fonte` |
| Module-integration tabular | Author-made | App→Classifier→V2xHcf/EDCA→PHY |
| MAC integration hooks table | Author-made | Optional; gating / activation / drop |

Legacy figures (`classifier.png`, `upperframe.png`, `lowerframe.png`, `mymodel.png`, throughput PNGs) are no longer referenced after rewrite.

---

## Module / policy names (must match code)

| Role | Module / config |
|------|-----------------|
| BE app | `CritPacketSender` |
| VO crash app | `CrashBurstApp` |
| Classifier | `QosClassifier` |
| Adaptive HCF | `V2xHcf` + `V2xEdcaFsmController` |
| Instrumented MAC | `V2xIeee80211Mac` |
| Policies | `plain`, `edca_only`, `edca_v2x_vo_stable`, `edca_v2x_vo_guarded`, `edca_v2x_vo_emergency` |
| Config pattern | `<policy>_netload_<low\|medium\|high>` |

---

## Remove list

- All DQ-WiFi / reservation / `BEAperiodic` / ACTIVE–LISTENING cycle prose
- `UdpCritApp`, `UdpCollisionApp`, `EdcaFsmController`, four-level criticality
- Entire `\chapter{Preliminary Results}` and legacy KPI/throughput floats
- Cross-refs to deleted `sec:analysis`, legacy figure labels
- Deterministic / worst-case latency claims
- Seed counts, CI statements, result numbers, `ts22186` framing
