"""Tests for the INTERMEDIATE starter.

    python -m pytest -q

Four groups: configuration refuses nonsense, the data contract refuses
bad frames, the pipeline runs end to end and writes a manifest, and the
whole thing is deterministic.
"""

from __future__ import annotations

import json

import pandas as pd
import pytest

from pipeline import data as D
from pipeline import run as R
from pipeline.config import ConfigError, load_config


# ---------------------------------------------------------------- config

def test_valid_config_loads():
    config = load_config()
    assert 0.0 < config["test_size"] < 1.0
    assert config["threshold"] in (0.0, 0.5, 1.0) or 0 <= config["threshold"] <= 1


def test_config_rejects_impossible_values():
    for bad in (
        {"seed": 1, "rows": 800, "test_size": 1.5, "threshold": 0.5,
         "output_dir": "out"},
        {"seed": 1, "rows": 800, "test_size": 0.25, "threshold": 2.0,
         "output_dir": "out"},
        {"seed": 1, "rows": 10, "test_size": 0.25, "threshold": 0.5,
         "output_dir": "out"},
        {"seed": 1, "test_size": 0.25, "threshold": 0.5, "output_dir": "out"},
    ):
        with pytest.raises(ConfigError):
            from pipeline.config import validate
            validate(bad)


# ------------------------------------------------------------ data contract

def test_clean_data_passes_the_contract():
    assert D.validate(D.generate()) == []
    assert D.validated(D.generate()) is not None


def test_contract_refuses_missing_column():
    df = D.generate().drop(columns=["support_calls"])
    problems = D.validate(df)
    assert any("support_calls" in p for p in problems)


def test_contract_refuses_out_of_range_and_duplicates():
    df = D.generate()
    df.loc[0, "monthly_charges"] = -99.0
    df.loc[1, "customer_id"] = df.loc[0, "customer_id"]
    problems = D.validate(df)
    assert any("monthly_charges" in p for p in problems)
    assert any("duplicate" in p for p in problems)

    with pytest.raises(D.DataValidationError) as exc:
        D.validated(df)
    assert exc.value.problems                      # the error names the issues


def test_contract_refuses_schema_drift_and_nulls():
    df = D.generate()
    df["new_column"] = 1
    df.loc[0, "churned"] = None
    problems = D.validate(df)
    assert any("schema drift" in p or "unexpected" in p for p in problems)
    assert any("null" in p for p in problems)


# --------------------------------------------------------------- pipeline

def test_pipeline_runs_and_writes_manifest(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "OUT", tmp_path)
    config = load_config()
    manifest = R.run(config, force=True)
    assert manifest["ok"] is True
    assert [s["stage"] for s in manifest["stages"]] == ["generate", "train"]
    assert all(s["status"] == "ok" for s in manifest["stages"])
    assert (tmp_path / "manifest.json").exists()
    assert (tmp_path / "metrics.json").exists()
    metrics = json.loads((tmp_path / "metrics.json").read_text("utf-8"))
    assert 0.5 < metrics["roc_auc"] <= 1.0


def test_pipeline_is_deterministic(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "OUT", tmp_path)
    config = load_config()
    R.run(config, force=True)
    first = (tmp_path / "metrics.json").read_text("utf-8")
    R.run(config, force=True)
    second = (tmp_path / "metrics.json").read_text("utf-8")
    assert first == second


def test_generated_frame_is_stable():
    a = D.generate()
    b = D.generate()
    assert isinstance(a, pd.DataFrame) and a.equals(b)
