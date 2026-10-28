"""Reference FIXED service for LAB 11 (Module 10's contract, applied).

    python fixed_service.py        # starts on 127.0.0.1:8001 for manual poking

Every defect listed in ../../lab-11/broken_service.py is repaired here:

  1. no request model             -> Pydantic request models (422 with field names)
  2. payload["records"] KeyError  -> `records` is a required, typed field
  3. empty list accepted          -> min_length=1 on the records list
  4. score() divide-by-zero       -> tenure bounded ge=1, charges bounded
  5. unknown contract passes      -> Literal["monthly","one_year","two_year"]
  6. health 200 while degraded    -> 503 with a machine-readable body

The scoring formula is unchanged on purpose: only the *handling* of the
request changed. Run ../../lab-11/characterize.py against your own copy to
prove all 10 rows flip to `ok`.
"""

from __future__ import annotations

import os
from typing import Literal

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(title="subscription risk API (LAB 11 — reference fix)")

THRESHOLD = 0.5


class Record(BaseModel):
    """One subscription record — bounds come from the characterisation table."""

    tenure_months: int = Field(..., ge=1, le=120)
    monthly_charges: float = Field(..., ge=0.0, le=500.0)
    support_calls: int = Field(..., ge=0, le=50)
    contract_type: Literal["monthly", "one_year", "two_year"]


class PredictRequest(BaseModel):
    records: list[Record] = Field(..., min_length=1, max_length=1000)


def score(record: Record) -> float:
    base = record.monthly_charges / record.tenure_months   # tenure >= 1 now
    bonus = 0.1 if record.contract_type == "monthly" else -0.05
    calls = 0.02 * record.support_calls
    return min(max(base * 0.1 + bonus + calls, 0.0), 1.0)


@app.post("/predict")
def predict(request: PredictRequest) -> dict:
    out = []
    for record in request.records:
        probability = score(record)
        out.append({
            "probability": round(probability, 4),
            "flag": int(probability >= THRESHOLD),
            "contract": record.contract_type,   # validated, never coerced
        })
    return {"threshold": THRESHOLD, "predictions": out}


@app.get("/health")
def health():
    if os.environ.get("MODEL_MISSING") == "1":
        # degraded state -> 503 with a machine-readable body: monitoring
        # can tell the difference between "ok" and "sorry, not now".
        return JSONResponse(status_code=503,
                            content={"error": "no model loaded",
                                     "predictions_available": False})
    return {"status": "ok", "predictions_available": True}


def main() -> None:
    port = int(os.environ.get("PORT", "8001"))
    print(f"serving on http://127.0.0.1:{port}")
    uvicorn.run("fixed_service:app", host="127.0.0.1", port=port,
                log_level="warning")


if __name__ == "__main__":
    main()
