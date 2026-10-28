# Module 11 — Docker images, containers, and deployment environments

!!! success "Module complete"
    Lessons, worked example, lab, independent challenge, knowledge check (with
    answers), troubleshooting, and references are all written.

**Stage:** Intermediate · **Estimated effort:** 9 h · **Depends on:** 10 · **Next:** 12

---

## What this module is about

"It works on my machine" ends the day someone else's machine disagrees. This
module packages the Module 10 API — code, interpreter, exact dependency
versions, and model artefact — into one **image** that runs identically on any
machine with Docker:

| You learn | By doing |
|---|---|
| Images vs containers | Reading a Dockerfile layer by layer, then running it |
| Build context & caching | Ordering `COPY` so dependency layers stay cached |
| Ports & environment | `HOST=0.0.0.0`, `-p 8000:8000`, why 127.0.0.1 fails in a container |
| Logs & lifecycle | `docker logs`, `docker stop`, exit codes |
| Volumes | Persisting results *deliberately*, not by accident |
| Reproducible environments | Pinned base tag + pinned requirements = rebuildable bytes |

**Verification honesty for this module:** the Dockerfile and pinned
requirements in the repo were **statically verified where the authoring
environment allows** (structure parsed, every pin confirmed to resolve from
PyPI, service bind behaviour tested) — the actual `docker build` must run on
**your** machine, because Docker is not available in every environment. The
lab says exactly which command produces which proof.

## How to study this module (in order)

| # | File | What it does | Time |
|---|---|---|---|
| 1 | [learning-objectives.md](learning-objectives.md) | What you must be able to do, and how you prove it | 10 min |
| 2 | [concepts.md](concepts.md) | Images, layers, contexts, ports, env, volumes, reproducibility | 120 min |
| 3 | [worked-example.md](worked-example.md) | The real Dockerfile, its parsed structure, verified pins | 45 min |
| 4 | [lab.md](lab.md) | **Guided lab:** package the service, build, run, test, clean up | 140 min |
| 5 | [independent-challenge.md](independent-challenge.md) | Shrink the image, persist a volume, and defend the result | 75 min |
| 6 | [knowledge-check.md](knowledge-check.md) | 10 questions with reasoning | 30 min |
| 7 | [troubleshooting.md](troubleshooting.md) | Build failures, unreachable ports, slow containers | as needed |
| 8 | [references.md](references.md) | Docker docs, best-practice guides, image security sources | optional |

## Before you start

- Module 10: the API runs locally and its tests pass.
- **Docker Desktop (Windows) or Docker Engine (Linux) installed and running**
  — this is the one module where a machine-level install is required
  (free for personal use; no account needed for the steps we use).
- ⚠️ ~2–4 GB disk for the base image and build cache.

## Evidence you should produce

1. Your `docker build` transcript ending in a tag, plus `docker run` +
   `/health` from **inside** the container.
2. The same API answering on the host through the published port.
3. `docker images`/`docker ps` output and a cleanup transcript (`docker rmi`).

---

[← Module 10: Model serving with FastAPI](../10-model-serving-fastapi/index.md) · [Full syllabus](../../syllabus/detailed-syllabus.md#module-11-docker-images-containers-and-deployment-environments) · [Module 12 →](../12-cicd-github-actions/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*