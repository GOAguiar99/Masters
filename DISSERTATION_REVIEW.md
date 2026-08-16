# Dissertation Review & Evaluation

> ⚠️ **SUPERSEDED (2026-08-16).** This review documents the **pre-measurement-fix** campaign
> (VO P95 0.896 → 0.461 ms, −49%). The dissertation has since been rebuilt on the
> measurement-fix campaign (`5b0f584`) plus the hotspot campaign (`da0d616`): Voice is
> policy-invariant under uniform Poisson load (P95 ≈ 2.2 ms), and emergency preemption
> recovers Voice service only under concentrated hotspot contention. **All "verified"
> numbers below are stale.** See `REVIEW_2026-08-16.md` for the current review,
> `EVAL_MEASUREMENT_REVIEW.md` for why the campaign was rerun, and
> `EVAL_HOTSPOT_VO_PROTECTION.md` for the hotspot evidence.

---

> **Document under review:** *Crash-Aware Traffic Prioritization in Vehicular Wi-Fi Networks* — UFSC Master's Dissertation
> **Compiled artifact:** `build/main.pdf` (~94 pages, build of 2026-08-14 17:21)
> **Review date:** 2026-08-14
> **Scope:** all seven chapters, front matter, bibliography, LaTeX build health, plus independent cross-verification against `../SBESC-2026-Paper/text.tex`, `../SBESC-2026-Paper/DSD2026_REVIEW.md`, and the `../veins-inet-qos/` artifact (OMNeT++ configs, C++ sources, SUMO files, Rust KPI pipeline).
> **Relation to prior work:** this review supersedes the 2026-08-10 final-audit revision plan (removed; formerly `REVISION_PLAN.md` on branch `revision/final-audit-fixes`). Open and deferred items from that audit were re-checked against current `main`.

---

## 1. Overall Verdict

**Grade: A− (near-submission-ready).**

The dissertation's narrative is coherent, the claims are scrupulously hedged, and — unusually for simulation theses — **the prose matches the code almost exactly**. Roughly 30 independent technical claims were re-verified against the artifact in this review (policy knobs, EDCA parameters, load profiles, timing, ports, FSM states, signals, drop counters, radio/mobility settings, vehicle counts, SUMO models) with **zero discrepancies** in the current text.

The single material risk is **not in the writing**: it is the **evidence chain**. The artifact currently contains **zero archived result files** and no documented seed configuration, so the Evaluation numbers cannot be regenerated from the repository as of today (item C2 of the prior audit, still open).

**Recommendation:** clear the reproducibility gap (§6.1) plus one layout overflow, and the manuscript is defense-ready.

---

## 2. Score Card

| Dimension | Grade | Notes |
|---|---|---|
| Research question & contribution | **A** | Focused, honest, deployable framing; protection-versus-cost frontier is a genuine, well-positioned contribution |
| Structure & argumentation | **A** | Clean Intro → Background → Related Work → System Model → Implementation → Evaluation → Conclusion separation; tool-agnostic where it should be (per `context/scientific-paper-structure.md`) |
| Technical accuracy vs. code | **A** | Verification matrix essentially 100%; more accurate than the SBESC short paper itself (exponential BE inter-arrivals; INET 4.5.4) |
| Bibliography & citation practice | **A−** | 45/45 keys cited, 0 undefined; normative-vs-informational RFC discipline is exemplary; one unresolved 5G/6G mismatch |
| Reviewer-feedback integration | **A** | All four DSD 2026 reviews' objections mapped to specific dissertation sections (§5) |
| Statistical rigor / reproducibility | **B** | Hedging exemplary, but 3 seeds, no CIs, and **no archived evidence** — the weakest dimension |
| Formatting / ABNT / build health | **A−** | 0 errors, 0 undefined refs, 0 overfull hboxes; one 13.45 pt float overflow; orphaned legacy figures |

---

## 3. Verification Methodology

Independent checks performed for this review (not relying on the prior audit):

1. **Full-text read** of `main.tex`, `beforetext/beforetext.tex`, and `chapters/0-Intro.tex` … `6-chapter.tex`.
2. **Citation integrity**: extracted all `\cite/\textcite` keys from chapters and compared against `aftertext/references.bib`.
3. **Number consistency**: cross-read every table/percentage against `SBESC-2026-Paper/text.tex` and across Abstract/Resumo/Intro/Evaluation/Conclusion.
4. **Config fidelity**: diffed the five MAC policies, EDCA parameters, load profiles, crash timing, ports, radio, and antenna/mobility settings against `veins_qos/simulations/veins_inet_highway_{light,heavy}/omnetpp.ini` and `highway.{rou,sumocfg,obstacles}.xml`.
5. **Code fidelity**: checked FSM states/transitions, `v2xState` encoding, `beDroppedWhileBlocked` signal, emergency congestion-reason drop semantics in `V2xEdcaFsmController.{h,cc}` and `V2xHcf.cc`; drop-attribution ÷2 guard in `kpi_dashboard/src/lib.rs`.
6. **Toolchain pins**: INET/Veins submodules vs. claimed versions; LICENSE presence; repo `AUDIT_REPORT.md` status.
7. **Build health**: `build/main.log` scanned for errors, undefined refs/citations, overfull boxes, float overflows, missing figure files.
8. **Reviewer coverage**: mapped every DSD 2026 "points against" item to dissertation sections.
9. **Figure inventory**: cross-referenced `\includegraphics` calls against `Figs/`.

---

## 4. Verified Correct (checked independently in this review)

### 4.1 Results integrity

Every Evaluation number matches the SBESC paper exactly, and the headline figures are internally consistent everywhere they are repeated:

| Claim | Value | Verified consistent in |
|---|---|---|
| VO P95 EDCA → emergency | 0.896 → 0.461 ms (≈ −49%) | Resumo, Abstract, Ch. 1 Contrib. 3, Tabs. `tab:eval:heavy_qos`/`tab:eval:heavy_p95`, Conclusion |
| VO jitter under emergency | 0.047 ms | Ch. 6 summary, Conclusion |
| VO-attributed MAC drops | 15 vs 18–21 ×10³ | Tabs. `tab:eval:heavy_vo_loss`, `tab:eval:heavy_drop_attr`, Conclusion |
| BE P95 plain → emergency | 57.4 → 98.7 ms | Tabs. `tab:eval:heavy_qos`/`tab:eval:heavy_p95`, Conclusion |
| MAC drop totals | 251–485 ×10³/run; BE overflow ≤ 197 ×10³ | Ch. 6 §6.1 text vs. tables |
| Light sweep (high load, vs. plain) | EDCA +2.2% VO P95; emergency −37.6% VO P95; BE +4854.7%…+9665.7% | Tab. `tab:eval:light` = SBESC Tab. I |
| Drop-attribution rows | sum to totals within rounding | Tab. `tab:eval:heavy_drop_attr` |

### 4.2 Code and configuration fidelity

| Claim in dissertation | Repository evidence | Result |
|---|---|---|
| Policy knobs: stable 15/80/5/2; guarded 4/20/4/3; emergency 10/60/5/1 + `emergencyPreemption` | `omnetpp.ini:137-168` | ✅ exact |
| EDCA queues BK/BE/VI/VO = 128/128/64/32; AIFSN 7/3/2/2; cwMin 15/15/7/3; cwMax 1023/1023/15/7; MSDU aggregation cleared | `omnetpp.ini:110-131` | ✅ exact |
| `plain`: single DCF queue 128, no classifier, `qosStation` off | `omnetpp.ini:106` | ✅ |
| QosClassifier: `crashDscp=46`, `defaultUp=0`, EDCA policies only | `omnetpp.ini:117-119`; `QosClassifier.cc` | ✅ |
| BE loads `exponential(500/250/125 ms)`, 200/320/420 B | `omnetpp.ini:78-99` | ✅ (dissertation is *more* accurate than the SBESC paper's "deterministic interval") |
| VO bursts 120/75/20 ms, repeats 3/4/8, gaps 20/15/5 ms, jitter 5/5/2 ms | `omnetpp.ini:80-102` | ✅ exact |
| sim-time-limit 70 s; crashAt 30 s; resumeAfter 30 s; target node index 0 | `omnetpp.ini:3,21-22` | ✅ |
| FSM modes `LISTENING/BLOCKING/SENDING`; `v2xState` = 0/1/2 | `V2xEdcaFsmController.h:8-10`, `.cc:37-44` | ✅ |
| `beDroppedWhileBlocked`, `beGrantSuppressedWhileBlocked`, `voProtectionActivation` signals | `V2xHcf.cc:36-53` | ✅ |
| Emergency drop uses congestion reason; only emergency drops BE | `V2xHcf.cc:115-185` | ✅ |
| ÷2 drop-attribution guard disclosed in §6.2 | `kpi_dashboard/src/lib.rs:899-906` | ✅ real mechanism, correctly disclosed |
| Density: 10 / 100 vehicles | `highway.rou.xml`: 9 flows + 1 fixed (light); 99 + 1 (heavy) | ✅ |
| Corridor: straight 5 km, 3 lanes *per direction*, EIDM + LC2013, mixed car/truck | `highway.net.xml`, `highway.rou.xml` | ✅ (H2 fixed) |
| Radio: 5.9 GHz, ch. 3, 10 MHz, 20 mW, opMode `p`, `Ieee80211DimensionalRadio` | `omnetpp.ini:34-37` | ✅ |
| SNIR 4 dB / sens −85 dBm / noise −110 dBm framed as **INET 4.5.4 defaults, not overridden**; 12 Mbit/s fastest-mandatory data rate stated | `omnetpp.ini` (absent ⇒ defaults), `tab:impl:parameters` | ✅ (H3 fixed) |
| OCB approximation caveat + BSS-vs-OCB EDCA parameter-set caveat | Ch. 5 §8.4 fidelity caveats | ✅ (H4 fixed) |
| TraCI port 9999, `veins_launchd`, update 1 s, SUMO step 0.1 s | `omnetpp.ini:58-62`, `highway.sumocfg` | ✅ |
| Antenna `AttachedMobility` fixed offsets (−2.5 m longitudinal, 1.5 m height) | `omnetpp.ini:38-44` | ✅ |
| Toolchain: OMNeT++ 6.1 / **INET 4.5.4** / Veins 5.3.1 | submodule pins + repo README | ✅ (C4 fixed; SBESC paper itself is stale at 4.5.2) |
| Artifact URL `github.com/GOAguiar99/veins-inet-qos` | `references.bib` | ✅ (C3 fixed; 404 removed) |
| LICENSE present | `veins-inet-qos/LICENSE` (GPL-2.0) | ✅ |
| Repo `AUDIT_REPORT.md` P95-scope error (node[0] claim) | marked resolved in repo | ✅ |

### 4.3 Citation and build integrity

- `references.bib` → 45 keys; chapters → 45 distinct cited keys; **sets are identical** (no orphans, no missing).
- `build/main.log`: **0 errors, 0 undefined references, 0 undefined citations, 0 overfull hboxes, 0 missing figure files**.
- No `\todo`/placeholder remnants in chapters or front matter (the two "placeholder" hits are legitimate technical descriptions; the 13 `FIXME` comments in `main.tex` are template boilerplate with fields already filled).
- Cross-reference audit: intro's roadmap ("Chapter 2 … Chapter 7") matches printed numbering; policy names uniform across Ch. 1/4/5/6/7 and ini config names.

---

## 5. Chapter-by-Chapter Assessment

### Introduction (Ch. 1)
Precise research question, explicit scope exclusions, objectives that map 1:1 onto Ch. 4–6. Claim ladder is conservative (no deterministic guarantees; statistical headroom only). No changes needed.

### Background (Ch. 2)
Technically the strongest chapter. The DCF → EDCA → 802.11p → DSCP path is rigorous; RFC normative/informational grading is a real intellectual strength; the Bianchi/Wu-et-al. "trend-not-numbers" handling of the backoff-freezing citation is mathematically careful; the three-pillar summary genuinely frames the problem. **One cross-reference error** (§6.2, item 3).

### Related Work (Ch. 3)
Four-family taxonomy (stronger coordination / contention timing and cost / always-on regulation / TSN-OFDMA contrast) is honest; the schematic-taxonomy figure discloses its qualitative nature; TSNCtl is correctly flagged as a non-peer-reviewed preprint; the comparison table is fair; the gap statement crisply instantiates the System Model.

### System Model (Ch. 4)
Correctly tool-agnostic. The controller description now includes the single-overheard-frame trigger and the two extra transitions (listening→sending; sending→blocking on guard expiry), so the figure is no longer falsifiable from source. Scope limits (no DCC, no fading, statistical-only) explicit.

### Implementation (Ch. 5)
Reference-quality. `tab:impl:parameters` is exactly the ini; both fidelity caveats (AdhocHost ≈ OCB; BSS-default EDCA vs OCB defaults, with the correct "conservative direction" argument) disclosed; `voDedupWindow` run-long semantics honestly documented; per-repeat `CreationTimeTag` delay semantics handled correctly (a known past pitfall, handled right).

### Evaluation (Ch. 6)
Strongest improvement over the short paper: expanded tables (drop attribution, controller actions, load ladders), honest light-sweep "gating test," mean-of-per-run-P95 aggregation stated explicitly, non-monotonic BE tails flagged as regime indicators rather than effect sizes, seven candid discussion subsections (escalation, plain-DCF sampling, significance ceiling, coarse-BE cost, spatial fairness, DoS, limitations). The framing "qualitative mechanism checks, not proven effect sizes" is exactly the right register.

### Conclusion (Ch. 7)
Mirrors the evidence without overreach; limitations restated as boundary conditions; future work is concrete and derived from the limitations rather than generic.

---

## 6. DSD 2026 Reviewer-Coverage Matrix

| # | Reviewer concern (source) | Where addressed | Verdict |
|---|---|---|---|
| 1 | Sub-millisecond absolute delays → practical significance unclear (R1, R2) | §5.6.3 (TS 22.186 25 ms framing: "headroom, not safety outcome") + Abstract hedging + §7.2 | ✅ addressed |
| 2 | Three seeds, no CIs/statistical tests (R1) | §5.2, §5.6.6, §7.3 (disclosed) | ⚠️ disclosed, not strengthened |
| 3 | No adaptive-EDCA / DCC baseline (R2) | §5.6.6, §7.3-7.4; positioned as complementary | ✅ addressed |
| 4 | Binary VO/BE underestimates preemption harm (R2) | §5.6.4 (worst-case-bound argument) + §7.4 (finer classes) | ✅ addressed |
| 5 | DoS via unauthenticated VO frames (R3) | §5.6.5 + §7.2 prerequisites; finite windows (20–80 ms, matches ini) | ✅ addressed |
| 6 | VO ≠ BE delays under plain DCF "not believable" (R3) | §5.6.2 dedicated explanation (traffic-process sampling) | ⚠️ textual only — R3 asked for supporting graphs/metrics; a small control experiment (matched payloads / per-sender breakdown) would close it definitively |
| 7 | One-hop restriction on a 5 km corridor; no multi-hop (R4) | §7.3 + future work (multi-hop relay settings) | ✅ addressed |
| 8 | Only 2 densities × 3 loads; no highway-parameter sweep (R4) | §7.3 (no continuous parameter space) + future work | ✅ addressed |
| 9 | Propagation model too optimistic (R2) | §4.5, §5.6.6, §7.3; richer propagation listed as future work | ✅ addressed |
| 10 | Modest novelty; fixed manual parameterizations (R2) | §5.6.6 + §7.4 (fixed design points, no trigger ablation; parameter sweep as future work) | ✅ addressed |
| 11 | Simulation-only, no testbed (R1, R2) | §7.3 + §7.4 (testbed/HIL validation) | ✅ addressed |

---

## 7. Issues Found, Ranked

### 7.1 Blocker-ish (close before submission)

1. **Reproducibility / evidence chain (C2 — still open).** Both `results/` trees are empty; `omnetpp.ini` has no `repeat`/seed stanza; `run_matrix.sh` defaults `RUNS=0`; figures are mixed vintage (`fig_06` Aug 2 export vs. `fig_01`/`fig_05` Aug 10). Every Ch. 6 number is today unregenerable from the artifact. *Actions:* document `repeat = 5`/`3` (or explicit seeds); re-run `PROFILE=full` on both packages; archive `results/` or at least the KPI exports (`run_rows.json`/`config_summary.json` + tables) in the repo or a companion (Zenodo) archive; pin the artifact commit hash in §5.1; re-export all Evaluation figures from one dataset (H6).

### 7.2 Should-fix (small, mechanical)

2. **Layout overflow.** `tab:rw:comparison` exceeds the page by 13.45 pt (`main.log:3142`, input line 118 of `2-chapter.tex`); one additional 5 pt overfull vbox later. Tighten `\tabcolsep` or a column.
3. **Cross-reference error (new finding, not in prior audit).** Ch. 2 §"EDCA access categories" text and the `tab:bg:edca-params` caption point to the **System Model chapter** for the study's numeric EDCA defaults; they actually live in the **Implementation** chapter (`tab:impl:parameters`). Fix the pointer twice (text + caption).
4. **5G/6G mismatch (deferred in prior audit, still open).** Prose (§3.1.4) says "5G New Radio V2X (NR-V2X) sidelink Mode 2"; the bib title says "Adaptive Autonomous Resource Allocation for **6G** V2x Sidelink" with a `NOTE` admitting unverified status. Verify the actual paper or align wording.
5. **Unexplained reach gap (candidate defense question).** At heavy/high, VO RX/alert ≈ 9.1–9.95 while BE RX/TX ≈ 6.15: alert frames reach *more* neighbors than background frames, and the text never explains why. Likely causes: denominators (logical sequences vs. physical packets), the crash source stopped in a denser neighborhood, and BE averaging over the early sparse-fleet phase. One clarifying sentence in §5.6 neutralizes the question.

### 7.3 Polish (optional)

6. `Figs/` carries ~18 unreferenced files (13 legacy raster/PDF + unused exports `fig_01_*_light`, `fig_02`, `fig_03`, `fig_04`, `fig_07`) — the known "orphaned figure cleanup" from `AGENTS.md`.
7. `WRITING_ROADMAP.md:29` still says "INET 4.5.2" (stale internal doc only).
8. `fig:sys:stack`, `fig:sys:fsm`, `fig:impl:stack` are tabular diagrams inside `figure` environments (listed in the LoF) — borderline "quadro vs. figura" under a strict ABNT reading; acceptable as-is but an examiner could quibble.
9. `\Autoref` multi-reference macro joins with Portuguese "e~" — currently unused in chapters (dormant, harmless).
10. Approval page placeholders (`Prof.(a) xxxx`) — expected pre-defense; final-version checklist item.
11. `tab:eval:light` percentages (+5605%, +9665%) rest on sub-millisecond baselines; the body explains it — adding "relative to sub-millisecond baseline delays" to the caption would armor it further.
12. "near ten receivers" covers 9.07–9.95; the `plain` row (9.07) is closer to nine. Cosmetic.

---

## 8. Deltas Since the Prior Audit (2026-08-10)

**Verified fixed:** C3 (URL), C4 (INET 4.5.4 everywhere incl. bib note), C5 (VO MAC drops relabel + `n.a.` for plain + caption note), H1 (÷2 heuristic disclosed), H2 (straight corridor + "3+3 lanes"), H3 (INET-default footnote + 12 Mbit/s rate), H4 (OCB approximation + BSS-vs-OCB caveat), H5 (FSM trigger semantics + extra transitions), H7/L5/L6 (bib repairs, duplicates pruned, umlauts, entry types), M1 (non-monotonic BE-tails caveat), M2 (light low/medium claim softened to "in our runs"), M3 (burst overlap + progressive fleet injection), M4 (mean-of-per-run-P95 wording), M5 (UPPAAL hedge removed), M7 (nine/ten harmonized), M8 (RFC 9119 "loss rate"), M9 (0.17 ↔ ~170 events note), L1, L2, L4 (Master's Dissertation label). C1 (figures) landed after the audit in commits `fbdfcfb` and `b42c85f`.

**Still open:** C2 (results archive + documented seeds — *the blocker*), H6 (depends on C2), CV2X title verification (bib `NOTE` still present), M10 partially (one oversized float remains; overfull hboxes are gone), L8 (orphan figures), L3 (committee page — defense-time).

**Newly found in this review:** the Background→System-Model cross-reference error (§7.2 item 3) and the unexplained VO/BE reach gap (§7.2 item 5).

---

## 9. Final Recommendation

The manuscript is ~95% of the way. Close §7.1 (archive runs + seeds + one-vintage figures), apply §7.2 items 2–5, and the remaining weak points — 3 seeds without CIs, the coarse two-class abstraction, simulation-only evidence — are **honestly disclosed scope decisions**, defensible as-is at a master's defense given the consistent hedging throughout.

The dissertation's distinguishing strengths, worth protecting in any final pass:

1. Claim/evidence alignment between prose and code (verified at ~100% in this review).
2. Normative-source discipline (normative vs. informational RFCs, preprint flagging, "trend-not-numbers" citation handling).
3. Candor about negative results (untimely protection, non-monotonic BE tails, DoS risk) — the same quality reviewers praised in the short paper.
4. The protection-versus-cost frontier as the organizing result, rather than as a side effect.

---

*Generated by an independent full review pass over the current `main` branch (`b42c85f`) and the `veins-inet-qos` artifact (branch `revision/dissertation-audit-fixes`, `a2aa5a6`).*
