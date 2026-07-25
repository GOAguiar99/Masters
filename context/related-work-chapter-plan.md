# Related Work chapter plan (`chapters/2-chapter.tex`, prints as Chapter 3)

**Goal:** replace the legacy DQ-WiFi / TSN-primary survey with a dissertation-depth Related Work that positions crash-aware, local, event-triggered BE suppression against stronger MAC alternatives, always-on load regulation, and a short TSN/OFDMA contrast.

**Status of this file:** implemented in `chapters/2-chapter.tex` (July 2026).

---

## Current state

[`chapters/2-chapter.tex`](../chapters/2-chapter.tex) is still the legacy draft:

- Wired composite shapers, TSN–5G convergence, ATAS, wireless TSN, OFDMA/Wi-Fi 6
- Comparison table whose last row is “DQ-WiFi (This Work)”
- Broken cross-refs (`sec:fsm`, `sec:analysis`, `fig:generic_fsm`)
- Deterministic / AP-centric claims that contradict Intro + Background

**Primary port source:** SBESC §II-B (`../SBESC-2026-Paper/text.tex`) — three paragraphs:

1. Stronger MAC alternatives (TSNCtl, PRP-MAC, CFC-MAC, NR-V2X) + prior SBESC2025 work
2. Backoff freezing + SkipCCH + protection-cost motivation
3. Adaptive EDCA + DCC as always-on complements

**Secondary:** ETFA Related Work (same papers, slightly longer); verified claims in [`reference-notes.md`](reference-notes.md).

**Background already covers** DCF/EDCA/DCC/DSCP mechanics — Related Work must **not** re-teach those; only survey alternatives and draw contrasts.

**Depth (default for writing pass):** same graduate depth as Background (~8–12 pages), with subsections, one real comparison table, multiple figure placeholders, and comprehensive literature synthesis. This chapter should resemble a PhD dissertation chapter rather than a conference paper. Do not compress discussions simply to save space.

---

## Citation and scholarly requirements (mandatory)

This chapter is a literature review. Every technical claim, architectural description, comparison, limitation, historical statement, or design trade-off must be supported by appropriate citations. The writing should read as a synthesis of the research literature, not as an unsupported explanation.

### General requirements

- Every subsection must be grounded in primary literature rather than relying primarily on survey papers.
- Every substantive paragraph should normally contain one or more citations. Technical paragraphs without citations should be considered incomplete.
- Prefer original research papers and standards whenever possible. Use survey papers primarily to provide historical context or broad overviews.
- Every comparison between approaches must cite the original work(s) being compared.
- Every claimed limitation, assumption, trade-off, or design requirement must be traceable to the cited literature unless it is explicitly presented as the author's own synthesis.
- Standards (IEEE 802.11, IEEE 802.1 TSN, ETSI ITS-G5 DCC, 3GPP NR-V2X, etc.) should be cited directly whenever describing normative behavior.
- Avoid citation clustering whenever practical. Rather than attaching a long list of references to the end of a paragraph, attribute each important technical statement to its supporting source.
- Never fabricate citations or attribute claims that are not supported by the referenced paper.
- If an important statement cannot be supported by the existing bibliography, mark it for verification instead of inventing a reference.

### Literature synthesis

The chapter must synthesize the literature rather than becoming a sequence of paper summaries.

For every major family of work:

- explain the motivation behind the proposed approach;
- describe the technical mechanism;
- discuss its assumptions;
- identify the scenarios where it performs well;
- explain its limitations;
- explicitly relate those limitations to the crash-aware event-triggered V2X problem addressed in this dissertation.

Each subsection should conclude with a brief synthesis paragraph identifying what the surveyed works collectively demonstrate and what remains unsolved.

The final section should provide an analytical comparison of the literature, identifying common trends, recurring assumptions, unresolved challenges, and the precise research gap motivating this dissertation.

---

## Writing style

- Write at graduate/PhD dissertation level.
- Assume the reader has a networking and wireless communications background.
- Avoid textbook explanations already covered in Background.
- Prioritize critical analysis over description.
- Use precise technical language throughout.
- Make transitions between subsections explicit so the chapter reads as a coherent narrative instead of isolated literature summaries.
- Do not simply describe each paper independently; compare approaches continuously.

---

## Figures and tables

Figures are **not** required during this writing pass.

Instead:

- Insert descriptive figure placeholders wherever a figure would significantly improve understanding.
- Reference placeholders naturally within the text (e.g., "Figure X illustrates...").
- Use the same boxed placeholder style adopted in the Background chapter.
- Every placeholder should include a descriptive caption sufficient for future figure creation.

Examples:

- `[Figure X: Taxonomy of MAC coordination mechanisms according to synchronization requirements and infrastructure dependency.]`
- `[Figure X: Design-space comparison between always-on congestion control and event-triggered contention protection.]`
- `[Figure X: Timeline of MAC evolution from IEEE 802.11p EDCA to TSN-inspired and NR-V2X approaches.]`

Tables should be real LaTeX tables whenever possible, not placeholders.

---

## Target architecture

Keep stable label `\label{sec:rel_work}` (Background already `\ref{sec:rel_work}`).

### Opening (~0.5 page)

- One-paragraph problem restatement: EDCA is statistical; crash alerts need local protection without sync/infrastructure (`kosekszott2012What`, `Evolution_QoS_Mechanisms`).
- Taxonomy of the survey:
  - stronger vehicular/MAC alternatives;
  - contention-shaping and protection-cost literature;
  - always-on load regulation;
  - short TSN / wireless-TSN / OFDMA contrast.
- Position this dissertation:
  - explicit DSCP→VO prioritization;
  - event-triggered BE suppression;
  - IEEE 802.11p OCB operation;
  - no new MAC protocol;
  - no reservations;
  - no synchronization.

---

### 3.1 Stronger contention control for V2X (~3 pages)

One family per subsubsection.

For each family discuss:

- motivation;
- technical mechanism;
- assumptions;
- strengths;
- limitations;
- relation to this dissertation.

| Family | Keys | Required assumptions |
|---------|------|----------------------|
| TSN-like slot scheduling | `TSNCtl_Feraudo` | synchronization + platoon master; cite as arXiv preprint |
| Preemptive priority MAC | `PRP_MAC_Li` | UAV-assisted arbiter + richer MAC |
| Cooperative TDMA | `CFC_MAC_Linn` | synchronized slot allocation |
| Cellular sidelink | `CV2X_Sidelink_Allocation` | NR-V2X Mode 2 SPS/resource selection |
| Authors' previous work | `11288825` | Wireless TSN/TAS focus; precursor but different research question |

Conclude with the SBESC synthesis:

These approaches demonstrate the benefits of stronger contention control but generally rely on synchronization, centralized scheduling, TDMA reservations, or cellular infrastructure, making them broader solutions than the focused crash-aware local protection problem considered here.

### Figure placeholder

Design-space taxonomy:

- synchronization required vs local-only;
- infrastructure required vs infrastructure-free;
- always-on vs event-triggered.

### Real comparison table

Replace the legacy table.

Columns:

- Approach
- Key mechanism
- Requirements
- Target traffic
- Advantages
- Limitations
- Relation to this dissertation

Final row:

"This dissertation: crash-aware EDCA prioritization with adaptive BE suppression."

---

### 3.2 Contention dynamics and when traffic may contend (~2 pages)

Discuss:

- Continuous backoff freezing (`Continuous_Backoff_Freezing_Li`)
- SkipCCH (`SkipCCH_Garrido`)
- Protection-versus-cost (`Evolution_QoS_Mechanisms`, `kosekszott2012What`)

Focus on:

- dense-contention behavior;
- contention timing;
- cost of protecting critical traffic;
- why event-triggered suppression represents a different design philosophy.

Do **not** repeat the Background explanation of the IEEE 802.11 backoff algorithm.

---

### 3.3 Always-on load regulation: adaptive EDCA and DCC (~2 pages)

Cover:

- Adaptive EDCA parameter tuning
  (`romdhani2003AdaptiveEDCF`, `ni2004Qiang`, `Evolution_QoS_Mechanisms`)
- ETSI ITS-G5 DCC (`etsi_dcc_2018`)

Deepen the comparison with this dissertation:

- always-on operation;
- aggregate congestion management;
- continuous parameter adaptation.

Contrast with:

- event-triggered activation;
- selective BE suppression;
- complementary rather than competing objectives.

Avoid claiming superiority over DCC.

---

### 3.4 Short contrast: wired TSN, wireless TSN, and OFDMA (~1.5–2 pages)

Keep intentionally concise.

One paragraph each:

- Wired TSN (`ieee8021qbv`, `craciunas2016`, `debnath2023mixed`)
- Wireless TSN (`seliem2023wirelesstsn`, `satka2023wireless`, `schneider2022twt`)
- OFDMA / Trigger Frames (`karthik2018`, `schneider_mu_edca_2023`, `schneider_trigger_2024`)

State explicitly:

- no TAS evaluation;
- no TWT evaluation;
- no OFDMA evaluation;
- no migration-path discussion inherited from DQ-WiFi.

Purpose:

Provide context rather than becoming another TSN survey.

---

### 3.5 Synthesis and research gap (~0.5–1 page)

Integrate the previous sections.

Discuss:

- common assumptions across the literature;
- recurring design philosophies;
- unresolved challenges;
- why existing approaches do not fully address crash-aware local event-triggered protection.

End by motivating the System Model chapter.

Bridge naturally into `chap:sysmodel` and the five-policy framework.

---

## Guardrails

- Remove every DQ-WiFi reference.
- Remove beacon FSM references.
- Remove LISTENING/BLOCKED deterministic scheduling.
- Remove AP-centric scheduling claims.
- Remove worst-case deterministic delay equations.
- Use statistical contention language consistently.
- Treat TSNCtl as an arXiv preprint.
- Do not re-derive DCF, EDCA, DSCP, or DCC fundamentals.
- Do not cite `IEEE_80211p_Survey`; prefer `jiang2008ieee80211p`.
- Preserve consistency with the Introduction and Background chapters.

---

## Deliverables (writing pass)

1. Rewrite `chapters/2-chapter.tex` according to the architecture above.
2. Update `WRITING_ROADMAP.md`.
3. Update `AI_CONTEXT.md`.
4. Update `AGENTS.md`.
5. Run `./compile.sh`.
6. Confirm all citations resolve successfully.
7. Confirm all legacy DQ-WiFi references from this chapter have been removed.
8. Verify that every substantive technical paragraph contains appropriate citations.
9. Verify that every citation actually supports the statement being made.
10. Prefer original papers and standards over secondary surveys whenever both are available.
11. Ensure the final chapter reads as a cohesive literature synthesis rather than a collection of independent paper summaries.

---

## Out of scope

- No System Model rewrite.
- No Implementation rewrite.
- No Evaluation rewrite.
- No new simulation results.
- No additional PDF downloads unless a required claim cannot be supported from the existing bibliography or `reference-notes.md`.