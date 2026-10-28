"""The FastAPI application (Module 10).

Run it:  python -m service      (then open http://127.0.0.1:8000/docs)

Endpoints
    GET  /health      liveness: is the process up, which model is loaded
    GET  /model-info  what exactly is serving (version, metrics, features)
    POST /predict     batch scoring; schema-validated, 422 on bad input
"""

from __future__ import annotations

import pandas as pd
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from service.model import FEATURES, THRESHOLD, resolve_model
from service.schemas import (
    HealthResponse,
    ModelInfoResponse,
    Prediction,
    PredictRequest,
    PredictResponse,
)

app = FastAPI(
    title="Churn prediction API",
    description=(
        "Scores customers for churn. Synthetic Lahore Retail Co. data, "
        "model trained by the MLOps course example pipeline."
    ),
    version="1.0.0",
)

# Resolve the model ONCE at import time (not per request).
_state = resolve_model()


@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Turn pydantic's raw errors into messages a caller can act on."""
    problems = []
    for err in exc.errors():
        where = ".".join(str(p) for p in err["loc"] if p != "body")
        problems.append(f"{where or 'body'}: {err['msg']}")
    return JSONResponse(
        status_code=422,
        content={"error": "invalid request", "detail": problems},
    )


@app.get("/health", response_model=HealthResponse, tags=["ops"])
def health() -> HealthResponse:
    """Liveness probe. Cheap, no model work: an orchestrator will poll this."""
    return HealthResponse(
        status="ok" if _state["model"] is not None else "degraded",
        model_version=_state["version"],
        model_source=_state["source"],
    )


@app.get("/model-info", response_model=ModelInfoResponse, tags=["ops"])
def model_info() -> ModelInfoResponse:
    """Exactly what is serving: version, quality, feature contract, threshold."""
    return ModelInfoResponse(
        model_version=_state["version"],
        model_source=_state["source"],
        model_sha256=_state["sha256"],
        metrics={k: v for k, v in _state["metrics"].items()
                 if isinstance(v, (int, float))},
        features=FEATURES,
        threshold=THRESHOLD,
    )


@app.post("/predict", response_model=PredictResponse, tags=["scoring"])
def predict(request: PredictRequest) -> PredictResponse:
    if _state["model"] is None:
        return JSONResponse(  # type: ignore[return-value]
            status_code=503,
            content={
                "error": "no model loaded",
                "detail": [
                    "train one first: python -m pipe.run",
                    ("or register one:  python -m registry register "
                     "--model pipe_out/model.joblib "
                     "--metrics pipe_out/train_metrics.json"),
                ],
            },
        )

    frame = pd.DataFrame([r.model_dump() for r in request.records])
    frame = frame[list(FEATURES["numeric"]) + list(FEATURES["categorical"])]
    proba = _state["model"].predict_proba(frame)[:, 1]
    predictions = [
        Prediction(
            churn_probability=round(float(p), 4),
            churn_pred=int(p >= THRESHOLD),
        )
        for p in proba
    ]
    return PredictResponse(
        model_version=_state["version"],
        threshold=THRESHOLD,
        predictions=predictions,
    )