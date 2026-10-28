"""Unit tests: small pieces of logic, in isolation (Module 07).

Unit tests answer: "does this function do what its name says?"
They are the cheapest tests to write and the fastest to run.
"""

from __future__ import annotations

import pandas as pd

from src.features import build_preprocessor, split_data, split_xy


def test_load_config_returns_expected_keys(config):
    assert {"seed", "test_size", "features", "model"} <= set(config)


def test_split_xy_returns_only_configured_features(data, config):
    x, y = split_xy(data, config)
    expected = config["features"]["numeric"] + config["features"]["categorical"]
    assert list(x.columns) == expected
    assert y.name == config["features"]["target"]
    assert len(x) == len(y) == len(data)


def test_split_respects_test_size_and_seed(data, config):
    x, y = split_xy(data, config)
    x1, x2, y1, y2 = split_data(x, y, config)
    assert len(x1) + len(x2) == len(x)
    assert abs(len(x2) / len(x) - config["test_size"]) < 0.01
    # stratified split keeps the churn rate similar in both halves
    assert abs(y1.mean() - y2.mean()) < 0.02


def test_split_is_deterministic(data, config):
    x, y = split_xy(data, config)
    a = split_data(x, y, config)   # returns (x_train, x_test, y_train, y_test)
    b = split_data(x, y, config)
    pd.testing.assert_frame_equal(a[0], b[0])
    pd.testing.assert_series_equal(a[2], b[2])


def test_preprocessor_handles_unknown_categories(config):
    prep = build_preprocessor(config)
    frame = pd.DataFrame(
        {
            "tenure_months": [12],
            "monthly_charges": [55.0],
            "support_tickets": [2],
            "contract_type": ["lifetime_deal"],   # a category never seen in training
        }
    )
    prep.fit(frame)
    transformed = prep.transform(frame)
    assert transformed.shape[0] == 1