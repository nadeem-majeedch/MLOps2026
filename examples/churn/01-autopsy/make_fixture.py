"""Generate the synthetic incident bundle used by Lab 01 (Module 01).

Deliberately *bad* data on purpose: this is the aftermath of a fictional model
failure. Nothing here is a real measurement.

    python make_fixture.py

Outputs:
    metrics_snapshot.csv     60 days of daily monitoring numbers (synthetic)
    predictions_sample.csv   200 prediction records from the incident (synthetic)
"""

from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd

SEED = 1301
ROOT = pathlib.Path(__file__).parent


def metrics_snapshot() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    days = pd.date_range("2026-07-01", periods=60, freq="D")
    day_no = np.arange(60)

    # Days 0-40: model v2 is stable. Day 41: model v3 is silently promoted.
    # After day 41 quality decays, and a schema change lands on day 45.
    auc = 0.78 + rng.normal(0, 0.006, 60)
    post = day_no >= 41
    auc[post] = np.linspace(0.78, 0.61, post.sum()) + rng.normal(0, 0.006, post.sum())

    missing_rate = np.abs(rng.normal(0.004, 0.001, 60))
    missing_rate[day_no >= 45] = np.abs(rng.normal(0.07, 0.01, (day_no >= 45).sum()))

    pred_volume = rng.poisson(420, 60)
    p95_latency = np.abs(rng.normal(180, 12, 60)) + np.where(day_no >= 50, 90, 0)
    drift_score = np.abs(rng.normal(0.05, 0.01, 60))
    drift_score[day_no >= 48] = np.abs(rng.normal(0.34, 0.03, (day_no >= 48).sum()))

    version = np.where(day_no < 41, "v2", "v3")

    return pd.DataFrame(
        {
            "date": days.strftime("%Y-%m-%d"),
            "model_version": version,
            "auc": auc.round(4),
            "missing_rate": missing_rate.round(4),
            "pred_volume": pred_volume,
            "p95_latency_ms": p95_latency.round(1),
            "drift_score": drift_score.round(4),
        }
    )


def predictions_sample() -> pd.DataFrame:
    rng = np.random.default_rng(SEED + 1)
    n = 200
    days = pd.date_range("2026-08-14", periods=3, freq="h")
    version = rng.choice(["v2", "v3"], size=n, p=[0.35, 0.65])
    score = rng.beta(2, 5, size=n)
    # v3 scores are shifted — the calibration changed and nobody re-baselined it.
    score = np.where(version == "v3", np.clip(score - 0.12, 0, 1), score)
    actual = rng.binomial(1, np.clip(score + 0.05, 0, 1))
    actual = np.where(rng.uniform(size=n) < 0.30, np.nan, actual)  # labels arrive late

    return pd.DataFrame(
        {
            "ts": rng.choice(days.astype(str), size=n),
            "customer_id": [f"C{200000 + i}" for i in range(n)],
            "score": score.round(4),
            "actual_churn": actual,
            "model_version": version,
            "feature_source": np.where(version == "v3", "features_v3", "features_v2"),
            "latency_ms": np.round(np.abs(rng.normal(160, 30, n)), 1),
        }
    )


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    m = metrics_snapshot()
    p = predictions_sample()
    m.to_csv(ROOT / "metrics_snapshot.csv", index=False)
    p.to_csv(ROOT / "predictions_sample.csv", index=False)
    print(f"metrics_snapshot.csv    rows={len(m)}  auc range={m['auc'].min()}..{m['auc'].max()}")
    print(f"predictions_sample.csv  rows={len(p)}  v3 share={(p['model_version'] == 'v3').mean():.2f}")


if __name__ == "__main__":
    main()