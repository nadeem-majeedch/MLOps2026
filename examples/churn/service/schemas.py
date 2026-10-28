"""Request/response schemas (Module 10).

The schema *is* the API contract: it validates every request before any
code touches the model, and FastAPI turns violations into a structured 422.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

ContractType = Literal["monthly", "one_year", "two_year"]


class CustomerRecord(BaseModel):
    """One customer as the application sees it (names match the dataset)."""

    tenure_months: int = Field(..., ge=1, le=120,
                               description="whole months with the service")
    monthly_charges: float = Field(..., gt=0, le=1000,
                                   description="monthly charge, PKR-thousands")
    support_tickets: int = Field(..., ge=0, le=50,
                                 description="support contacts last month")
    contract_type: ContractType = Field(...,
                                        description="monthly | one_year | two_year")


class PredictRequest(BaseModel):
    records: list[CustomerRecord] = Field(
        ..., min_length=1, max_length=1000,
        description="1-1000 customers per call (batching keeps requests cheap)",
    )


class Prediction(BaseModel):
    churn_probability: float = Field(..., description="P(churn), 0-1")
    churn_pred: int = Field(..., description="1 if probability >= threshold, else 0")


class PredictResponse(BaseModel):
    model_version: str
    threshold: float
    predictions: list[Prediction]


class HealthResponse(BaseModel):
    status: Literal["ok", "degraded"]
    model_version: str
    model_source: str


class ModelInfoResponse(BaseModel):
    model_version: str
    model_source: str
    model_sha256: str
    metrics: dict[str, float]
    features: dict[str, list[str]]
    threshold: float