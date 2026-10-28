# Worked example — two real runs, one comparison

Everything below was executed on the reference machine (MLflow **3.17.2**,
Python 3.14) in `examples/churn/`. Run IDs and the comparison table are actual.

---

## 1. The tracking script

`experiments/train_mlflow.py` reuses Module 05's `train()` — no duplicated
training code — and adds the tracking layer:

```python
mlflow.set_tracking_uri("sqlite:///mlflow.db")     # local database, no server needed
mlflow.set_experiment("churn-baseline")

with mlflow.start_run(run_name=args.run_name) as run:
    metrics, pipeline = train(args.config, args.data, family=args.family)
    config = load_config(args.config)
    mlflow.log_params({...seed, split, model settings...})
    mlflow.log_metrics({accuracy, roc_auc, f1})
    mlflow.log_artifact(args.config)               # the config travels with the run
    mlflow.sklearn.log_model(pipeline, name="churn-model")
```

**Four things logged:** parameters, metrics, an artifact (the config), and the
fitted pipeline itself. Not logged (and why): raw data — it is versioned by
Module 04's hash instead, so the tracker stays small and data stays private.

## 2. Run the baseline

```powershell
# 🪟 Windows / PowerShell — from examples/churn
python -m experiments.train_mlflow --config config.yaml --data data/raw/churn.csv --run-name baseline-logistic
```

Actual output:

```text
run_id:   8e541425cadb402ca39d30344688a497
uri:      sqlite:///mlflow.db
metrics:  {'model_family': 'logistic', 'accuracy': 0.91, 'roc_auc': 0.7163, 'f1': 0.0,
           'positive_rate_test': 0.09, 'n_train': 1600, 'n_test': 400, 'seed': 42}
```

✅ **Checkpoint:** you have a run ID. Write it down — that ID is now the address
of everything about this run.

## 3. Run the challenger

```powershell
python -m experiments.train_mlflow --config config.yaml --data data/raw/churn.csv --run-name challenger-gb --family gradient_boosting
```

It logs a second run with `model_family=gradient_boosting` and metrics
`roc_auc 0.6431`, `accuracy 0.90`, `f1 0.0476` (identical to Module 05's direct
run — the tracker changed nothing about the training).

## 4. Compare — the query that *is* the report

```python
import mlflow
mlflow.set_tracking_uri("sqlite:///mlflow.db")
df = mlflow.search_runs(experiment_names=["churn-baseline"],
                        order_by=["metrics.roc_auc DESC"])
print(df[["run_id", "tags.mlflow.runName", "params.model_family",
          "metrics.roc_auc", "metrics.accuracy", "metrics.f1"]].to_string(index=False))
```

Actual output:

```text
                          run_id tags.mlflow.runName params.model_family  metrics.roc_auc  metrics.accuracy  metrics.f1
8e541425cadb402ca39d30344688a497   baseline-logistic            logistic           0.7163              0.91      0.0000
aadcabb3a55b41a29b91106079f9bbff       challenger-gb   gradient_boosting           0.6431              0.90      0.0476
```

**Reading the table:**

- Sorted by the metric we declared primary (ROC AUC) — the baseline wins.
- Accuracy is nearly identical and *uninformative* here (both ≈ the 0.91
  majority baseline): the imbalance lesson from Module 05, now visible in a
  comparison.
- `f1` ≈ 0 for both at threshold 0.5 — a threshold question, not a ranking one.

**The decision, written the way the lab's memo asks for it:**

> Baseline (logistic, run `8e541425…`) is chosen as champion on ROC AUC
> 0.7163 vs 0.6431, same data version and seed. The challenger does not beat it.
> Next experiment: threshold tuning for recall at a fixed contact budget —
> because ranking quality is adequate while the operating point is undefined.

Note what the memo does **not** say: "the new model was better". It names the
metric, the runs, and the next falsifiable step.

## 5. Browsing the same data in the UI

```powershell
# 🪟 Windows / PowerShell — local server, no account
mlflow server --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1
```

Open <http://127.0.0.1:5000> — experiments, runs, params, metrics, and the logged
config artifact are all browsable. Stop with `Ctrl+C`.

✅ **Checkpoint:** both runs appear under `churn-baseline`, and the logged
`config.yaml` artifact opens from the run page.

## 6. What you just did, in lifecycle terms

| Step | Stage it serves |
|---|---|
| Log params/metrics/artifacts with a run ID | **Train & experiment** — the record that makes results addressable |
| Keep data out of the tracker, referenced by hash | **Validate & version** — lineage without data duplication |
| Choose by a pre-stated metric against a baseline | **Evaluate** — decision, not vibes |
| Config artifact + seed parameters | **Reproducibility** — the chain from Module 01 |

Next module turns "this run is good" into "this run is *allowed to ship*" —
tests and gates.

---

**Next:** [lab.md](lab.md) — ten runs, one decision.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*