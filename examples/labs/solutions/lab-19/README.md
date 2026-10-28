# LAB-19 — reference solution

> Attempt the lab first. This is the answer key, not the assignment.

## Verified scanner runs (authoring machine, Python 3.14)

```text
$ python scan_secrets.py flawed
flawed\config.py:13: R1 sensitive assignment API_KEY = "prod-secret-2f8a1c77b4e9d0136ac5"
flawed\config.py:17: R2 credentials inside a URL: postgres://svc_admin:Tr0ub4dor-3@...
2 finding(s) in 3 file(s) …
exit 1

$ python scan_secrets.py ../capstone-support
clean: 17 file(s), no findings
exit 0

$ python -m pytest tests/test_data.py -q      # in examples/capstone-support
5 passed

$ python -c "from service.app import resolve_model; print(resolve_model()['source'])"
releases/r001/model.joblib          # the promoted copy, not artifacts/
```

The scanner proves what regexes can see. **Exit codes 1 and 0 are the
deliverable** — paste both, from your own run.

## "What the scanner cannot see" — model list (≥5, each with evidence)

1. **Secrets in git *history* — not in the working tree.** A rotated key
   stays exploitable in old commits. Evidence: `git log -p -S "prod-secret" -- .
   ` / GitHub *Settings → Secrets* rotation note.
2. **Over-broad IAM / tokens with too many scopes.** Evidence: read the
   role/policy file, list actions granted vs actions used.
3. **PII written to logs by the application at runtime.** Evidence: run
   the service, send a record, grep the log lines for identifiers —
   scanners read source, not emitted logs.
4. **Unsafe deserialization** (`joblib.load`/`pickle` of an artefact from
   an untrusted source). Evidence: file:line of every `load()` + where
   the bytes came from.
5. **Model/data leakage and membership inference risk** in what the API
   exposes (`/model-info` metrics, per-record probabilities).
6. **Container posture**: running as root, unpinned base tag, secrets
   baked via `ENV`/`ARG`. Evidence: `grep -n "USER\|FROM\|ARG\|ENV"
   Dockerfile`.
7. **Dependency supply chain**: no hashes/pins, transitive CVEs.
   Evidence: `pip list --outdated`, `pip-audit` if available.

## Findings table shape (≥5 rows, none unowned)

| # | Finding | Where (file:line) | Severity | Fix or accepted risk + owner |
|---|---|---|---|---|
| 1 | Hard-coded API key | `flawed/config.py:13` | Critical | env var + rotate the exposed value |
| 2 | DB creds in URL | `flawed/config.py:17` | Critical | DSN from env; never log the DSN |
| 3 | PII (email) in logs | `flawed/service.py` predict() | High | log a pseudonymous id, drop the address |
| 4 | Unauthenticated endpoint | `flawed/service.py` | High | bearer token / internal network + auth |
| 5 | Group-dependent threshold | `flawed/service.py` flag() | High | single threshold + fairness test (Module 15) |
| … | … | … | … | "accepted risk" needs a named owner and a review date |

## PII/logging section

Name the **logged fields** you actually emit (model version, latency,
input feature *values*?) and cross-check against `tests/test_data.py`,
whose assertions prove the **absent identifiers** (no name, email, or
student id can appear in predictions or logs). If you can't point at the
assertion, you haven't checked — you've hoped.

## Container posture (this repo's actual answers)

- `USER`: the churn/capstone Dockerfiles rely on the base image default —
  state that honestly and add a non-root `USER` as your recommendation.
- Pinning: tags pinned (`python:3.14-slim`, `==` pins in
  `requirements-docker.txt`); digest-pinning is the production upgrade.
- `.dockerignore` excludes `.venv/`, `data/`, logs, tests — context stays
  small and secrets can't ride along.

## Verdict template (dated, conditional)

> **Verdict 2026-10-27 — CONDITIONALLY SAFE TO DEPLOY:** capstone
> service only, behind auth, with findings 1–3 fixed first; container
> runs non-root after PR #N. Re-review required if the model version,
> exposed endpoints, or data category changes.

## Common wrong answers

- Treating "scanner: clean" as a security audit — it is one narrow check.
- A findings table where every row says "accepted" with no owner.
- Leaving `git status` dirty or a real credential anywhere in the repo
  at submission.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../../docs/about/index.md).*
