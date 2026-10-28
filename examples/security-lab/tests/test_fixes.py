"""Fix-verification tests for Lab 15 (Module 15).

They are about YOUR repaired copy (`fixed/`), which does not exist in the
repository — so this module *skips* on a fresh clone (that skip is honest,
not a failure). Workflow:

    Copy-Item -Recurse flawed fixed        # 🪟   (cp -r flawed fixed 🐧)
    python make_model.py
    python -m pytest tests/test_fixes.py   # RED  - the five defects show up
    ... apply the fixes described in lab.md ...
    python -m pytest tests/test_fixes.py   # GREEN - evidence for the lab
"""

from __future__ import annotations

import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Skip the whole module until the student creates fixed/ (import errors in
# fixed/ itself are surfaced as failures — those are real red-phase signals).
pytest.importorskip("fixed.service", reason="create fixed/ first (lab step 1)")

SERVICE = ROOT / "fixed" / "service.py"
CONFIG = ROOT / "fixed" / "config.py"

GOOD = {
    "record": {
        "email": "amina@example.edu",
        "student_ref": "S-0007",
        "attendance_rate": 0.62,
        "prior_score": 55,
        "device_access": 0,
    }
}


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setenv("SERVICE_API_KEY", "unit-test-key-not-a-real-secret")
    from fastapi.testclient import TestClient
    from fixed.service import app

    return TestClient(app)


def _source(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


# --- defect 1: no secrets in source --------------------------------------
def test_config_reads_secrets_from_the_environment():
    source = _source(CONFIG)
    assert "prod-secret-2f8a1c77b4e9d0136ac5" not in source, \
        "the fake service key is still hard-coded in config.py"
    assert "Tr0ub4dor-3" not in source, "DB credentials are still in source"
    assert "environ" in source, "config.py must read the environment instead"


# --- defect 3: the endpoint requires authentication -----------------------
def test_unauthenticated_requests_are_rejected(client):
    response = client.post("/predict", json=GOOD)
    assert response.status_code == 401, "endpoint accepts anonymous callers"


def test_wrong_key_is_rejected(client, monkeypatch):
    monkeypatch.setenv("SERVICE_API_KEY", "unit-test-key-not-a-real-secret")
    response = client.post("/predict", json=GOOD,
                           headers={"X-API-Key": "not-the-key"})
    assert response.status_code in (401, 403)


def test_correct_key_is_accepted(client):
    response = client.post("/predict", json=GOOD,
                           headers={"X-API-Key": "unit-test-key-not-a-real-secret"})
    assert response.status_code == 200


# --- defect 2: no PII in logs --------------------------------------------
def test_email_never_reaches_the_log(client, caplog):
    import logging

    with caplog.at_level(logging.INFO):
        client.post("/predict", json=GOOD,
                    headers={"X-API-Key": "unit-test-key-not-a-real-secret"})
    text = caplog.text
    assert "amina@example.edu" not in text, "PII written to the log"
    assert "amina" not in text, "PII fragment written to the log"


# --- defect 4: no unverified deserialization ------------------------------
def test_model_loading_is_integrity_checked():
    source = _source(SERVICE)
    uses_pickle = "pickle" in source
    verifies = "hashlib" in source and "sha256" in source
    assert not uses_pickle or verifies, (
        "service.py still deserialises without an integrity check: "
        "either drop pickle or verify a sha256 digest before loading"
    )


# --- defect 5: one threshold for everybody --------------------------------
def test_threshold_does_not_depend_on_group():
    from fixed.service import flag_for_support

    same_probability = 0.40
    assert flag_for_support(same_probability, 0) == flag_for_support(
        same_probability, 1
    ), "identical probabilities must produce identical decisions"