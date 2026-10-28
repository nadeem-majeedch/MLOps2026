# Lab 11 — Same bytes, two places

## 1. Scenario and business problem

The application team wants your API, but their host has a different Python and
three conflicting packages already installed. Every "works here, fails there"
ticket this month started the same way.

**Business problem:** stop shipping *code* and start shipping an *image* — a
single artefact that contains the runtime, the exact dependencies, and the
model, so environment drift cannot be part of the conversation.

## 2. Skills practising

- Reading a Dockerfile as an executable specification.
- Building with cache, verifying the cache actually hit.
- Publishing ports and diagnosing "connection refused" causes.
- Reading container logs and lifecycle states.
- Persisting outputs through a volume — deliberately.

## 3. Prerequisites

- [concepts.md](concepts.md) read (§1–§7).
- Module 10's service running locally (to compare against).
- **Docker installed and running** — ⚠️ this module requires it (free,
  personal use; no account for these steps). Check: `docker version` shows
  both Client and Server.

## 4. Required tools and estimated time

| Item | Detail |
|---|---|
| Tools | Docker Desktop (🪟) / Docker Engine (🐧), curl, PowerShell/bash |
| Cost | Free for personal use; no registry account needed |
| ⚠️ Resource-heavy | ~2–4 GB disk (base image + cache), ~500 MB RAM while running |
| ⏱️ Estimated time | 140 minutes (first build downloads the base image) |

## 5. Input data and how to obtain it

Everything needed is in `examples/churn/`: `Dockerfile`,
`.dockerignore`, `requirements-docker.txt`, `src/`, `service/`, `artifacts/`.
Verify the baseline first:

```powershell
python -m pytest          # ✅ 34 passed — the image must preserve this
docker version            # ✅ Client AND Server sections
```

## 6. Directory layout (what the build context contains)

```
examples/churn/
├── Dockerfile              # the recipe
├── .dockerignore           # keeps data/, .venv/, pipe_out/... OUT of the context
├── requirements-docker.txt # pinned: exactly what tests passed against
├── src/  service/  config.yaml   # copied in
├── artifacts/              # copied in (the model served)
└── data/ pipe_out/ ...     # excluded — mounted or regenerated instead
```

## 7. Setup and execution steps

**Step 1 — Predict the layers.** List the Dockerfile's instructions in order
and mark where the cache boundary falls. Answer before building: *if I edit
`service/app.py`, which layers rebuild?*
✅ **Checkpoint:** your answer = "everything after `COPY service/` only; the
pip layer stays cached."

**Step 2 — Build.**
```powershell
docker build -t churn-api:1.0 .
```
✅ **Checkpoint:** exit 0; image listed by `docker images | findstr churn-api`.

**Step 3 — Prove the cache.** Build again unchanged.
✅ **Checkpoint:** `RUN pip install` prints `CACHED`; total time is seconds.

**Step 4 — Run and reach it.**
```powershell
docker run --rm -d --name churn-api -p 8000:8000 churn-api:1.0
Start-Sleep 5
curl -s http://127.0.0.1:8000/health
docker logs churn-api
```
✅ **Checkpoint:** Module 10's health JSON appears; uvicorn log lines are
visible *without* waiting for exit (unbuffered stdout).

**Step 5 — Deliberately break reachability.** Re-run with the port mapping
removed (`docker run --rm -d --name churn-np churn-api:1.0`) and curl it.
Record the error, remove that container.
✅ **Checkpoint:** you can state precisely which half of `-p HOST:CONTAINER`
was missing and why the app inside was still fine (`docker logs` shows it
serving).

**Step 6 — Same contract, inside the box.** Send the Module 10 invalid payload
(`{"records":[]}`) and confirm **422** — the container behaves like the local
server.

**Step 7 — Persist one thing deliberately.**
```powershell
docker run --rm -d --name churn-vol -p 8000:8001 -e PORT=8001 `
  -v "${PWD}/monitoring:/app/monitoring" churn-api:1.0
```
(Copy `monitoring/` into place first if your build context lacks it; if you
prefer, mount any writable folder.) Stop and remove the container, confirm the
mounted host folder still exists.
✅ **Checkpoint:** evidence that container filesystems die and mounts don't.

**Step 8 — Second environment (LO 11.4).** Either (a) run the same tag on
another machine/profile you have access to, or (b) `docker rmi churn-api:1.0`,
`docker builder prune -af`, rebuild from the same source, and compare
`docker images` metadata + re-run Steps 4–6.
✅ **Checkpoint:** the service behaves identically; record which option you did.

**Step 9 — Cleanup and re-verify.**
```powershell
docker ps -a                 # no churn-* containers
docker rmi churn-api:1.0     # tag gone
python -m pytest             # ✅ still 34 passed on the host
```

## 8. Expected outputs and verification

| Step | Expected | Verify |
|---|---|---|
| 2 | exit 0, image tagged | `docker images` |
| 3 | `CACHED` on the pip layer | build output |
| 4 | health JSON + startup logs | curl + `docker logs` |
| 5 | connection refused from host, app fine inside | curl error vs logs |
| 6 | 422 on empty batch | status code |
| 7 | host folder survives `docker rm` | `ls monitoring/` |
| 8 | identical behaviour, evidence recorded | your transcript |
| 9 | no containers/images left; suite green | commands above |

## 9. Acceptance criteria

- [ ] Build succeeds from a clean checkout; second build uses the cache (proved).
- [ ] `/health` answers **through the published port**; invalid payload → 422.
- [ ] Container logs visible in real time; `docker stop`/`rm` transcript included.
- [ ] Step 5's reachability failure explained in terms of `-p`, not guessed.
- [ ] One mounted volume demonstrated surviving container removal.
- [ ] Step 8 evidence recorded (second machine **or** clean rebuild).
- [ ] Everything filed as `modules/11/`, including any **limitations** you hit
      (e.g. no Docker on a lab machine) — honest gaps earn full credit.

## 10. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `docker: command not found` / no Server section | Docker not installed or daemon not running | Install Docker Desktop/Engine; start it; re-check `docker version` |
| `build failed: failed to read file` | Wrong folder / typo in COPY | Build from `examples/churn`; check `.dockerignore` didn't exclude the path |
| Build re-downloads pip every time | `requirements-docker.txt` changed, or COPY order wrong | Keep deps first; don't touch the pin file casually |
| `connection refused` on localhost | Missing `-p`, or app bound to `127.0.0.1` inside | Compare with `docker ps` PORTS column; our Dockerfile sets `HOST=0.0.0.0` |
| Container starts then exits | Startup exception (missing artefact, bad path) | `docker logs <name>`; remember the (removed) container via `--rm` — rerun without `--rm` to inspect |
| Health shows `degraded` | `artifacts/` excluded from context | Check `.dockerignore` keeps `artifacts/` (it must) |
| Permission denied writing mounted folder | Windows bind-mount ACLs | Mount a folder you own; avoid OneDrive-synced paths |
| `docker build` extremely slow on Windows | Large context being sent | Re-check `.dockerignore` (`du -sh .` vs context size in build output) |

More: [troubleshooting.md](troubleshooting.md).

## 11. Cleanup

```powershell
docker ps -a | findstr churn-api        # containers
docker rm -f churn-api churn-np churn-vol -ErrorAction SilentlyContinue
docker rmi churn-api:1.0
docker builder prune -af                # 🐧/🪟 reclaim cache (optional, ~GB)
python -m pytest                        # ✅ host still green
```

Keep `requirements-docker.txt` and `Dockerfile` — they are deliverables.

## 12. Optional extension tasks

1. **Multi-stage build:** move `pip install` into a builder stage and keep the
   runtime stage slim; compare `docker images` sizes before/after.
2. **Non-root user:** add `USER app` and verify the service still serves
   (`docker exec … whoami`).
3. **Compose:** write a `compose.yaml` that runs the API with a named volume
   and one environment override, then `docker compose up`/`down`.

---

**Next:** [independent-challenge.md](independent-challenge.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*