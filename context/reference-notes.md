# Reference verification notes (Background pass, July 2026)

All reference PDFs live in `ref_papers/Relevant/` (gitignored, filenames = bib keys). 20 PDFs downloaded from official/reliable sources (RFC Editor, ETSI, MDPI CDN, arXiv, author preprints, DLR, university mirrors) and read by AI reviewers; every entry below was verified against `aftertext/references.bib`.

## Verification verdicts

| Bib key | PDF | Verdict | Notes |
|---------|-----|---------|-------|
| `RFC2474_DSField` | yes | Match | Standards Track. DSCP field definition (§3); DSCP 0 = Default/BE (§4.1); unmapped codepoints → Default (§3) |
| `RFC2475_DiffServ_Architecture` | yes | Match | **Informational.** BA classifier (§2.3.1); PHB definition (§2.4); L2 mapping dependency (§1.4, G.15); host pre-marking (§2.3.4.1) |
| `RFC3246_EF_PHB` | yes | Match | Standards Track. **DSCP 46 = EF codepoint: §2.7** ("Codepoint 101110 RECOMMENDED"); EF = low delay/jitter/loss building block; damage-limiting requirement for preemptive implementations (§2.10) |
| `RFC4594_DiffServ_Service_Classes` | yes | Match | **Informational** guidelines. Telephony class → EF PHB, priority queuing, end-point pre-marking (§4.1); Standard class = DF/DSCP 0 (§4.9) |
| `RFC8325_WiFi_QoS` | yes | Match | Standards Track. **Load-bearing mapping citation**: no standard default DSCP→UP mapping (§2.3); default 3-MSB practice sends EF to UP 5/AC_VI instead of AC_VO (§2.3); recommended EF→UP 6/AC_VO (§4.2.1, Fig. 1); UP→AC tables + EDCA parameters (§6.2.2–6.2.4); 802.11 cannot deliver true EF/strict priority (§2); DSCP-marking DoS vector (§8.2). Caveat: infrastructure-WLAN scenario, not OCB — mechanics carry over, AP-centric recommendations do not |
| `RFC9119_Multicast_IEEE802_Wireless` | yes | Match | **Informational.** No ACK/retransmission/backoff for multicast, PER ≥ 5% common (§3.1.1); basic-rate transmission (§3.1.2); airtime cost (§3.1.3); GCR helps but no guarantee (§4.7). Caveat: AP/BSS-centric — cite §3.1.x facts (valid for OCB broadcast), not the §4–5 AP-based mitigations |
| `ts22186` | yes | Match | ETSI TS 122 186 V16.2.0 mirror. **25 ms platooning bound confirmed: Table 5.2-1, requirement [R.5.2-004]** — lowest degree of automation, 90% reliability, 300–400 B, 30 msg/s. Cite exactly this anchor |
| `3gpp_ts_22_261_r18` | yes | Match | Rel-18 (v18.16.0) has **no URLLC KPI table in clause 7.2** — V2X values are deferred to TS 22.186. Usable: ITS-backhaul 30 ms figure, general low-latency clauses. Prefer TS 22.186 for V2X numbers |
| `etsi_dcc_2018` | yes | Match | TS 102 687 V1.2.1. Reactive + adaptive DCC approaches; CBR (channel busy ratio) drives TPC/TRC/DCC access control; always-on regulation of a station's aggregate offered load — contrast with event-triggered per-class suppression |
| `bianchi2000DCF` | yes | Match | JSAC 18(3):535–547. DCF = CSMA/CA + binary slotted exponential backoff; backoff freezing described (§II); 2-D Markov saturation model (§IV); throughput degrades with station count (§VII); fixed CW suboptimal → motivates adaptive tuning (§VI). Assumes ideal channel + saturation |
| `mangold2003QoS` | yes | Match | IEEE Wireless Comm 10(6):40–50. "No QoS support in the DCF" (p. 41); EDCA mechanism (AIFS/CW/TXOP, virtual collisions); prioritization is relative (Fig. 8); EDCA delay "increases unpredictably" with load (Fig. 10). **Caveat: analyzes 802.11e draft D5.0 — do not cite its parameter values as the final standard's** |
| `kosekszott2012What` | yes | Match (prepublication) | Published IEEE Network 27(6):95–104, Nov 2013 (bib year 2013 correct; key name "2012" is historical). "EDCA cannot guarantee any throughput or delay bounds, only differentiation" (§2.1); group-addressed frames transmitted without retries (§3.1); 802.11aa GCR/SCS, 802.11ae QMF. Don't cite this PDF's page numbers (prepub layout) |
| `Evolution_QoS_Mechanisms` | yes | **Version mismatch** | Local file = arXiv:1411.2852 (2014) titled "…A Contemporary **Survey**"; bib cites JNCA 55:24–46 (2015) "…A contemporary **review**". Keep bib as-is (version of record); re-verify any verbatim quote against the JNCA version. Claims: legacy 802.11 has no differentiation; strict priority starves low-priority ("zero-valued throughput"); differentiation fails beyond a load limit; adaptive-parameter precedents |
| `Continuous_Backoff_Freezing_Li` | yes | Match | Electronics 8(12):1404, 2019. Continuous backoff freezing inflates 802.11p delay; delay/PDR degrade with density; broadcast more practical than unicast for safety. **Cite trends, not absolute values** (their config is lightly loaded: 0.17–0.26 ms delays) |
| `TSNCtl_Feraudo` | yes | Match | Full arXiv WIP preprint (8 pp). TSN-like slot-based platooning scheduler; relies on synchronized slotting + platoon leader. **Cite as non-peer-reviewed preprint** |
| `PRP_MAC_Li` | yes | Match | Applied Sciences 14(5):2151, 2024. Preemptive-resume priority MAC, UAV-assisted VANETs — relies on richer protocol machinery + UAV infrastructure |
| `CFC_MAC_Linn` | yes | Match | Sensors 23(2):1033, 2023. Distributed TDMA-based cooperative MAC — relies on time-slotted (synchronization-like) operation |
| `SkipCCH_Garrido` | yes | Match | Computers 13(1):16, 2024. Multi-channel packet scheduling (SkipCCH) for video over VANET — relies on 1609.4 multi-channel machinery |
| `veins_sommer2011` | yes | Match | IEEE TMC 10(1):3–15, Jan 2011 (verified from PDF header). Bidirectional coupling of OMNeT++ and SUMO via TraCI; mobility model choice strongly influences IVC results |
| `lopez2018sumo` | yes | Match | ITSC 2018, pp. 2575–2582 (DLR open-access copy). SUMO reference publication; microscopic, intermodal, TraCI coupling |

The intro sentence "these approaches rely on synchronization, infrastructure, or richer protocol machinery" is **supported** by all four related-work papers (TSNCtl: sync+leader; PRP-MAC: UAV infrastructure+machinery; CFC-MAC: TDMA sync; NR-V2X sidelink: cellular resource machinery).

## Problem references (action needed)

| Bib key | Problem | Recommended action |
|---------|---------|--------------------|
| `IEEE_80211p_Survey` (Miao et al. 2012) | **Unreliable**: defunct publisher ("Mobile Computing", Science and Engineering Publishing), no working official source, a bogus DOI (10.1001/JAMA…) circulates in indexes. No PDF obtainable from a trustworthy host | **Replace in dissertation text** with reliable 802.11p sources: (a) Jiang & Delgrossi, "IEEE 802.11p: Towards an International Standard for Wireless Access in Vehicular Environments", IEEE VTC-Spring 2008 (add to bib); (b) the IEEE 802.11p-2010 amendment or IEEE 802.11-2020 OCB clauses; (c) optionally ETSI EN 302 663 (ITS-G5 access layer). Keep the old key only until chapters are rewritten |
| `kong2004EDCA` | No open PDF found (IEEE paywall); metadata verified via HKUST repository + DOI (matches bib exactly) | Keep; cite for the EDCA analytical model (virtual collision, AIFS, CW differentiation, mean access delay) |
| `ni2004Qiang`, `romdhani2003AdaptiveEDCF` | No open PDF found (Wiley/IEEE paywalls); metadata verified via publisher pages (both match bib) | Keep; cite from abstract-level claims or obtain via library access |
| `IEEE80211`, `IEEE80211e_2005`, `ieee1609_4` | Standards paywalled (802.11-2020 free via IEEE GET with account) | Cite normatively as standard practice; obtain via IEEE GET/library if quoting clauses |
| `CV2X_Sidelink_Allocation` | IEEE paywall (MIUCC 2025) | Keep for Related Work; verified via ETFA/SBESC usage |

## Minor bib improvements (safe to apply during Background rewrite)

- `kosekszott2012What`: add `volume = {27}, number = {6}, pages = {95--104}`.
- `Evolution_QoS_Mechanisms`: optionally add `eprint = {1411.2852}, eprinttype = {arxiv}` to record the accessible version.
- `TSNCtl_Feraudo`: fine as arXiv entry; do not describe as peer-reviewed in prose.

## Key citation chains (write-up ready)

- **Alert-class marking chain:** RFC 2474 §3/§4.1 (DSCP field; DSCP 0 = BE) → RFC 3246 §2.7 (DSCP 46 = EF) → RFC 4594 §4.1 (inelastic delay/loss-intolerant traffic → Telephony class → mark EF, pre-mark at end point) → RFC 8325 §2.3 + §4.2.1 (default mapping sends EF to AC_VI; explicit EF→UP 6/AC_VO recommended).
- **Hostile-channel chain:** RFC 9119 §3.1.1–3.1.3 (multicast: no ACK/retry, basic rate, airtime cost) + RFC 8325 §2 (EDCA cannot provide EF/strict priority) + Bianchi §VII (throughput collapse with station count) + Wu et al. (continuous backoff freezing inflates 802.11p delay) → justifies going beyond plain EDCA.
- **Statistical-not-guaranteed chain:** Kosek-Szott §2.1 ("EDCA cannot guarantee any throughput or delay bounds") + Mangold Fig. 10 (unbounded EDCA delay) + Malik §III-C3/§IV-A (strict priority starves; differentiation fails beyond a load limit).
- **Requirements anchor:** 3GPP TS 22.186 Table 5.2-1 [R.5.2-004]: 25 ms end-to-end, 90% reliability, 300–400 B, 30 msg/s (platooning, lowest automation degree).
- **DCC contrast:** ETSI TS 102 687 V1.2.1 — CBR-driven TPC/TRC acting continuously on aggregate load vs the dissertation's event-triggered per-class suppression.
