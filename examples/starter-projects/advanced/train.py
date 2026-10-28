"""ADVANCED starter — train the model and write the artefact.

    python train.py            # -> artifacts/model.joblib + model_info.json
                               #    + data/reference.csv (drift baseline)

Same recipe as the beginner/intermediate starters, but the outputs are
shaped for a *service*: an artefact folder, a model card-ish info file,
and a reference window the monitor can compare future traffic against.
"""

from __future__ import annotations

import json
import pathlib

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

HERE = pathlib.Path(__file__).resolve().parent
ARTIFACTS = HERE / "artifacts"
DATA = HERE / "data"
NUMERIC = ["tenure_months", "monthly_charges", "support_calls"]
CATEGORICAL = ["contract_type"]
FEATURES = NUMERIC + CATEGORICAL
SEED = 20261103
ROWS = 1200


def generate(rows: int = ROWS, seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    tenure = rng.integers(1, 72, rows)
    charges = np.round(rng.normal(70, 25, rows).clip(15, 160), 2)
    calls = rng.integers(0, 10, rows)
    contract = rng.choice(["monthly", "one_year", "two_year"], rows,
                          p=[0.5, 0.3, 0.2])
    logits = (-0.04 * tenure - 0.03 * calls + 0.012 * (charges - 70)
              + np.where(contract == "monthly", 0.8, -0.3))
    churned = (logits + rng.normal(0, 0.9, rows) > 0).astype(int)
    return pd.DataFrame({
        "customer_id": [f"ADV-{i:04d}" for i in range(1, rows + 1)],
        "tenure_months": tenure,
        "monthly_charges": charges,
        "support_calls": calls,
        "contract_type": contract,
        "churned": churned,
    })


def train(df: pd.DataFrame) -> tuple[Pipeline, dict]:
    x, y = df[FEATURES], df["churned"]
    x_tr, x_te, y_tr, y_te = train_test_split(x, y, test_size=0.25,
                                              random_state=SEED, stratify=y)
    prep = ColumnTransformer([
        ("num", StandardScaler(), NUMERIC),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
    ])
    model = Pipeline([
        ("prep", prep),
        ("clf", LogisticRegression(max_iter=1000, random_state=SEED)),
    ])
    model.fit(x_tr, y_tr)
    auc = float(roc_auc_score(y_te, model.predict_proba(x_te)[:, 1]))
    return model, {"roc_auc": round(auc, 4), "seed": SEED,
                   "rows": int(len(df)), "threshold": 0.5}


def main() -> int:
    df = generate()
    model, info = train(df)

    ARTIFACTS.mkdir(exist_ok=True)
    DATA.mkdir(exist_ok=True)
    joblib.dump(model, ARTIFACTS / "model.joblib")
    info["features"] = FEATURES
    info["contract_type_values"] = ["monthly", "one_year", "two_year"]
    (ARTIFACTS / "model_info.json").write_text(
        json.dumps(info, indent=2) + "\n", encoding="utf-8")
    df.head(400).to_csv(DATA / "reference.csv", index=False)  # drift baseline

    print("advanced starter — artefacts written")
    print(f"  roc_auc {info['roc_auc']}  rows {info['rows']}")
    print("  artifacts/model.joblib + model_info.json + data/reference.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
