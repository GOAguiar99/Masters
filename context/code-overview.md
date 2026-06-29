# Code overview (from `veins-inet-qos/veins_qos/`)

Canonical path: `../veins-inet-qos/veins_qos/`

## Purpose

Minimal crash-aware QoS testbed: BE vs VO under Veins/INET Wi-Fi simulation.

## Module map

| Path | Role |
|------|------|
| `src/traffic/CritPacketSender` | Periodic BE multicast (DSCP 0) |
| `src/traffic/CrashBurstApp` | Crash-triggered VO burst (DSCP 46) |
| `src/qos/QosClassifier` | DSCP → 802.11 user priority |
| `src/mac/V2xHcf` | Custom HCF with adaptive BE suppression |
| `src/mac/V2xEdcaFsmController` | LISTENING / BLOCKING / SENDING FSM |
| `src/mac/V2xIeee80211Mac` | Instrumented MAC (drop counters) |
| `src/veins_inet/` | Veins+INET car/mobility integration |
| `simulations/veins_inet_highway_light/` | 10-vehicle density study |
| `simulations/veins_inet_highway_heavy/` | 100-vehicle stress study |
| `../kpi_dashboard/` | Python Dash KPI analysis |
| `../uppaal/` | Offline V2xHcf model checking |

## Packet path

1. Apps tag packets (DSCP 0 or 46)
2. `QosClassifier` maps to UP / AC
3. EDCA queues arbitrate (`plain` uses single DCF queue)
4. `V2xHcf` (adaptive profiles only) suppresses or drops BE channel requests when VO protection active

## Five MAC configs (ini suffix pattern)

`<policy>_netload_<low|medium|high>`

- `plain_*` — no EDCA differentiation
- `edca_only_*` — classifier + standard EDCA
- `edca_v2x_vo_stable_*`, `edca_v2x_vo_guarded_*`, `edca_v2x_vo_emergency_*` — adaptive profiles

## Hypotheses (H1–H5)

- H1: VO delay < BE under contention
- H2: VO reception better than BE when congested
- H3: EDCA tuning may be needed beyond default mapping
- H4: VO gains must be weighed against BE penalty
- H5: Conclusions must hold across light and heavy density

## Version pins (experiments)

- OMNeT++ 6.1
- INET 4.5.2
- Veins (git submodule — record commit at experiment time)
- SUMO via TraCI (record `sumo --version`)

## What the code is not

- Not a full ITS/CAM/DENM stack
- Not DCC rate control
- Not deterministic TSN / schedule-based access
- Not claiming provable worst-case latency bounds

## Attribution

- Veins integration: Christoph Sommer et al.
- `VeinsInetTransparentMobility`: Jannusch Bigge, TU Dresden

See [code-references.md](code-references.md) for bibliography mapping.
