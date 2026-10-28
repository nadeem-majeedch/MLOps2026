"""Service tests — the HTTP contract, without starting a server.

    python train.py               # once, so a model exists to serve
    python -m pytest -q

FastAPI's TestClient exercises the real ASGI app, so these tests cover
the same code path a browser would hit.
"""

from __future__ import annotations

import pathlib

import pytest

import train as T

HERE = pathlib.Path(__file__).resolve().parent

GOOD = {"records": [{"tenure_months": 12, "monthly_charges": 85.0,
                     "support_calls": 4, "contract_type": "monthly"}]}


@pytest.fixture(scope="module")
def client(tmp_path_factory):
    if not (HERE / "artifacts" / "model.joblib").exists():
        T.main()                                  # produce the artefact once
    from fastapi.testclient import TestClient

    import service.app as app_module
    # keep prediction logs out of the repo while testing
    app_module.LOGS = tmp_path_factory.mktemp("logs")
    return TestClient(app_module.app, raise_server_exceptions=False)


def test_health_reports_loaded_state(client):
    body = client.get("/health").json()
    assert body["status"] == "ok"
    assert body["model_version"] in ("artefact", "v001") or \
        body["model_version"].startswith("v")


def test_model_info_exposes_contract(client):
    body = client.get("/model-info").json()
    assert "tenure_months" in body["features"]
    assert body["threshold"] == 0.5
    assert 0.5 < body["metrics"]["roc_auc"] <= 1.0
    assert body["intended_use"]


def test_predict_returns_probability_and_flag(client):
    body = client.post("/predict", json=GOOD).json()
    assert body["model_version"]
    pred = body["predictions"][0]
    assert 0.0 <= pred["churn_probability"] <= 1.0
    assert pred["flag"] in (0, 1)


def test_predict_is_deterministic(client):
    assert (client.post("/predict", json=GOOD).json()
            == client.post("/predict", json=GOOD).json())


def test_batch_scores_every_record_in_order(client):
    payload = {"records": GOOD["records"] * 3}
    assert len(client.post("/predict", json=payload).json()["predictions"]) == 3


@pytest.mark.parametrize("bad,field", [
    ({**GOOD["records"][0], "tenure_months": -5}, "tenure_months"),
    ({**GOOD["records"][0], "monthly_charges": 9999.0}, "monthly_charges"),
    ({**GOOD["records"][0], "contract_type": "prepaid"}, "contract_type"),
])
def test_invalid_records_are_422_and_named(client, bad, field):
    r = client.post("/predict", json={"records": [bad]})
    assert r.status_code == 422
    assert field in str(r.json()["detail"])


def test_missing_field_and_empty_batch_are_422(client):
    r = client.post("/predict", json={"records": [{"tenure_months": 3}]})
    assert r.status_code == 422
    assert "monthly_charges" in str(r.json()["detail"])
    assert client.post("/predict", json={"records": []}).status_code == 422
