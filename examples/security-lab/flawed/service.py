"""Deliberately FLAWED prediction service — Lab 15's audit target.

Five defects, on purpose:

  1. hard-coded service key and DB credentials   (config.py)
  2. PII (an email address) written to logs      (predict below)
  3. no authentication on the endpoint           (predict below)
  4. unsafe deserialization: pickle.load         (load_model below)
  5. a group-dependent decision threshold        (flag_for_support below)

Audit it, then fix YOUR copy:  Copy-Item -Recurse flawed fixed  (🪟)
or  cp -r flawed fixed  (🐧). The fix-verification tests skip until
`fixed/` exists — see tests/test_fixes.py.
"""

from __future__ import annotations

import logging
import pickle
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, Field

from flawed import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("flawed-service")

app = FastAPI(title="Support early-alert API (FLAWED audit target)")

HERE = Path(__file__).resolve().parent


def load_model(path: Path | str | None = None):
    """Defect 4: pickle.load executes whatever bytes are on disk.

    If an attacker can swap `model.pkl` (a shared drive, a compromised
    build step, a careless download), they run arbitrary code as your
    service. There is no integrity check of any kind.
    """
    target = Path(path) if path else HERE / "model.pkl"
    with open(target, "rb") as fh:
        return pickle.load(fh)


def flag_for_support(probability: float, device_access: int) -> int:
    """Defect 5: the decision threshold depends on the student's group.

    Same probability, different outcome — a group-dependent rule that
    silently advantages one group. Lab step 6 quantifies it.
    """
    threshold = 0.25 if device_access == 1 else 0.60
    return int(probability >= threshold)


class Record(BaseModel):
    email: str = Field(..., description="contact email — PII")
    student_ref: str = Field(..., description="internal student reference")
    attendance_rate: float = Field(..., ge=0.0, le=1.0)
    prior_score: float = Field(..., ge=0, le=100)
    device_access: int = Field(..., ge=0, le=1)


class PredictRequest(BaseModel):
    record: Record


@app.post("/predict")
def predict(request: PredictRequest) -> dict:
    # Defect 2: PII straight into the log line. Logs are copied to support
    # tools, retained for months, and read by far more people than the DB.
    logger.info(
        "predict email=%s ref=%s attendance=%s",
        request.record.email,
        request.record.student_ref,
        request.record.attendance_rate,
    )
    # Defect 3: no authentication — anyone who can reach the port can score
    # records (and read defect 2's logs back out through their side effects).
    model = load_model()
    probability = float(model.get("score", 0.42))  # toy stub score
    return {
        "probability": probability,
        "flag_for_support": flag_for_support(
            probability, request.record.device_access
        ),
        "service_key": config.API_KEY,  # defect 1, now also an info leak
    }