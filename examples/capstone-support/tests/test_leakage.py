"""Leakage-prevention tests (Modules 05 + 17).

These are regression tests for a *class of mistake*: a post-outcome column
entering the feature list. They fail loudly if anyone edits config.yaml
carelessly — which is exactly when this guard matters.
"""

from __future__ import annotations

from src import features as F
from src.validate import run_checks


def test_split_xy_returns_only_configured_features(data, config):
    x, y = F.split_xy(data, config)
    assert list(x.columns) == F.feature_columns(config)
    assert "term_end_flag" not in x.columns
    assert "student_ref" not in x.columns
    assert y.name == "at_risk"


def test_forbidden_columns_are_declared(config):
    forbidden = set(config["features"]["forbidden"])
    assert {"term_end_flag", "student_ref"} <= forbidden


def test_validator_rejects_a_config_that_references_leakage(data, config):
    bad = {**config, "features": {**config["features"],
           "numeric": config["features"]["numeric"] + ["term_end_flag"]}}
    failed = [c["name"] for c in run_checks(data, bad) if not c["ok"]]
    assert "no_forbidden_features" in failed


def test_split_xy_refuses_a_bad_config(data, config):
    bad = {**config, "features": {**config["features"],
           "categorical": ["term_end_flag"]}}
    try:
        F.split_xy(data, bad)
    except AssertionError:
        return
    raise AssertionError("split_xy accepted a forbidden feature column")


def test_train_val_test_split_is_disjoint_and_seeded(data, config):
    x, y = F.split_xy(data, config)
    a = F.train_val_test_split(x, y, config)
    b = F.train_val_test_split(x, y, config)
    x_train, x_val, x_test = a[0], a[1], a[2]
    # identical seeds -> identical splits (reproducibility)
    assert x_train.index.equals(b[0].index)
    assert x_test.index.equals(b[2].index)
    # the three parts are disjoint and cover every row
    combined = set(x_train.index) | set(x_val.index) | set(x_test.index)
    assert len(combined) == len(x)
    assert not (set(x_train.index) & set(x_test.index))