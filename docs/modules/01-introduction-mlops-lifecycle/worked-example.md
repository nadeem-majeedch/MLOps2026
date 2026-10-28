# Worked example — reading the incident with pandas

A complete, runnable analysis of the Module 01 incident data. Everything below
was executed on the reference machine (Windows 11, Python 3.14, pandas 3.0.6)
and the output shown is what it actually printed. Copy the commands; your output
should match except where noted.

**Where:** the `examples/churn/01-autopsy/` folder of the repository.

---

## 1. Regenerate the incident data (proves it is reproducible)

```powershell
# 🪟 Windows / PowerShell
python make_fixture.py
```

```bash
# 🐧 Linux / macOS
python3 make_fixture.py
```

Actual output:

```text
metrics_snapshot.csv    rows=60  auc range=0.6031..0.7958
predictions_sample.csv  rows=200  v3 share=0.64
```

Two files were written: 60 days of daily monitoring numbers, and 200 prediction
records from the incident window.

## 2. Load and look before you trust

```python
import pandas as pd

m = pd.read_csv("metrics_snapshot.csv", parse_dates=["date"])
print("rows:", len(m), "| date range:", m.date.min().date(), "->", m.date.max().date())
print(m.head(3).to_string(index=False))
```

Actual output:

```text
rows: 60 | date range: 2026-07-01 -> 2026-08-29
        date model_version    auc  missing_rate  pred_volume  p95_latency_ms  drift_score
 2026-07-01            v2 0.7830        0.0036          404           188.8      0.0515
 2026-07-02            v2 0.7750        0.0037          414           189.5      0.0569
 2026-07-03            v2 0.7851        0.0040          431           190.6      0.0531
```

**Checkpoint:** you must see both `v2` and `v3` in `model_version`. If you see
only one, your file is truncated — regenerate it (step 1).

## 3. Compare the two model periods

```python
v2 = m[m.model_version == "v2"]
v3 = m[m.model_version == "v3"]

print(f"v2 auc mean={v2.auc.mean():.4f}  min={v2.auc.min():.4f}  max={v2.auc.max():.4f}")
print(f"v3 auc mean={v3.auc.mean():.4f}  min={v3.auc.min():.4f}  max={v3.auc.max():.4f}")
print(f"missing_rate  v2 mean={v2.missing_rate.mean():.4f}  v3 mean={v3.missing_rate.mean():.4f}")
print(f"drift_score   v2 mean={v2.drift_score.mean():.4f}  v3 mean={v3.drift_score.mean():.4f}")
```

Actual output:

```text
v2 auc mean=0.7814  min=0.7722  max=0.7958
v3 auc mean=0.6944  min=0.6031  max=0.7837
missing_rate  v2 mean=0.0042  v3 mean=0.0569
drift_score   v2 mean=0.0488  v3 mean=0.2356
```

**How to read this:**

- `v2` is *stable* — its AUC wobbles inside a narrow band (0.772–0.796). That
  band is noise, not decay.
- `v3` is *declining* — the mean drops ~0.09 and the minimum falls to 0.60. A
  trend inside a period is the signature of decay; a level change between
  periods is the signature of a bad release.
- Missing values went up **13×** (0.0042 → 0.0569) and drift went up **~5×**.
  Both moved *after* the release, which is what makes them evidence rather than
  coincidence.

## 4. Find the first day a sane threshold would have fired

```python
first_bad = m[(m.auc < 0.75) | (m.missing_rate > 0.03) | (m.drift_score > 0.15)]
print("first breach:", first_bad.iloc[0]["date"].date())
```

Actual output:

```text
first breach: 2026-08-14
```

The model was promoted on 2026-08-11; a threshold on AUC alone would have fired
**3 days later**. The human complaint came on 2026-08-24 — **10 days later**.
That gap is what monitoring buys you.

!!! note "Thresholds are a policy, not a fact"
    0.75 / 0.03 / 0.15 are course values chosen to make the point. In a real
    system they come from a decision about cost: *"how much damage do we accept
    before someone is paged?"* Module 14 covers choosing and testing them.

## 5. Look at predictions, not just aggregates

```python
p = pd.read_csv("predictions_sample.csv")
print("predictions rows:", len(p))
print(p.groupby("model_version")[["score", "latency_ms"]].mean().round(4).to_string())
print("labels missing:", int(p.actual_churn.isna().sum()), "of", len(p))
```

Actual output:

```text
predictions rows: 200
              score  latency_ms
model_version
v2           0.2611     165.7493
v3           0.1725     163.0898
labels missing: 60 of 200
```

**Reading it:** `v3` scores are systematically **lower** than `v2`'s for the same
kind of customer — the calibration moved when the model moved. And 30% of labels
are missing, because churn labels arrive late. That is why quality *appears*
fine in real time and only decays in hindsight — the exact reason a team can be
wrong for ten days.

## 6. What you have just done

You performed, in six steps, the diagnostic half of the MLOps lifecycle:

1. loaded **versioned** inputs (regenerated deterministically),
2. compared against the **previous period as a baseline**,
3. checked **data quality** (missing rate), not only model metrics,
4. evaluated against an explicit **threshold**,
5. cross-checked **aggregate** metrics against **record-level** predictions, and
6. quantified **delay** in labels — the reason monitoring must be proactive.

Modules 04, 06, and 14 each take one of those steps and turn it into an
automated, tested part of your pipeline.

---

**Next:** [lab.md](lab.md) — do this yourself, with questions to answer and
acceptance criteria to meet.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*