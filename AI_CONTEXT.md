# AI Context for `Masters/` (UFSC dissertation)

## What this repository is

`Masters/` is the LaTeX workspace for Gabriel de Oliveira Aguiar's UFSC Master's thesis on **crash-aware QoS in vehicular Wi-Fi**.

This repository is for writing, structuring, revising, and formatting the dissertation.
It is **not** the source of truth for simulation logic, KPI generation, or protocol behavior.

When working here, assume:
- `main.tex` is the master document (abnTeX2 / UFSC template)
- `chapters/*.tex` hold the body text (**legacy DQ-WiFi draft — do not rewrite until explicitly requested**)
- `aftertext/references.bib` is the single bibliography database (biblatex/abnt)
- `Figs/` contains dissertation figures
- `context/` holds AI-readable knowledge (summaries, glossary, bib guide)
- `ref_papers/` contains local reference PDFs for author context only (gitignored)

## Scope of current work (context pass)

This repository currently has:
- **Ready:** AI context, bibliography merge, ref-papers pipeline, ETFA/code summaries, ETFA figures in `Figs/`
- **Not yet rewritten:** `chapters/*.tex`, `beforetext/beforetext.tex` (still DQ-WiFi draft)

When assisting, prefer updating `context/`, `references.bib`, and `ref_papers/` over editing chapter prose unless the user explicitly asks for a chapter rewrite.

## Canonical sources

| Role | Path |
|------|------|
| Simulation code | `../veins-inet-qos/veins_qos/` |
| Code AI context | `../veins-inet-qos/veins_qos/AI_CONTEXT.md` |
| ETFA 2026 paper (short form) | `../ETFA-2026---Paper/text.tex` |
| ETFA AI context | `../ETFA-2026---Paper/AI_CONTEXT.md` |
| Research critique | `../veins-inet-qos/review.md` |

Before making non-trivial technical claims, check the code and `veins_qos/AI_CONTEXT.md`.
If LaTeX text and code disagree, prefer the active `veins_qos/` implementation.

## Thesis topic (active pivot)

Crash-aware QoS in vehicular Wi-Fi with a minimal two-class model:
- ordinary Best Effort (BE) traffic vs crash-critical Voice (VO) traffic under contention

Central question:

Can crash-triggered traffic obtain better wireless service than ordinary traffic in Veins/INET simulations, and what cost does that protection impose on ordinary traffic?

## Core study framing

- All vehicles send periodic ordinary traffic through `CritPacketSender` (DSCP 0, BE)
- One target vehicle enters crash state through `CrashBurstApp` (DSCP 46, VO)
- `QosClassifier` maps DSCP 46 → `UP_VO`
- Five MAC policies: `plain`, `edca_only`, `edca_v2x_vo_stable`, `edca_v2x_vo_guarded`, `edca_v2x_vo_emergency`
- Simulation time: **70 s**; crash window: 30 s starting at t=30 s
- Active scenarios: `veins_inet_highway_light` (10 vehicles), `veins_inet_highway_heavy` (100 vehicles)

Do not expand into a full ITS stack, generic QoS framework, or multi-class orchestration unless explicitly requested.

## Legacy-topic guardrail

Older dissertation drafts described **DQ-WiFi** (Wireless TSN, TAS, beacon-synchronized FSM, bandwidth reservation).
That content is **deprecated** unless kept explicitly as related-work contrast.

Default behavior:
- Remove or rewrite TSN/TAS/reserva/LISTENING-BLOCKED-ACTIVE FSM material
- Do not claim deterministic slotting, synchronization, or provable worst-case bounds unless the code implements them
- TSN/OFDMA references belong in a short contrast subsection only (see `context/bibliography-guide.md`)

## UFSC / abnTeX2 constraints

- Document class: `abntex2` with `\addbibresource{aftertext/references.bib}`
- Portuguese **Resumo** + English **Abstract** in `beforetext/beforetext.tex`
- Main chapters in English
- Citation commands: `\cite{}`, `\textcite{}`, `\parencite{}` (biblatex/abnt)

## Reference-paper workflow

See [REF_PAPERS_WORKFLOW.md](REF_PAPERS_WORKFLOW.md).

- New PDFs → `ref_papers/Analysis/`
- `python3 scripts/process_ref_papers.py prepare`
- AI reviews `ref_papers/review_queue.json`
- `python3 scripts/process_ref_papers.py apply ref_papers/review_decisions.json`
- `python3 scripts/generate_bib.py` appends missing keys to `aftertext/references.bib`

## Writing guardrails

- Do not invent results, measurements, or citations
- Do not claim experiments were run unless results exist in `veins-inet-qos/`
- Keep terminology consistent (BE, VO, DSCP 46, EF, UP 6, AC_VO are linked but not synonyms)
- Prefer precise technical prose over marketing language
- Emphasize protection-versus-cost trade-off, not deterministic guarantees

## Safe assumptions

- `plain` = DCF baseline without effective EDCA prioritization
- `edca_only` = standard EDCA with custom DSCP→Voice classifier
- `stable` / `guarded` / `emergency` = adaptive V2X profiles (BE suppression; emergency may drop BE)
- Main KPIs: delay (mean, P95), jitter, RX/TX reach, MAC drops, V2X controller actions
- Tail metrics pool receiving `app[0]` vectors across nodes

## Editing boundaries

Normal edits: chapters, bibliography, figures, context docs, abstracts.

Avoid: changing simulation code in dependency trees; claiming features not in `veins_qos/`; modifying `setup/ufscthesisA4-alf.sty` without explicit request.
