# Module 10 — Model serving and REST APIs using FastAPI

!!! success "Module complete"
    Lessons, worked example, lab, independent challenge, knowledge check (with
    answers), troubleshooting, and references are all written.

**Stage:** Intermediate · **Estimated effort:** 9 h · **Depends on:** 09 · **Next:** 11

---

## What this module is about

A model nobody can call is a file on a disk. This module turns the registry's
production version into a **live HTTP API** that an application team can use:

| Endpoint | Answers |
|---|---|
| `GET /health` | "Is it up, and which model is serving?" |
| `GET /model-info` | "Exactly what is serving — version, metrics, features, threshold" |
| `POST /predict` | "Score these customers" (batched, schema-validated) |
| `GET /docs` | Interactive documentation generated from the schema itself |

The service ships **tested**: 8 API tests (schema, errors, determinism) run in
the same suite as everything else, and you will exercise a *real* server with
curl — health, a valid batch, and a deliberately invalid request whose 422 you
read carefully.

## How to study this module (in order)

| # | File | What it does | Time |
|---|---|---|---|
| 1 | [learning-objectives.md](learning-objectives.md) | What you must be able to do, and how you prove it | 10 min |
| 2 | [concepts.md](concepts.md) | Batch vs online vs streaming, schemas, errors, latency, docs | 120 min |
| 3 | [worked-example.md](worked-example.md) | Real requests and responses, incl. a real 422 | 45 min |
| 4 | [lab.md](lab.md) | **Guided lab:** serve a trained model to an application | 140 min |
| 5 | [independent-challenge.md](independent-challenge.md) | Add a versioned endpoint and measure latency honestly | 75 min |
| 6 | [knowledge-check.md](knowledge-check.md) | 10 questions with reasoning | 30 min |
| 7 | [troubleshooting.md](troubleshooting.md) | Port conflicts, 422s, 503s, slow predictions | as needed |
| 8 | [references.md](references.md) | FastAPI, pydantic, uvicorn, HTTP/latency sources | optional |

## Before you start

- Module 09: a registered, promoted production version (or the training
  artefact as fallback).
- `fastapi`, `uvicorn`, `httpx` available (`python -m pytest tests/test_service.py`).
- Free, local, no accounts — uvicorn runs on your laptop; nothing is deployed.

## Evidence you should produce

1. A live-server transcript: `/health`, a valid `POST /predict`, and an
   **invalid** request with its 422 body.
2. The 8-test API suite output, green, with the coverage report.
3. A latency measurement you took yourself (number of requests, timing method,
   p50/max) — no invented numbers.

---

[← Module 09: Model artifacts and registries](../09-model-artifacts-registry/index.md) · [Full syllabus](../../syllabus/detailed-syllabus.md#module-10-model-serving-and-rest-apis-using-fastapi) · [Module 11 →](../11-docker-containers/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*