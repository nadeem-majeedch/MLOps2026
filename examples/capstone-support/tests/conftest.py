"""Shared fixtures for the capstone test suite (Module 07's pattern)."""

from __future__ import annotations

import pathlib

import pandas as pd
import pytest

from src import features as F

ROOT = pathlib.Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def config() -> dict:
    return F.load_config(ROOT / "config.yaml")


@pytest.fixture(scope="session")
def data_path() -> pathlib.Path:
    """Guarantee the dataset exists (a fresh clone runs the generator)."""
    path = ROOT / "data" / "support.csv"
    if not path.exists():
        import generate_data

        generate_data.main()
    return path


@pytest.fixture(scope="session")
def data(data_path: pathlib.Path) -> pd.DataFrame:
    return pd.read_csv(data_path)


@pytest.fixture(scope="session")
def trained(tmp_path_factory: pytest.TempPathFactory) -> dict:
    """Train once per session into an isolated copy of the config."""
    from src.train import train as train_fn

    return train_fn(str(ROOT / "config.yaml"), str(ROOT / "data" / "support.csv"))