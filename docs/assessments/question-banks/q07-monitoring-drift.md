# Question bank 07 — Monitoring and drift

**Covers:** Module [14 — Monitoring, drift, and retraining](../../modules/14-monitoring-drift-retraining/index.md).
**Format:** 10 questions — multiple choice, short answer, debugging, architecture, scenario.
**Suggested check:** 7/10, with **M5** and **M10** correct — those two are the
module's entire thesis.

> *Attempt first, then read the
> [reference solutions](../keys/question-banks-KEY.md).*

---

## Part A — Multiple choice

**M1.** Prediction logging should capture:

- (a) Only the predicted class
- (b) Input features (or a lawful representation), prediction, model version,
  timestamp, and later the realised outcome
- (c) Everything including raw personal identifiers, for completeness
- (d) Nothing; metrics are enough

**M2.** PSI (population stability index) compares:

- (a) Predicted vs actual labels
- (b) Two distributions — reference vs current — binned the same way
- (c) Training speed vs inference speed
- (d) Two models' parameters

**M3.** Labels arrive 30 days after prediction. Until they arrive you can
measure:

- (a) Data drift immediately; performance degradation only once labels land
- (b) Neither
- (c) Performance degradation immediately
- (d) Only uptime

**M4.** An alert threshold should be set by:

- (a) Whatever the library defaults to
- (b) A documented, justified rule tied to a decision and a response, tuned on
  historical data
- (c) Guessing, then never revisiting
- (d) Maximising the number of alerts so nothing is missed

## Part B — Short answer

**M5.** State plainly: does detected drift prove the model got worse? Explain
your answer, and name the measurement that *would* support the claim.

**M6.** Describe the 2×2 decision matrix (drift yes/no × performance degraded
yes/no) and what action each cell argues for.

**M7.** What is a *reference* (baseline) window, why must it be recorded with
its date range, and what goes wrong when it isn't?

## Part C — Debugging

**M8.** A dashboard shows every feature in strong drift the day after
deployment, then returns to normal. Two weeks later someone "fixed" the
monitoring. Give the two most likely explanations (one technical, one
process), and how you would verify each.

## Part D — Architecture

**M9.** Draw the monitoring loop: serving → prediction log → drift check →
label arrival → performance check → decision → (retrain | monitor | roll back).
Mark the two places where a human must be in the loop.

## Part E — Scenario

**M10.** Monday: PSI 0.31 on `monthly_charges`, 6 alerts, mean AUC down from
0.7798 to 0.7302, p95 latency 38 ms → 118 ms, error rate 0.2% → 2.6%. Decide:
roll back, retrain, or ride it out. Give your decision, the full reasoning
chain, the evidence you checked, and the flip-conditions that would change
your mind this week.

---

**Next:** [reference solutions](../keys/question-banks-KEY.md) (bank 07), then
[bank 08](q08-security-governance.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../../about/index.md).*
