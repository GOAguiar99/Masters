# Evaluation KPI archive

Compact per-run KPI rows used by Chapter 6 (Evaluation). These JSON files are
the regenerable evidence chain for the printed tables; they are **not** the raw
OMNeT++ `.sca`/`.vec` traces.

## Packages

| Density | Vehicles | Seeds (OMNeT run numbers) | Configs | Runs |
|---------|----------|---------------------------|---------|------|
| `highway_light` | 10 | `#0`–`#4` | 5 policies × 3 loads | 75 |
| `highway_heavy` | 100 | `#0`–`#2` | 5 policies × 3 loads | 45 |

Parser: `rust-kpi-dashboard-0.2.0`, cache schema 3.

Configuration names follow `<policy>_netload_<low|medium|high>` with policies
`plain`, `edca_only`, `edca_v2x_vo_stable`, `edca_v2x_vo_guarded`,
`edca_v2x_vo_emergency`.

## Files

Each density directory contains:

- `run_rows.json` — one object per seed (delay, jitter, reach, MAC drops, controller counters)
- `config_summary.json` — arithmetic means over seeds
- `meta.json` — parser version and run counts (source-file signatures omitted to keep the thesis tree small)

## Raw traces

The `.sca`/`.vec` trees live in the simulation artifact clone, not in this
dissertation repository:

- `veins_qos/simulations/veins_inet_highway_light/results/`
- `veins_qos/simulations/veins_inet_highway_heavy/results/`

Artifact: <https://github.com/GOAguiar99/veins-inet-qos>  
Pinned commit used for this archive: `39155fae0bf8ccd798536ac4321e1c5c2a5b4e86` (2026-05 KPI export cleanup).

Rebuild the cache from raw traces with:

```bash
cd kpi_dashboard
cargo run --release -- --rebuild --results ../veins_qos/simulations/veins_inet_highway_heavy/results
```
