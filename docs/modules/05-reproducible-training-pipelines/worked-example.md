# Worked example — two runs, one hash

All output below is **actual**, captured on the reference machine in
`examples/churn/` (Windows 11, Python 3.14, pandas 3.0.6, scikit-learn 1.9.1).

---

## 1. Train once

```powershell
# 🪟 Windows / PowerShell — from examples/churn
python -m src.train --config config.yaml --data data/raw/churn.csv
```

Actual output:

```json
{
  "model_family": "logistic",
  "accuracy": 0.91,
  "roc_auc": 0.7163,
  "f1": 0.0,
  "positive_rate_test": 0.09,
  "n_train": 1600,
  "n_test": 400,
  "seed": 42
}
```

Record the artefact's fingerprint:

```powershell
# 🪟
(Get-FileHash artifacts\model.joblib -Algorithm MD5).Hash.ToLower()
# 🐧
md5sum artifacts/model.joblib
```

Actual: `8a172026a7f5f015194cb14b6bd55159`

## 2. Train again — and compare

```powershell
python -m src.train --config config.yaml --data data/raw/churn.csv
```

Actual result: the metrics JSON is **identical** line for line, and the model hash
is again `8a172026a7f5f015194cb14b6bd55159`.

✅ **Checkpoint 1 — reproducibility:** same metrics *and* same bytes. The second
is the stronger claim: it proves nothing invisible changed (an unseeded step
would alter the file even when metrics rounded the same).

## 3. Change exactly one config value

Copy `config.yaml`, change `seed: 42` → `seed: 4242`, and run with it:

```powershell
python -m src.train --config _tmp.yaml --data data/raw/churn.csv
```

Actual output:

```json
{
  "model_family": "logistic",
  "accuracy": 0.91,
  "roc_auc": 0.7418,
  "f1": 0.0,
  "positive_rate_test": 0.09,
  "n_train": 1600,
  "n_test": 400,
  "seed": 4242
}
```

✅ **Checkpoint 2 — configuration governs the run:** the seed changed, so the
*split* changed, so a different 400 rows were held out: AUC moved 0.7163 → 0.7418
while accuracy stayed 0.91.

**This is a measured lesson, not a theoretical one:** with 400 test rows and
only ~36 churners, metric movement of this size is *sampling noise*. A single
run's AUC is not a verdict — which is precisely why Module 06 tracks experiments
in batches and Module 07 sets thresholds you can defend.

## 4. Change the model family

```powershell
python -m src.train --config config.yaml --data data/raw/churn.csv --family gradient_boosting
```

Actual output:

```json
{
  "model_family": "gradient_boosting",
  "accuracy": 0.9,
  "roc_auc": 0.6431,
  "f1": 0.0476,
  "positive_rate_test": 0.09,
  "n_train": 1600,
  "n_test": 400,
  "seed": 42
}
```

| Model | accuracy | **roc_auc** | f1 |
|---|---|---|---|
| logistic (baseline) | 0.91 | **0.7163** | 0.0 |
| gradient_boosting (challenger) | 0.90 | **0.6431** | 0.0476 |

**The fancier model loses on ranking** (AUC), ties roughly on accuracy, and
scarcely finds any churners either. On this dataset — a near-linear signal with
9% positives and 1,600 training rows — the simpler model generalises better.
(Held-out AUCs measured alongside: logistic 0.7163, gradient boosting 0.6431,
histographic gradient boosting 0.5736 on the same split.)

**Why the course shows this:** "we used the advanced model" is not a result.
Beating a baseline, on a stated metric, with a stated split, is.

## 5. Read the metrics honestly

- `accuracy 0.91` equals the **majority baseline** (91% of test rows are
  non-churn). Accuracy alone proves nothing here — concepts §5.
- `f1 0.0` means the model predicted **no churners** at a 0.5 threshold. Not a
  code fault: rare events rarely cross 0.5. The fix is a *decision* about
  threshold, made later and recorded — not a silent default.
- `roc_auc 0.7163` is the honest signal: the model ranks churners above
  non-churners about 72% of the time — useful, modest, and far from the 0.91
  accuracy headline.

## 6. What you have built

```python
# src/train.py — the shape, not the whole file
pipeline = Pipeline([
    ("preprocess", build_preprocessor(config)),   # no leakage: fit only on train
    ("model", build_model(config, family)),       # seeded from config
])
pipeline.fit(x_train, y_train)
joblib.dump(pipeline, config["output"]["model_path"])   # one artefact
```

Five guarantees, each verified above:

1. Same inputs ⇒ same outputs (hash).
2. Config governs behaviour (seed change).
3. Preprocessing travels with the model (single `Pipeline`).
4. Metrics are written beside the model (`metrics.json`).
5. Nothing random is unseeded — and nothing else about the environment is
   assumed, because you pinned it in Module 02.

---

**Next:** [lab.md](lab.md) — prove reproducibility yourself, then break it on purpose to find where determinism actually comes from.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*