"""Prediction service for the capstone (Modules 10 + 17).

    python -m service            # http://127.0.0.1:8000  (docs at /docs)

Loads the model ONCE at startup: the promoted release if one exists
(`release.json`), else the training artefact. /health reports which, so a
rollback (`python release.py rollback` + restart) is observable from outside.
"""

from __future__ import annotations

import json
import pathlib

import joblib
import pandas as pd
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

ROOT = pathlib.Path(__file__).resolve().parent.parent
FEATURES = ["attendance_rate", "prior_score", "lms_logins",
            "missed_assessments", "assignment_rate", "device_access"]
THRESHOLD_DEFAULT = 0.25


def resolve_model() -> dict:
    """Promoted release -> training artefact -> none (503 with instructions)."""
    state_path = ROOT / "release.json"
    if state_path.exists():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        rid = state.get("current")
        if rid:
            rdir = ROOT / "releases" / rid
            metrics = json.loads((rdir / "metrics.json").read_text(encoding="utf-8"))
            return {
                "model": joblib.load(rdir / "model.joblib"),
                "version": rid,
                "source": f"releases/{rid}/model.joblib",
                "threshold": float(metrics.get("threshold", THRESHOLD_DEFAULT)),
                "metrics": metrics,
            }

    artefact = ROOT / "artifacts" / "model.joblib"
    if artefact.exists():
        metrics = json.loads((ROOT / "artifacts" / "metrics.json").read_text(encoding="utf-8"))
        return {
            "model": joblib.load(artefact),
            "version": "artefact",
            "source": "artifacts/model.joblib",
            "threshold": float(metrics.get("threshold", THRESHOLD_DEFAULT)),
            "metrics": metrics,
        }
    return {"model": None, "version": "none", "source": "none",
            "threshold": THRESHOLD_DEFAULT, "metrics": {}}


class StudentRecord(BaseModel):
    """One student referral — synthetic attributes only (no identifiers)."""

    attendance_rate: float = Field(..., ge=0.0, le=1.0)
    prior_score: float = Field(..., ge=0, le=100)
    lms_logins: int = Field(..., ge=0, le=100)
    missed_assessments: int = Field(..., ge=0, le=30)
    assignment_rate: float = Field(..., ge=0.0, le=1.0)
    device_access: int = Field(..., ge=0, le=1,
                               description="1 = reliable device at home")


class PredictRequest(BaseModel):
    records: list[StudentRecord] = Field(..., min_length=1, max_length=1000)


class Prediction(BaseModel):
    support_probability: float = Field(..., description="P(at_risk)")
    flag_for_support: int = Field(..., description="1 at the frozen threshold")


class PredictResponse(BaseModel):
    model_version: str
    threshold: float
    intended_use: str
    predictions: list[Prediction]


app = FastAPI(
    title="Student-support early-alert API",
    description=("Scores synthetic student records to help counsellors "
                 "offer support earlier. Synthetic data; a support signal, "
                 "never an automated decision."),
    version="1.0.0",
)

_state = resolve_model()

INTENDED_USE = ("Triage aid for human counsellors on synthetic-like data. "
                "Never the sole basis for any decision about a student.")


@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
    problems = []
    for err in exc.errors():
        where = ".".join(str(p) for p in err["loc"] if p != "body")
        problems.append(f"{where or 'body'}: {err['msg']}")
    return JSONResponse(status_code=422,
                        content={"error": "invalid request", "detail": problems})


@app.get("/health")
def health() -> dict:
    return {"status": "ok" if _state["model"] is not None else "degraded",
            "model_version": _state["version"], "model_source": _state["source"]}


@app.get("/model-info")
def model_info() -> dict:
    metrics = {k: v for k, v in _state["metrics"].items() if isinstance(v, (int, float))}
    return {"model_version": _state["version"], "model_source": _state["source"],
            "metrics": metrics, "threshold": _state["threshold"],
            "features": FEATURES, "intended_use": INTENDED_USE}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    if _state["model"] is None:
        return JSONResponse(  # type: ignore[return-value]
            status_code=503,
            content={"error": "no model loaded",
                     "detail": ["train one: python pipeline.py",
                                "then:       python release.py register --note v1"]},
        )
    frame = pd.DataFrame([r.model_dump() for r in request.records])[FEATURES]
    proba = _state["model"].predict_proba(frame)[:, 1]
    return PredictResponse(
        model_version=_state["version"],
        threshold=_state["threshold"],
        intended_use=INTENDED_USE,
        predictions=[{"support_probability": round(float(p), 4),
                      "flag_for_support": int(p >= _state["threshold"])}
                     for p in proba],
    )