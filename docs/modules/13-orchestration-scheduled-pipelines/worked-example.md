# Worked example — five ticks, observed

All output is **actual** from `python -m orchestrate.flow` in `examples/churn/`
(the last tick uses a regenerated dataset to return the workspace to its
original state).

---

## 1. The graph as the scheduler sees it

```powershell
python -m orchestrate.flow --list
```

```text
task graph (linear, mirrors Module 08):
  1. validate
  2. features
  3. train
  4. evaluate
  5. report
schedule: --every N s | --once
retries: 2 with 1.0s backoff
history: orch_out/runs.jsonl   alert: orch_out/ALERT.md
```

Same stages as `pipe.run` — the module's point is what surrounds them.

## 2. Tick 1 — first run (nothing recorded yet)

```powershell
python -m orchestrate.flow --once
```

```text
tick 20261025T202930Z: work needed (previous run did not succeed)
  validate  success  (1 attempt(s))
  features  success  (1 attempt(s))
  train     success  (1 attempt(s))
  evaluate  success  (1 attempt(s))
  report    success  (1 attempt(s))
tick 20261025T202930Z: success in 0.22s
exit=0
```

## 3. Tick 2 — nothing to do (the skip logic)

```text
tick 20261025T202933Z: skipped - no new data and outputs are intact
exit=0
```

One line, exit 0 — an *explicit* no-op, distinct from a crash or a silent
success (concepts §4).

## 4. Tick 3 — new data arrives

```text
tick 20261025T202956Z: work needed (new data detected)
  validate  success  (1 attempt(s))
  features  success  (1 attempt(s))
  train     success  (1 attempt(s))
  evaluate  success  (1 attempt(s))
  report    success  (1 attempt(s))
tick 20261025T202956Z: success in 0.25s
```

(New data = a different extract swapped in; the hash moved, so work was needed.)

## 5. Tick 4 — corrupt data: retries, then an alert

```text
tick 20261025T202959Z: work needed (new data detected)
  validate  failed  (3 attempt(s))
tick 20261025T202959Z: FAILED at 'validate' - see orch_out/ALERT.md
exit=1
```

`orch_out/ALERT.md` (real content):

```markdown
# ALERT - training workflow failed

| | |
|---|---|
| run | `20261025T202959Z` |
| failed task | **validate** |
| attempts | 3 |

## What happened

```
attempt 1: data contract violated: no_missing_values, value_ranges
attempt 2: data contract violated: no_missing_values, value_ranges
attempt 3: data contract violated: no_missing_values, value_ranges
```
...
```

Read the attempts: **three identical strings** — a deterministic failure
exhausting its retries (concepts §3). The alert carries the diagnosis, not
just the news.

## 6. Tick 5 — recovery clears the alert

Dataset regenerated, same command:

```text
tick 20261025T203005Z: work needed (new data detected)
  validate  success  (1 attempt(s))
  features  success  (1 attempt(s))
  train     success  (1 attempt(s))
  evaluate  success  (1 attempt(s))
  report    success  (1 attempt(s))
tick 20261025T203005Z: success in 0.21s
exit=0
```

```text
ALERT exists after recovery? no
```

## 7. The history file (one JSON line per tick)

```json
{"run_id": "20261025T202930Z", "trigger": "once", "status": "success", "duration_s": 0.22, "data_sha": "e38d7738cf5524df", "tasks": {"validate": {"status": "success", "attempts": ["attempt 1: ok (0.06s)"]}, "...": "..."}}
{"run_id": "20261025T202933Z", "trigger": "once", "status": "no_new_data", "reason": "no new data and outputs are intact", "data_sha": "e38d7738cf5524df"}
{"run_id": "20261025T202956Z", "trigger": "once", "status": "success", "duration_s": 0.25, "data_sha": "603b35e423a62045", "tasks": {"...": "..."}}
{"run_id": "20261025T202959Z", "trigger": "once", "status": "failed", "duration_s": 2.08, "data_sha": "d3e85a1ceb9c35f4", "tasks": {"validate": {"status": "failed", "attempts": ["attempt 1: data contract violated: no_missing_values, value_ranges", "attempt 2: ...", "attempt 3: ..."]}}}
{"run_id": "20261025T203005Z", "trigger": "once", "status": "success", "duration_s": 0.21, "data_sha": "e38d7738cf5524df", "tasks": {"...": "..."}}
```

Five ticks, five statuses, two data hashes (the corrupt swap and the
regeneration are visible in the record without reading any log).

## 8. Interval mode (same code, different trigger)

```powershell
python -m orchestrate.flow --every 60 --max-runs 3
```

```text
scheduler started: every 60s, max 3 ticks (Ctrl+C to stop)
tick ...: skipped - no new data and outputs are intact
tick ...: skipped - no new data and outputs are intact
tick ...: skipped - no new data and outputs are intact
```

Three honest no-ops at one-minute spacing (interval runs behave exactly like
the `--once` ticks above — one of which you have seen fail).

---

**Next:** [lab.md](lab.md) — build the same evidence yourself, plus a real OS
scheduler entry.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*