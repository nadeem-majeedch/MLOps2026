# Troubleshooting — Module 06

Tracking problems seen while writing this course's labs are listed first — they
are real, not hypothetical. General issues:
[course troubleshooting](../../troubleshooting/index.md).

## 1. The backend error (you will hit this if you improvise)

```text
mlflow.exceptions.MlflowException: The filesystem tracking backend (e.g., './mlruns')
is in maintenance mode and will not receive further updates. Please migrate to a
database backend (e.g., 'sqlite:///mlflow.db') ...
```

**Cause:** MLflow 3.x refuses the legacy plain-folder store.
**Fix:** use a database backend — still local:

```python
mlflow.set_tracking_uri("sqlite:///mlflow.db")
```

(The course script already does. If you need the old behaviour explicitly, MLflow
offers an opt-out env var and a migration tool — read the URL in the error
message; do not copy it blindly into every project.)

## 2. Runs and queries

| Symptom | Likely cause | Fix |
|---|---|---|
| `ModuleNotFoundError: mlflow` | Wrong interpreter | `.venv\Scripts\python -m pip install mlflow` 🪟 / equivalent 🐧 |
| `mlflow: command not found` | Console script not on PATH | Use `python -m pip show mlflow` to confirm, then run via the project script or `python -m mlflow` |
| Run created but shows no params/metrics | Logging code not reached (exception before it, or run context closed) | Wrap logging *inside* `with mlflow.start_run(...)`; check for an early `return` |
| Runs land in different experiments | Different `set_experiment` names in different scripts | Print `mlflow.search_experiments()` and standardise the name |
| `search_runs` returns an empty DataFrame | Wrong tracking URI or experiment name | Set the URI explicitly; list experiments before querying |
| Metrics look right, artifacts missing | `log_artifact` called with a relative path from another working directory | Run from `examples/churn`, or pass absolute paths |
| UI shows no runs | Server pointed at a different store | Start with `--backend-store-uri sqlite:///mlflow.db` from the same folder |
| Two runs, identical params, different metrics | Unseeded randomness (Module 05) | Fix the seed before comparing — otherwise the sweep measures noise |

## 3. Evaluation mistakes (not tooling)

| You are tempted to… | Instead… |
|---|---|
| Call the max-AUC run "the best" | Apply your **pre-stated** rule; if none exists, write one before looking again |
| Compare runs made on different data versions | Fix the data version; a comparison across versions measures the data, not the model |
| Report 0.01 AUC as a win | Compare against the measured seed noise (~0.03 here); re-run with several seeds |
| Lead with accuracy on a 9% positive rate | Choose the metric from the business question (recall@k, precision@k) |
| Log raw data "for completeness" | Reference it by version/hash; keep the store small and data private |

## 4. Concept blocks

| Stuck because… | Reframe |
|---|---|
| "Do I need a tracking *server*?" | No for logging (the script writes directly to the store); yes only for the UI or remote access |
| "What is the difference between experiment and run?" | Filing cabinet vs. a document inside it |
| "Why not just a CSV of results?" | It works to run ~10; tracking adds identity, artifacts, lineage, and query — try joining a CSV to its model file six months later |
| "Should I track every debug run?" | Track runs you might compare later; delete nothing — a tagged `failed:` run is information too |
| "Is this data private if MLflow logs it?" | You logged metrics and params, not rows; keep data out of artifacts, keep the store local, and the answer stays yes |

## 5. If your numbers do not match the course's

1. Confirm data hash `18df7e78…` and validation `7/7`.
2. Confirm config values (`seed 42`, `test_size 0.2`, `family logistic`).
3. Record versions: `mlflow`, `pandas`, `scikit-learn`.
4. If they still differ on identical inputs, report it as a course issue with
   your command and output — do not adjust your results to match ours.

---

[← Knowledge check](knowledge-check.md) · [References →](references.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*