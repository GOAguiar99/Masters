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
- Roadmap: Setup → Metrics → Headline → Hotspot (primary) → Uniform null → Cost → Discussion → Summary.

### Experimental Setup (`sec:eval:setup`)

- Light 10 veh / 3 seeds; heavy 100 veh / 3 seeds; 5×3 matrix + hotspot overlay (15×3 = 45 seeded runs).
- Cross-ref `tab:impl:parameters`; artifact cite; high-load stress quantification from SBESC.

### Metrics and Aggregation (`sec:eval:metrics`)

- E2E delay, P95, jitter; VO RX/alert; BE RX/TX; MAC drops; controller actions.
- Arithmetic means over seeds; no CIs / no significance tests.

### Headline (`sec:eval:headline`)

- Conditional claim once; **tab:eval:glance** map; regime contrast **fig_10** only (dose fig_09 lives under hotspot).
- Early caveat: 2.2 ms is the high-load 5 ms gap; low/medium quantize to ~4.6–4.9 ms.
- Relative-% vs plain unless noted; VO MAC-drop % vs EDCA.

### Hotspot primary (`sec:eval:hotspot`)

- `hotspot_high` win table + **fig_08**; dose table + **fig_09**; mechanism (preemption, starvation, dropping vs deferring).
- Scale bridge 22k→72k BE TX; VO drops ~3.7k→~25k before policy separation.

### Uniform null (`sec:eval:light`)

- Short contrast: light table (VO % + absolute BE P95 ms); heavy QoS table + dual-panel **fig_01**.
- No VO CDF / drop-attr floats; drop-attr reduced to one prose sentence.

### Cost (`sec:eval:cost`)

- Hotspot pricing first (**fig_04**); uniform controller / BE ladder as short coda (**fig_07**).
- `tab:eval:heavy_p95` is **BE-only** (fleet + crash-node); VO rows removed.

### Discussion (`sec:eval:discussion`)

Seven mandatory points; cross-ref hotspot/tables instead of re-quoting −39%/−21%/2.2 ms every subsection.

### Chapter summary (`sec:eval:summary`)

- Conditional takeaway; bridge to Conclusion.

---

## Figures and tables

**Kept figures (delay/jitter + VO-loss focus):**
| Float | Source |
|-------|--------|
| Heavy P95 gap (uniform null) | `Figs/fig_01_p95_delay_priority_gap_highway_heavy.pdf` |
| Hotspot VO by policy | `Figs/fig_08_hotspot_vo_delay_by_policy_highway_heavy.pdf` |
| Hotspot VO P95 by load | `Figs/fig_09_hotspot_vo_p95_by_load_highway_heavy.pdf` |
| Regime contrast (netload vs hotspot) | `Figs/fig_10_regime_vo_p95_contrast_highway_heavy.pdf` |
| VO gain vs BE cost | `Figs/fig_04_vo_gain_vs_be_cost_highway_heavy.pdf` |
| V2X control load sweep | `Figs/fig_07_v2x_control_actions_by_load_highway_heavy.pdf` |

Uncited after 2026-09 focus pass: fig_05 drop-attribution, fig_06 VO CDF (invariance already in tables + fig_01).


**Tables:**
| Float | Source |
|-------|--------|
| Results at a glance | `tab:eval:glance` (headline map) |
| Light gating (VO % + absolute BE P95) | SBESC light high vs plain |
| Heavy delay/jitter/RX | SBESC panel (a) / `tab:eval:heavy_qos` |
| Hotspot win + dose | `tab:eval:hotspot`, `tab:eval:hotspot_dose` |
| Heavy BE P95 ladder (BE-only) | `tab:eval:heavy_p95` (VO rows removed 2026-09 clarity) |
| Heavy controller actions | SBESC panel (b) / `tab:eval:heavy_ctrl` |

Removed from chapter (prose only): `tab:eval:heavy_drop_attr` — VO drops ~3.7×10³, no policy separation.

Trimmed / optional: audit heatmaps fig_02–03; light fig_05–07 when counters are empty.

---

## Numbers that must match exactly (heavy, high load, 3-run means)

| Policy | VO mean / P95 / jit (ms) | BE mean / P95 (ms) | VO RX/alert | BE RX/TX |
|--------|--------------------------|--------------------|-------------|----------|
| plain | 0.575 / 1.290 / 0.321 | 27.589 / 57.367 | 9.068 | 6.153 |
| edca_only | 0.433 / 0.896 / 0.193 | 54.760 / 155.857 | 9.904 | 6.147 |
| stable | 0.469 / 1.155 / 0.261 | 59.434 / 144.314 | 9.826 | 5.534 |
| guarded | 0.443 / 0.960 / 0.207 | 74.938 / 174.401 | 9.778 | 3.644 |
| emergency | **0.282 / 0.461 / 0.047** | 60.664 / 98.663 | 9.912 | 5.021 |
