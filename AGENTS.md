# Agent guide for `Masters/`

Read [AI_CONTEXT.md](AI_CONTEXT.md) before editing chapters or bibliography.

| Resource | Path |
|----------|------|
| Technical source of truth | `../veins-inet-qos/veins_qos/` |
| Latest short paper (primary source) | `../SBESC-2026-Paper/text.tex` |
| Earlier short paper (secondary) | `../ETFA-2026---Paper/text.tex` |
| Reviewer feedback to address | `../SBESC-2026-Paper/DSD2026_REVIEW.md` |
| Bibliography | `aftertext/references.bib` |
| Citation usage map | `context/bibliography-guide.md` |
| Code → cite mapping | `context/code-references.md` |
| Paper summaries | `context/sbesc-paper-summary.md`, `context/etfa-paper-summary.md` |
| Reference verification notes | `context/reference-notes.md` |
| Background chapter plan | `context/background-chapter-plan.md` |
| Related Work chapter plan | `context/related-work-chapter-plan.md` |
| System Model chapter plan | `context/system-model-chapter-plan.md` |
| Implementation chapter plan | `context/implementation-chapter-plan.md` |
| Evaluation chapter plan | `context/evaluation-chapter-plan.md` |
| Conclusion chapter plan | `context/conclusion-chapter-plan.md` |
| System Model / Implementation / Evaluation separation | `context/scientific-paper-structure.md` |
| Chapter alignment audit | `WRITING_ROADMAP.md` |
| Current dissertation review | `REVIEW_2026-08-16.md` (`DISSERTATION_REVIEW.md` = superseded pre-fix review) |
| Evaluation notes (why campaigns changed) | `EVAL_MEASUREMENT_REVIEW.md`, `EVAL_HOTSPOT_VO_PROTECTION.md` |
| KPI evidence archive | `context/eval-kpis/` (artifact pinned to tag `dissertation-2026-08` = `da0d616`) |
| Reference PDF workflow | `REF_PAPERS_WORKFLOW.md` |

Build: `./compile.sh` → `build/main.pdf` (persistent, gitignored). `./compile.sh clean` removes artifacts. Sources compile unchanged on Overleaf.

**Main chapters are pivoted to the crash-aware topic** (Introduction through Conclusion). Do not revive legacy DQ-WiFi Work Plan / schedule material unless explicitly asked. Title/metadata, Resumo/Abstract, Background, Related Work, System Model, Implementation, Evaluation, and Conclusion already follow the crash-aware study.

Do not invent results, measurements, or citations. Prefer the active `veins_qos/` implementation and the SBESC paper over legacy TSN/DQ-WiFi draft material when planning future edits.
