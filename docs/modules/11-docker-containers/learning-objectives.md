# Learning objectives — Module 11

Maps to syllabus outcomes
[LO 11.1–11.4](../../syllabus/detailed-syllabus.md#module-11-docker-images-containers-and-deployment-environments).

| # | You can… | You prove it by… |
|---|---|---|
| **11.1** | Write a Dockerfile that packages the Module 10 API with its exact dependencies | Your build succeeding from a clean checkout, with `requirements-docker.txt` pins, and `/health` answering from the container |
| **11.2** | Explain images, containers, layers, tags, and digests — and why "it works on my machine" ends | A 150-word explanation naming what the image freezes (OS userland + Python + pins + code) and what it does *not* (kernel, hardware, host network) |
| **11.3** | Build, run, stop, and inspect containers; read logs; persist data deliberately | A transcript: `build` → `run -p` → `docker logs` → `docker stop` → `docker rm`, plus one `-v` mount that survives container removal |
| **11.4** | Reproduce the service in a second environment from the image alone | The same tag answering `/health` on another machine/profile (or, if you only have one machine: a clean rebuild after `docker rmi` + cache purge, hashes compared) |

## Supporting skills

- Order Dockerfile instructions so the **dependency layer caches** (change
  code, rebuild: pip install is not repeated).
- Explain why the service binds `0.0.0.0` *inside* the container while your
  laptop still uses `127.0.0.1`.
- State what `.dockerignore` protects against, with two concrete examples.
- Say honestly what this module did **not** verify in your own environment if
  you hit a limitation — and how you would verify it elsewhere.

## Self-check questions

1. Difference between an image and a container, in one sentence each.
2. Why does `COPY requirements-docker.txt` come before `COPY src/`?
3. What does `-p 8000:8000` mean, left and right of the colon?
4. Which file stops `data/` and `.venv/` from entering the build context?

*(Answers in [knowledge-check.md](knowledge-check.md) — attempt first.)*

---

[← Module 11 index](index.md) · [Next: concepts →](concepts.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*