# Dissertation Writing Roadmap

**Primary short-paper source:** `../SBESC-2026-Paper/text.tex` (latest, condensed, expanded discussion)
**Secondary short-paper source:** `../ETFA-2026---Paper/text.tex`
**Technical source of truth:** `../veins-inet-qos/veins_qos/`
**Reviewer feedback:** `../SBESC-2026-Paper/DSD2026_REVIEW.md` (DSD 2026 reviews — address these in the dissertation)
**Status:** Repo cleaned (build/ workflow, Overleaf-ready), title/metadata pivoted. **Pivoted:** Resumo/Abstract, Introduction, Background, Related Work, System Model, Implementation, Evaluation, and Conclusion (`chapters/6-chapter.tex`).

> Do not rewrite the remaining legacy chapters until explicitly requested. Use this roadmap and `context/` when planning future edits.

---

## Build

- `./compile.sh` → `build/main.pdf` (persistent `build/` folder, gitignored)
- `./compile.sh clean` → removes `build/` and stray root artifacts
- Overleaf: sync the git repo as-is; `main.tex` at root compiles directly (`.latexmkrc` is Overleaf-safe, biber autodetected)

## Chapter alignment

Port from SBESC sections first (tighter prose, post-review); fall back to ETFA where SBESC condensed too much (e.g., DiffServ RFC background).

| Chapter | File | Target content | Port from | Legacy content to remove |
|---------|------|----------------|-----------|--------------------------|
| Intro | `chapters/0-Intro.tex` | **Done** — crash-aware QoS question, objectives, five MAC policies, contributions | SBESC §I | (removed) |
| Background | `chapters/1-chapter.tex` | **Done** — 802.11p, DCF, EDCA, DSCP/EF path, multicast limits, DCC contrast, simulation toolchain (plan: `context/background-chapter-plan.md`) | SBESC §II-A + ETFA §Background + `context/reference-notes.md` | (removed) |
| Related Work | `chapters/2-chapter.tex` | **Done** — stronger MACs, contention dynamics, adaptive EDCA/DCC, short TSN/OFDMA contrast (plan: `context/related-work-chapter-plan.md`) | SBESC §II-B + `context/reference-notes.md` | (removed) |
| System Model | `chapters/3-chapter.tex` | **Done** — highway multicast, BE/VO two-class model, crash timeline, five policies, three-mode controller (plan: `context/system-model-chapter-plan.md`) | SBESC §III-A/B + ETFA §System Model | (removed) |
| Implementation | `chapters/4-chapter.tex` | **Done** — OMNeT++ 6.1 / INET 4.5.4 / Veins modules, `V2xHcf`/`V2xEdcaFsmController`, artifact mapping table (plan: `context/implementation-chapter-plan.md`) | SBESC §III-C | (removed) |
| Evaluation | `chapters/5-chapter.tex` | **Done** — regime-conditional: uniform-load invariance (light+heavy) + hotspot VO gain + BE cost; fig_01/05/06/07/08/09 (plan: `context/evaluation-chapter-plan.md`) | post-fix KPI archive `context/eval-kpis/` | (legacy Preliminary Results removed earlier; supersedes SBESC §IV numbers) |
| Conclusion | `chapters/6-chapter.tex` | **Done** — conditional takeaway (marking as default, blocking as event-triggered escalation); no Work Plan/Schedule (plan: `context/conclusion-chapter-plan.md`) | SBESC §V | DQ-WiFi work-plan phases / timeline |

## SBESC-only discussion material to absorb (post-DSD-review)

These points were added in the SBESC rewrite in response to DSD 2026 reviews and must appear in the dissertation Evaluation/Discussion:

1. **Event-triggered, not always-on** — adaptive blocking is an escalation level, harmful when armed under low channel stress (light-density sweep as gating test).
2. **Plain-policy sampling caveat** — under `plain`, BE and VO statistics differ because the traffic processes differ (100 senders/70 s vs 1 sender/30 s window, different payloads), not because of MAC treatment; only within-class cross-policy comparisons are controlled.
3. **3GPP TS 22.186 25 ms budget framing** — absolute VO tails are far below the platooning latency bound; claim MAC-level tail shaping under synthetic saturation, not application-level safety benefit. Cite `ts22186`.
4. **Spatial BE unfairness** — the BE penalty concentrates near the crash source (protection armed by overheard VO frames); pooled averages understate worst-affected vehicles.
5. **DoS risk of VO-triggered suppression** — unauthenticated VO frames could keep neighbors blocking; deployment prerequisites are authentication, rate limiting, plausibility checks. Bounded by finite windows (20–80 ms max continuous block).
6. **Coarse BE class as worst-case bound** — treating all BE as suppressible overestimates acceptable aggression; real stacks need finer classes.
7. **Limitations** — 3 seeds, no CIs/significance tests; single crash source; simplified PHY (no fading/shadowing, free-space + binary obstacle); no DCC/adaptive-EDCA baseline; fixed profiles not individually ablated.

## Five MAC policies (must stay consistent)

1. `plain` — DCF, single 128-packet queue, no classifier
2. `edca_only` — DSCP 46 → AC_VO; queues BK/BE/VI/VO 128/128/64/32, AIFSN 7/3/2/2, cwMin 15/15/7/3, cwMax 1023/1023/15/7
3. `edca_v2x_vo_stable` — sustained protection: block 15 ms, max continuous 80 ms, guard 5 ms, VO threshold 2
4. `edca_v2x_vo_guarded` — bounded suppression: block 4 ms, max continuous 20 ms, guard 4 ms, VO threshold 3
5. `edca_v2x_vo_emergency` — `emergencyPreemption=true`: block 10 ms, max continuous 60 ms, guard 5 ms, VO threshold 1; may drop BE

Controller modes: *listening* / *blocking* / *sending* (`V2xHcf` + `V2xEdcaFsmController`). Runnable configs: `<policy>_netload_<low|medium|high>` (15 total per density package).

## Key parameters (Table reference)

- Simulation time: **70 s**; crash: t=30 s, duration 30 s, node index 0
- Topology: 5 km highway, 3 lanes/direction, 120 km/h, SUMO/TraCI
- Radio: IEEE 802.11p, 5.9 GHz, channel 3, 10 MHz, 20 mW; free-space path loss, binary obstacle loss, −85 dBm sensitivity, 4 dB SNIR
- Load profiles: low BE 500 ms/200 B, VO 120 ms/150 B ×3; medium BE 250 ms/320 B, VO 75 ms/180 B ×4; high BE 125 ms/420 B, VO 20 ms/260 B ×8
- Light: 10 vehicles, 3 seeds; Heavy: 100 vehicles, 3 seeds (hotspot overlay: heavy only, 3 seeds)

## Figures in `Figs/`

### Active (crash-aware pivot)

| File | Use |
|------|-----|
| `system_model_architecture.pdf` | System model (Ch4; also ETFA) |
| `event_timeline_cropped.pdf` | Crash timeline (Ch4; SBESC Fig. 1) |
| `fig_01_p95_delay_priority_gap_highway_{light,heavy}.pdf` | BE vs VO P95 gap, high load (Ch6; post-fix campaign) |
| `fig_05_mac_drop_attribution_high_load_highway_heavy.pdf` | MAC drop attribution, heavy/high (Ch6) |
| `fig_06_vo_delay_cdf_high_load_highway_heavy.pdf` | VO delay CDF, heavy/high (Ch6; post-fix campaign) |
| `fig_07_v2x_control_actions_by_load_highway_heavy.pdf` | Controller actions by load, heavy (Ch6) |
| `fig_08_hotspot_vo_delay_by_policy_highway_heavy.pdf` | Hotspot VO mean/P95 by policy (Ch6) |
| `fig_09_hotspot_vo_p95_by_load_highway_heavy.pdf` | Hotspot VO P95 dose-response (Ch6) |
| `plain_class_p95.{tex,pdf}` | Removed 2026-08-16 (measurement-review figure; never referenced) |

### Legacy (delete when the referencing chapter is rewritten)

All legacy raster figures were removed 2026-08-16: `fsm_simple.pdf`, `delay.pdf`,
`Topology.png`, `delay.png`, `classifier.png`, `mymodel.png`, `upperframe.png`,
`lowerframe.png`, `noqos.png`, `edca_only.png`, `reservaonly.png`, `both.png`,
`carcrashonly.png`, `plain_class_p95.{tex,pdf}` (verified unreferenced in all LaTeX
sources before removal).

## Suggested writing order

1. ~~Abstract + Resumo (beforetext)~~ — done (regime-conditional headline: VO flat ~2.2 ms under uniform Poisson; emergency −39%/−21% VO gain under hotspot dense bursts; protection-versus-cost frontier)
2. ~~Introduction (Ch0)~~ — done (SBESC §I + research question, scope, objectives)
3. ~~Background (Ch1)~~ — done (full rewrite; figure placeholders pending artwork)
4. ~~Related Work (Ch2)~~ — done (stronger MACs, dynamics, adaptive EDCA/DCC, short TSN/OFDMA)
5. ~~System Model (Ch3)~~ — done (SBESC §III-A/B + ETFA System Model structure)
6. ~~Implementation (Ch4)~~ — done (SBESC §III-C + code module map)
7. ~~Evaluation (Ch5 file / prints as Ch6)~~ — done (regime-conditional structure: headline → uniform-load invariance → hotspot gain → BE cost → eight discussion subsections)
8. ~~Conclusion (Ch6 file / prints as Ch7)~~ — done (SBESC §V; Work Plan deleted)
9. Proofread against `veins_qos/AI_CONTEXT.md`, SBESC paper, and `DSD2026_REVIEW.md`

## Headline results (heavy density, high load, 3-run means; measurement-fix campaign `5b0f584`)

| Policy | VO mean / P95 / jitter (ms) | BE mean / P95 (ms) | crash BE P95 (ms) | VO RX/alert | BE RX/TX |
|--------|-----------------------------|--------------------|-------------------|-------------|----------|
| plain | 0.991 / 2.249 / 1.024 | 0.387 / 0.511 | 0.631 | 9.95 | 8.06 |
| edca_only | 0.994 / 2.242 / 1.018 | 0.389 / 0.524 | 0.772 | 9.95 | 8.09 |
| stable | 0.988 / 2.245 / 1.026 | 3.696 / 30.491 | 13.763 | 9.95 | 7.61 |
| guarded | 0.998 / 2.241 / 1.029 | 0.896 / 3.889 | 3.865 | 9.95 | 7.66 |
| emergency | 0.952 / 2.211 / 0.979 | 0.432 / **0.369** | **0.435** | 9.95 | 6.93 |

- Voice P95 is ~2.2 ms on every policy (alert age; 5 ms repeat gap). No −49% Voice win.
- Policy contrast is Best Effort cost: stable 30 ms fleet P95, guarded 3.9 ms, emergency 0.37 ms via preemption.
- MAC drops (×10³): plain 16.2, edca 15.6, stable 19.6, guarded 19.8, emergency 16.0 (2.53×10³ explicit BE drops). Overflow is zero.
- Light density, high load vs plain: Voice P95 unchanged (~2.08 ms); stable BE P95 +11044%; emergency BE P95 −15.5%.

Do not cite results not present in the simulation artifact or the SBESC/ETFA papers. Conference papers still report the pre-fix campaign.
