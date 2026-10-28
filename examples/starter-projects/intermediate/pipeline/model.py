"""Model stage — train and evaluate, deterministically.

    model, metrics = train_and_evaluate(df, config)

Same modelling recipe as the beginner starter (so you can compare
like with like), but every input is now data-validated first and every
output is a plain dict you can log, diff, or assert on in tests.
"""

from __future__ import annotations

from typing import Any

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             roc_auc_score)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUMERIC = ["tenure_months", "monthly_charges", "support_calls"]
CATEGORICAL = ["contract_type"]
FEATURES = NUMERIC + CATEGORICAL


def build_pipeline(seed: int) -> Pipeline:
    """The estimator, assembled from config — no hidden defaults."""
    prep = ColumnTransformer([
        ("num", StandardScaler(), NUMERIC),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
    ])
    return Pipeline([
        ("prep", prep),
        ("clf", LogisticRegression(max_iter=1000, random_state=seed)),
    ])


def train_and_evaluate(df: pd.DataFrame,
                       config: dict[str, Any]) -> tuple[Pipeline, dict]:
    x, y = df[FEATURES], df["churned"]
    x_tr, x_te, y_tr, y_te = train_test_split(
        x, y, test_size=config["test_size"], random_state=config["seed"],
        stratify=y)

    model = build_pipeline(config["seed"])
    model.fit(x_tr, y_tr)

    proba = model.predict_proba(x_te)[:, 1]
    pred = (proba >= config["threshold"]).astype(int)
    metrics: dict[str, Any] = {
        "roc_auc": round(float(roc_auc_score(y_te, proba)), 4),
        "accuracy": round(float(accuracy_score(y_te, pred)), 4),
        "precision": round(float(precision_score(y_te, pred,
                                                  zero_division=0)), 4),
        "recall": round(float(recall_score(y_te, pred, zero_division=0)), 4),
        "threshold": float(config["threshold"]),
        "seed": int(config["seed"]),
        "rows": int(len(df)),
    }
    return model, metrics
