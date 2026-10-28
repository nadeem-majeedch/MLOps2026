# Question bank 06 — CI/CD and orchestration

**Covers:** Modules [12 — CI/CD with GitHub Actions](../../modules/12-cicd-github-actions/index.md)
and [13 — Workflow orchestration](../../modules/13-orchestration-scheduled-pipelines/index.md).
**Format:** 10 questions — multiple choice, short answer, debugging, architecture, scenario.
**Suggested check:** 7/10, with **C5** and **C10** correct.

> *Attempt first, then read the
> [reference solutions](../keys/question-banks-KEY.md).*

---

## Part A — Multiple choice

**C1.** The correct place for a secret used by CI is:

- (a) In the workflow YAML, committed
- (b) In the repository's settings/secrets, injected at run time via
  `${{ secrets.NAME }}`
- (c) In an environment file committed to the repo
- (d) In the README so everyone has it

**C2.** `permissions: contents: read` in a workflow means:

- (a) The job cannot run
- (b) The job can read the repository and nothing else (least privilege)
- (c) Secrets are readable
- (d) Releases can be published

**C3.** A workflow should install dependencies from:

- (a) Whatever is newest on PyPI that day
- (b) A pinned requirements/lock file, cached between runs
- (c) A manual `pip install` by whoever set up the runner
- (d) A global system Python environment

**C4.** Which is the strongest argument *against* adding an orchestrator to a
project with one five-second nightly script?

- (a) Orchestrators are fashionable
- (b) The operational cost (deploying, maintaining, learning a scheduler)
  outweighs the benefit for a single simple job
- (c) Orchestrators cannot run Python
- (d) Cron is more secure

## Part B — Short answer

**C5.** Explain *retries*, *backfills*, and *idempotency* in scheduled
pipelines. For each: what it is, and one concrete failure it prevents.

**C6.** What should a CI run for an ML project include, and what should it
deliberately *not* include (cost, time, nondeterminism)?

**C7.** Describe how CI handles a failed job: where the error appears, what the
developer reads first, and why artefacts/reports are uploaded even on failure.

## Part C — Debugging

**C8.** This workflow passes locally but fails in CI. Find **three** likely
defects:

```yaml
- run: pip install -r requirements.txt
- run: python src/train.py        # works on the author's machine only
- run: pytest -q
  env:
    API_KEY: "sk-live-123456"     # needed for one test
```

## Part D — Architecture

**C9.** Draw a CI pipeline for an ML repo with three jobs (lint, tests, ML
validation). Show triggers, caching, artefact upload, and where a release gate
would sit if there were a fourth job.

## Part E — Scenario

**C10.** You must decide between (i) a cron-scheduled script, (ii) a
lightweight orchestrator, and (iii) a full platform, for: a nightly retrain of
one model; a 12-step DAG across four teams with backfills and SLAs; a
one-off experiment. Give your choice for each with a one-line justification,
and name the signal that would make you move to the next option up.

---

**Next:** [reference solutions](../keys/question-banks-KEY.md) (bank 06), then
[bank 07](q07-monitoring-drift.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../../about/index.md).*
