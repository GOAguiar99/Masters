# Dissertation Writing Roadmap

**Source of truth:** `../veins-inet-qos/veins_qos/`  
**Short paper reference:** `../ETFA-2026---Paper/text.tex`  
**Status:** Context/bibliography infrastructure ready; **chapter text not yet pivoted** (still legacy DQ-WiFi draft)

> Do not rewrite `chapters/*.tex` or abstracts until explicitly requested. Use this roadmap and `context/` when planning future edits.

---

## Chapter alignment

| Chapter | File | Target content | Legacy content to remove |
|---------|------|----------------|--------------------------|
| Intro | `chapters/0-Intro.tex` | Crash-aware QoS question, five MAC policies, contributions | DQ-WiFi, TAS, beacon FSM, deterministic claims |
| Background | `chapters/1-chapter.tex` | 802.11p, DCF, EDCA, DSCP path, contention limits | Long TSN-only outline (commented blocks OK to delete) |
| Related Work | `chapters/2-chapter.tex` | EDCA/V2X QoS surveys + contrast papers; short TSN/OFDMA subsection | TSN-primary narrative |
| System Model | `chapters/3-chapter.tex` | Highway multicast, BE/VO, crash timeline, five policies | Reserva, TAS gates, analytical TSN delay |
| Implementation | `chapters/4-chapter.tex` (part 1) | OMNeT++/INET/Veins modules, V2xHcf FSM | UdpCritApp, EdcaFsmController, classifier PNGs |
| Evaluation | `chapters/4-chapter.tex` (part 2) or split | ETFA results tables, fig_06 CDF | Legacy noqos/edca/reserva plots |
| Work plan | `chapters/5-chapter.tex` | SBESC2025 + ETFA submission + thesis completion | DQ-WiFi phase descriptions |

## Five MAC policies (must stay consistent)

1. `plain` — DCF, single queue, no classifier
2. `edca_only` — DSCP 46 → AC_VO
3. `edca_v2x_vo_stable` — bounded BE suppression
4. `edca_v2x_vo_guarded` — tighter suppression windows
5. `edca_v2x_vo_emergency` — BE drop + preemption

## Key parameters (Table reference)

- Simulation time: **70 s**
- Crash: t=30 s, duration 30 s, node index 0
- High load: BE 125 ms / 420 B; VO 20 ms / 260 B, repeat 8
- Light: 10 vehicles, 5 seeds; Heavy: 100 vehicles, 3 seeds

## Figures in `Figs/`

| File | Use |
|------|-----|
| `system_model_architecture.pdf` | System model |
| `event_timeline_cropped.pdf` | Crash timeline |
| `fig_06_vo_delay_cdf_high_load_highway_heavy.svg` | VO delay CDF (convert to PDF for pdflatex if needed) |

## Suggested writing order

1. Abstract + Resumo (beforetext)
2. Introduction (Ch0)
3. Background (Ch1) — port from ETFA §Background
4. Related Work (Ch2) — port ETFA §Related Work + shorten TSN contrast
5. System Model (Ch3) — port ETFA §System Model
6. Implementation + Evaluation (Ch4)
7. Work plan + conclusion (Ch5)
8. Proofread against `veins_qos/AI_CONTEXT.md` and ETFA paper

## Headline results (heavy high-load)

- Emergency VO P95 ≈ 0.46 ms vs EDCA 0.90 ms vs plain 1.29 ms
- Light density: only emergency improves VO vs plain at high load
- Bounded stable/guarded can harm BE without helping VO when channel is not congested

Do not cite results not present in the simulation artifact or ETFA paper.
