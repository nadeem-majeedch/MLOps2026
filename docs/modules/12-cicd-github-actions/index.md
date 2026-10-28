# Module 12 — CI/CD and ML validation workflows using GitHub Actions

!!! success "Module complete"
    Lessons, worked example, lab, independent challenge, knowledge check (with
    answers), troubleshooting, and references are all written.

**Stage:** Intermediate · **Estimated effort:** 9 h · **Depends on:** 07, 11 · **Next:** 13

---

## What this module is about

Your gates exist — in your terminal, where nobody is forced to run them. This
module moves them into **CI** (continuous integration): every push and pull
request gets linted, tested, and ML-validated by a machine that cannot be
talked out of it.

The shipped workflow `.github/workflows/ci.yml` has three jobs:

| Job | Blocks a merge when… |
|---|---|
| `lint` (ruff) | style/unused-import errors appear |
| `test` (pytest + coverage) | any of the **34** tests fails; coverage artifact uploaded |
| `ml-validate` (`ml_check.py`) | the data contract fails **or** metrics fall below `quality.roc_auc_floor` |

Two design commitments this module teaches and enforces: **least-privilege
permissions** (`contents: read` — the workflow cannot write to your repo), and
**secrets never in source** — there are none in this workflow, and the file
itself documents where they would go if you had them.

## How to study this module (in order)

| # | File | What it does | Time |
|---|---|---|---|
| 1 | [learning-objectives.md](learning-objectives.md) | What you must be able to do, and how you prove it | 10 min |
| 2 | [concepts.md](concepts.md) | CI vs CD, triggers, jobs, caching, artifacts, secrets, permissions | 120 min |
| 3 | [worked-example.md](worked-example.md) | The real workflow: parsed structure + every step run locally | 45 min |
| 4 | [lab.md](lab.md) | **Guided lab:** block a defective model release in CI | 140 min |
| 5 | [independent-challenge.md](independent-challenge.md) | Break CI on purpose, then harden it | 75 min |
| 6 | [knowledge-check.md](knowledge-check.md) | 10 questions with reasoning | 30 min |
| 7 | [troubleshooting.md](troubleshooting.md) | Failing runs, cache misses, YAML traps | as needed |
| 8 | [references.md](references.md) | Actions docs, workflow syntax, security guides | optional |

## Before you start

- Module 07's suite and Module 08's gates understood (CI *is* those, automated).
- **☁️ Optional but recommended:** a GitHub account to see the workflow run
  live. Everything else works **fully local** — you can run every step
  yourself, which is exactly what the lab does first.
- Free tier covers all steps (GitHub Actions has a free allowance for public
  repos).

## Evidence you should produce

1. A local transcript showing each job's commands passing.
2. A deliberately failing run: which job went red, and the log line you used
   to diagnose it (locally or on GitHub).
3. Your write-up of where a secret would go if you had one — and why it must
   never appear in the YAML, the logs, or the code.

---

[← Module 11: Docker containers](../11-docker-containers/index.md) · [Full syllabus](../../syllabus/detailed-syllabus.md#module-12-cicd-and-ml-validation-workflows-using-github-actions) · [Module 13 →](../13-orchestration-scheduled-pipelines/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*