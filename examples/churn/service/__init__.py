"""Prediction service (Module 10): a minimal FastAPI app that serves the
churn model from the local registry (or the training artefact as fallback).

    python -m service              # serve on http://127.0.0.1:8000
    python -m pytest tests/test_service.py

Interactive docs: http://127.0.0.1:8000/docs (Swagger) and /redoc.
"""