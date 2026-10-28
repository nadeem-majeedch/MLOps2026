"""Data tests: is the input what we claim it is? (Module 07)

Data tests run *before* modelling tests, because a model trained on bad data
passes every code test while being worthless. These reuse the validation checks
from Module 04 — one definition of "valid", used twice.
"""

from __future__ import annotations

from src.validate import REQUIRED_COLUMNS, run_checks


def test_all_required_columns_present(data):
    missing = [c for c in REQUIRED_COLUMNS if c not in data.columns]
    assert missing == []


def test_no_nulls_in_required_columns(data):
    assert int(data[REQUIRED_COLUMNS].isna().sum().sum()) == 0


def test_customer_ids_are_unique(data):
    assert int(data["customer_id"].duplicated().sum()) == 0


def test_numeric_columns_are_numeric(data, config):
    for col in config["features"]["numeric"] + [config["features"]["target"]]:
        assert data[col].dtype.kind in "iuf", f"{col} has dtype {data[col].dtype}"


def test_target_balance_within_expected_bounds(data):
    rate = float(data["churn"].mean())
    assert 0.02 <= rate <= 0.50, f"churn rate {rate:.3f} outside sane bounds"


def test_validator_passes_the_good_file(data):
    results = run_checks(data)
    failed = [r["name"] for r in results if not r["ok"]]
    assert failed == [], f"validator reported failures: {failed}"


def test_validator_catches_the_seeded_defect(data_path):
    """A test must also prove it can *fail*: feed it a known-bad file."""
    import pandas as pd

    bad = pd.read_csv(data_path.parents[1] / "corrupt" / "duplicates.csv")
    results = {r["name"]: r["ok"] for r in run_checks(bad)}
    assert results["unique_customer_id"] is False