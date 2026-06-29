# Bibliography guide

Single database: `aftertext/references.bib` (biblatex/abnt).

## Tier 1 — Core (must cite in main narrative)

| Key | Chapter / use |
|-----|----------------|
| `IEEE_80211p_Survey` | Intro, Background — vehicular Wi-Fi motivation |
| `IEEE80211`, `IEEE80211e_2005` | Background — DCF/EDCA standards |
| `bianchi2000DCF`, `kong2004EDCA`, `mangold2003QoS` | Background — DCF/EDCA analysis |
| `ni2004Qiang`, `kosekszott2012What`, `Evolution_QoS_Mechanisms` | Background, Related Work — QoS surveys |
| `RFC2474_DSField`, `RFC2475_DiffServ_Architecture` | Background — DiffServ |
| `RFC3246_EF_PHB`, `RFC4594_DiffServ_Service_Classes` | Background — EF semantics |
| `RFC8325_WiFi_QoS` | Background, Implementation — DSCP→UP mapping |
| `RFC9119_Multicast_IEEE802_Wireless` | Background — multicast limits |
| `Continuous_Backoff_Freezing_Li` | Background, Related Work — 802.11p delay under load |
| `romdhani2003AdaptiveEDCF`, `SkipCCH_Garrido` | Related Work — adaptive MAC contrast |
| `TSNCtl_Feraudo`, `PRP_MAC_Li`, `CFC_MAC_Linn`, `CV2X_Sidelink_Allocation` | Related Work — stronger alternatives |
| `11288825` | Related Work — prior SBESC2025 work (wireless TSN precursor) |
| `aguiar2026_veins_qos` | Implementation, Evaluation — software artifact |

## Tier 2 — Tools (Implementation / Methodology)

| Key | Use |
|-----|-----|
| `varga2008omnetpp`, `varga2010omnetpp` | OMNeT++ simulator |
| `inet_framework` | INET Framework |
| `sommer2015veins` | Veins V2X coupling |
| `lopez2018sumo` | SUMO mobility |
| `bengtsson1995uppaal` | UPPAAL verification (optional section) |
| `inet_ideal_obstacle_loss` | Propagation model documentation |

## Tier 3 — Contrast only (Related Work subsection)

| Key | Topic |
|-----|-------|
| `3gpp_ts_22_261_r18` | URLLC requirements (intro motivation) |
| `vardakas2007end` | DCF delay analysis (optional background) |
| `ieee8021qbv`, `modeling`, `debnath2023mixed`, `craciunas2016` | Wired TSN |
| `qosaware`, `nesting`, `mate2022asynchronous` | TSN simulation/orchestration |
| `seliem2023wirelesstsn`, `satka2023wireless`, `schneider2022twt` | Wireless TSN |
| `karthik2018`, `dovelos2020`, `schneider_mu_edca_2023`, `schneider_trigger_2024`, `yamakata2024` | Wi-Fi 6 OFDMA determinism |
| `ieee1609_4`, `etsi_dcc_102687` | V2X standards baselines (not modeled) |
| `rfc9320_detnet` | DetNet contrast — do not claim DetNet properties |

## Deprecated keys (do not cite for active contribution)

- `veins_inet_qos_2026` — replaced by `aguiar2026_veins_qos` (use after chapter pivot)
- `seliem2023wireless` vs `seliem2023wirelesstsn` — legacy intro cites `seliem2023wireless`; ETFA pivot prefers `seliem2023wirelesstsn`
- `ieee80211e` vs `IEEE80211e_2005` — legacy intro uses `ieee80211e`; ETFA pivot uses `IEEE80211e_2005`

## ETFA → dissertation key mapping

| ETFA key | Dissertation key |
|----------|------------------|
| `veins_inet_qos_2026` | `aguiar2026_veins_qos` |
| (all others) | same key |

## Adding new references

1. Drop PDF in `ref_papers/Analysis/`
2. Run workflow in `REF_PAPERS_WORKFLOW.md`
3. Update this guide with the new key and intended chapter
