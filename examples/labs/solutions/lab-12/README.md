# LAB-12 — reference solution

> Attempt the lab first. This is the answer key, not the assignment.

**Files in this folder:** `Dockerfile` + `.dockerignore` — the reference
build for packaging your LAB-10 service. Copy them next to `app.py`,
`model.joblib`, `model_info.json` and `examples/labs/lab-12/requirements.txt`
before building.

## Honesty first: two paths

- **Path A (container runtime present):** build, run, test, cache.
- **Path B (no Docker):** written review of the reference Dockerfile
  (`examples/churn/Dockerfile`) + design rationale — every command
  labelled **NOT RUN**.

**The authoring machine for this course had no Docker installed**
(`docker: command not found`), so no build transcript from it exists.
Never paste someone else's build log as your own.

## Path A — reference transcript shape

```text
$ docker build -t churn-api:lab12 .
… deps layer … Successfully tagged churn-api:lab12:latest
$ docker build -t churn-api:lab12 .        # again, immediately
… → uses cache for the dependency layer  ✅
$ docker run --rm -d --name lab12 -p 8010:8010 -e PORT=8010 churn-api:lab12
$ curl http://127.0.0.1:8010/health
{"status":"ok", …}                          ✅ from the HOST, against the container
$ docker logs lab12
serving on http://0.0.0.0:8010 …            ✅ (HOST=0.0.0.0 is what makes -p work)
$ docker stop lab12                         ✅ stops cleanly (exec-form CMD ⇒ PID 1 gets SIGTERM)
```

## Path B — the review checklist (reference answers)

| Layer | Why it is there |
|---|---|
| `FROM python:3.14-slim` | pinned tag (never `:latest`); slim = smaller attack surface |
| `ENV PYTHONDONTWRITEBYTECODE/ PYTHONUNBUFFERED=1` | no stale `.pyc`; logs appear immediately in `docker logs` |
| `ENV HOST=0.0.0.0` | inside the container the app must listen on all interfaces for `-p` to reach it |
| deps copied **before** code | the expensive layer is cached; editing app code doesn't re-download packages |
| `.dockerignore` | keeps `.venv/`, caches, logs, `data/`, `.git` out of the **build context** (context size + no secret leakage) |
| `model.joblib` **included** | the image must serve it — the one thing you deliberately do *not* ignore |
| `HEALTHCHECK` | the platform can restart a dead API instead of serving silence |
| exec-form `CMD ["python","-m","service"]` | signal handling: Ctrl+C/`docker stop` reaches Python |

## Reproducibility claim — state it honestly

`docker inspect --format='{{.Id}}' churn-api:lab12` gives the image ID
for *your* build. Identical IDs across machines require identical base
image digest, dependency resolution **and** buildkit settings — say
exactly what you compared ("same Dockerfile, same pins, same platform;
IDs match on my two runs") rather than "fully reproducible".

## Common wrong answers

- Claiming Path A results without a runtime — the course's grading rule
  is evidence-before-claim.
- Forgetting `-e PORT`/publishing the wrong port: `/health` on 8010
  while the app listens on 8000.
- `docker run -it` foreground without `--rm -d`, then "the container
  vanished" after stop — read `docker ps -a`.
- Putting `.env` or credentials into the context "just for the test".

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../../docs/about/index.md).*