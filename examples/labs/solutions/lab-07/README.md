# LAB-07 — reference solution

> Attempt the lab first. This is the answer key, not the assignment.

## The two numbers (verified on the authoring machine)

```text
as shipped:   reported roc_auc = 1.0000   "suspiciously good"
honest re-run: test roc_auc = 0.8245
```

*(Your honest figure will land near 0.82 — it depends on your exact
split seed. The point is the gap: 1.0000 was never a model quality
number, it was a measurement error.)*

## The three defects, by their standard names

| # | In the fixture | Standard name | Why it inflates the score |
|---|---|---|---|
| 1 | `retention_offered = (churned == 1)` and `last_offer_outcome = churned.map(…)` in `load()` | **Target leakage** (features derived from the label) | the model reads the answer key; timing question: these are known *after* the churn event, not at prediction time |
| 2 | `StandardScaler().fit_transform(x)` before any split | **Preprocessing leakage** (fit on data outside the training fold) | the scaler's mean/σ already include the test rows |
| 3 | `model.fit(X, y)` then `predict_proba(X)` on the **same** rows; `roc_auc_score(y, …)` | **Train-on-test evaluation** (no held-out set) | scoring memorised data |

## The honest fix, in order

```python
df = pd.read_csv(DATA)
feats = ["tenure_months", "monthly_charges", "support_calls", "contract_type"]
x = pd.get_dummies(df[feats], columns=["contract_type"]); y = df["churned"]

x_tr, x_te, y_tr, y_te = train_test_split(x, y, test_size=0.25,
                                          stratify=y, random_state=42)
pipe = Pipeline([("scale", StandardScaler()),          # fit = train rows only
                 ("model", GradientBoostingClassifier(n_estimators=150,
                                                      random_state=0))])
pipe.fit(x_tr, y_tr)
auc = roc_auc_score(y_te, pipe.predict_proba(x_te)[:, 1])
```

The `Pipeline` is the structural fix for #2: scikit-learn fits the
scaler **inside** each training fold, so leakage cannot reappear the
next time you refactor.

## Reasoning checkpoints (model answers)

- **Why is defect 1 the worst?** Defects 2 and 3 inflate a number;
  defect 1 builds a model whose inputs *do not exist* at the moment of
  prediction — it would fail in production even if evaluated honestly.
- **"Would this feature exist at scoring time?"** is the leakage
  question. Ask it of every column, not just suspicious ones.
- **Why not just delete the bad rows?** Leakage is structural; you fix
  the pipeline, not the data.
- **Both transcripts in `evidence.md`:** the 1.0000 run *and* the honest
  run — the comparison is the learning object.

## Common wrong answers

- "Fixing" defect 3 by reporting training accuracy on the test split —
  you need untouched rows the model never saw.
- Removing the leaked columns but keeping fit-on-all-data — the number
  stays inflated and you misattribute the cause.
- Declaring 0.8245 "the true AUC" — it is one honest estimate on one
  split; say the split, the seed, and the confidence you do not have.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../../docs/about/index.md).*