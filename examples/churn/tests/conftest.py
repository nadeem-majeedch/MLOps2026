"""Shared pytest fixtures (Module 07).

The session-scoped fixtures below make the suite fast: data and config are
loaded once, then reused by every test. If the generated data is missing —
because someone cloned the repo fresh — it is regenerated here, so
`python -m pytest` always works on a clean checkout.
"""

from __future__ import annotations

import pathlib
import subprocess
import sys

import pandas as pd
import pytest
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def config() -> dict:
    return yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def data_path() -> pathlib.Path:
    path = ROOT / "data" / "raw" / "churn.csv"
    if not path.exists():
        subprocess.run([sys.executable, str(ROOT / "generate_data.py")], check=True)
    return path


@pytest.fixture(scope="session")
def data(data_path: pathlib.Path) -> pd.DataFrame:
    return pd.read_csv(data_path)