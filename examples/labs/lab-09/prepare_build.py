"""LAB 09 fixture — produce the build outputs that get staged.

    python prepare_build.py

Trains a tiny model on the shared synthetic dataset so `stager.py stage`
has real bytes to copy (and the lab has real bytes to tamper with).
"""

from __future__ import annotations

import json
import pathlib

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE.parent / "data" / "customers_clean.csv"
BUILD = HERE / "build"


def main() -> int:
    df = pd.read_csv(DATA)
    features = ["tenure_months", "monthly_charges", "support_calls",
                "contract_type"]
    x, y = df[features], df["churned"]
    model = Pipeline([
        ("cat", OneHotEncoder(handle_unknown="ignore")),
        ("clf", LogisticRegression(max_iter=1000)),
    ])
    model.fit(x, y)

    BUILD.mkdir(exist_ok=True)
    joblib.dump(model, BUILD / "model.joblib")
    (BUILD / "metrics.json").write_text(
        json.dumps({"roc_auc": 0.8874, "rows": len(df),
                    "model": "logreg-baseline"}, indent=2) + "\n",
        encoding="utf-8")
    (BUILD / "config.yaml").write_text(
        "seed: 20261026\nfloor_roc_auc: 0.75\n", encoding="utf-8")
    print(f"build/ ready: {', '.join(sorted(p.name for p in BUILD.iterdir()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())