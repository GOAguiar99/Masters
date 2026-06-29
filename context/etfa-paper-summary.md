# ETFA 2026 paper summary (for dissertation context)

Source: `../ETFA-2026---Paper/text.tex`

## Title theme

Crash-aware QoS in vehicular IEEE 802.11p: BE vs VO under shared-channel contention.

## Section structure

1. **Introduction** — V2X motivation, DSCP+EDCA path, gap for local event-driven prioritization, five MAC policies
2. **Background** — 802.11p/DCF, EDCA, DiffServ/DSCP mapping, contention/multicast limits
3. **Related Work** — Stronger mechanisms (TSNCtl, PRP-MAC, CFC-MAC, NR-V2X), prior SBESC work, backoff freezing, SkipCCH
4. **System Model** — Decentralized highway, two-class traffic, five policies, crash timeline
5. **Implementation** — OMNeT++ 6.1 / INET 4.5.2 / Veins artifact
6. **Evaluation** — Light (10 veh) + heavy (100 veh) sweeps, protection–cost discussion
7. **Conclusion** — Emergency best for VO tail under congestion; bounded blocking risky at light load

## Contributions (from paper)

- Synthetic crash-triggered two-class traffic model (BE + VO burst)
- Five-policy comparison in open Veins/INET artifact
- Adaptive V2X MAC trade-off analysis (protection vs BE penalty)

## Citation keys used in ETFA (24)

`IEEE_80211p_Survey`, `IEEE80211`, `IEEE80211e_2005`, `bianchi2000DCF`, `kong2004EDCA`, `mangold2003QoS`, `ni2004Qiang`, `kosekszott2012What`, `romdhani2003AdaptiveEDCF`, `RFC2474_DSField`, `RFC2475_DiffServ_Architecture`, `RFC3246_EF_PHB`, `RFC4594_DiffServ_Service_Classes`, `RFC8325_WiFi_QoS`, `RFC9119_Multicast_IEEE802_Wireless`, `Continuous_Backoff_Freezing_Li`, `Evolution_QoS_Mechanisms`, `TSNCtl_Feraudo`, `PRP_MAC_Li`, `CFC_MAC_Linn`, `CV2X_Sidelink_Allocation`, `SkipCCH_Garrido`, `11288825`, `veins_inet_qos_2026`

Dissertation uses `aguiar2026_veins_qos` instead of the anonymized artifact key.

## Figures

- `figures/system_model_architecture.pdf` — decentralized V2V architecture
- `figures/event_timeline_cropped.pdf` — normal / crash / recovery phases
- `figures/eval/fig_06_*` — VO delay CDF at heavy high load

## Experiment matrix

| Dimension | Values |
|-----------|--------|
| Density | light (10), heavy (100) |
| Load | low, medium, high (`_netload_*`) |
| MAC | plain, edca_only, stable, guarded, emergency |
| Seeds | 5 (light), 3 (heavy) |

## Key numeric anchors (heavy, high load)

| Policy | VO P95 (ms) | BE P95 (ms) |
|--------|-------------|-------------|
| plain | 1.290 | 57.367 |
| edca_only | 0.896 | 155.857 |
| stable | 1.155 | 144.314 |
| guarded | 0.960 | 174.401 |
| emergency | **0.461** | 98.663 |

Emergency ≈ −49% VO P95 vs EDCA at high load.

## Dissertation differences from paper

- abnTeX2 format, longer background, optional UPPAAL formal verification section
- May include expanded TSN contrast from earlier draft
- De-anonymized artifact citation and full implementation detail
