# Troubleshooting — Module 11

Symptom → likely cause → fix. See the
[course troubleshooting hub](../../troubleshooting/index.md) for Python issues.

---

## 1. The daemon is not there

| Symptom | Likely cause | Fix |
|---|---|---|
| `docker: command not found` | Docker not installed | Install Docker Desktop (🪟) / Docker Engine (🐧), then reopen the terminal |
| `error during connect ... named pipe` / `Cannot connect to the Docker daemon` | Desktop not running | Start Docker Desktop; wait for the whale icon / `docker version` shows a Server section |
| `permission denied` (Linux) | Your user not in the `docker` group | Use the distro's documented group add, or run where you legitimately can — do not paste random sudo lines from forums |

## 2. Build problems

| Symptom | Likely cause | Fix |
|---|---|---|
| `failed to compute cache key: ... not found` | A `COPY` source is misspelled **or excluded by `.dockerignore`** | Check spelling; then check `.dockerignore` — exclusions apply to COPY too |
| pip layer rebuilds every time | The requirements file changed, or its COPY shares a layer with code COPY | Keep `COPY requirements-docker.txt` + `RUN pip install` together, before code |
| Build sends gigabytes / very slow | Large context (data, `.venv`, `pipe_out`) not excluded | Review `.dockerignore`; watch "sending build context" size in the output |
| `no matching manifest for windows/amd64` | Rare base-image tag gap | Use the documented tag, or build with `--platform linux/amd64` and understand the emulation cost |
| Out of disk mid-build | Build cache grew | `docker builder prune -af` (frees cache; next build is slower) |

## 3. Run / reachability

| Symptom | Likely cause | Fix |
|---|---|---|
| Host `connection refused` | No `-p` mapping | Add `-p 8000:8000`; confirm in `docker ps` PORTS column |
| Host `connection refused` *with* `-p` | App bound to `127.0.0.1` inside the container | Our Dockerfile sets `ENV HOST=0.0.0.0`; if you overrode it, fix the env |
| `health` returns `degraded` + `/predict` 503 | `artifacts/` missing from the image | `.dockerignore` must NOT exclude `artifacts/`; rebuild |
| Container exits immediately | Startup exception | Run without `--rm` and `docker logs <name>`; the traceback is your answer |
| Health stays `(starting)` then `(unhealthy)` | Model slow to load, or probe URL/port wrong | Check `docker inspect --format '{{json .State.Health}}'`; align HEALTHCHECK port with `PORT` |
| Port already allocated | Another container holds host 8001/8000 | Pick another host port: `-p 8001:8000` |

## 4. Logs and signals

- **Empty `docker logs` while the app works:** stdout buffering —
  `PYTHONUNBUFFERED=1` is set in our Dockerfile; if you removed it, put it back.
- **`docker stop` hangs ~10 s:** the app isn't handling SIGTERM (shell-form CMD
  swallowing it). Use the exec-form `CMD ["python", "-m", "service"]`.
- **Timestamps/cwd confusion:** logs come from the container's view
  (`/app`), not your host folder — that's the point.

## 5. Volumes

| Symptom | Likely cause | Fix |
|---|---|---|
| Writes vanish after `docker rm` | You wrote to the container filesystem, not the mount | Only paths under the `-v` source survive; check the mount target path |
| `Mounts denied` / permission errors (🪟) | Windows path/ACL not shared with Docker | Use a plain local path (avoid OneDrive-synced folders); Docker Desktop file sharing settings |
| Host folder appears empty | You mounted a different host path than you think | Echo the full `-v` value; relative paths resolve oddly from PowerShell |

## 6. Conceptual traps worth re-reading

- Deleting a *container* is normal hygiene; deleting an *image* removes your
  build — know which `rm` you are typing.
- `docker cp` and mounts are for debugging, not architecture: if data must
  persist, design the mount, don't patch it in during an incident.
- An image containing a model does not make the model *current* — promotion
  (Module 09) still decides what is latest; rebuilding is how a new model
  reaches the image.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*