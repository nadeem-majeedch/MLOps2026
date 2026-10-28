"""LAB 01 fixture — a training script whose answer changes every run.

    python train_nondeterministic.py            # metrics.json (overwritten)
    python train_nondeterministic.py --label a   # keep one run's output

The bug is deliberate: three independent sources of nondeterminism hide in
here (find all three). Nothing is random about the *data* — the file on
disk is fixed — so every difference between two runs comes from this code.
"""

from __future__ import annotations

import argparse
import json
import pathlib

import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import f1_score, roc_auc_score
from sklearn.model_selection import train_test_split

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE.parent / "data" / "customers_clean.csv"
NUMERIC = ["tenure_months", "monthly_charges", "support_calls"]
CATEGORICAL = ["contract_type"]


def load() -> pd.DataFrame:
    df = pd.read_csv(DATA)
    # source of nondeterminism #1: the rows themselves get shuffled with no
    # seed... (does shuffling matter for a split? think about it)
    return df.sample(frac=1).reset_index(drop=True)


def build_xy(df: pd.DataFrame):
    features = NUMERIC + CATEGORICAL
    x = pd.get_dummies(df[features], columns=CATEGORICAL)
    y = df["churned"]
    return x, y


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", default="", help="suffix for the output file")
    args = parser.parse_args(argv)

    df = load()
    x, y = build_xy(df)

    # source of nondeterminism #2: 80% of the rows are used, chosen by a
    # random process... "the more data the better, right?"
    sample = df.sample(frac=0.8)
    idx = sample.index
    x_use, y_use = x.loc[idx], y.loc[idx]

    # source of nondeterminism #3: a gradient-boosted model with subsample
    # enabled and no random_state...
    model = GradientBoostingClassifier(
        n_estimators=120, subsample=0.8, random_state=None
    )
    x_tr, x_te, y_tr, y_te = train_test_split(
        x_use, y_use, test_size=0.25, stratify=y_use  # no random_state either!
    )
    model.fit(x_tr, y_tr)
    proba = model.predict_proba(x_te)[:, 1]
    pred = (proba >= 0.5).astype(int)

    metrics = {
        "roc_auc": round(float(roc_auc_score(y_te, proba)), 4),
        "f1": round(float(f1_score(y_te, pred)), 4),
        "n_test_rows": int(len(y_te)),
    }
    out = HERE / (f"metrics{('_' + args.label) if args.label else ''}.json")
    out.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metrics, indent=2))
    print(f"-> {out.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())