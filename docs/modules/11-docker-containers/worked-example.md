# Worked example — the Dockerfile, examined

**Honesty note first.** The environment this module was authored in has **no
Docker CLI**, so `docker build` / `docker run` were **not executed here**.
What *was* executed is marked ✅ **verified**; the build procedure is marked
🧪 **expected on your machine** with the acceptance signals to look for — it
is a procedure, not a captured log. No output below is invented.

---

## 1. ✅ Verified: the Dockerfile parses, instruction by instruction

Using `dockerfile-parse` (a static parser — no daemon needed):

```text
entries: 32
  line 15: FROM python:3.14-slim
  line 18: ENV PYTHONDONTWRITEBYTECODE=1 \ PYTHONUNBUFFERED=1 \ ...
  line 24: WORKDIR /app
  line 27: COPY requirements-docker.txt .
  line 28: RUN python -m pip install --no-cache-dir -r requirements-docker.txt
  line 31: COPY src/ ./src/
  line 32: COPY service/ ./service/
  line 33: COPY artifacts/ ./artifacts/
  line 34: COPY config.yaml .
  line 37: EXPOSE 8000
  line 41: HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 ...
  line 47: CMD ["python", "-m", "service"]
baseimage: python:3.14-slim
envs: {'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONUNBUFFERED': '1',
       'PIP_NO_CACHE_DIR': '1', 'HOST': '0.0.0.0', 'PORT': '8000'}
```

Checks this satisfies: dependencies copied **before** code (cache order),
`HOST=0.0.0.0` present (container reachability), `CMD` in exec form, base tag
pinned.

## 2. ✅ Verified: every pin resolves from PyPI

```powershell
python -m pip install --dry-run -r requirements-docker.txt
```

```text
... (resolution lines) ...
Requirement already satisfied: six>=1.5 ... (from python-dateutil>=2.8.2->pandas==3.0.6->...)
```

`--dry-run` resolves without installing: all nine pins (`fastapi==0.162.0`,
`uvicorn==0.54.0`, `pydantic==2.13.5`, `scikit-learn==1.9.1`, `pandas==3.0.6`,
`numpy==2.5.3`, `PyYAML==6.0.3`, `joblib==1.6.0`, `starlette==1.10.0`) exist
and are installable.

## 3. ✅ Verified: the HOST/PORT behaviour the Dockerfile relies on

```powershell
HOST=127.0.0.1 PORT=8001 python -m service
```

```text
serving on http://127.0.0.1:8001  (docs: /docs, health: /health)
INFO:     Started server process [8224]
{"status":"ok","model_version":"v001","model_source":"registry_store\\v001\\model.joblib"}
```

The same entrypoint honoured environment overrides — exactly what
`ENV HOST=0.0.0.0` will do inside the container (bind behaviour verified with
a real request in this case, on port 8001).

## 4. ✅ Verified: the tests the image must keep passing

```text
34 passed, 1 warning in 3.85s      (python -m pytest, from examples/churn)
All checks passed!                 (ruff check .)
```

The image packages the same code, so these are the image's acceptance baseline.

---

## 5. 🧪 Expected on your machine: build, run, test

**Prerequisite:** Docker Desktop/Engine running (`docker version` prints a
client **and** server section; if only the client appears, start the daemon).

```powershell
# 🪟 from examples/churn — build (first run downloads the base image: ~2-4 GB)
docker build -t churn-api:1.0 .
```

**Acceptance signals:** build reaches `writing image`; final lines name the
tag `churn-api:1.0`; exit code 0. On a *second* build immediately after, the
pip-install layer should print `CACHED` — proof of the layer ordering in §1.

```powershell
docker run --rm -d --name churn-api -p 8000:8000 churn-api:1.0
Start-Sleep 5
curl -s http://127.0.0.1:8000/health          # 🐧: curl -s localhost:8000/health
docker logs churn-api
```

**Acceptance signals:** the health JSON (Module 10's shape, with
`model_version` — `artefact` unless you mounted a registry); logs show uvicorn's
`Started server process` **immediately** (i.e. `PYTHONUNBUFFERED=1` worked);
`docker ps` shows `Up` and `(healthy)` after ~30 s (HEALTHCHECK passed).

```powershell
# invalid request still 422 from inside the container
curl -s -o $null -w "%{http_code}" -X POST http://127.0.0.1:8000/predict `
  -H "Content-Type: application/json" -d '{"records":[]}'        # expect 422
```

```powershell
docker stop churn-api        # removed by --rm on stop
docker rmi churn-api:1.0     # cleanup
```

**If any signal differs from the description, that is your lab result to
report — not something to fudge.** A clean-build + healthy-run pair is the
complete evidence for LO 11.1/11.3; running the same tag on a second
environment completes LO 11.4.

---

**Next:** [lab.md](lab.md) — the full build/run/test/cleanup procedure.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*