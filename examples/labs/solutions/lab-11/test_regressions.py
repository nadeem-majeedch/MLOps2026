"""Regression tests for the LAB 11 contract (starter — adapt the import).

    python -m pytest test_regressions.py -q

Point `SERVICE` at whatever you fixed:
  * your own repaired service -> change the import to your module name
  * this reference solution    -> `fixed_service` (as shipped)

Each case is one row of the characterisation table from
../../lab-11/characterize.py: expected status, observed status, and for
validation failures the offending field must be named in the body. These
tests are the *regression net*: once green they must never go red again,
which is exactly the point of writing them after the fix.
"""

from __future__ import annotations

import json

from fastapi.testclient import TestClient

from fixed_service import app   # <- swap for your module (e.g. broken_service)

client = TestClient(app, raise_server_exceptions=False)

BASE = {"tenure_months": 12, "monthly_charges": 85.0,
        "support_calls": 4, "contract_type": "monthly"}

# (name, body, expected status, field that must appear in the body)
CASES = [
    ("missing charges",
     {"records": [{"tenure_months": 12, "contract_type": "monthly"}]},
     422, "monthly_charges"),
    ("negative tenure",
     {"records": [{**BASE, "tenure_months": -3}]}, 422, "tenure_months"),
    ("charges out of range",
     {"records": [{**BASE, "monthly_charges": -20}]}, 422, "monthly_charges"),
    ("zero tenure (div-by-0)",
     {"records": [{**BASE, "tenure_months": 0}]}, 422, "tenure_months"),
    ("unknown contract",
     {"records": [{**BASE, "contract_type": "prepaid"}]}, 422, "contract_type"),
    ("empty records", {"records": []}, 422, "records"),
    ("records not a list", {"records": "yes"}, 422, "records"),
    ("no records key", {"rows": []}, 422, "records"),
]


def test_valid_record_is_200_with_threshold():
    r = client.post("/predict", json={"records": [BASE]})
    assert r.status_code == 200
    body = r.json()
    assert body["threshold"] == 0.5
    assert 0.0 <= body["predictions"][0]["probability"] <= 1.0


def test_health_ok_is_200():
    assert client.get("/health").status_code == 200


def test_characterisation_rows():
    for name, body, expected, field in CASES:
        r = client.post("/predict", json=body)
        assert r.status_code == expected, f"{name}: {r.status_code}"
        if expected == 422:
            assert field in json.dumps(r.json().get("detail", "")), name


def test_degraded_health_is_503():
    import os
    os.environ["MODEL_MISSING"] = "1"
    try:
        r = client.get("/health")
        assert r.status_code == 503
        assert r.json()["predictions_available"] is False
    finally:
        os.environ.pop("MODEL_MISSING", None)


def test_predict_is_deterministic():
    a = client.post("/predict", json={"records": [BASE]}).json()
    b = client.post("/predict", json={"records": [BASE]}).json()
    assert a == b
