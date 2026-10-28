# LAB-06 — reference solution

> Attempt the lab first. This is the answer key, not the assignment.

## Environment note (verified on the authoring machine)

`mlflow 3.17.2` is installed; a local file store needs no server or
account:

```powershell
mlflow server --host 127.0.0.1 --port 5000   # optional UI; runs are logged either way
python sweep.py
mlflow runs list -e lab06
```

## The decision rule — chosen **before** looking

Write it down first, then run the sweep. A defensible rule:

> **Champion = the family with the higher *mean* ROC AUC across seeds
> 1–5**, provided (a) every run logged the same `data_sha256`, and
> (b) the mean margin over the baseline exceeds one pooled standard
> deviation of the baseline runs. Ties → prefer the simpler/faster
> model.

What makes this rule good: it is aggregate-not-best (a lucky seed is
not a finding), it is pre-registered (no post-hoc cherry-picking), and
it has a stated tie-break.

## What `decision.md` must contain

1. **The rule**, quoted verbatim from your pre-registration note.
2. **The table:** 10 rows — run id, family, seed, roc_auc, data_sha256,
   duration; then two summary rows (mean ± sd per family).
3. **The champion** by the rule, with the margin over baseline stated
   as a number.
4. **Variance commentary:** e.g. "family X spans 0.7X–0.7Y across
   seeds — a single run of either family could have flipped the
   ranking, which is why family choice must never rest on one run."
5. **What you refuse to conclude:** nothing about production
   performance from a 600-row synthetic dataset.

## Sanity checks before you trust your own result

```powershell
mlflow runs search -e lab06 --order-by "metrics.roc_auc DESC"   # sorted view
# every run carries the same data hash:
mlflow runs list -e lab06   # data_sha256 column identical in all 10 rows
```

If `data_sha256` differs between runs you mixed datasets — the sweep is
void regardless of the scores (LAB-04's lesson, restated).

## Common wrong answers

- Champion = highest single run — that measures luck, not quality.
- Different `test_size`/split strategy per family — the comparison is
  then between *splits*, not models.
- Logging the metric but not `data_sha256` — you cannot later prove
  what the numbers were computed from.
- Letting MLflow's best-run view make the decision for you — the
  aggregation rule is *yours*, stated before the runs existed.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../../docs/about/index.md).*