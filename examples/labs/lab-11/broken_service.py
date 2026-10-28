"""LAB 11 fixture — a service that answers wrong questions wrongly.

    python broken_service.py        # starts uvicorn on 127.0.0.1:8001
    python characterize.py          # (preferred) battery of bad requests,
                                    # prints observed vs expected behaviour

Scoring is a trivial formula on purpose — the exercise is *request
handling*, and this way no model file can hide the bugs. Six real defects
live in `predict()`; the lab's characterisation table tells you what the
HTTP contract SHOULD be, your job is to prove what it IS and fix it.
"""

from __future__ import annotations

import os

import uvicorn
from fastapi import FastAPI

app = FastAPI(title="subscription risk API (LAB 11 — intentionally broken)")

CONTRACTS = {"monthly", "one_year", "two_year"}


def score(record: dict) -> float:
    # defect lives here too: what happens when tenure_months is 0?
    base = record["monthly_charges"] / record["tenure_months"]
    bonus = 0.1 if record["contract_type"] == "monthly" else -0.05
    calls = 0.02 * record.get("support_calls", 0)
    return min(max(base * 0.1 + bonus + calls, 0.0), 1.0)


@app.post("/predict")
def predict(payload: dict) -> dict:
    """No request model at all (defect 1): the shape of the input is a
    wish, not a contract. Every defect below follows from that."""
    records = payload["records"]            # defect 2: missing key -> 500
    out = []
    for record in records:                  # defect 3: empty list -> 200 []
        probability = score(record)         # defects 4-6 inside score()/below
        out.append({
            "probability": round(probability, 4),
            "flag": int(probability >= 0.5),
            "contract": record.get("contract_type", "monthly"),  # unknown
            #                                              values pass through
        })
    return {"predictions": out}             # defect 5: no threshold echoed,
                                            # contract silently coerced


@app.get("/health")
def health() -> dict:
    # defect 6: a degraded state still answers 200 with an "error" body —
    # monitoring cannot tell the difference.
    if os.environ.get("MODEL_MISSING") == "1":
        return {"error": "no model loaded", "predictions_available": False}
    return {"status": "ok"}


def main() -> None:
    port = int(os.environ.get("PORT", "8001"))
    print(f"serving on http://127.0.0.1:{port}")
    uvicorn.run("broken_service:app", host="127.0.0.1", port=port,
                log_level="warning")


if __name__ == "__main__":
    main()