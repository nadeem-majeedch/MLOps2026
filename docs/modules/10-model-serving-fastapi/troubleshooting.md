# Troubleshooting — Module 10

Symptom → likely cause → fix. See the
[course troubleshooting hub](../../troubleshooting/index.md) for environment issues.

---

## 1. Starting the server

| Symptom | Likely cause | Fix |
|---|---|---|
| `Address already in use` (OSError 10048/98) | An older `python -m service` still alive | 🪟 `Get-NetTCPConnection -LocalPort 8000` then `Stop-Process -Id <pid>` · 🐧 `lsof -i :8000` then `kill <pid>` — or start elsewhere: `PORT=8001 python -m service` |
| `ModuleNotFoundError: service` | Wrong working directory | Run from `examples/churn` |
| Server starts then immediately exits | An exception during import/startup | Read the traceback — often a missing `artifacts/` or a bad path in `service/model.py` |
| `PermissionError` binding the port | Port reserved by another app | Use `PORT=8001` (document it in your caller's guide) |
| Windows Firewall prompt | First inbound bind on a public profile | You bind `127.0.0.1` only — cancel is safe for this lab |

## 2. Requests and status codes

| Symptom | Likely cause | Fix |
|---|---|---|
| **422** on a "valid" request | `"70"` (string) vs `70`; missing field; wrong key name | Read `detail[]` — it names the exact field and the rule |
| **422** with `Input should be 'monthly', ...` | Enum mismatch (case-sensitive, no extras) | Copy allowed values from `/model-info` or `schemas.py` |
| **404** on `/predict` | Trailing-slash or path typo | Use exactly `/predict` (FastAPI does not auto-redirect `/predict/` by default) |
| **503** `no model loaded` | Registry empty and no artefact | `python -m pipe.run`, promote a version (Module 09), restart the service |
| **500** (the one that must not happen) | A path validation missed: bad numeric type reaching pandas, model returning unexpected shape | Reproduce with the same payload, read the server traceback, then fix *and add a test* (Module 07's rule) |
| Predictions differ between calls | Different input, or a different model_version after restart | Compare `model_version` in the responses first |

## 3. Model resolution surprises

- **`/health` says `artefact` but you promoted `v002`.** The service resolves
  the pointer at **startup** — restart it. (Promotion affects the *next*
  process start; that is deliberate, concepts §5.)
- **Serving a stale model after rollback.** Same cause: restart.
- **`model_source` shows a path you did not expect.** Print it — `/health`
  exists precisely so you never have to guess which file is live.

## 4. Tests

| Symptom | Likely cause | Fix |
|---|---|---|
| Tests hang or try to connect | Someone added a real network call | Tests must use `TestClient` (ASGI) — no server, no ports |
| `8 passed` locally, failures elsewhere | Working directory: relative paths resolve from `examples/churn` | Keep `rootdir` assumptions out of tests; run from the project folder |
| `StarletteDeprecationWarning` about httpx | Upstream deprecation notice in the installed stack | Informational; note it, pin consciously, do not silence tests |
| Determinism test fails | Model reloaded differently or unseeded preprocessing | Model is loaded once per process; the test compares within one process — check you didn't add randomness |

## 5. Performance questions

- **"Latency spiked."** First split the space: is it the model (slow call),
  the framework (JSON parsing), or the caller (huge batches)? Time
  `/health` (no model work) vs `/predict` to separate them.
- **"Throughput is lower than expected."** uvicorn runs a single worker by
  default; per-request work in Python is GIL-bound. That is *expected* here —
  Module 11 (container) and Module 16 (scaling) address it honestly; do not
  "fix" it with fake numbers.

## 6. Security-shaped reminders (no fixes here, deliberately)

The service binds localhost, has no auth, and no TLS — correct for a lab and
wrong for production. Module 15 covers auth/secrets/privacy; Module 16 covers
exposure, HTTPS, and rate limits. Do not "quickly" expose this port to a
network as an experiment.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*