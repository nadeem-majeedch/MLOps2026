# Concepts — Module 10

*Vocabulary: inference, online/batch/streaming serving, REST, endpoint, schema,
validation, status code, health check, latency, throughput, p50/p95, OpenAPI,
Swagger, uvicorn, ASGI.*

---

## 1. Serving: three shapes of the same question

**Inference** = using a trained model to score new data (vs *training*).

| Shape | What happens | Latency budget | Typical use |
|---|---|---|---|
| **Online (synchronous)** | request → prediction → response, within one HTTP call | milliseconds–seconds, user waiting | loan decision, churn flag in a CRM |
| **Batch** | score a file/table in bulk, results delivered later | minutes–hours, nobody waiting | nightly campaign lists |
| **Streaming** | events scored one by one as they arrive, continuously | per-event ms, pipelined | fraud checks per transaction |

**This module builds online serving with batched requests**: one record is a
wasteful round trip; `records: [ ... ]` lets an application score 100 customers
per call. Batch jobs (score a CSV nightly) remain a *script*, not a service —
knowing which shape a problem needs is LO 10.2.

## 2. REST, endpoints, status codes

**REST** here means: HTTP verbs on URLs that name *things*, with status codes
carrying the outcome:

| Code | Meaning | Where we use it |
|---|---|---|
| `200` | success | `/health`, `/model-info`, `/predict` |
| `422` | **your request was invalid** (schema rejected it) | bad types, out-of-range, empty batch |
| `503` | service can't do the job *right now* (no model loaded) | startup before training |
| `404` | unknown route (framework-generated) | typo'd URL |

The distinction between **422 (fix your payload)** and **503 (fix the
service)** is the core of "meaningful errors": one is the caller's problem,
the other is yours — and each needs a different action.

## 3. Schemas: the contract, enforced

A **schema** declares the shape of allowed requests. FastAPI reads pydantic
models (`service/schemas.py`) and enforces them *before* your code runs:

```python
tenure_months: int = Field(..., ge=1, le=120)
contract_type: Literal["monthly", "one_year", "two_year"]
records: list[CustomerRecord] = Field(..., min_length=1, max_length=1000)
```

Consequences:
- Type/range/enum violations **cannot reach the model** (no `try/except` jungle);
- the same schema generates **OpenAPI** (`/openapi.json`) → interactive
  `/docs` → documentation that cannot drift from the code;
- the contract is testable (our 422 tests assert the *message names the field*).

> Validation is the API's Module 04 equivalent: a data contract at the door.

## 4. Error bodies a caller can act on

We override FastAPI's default validation handler to return:

```json
{"error": "invalid request",
 "detail": ["records.0.contract_type: Input should be 'monthly', 'one_year' or 'two_year'"]}
```

Rules behind it: say **which field**, **what was wrong**, **what is allowed**;
never leak stack traces, file paths, or model internals (they help attackers,
not callers). Domain errors (no model) return `error` + a `detail` list of
*remediation steps* — the message is the first line of support.

## 5. Loading the model once

`service/app.py` resolves the model **at import time** (`_state =
resolve_model()`), not per request:

- per-request loading would re-read `model.joblib` (~50–100 ms) for every call;
- the process serves the *same* model throughout its life → predictions for a
  request are consistent (important for auditability);
- deployment **restarts** to change models — that is a feature: promotion
  (Module 09) becomes an explicit, observable event.

Resolution order: registry `production` → training artefact → none. The
"none" case returns **503 with instructions** instead of crashing: an
orchestrator sees a live-but-unready service (and `/health` reports
`degraded`), while a human gets told exactly what to run.

## 6. Health checks

`/health` must be **cheap** (no model work) and **honest** (names the model
version). Consumers: Docker's `HEALTHCHECK` (Module 11), CI smoke tests
(Module 12), schedulers (Module 13), monitoring (Module 14). "Liveness" (the
process answers) vs "readiness" (it can serve) — our single endpoint reports
both via `status: ok | degraded`.

## 7. Documentation as a by-product

`GET /docs` (Swagger UI) and `/redoc` are generated from the schema and
decorator metadata (`description`, `response_model`). Update the model, and
the docs update themselves — the failure mode of hand-written API docs
("the doc says `str`, the API wants `int`") disappears structurally.

## 8. Latency and throughput — measure, don't guess

- **Latency** — time for one request (report p50/max; p95 when you have ≥100 samples).
- **Throughput** — requests per second the service sustains.
- Measurement needs honesty: `curl` timings include your own machine and an
  empty server; N=1 says almost nothing. Our lab measures a small loop, names
  the method, and states the caveat. (Module 16 adds load and concurrency.)

## 9. What we deliberately leave out

| Left out | Belongs to |
|---|---|
| Authentication / authorisation | Module 15 |
| HTTPS, real deployment, scaling | Module 11 (container), Module 16 (platform) |
| Request logging / prediction logs | Module 14 |
| Rate limiting, timeouts under load | Module 16 |

Building the *core* first is the course's rule: one major new concern at a
time.

---

**Next:** [worked-example.md](worked-example.md) — real requests against a
running server.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*