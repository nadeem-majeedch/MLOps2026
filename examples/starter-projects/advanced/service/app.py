"""Prediction service — the ADVANCED starter's HTTP surface.

    python -m service                # http://127.0.0.1:8000  (docs at /docs)
    python -m pytest -q              # tests never need a live server

Endpoints:
    GET  /health      liveness + which version is being served
    GET  /model-info  metrics, threshold, features, intended use
    POST /predict     batch scoring with a validated request contract

Design points the tests pin down:
  * the model is loaded ONCE at import (deterministic + fast),
  * invalid input is 422 with the offending field named — never a 500,
  * every prediction is appended to logs/predictions.jsonl for monitor.py,
  * the served version comes from the registry, so a rollback is visible
    from outside via /health.
"""

from __future__ import annotations

import json
import pathlib
from datetime import datetime, timezone
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

HERE = pathlib.Path(__file__).resolve().parent.parent
LOGS = HERE / "logs"
FEATURES = ["tenure_months", "monthly_charges", "support_calls",
            "contract_type"]


def resolve_model() -> dict:
    """Current registry version -> staged fallback -> raw artefact -> none."""
    state_path = HERE / "registry.json"
    if state_path.exists():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        vid = state.get("current")
        if vid:
            base = HERE / "versions" / vid
            info = json.loads((base / "model_info.json").read_text("utf-8"))
            return {"model": joblib.load(base / "model.joblib"),
                    "version": vid, "source": f"versions/{vid}", "info": info}

    if (HERE / "artifacts" / "model.joblib").exists():
        base = HERE / "artifacts"
        info = json.loads((base / "model_info.json").read_text("utf-8"))
        return {"model": joblib.load(base / "model.joblib"),
                "version": "artefact", "source": "artifacts", "info": info}
    return {"model": None, "version": "none", "source": "none", "info": {}}


class Record(BaseModel):
    """One customer record — bounds are the request contract."""

    tenure_months: int = Field(..., ge=1, le=72)
    monthly_charges: float = Field(..., ge=15.0, le=160.0)
    support_calls: int = Field(..., ge=0, le=20)
    contract_type: Literal["monthly", "one_year", "two_year"]


class PredictRequest(BaseModel):
    records: list[Record] = Field(..., min_length=1, max_length=1000)


class Prediction(BaseModel):
    churn_probability: float = Field(..., description="P(churn)")
    flag: int = Field(..., description="1 at the configured threshold")


class PredictResponse(BaseModel):
    model_version: str
    threshold: float
    predictions: list[Prediction]


INTENDED_USE = ("Baseline churn triage on synthetic-like data. "
                "Never the sole basis for a customer-facing decision.")

app = FastAPI(title="Churn scoring API (advanced starter)",
              description=INTENDED_USE, version="1.0.0")

_state = resolve_model()
THRESHOLD = float(_state["info"].get("threshold", 0.5))


@app.exception_handler(RequestValidationError)
async def validation_error(request, exc):          # noqa: ANN001, ARG001
    problems = [f"{'.'.join(str(p) for p in err['loc'] if p != 'body') or 'body'}: {err['msg']}"
                for err in exc.errors()]
    return JSONResponse(status_code=422,
                        content={"error": "invalid request", "detail": problems})


def _log_predictions(records: list[dict], probabilities: list[float]) -> None:
    """Append-only prediction log — the raw material for drift detection."""
    LOGS.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with (LOGS / "predictions.jsonl").open("a", encoding="utf-8") as fh:
        for record, proba in zip(records, probabilities, strict=True):
            fh.write(json.dumps({"at": stamp,
                                 "model_version": _state["version"],
                                 **record,
                                 "churn_probability": round(proba, 4)})
                     + "\n")


@app.get("/health")
def health() -> dict:
    return {"status": "ok" if _state["model"] is not None else "degraded",
            "model_version": _state["version"],
            "model_source": _state["source"]}


@app.get("/model-info")
def model_info() -> dict:
    info = _state["info"]
    return {"model_version": _state["version"],
            "model_source": _state["source"],
            "metrics": {k: v for k, v in info.items()
                        if isinstance(v, (int, float))},
            "threshold": THRESHOLD,
            "features": FEATURES,
            "intended_use": INTENDED_USE}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse | JSONResponse:
    if _state["model"] is None:
        return JSONResponse(       # type: ignore[return-value]
            status_code=503,
            content={"error": "no model loaded",
                     "detail": ["train one: python train.py",
                                "optionally stage it: python registry.py stage"]})
    rows = [r.model_dump() for r in request.records]
    frame = pd.DataFrame(rows)[FEATURES]
    proba = _state["model"].predict_proba(frame)[:, 1]
    _log_predictions(rows, [float(p) for p in proba])
    return PredictResponse(
        model_version=_state["version"],
        threshold=THRESHOLD,
        predictions=[{"churn_probability": round(float(p), 4),
                      "flag": int(p >= THRESHOLD)} for p in proba],
    )


def main() -> None:
    import os

    import uvicorn
    import yaml

    config_path = HERE / "config.yaml"
    service_cfg = (yaml.safe_load(config_path.read_text(encoding="utf-8"))
                   .get("service", {})) if config_path.exists() else {}
    host = os.environ.get("HOST", str(service_cfg.get("host", "127.0.0.1")))
    port = int(os.environ.get("PORT", str(service_cfg.get("port", 8000))))
    print(f"serving on http://{host}:{port}  (docs: /docs)")
    uvicorn.run("service.app:app", host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()
