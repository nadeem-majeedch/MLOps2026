# LAB-16 — reference solution

> Attempt the lab first. This is the answer key, not the assignment.

## Verified runs (authoring machine, Python 3.14)

```text
$ python tick_runner.py --ticks 3 --interval 0.2 --fail-tick 2
schedule: 3 tick(s) every 0.2s (fail-tick=2)
  tick 1: success on attempt 1
  tick 2: attempt 1 failed (injected fault (synthetic outage))
  tick 2: attempt 2 failed (injected fault (synthetic outage))
  tick 2: attempt 3 failed (injected fault (synthetic outage))
  ALERT raised -> ALERT.md
  tick 3: success on attempt 1
  ALERT cleared
history: 2/5 successful attempts in runs.jsonl
```

```text
$ python tick_runner.py --ticks 2 --interval 0.2 --fail-tick 2
… tick 2 fails all 3 attempts …
$ ls ALERT.md
ALERT.md                       # persists — no recovery tick ran
```

Both rows of the reliability contract verified: **alert raises, clears on
recovery, and *stays* when recovery never comes.**

## What the numbers mean (the monitoring note you write)

- `2/5 successful` counts *attempts*, not ticks — retry policy is visible
  in the log, which is the point: an orchestrator that retries three
  times must show three failures, not one silent success.
- `runs.jsonl` grows monotonically; `out/summary.json` is the latest
  state. Timestamps in the JSONL are the audit trail you quote in your
  scheduled-run evidence ("entries with timestamps you didn't trigger").

## OS scheduling — model answers

| | 🪟 Windows | 🐧 Linux/macOS |
|---|---|---|
| Register | `schtasks /create /tn MLOpsLab16 /sc minute /mo 15 /tr "python C:\path\tick_runner.py --ticks 1"` | `crontab -e` → `*/15 * * * * cd /path && python tick_runner.py --ticks 1` |
| Verify it fired | `schtasks /query /tn MLOpsLab16` + entries in `runs.jsonl` you did not trigger | `grep tick_runner /var/log/syslog` or just the JSONL |
| **Remove (cleanup)** | `schtasks /delete /tn MLOpsLab16 /f` | `crontab -e` and delete the line |

Trade-off table (what your note must contain): a plain scheduled script
is *right* when the job is one command, single-machine, no dependency
between steps, and you can read its outcome from a file. It stops being
right when you need retries across steps, backfills, parallel branches,
a UI of run history, or multi-machine workers — that is when an
orchestrator (Module 13: Airflow/Prefect/Dagster compared) earns its
complexity. Running an orchestrator for one five-second job is
infrastructure theatre.

## Common wrong answers

- Leaving `schtasks`/cron registered after the lab — the next person's
  machine runs your experiment forever. Cleanup is part of the grade.
- Reading `out/summary.json` instead of `runs.jsonl` for the history —
  summary is *latest state*, JSONL is *evidence*.
- Claiming scheduled ticks fired without pasting the JSONL rows.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../../docs/about/index.md).*
