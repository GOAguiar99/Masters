# Background chapter plan (`chapters/1-chapter.tex`, prints as Chapter 2)

**Goal:** replace the legacy TSN-only outline with a dissertation-scale Background that gives a reader everything needed to understand the crash-aware study: vehicular safety messaging and its budgets, 802.11 channel access, EDCA and its limits, 802.11p specifics, the DSCP-to-air-interface path, multicast limitations, and the simulation toolchain.

**Sources:** SBESC §II-A as the skeleton (tight prose), expanded with ETFA §Background (DiffServ RFC path) and the verified claims in [reference-notes.md](reference-notes.md). Size is not constrained (dissertation, not paper): target 12–18 pages.

**Reference base:** all claims below are backed by PDFs in `ref_papers/Relevant/` and the citation chains in [reference-notes.md](reference-notes.md). Cite section anchors from there.

---

## Section architecture

### 2.1 Vehicular Safety Communication and Its Requirements (~2 pages)

Purpose: motivate why timely delivery matters and what "timely" means, before any MAC detail.

- Cooperative ITS and V2X message classes; event-driven safety alerts vs periodic awareness traffic.
- Why broadcast/multicast one-hop dissemination is the natural primitive for safety messages (`Continuous_Backoff_Freezing_Li` §1; RFC 9119 §1 framing).
- Quantified budgets: 3GPP TS 22.186 Table 5.2-1 — cite [R.5.2-004] 25 ms / 90% / 300–400 B / 30 msg/s (platooning, lowest automation) plus one or two harsher rows for higher automation (`ts22186`). One sentence on 5G service requirements deferring V2X KPIs to TS 22.186 (`3gpp_ts_22_261_r18`).
- Positioning: 802.11p as the decentralized, infrastructure-free access technology this work targets — cite the 802.11p reference (see bib action below; **do not lean on `IEEE_80211p_Survey`**).

### 2.2 IEEE 802.11 Distributed Channel Access (~3 pages)

Purpose: the DCF baseline (= `plain` policy) and why contention degrades under load.

- 2.2.1 **DCF and CSMA/CA**: carrier sensing, DIFS, binary slotted exponential backoff, retransmission; backoff freezing as a *baseline* DCF mechanism (`bianchi2000DCF` §II; `IEEE80211`).
- 2.2.2 **Saturation behavior**: Bianchi's 2-D Markov model; saturation throughput; throughput decays as station count grows; collision cost of basic access (`bianchi2000DCF` §IV, §VII). One paragraph, no equations reproduced beyond the essentials — this dissertation does not build an analytical model.
- 2.2.3 **Fixed parameters are suboptimal**: optimal contention window depends on network size, but CWmin/m are fixed by the standard → adaptive approaches are a natural response (`bianchi2000DCF` §VI). This is the earliest hook for the adaptive-policy idea.
- 2.2.4 **No differentiation**: "all stations operate with the same CWmin … no QoS support in the DCF" (`mangold2003QoS` p. 41; RFC 8325 §6.1).

### 2.3 Quality of Service in 802.11: EDCA and Its Limits (~3–4 pages)

Purpose: the `edca_only` policy and the core argument that EDCA is statistical.

- 2.3.1 **802.11e HCF**: EDCA (contention-based) + HCCA (polling); TXOP concept (`mangold2003QoS`; `IEEE80211e_2005`; `IEEE80211` for the current consolidated standard).
- 2.3.2 **EDCA mechanics**: four ACs (VO/VI/BE/BK) as parallel backoff entities; AIFS[AC], CWmin/CWmax[AC], TXOP[AC]; internal (virtual) collisions resolved in favor of higher AC (`mangold2003QoS`; `kong2004EDCA` for the analytical treatment incl. virtual collision and mean access delay; RFC 8325 §6.2.2–6.2.4 for the UP→AC and parameter tables). Caveat from notes: do not cite Mangold's draft-D5.0 parameter values as the final standard's.
- 2.3.3 **Statistical, not guaranteed**: higher ACs win on average but still contend randomly; delay "increases unpredictably" with load (`mangold2003QoS` Fig. 10); "EDCA cannot guarantee any throughput or delay bounds, only differentiation" (`kosekszott2012What` §2.1); differentiation collapses beyond a load limit and strict priority can starve low-priority traffic to zero throughput (`Evolution_QoS_Mechanisms` §III-C3, §IV-A). The starvation citation is double-edged and should be framed as such: the adaptive policies *deliberately* impose a bounded version of this effect.
- 2.3.4 **Adaptive EDCA lineage**: parameter retuning to observed traffic (`romdhani2003AdaptiveEDCF`; survey classification in `ni2004Qiang`, `Evolution_QoS_Mechanisms`). One short subsection — full contrast belongs in Related Work.
- 2.3.5 **Later QoS amendments and the multicast gap**: 802.11aa GATS/GCR and SCS, 802.11ae management-frame prioritization (`kosekszott2012What` §3–4) — evidence that standard group-addressed QoS remained an acknowledged gap; these amendments target infrastructure WLANs, not OCB.

### 2.4 IEEE 802.11p and Vehicular Ad Hoc Operation (~2–3 pages)

Purpose: the concrete radio/MAC environment of the study.

- OCB (outside the context of a BSS) operation: no association, no AP, no centralized coordination; 5.9 GHz, 10 MHz channels (new reliable 802.11p reference + `IEEE80211`).
- WAVE/1609.4 multi-channel note, one paragraph, as context only (`ieee1609_4`) — the study uses a single channel.
- EDCA in 802.11p and broadcast frames: group-addressed transmission without ACK/retransmission → priority markings still contend, and losses are invisible to the sender (RFC 9119 §3.1.1 facts, applied to OCB; `kosekszott2012What` §3.1).
- Delay under load: continuous backoff freezing inflates 802.11p delay; delay and PDR degrade with vehicle density (`Continuous_Backoff_Freezing_Li` — cite trends, not their absolute values).
- **DCC**: ETSI TS 102 687 — CBR-driven transmit power/rate/access control, reactive and adaptive variants, acting *continuously on a station's aggregate offered load* (`etsi_dcc_2018`). Close with the contrast sentence: the mechanism studied here intervenes only while a crash alert is active, so it complements rather than replaces DCC (mirrors SBESC §II-B wording).

### 2.5 From DSCP to the Air Interface (~3 pages)

Purpose: the exact standards path the `QosClassifier` implements. This is the most dissertation-specific background section.

- 2.5.1 **DiffServ architecture**: DS field/DSCP definition; per-hop behaviors; classification at boundaries incl. source hosts; unmapped codepoints fall back to Default (RFC 2474 §3, §4.1; RFC 2475 §2.3.1, §2.4, §2.3.4.1).
- 2.5.2 **EF and DSCP 46**: EF PHB as the low-delay/low-loss building block; codepoint 101110 = 46 (RFC 3246 §2.7); Telephony service class guidance — inelastic, delay/loss-intolerant traffic should be EF-marked at the end point and served by priority queuing (RFC 4594 §4.1). Frame the crash-alert analogy honestly: alerts are not telephony, but match the class's defined characteristics.
- 2.5.3 **Mapping DiffServ to 802.11**: no standard default DSCP→UP mapping; common 3-MSB practice sends EF (46 → UP 5) to AC_VI, not AC_VO; RFC 8325 recommends EF→UP 6/AC_VO (RFC 8325 §2.3, §4.2.1). The DSCP→UP→AC causal chain (§6.2.1). Include the honesty clause: 802.11 cannot provide a true EF service because of random contention (§2) — this is precisely why the study adds adaptive suppression on top of correct mapping. Optionally note the marking-abuse DoS vector (§8.2) forward-referencing the Discussion.
- 2.5.4 **Multicast over 802.11**: no ACK, no retransmission, no loss-driven backoff, basic-rate transmission, airtime cost (RFC 9119 §3.1.1–3.1.3); AP-based mitigations (DMS, GCR) do not apply in OCB → the crash alert inherits all of this. Table or short list summarizing which reliability tools are unavailable in the study's setting.

### 2.6 Simulation of Vehicular Networks (~1.5 pages)

Purpose: background for the toolchain (detailed module description stays in the Implementation chapter).

- Discrete-event network simulation with OMNeT++/INET (`varga2008omnetpp`, `inet_framework`).
- Why bidirectional network-mobility coupling matters for IVC studies; Veins architecture, TraCI (`veins_sommer2011`).
- SUMO microscopic mobility (`lopez2018sumo`).

### 2.7 Summary (~0.5 page)

- Recap the three background pillars: (i) safety alerts have millisecond-scale budgets but ride on contention-based access; (ii) EDCA gives statistical priority only, and correct DSCP→AC mapping is not automatic; (iii) multicast alerts get no link-layer reliability, and standardized remedies (802.11aa, DCC) either do not apply to OCB or act on aggregate load. Close by pointing to Related Work (stronger mechanisms) and the System Model (the five-policy ladder).

---

## Reference map (section → keys)

| Section | Primary keys | Supporting keys |
|---------|--------------|-----------------|
| 2.1 | `ts22186`, new 802.11p ref | `3gpp_ts_22_261_r18`, `Continuous_Backoff_Freezing_Li`, `RFC9119_Multicast_IEEE802_Wireless` |
| 2.2 | `bianchi2000DCF`, `IEEE80211` | `mangold2003QoS`, `RFC8325_WiFi_QoS` |
| 2.3 | `mangold2003QoS`, `kosekszott2012What`, `Evolution_QoS_Mechanisms` | `kong2004EDCA`, `IEEE80211e_2005`, `romdhani2003AdaptiveEDCF`, `ni2004Qiang` |
| 2.4 | new 802.11p ref, `etsi_dcc_2018`, `Continuous_Backoff_Freezing_Li` | `ieee1609_4`, `IEEE80211`, `RFC9119_Multicast_IEEE802_Wireless` |
| 2.5 | `RFC2474_DSField`, `RFC3246_EF_PHB`, `RFC4594_DiffServ_Service_Classes`, `RFC8325_WiFi_QoS`, `RFC9119_Multicast_IEEE802_Wireless` | `RFC2475_DiffServ_Architecture` |
| 2.6 | `veins_sommer2011`, `lopez2018sumo`, `varga2008omnetpp` | `inet_framework` |

## Bibliography actions before/while writing

1. **Add a reliable 802.11p reference** and stop using `IEEE_80211p_Survey` in new text (defunct publisher, bogus DOI in circulation — see [reference-notes.md](reference-notes.md)). Candidates: Jiang & Delgrossi, "IEEE 802.11p: Towards an International Standard for Wireless Access in Vehicular Environments," IEEE VTC-Spring 2008, DOI 10.1109/VETECS.2008.458; optionally ETSI EN 302 663 (ITS-G5 access layer). Add entries + fetch PDFs into `ref_papers/`.
2. Add `volume = {27}, number = {6}, pages = {95--104}` to `kosekszott2012What`.
3. Optionally add `eprint`/`eprinttype` to `Evolution_QoS_Mechanisms` (local PDF is the arXiv version; version-of-record is JNCA 2015 — re-verify verbatim quotes).
4. Keep `TSNCtl_Feraudo` described as a preprint wherever mentioned.
5. Legacy TSN keys (`ieee8021qbv`, `seliem2023wirelesstsn`, OFDMA cluster, etc.) do **not** enter the Background — they stay confined to the Related Work TSN-contrast subsection per the guardrail.

## Guardrails for the writing pass

- No deterministic/worst-case claims anywhere; EDCA and all five policies provide statistical service (`kosekszott2012What` §2.1 is the anchor).
- Attribute normative force only to Standards-Track documents (RFC 2474/3246/8325); describe RFC 2475/4594/9119 as architecture/guidelines/operational analysis.
- RFC 8325 and RFC 9119 are written for infrastructure WLANs: carry over the mechanics/facts, never the AP-based recommendations, and say so once.
- Cite trends, not absolute values, from `Continuous_Backoff_Freezing_Li` (their load is far lighter than the study's).
- Keep BE / VO / DSCP 46 / EF / UP 6 / AC_VO distinct: DSCP 46 is the codepoint, EF the PHB, UP 6 the 802.11 user priority, AC_VO the EDCA queue.
- Terminology set once in 2.2–2.3 and reused verbatim in System Model: AIFSN, CWmin/CWmax, TXOP, backoff freezing, virtual collision.

## Suggested writing order

1. 2.5 (DSCP path) — most self-contained, all anchors verified.
2. 2.2 + 2.3 (DCF, EDCA) — port SBESC §II-A skeleton, expand with Bianchi/Mangold/Kosek-Szott/Malik claims.
3. 2.4 (802.11p + DCC) — needs the new 802.11p reference added first.
4. 2.1 (requirements) — short, uses TS 22.186 anchors.
5. 2.6 + 2.7 (tools, summary).
6. Then delete the legacy TSN outline and commented blocks from `chapters/1-chapter.tex` and rebuild with `./compile.sh`.
