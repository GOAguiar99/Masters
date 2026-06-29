# Code references for dissertation text

Maps `veins-inet-qos` modules to bibliography keys and version pins.

## Version pins (state in Implementation chapter)

| Component | Version | Citation |
|-----------|---------|----------|
| OMNeT++ | 6.1 | `varga2008omnetpp`, `varga2010omnetpp` |
| INET Framework | 4.5.2 | `inet_framework` |
| Veins | submodule commit at experiment time | `sommer2015veins` |
| SUMO | record `sumo --version` at experiment time | `lopez2018sumo` |
| UPPAAL | if verification section included | `bengtsson1995uppaal` |

## Module → citation map

| Code location | Dissertation mention | Bibliography |
|---------------|---------------------|--------------|
| `veins_qos/src/traffic/CritPacketSender` | Periodic BE multicast traffic model | Own design; `RFC8325_WiFi_QoS` for marking context |
| `veins_qos/src/traffic/CrashBurstApp` | Crash event and VO burst | Own design; `RFC3246_EF_PHB` for DSCP 46 |
| `veins_qos/src/qos/QosClassifier` | Explicit DSCP→Voice mapping | `RFC8325_WiFi_QoS`, `IEEE80211e_2005` |
| `veins_qos/src/mac/V2xHcf` | **Main contribution** — adaptive BE suppression | `aguiar2026_veins_qos`; contrast `romdhani2003AdaptiveEDCF`, `SkipCCH_Garrido` |
| `veins_qos/src/mac/V2xEdcaFsmController` | FSM states and protection windows | Same as V2xHcf |
| `veins_qos/src/mac/V2xIeee80211Mac` | Drop instrumentation | `inet_framework` |
| `veins_qos/src/veins_inet/*` | Veins+INET integration | `sommer2015veins`, `inet_framework`; acknowledge Sommer/Bigge in text |
| `simulations/veins_inet_highway_*` | Evaluation scenarios | `sommer2015veins`, `lopez2018sumo`, `IEEE_80211p_Survey` |
| INET `IdealObstacleLoss` | Binary propagation model | `inet_ideal_obstacle_loss` |
| INET `Ieee80211DimensionalRadio` | 802.11p radio baseline | `IEEE80211`, `IEEE_80211p_Survey` |
| `uppaal/v2x_edca.xml` | Formal model (optional) | `bengtsson1995uppaal` |
| `kpi_dashboard/` | Results aggregation | Methodology paragraph; no formal cite required |

## Standards referenced but not modeled

| Standard | Key | Note |
|----------|-----|------|
| IEEE 1609.4 multi-channel WAVE | `ieee1609_4` | Contrast for SkipCCH-related work |
| ETSI DCC TS 102 687 | `etsi_dcc_102687` | Future baseline; not in current ini |
| DetNet bounded latency | `rfc9320_detnet` | Contrast only — do not claim DetNet |

## Acknowledgment text (Implementation)

> The Veins/INET integration modules derive from the Veins project (Sommer et al.) and INET Framework. `VeinsInetTransparentMobility` incorporates work by Jannusch Bigge (TU Dresden).

## Artifact citation (Evaluation / Implementation)

Use `\cite{aguiar2026_veins_qos}` when referring to the public simulation artifact, scenario matrices, and KPI dashboard.

Update the `url` field in `references.bib` when the repository is published.
