# Lab 06 — Ten runs, one decision

## 1. Scenario and business problem

The retention team has a contact budget: they can call 100 customers a week.
They want the model that puts the most actual churners in that top 100 — and
they want to know what you tried, what you kept, and why.

**Business problem:** without tracked experiments, model choice is a story told
after the fact. With them, it is a decision anyone can re-check.

## 2. Skills practising

- Logging parameters, metrics, and artifacts for every run.
- Designing a small, *meaningful* sweep (varying what matters, holding the rest fixed).
- Comparing runs against a pre-stated metric and baseline.
- Writing a decision memo an auditor can follow.

## 3. Prerequisites

- [concepts.md](concepts.md) read (§1–§5).
- Module 05 lab completed (reproducible pipeline).
- MLflow installed: `python -c "import mlflow; print(mlflow.__version__)"` → verified with 3.17.2.

## 4. Required tools and estimated time

| Item | Detail |
|---|---|
| Tools | Python, scikit-learn, MLflow (local, free, no account) |
| Cost | **Free and local** — the tracking store is a file in your folder |
| ⚠️ Resource-heavy | none |
| ⏱️ Estimated time | 120 minutes |

## 5. Input data and how to obtain it

```powershell
# 🪟 Windows / PowerShell — from examples/churn
python generate_data.py
python -m src.validate --data data/raw/churn.csv     # ✅ 7/7 before any run
```

## 6. Directory layout

```
examples/churn/
├── experiments/train_mlflow.py   # tracking wrapper around src.train
├── src/…                         # the pipeline you already built (M05)
├── config.yaml                   # the values you will vary
├── mlflow.db                     # tracking backend (generated, gitignored)
└── mlruns/                       # artifacts (generated, gitignored)
```

## 7. Setup and execution steps

**Step 1 — Decide before you run.** Write three lines *first*:
primary metric, baseline, and what counts as "better" (e.g. *"≥0.01 AUC above
baseline, on the same seed and split"*). This pre-registration is what makes the
final decision defensible — concepts §4.

**Step 2 — Sanity run (should reproduce Module 05).**

```powershell
python -m experiments.train_mlflow --config config.yaml --data data/raw/churn.csv --run-name baseline
```

✅ Checkpoint: a run ID prints; `accuracy 0.91`, `roc_auc 0.7163`.

**Step 3 — Build the sweep.** Ten runs minimum, varying deliberately:

| Runs | Vary | Hold fixed |
|---|---|---|
| 1–2 | baseline, re-run (repeatability check) | everything |
| 3–5 | `test_size`: 0.15 / 0.20 / 0.30 | seed, model family |
| 6–8 | `model.family`: logistic vs `gradient_boosting` (+ a settings variant) | split, seed |
| 9–10 | `seed`: 42 / 4242 | split, family |

Create a config copy per run (name it clearly) and pass `--config`, or edit and
revert — but **record which file each run used** (`mlflow.log_artifact(args.config)`
already stores it).

```powershell
# example of one sweep run
python -m experiments.train_mlflow --config _sweep_size015.yaml --data data/raw/churn.csv --run-name split-015
```

✅ **Checkpoint:** ≥10 runs exist, each with a name, parameters, and metrics.

**Step 4 — The repeatability check.** Two identical runs must show identical
metrics. Any difference means a seed or config is drifting — stop and fix it
before comparing anything else.

**Step 5 — Query and compare.**

```python
import mlflow
mlflow.set_tracking_uri("sqlite:///mlflow.db")
df = mlflow.search_runs(experiment_names=["churn-baseline"],
                        order_by=["metrics.roc_auc DESC"])
cols = ["run_id", "tags.mlflow.runName", "params.seed", "params.test_size",
        "params.model_family", "metrics.roc_auc", "metrics.accuracy", "metrics.f1"]
print(df[cols].to_string(index=False))
```

✅ Checkpoint: a table where **your declared primary metric** decides the order.

**Step 6 — Look for the traps.**
1. Does the top row win on accuracy too? If not, say which metric you trust and why.
2. Do any "improvements" fall inside Module 05's measured seed noise (~0.03 AUC)?
   Mark them as noise, not gains.
3. Are parameters complete for every run? A run with missing params is
   unusable for comparison — log it as a known gap or re-run it.

**Step 7 — Browse the UI.**

```powershell
mlflow server --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1
```

Open <http://127.0.0.1:5000>. ✅ Confirm runs, params, metrics, and the logged
config artifact render. `Ctrl+C` to stop.

**Step 8 — Write the memo** (one page):

1. Question and contact-budget framing
2. Pre-stated metric and baseline (from Step 1)
3. Comparison table (from Step 5)
4. Decision: champion, with run ID
5. What was ruled out, and what noise you refused to call a gain
6. Next experiment, stated falsifiably

## 8. Expected outputs and verification

| Step | Expected (actual for the baseline run) | Verify |
|---|---|---|
| 2 | run ID printed; `roc_auc 0.7163`, `accuracy 0.91` | console output |
| 3 | ≥10 runs with complete params/metrics | query output / UI |
| 4 | identical metrics across two identical runs | side-by-side rows |
| 5 | ordered table, primary metric first | printed dataframe |
| 7 | UI shows both runs and artifacts | browser at 127.0.0.1:5000 |
| 8 | memo contains run IDs, metric, baseline, next step | your own read-through |

## 9. Acceptance criteria

- [ ] Pre-stated metric, baseline, and "better" rule written **before** runs.
- [ ] ≥10 runs, each with parameters and metrics; config artifact attached.
- [ ] Repeatability check passes (two identical runs agree).
- [ ] Comparison ordered by the declared metric; at least one "gain" correctly
      identified as within seed noise.
- [ ] Decision names a champion **run ID** and a falsifiable next step.
- [ ] UI verified locally.
- [ ] Evidence filed as `modules/06/` (memo + table + screenshot or query output).

## 10. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `The filesystem tracking backend ... is in maintenance mode` / `MlflowException` about file store | MLflow 3.x rejects `file:./mlruns` | Use `mlflow.set_tracking_uri("sqlite:///mlflow.db")` — the course script already does |
| `mlflow: command not found` | Console script not on PATH | `python -m pip show mlflow` to confirm install; use `python -m mlflow` or the module's script |
| `ModuleNotFoundError: mlflow` | Wrong interpreter | `.venv\Scripts\python -m pip install mlflow` 🪟 |
| Runs appear in a *different* experiment | Experiment name set elsewhere | The script calls `set_experiment("churn-baseline")`; check the UI's experiment list |
| `search_runs` returns an empty dataframe | Wrong tracking URI or experiment name | Set `sqlite:///mlflow.db` explicitly; print `mlflow.search_experiments()` |
| UI shows runs but no artifacts | Artifact store path resolved elsewhere | Run the server from `examples/churn` so `mlruns/` resolves consistently |
| Two runs show identical params but different metrics | Unseeded step (Module 05's problem returning) | Re-check `random_state` everywhere before drawing conclusions |
| Slow first run | MLflow creating DB tables | One-time; subsequent runs are fast |

More: [troubleshooting.md](troubleshooting.md) ·
[course troubleshooting](../../troubleshooting/index.md).

## 11. Cleanup

```powershell
# 🪟 from examples/churn — keep the memo, drop the local store if you want a clean slate
Remove-Item mlflow.db -ErrorAction SilentlyContinue
Remove-Item -Recurse mlruns, artifacts, __pycache__ -ErrorAction SilentlyContinue
python generate_data.py
```

```bash
# 🐧
rm -f mlflow.db && rm -rf mlruns artifacts __pycache__ && python3 generate_data.py
```

✅ Verify: data regenerates (`rows written: 2000`) and a fresh
`python -m experiments.train_mlflow …` creates a new database cleanly.
Your memo and comparison table are what you keep — they are the evidence.

## 12. Optional extension tasks

1. **Threshold sweep:** log a second family of metrics computed at thresholds
   0.2/0.3/0.5 and choose on recall@100 — the contact budget from the scenario.
2. **Tagging and notes:** use `mlflow.set_tag(...)` and run notes to record
   hypotheses; read them back in the UI.
3. **Hosted comparison (☁️ optional):** read the docs for one hosted tracker and
   write five lines on what it adds over local MLflow — and what it costs you
   in privacy and setup.
4. **Auto-sweep:** replace manual runs with a `for` loop over a config list — a
   preview of Module 08's automation.

---

**Next:** [independent-challenge.md](independent-challenge.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*