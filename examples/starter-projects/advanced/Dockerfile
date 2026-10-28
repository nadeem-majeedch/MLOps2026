# syntax=docker/dockerfile:1
# =====================================================================
# ADVANCED starter — containerised prediction API.
#
#   docker build -t churn-api:starter .
#   docker run --rm -p 8000:8000 churn-api:starter
#
# NOTE: not built on the course's authoring machine (no container
# runtime there) — build it yourself and paste YOUR output. The file
# follows the same pattern as examples/churn/Dockerfile, which the
# Docker module (11) explains layer by layer.
# =====================================================================

FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HOST=0.0.0.0 \
    PORT=8000

WORKDIR /app

# dependencies before code: this expensive layer stays cached
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# application + model artefact (the one binary the image must contain)
COPY service/ ./service/
COPY artifacts/ ./artifacts/
COPY registry.py monitor.py train.py config.yaml ./

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request,sys; \
r=urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2); \
sys.exit(0 if r.status==200 else 1)"

CMD ["sh", "-c", "exec python -m service"]
