# Conclusion chapter plan (`chapters/6-chapter.tex`, prints as Chapter 7)

**Goal:** replace the legacy DQ-WiFi Work Plan / Schedule with a crash-aware Conclusion that closes the research question, restates headline findings with exact KPIs, states the conditional practical takeaway, and lists limitations and future work—without inventing results or re-running Evaluation discussion.

**Status of this file:** implemented in `chapters/6-chapter.tex` (August 2026). Work Plan / timeline deleted.

**Primary port source:** SBESC §V (`../SBESC-2026-Paper/text.tex`), expanded with Evaluation headline numbers (delay/jitter/VO drops) and Intro objectives/contributions.

**Do not invent** CIs, significance tests, or unreported figures. Prefer SBESC + Evaluation tables already in the thesis.

---

## Section architecture

Keep label `\label{chap:conclusion}`.

1. Opening — restate protection-versus-cost question; two-class model; five policies; simulation-only scope (cross-ref System Model / Implementation / Evaluation).
2. Main findings (`sec:conc:findings`) — heavy/high emergency Voice gains + BE cost; light gating warning; enabling condition.
3. Practical takeaway (`sec:conc:takeaway`) — marking as default; blocking as event-triggered escalation; auth/rate-limit prerequisites; `ts22186` framing.
4. Limitations (`sec:conc:limits`) — expanded restatement of Evaluation/DSD threats: simulation-only + seeds/no CIs; two-class abstraction + no DCC/adaptive-EDCA baseline + fixed profiles; optimistic PHY + one-hop/single crash + limited density/load sweep; VO significance / plain sampling / spatial BE / DoS caveats (cross-ref Evaluation discussion).
5. Future work (`sec:conc:future`) — stronger stats + richer radio/traffic/multi-hop + app-level outcomes; ablations + DCC/adaptive-EDCA/sidelink + concurrent alerts; auth/finer classes/spatial fairness + testbed.

No tables, figures, or schedule.

---

## Citation requirements

`aguiar2026_veins_qos`, `ts22186`, `IEEE80211e_2005`, `kosekszott2012What` as needed; cross-refs to `chap:sysmodel`, `chap:implementation`, `chap:evaluation`.

---

## Bridge fixes done with this rewrite

- Intro §Document Structure ends at Conclusion (Ch7); Implementation and Evaluation are separate chapters.
- Evaluation chapter summary bridges to Conclusion (not Work Plan).
- `main.tex` comment labels Ch6 file as Conclusion.
