# Research notes (merged from `veins-inet-qos/review.md`)

## Publishable claim (target)

Bounded crash-triggered BE contention-suppression for 802.11p-style vehicular multicast that improves VO tail latency and reach while bounding BE starvation — **not** deterministic TSN guarantees.

## Known mechanisms (not novel alone)

- DSCP → VO mapping
- EDCA CW/AIFS tuning
- Veins/INET integration patterns

## Novel element (requires validation)

Adaptive `V2xHcf`: suppresses BE channel requests when local or overheard VO demand is active. Three profiles (`stable`, `guarded`, `emergency`) with increasing aggressiveness.

## Do not over-claim

- No deterministic networking or TSN guarantees
- Multicast ≠ unicast reliability; define reach/receiver-opportunity metrics
- `IdealObstacleLoss` is binary — simplified propagation
- Queue isolation (DCF 128 vs EDCA separate queues) confounds comparisons
- Whole-run KPIs dilute crash-window effects — prefer windowed analysis when possible

## Suggested baselines (literature)

DCF, standard EDCA, tuned EDCA, application repetition only, adaptive BE suppression, ETSI DCC, WAVE/1609.4 priority access.

## KPI priorities for safety traffic

P95/P99 delay, first-success latency, receiver-opportunity reach, MAC drop attribution, BE starvation duration, Jain fairness, CBR.

## Instrumentation gaps to watch

- `beGrantWhileBlocked` — BE grant while FSM blocked
- VO logical vs physical TX/RX (repeat bursts)
- Time windows: pre-crash, crash, post-crash

## Standards URLs (for bib entries)

- INET QoS: https://inet.omnetpp.org/docs/showcases/wireless/qos/doc/index.html
- IEEE 1609.4: https://standards.ieee.org/ieee/1609.4/6183/
- ETSI DCC TS 102 687
- RFC 9320 (DetNet contrast only)
