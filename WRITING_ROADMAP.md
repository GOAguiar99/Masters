# Dissertation Writing Roadmap

**Primary short-paper source:** `../SBESC-2026-Paper/text.tex` (latest, condensed, expanded discussion)
**Secondary short-paper source:** `../ETFA-2026---Paper/text.tex`
**Technical source of truth:** `../veins-inet-qos/veins_qos/`
**Reviewer feedback:** `../SBESC-2026-Paper/DSD2026_REVIEW.md` (DSD 2026 reviews — address these in the dissertation)
**Status:** Repo cleaned (build/ workflow, Overleaf-ready), title/metadata pivoted. **Pivoted so far:** Resumo/Abstract (`beforetext/beforetext.tex`), Introduction (`chapters/0-Intro.tex`), and Background (`chapters/1-chapter.tex`). **Still legacy DQ-WiFi draft:** `chapters/2-chapter.tex` through `5-chapter.tex`.

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
| Related Work | `chapters/2-chapter.tex` | TSNCtl/PRP-MAC/CFC-MAC/NR-V2X contrast, backoff freezing, SkipCCH, adaptive EDCA + DCC positioning; short TSN/OFDMA subsection | SBESC §II-B | TSN-primary narrative |
| System Model | `chapters/3-chapter.tex` | Highway multicast, BE/VO two-class model, crash timeline, five policies, three-mode controller | SBESC §III | Reserva, TAS gates, analytical TSN delay |
| Implementation | `chapters/4-chapter.tex` (part 1) | OMNeT++ 6.1 / INET 4.5.2 / Veins modules, `V2xHcf`/`V2xEdcaFsmController`, artifact mapping table | SBESC §III-C | UdpCritApp, EdcaFsmController, classifier PNGs |
| Evaluation | `chapters/4-chapter.tex` (part 2) or split | Light sweep + heavy stress tables, fig_06 CDF, full discussion (see below) | SBESC §IV | Legacy noqos/edca/reserva plots |
| Work plan / Conclusion | `chapters/5-chapter.tex` | SBESC2025 prior work + DSD→SBESC 2026 submission trail + thesis completion; conditional takeaway (marking as default, blocking as event-triggered escalation) | SBESC §V | DQ-WiFi phase descriptions |

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
- Light: 10 vehicles, 5 seeds; Heavy: 100 vehicles, 3 seeds

## Figures in `Figs/`

### Active (crash-aware pivot)

| File | Use |
|------|-----|
| `system_model_architecture.pdf` | System model (used in ETFA; unused in SBESC but useful for the thesis) |
| `event_timeline_cropped.pdf` | Crash timeline (SBESC Fig. 1) |
| `fig_06_vo_delay_cdf_high_load_highway_heavy.pdf` | VO delay CDF, heavy/high load (SBESC Fig. 2; PDF, Overleaf-ready) |

### Legacy (delete when the referencing chapter is rewritten)

| File(s) | Referenced by |
|---------|---------------|
| `Topology.png`, `fsm_simple.pdf`, `delay.png`, `delay.pdf` | `chapters/3-chapter.tex` |
| `classifier.png`, `mymodel.png`, `upperframe.png`, `lowerframe.png` | `chapters/4-chapter.tex` |
| `noqos.png`, `edca_only.png`, `reservaonly.png`, `both.png`, `carcrashonly.png` | `chapters/4-chapter.tex` |

## Suggested writing order

1. ~~Abstract + Resumo (beforetext)~~ — done (leads with ~49% VO P95 reduction and protection-versus-cost frontier)
2. ~~Introduction (Ch0)~~ — done (SBESC §I + research question, scope, objectives)
3. ~~Background (Ch1)~~ — done (full rewrite; figure placeholders pending artwork)
4. Related Work (Ch2) — port SBESC §II-B (includes adaptive EDCA + DCC positioning) + shorten TSN contrast
5. System Model (Ch3) — port SBESC §III-A/B
6. Implementation + Evaluation (Ch4) — port SBESC §III-C + §IV including all discussion paragraphs
7. Work plan + conclusion (Ch5)
8. Proofread against `veins_qos/AI_CONTEXT.md`, SBESC paper, and `DSD2026_REVIEW.md`

## Headline results (heavy density, high load, 3-run means)

| Policy | VO mean / P95 / jitter (ms) | BE mean / P95 (ms) | VO RX/alert | BE RX/TX |
|--------|-----------------------------|--------------------|-------------|----------|
| plain | 0.575 / 1.290 / 0.321 | 27.6 / 57.4 | 9.07 | 6.15 |
| edca_only | 0.433 / 0.896 / 0.193 | 54.8 / 155.9 | 9.90 | 6.15 |
| stable | 0.469 / 1.155 / 0.261 | 59.4 / 144.3 | 9.83 | 5.53 |
| guarded | 0.443 / 0.960 / 0.207 | 74.9 / 174.4 | 9.78 | 3.64 |
| emergency | **0.282 / 0.461 / 0.047** | 60.7 / 98.7 | 9.91 | 5.02 |

- Emergency ≈ **−49% VO P95 vs EDCA** (0.896 → 0.461 ms)
- MAC drops (×10³): plain 281, edca 251, stable 340, guarded **485**, emergency 273 (with 22×10³ explicit BE drops)
- Light density, high load vs plain: emergency VO P95 **−37.6%**; EDCA/stable/guarded slightly *worse* VO; all inflate BE delay by orders of magnitude

Do not cite results not present in the simulation artifact or the SBESC/ETFA papers.
