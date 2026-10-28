"""Feature building and splitting (Module 05).

Design rules this file demonstrates:

* Preprocessing is declared *once* and travels with the model — this is why
  `sklearn.pipeline.Pipeline` exists. A model trained with one preprocessing
  path and served with another is the classic train/serve skew bug.
* Nothing here reads a random state from the environment or wall clock: the
  seed comes from the config, so runs are repeatable.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def load_config(path: str | Path) -> dict:
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_data(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path)


def build_preprocessor(config: dict) -> ColumnTransformer:
    feats = config["features"]
    numeric = feats["numeric"]
    categorical = feats["categorical"]

    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
        ]
    )


def split_xy(df: pd.DataFrame, config: dict):
    feats = config["features"]
    y = df[feats["target"]]
    x = df[feats["numeric"] + feats["categorical"]]
    return x, y


def split_data(x: pd.DataFrame, y: pd.Series, config: dict):
    return train_test_split(
        x,
        y,
        test_size=config["test_size"],
        random_state=config["seed"],
        stratify=y,
    )