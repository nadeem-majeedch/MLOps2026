# Learning objectives — Module 14

Maps to syllabus outcomes
[LO 14.1–14.4](../../syllabus/detailed-syllabus.md#module-14-prediction-monitoring-data-drift-model-drift-and-retraining).

| # | You can… | You prove it by… |
|---|---|---|
| **14.1** | Instrument predictions for monitoring: what to log, at what rate, and why | `monitoring/log_predictions.py` records: inputs, probability, thresholded output, model version, timestamp, label-or-null — with a written note on sampling/sensitivity (Module 15 deepens the privacy angle) |
| **14.2** | Detect data (covariate) drift and performance drift with defensible thresholds | `drift_report.md` with PSI/KS numbers **against the stated rule** (PSI > 0.20 strong, KS p < 0.01) — thresholds cited, not vibes |
| **14.3** | Distinguish drift from seasonal variation, sampling noise, and measurement change | Your analysis of the baseline window (AUC 0.6902 on 400 rows) explaining window noise vs real degradation — with numbers |
| **14.4** | Trigger and evaluate retraining from monitoring evidence, and decide when *not* to retrain | Two `decision.md` files: **MONITOR** (drift, no degradation) and **RETRAIN CANDIDATE** (drift + degradation), each with the human checklist |

## Supporting skills

- State the difference between **covariate shift** (inputs moved) and
  **concept drift** (the input→label relationship moved), and say which one
  *only labels* can reveal.
- Explain why a fixed 400-row window makes AUC noisy, and what that means for
  alert thresholds.
- Describe the full retraining loop end to end: evidence → decision →
  `pipe.run --clean` → gate → register → promote → **rollback rehearsed**.
- Name what monitoring must NOT log (privacy) and where that is handled.

## Self-check questions

1. Drift detected, labels silent: what do you do — and what must you *not* do?
2. Which report is allowed to say "the model is wrong"? Why only that one?
3. What two conditions make `RETRAIN CANDIDATE` rather than `MONITOR`?

*(Answers in [knowledge-check.md](knowledge-check.md) — attempt first.)*

---

[← Module 14 index](index.md) · [Next: concepts →](concepts.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*