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
| Chapter alignment audit | `WRITING_ROADMAP.md` |
| Reference PDF workflow | `REF_PAPERS_WORKFLOW.md` |

Build: `./compile.sh` → `build/main.pdf` (persistent, gitignored). `./compile.sh clean` removes artifacts. Sources compile unchanged on Overleaf.

**Do not rewrite `chapters/*.tex` or abstracts unless explicitly asked.** Title/metadata in `main.tex` are already pivoted to the crash-aware topic; the chapter text is still the legacy DQ-WiFi draft.

Do not invent results, measurements, or citations. Prefer the active `veins_qos/` implementation and the SBESC paper over legacy TSN/DQ-WiFi draft material when planning future edits.
