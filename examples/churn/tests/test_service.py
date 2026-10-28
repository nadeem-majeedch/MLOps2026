"""API tests (Module 10) — run with: python -m pytest tests/test_service.py

These are integration tests against the real app object (TestClient sends
real HTTP requests through ASGI — no server, no network, no mocks of FastAPI).
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from service.app import app

client = TestClient(app)

GOOD = {
    "records": [
        {
            "tenure_months": 24,
            "monthly_charges": 70.0,
            "support_tickets": 2,
            "contract_type": "monthly",
        }
    ]
}


def test_health_is_ok_and_names_the_model():
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] in ("ok", "degraded")
    assert body["model_version"]


def test_model_info_exposes_the_contract():
    r = client.get("/model-info")
    assert r.status_code == 200
    body = r.json()
    assert "contract_type" in body["features"]["categorical"]
    assert body["threshold"] == 0.5
    assert "roc_auc" in body["metrics"]


def test_predict_returns_one_probability_per_record():
    payload = {"records": GOOD["records"] * 3}
    r = client.post("/predict", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert len(body["predictions"]) == 3
    for p in body["predictions"]:
        assert 0.0 <= p["churn_probability"] <= 1.0
        assert p["churn_pred"] in (0, 1)


def test_unknown_contract_type_is_rejected_with_a_useful_message():
    bad = {"records": [{**GOOD["records"][0], "contract_type": "lifetime"}]}
    r = client.post("/predict", json=bad)
    assert r.status_code == 422
    detail = " ".join(r.json()["detail"])
    assert "contract_type" in detail


def test_out_of_range_values_are_rejected():
    bad = {"records": [{**GOOD["records"][0], "tenure_months": 0}]}
    r = client.post("/predict", json=bad)
    assert r.status_code == 422
    assert "tenure_months" in " ".join(r.json()["detail"])


def test_empty_batch_is_rejected():
    r = client.post("/predict", json={"records": []})
    assert r.status_code == 422


def test_probability_is_deterministic_for_the_same_input():
    first = client.post("/predict", json=GOOD).json()
    second = client.post("/predict", json=GOOD).json()
    assert first == second


def test_missing_record_field_is_reported_by_field_name():
    bad = {"records": [{"tenure_months": 12, "contract_type": "monthly"}]}
    r = client.post("/predict", json=bad)
    assert r.status_code == 422
    detail = " ".join(r.json()["detail"])
    assert "monthly_charges" in detail