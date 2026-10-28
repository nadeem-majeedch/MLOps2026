# LAB-12 — Ship the Image

## 1. Lab identity

| | |
|---|---|
| **Lab ID** | **LAB-12** |
| **Difficulty / topic** | 🔧 Intermediate · Containers & reproducible environments |
| **Prerequisite module** | [11 — Docker images and containers](../modules/11-docker-containers/index.md) · **LAB-10 completed** (you package *your* service) |
| **Fixture** | `examples/labs/lab-12/requirements.txt` (+ your LAB-10 service) |
| **Estimated time** | 105 minutes · ⚠️ requires Docker or another container runtime (free, local) |

## 2. Scenario and background

"It works on my laptop" dies today. The product team wants the service
from LAB-10 shipped as an image: same bytes, any machine, one command.
You will write a Dockerfile that builds a pinned, layer-cached,
health-checked image, run the acceptance suite **inside the container**,
and prove reproducibility by building twice and comparing. If your
machine has no container runtime, the honest **Path B** (review + design
write-up) keeps this lab gradeable — labelled as such.

## 3. Learning objectives

By the end you can:

1. Structure a Dockerfile for cache efficiency (deps before code) with
   pinned dependencies and a non-`:latest` base.
2. Choose what enters the build context (`.dockerignore`) so data,
   secrets, and caches never ship.
3. Run, health-check, and test a container; explain ports, env vars, and
   PID-1 signal handling.
4. Judge build success by *behaviour inside the container*, not by
   `docker build` exit alone.

## 4. Prerequisites and estimated time

- LAB-10 done: `app.py`, `model.joblib`, `test_service.py` exist.
- Module 11 read. **Preflight:**
  ```powershell
  docker --version        # 🪟/🐧 — if missing → Path B
  ```
- **105 min Path A** (design 15 · build 20 · verify 40 · repro 15 ·
  write-up 15) · **60 min Path B**.

## 5. Student task statement

**Path A:** deliver `Dockerfile` + `.dockerignore` in your LAB-10 folder
such that: image builds from `lab-12/requirements.txt` pins; container
serves `/health` 200 from the host; the 10 acceptance tests pass against
the containerised service; a second build succeeds with layers cached;
build context contains no `data/`, no `.git`, no `__pycache__`.
**Path B:** deliver a written review of the reference Dockerfile (design
decisions + what your build would do) plus a rebuild checklist — clearly
labelled *not executed*.

## 6. Required dataset and setup instructions

```powershell
# 🪟 Windows — PowerShell — from examples/labs/lab-10 (your service)
python train_model.py                 # model present before you build
Copy-Item ..\lab-12\requirements.txt . # pins to build with
# your files: app.py, model.joblib, model_info.json, test_service.py
```
Reference design: `examples/churn/Dockerfile` (Module 11's pattern).

## 7. Starter files

| File | Role |
|---|---|
| `../lab-12/requirements.txt` | verified pins (fastapi 0.162.0, scikit-learn 1.9.1, …) |
| `examples/churn/Dockerfile` | the pattern to follow (read it first) |
| `Dockerfile`, `.dockerignore` | **you write them** (reference in solutions) |

## 8. Numbered implementation steps

**Step 1 — Design on paper.** Layers: base → env → workdir → deps →
code → model → expose → healthcheck → cmd. ✅ rationale line per layer.

**Step 2 — Write `.dockerignore`** first: `.venv/`, `__pycache__/`,
`data/`, `*.log`, `.git`, tests' caches — and say why `model.joblib` IS
included (the image must serve it).

**Step 3 — Build.**
```powershell
docker build -t churn-api:lab12 .
docker images churn-api:lab12          # ✅ CREATED, size noted
```

**Step 4 — Run and health-check.**
```powershell
docker run --rm -d --name lab12 -p 8010:8010 -e PORT=8010 churn-api:lab12
curl http://127.0.0.1:8010/health       # ✅ {"status":"ok",...}
docker logs lab12                       # ✅ startup line visible
docker stop lab12
```

**Step 5 — Test inside.** Point the acceptance suite at the running
container (or `docker exec … python -m pytest`) → ✅ **10 passed**.

**Step 6 — Prove cache + reproducibility.** Rebuild → ✅ `Using cache`
for the deps layer. `docker inspect --format='{{.Id}}' churn-api:lab12`
recorded; note that **identical content digests** require the same
buildkit settings — state what you compared honestly.

**Step 7 — Path A only:** write the 5-line "why each flag" note
(`ENV PYTHONUNBUFFERED`, exec-form CMD, healthcheck interval) for your
evidence file.

## 9. Commands and expected results

| Command | Expected |
|---|---|
| `docker build -t churn-api:lab12 .` | `Successfully tagged …` (Path A) |
| rebuild immediately | deps layer `Using cache` |
| `docker run … -p 8010:8010 …` + `curl …/health` | HTTP 200 JSON |
| acceptance tests vs container | **10 passed** |
| `docker stop lab12` | container stops cleanly (signal handling) |
| ⚠️ no Docker | Path B deliverable instead — label `NOT RUN` |

## 10. Acceptance criteria (objective)

- [ ] Dockerfile follows the pattern: pinned base tag, deps-before-code,
      exec-form CMD, healthcheck (Path A) — or the written review
      (Path B, labelled NOT RUN).
- [ ] `.dockerignore` present with justification lines.
- [ ] `/health` 200 **from the host against the container** (transcript).
- [ ] Acceptance suite green against the containerised service (or
      Path B checklist).
- [ ] Second build uses the cached dependency layer.
- [ ] Evidence honestly labels anything not executed.

## 11. Troubleshooting and recovery

| Symptom | Cause | Fix |
|---|---|---|
| `model.joblib: not found` at runtime | not copied, or `.dockerignore` excluded it | COPY it explicitly; check your ignore file |
| connection refused on 8010 | app binds `127.0.0.1` inside container | bind `0.0.0.0` (`HOST` env) and publish `-p` |
| tests pass locally, fail in image | test deps not in requirements | include test deps or run tests from the host against the published port |
| huge image / slow build | context includes data + venv | tighten `.dockerignore`; order layers by change-frequency |
| Windows line-endings break scripts | CRLF in files copied into image | keep `.gitattributes`/editor on LF for build files |
| no Docker | machine lacks the runtime | **Path B** — never claim a build you didn't run |

## 12. Reflection questions

1. Why do dependencies get their own layer — quantify the win for a
   2-minute dependency install and a 2-second code edit loop.
2. `:latest` vs a pinned tag: what breaks a year from now, in each case?
3. The image contains your model — is the model a build artefact or a
   release artefact? Which Module's rules say so?

## 13. Optional challenge tasks

1. Drop the image size ≥20% (multi-stage or slimmer base) with before/
   after numbers.
2. Add a non-root `USER` and prove the service still works.
3. Two consecutive builds with `--no-cache` → compare content digests and
   explain any difference (BuildKit metadata vs content).

## 14. Rubric / checklist

| Points | Criterion |
|---|---|
| 3 | Dockerfile pattern elements present (or Path B review quality) |
| 2 | `.dockerignore` with reasons |
| 4 | container health 200 from host + acceptance tests green inside/against |
| 3 | cached rebuild evidence |
| 2 | honest labelling of anything unexecuted |
| **14** | **total** · ≥11 = pass (Path B graded on review depth) |

## 15. Cleanup

```powershell
docker stop lab12 2>$null; docker rm lab12 2>$null
docker rmi churn-api:lab12
cd examples\labs\lab-12          # nothing generated here by default
```
⚠️ On a machine without Docker: delete nothing — you generated nothing.

---

**After attempting:** a reference Dockerfile + `.dockerignore` for the
LAB-10 service live in
[`examples/labs/solutions/lab-12/`](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/labs/solutions/lab-12)
— **⚠️ not built on the authoring machine (no Docker there); it mirrors
the verified Module 11 Dockerfile.**

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../about/index.md).*