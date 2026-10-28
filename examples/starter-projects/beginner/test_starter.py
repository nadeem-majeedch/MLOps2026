"""Tests for the BEGINNER starter — your first ML tests.

    python -m pytest -q

Three ideas worth noticing:
  * schema tests catch silent column drift,
  * determinism tests catch accidental randomness,
  * metric sanity tests catch a pipeline that "trains" but learns nothing.
"""

from __future__ import annotations

import json
import pathlib

import churndata
import train

HERE = pathlib.Path(__file__).resolve().parent


def test_dataset_schema_matches_the_documented_contract():
    df = churndata.generate()
    assert list(df.columns) == churndata.COLUMNS
    assert len(df) == churndata.ROWS
    assert set(df["contract_type"].unique()) <= {"monthly", "one_year",
                                                 "two_year"}
    assert set(df["churned"].unique()) <= {0, 1}
    assert not df.isna().any().any()


def test_generation_is_deterministic():
    a = churndata.generate()
    b = churndata.generate()
    assert a.equals(b), "same seed must produce the same rows, byte for byte"


def test_training_produces_sane_metrics_and_artefacts(tmp_path):
    config = train.load_config()
    df = churndata.generate()
    model, metrics = train.train_and_evaluate(df, config)

    assert 0.5 < metrics["roc_auc"] <= 1.0, metrics
    assert 0.0 <= metrics["accuracy"] <= 1.0
    assert metrics["rows_train"] + metrics["rows_test"] == len(df)

    # the model must actually predict, and predictably
    row = df[train.FEATURES].head(1)
    first = model.predict_proba(row)[0][1]
    second = model.predict_proba(row)[0][1]
    assert first == second

    out = tmp_path / "metrics.json"
    out.write_text(json.dumps(metrics), encoding="utf-8")
    assert json.loads(out.read_text(encoding="utf-8"))["seed"] == config["seed"]
