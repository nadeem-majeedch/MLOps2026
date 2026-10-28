"""LAB 07 fixture — a model that looks brilliant for three bad reasons.

    python leaky_model.py

Reports suspiciously good metrics. Three leakage/validation defects are
seeded (names below are hidden from you on purpose — the lab says find
them, the comments here are the shape of the fix, not the answer).

Your job: write pytest tests that FAIL against this file and PASS against
your fixed version (the tests are the deliverable; see ../solutions/lab-07/
only afterwards).
"""

from __future__ import annotations

import pathlib

import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE.parent / "data" / "customers_clean.csv"

BASE_FEATURES = ["tenure_months", "monthly_charges", "support_calls",
                 "contract_type"]


def load() -> pd.DataFrame:
    df = pd.read_csv(DATA)
    # "helpful enrichment" from the CRM join... think hard about *when*
    # this column becomes known relative to the prediction moment.
    df["retention_offered"] = (df["churned"] == 1).astype(int)
    df["last_offer_outcome"] = df["churned"].map({0: "no", 1: "accepted"})
    return df


def build_model() -> Pipeline:
    return Pipeline([
        ("scale", StandardScaler()),
        ("model", GradientBoostingClassifier(n_estimators=150, random_state=0)),
    ])


def main() -> int:
    df = load()
    features = BASE_FEATURES + ["retention_offered", "last_offer_outcome"]
    x = pd.get_dummies(df[features], columns=["contract_type",
                                              "last_offer_outcome"])
    y = df["churned"]

    # defect 2 lives here: the scaler's fit() sees data it should not have
    x_scaled = StandardScaler().fit_transform(x)

    # defect 3 lives here: where exactly is the holdout?
    model = build_model()
    model.fit(pd.DataFrame(x_scaled, columns=x.columns), y)
    proba = model.predict_proba(pd.DataFrame(x_scaled, columns=x.columns))[:, 1]
    auc = roc_auc_score(y, proba)

    print(f"reported roc_auc = {auc:.4f}")
    if auc >= 0.95:
        print("-> suspiciously good. Ask three questions before celebrating.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())