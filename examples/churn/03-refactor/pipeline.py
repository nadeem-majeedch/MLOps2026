"""The legacy notebook, refactored (Module 03 reference solution).

Same numbers as `legacy/analysis.ipynb`, expressed as:

* small functions with one job each,
* configuration in `config.yaml` instead of magic numbers scattered in cells,
* one declared entry point (`run.py`),
* no duplicated logic, no hidden state between cells.

Run it with:  python run.py
"""

from __future__ import annotations

import pathlib

import pandas as pd
import yaml
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

ROOT = pathlib.Path(__file__).parent
CONTRACT_MAP = {"monthly": 0, "one_year": 1, "two_year": 2}


def load_config(path: pathlib.Path) -> dict:
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_data(csv_path: pathlib.Path) -> pd.DataFrame:
    """Load and clean — one place, one behaviour."""
    return pd.read_csv(csv_path).dropna()


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Derived columns live in exactly one function."""
    out = df.copy()
    out["contract_num"] = out["contract_type"].map(CONTRACT_MAP)
    return out


def split(frame: pd.DataFrame, config: dict):
    features = config["features"]
    x = frame[features]
    y = frame["target"]
    return train_test_split(
        x,
        y,
        test_size=config["test_size"],
        random_state=config["seed"],
    )


def fit_and_score(x_train, x_test, y_train, y_test, config: dict) -> float:
    model = RandomForestClassifier(
        n_estimators=config["n_estimators"],
        random_state=config["seed"],
    )
    model.fit(x_train, y_train)
    return float(accuracy_score(y_test, model.predict(x_test)))


def churn_rate(df: pd.DataFrame, target: str) -> float:
    """One implementation — used everywhere, instead of computed twice."""
    return float(df[target].mean())