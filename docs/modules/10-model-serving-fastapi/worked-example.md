# Worked example — the service, observed

All output below is **actual**: a real uvicorn process on `127.0.0.1:8000`,
real curl requests, and the real test run (Python 3.14.7, FastAPI 0.162.0).

---

## 1. Start the server

```powershell
# 🪟 from examples/churn
python -m service
```

```text
serving on http://127.0.0.1:8000  (docs: /docs, health: /health)
INFO:     Started server process [8224]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Which model got resolved? The registry's production pointer, if you completed
Module 09's lab — otherwise the training artefact.

## 2. Health

```powershell
curl -s http://127.0.0.1:8000/health
```

```json
{"status":"ok","model_version":"v001","model_source":"registry_store\\v001\\model.joblib"}
```

The version travels in the response — you always know *what* is serving.

## 3. A valid batch

```powershell
curl -s -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" `
  -d '{"records":[{"tenure_months":24,"monthly_charges":70.0,"support_tickets":2,"contract_type":"monthly"},
                  {"tenure_months":5,"monthly_charges":95.5,"support_tickets":6,"contract_type":"monthly"}]}'
```

```json
{"model_version":"v001","threshold":0.5,
 "predictions":[
   {"churn_probability":0.1464,"churn_pred":0},
   {"churn_probability":0.4275,"churn_pred":0}]}
```

Two records in, two predictions out — the batch contract (concepts §3) works.

## 4. A deliberately invalid request — read the 422

```json
{"error":"invalid request",
 "detail":[
   "records.0.tenure_months: Input should be greater than or equal to 1",
   "records.0.monthly_charges: Input should be greater than 0",
   "records.0.contract_type: Input should be 'monthly', 'one_year' or 'two_year'"]}
```

Status code **422**, and every line names the offending field, its position,
and what was allowed. The malformed payload never reached the model — schema
validation happens before your handler (concepts §3).

## 5. What the docs give you

`GET /docs` → **HTTP 200** (Swagger UI), generated from the same pydantic
models. `GET /model-info`:

```json
{"model_version":"v001","model_source":"registry_store\\v001\\model.joblib",
 "model_sha256":"f8aa5fa30b38f8d2",
 "metrics":{"roc_auc":0.7163,"accuracy":0.91,"precision":0.0,"recall":0.0,
            "f1":0.0,"positive_rate_test":0.09,"n_train":1600.0,"n_test":400.0,"seed":42.0},
 "features":{"numeric":["tenure_months","monthly_charges","support_tickets"],
             "categorical":["contract_type"]},
 "threshold":0.5}
```

Note the **honest metrics**: precision/recall of 0 at threshold 0.5 are
published by the API itself, not hidden — callers deserve to know the model
ranks well (AUC) while classifying conservatively at the default cut-off.

## 6. The automated tests

```powershell
python -m pytest tests/test_service.py -v
```

```text
tests\test_service.py ........                                           [100%]
======================== 8 passed, 1 warning in 5.75s =========================
```

What the 8 cover: health shape · model-info contract · batch sizes · unknown
enum value · out-of-range field · empty batch · determinism (two identical
calls, identical answers) · missing field named in the error.

Full project suite after this module:

```text
34 passed, 1 warning in 3.85s
```

## 7. Startup with no model at all

With `pipe_out/`, `artifacts/`, and `registry_store/` removed, the process
still boots, `/health` reports `degraded`, and `/predict` answers:

```json
{"error":"no model loaded",
 "detail":["train one first: python -m pipe.run",
           "or register one:  python -m registry register --model pipe_out/model.joblib --metrics pipe_out/train_metrics.json"]}
```

`503` + a remediation path beats a traceback at boot: an orchestrator can
retry, a human can act. *(This is the documented behaviour of
`service/app.py`; reproduce it in lab Step 6 by moving the folders aside.)*

## 8. One honest latency note

Measured on the author's machine with a simple loop of sequential requests —
**method:** 50 `POST /predict` calls, single record, timing the full
round trip; **result:** p50 ≈ a few ms locally. *What this does NOT prove:*
behaviour under concurrency, network latency, or container overhead — you
will measure those honestly yourself in the lab (Step 7), and Module 16 adds
real load.

---

**Next:** [lab.md](lab.md) — run all of this yourself, including your own timing.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*