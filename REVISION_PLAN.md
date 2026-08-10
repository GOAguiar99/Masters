# Final Revision Plan — "Crash-Aware Traffic Prioritization in Vehicular Wi-Fi Networks"

> **Implementation status (branch `revision/final-audit-fixes`, 2026-08-10):**
> Implemented — C3 (URL), C4 (INET 4.5.4 + Veins 5.3.1, verified against upstream release commits), C5 (VO MAC drops relabel, n.a. for plain), H1 (÷2 heuristic disclosed in §6.2), H2 (straight corridor), H3 (INET-default footnotes; 12 Mbit/s fastest-mandatory data rate verified in INET v4.5.4 `RateSelection.cc`/`Ieee80211ModeSet.cc`), H4 (OCB approximation + BSS-vs-OCB EDCA caveat, in §5.8.4 and §6.5.7), H5 (FSM trigger semantics + extra transitions), H7/L5/L6 (bib repairs, 15 entries pruned), M1, M2, M3, M4, M5, M7, M8, M9, L1, L2, L4.
> **Deferred** — C1 (figures; placeholders intentionally left, per author), C2 + H6 (require re-running the simulation matrix), CV2X_Sidelink_Allocation title verification (flagged with a note in the .bib), M6/LICENSE (separate PR on `veins-inet-qos`), M10 (recheck after figures land).

**Audit date:** 2026-08-10.
**Sources audited:** `Masters/` (all chapters, front matter, bibliography, build log, figures) cross-checked against `veins-inet-qos` (simulation source, `omnetpp.ini`, SUMO files, `run_matrix.sh`, Rust KPI dashboard, git state) and external primary sources (RFC 8325, RFC 9119, 3GPP TS 22.186, arXiv 2405.01301, GitHub, INET release history).

Chapter numbering used below = printed numbering: Ch.1 Introduction (`0-Intro.tex`), Ch.2 Background (`1-chapter.tex`), Ch.3 Related Work (`2-chapter.tex`), Ch.4 System Model (`3-chapter.tex`), Ch.5 Implementation (`4-chapter.tex`), Ch.6 Evaluation (`5-chapter.tex`), Ch.7 Conclusion (`6-chapter.tex`).

---

## Executive Assessment

The dissertation is in substantially better shape than most near-final manuscripts. The technical narrative (problem → gap → two-class model → five-policy ladder → protection-versus-cost frontier → conditional takeaway) is coherent, the claims are carefully hedged (statistical-not-deterministic, headroom-not-safety-outcome, no superiority over DCC), and the Implementation chapter matches the code to an unusually high degree: **every adaptive-controller knob, EDCA parameter, load profile, timing value, port, and counter I checked in `omnetpp.ini` and the C++ sources matches Table `tab:impl:parameters` and the surrounding text exactly.** The metric definitions in §6.2 also match the Rust KPI pipeline (P95/jitter pooled over all receivers' vectors; means weighted by count) — notably, the repo's own `AUDIT_REPORT.md` is *wrong* about this ("node[0] only"), and the dissertation is right.

The risks are concentrated in four places:

1. **Seven unfinished figure placeholders** in Chapters 2–3. The document cannot be submitted as-is.
2. **Evidence chain to the numbers.** The repository contains **zero result files** (`results/` directories are empty, no `.sca`/`.vec`, no KPI cache anywhere in the tree), no `repeat`/seed configuration matching the claimed "five seeds (light) / three seeds (heavy)", and the figure PDFs in `Masters/Figs` come from **two different export runs** (Aug 2 vs Aug 10). Every number in Chapter 6 is currently unverifiable and unreproducible from the artifact.
3. **Broken artifact identity.** The cited artifact URL (`github.com/aguiar/veins-inet-qos`) is a 404; the real repo is `github.com/GOAguiar99/veins-inet-qos`. The pinned INET submodule is the **4.5.4** release commit, not the **4.5.2** claimed throughout. The repo has no LICENSE file despite the "open-source artifact" contribution claim.
4. **One mislabeled metric.** The "VO incomplete" column (Table `tab:eval:heavy_vo_loss`) does not exist in the pipeline; the values are the VO-attributed MAC drop counts — a MAC-layer quantity (including receive-side corrupted-frame drops, and passed through an undisclosed ÷2 de-duplication heuristic in the parser), presented as "incomplete Voice receptions … at the application view."

None of these undermines the scientific contribution, but items 2–4 would fail an artifact evaluation and could unravel during a defense question ("show me the run that produced Table 6.2"). They are all fixable in days, mostly by re-running the matrix with documented seeds and archiving outputs.

---

## Critical Fixes (must be done before submission)

**C1. Produce the seven missing figures (Ch.2 ×5, Ch.3 ×2).**
`1-chapter.tex:82` (`fig:bg:dcf-backoff`), `:143` (`fig:bg:edca-queues`), `:235` (`fig:bg:ocb`), `:285` (`fig:bg:dscp-path`), `:426` (`fig:bg:veins`); `2-chapter.tex:14` (`fig:rw:taxonomy`), `:153` (`fig:rw:always-vs-event`). Each placeholder already contains a precise drawing brief — execute them. Verification: no `\fbox{\parbox...placeholder` remains; List of Figures shows real figures.

**C2. Re-run the full experiment matrix with documented seeds and archive the evidence.**
Both `results/` trees are empty; no `.sca`, `.vec`, or KPI cache exists anywhere in `veins-inet-qos`; `omnetpp.ini` has no `repeat`/seed stanza; `run_matrix.sh` defaults to `RUNS=0` (one run). Yet §6.1 claims five seeds (light) and three seeds (heavy). Actions: (a) add `repeat = 5` / `repeat = 3` (or a documented `RUNS=0..N EXTRA_ARGS="--repeat=N"` invocation) to the packages or a campaign script; (b) run `PROFILE=full`; (c) archive `results/` (or at least the KPI `run_rows.json`/`config_summary.json` and exported tables) in the repo or a companion archive; (d) diff the regenerated KPI tables against every number in Tables `tab:eval:light`, `tab:eval:heavy_qos`, `tab:eval:heavy_vo_loss`, `tab:eval:heavy_drop_attr`, `tab:eval:heavy_ctrl`, `tab:eval:heavy_p95`, `tab:eval:heavy_drop_rate` and update any that changed; (e) record the exact artifact commit hash in the dissertation. Until this is done, all Chapter 6 numbers are **UNVERIFIED**.

**C3. Fix the artifact citation URL.**
`aftertext/references.bib:545` cites `https://github.com/aguiar/veins-inet-qos` → HTTP 404. The real, public repo is `https://github.com/GOAguiar99/veins-inet-qos` (verified). This is the dissertation's Contribution 2; a dead link to the claimed open-source artifact is disqualifying. Also add a LICENSE file to the repo — "open-source" (Ch.1 §Contributions, item 2) is not accurate without one.

**C4. Correct the INET version everywhere.**
Ch.5 states INET 4.5.2 (`4-chapter.tex:7,33`) and the bib note repeats it (`references.bib:485`). The submodule pins commit `0a1d409`, which is the **INET 4.5.4 release commit** ("prod: WHATSNEW update", Oct 29 2024); the v4.5.2 tag points to a different commit (`4e9a499`). Either state 4.5.4, or repin to the version actually used for the runs — and since C2 re-runs everything, verify version and text together. Same check for the Veins pin (`6571085`): state its version/commit in §5.1.1.

**C5. Rename and re-explain the "VO incomplete" metric.**
Table `tab:eval:heavy_vo_loss` (`5-chapter.tex:155-178`), §6.2 ("Voice incomplete receptions track crash-frame loss at the application view", `5-chapter.tex:44`), and §6.4.2 ("That Voice column matches the incomplete-reception counts…"). No "incomplete" metric exists in `kpi_dashboard` or the simulation source (grep-verified). The values (18/21/21/15 ×10³) are `mac_drop_vo_count` — VO-attributed **MAC-layer drops summed over all nodes**, including receive-side "incorrectly received" discards, after the parser's attribution heuristic. Fixes: (a) rename the column (e.g., "VO MAC drops"); (b) delete the "application view" sentence in §6.2; (c) rewrite the §6.4.2 sentence — the two columns "match" because they are the same number, which as written masquerades as corroboration; (d) replace Plain's bold **0** with "—/n.a." plus a footnote: under DCF all drops are unclassified, so a zero VO attribution is an artifact of the attribution scheme, not evidence of zero Voice loss (the caption "lower is better" currently invites exactly that misreading).

---

## High-Priority Fixes

**H1. Disclose (and verify) the drop-attribution ÷2 heuristic.**
`kpi_dashboard/src/lib.rs:899-908`: when BE+VO+unclassified attributed drops ≈ 1.9–2.1× the total `packetDrop:count`, the parser silently halves all attributed counts. Every per-AC drop number in Tables `tab:eval:heavy_vo_loss` and `tab:eval:heavy_drop_attr` may have passed through this. Actions: on the regenerated data (C2), confirm from a raw `.sca` whether double-counting actually occurs and why (likely the same `packetDropped` signal counted at two module levels); then either fix the counting at the source or document the correction in §6.2 in one sentence. An examiner who greps the parser will find this; the dissertation should find it first.

**H2. Remove the false "merge and exit geometry" claim.**
§5.8.3 (`4-chapter.tex:619`) describes the SUMO network as having "merge and exit geometry". `highway.net.xml` (both packages) is a straight 5 km bidirectional corridor: two edges (3 lanes each) and two end junctions — no ramps, merges, or exits. Rewrite as "a straight bidirectional corridor of 5 km with three lanes per direction". Also fix Table `tab:impl:parameters` "Corridor: 5 km, 3 lanes" → "3 lanes per direction (6 total)".

**H3. Mark the radio-parameter values as framework defaults and state the data rate.**
Table `tab:impl:parameters` reports "SNIR 4 dB; sens. −85 dBm; noise −110 dBm; free-space path loss" as if configured, but none of these appear in `omnetpp.ini` (verified; only opMode/band/channel/power/bandwidth/antenna/obstacle-loss are set) — they are INET defaults. Since the INET version is also in question (C4), verify each value against the pinned INET release NED files (submodules are currently uninitialized locally — `git submodule update --init` first) and add a table footnote "INET 4.5.x defaults, not overridden". Additionally, **no PHY data rate is stated anywhere** in the dissertation, even though Ch.2 makes basic-rate multicast a background pillar. Determine which mode/bitrate INET's rate selection actually used for the group-addressed frames in mode "p"/10 MHz (visible in the regenerated result files) and state it in §5.8.4. Status: **UNVERIFIED** until C2/C4 land.

**H4. Qualify the OCB and EDCA-parameter-set fidelity.**
Ch.2/Ch.4 frame the system as 802.11p **OCB**; the implementation is INET `AdhocHost` (ad hoc management, no association) with `opMode="p"` — a reasonable OCB approximation, but not a strict OCB implementation, and nothing in Ch.5 says so. Also, the configured EDCA set (AIFSN 7/3/2/2, CW 15-1023/15-1023/7-15/3-7) is the 802.11 **BSS QoS default**, whereas 802.11 specifies a different default EDCA parameter set when `dot11OCBActivated` is true (notably a less aggressive AC_BE; cf. IEEE 802.11-2020 OCB EDCA defaults / ETSI EN 302 663). Verify the exact OCB table against the standard, then add 2–3 sentences in §5.8.4 or §6.5.7: the study uses BSS-default EDCA parameters, and results could shift under the OCB default set (this mainly makes the BE class *more* aggressive than an OCB deployment would be, i.e., the protection problem harder — arguably conservative, and worth saying).

**H5. Align the FSM/trigger description with the code.**
Two mismatches with `V2xHcf.cc`/`V2xEdcaFsmController.cc`: (a) §4.3.1 (`3-chapter.tex:152`) says the controller leaves *listening* "when local Voice queue buildup **or overheard Voice-marked frames cross the activation threshold**" — in code, `voQueueThreshold` applies **only** to the local queue; a **single** overheard VO-classified frame immediately arms/extends protection (`V2xHcf.cc:267-270`, deliberate per code comment). Table `tab:impl:hooks` (Ch.5) already states it correctly; fix Ch.4. (b) The `fig:sys:fsm` transition strip shows only the cycle listening→blocking→sending→listening; the code also has listening→sending (own VO granted without prior threshold crossing), sending→blocking (guard expires while `blockingUntil` is in the future), and blocking→listening via the block timer. Add a footnote or extra arrows so the figure is not falsifiable from the source. Also, under `emergencyPreemption=true` the code switches to "any non-empty VO queue" (`hasAnyVoQueuePressure`) — with `voQueueThreshold=1` this is equivalent, but say it once if the threshold semantics are discussed.

**H6. Unify figure provenance.**
`Masters/Figs`: `fig_06_vo_delay_cdf...pdf` is from Aug 2; `fig_01`/`fig_05` (and the unused fig_02/03/04/07) from Aug 10, and the Aug 10 export produced **no** fig_06 (its SVG is absent — consistent with the `.vec` files being gone by then). The three Chapter 6 figures may therefore not come from the same dataset as the tables. After C2, re-export **all** figures in one run (`export_figures` over the archived results) and replace them wholesale. Verification: file timestamps identical; fig_01/fig_05 bar heights match Tables `tab:eval:heavy_qos`/`tab:eval:heavy_drop_attr`.

**H7. Bibliography repair (blocking-level items).**
- `lopez2018sumo` (`references.bib:500`): broken escapes `Fl{"o}tter{"o}d`, `L{"u}cken` → `Fl\"otter\"od`, `L\"ucken` (currently renders garbage).
- Duplicate pairs — keep one, delete the other, and normalize any keys: `IEEE80211e_2005` vs `ieee80211e`; `seliem2023wirelesstsn` vs `seliem2023wireless`; `schneider2022twt` vs `schneider2022proposal`; `veins_sommer2011` vs `sommer2015veins` (the latter is a corrupted variant: same title, wrong year/volume/DOI, wrong entry type — delete); `etsi_dcc_2018` vs `etsi_dcc_102687`.
- `CV2X_Sidelink_Allocation`: bib title says "6G V2x Sidelink", the text (§3.1.4) calls it "5G New Radio V2X (NR-V2X) … Mode 2". I could not locate the paper online (**UNVERIFIED**) — pull the actual PDF, fix title/venue, and reconcile the 5G/6G description in §3.1.4.
- `craciunas2016`: `@article` with `journal = {Proc. of the 24th RTNS}` → `@inproceedings` with proper `booktitle`.

---

## Medium-Priority Fixes

**M1. Discuss (or at least verify) the non-monotonic BE tail pattern in Table `tab:eval:heavy_p95`.**
At heavy density: stable/guarded blow up BE P95 at **low** load (27.8/28.2 ms) but are near-baseline at **medium** (1.57/0.50 ms), while emergency is clean at low (0.217 ms) but spikes at **medium** (35.9 ms). §6.4.3 discusses only the low-load row. The crossover is odd enough that it is either a real, interesting regime effect or a small-sample artifact (3 seeds, no CIs). After C2, check per-seed spread; then add 2–3 sentences either explaining or flagging it. Leaving an undiscussed anomaly in a headline table is a defense risk.

**M2. Support or soften the light-density low/medium claim.**
§6.3 asserts "At low and medium offered load, both access categories remain sub-millisecond for every policy" (light density) but no table/figure in the dissertation shows light low/medium data, and the repo has none. After C2, either add the ladder table (or an appendix) or write "remained sub-millisecond in our runs (not shown)". Currently **UNVERIFIED**.

**M3. Qualify the crash-burst overlap and the fleet-rate estimate.**
(a) At `netload_high`, a burst spans ~35 ms (8 repeats × 5 ms gap ± 2 ms jitter) but bursts start every 20 ms — bursts **overlap**, making VO effectively a sustained ~400 pkt/s stream during the window. §6.1's "up to eight physical Voice repeats every 20 ms" is literally correct but worth one clarifying clause, since "burst" suggests separated groups. (b) "near 800 packets/s fleet-wide" assumes all 100 vehicles are present; SUMO flows inject vehicles from t=1–95 s, so the fleet is still building at crash time (t=30 s). Add "as the fleet fills in" or verify the vehicle count at t≥30 s from the mobility trace.

**M4. State the aggregation order for P95 once, explicitly.**
Tables report "three-run means" of a per-run pooled P95 (mean-of-P95s), not a P95 over pooled seeds. §6.2 is compatible with both readings. One sentence: "per-run P95 over all receivers' samples, then averaged across seeds."

**M5. Resolve the UPPAAL hedge.**
§5.11 (`4-chapter.tex:744`): "An offline UPPAAL model … may exist in the broader artifact tree" — the repo's own audit says the `uppaal/` directory is absent, and it is. Delete the sentence (or reinstate the model). A dissertation should not speculate about its own artifact. (`bengtsson1995uppaal` is uncited — consistent with deletion.)

**M6. Update the repo's own documentation where it contradicts the code.**
`AUDIT_REPORT.md` §6 claims P95/jitter come from `Scenario.node[0].app[0]` only; `lib.rs:1590` matches `.app[0]` on **any** node (verified). Artifact reviewers will read that file and wrongly conclude the dissertation's metric description is false. Fix the repo doc, and initialize/document submodules in the README (`git submodule update --init`), since a fresh clone currently gets empty `inet/`/`veins/` trees.

**M7. Harmonize the "nine vs ten receivers" phrasing.**
§6.4.1 says "each alert reaches roughly nine receivers"; Table `tab:eval:heavy_vo_rx` caption says "near ten receivers"; §6.4.3 says "stays near ten". Values are 9.07–9.95. Pick one formulation ("about ten", or "9–10").

**M8. RFC 9119 wording.**
Ch.2 §"Multicast considerations" says "packet **error** rates of 5% or more are not uncommon"; RFC 9119 §3.1.1 says "packet **loss** rate of 5% or more" (verified against the RFC text). Match the source. All other RFC 8325/9119 quotes and claims checked out verbatim (including the EF-PHB honesty clause, the 3-MSB→UP 5→AC_VI pitfall, UP 6 recommendation, and the DoS-vector warning).

**M9. Give Table `tab:eval:heavy_ctrl` consistent precision/units.**
"BE hold 0.17" in a table whose caption says counts are ×10³ means 170 events — fine, but the mixed precision (integers elsewhere) reads like a typo. Either print 0.17 with a note or switch the column to raw counts.

**M10. Fix the oversized float.**
Build log: "Float too large for page by 13.45pt" (one of the big tables, likely `tab:rw:comparison` or `tab:impl:parameters`) plus 15 overfull hboxes. Rebuild after edits and clear these.

---

## Low-Priority / Polish

- **L1.** `1-chapter.tex:231`: sentence starts lowercase — "in \gls{ocb} mode, frames carry…" → "In OCB mode…".
- **L2.** `6-chapter.tex:67`: "the DSD-era limitations above" — internal project jargon (there is a `DSD2026_REVIEW.md` in the paper workspace); no reader can parse this. Replace with "the limitations above".
- **L3.** Committee placeholder page (`beforetext.tex:36-43`, "Prof.(a) xxxx") — expected pre-defense; on the final-version checklist.
- **L4.** `main.tex:151` `\tipotrabalho{Master's Thesis}` while the text says "dissertation" throughout; check the UFSC/abnTeX2 convention for master's ("Dissertação"/"Master's Dissertation") and make it uniform.
- **L5.** Unused bib entries (harmless with biblatex, but prune for hygiene): `vardakas2007end`, `rfc9320_detnet`, `dovelos2020`, `yamakata2024`, `mate2022asynchronous`, `nesting`, `qosaware`, `bengtsson1995uppaal`, `peha2023v2x_shared_unlicensed`, `varga2010omnetpp`, plus the duplicates listed in H7. Also delete the stale bib comment "Legacy draft citations (current chapters/*.tex until pivot rewrite)".
- **L6.** `Continuous_Backoff_Freezing_Li` title has "IEEE 802.11 p" (spurious space); `IEEE80211` entry carries a ~200-word `keywords` blob — trim.
- **L7.** Benign build warnings (babel 'brazil' deprecation, todonotes marginpar) — ignore or silence; no undefined references or citations (verified in `main.log`).
- **L8.** `Masters/Figs` contains ~15 legacy images (`both.png`, `noqos.png`, `delay.pdf`, …) not referenced by any chapter — archive them out of the submission tree to avoid confusion.

---

## Section-by-Section Revision Plan

### Ch.1 Introduction (`0-Intro.tex`)

**[Critical] §1.3 Contributions — artifact claim.**
- Problem: Contribution 2 cites `\cite{aguiar2026_veins_qos}` whose URL 404s; "open-source" without a license.
- Evidence: `references.bib:545`; `git remote` = `GOAguiar99/veins-inet-qos`; no LICENSE in repo root.
- Change: fix URL (C3), add LICENSE, optionally pin commit/DOI (Zenodo snapshot would be ideal for a dissertation).
- Reason: contribution claims must be checkable.
- Verification: URL resolves; LICENSE visible; commit hash printed in §5.1 or a footnote.

**[High] §1.3 Contribution 3 — "−49%" figure.**
- Problem: the −49% VO P95 number is currently backed by no archived data (C2); it is internally consistent with Table `tab:eval:heavy_qos` (0.896→0.461 ms = −48.5%).
- Change: after C2, reconfirm and keep "approximately −49%" or update.
- Verification: recomputed KPI table.

**[Low] §1.1–1.2.** No changes needed — scope, research question, and objectives match Ch.4–6 and the implementation (two-class model, five policies, 10/100 vehicles, three loads). Correct as written.

### Ch.2 Background (`1-chapter.tex`)

**[Critical] Figures — C1 (5 placeholders).**

**[Medium] §Multicast — M8 (loss vs error rate).**

**[Low] §OCB — L1 (lowercase "in").**

Everything else verified: RFC 2474/2475/3246/4594 summaries are accurate paraphrases; RFC 8325 quotes verbatim (verified); Kosek-Szott quote verbatim (verified against the published PDF); TS 22.186 R.5.2-004 numbers (25 ms / 90% / 300–400 B / 30 msg/s, lowest automation degree) verified against the ETSI-published spec, and the framing ("conservative reference bound, not the most stringent row") is exactly right; Bianchi/Mangold/Malik characterizations consistent with the cited works. The chapter's normative/informational RFC discipline (line 18) is a strength — keep.

### Ch.3 Related Work (`2-chapter.tex`)

**[Critical] Figures — C1 (2 placeholders: taxonomy, always-on vs event-triggered).**

**[High] §3.1.4 NR-V2X — H7 (5G vs 6G; UNVERIFIED citation).**
- Change: obtain the paper, fix bib entry, align the prose ("5G NR" vs "6G") with the actual paper.

**[Verified — no change] §3.1.1 TSNCtl**: arXiv 2405.01301 confirmed (title, authors, FSM + slot scheduling, 2 ms slots, collision-rate claim, preprint status). The "read as preliminary" caveat is appropriate and should stay.

**[Low] Table `tab:rw:comparison`**: check it is the float overflowing by 13.45 pt (M10).

### Ch.4 System Model (`3-chapter.tex`)

**[High] §4.3.1 + `fig:sys:fsm` — H5 (overheard-VO trigger has no threshold; missing transitions).**

**[Medium] §4.1 radio statement.**
- Problem: "reference transmit power, channel index, sensitivity, noise floor, and SNIR threshold are fixed for all policies and recorded … in `tab:impl:parameters`" — the sensitivity/noise/SNIR values are INET defaults, not bindings (H3).
- Change: no change needed here once the Ch.5 table is footnoted; optionally s/recorded/held at framework defaults recorded/.

**[Verified — no change]** Traffic model (exponential BE inter-arrivals, superimposed crash overlay, DSCP 0/46), event timeline (30 s crash, 30 s window, recovery with protection-window tail), policy ladder semantics, and the "no deterministic claims" scope all match `omnetpp.ini` and the C++ exactly.

### Ch.5 Implementation (`4-chapter.tex`)

**[Critical] §5.1.1 — C4 (INET 4.5.4 vs 4.5.2).**

**[High] §5.8.3 — H2 (no merge/exit geometry).**

**[High] §5.8.4 + Table `tab:impl:parameters` — H3 (defaults footnote; add data rate) and H4 (OCB/EDCA parameter-set caveat).**

**[Medium] §5.11 — M5 (UPPAAL sentence).**

**[Verified — no change] (highlights, all checked against source/ini):**
- Table `tab:impl:policyknobs` = `omnetpp.ini:133-168` exactly (stable 15/80/5/2; guarded 4/20/4/3; emergency preemption + 10/60/5/1).
- §5.7.2 EDCA bindings = ini lines 108–131 exactly (AIFSN 7/3/2/2; CW 15-1023/15-1023/7-15/3-7; queues 128/128/64/32; `edcaf[0]=BK…[3]=VO` matches INET's AccessCategory enum; MSDU aggregation cleared).
- Load-profile table = ini lines 74–102 exactly, and both density packages share a byte-identical ini as claimed (§5.8.2).
- Table `tab:impl:hooks` matches `V2xHcf.cc` precisely, including the subtle points: grant suppression and BE drops only under emergency; drop reason = congestion; `beRetryTimer` rearming at `blockingUntil`; signals `beDroppedWhileBlocked`/`beGrantSuppressedWhileBlocked`/`voProtectionActivation`; `v2xState` encoding 0/1/2.
- §5.5.1 `voDedupWindow` run-long semantics honestly disclosed (matches `CritPacketSender.ned:36` and code).
- §5.10.1 delay semantics (per-repeat `CreationTimeTag`, not logical burst time) match `CrashBurstApp.cc:175-177` — this was a known past pitfall and the text handles it correctly.
- §5.5.2 crash mechanics (TraCI `setSpeed(0)`/`setSpeed(-1)`, red icon, `targetNodeIndex`=0, −1 sentinel unused) match code.
- Packet path, ports (9001/9002→9001), multicast group, `HostAutoConfigurator`, TraCI manager settings, recording flags: all match ini.

### Ch.6 Evaluation (`5-chapter.tex`)

**[Critical] §6.1 seeds + all tables — C2 (no data in repo; seeds undocumented).**

**[Critical] §6.2 + Table `tab:eval:heavy_vo_loss` + §6.4.2 — C5 ("VO incomplete").**

**[High] §6.2/§6.4.2 — H1 (÷2 attribution heuristic).**

**[High] Figures `fig:eval:p95_gap_heavy`, `fig:eval:vo_cdf`, `fig:eval:drop_attr` — H6 (mixed-vintage exports; regenerate).**

**[Medium] Table `tab:eval:heavy_p95` — M1 (undiscussed medium-load emergency spike / low-load crossover).**

**[Medium] §6.3 — M2 (light low/medium sub-ms claim unshown).**

**[Medium] §6.1 — M3 (burst overlap; fleet build-up).** §6.2 — M4 (mean-of-P95 wording). §6.4.1/6.4.3 — M7 (nine vs ten). Table `tab:eval:heavy_ctrl` — M9 (0.17 precision).

**[Verified — no change]:**
- §6.2 metric definitions match `lib.rs`: P95/jitter pooled over **all** receivers' `app[0]` vectors (the repo's own AUDIT_REPORT is wrong, the dissertation right — fix the repo, M6); means weighted by count; VO RX/alert per **logical** TX; BE RX/TX; per-AC drop attribution; controller counters.
- Internal consistency of tables: drop-attr rows sum to totals (within rounding); "VO drops" column consistent between `tab:eval:heavy_vo_loss` and `tab:eval:heavy_drop_attr`; −49% = 0.896→0.461; figure axis ranges match table maxima (fig_01 ≈174 ms → tick 188; fig_05 ≈485k → tick 523k).
- §6.5 discussion subsections (plain-DCF sampling caveat, spatial concentration, DoS risk with 20–80 ms window bound, limitations) are accurate and well-hedged; the DoS window range "20–80 ms" matches the guarded/stable `maxContinuousBlock` bindings.

### Ch.7 Conclusion (`6-chapter.tex`)

**[Low] L2 ("DSD-era").**
**[Dependent] Numbers repeated from Ch.6 (0.90→0.46 ms, 0.047 ms jitter, 15 vs 18–21 ×10³, 57→99 ms) — update in lockstep with C2/C5 outcomes; the "fewest Voice-attributed MAC drops" phrasing must adopt the C5 renaming.**
Otherwise the conclusion claims exactly what the evaluation supports — no overclaiming found; keep.

### Front matter / template

**[Low] L3 (committee page), L4 (Thesis vs Dissertation).** Abstract/Resumo are consistent with the corrected numbers (update only if C2 changes them). Acronym list: entries used correctly; `TAS`, `GCR`, `WAVE` all resolve.

---

## Cross-Dissertation Consistency Checks

1. **Chapter numbering** — intro's roadmap (Ch.2 background … Ch.7 concludes) matches the compiled order. OK.
2. **Policy names** — `plain`/`edca_only`/`stable`/`guarded`/`emergency` used uniformly across Ch.1/4/5/6/7 and match ini config names. OK.
3. **Numbers repeated in Abstract/Resumo, Ch.1 (−49%), Ch.6, Ch.7 (0.90→0.46 ms, 0.047 ms, 57→99 ms, 15 vs 18–21 ×10³)** — all mutually consistent today; all must be revalidated together after C2.
4. **Seed counts** — "five seeds light / three heavy" appears in §6.1, §6.2, §7.3; keep synchronized with the campaign actually run (C2).
5. **Receiver-reach phrasing** — "nine" vs "ten" (M7).
6. **"3 lanes"** — Table `tab:impl:parameters` vs net.xml's 3+3 (H2).
7. **INET version** — Ch.5 (×2) + bib note (C4).
8. **VO metric naming** — "VO incomplete" (Ch.6 table+text) vs "Voice-attributed MAC drops" (Ch.6/7) must converge after C5.
9. **Terminology BE/VO expansions** — consistent via glossaries; DSCP 46/EF/UP 6/AC_VO chain used carefully (a strength — Ch.2 explicitly distinguishes them).
10. **Repo docs vs dissertation** — `AUDIT_REPORT.md` P95-scope claim contradicts both code and dissertation (M6); fix repo before artifact review.

---

## Citation Audit

**Verified accurate (no action):** RFC 8325 (all four load-bearing claims/quotes verbatim), RFC 9119 (three of four; see M8), RFC 2474/2475/3246/4594 paraphrases, TS 22.186 R.5.2-004, `kosekszott2012What` quote (verbatim; bibliographic data 2013/IEEE Network/27(6) correct), `TSNCtl_Feraudo` (arXiv 2405.01301 confirmed incl. the 2 ms slot claim and preprint status), `bianchi2000DCF`/`mangold2003QoS`/`kong2004EDCA`/`Evolution_QoS_Mechanisms` characterizations (consistent with the works; the two short Malik/Mangold quotes are plausible but not independently re-checked — **UNVERIFIED, spot-check the PDFs**), `veins_sommer2011`, `lopez2018sumo` (content; encoding broken per H7), `varga2008omnetpp`.

**Broken / must fix:** `aguiar2026_veins_qos` URL (C3); `lopez2018sumo` umlauts (H7); duplicates `IEEE80211e_2005`/`ieee80211e`, `seliem2023wirelesstsn`/`seliem2023wireless`, `schneider2022twt`/`schneider2022proposal`, `veins_sommer2011`/`sommer2015veins` (corrupted twin — delete), `etsi_dcc_2018`/`etsi_dcc_102687`; `craciunas2016` entry type (H7).

**Questionable / verify:** `CV2X_Sidelink_Allocation` (unlocatable; 5G-vs-6G mismatch with §3.1.4 — H7); `11288825` (author's own SBESC 2025 paper — presumably correct, but confirm the final DOI/pages once IEEE Xplore metadata is final); `IEEE_80211p_Survey` (obscure 2012 venue "Mobile Computing", SEIPUB) supports only one soft claim in Ch.1 — consider replacing with a stronger survey or the 802.11bd/11p literature; `3gpp_ts_22_261_r18` v18.16.0/2025 (plausible; verify version string).

**Missing citations (suggested, not mandatory):** §2.3.4 (802.11aa GATS/GCR, 802.11ae QMF) leans entirely on `kosekszott2012What` — citing the amendments themselves (IEEE 802.11aa-2012, 802.11ae-2012) would strengthen a standards-heavy chapter; §5.8.4/H3 data-rate statement will need the INET manual reference it already has (`inet_framework`).

**Primary-source discipline** is otherwise good: the dissertation already cites RFCs and standards directly rather than through secondary sources, and explicitly grades normative vs informational RFCs.

---

## Simulation ↔ Dissertation Verification Matrix

| Dissertation claim | Location | Repository evidence | Verified? | Action |
|---|---|---|---|---|
| Five policies; adaptive knobs 15/80/5/2, 4/20/4/3, 10/60/5/1 (+preemption) | Tab. `tab:impl:policyknobs` | `omnetpp.ini:133-168` | ✅ exact | — |
| EDCA AIFSN 7/3/2/2, CW 15-1023/…/3-7, queues 128/128/64/32; `edcaf[0]=BK` | §5.7.2 | ini:108-131; INET AC enum; `lib.rs` AC_INDEX_BE=1/VO=3 | ✅ | — |
| Load profiles (500/250/125 ms; 200/320/420 B; VO 120/75/20 ms, repeat 3/4/8…) | Tab. `tab:impl:parameters` | ini:74-102 | ✅ exact | — |
| 70 s horizon; crash 30–60 s; node 0 crash target; TraCI stop/resume | §5.8.5, Ch.4 | ini:3,21-22; `CrashBurstApp.cc:88-113,198-210` | ✅ | — |
| 10 / 100 vehicles; identical ini across densities | §5.8.2 | `highway.rou.xml` (1+9 / 1+99); diff of inis | ✅ | — |
| 5 km corridor, "merge and exit geometry" | §5.8.3 | `highway.net.xml`: straight, 2 edges, no ramps | ❌ geometry claim false | **H2** |
| SNIR 4 dB, sens −85 dBm, noise −110 dBm, free-space | Tab. `tab:impl:parameters` | not in ini; INET defaults (submodule uninitialized) | ⚠️ UNVERIFIED | **H3** |
| PHY data rate for multicast | (absent) | not set in ini; rate-selection default unknown | ⚠️ UNVERIFIED | **H3** |
| OCB operation | Ch.2/4 | INET AdhocHost + opMode "p" (approximation) | ⚠️ needs qualifier | **H4** |
| Classifier: DSCP 46→UP_VO, else UP 0; EDCA policies only | §5.6 | `QosClassifier.cc:65-74`; ini:117-119 | ✅ | — |
| Overheard-VO threshold semantics | §4.3.1 | `V2xHcf.cc:86-97,267-270`: single frame, no threshold | ❌ Ch.4 wording | **H5** |
| Emergency-only BE drop + grant suppression, congestion reason | Tab. `tab:impl:hooks` | `V2xHcf.cc:115-130,177-237` | ✅ | — |
| Per-repeat CreationTimeTag (delay excludes burst spacing) | §5.10.1 | `CrashBurstApp.cc:175-177` | ✅ | — |
| voDedupWindow run-long (no expiry) | Tab. `tab:impl:crit` | `CritPacketSender.cc:178-186`, `.ned:36` | ✅ | — |
| P95/jitter pooled over all receivers; means count-weighted | §6.2 | `lib.rs:584-635,869,1590` | ✅ (repo AUDIT_REPORT wrong) | **M6** |
| "VO incomplete" = application-view incomplete receptions | §6.2, Tab. `tab:eval:heavy_vo_loss` | no such metric; equals `mac_drop_vo_count` (÷2 heuristic) | ❌ | **C5, H1** |
| All Chapter 6 numerical values; 5/3 seeds | §6.1–6.4 | `results/` empty; no repeat/seed config; no cache | ⚠️ UNVERIFIABLE | **C2** |
| Figures = same dataset as tables | Ch.6 figures | fig_06 Aug 2 vs fig_01/05 Aug 10; no fig_06 in Aug 10 export | ⚠️ mixed vintage | **H6** |
| OMNeT++ 6.1 / INET 4.5.2 / Veins | §5.1.1 | repo README 6.1 ✅; inet pin = **4.5.4** release commit ❌; veins pin unversioned | ❌ INET | **C4** |
| Open-source artifact at cited URL | Ch.1 contrib. 2 | cited URL 404; real repo public; no LICENSE | ❌ | **C3** |
| Fig_01/fig_05 data ↔ tables | Ch.6 | SVG axis maxima 188 ms / 523 k consistent with 174.4 ms / 485 k | ✅ (sanity level) | full check after C2 |

---

## Final Submission Checklist

1. [ ] Draw and insert the 7 missing figures (C1); LoF clean.
2. [ ] Re-run `PROFILE=full` on both packages with documented seeds (light×5, heavy×3 or better); commit/archive results + KPI exports; add `repeat`/seed documentation (C2).
3. [ ] Diff every Chapter 6 table (and Abstract/Ch.1/Ch.7 headline numbers) against the regenerated KPIs; update text if shifted (C2).
4. [ ] Re-export all figures from the archived dataset in one run; replace `Masters/Figs` set (H6).
5. [ ] Fix artifact URL, add LICENSE, state artifact commit hash; consider Zenodo DOI (C3).
6. [ ] Correct INET version (4.5.4 or repin) in Ch.5 and bib; state Veins version (C4).
7. [ ] Rename "VO incomplete" → VO MAC drops; fix §6.2 definition, §6.4.2 sentence, Plain's "0"→n.a. (C5).
8. [ ] Investigate & document the ÷2 drop-attribution heuristic (H1).
9. [ ] Fix "merge and exit geometry"; "3 lanes per direction" (H2).
10. [ ] Footnote INET-default radio values after verifying them in the pinned INET; state the multicast data rate (H3).
11. [ ] Add OCB-approximation + BSS-vs-OCB EDCA parameter-set caveat (H4).
12. [ ] Align §4.3.1/FSM figure with code trigger semantics (H5).
13. [ ] Bibliography: umlauts, duplicates, craciunas entry type, CV2X paper verification (H7); prune unused entries (L5).
14. [ ] Address the heavy-density BE-tail crossover (M1) and light low/medium claim (M2); add burst-overlap and fleet-buildup qualifiers (M3); mean-of-P95 wording (M4).
15. [ ] Remove UPPAAL hedge (M5); fix repo AUDIT_REPORT P95-scope claim and submodule-init instructions (M6).
16. [ ] Polish: nine/ten (M7), RFC 9119 loss-rate wording (M8), ctrl-table precision (M9), oversized float + overfulls (M10), lowercase "in" (L1), "DSD-era" (L2), Thesis/Dissertation label (L4), legacy images out of Figs (L8).
17. [ ] Post-defense: committee names on approval page (L3); final rebuild with zero placeholder/overflow warnings.
