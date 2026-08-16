# Evaluation KPI archive

Compact per-run KPI rows used by Chapter 6 (Evaluation). These JSON files are
the regenerable evidence chain for the printed tables; they are **not** the raw
OMNeT++ `.sca`/`.vec` traces.

This archive is the **measurement-fix** campaign: Poisson Best Effort redrawn
every packet, Voice delay stamped at logical burst start (alert age), and a
crash-node Best Effort delay slice. It replaces the 2026-05 export.

## Packages

| Density | Vehicles | Seeds (OMNeT run numbers) | Configs | Runs |
|---------|----------|---------------------------|---------|------|
| `highway_light` | 10 | `#0`–`#2` | 5 policies × 3 loads | 45 |
| `highway_heavy` | 100 | `#0`–`#2` | 5 policies × 3 loads | 45 |

Parser: `rust-kpi-dashboard-0.2.1`, cache schema 3.

Configuration names follow `<policy>_netload_<low|medium|high>` with policies
`plain`, `edca_only`, `edca_v2x_vo_stable`, `edca_v2x_vo_guarded`,
`edca_v2x_vo_emergency`.

## Files

Each density directory contains:

- `run_rows.json` — one object per seed (delay, jitter, reach, MAC drops, controller counters, crash-node BE delay)
- `config_summary.json` — arithmetic means over seeds
- `meta.json` — parser version and run counts (source-file signatures omitted to keep the thesis tree small)

## Raw traces

The `.sca`/`.vec` trees live in the simulation artifact clone, not in this
dissertation repository:

- `veins_qos/simulations/veins_inet_highway_light/results/`
- `veins_qos/simulations/veins_inet_highway_heavy/results/`

Artifact: <https://github.com/GOAguiar99/veins-inet-qos>  
Pinned commit used for this archive: `5b0f584` (`fix/measurement-poisson-vo-clock`).

Rebuild the cache from raw traces with:

```bash
cd kpi_dashboard
cargo run --release --bin export_figures -- --rebuild \
  --results ../veins_qos/simulations/veins_inet_highway_light/results \
  --results ../veins_qos/simulations/veins_inet_highway_heavy/results \
  --output publication_figures --formats svg,pdf
```
