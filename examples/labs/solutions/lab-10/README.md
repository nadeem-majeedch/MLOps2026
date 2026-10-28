# LAB-10 — reference solution

> Attempt the lab first. This is the answer key, not the assignment.

## What "done" means: 9 tests, no skips

```powershell
python train_model.py            # writes model.joblib + model_info.json
python -m pytest test_service.py -v
# as shipped: SKIPPED [1] create app.py first (see lab.md step 4)
# after your app.py: 9 passed
```

The skip is deliberate: `pytest.importorskip("app")` means *the exercise
is not done yet*, not *the suite is broken*.

## The contract, test by test

| Test | Your app must do |
|---|---|
| `test_health_reports_loaded_state` | `GET /health` → `{"status": "ok", "model_loaded": true}` |
| `test_model_info_exposes_features_and_target` | `GET /model-info` → `features` list contains `tenure_months`, plus a non-empty `target` description |
| `test_predict_returns_probability_and_flag` | `POST /predict` → probability in [0,1], `flag` ∈ {0,1}, `threshold == 0.5` |
| `test_predict_is_deterministic` | same request twice → identical body (model loaded **once**, not per call) |
| `test_batch_of_three` | 3 records → 3 predictions, in order |
| `test_missing_field_is_422_and_named` | 422 whose detail names `monthly_charges` |
| `test_out_of_range_is_422` | 422 naming `tenure_months` |
| `test_unknown_contract_is_422` | 422 naming `contract_type` |
| `test_empty_records_is_422` | `{records: []}` → 422 |

## The three design decisions the lab is really testing

1. **Load the model once at import** (`model = joblib.load(...)` at
   module scope or a cached loader). Per-request loading breaks the
   determinism test's spirit and multiplies latency.
2. **Let Pydantic do the validation.** Constrain in the schema
   (`Field(..., ge=0, le=120)`, `Literal["monthly","one_year","two_year"]`)
   so FastAPI returns 422 automatically — then add an exception handler
   only to *shape* the error body so the field name appears in `detail`.
3. **Return `threshold` from config, not `0.5` hardcoded** — the test
   asserts 0.5 because that is your configured operating point; a
   magic number that happens to match is a coincidence, not a design.

## Useful local checks (beyond pytest)

```powershell
python -m uvicorn app:app --port 8000        # then open /docs — Swagger UI works
curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d '{"records":[]}'
# ✅ 422, not 500 — an empty batch is a client error, not a crash
```

## Reference implementation (verify it yourself)

The code below is the reference `app.py`. **Verified:** copied next to
`test_service.py` on the authoring machine (Python 3.14, pytest 9.1.1) it
runs `9 passed`, then it was removed again — the exercise must stay yours
to do:

```python
# app.py — reference solution
import json
import pathlib
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

HERE = pathlib.Path(__file__).resolve().parent
INFO = json.loads((HERE / "model_info.json").read_text(encoding="utf-8"))
FEATURES = INFO["features"]
THRESHOLD = 0.5
MODEL = joblib.load(HERE / "model.joblib")      # loaded ONCE, at import


class Record(BaseModel):
    tenure_months: int = Field(..., ge=0, le=120)
    monthly_charges: float = Field(..., ge=0.0, le=500.0)
    support_calls: int = Field(..., ge=0, le=50)
    contract_type: Literal["monthly", "one_year", "two_year"]


class PredictRequest(BaseModel):
    records: list[Record] = Field(..., min_length=1, max_length=1000)


app = FastAPI(title="churn scoring API")


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": True}


@app.get("/model-info")
def model_info():
    return {"features": FEATURES, "target": INFO["target"],
            "threshold": THRESHOLD, "trained_on": INFO["trained_on"]}


@app.post("/predict")
def predict(request: PredictRequest):
    frame = pd.DataFrame([r.model_dump() for r in request.records])[FEATURES]
    proba = MODEL.predict_proba(frame)[:, 1]
    return {"threshold": THRESHOLD,
            "predictions": [
                {"churn_probability": round(float(p), 4),
                 "flag": int(p >= THRESHOLD)}
                for p in proba]}
```

Why each test passes: the four bounds plus the `Literal` contract make
FastAPI/Pydantic return **422 with the field in `loc`** (the tests read
`detail`); `min_length=1` rejects the empty batch; the module-scope
`MODEL` gives identical responses across calls.

## Common wrong answers

- `except Exception: return 500` around validation — masks bugs and
  fails the named-field tests.
- Round/truncate the probability before comparing — breaks
  determinism silently for borderline values.
- Returning 400 instead of 422 — the contract says 422 (Pydantic's
  code); "close enough" fails both the test and the client's handling.
- Loading `model.joblib` inside the handler — passes by luck today,
  burns latency and file handles at any real traffic.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../../docs/about/index.md).*