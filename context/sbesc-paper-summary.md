# SBESC 2026 paper summary (for dissertation context)

Source: `../SBESC-2026-Paper/text.tex` — **primary short-paper source for the dissertation** (latest, post-DSD-review rewrite of the same study as ETFA).

## Title

*Crash-Aware Traffic Prioritization in Vehicular Wi-Fi: A Simulation Study of Channel Access and Adaptive Blocking*

Authors: Gabriel de O. Aguiar, Enzo Nicolás Spotorno, Giovani Gracioli (LISHA/UFSC). Named authorship (ETFA copy is anonymized).

## Section structure

1. **Introduction** — V2X motivation, DSCP+EDCA path, gap for local event-driven prioritization, three contributions
2. **Background and Related Work** (merged)
   - II-A Contention-Based Vehicular Access and EDCA — 802.11p/DCF, EDCA ACs, DSCP 46/EF mapping ambiguity, multicast limits
   - II-B Related Work — TSNCtl, PRP-MAC, CFC-MAC, NR-V2X sidelink, prior SBESC2025 work, backoff freezing, SkipCCH, adaptive EDCA + DCC positioning
3. **System Model and Implementation** (merged)
   - III-A Network, Traffic, and Event Model — decentralized one-hop multicast, two-class abstraction, crash timeline
   - III-B MAC Policies — five policies, three-mode controller (listening/blocking/sending)
   - III-C Implementation and Scope — OMNeT++ 6.1 / INET 4.5.2 / Veins artifact, layer-mapping table, PHY simplifications
4. **Evaluation** — setup, metrics/aggregation, light-density sweep, heavy-density stress, expanded discussion
5. **Conclusion** — conditional takeaway: marking as default; blocking as event-triggered escalation with auth/rate-limit prerequisites

## Deltas vs ETFA paper

Same experiments, policies, scenarios, and numbers — **not** a new campaign. SBESC differs by:

- Condensed structure (merged Background+Related Work; System+Implementation)
- Abstract leads with the ~49% VO P95 result and protection-versus-cost takeaway
- Two figures in text (timeline + VO CDF); `system_model_architecture.pdf` unused (still available for the thesis)
- Expanded Discussion (responses to DSD 2026 reviews, see `../SBESC-2026-Paper/DSD2026_REVIEW.md`):
  - plain-policy BE/VO sampling caveat (different traffic processes, not MAC treatment)
  - practical significance vs 3GPP TS 22.186 25 ms platooning budget (`ts22186`)
  - protection cost / coarse binary BE class as worst-case bound
  - spatial concentration of the BE penalty near the crash source
  - DoS risk of unauthenticated VO-triggered suppression; deployment prerequisites
  - fuller limitations paragraph (3 seeds, no CIs, single crash source, simplified PHY, no DCC baseline, fixed non-ablated profiles)
- New citations vs ETFA: `etsi_dcc_2018`, `ts22186`, `omnet1`, `veins_sommer2011`, `sumo_lopez2018`
- Dropped vs ETFA: DiffServ RFCs 2474/2475/4594, `mangold2003QoS`, `ni2004Qiang` (dissertation Background should restore these from ETFA)

## Citation keys used in SBESC (~24)

`IEEE80211`, `IEEE80211e_2005`, `IEEE_80211p_Survey`, `RFC3246_EF_PHB`, `RFC8325_WiFi_QoS`, `RFC9119_Multicast_IEEE802_Wireless`, `bianchi2000DCF`, `kong2004EDCA`, `kosekszott2012What`, `romdhani2003AdaptiveEDCF`, `Continuous_Backoff_Freezing_Li`, `Evolution_QoS_Mechanisms`, `TSNCtl_Feraudo`, `PRP_MAC_Li`, `CFC_MAC_Linn`, `CV2X_Sidelink_Allocation`, `SkipCCH_Garrido`, `etsi_dcc_2018`, `ts22186`, `11288825`, `omnet1`, `veins_sommer2011`, `sumo_lopez2018`, `veins_inet_qos_2026`

SBESC → dissertation key mapping (duplicates under different names):

| SBESC key | Dissertation key |
|-----------|------------------|
| `omnet1` | `varga2008omnetpp` |
| `sumo_lopez2018` | `lopez2018sumo` |
| `veins_inet_qos_2026` | `aguiar2026_veins_qos` |
| `veins_sommer2011`, `etsi_dcc_2018`, `ts22186` | same key (added to `aftertext/references.bib`) |
| (all others) | same key |

## Figures

- `../SBESC-2026-Paper/figures/event_timeline_cropped.pdf` — Fig. 1, crash timeline (copy in `Figs/`)
- `../SBESC-2026-Paper/figures/eval/fig_06_vo_delay_cdf_high_load_highway_heavy.pdf` — Fig. 2, VO delay CDF (copy in `Figs/`)
- `../SBESC-2026-Paper/figures/system_model_architecture.pdf` — unused in SBESC, used in ETFA (copy in `Figs/`)

## Experiment matrix

| Dimension | Values |
|-----------|--------|
| Density | light (10 vehicles), heavy (100 vehicles) |
| Load | `netload_low` / `medium` / `high` |
| MAC | `plain`, `edca_only`, `edca_v2x_vo_stable`, `edca_v2x_vo_guarded`, `edca_v2x_vo_emergency` |
| Seeds | 5 (light), 3 (heavy) |
| Sim time / crash | 70 s; crash at 30 s for 30 s, node index 0 |

Policy knobs (block window / max continuous block / send guard / VO threshold): stable 15/80/5 ms, thr 2; guarded 4/20/4 ms, thr 3; emergency 10/60/5 ms, thr 1 + `emergencyPreemption=true`.

## Key numeric anchors (heavy, high load, 3-run means)

| Policy | VO mean (ms) | VO P95 (ms) | VO jitter (ms) | BE mean (ms) | BE P95 (ms) | VO RX/alert | BE RX/TX |
|--------|--------------|-------------|----------------|--------------|-------------|-------------|----------|
| plain | 0.575 | 1.290 | 0.321 | 27.589 | 57.367 | 9.068 | 6.153 |
| edca_only | 0.433 | 0.896 | 0.193 | 54.760 | 155.857 | 9.904 | 6.147 |
| stable | 0.469 | 1.155 | 0.261 | 59.434 | 144.314 | 9.826 | 5.534 |
| guarded | 0.443 | 0.960 | 0.207 | 74.938 | 174.401 | 9.778 | 3.644 |
| emergency | **0.282** | **0.461** | **0.047** | 60.664 | 98.663 | 9.912 | 5.021 |

MAC drops ×10³ (total / BE qdrop): plain 281/0, edca 251/31, stable 340/47, guarded 485/197, emergency 273/65 (+22×10³ explicit BE drops under protection, 112 VO protection activations).

Light density, high load, normalized vs `plain_netload_high`: emergency VO P95 **−37.6%**, VO mean −17.2%; EDCA/stable/guarded VO slightly worse (+2 to +17%); all policies inflate BE delay by +4855% to +9666%.

Heavy P95 ladder across loads: at `low`, VO P95 identical (0.185 ms) for all policies while stable/guarded inflate BE P95 to ~28 ms; at `medium`, emergency BE P95 is 35.9 ms; at `high`, emergency VO P95 0.461 ms is the minimum, guarded BE P95 174.4 ms the maximum.

## Dissertation usage notes

- Port SBESC prose first; restore ETFA's DiffServ background where SBESC condensed it.
- All seven discussion points (see `WRITING_ROADMAP.md`) must appear in the dissertation Evaluation.
- Do not cite results absent from the artifact or the papers; heavy KPIs are 3-seed means without confidence intervals.
