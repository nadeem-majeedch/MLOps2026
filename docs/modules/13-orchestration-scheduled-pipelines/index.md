# Module 13 — Workflow orchestration and scheduled pipelines

!!! success "Module complete"
    Lessons, worked example, lab, independent challenge, knowledge check (with
    answers), troubleshooting, and references are all written.

**Stage:** Advanced · **Estimated effort:** 10 h · **Depends on:** 08, 12 · **Next:** 14

---

## What this module is about

Module 08 built the graph; Module 12 made it run on every push. This module
answers a different question: **who runs it at 02:00 when nobody is watching —
and what happens when it fails alone?**

You will wrap the *same* stages in a scheduled runner that adds the four
concerns a developer command does not have:

| Concern | What the module adds |
|---|---|
| **Schedule** | `--every N` interval loop and `--once` (plus system cron/Task Scheduler recipes) |
| **Deciding if work is needed** | data-hash check → *no new data → skip the tick* |
| **Retries** | `--retries 2 --backoff 1` for transient failures, with a written rationale for what is *not* retried |
| **Alerting + history** | a failed tick writes `orch_out/ALERT.md` and a line in `runs.jsonl` — and recovery clears the alert |

The module is equally about **restraint**: you will be able to state when a
plain script or Make is still the right answer, and compare Airflow, Prefect,
Dagster, and hosted options on evidence rather than fashion.

## How to study this module (in order)

| # | File | What it does | Time |
|---|---|---|---|
| 1 | [learning-objectives.md](learning-objectives.md) | What you must be able to do, and how you prove it | 10 min |
| 2 | [concepts.md](concepts.md) | When orchestration is justified; retries, idempotence, scheduling, tool comparison | 120 min |
| 3 | [worked-example.md](worked-example.md) | Five real ticks: fresh run, no-op, new data, failure+alert, recovery | 45 min |
| 4 | [lab.md](lab.md) | **Guided lab:** a pipeline that runs itself (and tells you when it fails) | 130 min |
| 5 | [independent-challenge.md](independent-challenge.md) | Add a catch-up policy and an event trigger, then pick a tool for a case | 75 min |
| 6 | [knowledge-check.md](knowledge-check.md) | 10 questions with reasoning | 30 min |
| 7 | [troubleshooting.md](troubleshooting.md) | Scheduler loops, retry storms, alert fatigue | as needed |
| 8 | [references.md](references.md) | Airflow/Prefect/Dagster docs, cron, scheduling papers | optional |

## Before you start

- Module 08 complete (you know the stages and their gates).
- Module 12's CI green (automation you already trust in a different context).
- Free, local, no accounts. ⚠️ Only if you choose the Airflow extension:
  it is heavy (~1 GB of dependencies) — the core path never needs it.

## Evidence you should produce

1. A five-tick transcript covering: fresh run, *no-new-data* skip, new data,
   failure with `ALERT.md`, and recovery with the alert cleared.
2. Your `orch_out/runs.jsonl` history pasted as evidence.
3. A written tool choice for a given scenario, with the runner you *wouldn't*
   pick and why.

---

[← Module 12: CI/CD with GitHub Actions](../12-cicd-github-actions/index.md) · [Full syllabus](../../syllabus/detailed-syllabus.md#module-13-workflow-orchestration-and-scheduled-pipelines) · [Module 14 →](../14-monitoring-drift-retraining/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*