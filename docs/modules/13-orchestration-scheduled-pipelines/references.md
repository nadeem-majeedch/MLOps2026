# References — Module 13

## Tool documentation

| Resource | Use it for |
|---|---|
| [Apache Airflow documentation](https://airflow.apache.org/docs/) | The industry-standard orchestrator: DAG authoring, schedulers, sensors, pools |
| [Prefect documentation](https://docs.prefect.io/) | Python-native flows, retries-as-API, hybrid execution |
| [Dagster documentation](https://docs.dagster.io/) | Software-defined assets and data lineage as first-class concepts |
| [cron(5) man page](https://man7.org/linux/man-pages/man5/cron.5.html) | Interval syntax for Unix scheduling |
| [Windows Task Scheduler (`schtasks`)](https://learn.microsoft.com/windows-server/administration/windows-commands/schtasks) | The 🪟 equivalent used in lab Step 5 |
| [`watchdog` (PyPI)](https://pypi.org/project/watchdog/) | Filesystem event triggers (challenge task 3, if you want a library) |
| [Airflow best practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html) | Idempotency, scheduling hygiene — the same rules this module teaches |

## Reading

- **Katsifarakis et al. (2023), *A survey on workflow orchestration
  frameworks*** — an academic map of the tool landscape (useful counterweight
  to vendor comparison pages).
- **Braun & Statz (2021), *A Survey of Scientific Workflow Management Systems***
  — the older lineage (Pegasus, Taverna) that modern tools descend from.
- **Google SRE book, ch. 5 (*Handling Overload*) & ch. 4 (*Alerting*)** —
  alert fatigue, actionable alerts: the concepts §5 sources.
- **Kreideweis et al., *Towards Observability Pipelines*** (or any current
  observability vendor whitepaper) — how alert delivery scales beyond a file.

## Distinguishing tool-specific from general

| Claim | Kind |
|---|---|
| "Retries suit transient faults, not deterministic ones" | **General principle** |
| "Alerts need diagnosis + owner + action; silence trains ignore" | **General principle** |
| "Tasks must be idempotent under a scheduler" | **General principle** |
| "`--every N`, `runs.jsonl`, `ALERT.md`" | **Course-specific runner** |
| "`schtasks /Create /SC ONCE`", cron field order | **OS-specific syntax** |
| "Airflow requires a metadata DB + scheduler + webserver" | **Tool-specific architecture** — check current versions |

## Related course material

- Module 08 — the graph being scheduled.
- Module 12 — event (push) triggering as another trigger class.
- Module 14 — monitoring feeds the *decision* to run retraining at all.
- [Tool selection guide](../../syllabus/tool-selection-guide.md) — the course's
  overall tool philosophy.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*