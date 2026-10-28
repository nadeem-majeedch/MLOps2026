# syntax=docker/dockerfile:1
# =====================================================================
# LAB-12 reference image — packages the LAB-10 prediction service.
#
# Copy this file and .dockerignore NEXT TO your app.py, model.joblib,
# model_info.json and requirements.txt (use examples/labs/lab-12/
# requirements.txt — exact pins, verified on Python 3.14), then:
#
#   docker build -t churn-api:lab12 .
#   docker run --rm -d --name lab12 -p 8010:8010 -e PORT=8010 churn-api:lab12
#   curl http://127.0.0.1:8010/health
#   docker stop lab12
#
# Design notes (docs/labs/lab-12 + module 11 concepts):
#   * base image pinned by tag, never :latest
#   * dependencies installed BEFORE application code (layer caching)
#   * HOST=0.0.0.0 so -p can reach the app from outside the container
#   * exec-form shell keeps `docker stop` delivering SIGTERM to Python
#   * HEALTHCHECK lets a platform restart a dead API instead of
#     serving silence
# NOTE (honesty): this file was reviewed on the authoring machine, which
# had no container runtime — build it yourself and paste YOUR output.
# =====================================================================

FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HOST=0.0.0.0 \
    PORT=8010

WORKDIR /app

# --- layer 1: dependencies (rarely change -> cached) -------------------
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# --- layer 2: application + model (changes more often) -----------------
COPY app.py model.joblib model_info.json ./

EXPOSE 8010

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request,sys; \
r=urllib.request.urlopen('http://127.0.0.1:8010/health', timeout=2); \
sys.exit(0 if r.status==200 else 1)"

# PORT is honoured via the shell so `docker run -e PORT=...` really works;
# `exec` keeps python as PID 1 so Ctrl+C / docker stop reach it.
CMD ["sh", "-c", "exec python -m uvicorn app:app --host 0.0.0.0 --port ${PORT:-8010}"]
