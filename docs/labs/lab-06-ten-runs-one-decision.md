# LAB-06 — Ten Runs, One Decision

## 1. Lab identity

| | |
|---|---|
| **Lab ID** | **LAB-06** |
| **Difficulty / topic** | 🔧 Intermediate · Experiment tracking |
| **Prerequisite module** | [06 — Experiment tracking with MLflow](../modules/06-experiment-tracking-mlflow/index.md) |
| **Fixtures** | `examples/labs/` shared data + MLflow (installed: 3.17.2) |
| **Estimated time** | 105 minutes · free, local tracking server (file/sqlite store — no account) |

## 2. Scenario and background

The team chose a model by remembering. Now leadership asks: *"why is this
one better, and better by how much, across which seed?"* — and nobody can
answer. You will run a **10-run tracked sweep** (two model families ×
five seeds) in MLflow's local tracking store, then defend one champion
against the baseline using the recorded evidence, not memory.

## 3. Learning objectives

By the end you can:

1. Log params, metrics, and artefacts so every run is comparable.
2. Design a small sweep that answers a question (family × seed) instead
   of "random search theatre".
3. Compare runs in the MLflow UI/CLI and pick a champion **with a
   stated rule** (mean over seeds, not best single run).
4. Explain what a shared tracking *server* adds over a local file store —
   and when you need one.

## 4. Prerequisites and estimated time

- Module 06 read; `python -m pip show mlflow` → `3.17.2` (or newer).
- `python examples/labs/make_data.py`.
- **105 min** (setup 10 · sweep 30 · analysis 40 · write-up 15).

## 5. Student task statement

Produce `sweep.py` that logs **10 MLflow runs** (logistic vs gradient
boosting, seeds 1–5, same split strategy, `data_sha256` logged on every
run), then `decision.md` with: the aggregation rule you chose before
looking, the table of runs, the champion, the margin over baseline, and
one sentence on variance across seeds.

## 6. Required dataset and setup instructions

```powershell
# 🪟 Windows — PowerShell
cd examples\labs
python make_data.py
# tracking lives locally — no account, no cloud:
$env:MLFLOW_TRACKING_URI = "file:./mlruns"     # 🐧 export MLFLOW_TRACKING_URI=...
```
Optional UI: `mlflow ui --backend-store-uri file:./mlruns` →
`http://127.0.0.1:5000` (⚠️ needs a browser; the CLI path below is enough).

## 7. Starter files

| File | Role |
|---|---|
| `sweep.py` | **you write it** — spec in §8; reference in solutions |
| `../data/customers_clean.csv` | input (log its hash on every run) |
| `mlruns/` | local tracking store (generated; git-ignored) |

## 8. Numbered implementation steps

**Step 1 — First tracked run by hand.** In a REPL or a 15-line script:
`mlflow.set_experiment("lab06")`, `start_run()`, log
`{"family": "logistic", "seed": 1, "data_sha256": …}`, `log_metric("roc_auc", …)`,
`end_run()`. ✅ `mlflow runs list` shows one run.

**Step 2 — Write the sweep.** Loop families × seeds (5 each); same
features/split discipline as LAB-05; log params+metrics+the model file
(`mlflow.log_artifact`) for the champion only.
✅ Checkpoint: `mlflow runs list` shows **10** runs, each with
`family`, `seed`, `data_sha256`.

**Step 3 — Fix the rule BEFORE you look.** Write in `decision.md`:
"champion = highest **mean** roc_auc over 5 seeds; ties → lower std."
✅ Timestamp/commit the rule file first — discipline, not theatre.

**Step 4 — Aggregate.** Query the runs (MLflow API, `mlflow runs search`,
or export to CSV) → table: family, mean, std, min, max.
✅ Checkpoint: both families summarised; no cherry-picked single run in
the decision.

**Step 5 — Decide.** Champion + margin over baseline + seed-variance
sentence (`spread = max − min` for the winner).
✅ Checkpoint: `decision.md` contains the rule, the table, the verdict.

**Step 6 — Refuse the memory-habit.** Delete nothing — instead, one
paragraph: what question your 10 runs *cannot* answer (e.g. hyperparameter
interaction) and what you would track next.

## 9. Commands and expected results

| Command | Expected |
|---|---|
| `python sweep.py` | 10 runs created, no errors |
| `mlflow runs list -e lab06` (or `mlflow experiments list`) | 10 rows with params/metrics |
| `mlflow runs search -e lab06 --order-by "metrics.roc_auc DESC"` | sorted; you still decide by **mean per family** |
| UI (optional) | runs page with params/metrics/artefacts |

## 10. Acceptance criteria (objective)

- [ ] Exactly 10 runs, params (`family`, `seed`) + `data_sha256` logged.
- [ ] Aggregation rule written **before** the results were read (visible
      in your `decision.md` history/order).
- [ ] Mean/std table for both families (not best-run picking).
- [ ] Champion named with margin and seed-spread sentence.
- [ ] Honest limits paragraph (what the sweep doesn't show).
- [ ] Optional: model artefact attached to the champion run.

## 11. Troubleshooting and recovery

| Symptom | Cause | Fix |
|---|---|---|
| runs not appearing | different `MLFLOW_TRACKING_URI` per shell/cwd | set it once in the session; run from the same folder |
| `mlflow: command not found` | scripts module not on PATH | `python -m mlflow …` |
| runs logged without metrics | `log_metric` called outside active run | every log call between `start_run()` / `end_run()` (use the context manager) |
| UI shows empty experiment | experiment created in another store | check `mlruns/` location vs `--backend-store-uri` |
| AUC identical across seeds | split not seeded per run | seed derives from `seed` param — recheck LAB-05 lessons |

## 12. Reflection questions

1. Why is "best run wins" a trap even in a 10-run sweep? Give the
   statistical intuition in two sentences.
2. Your std is large for one family. What does that cost you in a release
   conversation?
3. Local file store vs tracking server: name the exact moment you would
   migrate — and what it must not cost you (data sovereignty).

## 13. Optional challenge tasks

1. Add a third family (e.g. `HistGradientBoostingClassifier`) and let the
   rule decide without touching the decision text.
2. Log a small plot (metrics by seed) as an artifact.
3. Export the run table to `runs.csv` and write the one-sentence
   leadership summary above it.

## 14. Rubric / checklist

| Points | Criterion |
|---|---|
| 4 | 10 runs, complete params + data hash, all queryable |
| 4 | rule-before-results discipline demonstrable |
| 4 | mean/std aggregation and a champion with margin |
| 2 | limits paragraph |
| 2 | decision.md complete and readable |
| **16** | **total** · ≥12 = pass |

## 15. Cleanup

```powershell
cd examples\labs
Remove-Item -Recurse mlruns -ErrorAction SilentlyContinue   # 🧹 keeps repo tidy
Remove-Item sweep.py, decision.md -ErrorAction SilentlyContinue   # only if discarding
```

---

**After attempting:** a reference `sweep.py` + `decision.md` skeleton live
in [`examples/labs/solutions/lab-06/`](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/labs/solutions/lab-06).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../about/index.md).*