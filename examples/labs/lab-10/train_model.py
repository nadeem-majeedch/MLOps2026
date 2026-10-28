"""LAB 10 fixture — the model your service must serve (run this first).

    python train_model.py        # -> model.joblib + model_info.json

Deliberately trivial: the exercise is the SERVICE, not the modelling.
"""

from __future__ import annotations

import json
import pathlib

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE.parent / "data" / "customers_clean.csv"
NUMERIC = ["tenure_months", "monthly_charges", "support_calls"]
CATEGORICAL = ["contract_type"]
FEATURES = NUMERIC + CATEGORICAL


def main() -> int:
    df = pd.read_csv(DATA)
    pre = ColumnTransformer([
        ("num", StandardScaler(), NUMERIC),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
    ])
    model = Pipeline([
        ("prep", pre),
        ("clf", LogisticRegression(max_iter=1000)),
    ])
    model.fit(df[FEATURES], df["churned"])

    joblib.dump(model, HERE / "model.joblib")
    info = {
        "features": FEATURES,
        "types": {"tenure_months": "number 0-120",
                  "monthly_charges": "number 0-500",
                  "support_calls": "integer 0-50",
                  "contract_type": "one of monthly|one_year|two_year"},
        "target": "churned (probability of churn)",
        "trained_on": "synthetic customers_clean.csv, 600 rows, seed 20261026",
    }
    (HERE / "model_info.json").write_text(json.dumps(info, indent=2) + "\n",
                                          encoding="utf-8")
    print("wrote model.joblib + model_info.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())