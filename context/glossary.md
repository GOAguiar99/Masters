# Glossary

| Term | Meaning in this thesis |
|------|------------------------|
| **BE** | Best Effort — ordinary background traffic, DSCP 0, AC_BE |
| **VO** | Voice — crash-alert traffic, DSCP 46 (EF), mapped to AC_VO |
| **DSCP 46** | Expedited Forwarding codepoint (RFC 3246); study's crash marker |
| **EF** | Expedited Forwarding PHB — low-delay intent, not a guarantee |
| **UP 6** | 802.11 user priority for voice class |
| **AC_VO** | EDCA voice access category — most aggressive contention params |
| **DCF** | Distributed Coordination Function — single-queue CSMA/CA baseline |
| **EDCA** | Enhanced Distributed Channel Access — four ACs with differentiated AIFS/CW |
| **802.11p** | Vehicular Wi-Fi mode (5.9 GHz, typically 10 MHz channels) |
| **WAVE** | Wireless Access in Vehicular Environments (IEEE 1609.x family) |
| **V2X** | Vehicle-to-everything communication |
| **V2xHcf** | Custom HCF module replacing INET `Hcf` for adaptive profiles |
| **FSM** | Finite state machine in `V2xEdcaFsmController`: LISTENING, BLOCKING, SENDING |
| **plain** | MAC config: DCF baseline, no effective QoS differentiation |
| **edca_only** | Standard EDCA + explicit DSCP→Voice classifier |
| **stable** | Adaptive profile: sustained VO protection, longer block windows |
| **guarded** | Adaptive profile: tighter block windows, higher VO threshold |
| **emergency** | Adaptive profile: may drop BE packets while protection active |
| **Protection–cost** | VO service improvement vs BE delay/loss/reach degradation |
| **Multicast reach** | RX copies per logical TX (not unicast delivery ratio) |
| **P95** | 95th percentile delay — primary tail metric for crash alerts |
| **DCC** | Decentralized Congestion Control (ETSI) — **not modeled** in current artifact |
| **TSN** | Time-Sensitive Networking — contrast only, not primary contribution |

## Mapping chain (study configuration)

```
DSCP 0  → BE  → AC_BE  (ordinary traffic)
DSCP 46 → UP 6 → AC_VO  (crash alerts, explicit policy)
```

These layers are linked by configuration, not automatic in all deployments (see RFC 8325).
