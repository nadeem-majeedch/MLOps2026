"""API tests (Module 10's pattern) for the capstone service."""

from __future__ import annotations

import pytest

GOOD = {
    "records": [
        {"attendance_rate": 0.62, "prior_score": 55.0, "lms_logins": 3,
         "missed_assessments": 4, "assignment_rate": 0.45, "device_access": 0}
    ]
}


@pytest.fixture()
def client(trained):
    """Import the app only after a model exists (session training fixture)."""
    from fastapi.testclient import TestClient

    from service.app import app

    return TestClient(app)


def test_health_reports_the_serving_version(client):
    body = client.get("/health").json()
    assert body["status"] == "ok"
    assert body["model_version"]


def test_model_info_states_intended_use(client):
    body = client.get("/model-info").json()
    assert body["intended_use"]
    assert "roc_auc" in body["metrics"]
    assert body["features"]


def test_predict_scores_a_batch(client):
    payload = {"records": GOOD["records"] * 4}
    body = client.post("/predict", json=payload).json()
    assert len(body["predictions"]) == 4
    for p in body["predictions"]:
        assert 0.0 <= p["support_probability"] <= 1.0
        assert p["flag_for_support"] in (0, 1)
    assert body["threshold"] > 0


def test_predict_is_deterministic(client):
    assert (client.post("/predict", json=GOOD).json()
            == client.post("/predict", json=GOOD).json())


def test_out_of_range_attendance_is_rejected(client):
    bad = {"records": [{**GOOD["records"][0], "attendance_rate": 1.4}]}
    response = client.post("/predict", json=bad)
    assert response.status_code == 422
    assert "attendance_rate" in " ".join(response.json()["detail"])


def test_invalid_device_access_code_is_rejected(client):
    bad = {"records": [{**GOOD["records"][0], "device_access": 7}]}
    assert client.post("/predict", json=bad).status_code == 422


def test_empty_batch_is_rejected(client):
    assert client.post("/predict", json={"records": []}).status_code == 422


def test_missing_field_names_the_field(client):
    bad = {"records": [{"attendance_rate": 0.9, "device_access": 1}]}
    response = client.post("/predict", json=bad)
    assert response.status_code == 422
    assert "prior_score" in " ".join(response.json()["detail"])