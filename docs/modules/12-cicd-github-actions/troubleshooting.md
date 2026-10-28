# Troubleshooting — Module 12

Symptom → likely cause → fix. See the
[course troubleshooting hub](../../troubleshooting/index.md) for Python issues.

---

## 1. The workflow never runs

| Symptom | Likely cause | Fix |
|---|---|---|
| No run appears at all | `.github/workflows/` not at **repository root** | It must be `<repo>/.github/workflows/ci.yml`, not inside `examples/` |
| Push ran, PRs don't (or vice versa) | Trigger mismatch | Our file needs `push` **and** `pull_request` on `main`; check your target branch |
| Runs on some branches only | `branches:` filters | Compare default branch name with the `on:` block |
| `Invalid workflow file` annotation | YAML syntax error | Parse locally: `python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"`; check 2-space indentation |
| Runs but never changes | Push landed on a different remote/branch | `git status -sb`; verify remote and branch |

## 2. Red runs — reading them properly

| Symptom | Likely cause | Fix |
|---|---|---|
| `lint` red, `F401 ...` | Unused import (this exact thing happened during authoring: 4 real finds) | Remove the import — do **not** add `noqa` to silence it |
| `test` red at *Generate the dataset* | Step order/paths: `working-directory` wrong, or generator failing | Run the same command in `examples/churn` locally |
| `test` red at *Run the test suite* | A real regression, or a test needing files CI doesn't have | Reproduce with the identical command; remember CI starts from a **clean checkout** — anything you forgot to commit (or gitignored wrongly) is missing there |
| `ml-validate` red: `missing artifacts/metrics.json` | The job trains *before* checking — if you edited the job, that order may be broken | Keep steps: generate → train → `ml_check.py` |
| `ml-validate` red: checks named (`no_missing_values`) | Corrupt/edited data committed, or generator seed changed | That's the gate working; inspect the extract (Module 04 tools) |
| Only on GitHub, never locally | Env difference (Python version, missing install step) | Compare the job's `run:` list with your local shell history line by line |

## 3. Caching, artifacts, and speed

- **Cache misses every run:** the key includes `requirements-docker.txt` —
  if your process edits pins constantly, expect misses (correctness > speed).
- **Artifact upload fails:** path wrong or file absent (coverage file is
  created only when `pytest --cov` runs with that exact flag).
- **Runs feel slow:** check for stale runs (our `concurrency` should cancel
  them), sequential `needs:` chains you added unnecessarily, and pip installing
  without the cache. Deferrable work (heavy validation) belongs in Module 13's
  schedule, not in every push.

## 4. Secrets and permissions (when you add them later)

| Symptom | Likely cause | Fix |
|---|---|---|
| Secret arrives empty in `env:` | Name typo, or secret defined in the wrong repo/environment | Check `Settings → Secrets and variables → Actions`; reference exactly `${{ secrets.NAME }}` |
| Secret printed in the log | You echoed it, or a tool printed the env | **Treat as leaked:** revoke/rotate immediately — masking only covers *registered* secrets |
| `Resource not accessible by integration` | Token lacks the permission a step needs | Grant the **narrowest** extra permission — do not widen to `write-all` as a shortcut |
| Third-party action fails/behaves oddly | Unpinned action changed | Pin official `actions/*` at major tags; be wary of unfamiliar repos (you are executing their code) |

## 5. Conceptual checks

- **"CI passed, so the model is good."** CI proved *gates held on that commit*:
  contract passed, metrics ≥ floor, tests green. It did not evaluate freshness
  or fairness in the wild — that's Module 14's evidence loop.
- **"We'll add deployment later, so permissions can be broad now."** Narrow
  permissions are cheapest at creation time; retrofitting means auditing what
  already ran with the broad token.
- **"The workflow is the gatekeeper, so I stopped running checks locally."**
  Local runs are the *debug loop* for CI (concepts §7) — the lab's whole
  method depends on that symmetry.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*