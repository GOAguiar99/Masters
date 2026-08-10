# Evaluation chapter plan (`chapters/5-chapter.tex`, prints as Chapter 6)

**Goal:** add a dissertation-depth Evaluation chapter that answers *whether* crash-triggered Voice obtains better service than Best Effort under contention and *at what cost*—without Implementation leakage or invented results.

**Status of this file:** implemented in `chapters/5-chapter.tex` (August 2026); Conclusion lives in `chapters/6-chapter.tex` (Work Plan deleted). Reviewed against [`scientific-paper-structure.md`](scientific-paper-structure.md).

**Separation authority:** always apply [`scientific-paper-structure.md`](scientific-paper-structure.md). Evaluation demonstrates performance; it must not re-describe modules/NED/`.ini` wiring (Implementation) or re-derive policies/FSM (System Model).

---

## Current state

- Implementation (`chapters/4-chapter.tex`) forwards to Evaluation and owns `tab:impl:parameters`.
- Legacy Preliminary Results removed from Ch4; Evaluation is a dedicated chapter.
- Conclusion lives in `chapters/6-chapter.tex` (crash-aware; no Work Plan).

**Primary port source:** SBESC §IV (`../SBESC-2026-Paper/text.tex`).

**Must absorb (post-DSD):** all seven discussion points in [`WRITING_ROADMAP.md`](../WRITING_ROADMAP.md).

**Technical truth for numbers:** only values present in SBESC/ETFA / artifact KPIs. Prefer SBESC tables. **Do not invent** CIs, significance tests, or unreported figures.

**Already covered elsewhere — cross-ref, do not re-teach:**
- Policies / FSM / timeline → System Model (`chap:sysmodel`)
- Modules, `.ini` wiring, parameter table → Implementation (`chap:implementation`, `tab:impl:parameters`)
- Toolchain motivation → Background (`sec:bg:sim`)

---

## Citation requirements

### Must cite (Evaluation / Discussion)

`aguiar2026_veins_qos`, `ts22186`, plus cross-refs to `tab:impl:parameters`, `chap:implementation`, `chap:sysmodel`.

### Optional light cross-cites

`IEEE80211e_2005`, `kosekszott2012What`, `Continuous_Backoff_Freezing_Li`, `veins_sommer2011`, `etsi_dcc_2018`

### Do **not** put in Evaluation

| Content | Belongs in |
|---------|------------|
| Module/class/NED walkthroughs | Implementation |
| Policy/FSM derivation, crash timeline definition | System Model |
| Invented KPIs, CIs, significance claims | Forbidden |
| Legacy DQ-WiFi NOQOS/CRASH_QOS* numbers | Deprecated |

---

## Section architecture

Keep label `\label{chap:evaluation}`.

### Opening

- Research question; protection-versus-cost; point to Implementation for how experiments are built.
- Roadmap: Setup → Metrics → Light → Heavy → Discussion → Summary.

### Experimental Setup (`sec:eval:setup`)

- Light 10 veh / 5 seeds; heavy 100 veh / 3 seeds; 5×3 matrix.
- Cross-ref `tab:impl:parameters`; artifact cite; high-load stress quantification from SBESC.

### Metrics and Aggregation (`sec:eval:metrics`)

- E2E delay, P95, jitter; VO RX/alert; BE RX/TX; MAC drops; controller actions.
- Arithmetic means over seeds; no CIs / no significance tests.

### Light-Density Sensitivity Sweep (`sec:eval:light`)

- Gating test; normalized table vs `plain_netload_high`.

### Heavy-Density Stress Results (`sec:eval:heavy`)

- QoS separation table; VO CDF (`Figs/fig_06_…`); MAC/controller panel; P95 ladder across loads.

### Discussion (`sec:eval:discussion`)

Seven mandatory points: event-triggered escalation; plain sampling caveat; `ts22186` framing; coarse BE class; spatial BE unfairness; DoS risk; limitations.

### Chapter summary (`sec:eval:summary`)

- Conditional takeaway; bridge to Conclusion.

---

## Figures and tables

**Kept figures (delay/jitter + VO-loss focus):**
| Float | Source |
|-------|--------|
| Heavy P95 gap | `Figs/fig_01_p95_delay_priority_gap_highway_heavy.pdf` |
| VO delay CDF | `Figs/fig_06_vo_delay_cdf_high_load_highway_heavy.pdf` |
| Drop attribution | `Figs/fig_05_mac_drop_attribution_high_load_highway_heavy.pdf` |

**Tables:**
| Float | Source |
|-------|--------|
| Light normalized | SBESC `tab:light_high_vs_plain` |
| Heavy delay/jitter/RX | SBESC panel (a) |
| Heavy VO loss | SBESC panel (b) VO incomplete / BE qdrop / totals |
| Heavy drop attribution BE/VO/unclassified | dashboard fig_05 (totals match SBESC) |
| Heavy controller actions | SBESC panel (b) |
| Heavy P95 ladder | SBESC `tab:heavy_high_load_p95` |
| Heavy drop rate × load | dashboard fig_02 cell values |
| Heavy VO RX × load | dashboard fig_03 cell values |

Trimmed figures (available in `Figs/` but not cited): light fig_01, fig_02–04, fig_07.

---

## Numbers that must match exactly (heavy, high load, 3-run means)

| Policy | VO mean / P95 / jit (ms) | BE mean / P95 (ms) | VO RX/alert | BE RX/TX |
|--------|--------------------------|--------------------|-------------|----------|
| plain | 0.575 / 1.290 / 0.321 | 27.589 / 57.367 | 9.068 | 6.153 |
| edca_only | 0.433 / 0.896 / 0.193 | 54.760 / 155.857 | 9.904 | 6.147 |
| stable | 0.469 / 1.155 / 0.261 | 59.434 / 144.314 | 9.826 | 5.534 |
| guarded | 0.443 / 0.960 / 0.207 | 74.938 / 174.401 | 9.778 | 3.644 |
| emergency | **0.282 / 0.461 / 0.047** | 60.664 / 98.663 | 9.912 | 5.021 |
