# LAB-17 — reference solution

> Attempt the lab first. This is the answer key, not the assignment.

## Verified outputs (authoring machine; re-run them yourself)

```text
$ python monitor.py drift
  attendance_rate      psi=0.8635  strong
  prior_score          psi=0.01    stable
  lms_logins           psi=0.0215  stable
  missed_assessments   psi=1.1786  strong
  assignment_rate      psi=0.4379  strong
overall: DRIFT DETECTED -> monitoring_out/drift_report.json

$ python monitor.py performance
  shifted    auc=0.7712 drop=-0.005 within tolerance

$ python monitor.py decision
decision: MONITOR -> monitoring_out/decision.md
```

## The verdict and why it is not "retrain"

| Evidence | Reading |
|---|---|
| 3 features **strong** PSI (≥ 0.20) | input distribution moved |
| AUC 0.7712 vs reference 0.7662 → drop −0.005 | the model still ranks correctly |
| Decision matrix cell | drift **yes** × performance **no** → MONITOR |

**Drift ≠ degradation.** PSI measures how the *inputs* are distributed;
AUC measures whether the model still *orders* outcomes. They can move
independently — and here they do. A retrain ticket opened from the chart
alone would spend a sprint fixing a problem the numbers say doesn't
exist yet. The flip conditions are the real deliverable: retrain when
AUC drop crosses the tolerance floor (and say the number), or when a
drifting feature starts impacting performance, not when a plot turns
orange.

## Inventory "why null" (step 1 model answer)

Prediction rows exist for the replayed windows; **labels are null for
recent rows** because ground truth (did the student actually need
support?) only arrives after the outcome window closes. Performance on
unlabelled rows is *undefined*, not zero — which is exactly why the
pipeline separates "drift on features" (answerable now) from
"performance degradation" (answerable only when labels land).

## Reconciling your hand computation (step 3)

PSI depends on **binning**: `monitor.py` uses 10 quantile bins of the
reference. If your manual histogram used fixed-width bins or a different
bin count you will get a different number of the same order of
magnitude. State your binning; a number without its bins is not a
measurement.

## Seasonality paragraph (model answer)

Enrolment data is seasonal (term start vs holidays): attendance and
LMS logins legitimately shift on a calendar cycle. That is why a single
PSI snapshot is a *trigger for investigation*, not proof — you must
compare against the same window a year/term ago before calling
something drift, and why the reference set must be recorded with its
date range.

## Common wrong answers

- "Drift detected → schedule retrain." Directly contradicts the module
  lesson and the decision matrix you were asked to fill in.
- Quoting AUC without the floor/tolerance (0.7662 reference, ±tolerance
  as configured) — a bare number cannot select a matrix cell.
- Treating null labels as 0 or dropping them silently — either poisons
  the AUC.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../../docs/about/index.md).*
