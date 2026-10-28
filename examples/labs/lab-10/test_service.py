"""LAB 10 acceptance tests — the contract YOUR app.py must satisfy.

    python train_model.py          # produce model.joblib first
    python -m pytest test_service.py -v

The tests skip until you create `app.py` exposing a FastAPI `app`
(they import `app`). That skip is the honest state of an undone exercise.

Contract under test (also stated in lab.md):
  GET  /health       -> {"status": "ok", "model_loaded": true}
  GET  /model-info   -> features + target description from model_info.json
  POST /predict      body  {"records": [{tenure_months, monthly_charges,
                                         support_calls, contract_type}]}
                        ->   {"threshold": float,
                              "predictions": [{"churn_probability": float,
                                               "flag": 0|1}]}
  validation         -> 422 with the offending field named; empty list = 422
"""

from __future__ import annotations

import json
import pathlib
import sys

import pytest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

pytest.importorskip("app", reason="create app.py first (see lab.md step 4)")

GOOD = {"records": [{"tenure_months": 12, "monthly_charges": 85.0,
                     "support_calls": 6, "contract_type": "monthly"}]}


@pytest.fixture(scope="module")
def client():
    from fastapi.testclient import TestClient

    from app import app

    return TestClient(app)


def test_health_reports_loaded_state(client):
    body = client.get("/health").json()
    assert body["status"] == "ok" and body["model_loaded"] is True


def test_model_info_exposes_features_and_target(client):
    body = client.get("/model-info").json()
    assert "tenure_months" in body["features"]
    assert body["target"]


def test_predict_returns_probability_and_flag(client):
    body = client.post("/predict", json=GOOD).json()
    assert 0.0 <= body["predictions"][0]["churn_probability"] <= 1.0
    assert body["predictions"][0]["flag"] in (0, 1)
    assert body["threshold"] == 0.5


def test_predict_is_deterministic(client):
    assert (client.post("/predict", json=GOOD).json()
            == client.post("/predict", json=GOOD).json())


def test_batch_of_three(client):
    payload = {"records": GOOD["records"] * 3}
    assert len(client.post("/predict", json=payload).json()["predictions"]) == 3


def _detail(response) -> str:
    return json.dumps(response.json().get("detail", ""))


def test_missing_field_is_422_and_named(client):
    bad = {"records": [{"tenure_months": 12, "contract_type": "monthly"}]}
    r = client.post("/predict", json=bad)
    assert r.status_code == 422
    assert "monthly_charges" in _detail(r)


def test_out_of_range_is_422(client):
    bad = {"records": [{**GOOD["records"][0], "tenure_months": -4}]}
    r = client.post("/predict", json=bad)
    assert r.status_code == 422
    assert "tenure_months" in _detail(r)


def test_unknown_contract_is_422(client):
    bad = {"records": [{**GOOD["records"][0], "contract_type": "prepaid"}]}
    r = client.post("/predict", json=bad)
    assert r.status_code == 422
    assert "contract_type" in _detail(r)


def test_empty_records_is_422(client):
    assert client.post("/predict", json={"records": []}).status_code == 422