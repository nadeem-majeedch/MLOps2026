# Learning objectives — Module 13

Maps to syllabus outcomes
[LO 13.1–13.4](../../syllabus/detailed-syllabus.md#module-13-workflow-orchestration-and-scheduled-pipelines).

| # | You can… | You prove it by… |
|---|---|---|
| **13.1** | Convert the Module 08 build graph into an orchestrated workflow with retries, logging, and failure policy | `orchestrate/flow.py` running the five stages with `--retries` visible in `runs.jsonl` |
| **13.2** | Schedule runs and trigger one on demand | `--every N --max-runs` ticks plus `--once`; plus a written cron / Task Scheduler entry that would do the same on a real host |
| **13.3** | Handle failure deliberately: alerting, idempotent re-runs | The failure tick writing `ALERT.md` (with attempts) and the recovery tick clearing it — both transcripts captured |
| **13.4** | Compare orchestrators (Airflow vs Prefect vs Dagster vs hosted) and justify a choice | Your scenario verdict in the lab §12/challenge: named tool, named rejected alternative, three reasons each |

## Supporting skills

- Distinguish **event-driven** triggering ("new file arrived") from
  **interval** scheduling ("every 15 minutes") and say which fits your data.
- Explain why retries are for *transient* faults, and what a retry does to a
  *deterministic* error (spoiler: three identical failures and a slower red).
- State the idempotency requirement a scheduler imposes on every task — and
  where Module 08 already established it.
- Identify what an orchestrator does **not** fix (bad tests, weak gates,
  missing lineage — they travel with you from Modules 07–09).

## Self-check questions

1. At what point does a `python -m pipe.run` in Task Scheduler stop being
   enough?
2. Why does a failed tick write a file instead of sending an email itself?
3. Which failure here should *not* be retried, and why?

*(Answers in [knowledge-check.md](knowledge-check.md) — attempt first.)*

---

[← Module 13 index](index.md) · [Next: concepts →](concepts.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*