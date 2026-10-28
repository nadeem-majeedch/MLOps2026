# References — Module 11

## Tool documentation

| Resource | Use it for |
|---|---|
| [Dockerfile reference](https://docs.docker.com/reference/dockerfile/) | Every instruction: `FROM`, `ENV`, `COPY`, `HEALTHCHECK`, exec vs shell form |
| [Build cache](https://docs.docker.com/build/cache/) | How layers are cached and how to order instructions |
| [`.dockerignore`](https://docs.docker.com/build/building/context/#dockerignore-files) | Keeping secrets/data/noise out of the build context |
| [Container networking / port publishing](https://docs.docker.com/engine/network/) | What `-p` actually forwards; `EXPOSE` semantics |
| [Volumes](https://docs.docker.com/engine/storage/volumes/) | Persisting data beyond container lifetime |
| [docker CLI reference](https://docs.docker.com/reference/cli/docker/) | `build`, `run`, `logs`, `inspect`, `stop`, `rmi` |
| [dockerfile-parse (PyPI)](https://pypi.org/project/dockerfile-parse/) | Static Dockerfile parsing — used for the ✅ verification in this module |

## Best-practice / security reading

- **Docker best practices for image building** (Docker docs, *Build effectively*)
  — dependency layer ordering, cache discipline, multi-stage builds.
- **OWASP Docker Security Cheat Sheet** — never bake secrets into layers, run
  non-root, minimise the surface (foreshadows Module 15).
- **NIST SP 800-190, *Application Container Security Guide*** — the standard
  reference for what containers do and do not isolate.

## Distinguishing tool-specific from general

| Claim | Kind |
|---|---|
| "Package the environment with the code" | **General principle** (also Conda packs, Nix, VM images) |
| "Never bake secrets or mutable data into an image" | **General principle** |
| "Cache dependencies before copying code" | **General principle** for layered builds; layer semantics are Docker-specific |
| "`-p HOST:CONTAINER`", `HEALTHCHECK` | **Docker-specific syntax** |
| "`python:3.14-slim` tag availability" | **Registry-specific** — check Docker Hub before relying on a tag |

## Related course material

- Module 10 — the service packaged here (`HOST`/`PORT` design).
- Module 12 — building this image in CI (the merge gate).
- Module 16 — the same image scaled on a platform.
- [Tool selection guide](../../syllabus/tool-selection-guide.md) — containers
  vs environments (conda/venv) in the wider course.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*