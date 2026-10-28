"""Train a baseline churn model — BEGINNER starter project.

    python train.py            # trains, prints metrics, writes out/metrics.json

Deliberately small and flat: three files (`churndata.py`, `config.yaml`,
this one) are the whole project. The intermediate starter turns the same
idea into a validated pipeline; the advanced starter serves it over HTTP.
"""

from __future__ import annotations

import json
import pathlib

import joblib
import pandas as pd
import yaml
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             roc_auc_score)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

import churndata

HERE = pathlib.Path(__file__).resolve().parent
NUMERIC = ["tenure_months", "monthly_charges", "support_calls"]
CATEGORICAL = ["contract_type"]
FEATURES = NUMERIC + CATEGORICAL


def load_config(path: pathlib.Path = HERE / "config.yaml") -> dict:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def train_and_evaluate(df: pd.DataFrame, config: dict) -> tuple[Pipeline, dict]:
    """Fit a pipeline and return (model, metrics). No hidden state."""
    x = df[FEATURES]
    y = df["churned"]
    x_tr, x_te, y_tr, y_te = train_test_split(
        x, y,
        test_size=config["test_size"],
        random_state=config["seed"],
        stratify=y,
    )

    prep = ColumnTransformer([
        ("num", StandardScaler(), NUMERIC),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
    ])
    model = Pipeline([
        ("prep", prep),
        ("clf", LogisticRegression(max_iter=1000,
                                   random_state=config["seed"])),
    ])
    model.fit(x_tr, y_tr)

    proba = model.predict_proba(x_te)[:, 1]
    pred = (proba >= config["threshold"]).astype(int)
    metrics = {
        "roc_auc": round(float(roc_auc_score(y_te, proba)), 4),
        "accuracy": round(float(accuracy_score(y_te, pred)), 4),
        "precision": round(float(precision_score(y_te, pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_te, pred, zero_division=0)), 4),
        "rows_train": int(len(x_tr)),
        "rows_test": int(len(x_te)),
        "seed": int(config["seed"]),
    }
    return model, metrics


def main() -> int:
    config = load_config()
    df = churndata.load()
    model, metrics = train_and_evaluate(df, config)

    out = HERE / "out"
    out.mkdir(exist_ok=True)
    joblib.dump(model, out / "model.joblib")
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n",
                                      encoding="utf-8")

    print("baseline churn model")
    for key, value in metrics.items():
        print(f"  {key:12} {value}")
    print(f"artefacts -> {out.relative_to(HERE)}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
