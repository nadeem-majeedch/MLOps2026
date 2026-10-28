# LAB-17 — Read the Drift, Not the Chart

## 1. Lab identity

| | |
|---|---|
| **Lab ID** | **LAB-17** |
| **Difficulty / topic** | 🚀 Advanced · Prediction logs & drift analysis |
| **Prerequisite module** | [14 — Monitoring, drift, and retraining](../modules/14-monitoring-drift-retraining/index.md) |
| **Fixtures** | `examples/capstone-support/monitoring_out/` (real logs from verified runs) + `examples/labs/data/customers_shifted.csv` |
| **Estimated time** | 105 minutes · free, local, offline |

## 2. Scenario and background

The capstone service has been scoring for a window;
`monitoring_out/predictions.jsonl` holds the log (inputs, probability,
flag, model version, `actual` or `null`), `reference.csv` the snapshot
distribution. A dashboard shows three features in **strong** drift —
someone is drafting a retrain ticket. Your job is to determine what the
evidence actually supports: drift is a statement about *inputs*; only
labels can speak for *accuracy*. The real numbers here already contain
the lesson (see §9).

## 3. Learning objectives

By the end you can:

1. Interrogate a prediction log: scenario split, label coverage,
   model versions present.
2. Compute/read PSI per feature against the stated thresholds, and say
   what each verdict means — and what it does not.
3. Separate covariate drift from performance degradation using labelled
   windows; decide with a 2×2 matrix, not a chart.
4. Write a retrain-or-wait decision a human can sign, with thresholds
   cited.

## 4. Prerequisites and estimated time

- Module 14 read; capstone monitoring outputs exist (regenerate if
  missing — §6).
- **105 min** (orientation 15 · drift 30 · labels 25 · decision 25 ·
  write-up 10).

## 5. Student task statement

Produce `drift-analysis.md`: (a) log inventory (rows per scenario, label
coverage, model version); (b) per-feature drift table with thresholds
cited; (c) labelled-window performance numbers; (d) the 2×2 verdict with
your recommendation and its **preconditions** (what would change your
mind); (e) the one thing you explicitly refuse to conclude from drift
alone.

## 6. Required dataset and setup instructions

```powershell
# 🪟 Windows — PowerShell — from examples/capstone-support
python monitor.py snapshot          # reference.csv (600 rows) if missing
python monitor.py log               # baseline window, 400 rows, labels=null
python monitor.py log --shifted --labels   # shifted window WITH labels
python monitor.py drift
python monitor.py performance
python monitor.py decision
```
🐧: identical. If `monitoring_out/` already exists (verified state), you
may analyse as-is — say which you did.

## 7. Starter files

| File | Role |
|---|---|
| `monitoring_out/predictions.jsonl` | scored records: scenario, features, probability, version, `actual` |
| `monitoring_out/reference.csv` | the snapshot distribution |
| `monitoring_out/drift_report.json`, `performance_report.json`, `decision.md` | generated evidence |
| `../data/customers_shifted.csv` | the raw shifted extract (for your own PSI cross-check) |

## 8. Numbered implementation steps

**Step 1 — Inventory the log.** Counts per scenario; how many rows have
`actual` vs `null`; model version(s).
✅ three numbers pasted (baseline rows are label-free **by design** —
say why).

**Step 2 — Drift table.** From `drift_report.json`: every feature, PSI,
verdict, and the thresholds (PSI > 0.20 strong / 0.10–0.20 moderate /
< 0.10 stable — cite them in your document, do not paraphrase).

**Step 3 — Cross-check one feature by hand.** Recompute PSI for
`monthly_charges` (reference vs shifted) with a 10-line snippet, or
justify the difference if your bins differ.
✅ your number vs the report's, reconciled.

**Step 4 — Labels.** From `performance_report.json`: reference AUC, the
windowed AUC, drop, floor.
✅ real numbers pasted (see §9).

**Step 5 — The 2×2.** Map drift {yes/no} × degradation {yes/no} →
verdict cell. ✅ your verdict + the exact matrix cell.

**Step 6 — Decision note.** Recommendation with: thresholds cited,
numbers, what would flip it (e.g. "if next window's AUC < 0.75 →
RETRAIN"), and the explicit non-conclusion ("drift alone does not prove
the model got worse").

**Step 7 — One paragraph on seasonality:** which feature's drift could
be calendar-driven, and what extra evidence would settle it.

## 9. Commands and expected results

| Command | Expected (verified outputs shipped with the capstone) |
|---|---|
| `python monitor.py drift` | `attendance_rate psi=0.8635 strong` · `missed_assessments psi=1.1786 strong` · `assignment_rate psi=0.4379 strong` · `prior_score 0.01 stable` · `lms_logins 0.0215 stable` → `overall: DRIFT DETECTED` |
| `python monitor.py performance` | `shifted auc=0.7712 drop=-0.005 within tolerance` |
| `python monitor.py decision` | `decision: MONITOR -> monitoring_out/decision.md` |
| your Step 3 cross-check | same order of magnitude; differences explained by binning |

**The lesson in these numbers:** three features in *strong* drift **and**
AUC slightly *above* the 0.7662 reference — verdict **MONITOR**. A
retrain ticket based on the drift chart alone would have been wrong.

## 10. Acceptance criteria (objective)

- [ ] Inventory: rows/labels/version with the "why null" explanation.
- [ ] Full drift table with thresholds cited (not paraphrased).
- [ ] One feature recomputed or reconciled by hand.
- [ ] Labelled performance numbers pasted (AUC, drop, floor).
- [ ] 2×2 cell chosen from evidence; recommendation + flip-conditions.
- [ ] Explicit non-conclusion about drift-only reasoning.
- [ ] Seasonality paragraph.

## 11. Troubleshooting and recovery

| Symptom | Cause | Fix |
|---|---|---|
| `no reference: … snapshot first` | `reference.csv` missing | `python monitor.py snapshot` |
| drift report shows only `rows` not features | log empty | run `monitor.py log` (and `--shifted --labels`) |
| performance says "no labelled records" | windows logged without `--labels` | re-log the shifted window with `--labels` |
| decision says `drift_report.json` missing | run `drift` first | commands in §6 order matter |
| your PSI differs from the report | different binning/edge policy | acceptable — explain; consistency with the *stated rule* matters more |
| all rows one scenario | you analysed an older run | check `scenario` values; regenerate |

## 12. Reflection questions

1. The verdict is MONITOR with PSI 1.18 on one feature. What would make
   that verdict wrong — and which measurement would reveal it?
2. Labels arrive late in the real world. How long do you wait, and what
   do you tell the stakeholder asking "is the model broken?" today?
3. Name one monitoring signal that would have caught a *real* problem
   here earlier than PSI, and why.

## 13. Optional challenge tasks

1. Recompute PSI for `customers_shifted.csv` vs `customers_clean.csv`
   with your own script (no capstone files) — do the verdicts agree?
2. Set a KS-test threshold (p < 0.01) alongside PSI; where do they
   disagree, and which do you trust for 400-row windows?
3. Add a "label lag" column to the decision note: days between scoring
   and truth — and what it costs your retrain latency.

## 14. Rubric / checklist

| Points | Criterion |
|---|---|
| 3 | inventory with label-coverage reasoning |
| 4 | drift table complete, thresholds cited |
| 2 | hand cross-check or reconciliation |
| 3 | labelled performance numbers correct |
| 3 | 2×2 verdict + flip-conditions + non-conclusion |
| 2 | seasonality paragraph |
| **17** | **total** · ≥13 = pass |

## 15. Cleanup

```powershell
# analysis only — regenerable state stays as-is; to reset the window:
cd examples\capstone-support
Remove-Item -Recurse monitoring_out -ErrorAction SilentlyContinue
python monitor.py snapshot && python monitor.py log
```
Delete your `drift-analysis.md` only if you are not submitting it.

---

**After attempting:** a reference analysis structure lives in
[`examples/labs/solutions/lab-17/`](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/labs/solutions/lab-17).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../about/index.md).*