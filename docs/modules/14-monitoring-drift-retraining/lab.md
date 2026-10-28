# Lab 14 — Catch the drift, then decide like an engineer

## 1. Scenario and business problem

The churn model is live behind the Module 10 API. Two things have happened
this month: your data scientist saw a monitoring chart spike and immediately
retrained (the new model was worse), while a *real* degradation went unnoticed
for a week because it looked like normal wobble on the dashboard.

**Business problem:** replace chart-reacting with an evidence chain — log what
you score, measure input movement against a stated threshold, wait for labels
before claiming damage, and produce a decision a human signs off on.

## 2. Skills practising

- Instrumenting predictions with the fields monitoring actually needs.
- Running drift tests with **cited** thresholds and reading PSI/KS honestly.
- Separating "inputs moved" from "accuracy fell" — with numbers from both.
- Applying a decision matrix, including the *restraint* cases.
- Entering the retraining loop with a rollback already rehearsed.

## 3. Prerequisites

- [concepts.md](concepts.md) read (§1–§7).
- Module 09 lab done (registry + a rollback in your history) — the decision
  checklist references it.
- Free, local, no accounts; synthetic data, labelled as such.

## 4. Required tools and estimated time

| Item | Detail |
|---|---|
| Tools | Python 3.10+ with scipy (installed for scikit-learn), the `monitoring/` package |
| Cost | Free, local, offline |
| ⚠️ Resource-heavy | none — each window is 400 rows, runs in seconds |
| ⏱️ Estimated time | 140 minutes |

## 5. Input data and how to obtain it

```powershell
# 🪟 from examples/churn
python generate_data.py             # baseline extract
python -m pipe.run                  # ✅ model exists (monitoring needs it)
python -m pytest                    # ✅ 34 passed
```

## 6. Directory layout

```
examples/churn/monitoring/
├── log_predictions.py   # scenario: baseline | shift | degrade  (+ --labels)
├── drift.py             # --snapshot | report | --check
├── performance.py       # labels required
├── decision.py          # 2x2 matrix -> decision.md
├── predictions.jsonl    # generated log (one JSON line per record)
├── reference.csv        # generated snapshot
└── *_report.md, decision.md   # generated evidence
```

## 7. Setup and execution steps

**Step 1 — Read one log line.** After a baseline run, open
`predictions.jsonl` and list every field; for each, write which of concepts
§1's four questions it supports. Identify the field that is `null` and why.
✅ **Checkpoint:** `actual: null` explained as feedback delay, not a bug.

**Step 2 — Baseline + reference.**
```powershell
python -m monitoring.log_predictions --scenario baseline --labels
python -m monitoring.drift --snapshot
```
✅ **Checkpoint:** 400 logged; `reference.csv` has 2000 rows.

**Step 3 — Drift, pre-label.** Log the `shift` window **without** `--labels`,
run `drift`, and record all four feature verdicts with their PSI values.
✅ **Checkpoint:** matches worked example §2 (`support_tickets` strong).

**Step 4 — Measure the no-damage case.** Add labels for the same window and
run `performance`, then `decision`.
✅ **Checkpoint:** shift `within tolerance`, decision **MONITOR**. Write five
words explaining why retraining now would have been a mistake.

**Step 5 — The damage case.** Log `degrade --labels`, rerun `performance` and
`decision`.
✅ **Checkpoint:** `degrade` DEGRADED with its AUC; decision **RETRAIN
CANDIDATE**; `decision.md` contains the five-item checklist.

**Step 6 — The noise case (LO 14.3).** Explain the baseline row
(`0.6902 → DEGRADED`) using: reference AUC 0.7163, floor 0.70, window size 400.
State what you would change to reduce this false-alarm class (window size?
multi-window confirmation? drop-vs-reference as the primary tripwire?) — and
what each choice costs.
✅ **Checkpoint:** a written argument citing all three numbers.

**Step 7 — Threshold discipline.** Cite, from `drift.py` output or file, the
exact three thresholds used (PSI strong/moderate, KS alpha, category mix) and
one sentence on where each convention comes from (not: "it looked right").

**Step 8 — From decision to action (no retrain needed — walk it).** Read the
RETRAIN CANDIDATE checklist and execute it **without changing the model**:
run `python -m pipe.run --clean`, confirm the gate, confirm your registry
rollback command still works (`python -m registry history` shows a rollback).
You are rehearsing the loop, not performing a fake retrain.
✅ **Checkpoint:** gate PASS + a rollback entry in history.

**Step 9 — The false-alarm hunt (preview of the challenge).** Run `drift
--check` on the *baseline* window against its own reference — a classic
self-comparison — and record the verdict. Note where a naive dashboard would
have alerted.

**Step 10 — Write the monitoring plan** for a real deployment: what to log,
sampling policy, thresholds + who set them, label delay estimate, alert
recipient, and the retraining rule (which two conditions, exactly).

## 8. Expected outputs and verification

| Step | Expected | Verify |
|---|---|---|
| 1 | Field-to-question table; `actual` explained | your note |
| 3 | 4 verdicts incl. one strong | drift report |
| 4 | `within tolerance` → **MONITOR** | console + `decision.md` |
| 5 | `degrade` DEGRADED → **RETRAIN CANDIDATE** | both reports |
| 6 | Three numbers cited; chosen fix + its cost | your argument |
| 7 | Three thresholds quoted from the file | quote + source line |
| 8 | Gate PASS + rollback in history | commands |
| 9 | Verdict recorded for the self-comparison | `--check` output |

## 9. Acceptance criteria

- [ ] Both decisions produced with their real outputs (MONITOR **and** RETRAIN CANDIDATE).
- [ ] Drift numbers reported with **cited** thresholds (no invented cutoffs).
- [ ] The baseline-noise explanation uses reference AUC, floor, and window size.
- [ ] Retraining loop rehearsed: clean pipeline + gate PASS + rollback present.
- [ ] Monitoring plan includes label delay and an explicit retraining rule.
- [ ] Everything filed as `modules/14/`.

## 10. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `no predictions logged yet` | Wrong folder or fresh checkout | Run from `examples/churn`; do Step 2 first |
| `no reference: run --snapshot first` | Snapshot not taken (or deleted) | `python -m monitoring.drift --snapshot` |
| `no labelled records yet: accuracy cannot be measured` | You logged without `--labels` | Expected and *correct*: labels arrive later — log the window again with `--labels` (appends) |
| Drift says stable on a window you *know* shifted | Comparing against the wrong scenario, or reference already drifted | Check `scenario=` in the report; re-snapshot only if the old reference is genuinely obsolete — and say so |
| AUC identical across windows | Same records logged twice (scenario filter) | Check the `scenario` field values in `predictions.jsonl` |
| PSI negative or odd on tiny samples | Too few distinct values/bins | Our `psi()` guards collapse with a floor; treat tiny-sample PSI as inconclusive |
| SciPy import error | Minimal Python install | scikit-learn pulls scipy in; `python -m pip install scipy` if you installed selectively |

More: [troubleshooting.md](troubleshooting.md).

## 11. Cleanup

```powershell
# 🪟 from examples/churn — reports are evidence: keep the .md files you filed
python generate_data.py                        # restore baseline extract
python -m pipe.run --once                      # re-verify the pipeline
python -m pytest                               # ✅ 34 passed
# optional full reset of generated monitoring state:
Remove-Item monitoring/predictions.jsonl, monitoring/reference.csv -ErrorAction SilentlyContinue
```

## 12. Optional extension tasks

1. **Multi-window confirmation:** require two consecutive degraded windows
   before RETRAIN CANDIDATE; re-run the sequence and show which decision
   changes and which does not.
2. **Seasonal control:** build a "same weekday/period last month" reference
   from `churn_day2.csv` and compare verdicts against the flat reference.
3. **Wire it to the scheduler (Module 13):** run the four monitoring steps as
   a scheduled tick that writes `ALERT.md` only on RETRAIN CANDIDATE — then
   argue which failures would still need a human to notice.

---

**Next:** [independent-challenge.md](independent-challenge.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*