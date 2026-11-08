# Crash-Aware QoS in Vehicular Wi-Fi — UFSC Master's Dissertation

LaTeX sources (abnTeX2 / UFSC template) for Gabriel de Oliveira Aguiar's Master's dissertation. The dissertation evaluates, through OMNeT++/Veins/INET simulation, whether crash-triggered Voice traffic can get better IEEE 802.11p service than ordinary Best Effort traffic using only local, standard MAC mechanisms, and what that protection costs ordinary traffic.

## Build

```bash
./compile.sh          # → build/main.pdf (needs TeX Live with biber; MacTeX on macOS)
./compile.sh clean    # remove build artifacts
```

The tracked tree also compiles unchanged on Overleaf. Figures drawn in TikZ (`Figs/*.tex`) are standalone documents: run `pdflatex` on them and commit the resulting PDF next to the source.

## Layout

| Path | Contents |
|------|----------|
| `main.tex` | Master document |
| `beforetext/` | Cover, approval page, Resumo/Abstract |
| `chapters/` | Introduction (`0`) through Conclusion (`6`) |
| `aftertext/` | `references.bib`, Appendix A (artifact repository layout), Appendix B (use of AI tools) |
| `Figs/` | Figures (PDF, plus TikZ sources) |
| `context/` | Chapter plans, bibliography guide, reference notes, KPI evidence archive |
| `docs/spec/professor-revisions.md` | Professor's revision checklist and status |

## Related repositories

- Simulation artifact (source of truth for all results): `../veins-inet-qos/veins_qos/`
- SBESC 2026 paper: `../SBESC-2026-Paper/`

## Contributors

Contributors and AI assistants should read `AGENTS.md` and `AI_CONTEXT.md` first.
