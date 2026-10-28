"""Scheduled training workflow (Module 13).

The *same* stages as the Module 08 pipeline, but run the way a real system
runs them: on a schedule, with retries, a run history, and an alert when
everything fails.

    python -m orchestrate.flow --once          # one scheduled tick
    python -m orchestrate.flow --every 60 --max-runs 3   # poll every 60 s

Differences from `python -m pipe.run` (a developer command):
  * it decides *whether* work is needed (no new data -> skip retraining),
  * it retries transient failures before giving up,
  * every tick is recorded in orch_out/runs.jsonl (audit trail),
  * a failed tick ends in orch_out/ALERT.md, not a forgotten console.
"""