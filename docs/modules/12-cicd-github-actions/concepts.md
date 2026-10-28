# Concepts — Module 12

*Vocabulary: CI, CD, workflow, job, step, runner, trigger, pull request,
artifact, cache, secret, permissions, concurrency, smoke test, quality gate,
deployment (and why we stop before it).*

---

## 1. CI, CD, and where this course stops

- **CI (continuous integration)** — every change is built and checked
  automatically, in a clean environment, before it can merge. *This module.*
- **CD (continuous delivery/deployment)** — the checked change is then shipped,
  by hand (delivery) or automatically (deployment).

Our workflow is **continuous integration for ML**: lint → tests → data/model
validation. Deployment needs a target (your laptop, a server, a platform) and
real credentials — that is Modules 15–16 territory. Shipping an ML system
*responsibly* means CI first: a gate you can't bypass is worth more than a
pipeline that auto-publishes.

## 2. The anatomy of a workflow

```yaml
name: ci
on:                        # TRIGGERS
  push: { branches: [main] }
  pull_request: { branches: [main] }
concurrency:               # one useful run per branch
  group: ci-${{ github.ref }}
  cancel-in-progress: true
permissions: { contents: read }      # least privilege
jobs:                      # independent machines, run in PARALLEL
  lint:      { runs-on: ubuntu-latest, steps: [...] }
  test:      { ... }
  ml-validate: { ... }
```

| Piece | Meaning |
|---|---|
| **Trigger (`on`)** | *when* runs happen: pushes to `main`, and every PR targeting `main` |
| **Job** | a fresh VM (`runs-on: ubuntu-latest`) with its own install; jobs are **parallel** unless `needs:` says otherwise |
| **Step** | one command or one reusable action (`uses: actions/checkout@v4`) |
| **Runner** | the VM itself — Linux in our workflow (cheapest and closest to deployment reality; you validated Windows-local behaviour yourself) |
| **`${{ }}`** | context expressions: `github.ref`, secrets, outputs |
| **Artifact** | files uploaded from a run for humans to download (our coverage report) |
| **Cache** | persisted downloads (pip wheels) keyed on the requirements file — a *speed* feature, never a correctness one |

Why the jobs are separate instead of one long job: **failure names the layer**.
A red `lint` tells you style; a red `test` tells you code; a red `ml-validate`
tells you *the model or the data* — which is the ML-specific message classic
CI cannot send.

## 3. The ML validation job — validation, not retraining

`ml_check.py` runs two gates with **no training**:

1. data contract on `data/raw/churn.csv` (Module 04's checks),
2. `roc_auc >= quality.roc_auc_floor` from `artifacts/metrics.json`.

CI trains *once* in the job (cheap, deterministic, ~1 s) so metrics exist for
a clean checkout — then validates. Why not full retraining with experiment
search in CI? Time, flakiness, and cost: CI must stay **fast and deterministic**
or people learn to ignore it. Heavy validation belongs in a nightly run —
Module 13's scheduler.

> **Quality gate in CI** = the Module 08/09 gates, now enforced by something
> that cannot be persuaded. "Who approved this model?" → "The workflow did,
> on commit `abc123`, with these logs."

## 4. Secrets: the three-place rule

A **secret** is a value that grants access (API key, token, password). Our
workflow uses none — deliberately, so the pattern is visible without
temptation. If you ever add one:

1. **Not in source** — not in the YAML, not in `.py`, not in the Dockerfile.
2. **Not in logs** — GitHub masks registered secrets in output, but only
   registered ones; never `echo` a variable "just to check".
3. **Not on disk in CI** — it arrives via `${{ secrets.NAME }}` in `env:` at
   runtime and dies with the runner.

Where secrets live: GitHub → Settings → *Secrets and variables → Actions* (or
your platform's equivalent). This repo's own conventions put project keys in
environment files the instructor controls — never committed. (Module 15
generalises this beyond CI.)

## 5. Permissions and blast radius

`permissions: contents: read` means the workflow token **cannot push, open
PRs, or alter the repo** — it only reads the checkout. Default tokens are
often broader than needed; narrowing them is free security. Same instinct as:
runner images are disposable, third-party actions (`uses:`) are **code you
are executing** — pin the ones you trust, prefer official `actions/*`.

## 6. Concurrency and cost

`concurrency` + `cancel-in-progress` stops stale runs piling up when you push
three times in a minute — you always care about the newest commit. Public
repos get free Actions minutes; private ones have an allowance. Designing for
*fast, parallel, cancellable* runs is a cost decision as much as a UX one.

## 7. What a red run teaches (LO 12.4)

The reading order of a failing run:

1. **Which job** went red → which *layer* (lint / tests / ML gates).
2. **Which step** → the exact command.
3. **The step's output** → the first error line, not the last.
4. Reproduce **locally with the same command** — our workflow uses only
   commands you can run on your laptop, which is exactly why the lab works
   even without a GitHub account.

## 8. Delivery (the honest boundary)

This workflow **stops at validation**. Adding delivery means answering:
deploy *where*? With *what credentials*? After *whose approval*? Those are the
Module 15 (secrets/approval) and Module 16 (platform) questions — and the
capstone's integration point. CD for ML adds one more rule: the artefact that
passes CI must be the *same bytes* that deploy (digest-pinned images, signed
artifacts — advanced reading in [references](references.md)).

---

**Next:** [worked-example.md](worked-example.md) — the workflow, parsed and
executed step by step.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*