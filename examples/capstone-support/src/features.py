"""Feature construction and splitting (Modules 05 + 17).

One deliberate design: `split_xy` returns ONLY the configured feature columns,
so the leakage guard (forbidden columns) is enforced structurally — a column
not in the config can never reach the model, however tempting the CSV.
"""

from __future__ import annotations

import pathlib

import pandas as pd
import yaml
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def load_config(path: str | pathlib.Path) -> dict:
    return yaml.safe_load(pathlib.Path(path).read_text(encoding="utf-8"))


def load_data(path: str | pathlib.Path) -> pd.DataFrame:
    return pd.read_csv(path)


def feature_columns(config: dict) -> list[str]:
    feats = config["features"]
    return list(feats["numeric"]) + list(feats["categorical"])


def split_xy(df: pd.DataFrame, config: dict) -> tuple[pd.DataFrame, pd.Series]:
    """X = configured features only. Asserts the leakage guard as code."""
    feats = config["features"]
    chosen = feature_columns(config)
    forbidden = set(feats["forbidden"])
    assert not (forbidden & set(chosen)), (
        f"forbidden columns in feature list: {sorted(forbidden & set(chosen))}"
    )
    assert set(chosen + [feats["target"]]).issubset(df.columns), "missing columns"
    return df[chosen].copy(), df[feats["target"]].copy()


def build_preprocessor(config: dict) -> ColumnTransformer:
    feats = config["features"]
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), list(feats["numeric"])),
            ("cat", OneHotEncoder(handle_unknown="ignore"),
             list(feats["categorical"])),
        ]
    )


def train_val_test_split(
    x: pd.DataFrame, y: pd.Series, config: dict
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame,
           pd.Series, pd.Series, pd.Series]:
    """Train / validation / test — stratified, seeded, in that order.

    The test set is produced here but consumed ONCE, by the final evaluation:
    model choice and threshold use train+validation only (leakage prevention).
    """
    x_tmp, x_test, y_tmp, y_test = train_test_split(
        x, y, test_size=config["test_size"], random_state=config["seed"],
        stratify=y,
    )
    rel_val = config["val_size"] / (1.0 - config["test_size"])
    x_train, x_val, y_train, y_val = train_test_split(
        x_tmp, y_tmp, test_size=rel_val, random_state=config["seed"],
        stratify=y_tmp,
    )
    return x_train, x_val, x_test, y_train, y_val, y_test