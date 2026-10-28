# syntax=docker/dockerfile:1
# =====================================================================
# Churn prediction API — Module 11 of the MLOps course.
#
#   docker build -t churn-api:1.0 .
#   docker run --rm -p 8000:8000 churn-api:1.0
#
# Design notes (explained in docs/modules/11-docker-containers/concepts.md):
#   * base image pinned by digest-able tag, not :latest
#   * dependencies copied+installed BEFORE application code (layer caching)
#   * only what serving needs is copied (see .dockerignore)
#   * HOST=0.0.0.0 so the port is reachable from outside the container
# =====================================================================

FROM python:3.14-slim

# Deterministic, readable container logs:
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HOST=0.0.0.0 \
    PORT=8000

WORKDIR /app

# --- layer 1: dependencies (rarely change -> cached) -------------------
COPY requirements-docker.txt .
RUN python -m pip install --no-cache-dir -r requirements-docker.txt

# --- layer 2: application code (changes often) -------------------------
COPY src/ ./src/
COPY service/ ./service/
COPY artifacts/ ./artifacts/
COPY config.yaml .

# --- runtime -----------------------------------------------------------
EXPOSE 8000

# A container with no healthy API should be restarted by the platform,
# not left silently broken.
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request,sys; \
r=urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2); \
sys.exit(0 if r.status==200 else 1)"

# exec form: python is PID 1 and receives signals (Ctrl+C stops the container)
CMD ["python", "-m", "service"]