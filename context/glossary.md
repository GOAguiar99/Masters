# Glossary

Canonical acronym and symbol definitions live in [`main.tex`](../main.tex) (`\newacronym` / `\simbololista`). Use `\gls{key}` / `\glspl{key}` in chapters so entries appear in the printed lists.

## Core study terms

| Term | Meaning in this thesis |
|------|------------------------|
| **BE** | Best Effort — ordinary background traffic, DSCP 0, AC_BE |
| **VO** | Voice — crash-alert traffic, DSCP 46 (EF), mapped to AC_VO |
| **BK / VI** | Background / Video EDCA access categories (present in queues; unused by the two-class generators) |
| **DSCP 46** | Expedited Forwarding codepoint (RFC 3246); study's crash marker |
| **EF** | Expedited Forwarding PHB — low-delay intent, not a guarantee |
| **UP** | 802.11 user priority (crash path uses UP 6 → AC_VO) |
| **DCF** | Distributed Coordination Function — single-queue CSMA/CA baseline (`plain`) |
| **EDCA** | Enhanced Distributed Channel Access — four ACs with differentiated AIFS/CW |
| **CAM / DENM** | ETSI awareness / event notification messages — contrasted, not reproduced |
| **SNIR** | Signal-to-Noise-plus-Interference Ratio threshold in the radio model |
| **P95** | 95th percentile delay — primary tail metric for crash alerts |
| **DCC** | Decentralized Congestion Control (ETSI) — **not modeled** in current artifact |
| **Veins / TraCI / SUMO** | Bidirectional network–mobility simulation stack |
| **TSN / TAS / OFDMA** | Contrast only (Related Work), not primary contribution |

## Mapping chain (study configuration)

```
DSCP 0  → BE  → AC_BE  (ordinary traffic)
DSCP 46 → UP 6 → AC_VO  (crash alerts, explicit policy)
```

## Symbols (Bianchi / EDCA math)

Declared via `\simbololista` in `main.tex`: \(\mathrm{CW}_{\min}\), \(\mathrm{CW}_{\max}\), \(W\), \(p\), \(\tau\), \(m\), \(\mathrm{AIFS}[i]\), \(\mathrm{AIFSN}[i]\), \(\mathrm{SIFS}\), \(a\mathrm{SlotTime}\).
