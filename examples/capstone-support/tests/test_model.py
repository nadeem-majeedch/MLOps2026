"""Model tests: gate, determinism, fairness arithmetic (Modules 06/07/15)."""

from __future__ import annotations

import json
import pathlib

import joblib
import numpy as np
import pandas as pd

from src import features as F
from src.train import fairness_audit, train

ROOT = pathlib.Path(__file__).resolve().parent.parent


def test_quality_gate_passes(trained, config):
    floor = float(config["quality"]["roc_auc_floor"])
    assert trained["roc_auc"] >= floor, (
        f"test AUC {trained['roc_auc']} below the floor {floor}"
    )


def test_model_selection_used_validation_not_test(trained):
    # The winner must be explainable from the validation table alone.
    val = trained["validation_by_family"]
    expected = max(val, key=lambda f: val[f]["roc_auc"])
    assert trained["winner"] == expected


def test_operating_point_came_from_the_allowed_range(trained):
    assert 0.05 <= trained["threshold"] <= 0.95


def test_training_is_deterministic_for_the_same_seed(config):
    first = train(str(ROOT / "config.yaml"), str(ROOT / "data" / "support.csv"))
    second = train(str(ROOT / "config.yaml"), str(ROOT / "data" / "support.csv"))
    assert first["roc_auc"] == second["roc_auc"]
    assert first["winner"] == second["winner"]
    assert first["threshold"] == second["threshold"]


def test_probabilities_and_flags_are_consistent(trained, config, data):
    model = joblib.load(ROOT / "artifacts" / "model.joblib")
    metrics = json.loads((ROOT / "artifacts" / "metrics.json").read_text(encoding="utf-8"))
    x, _ = F.split_xy(data, config)
    proba = model.predict_proba(x)[:, 1]
    assert np.all((proba >= 0) & (proba <= 1))
    flags = (proba >= metrics["threshold"]).astype(int)
    assert set(np.unique(flags)) <= {0, 1}


def test_fairness_audit_arithmetic():
    frame = pd.DataFrame({"device_access": [0, 0, 1, 1, 1, 1]})
    pred = np.array([1, 0, 0, 0, 1, 0])          # rates: 0->0.5, 1->0.25
    audit = fairness_audit(frame, pred, "device_access", max_gap=0.10)
    assert audit["selection_rate_by_group"] == {"0": 0.5, "1": 0.25}
    assert audit["selection_rate_gap"] == 0.25
    assert audit["within_target"] is False       # honest over-target flag
    assert "caveat" in audit


def test_fairness_within_target_flag_matches_the_threshold():
    frame = pd.DataFrame({"g": [0, 1]})
    audit = fairness_audit(frame, np.array([1, 1]), "g", max_gap=0.10)
    assert audit["selection_rate_gap"] == 0.0
    assert audit["within_target"] is True