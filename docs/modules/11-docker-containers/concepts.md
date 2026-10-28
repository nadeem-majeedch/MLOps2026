# Concepts — Module 11

*Vocabulary: container, image, layer, Dockerfile, build context, registry, tag,
digest, port mapping, environment variable, volume, bind mount, HEALTHCHECK,
image size, base image.*

---

## 1. The problem a container solves

Your service runs because of a pile of invisible conditions: Python 3.14, the
exact `scikit-learn==1.9.1` wheel, a model file in a known path, an env var, a
free port. Move the code without those conditions and it breaks — that is
**"it works on my machine"**: not a mystery, but *unrecorded environment state*.

> **Image** — a frozen, layered filesystem containing the OS userland, a
> runtime, dependencies, and your code, described by a **Dockerfile**.
> **Container** — a running instance of an image (like a process, but with its
> own filesystem view and network namespace).

The image is the *recipe + baked ingredients*; a container is *one cooked meal*.
Many containers from one image; each gets its own ephemeral filesystem.

## 2. The Dockerfile we ship, clause by clause

```dockerfile
FROM python:3.14-slim                      # base: OS userland + Python, pinned tag
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 \
    HOST=0.0.0.0 PORT=8000
WORKDIR /app
COPY requirements-docker.txt .             # dependencies FIRST (cache!)
RUN python -m pip install --no-cache-dir -r requirements-docker.txt
COPY src/ ./src/                           # code AFTER deps
COPY service/ ./service/
COPY artifacts/ ./artifacts/
COPY config.yaml .
EXPOSE 8000                                # documentation, not a firewall rule
HEALTHCHECK --interval=30s ...             # container self-probe
CMD ["python", "-m", "service"]            # exec form: PID 1, gets signals
```

- **Pinned base tag** (`python:3.14-slim`), never `:latest` — `:latest` moves
  under you, which is the disease this module cures. (A **digest**
  `python@sha256:…` is even stricter; tags are enough for the course.)
- **Pinned requirements** — `requirements-docker.txt` copies the exact
  versions your tests passed against.
- **`HOST=0.0.0.0`** — inside the container, `127.0.0.1` means *the container
  itself*; the host reaches it only if the process listens on all container
  interfaces. Your laptop's local run keeps `127.0.0.1` because of Module 10's
  env-var design — **same code, different environment, no forks**.
- **exec-form `CMD`** — `["python", "-m", "service"]` means python is PID 1
  and `docker stop` reaches it; the shell form would put a shell in between
  and strand the signal.

## 3. Layers and caching

Every instruction creates a **layer** (a diff on the filesystem). Docker caches
them: if `requirements-docker.txt` is unchanged, `RUN pip install` is *reused*;
if it changes, that layer and every later one rebuild. Hence the rule
**copy dependencies before code** — editing `app.py` must never re-download
scikit-learn.

## 4. Build context and `.dockerignore`

`docker build .` sends the `.` folder (the **build context**) to the daemon.
Our `.dockerignore` excludes `.venv/`, `data/`, `pipe_out/`, `registry_store/`,
`*.ipynb`, logs — otherwise every build ships gigabytes and may leak things
that should never be baked in (generated data, local state). Note
`artifacts/` is deliberately **kept**: the image serves that model.

> Secrets never enter an image. Not in the Dockerfile, not in the context, not
> in a layer (layers are inspectable). Module 15 returns to this.

## 5. Ports: `-p 8000:8000`

`-p HOST:CONTAINER` forwards a host port to a container port. `EXPOSE` is
documentation; `-p` is the actual mapping (no `-p` = unreachable from outside).
So: container listens on `0.0.0.0:8000`, host forwards `localhost:8000` →
container `8000`. Two failure modes to know: forgetting `-p` (connection
refused from the host) and binding the app to `127.0.0.1` inside (mapping
exists but nothing listens "outside" — connection refused anyway).

## 6. Logs, lifecycle, exit codes

```powershell
docker logs -f <container>      # stdout/stderr — why PYTHONUNBUFFERED=1 matters
docker stop <container>         # SIGTERM, then SIGKILL after grace period
docker rm <container>           # the container (ephemeral) is disposable
```

`PYTHONUNBUFFERED=1` means `print` reaches `docker logs` immediately; without
it, Python's block-buffered stdout hides output until exit — a classic
"my logs don't work" hour. **Exit codes** carry status: `docker run …; $LASTEXITCODE`
gives you the app's code (our pipeline's 0/1 discipline survives the box).

## 7. Volumes: persist *deliberately*

A container's filesystem dies with it. Anything you need later must be
**mounted**: `-v ${PWD}/monitoring:/app/monitoring` (a **bind mount** to a host
folder) or a named volume for managed storage. Rule: *code and model are baked
in; results and data are mounted out.* That split is what makes containers
disposable.

## 8. Reproducibility: what the image freezes — and does not

| Frozen in the image | NOT frozen |
|---|---|
| OS userland + Python version | Host kernel & drivers |
| Every pip package (pinned) | CPU architecture (x86 vs ARM images differ) |
| Application code + artefacts present at build | Files mounted via volumes |
| Env defaults (`ENV`) | Env passed at `run -e`, ports mapped at `-p` |

Two people building from the same commit get **functionally identical** images
(timestamps aside); identical *hashes* require a digest-pinned base and
reproducible build settings — say so honestly rather than overclaiming.

## 9. Where this sits in the course

Module 12 builds the image in CI (build = a test that the Dockerfile still
works). Module 13 runs scheduled jobs (possibly in containers). Module 16 puts
the same image behind a platform (Kubernetes) where **scaling is "more
containers of the same image"** — which only works because this module made
the image the unit of deployment.

---

**Next:** [worked-example.md](worked-example.md) — the parsed Dockerfile and
the verifications that *were* executed.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*