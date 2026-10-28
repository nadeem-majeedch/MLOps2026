"""The scheduled workflow runner (Module 13) — see package docstring."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import time
from datetime import datetime, timezone

from pipe import stages

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "orch_out"
STATE = OUT / "state.json"
RUNS = OUT / "runs.jsonl"
ALERT = OUT / "ALERT.md"
DATA = ROOT / "data" / "raw" / "churn.csv"

# The task graph is the Module 08 pipeline, unchanged: orchestration adds
# schedule/retries/history around stages, it does not rewrite them.
TASKS = [
    ("validate", stages.validate),
    ("features", stages.features),
    ("train", stages.train),
    ("evaluate", stages.evaluate),
    ("report", stages.report),
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def data_sha() -> str:
    if not DATA.exists():
        return "missing"
    return hashlib.sha256(DATA.read_bytes()).hexdigest()[:16]


def load_json(path: pathlib.Path, default: dict) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def work_needed(state: dict) -> tuple[bool, str]:
    """Decide whether this tick should do anything at all."""
    if state.get("status") != "success":
        return True, "previous run did not succeed"
    if data_sha() != state.get("data_sha"):
        return True, "new data detected"
    if not (ROOT / "pipe_out" / "report.md").exists():
        return True, "outputs are missing"
    return False, "no new data and outputs are intact"


def run_task(fn, retries: int, backoff: float) -> tuple[str, list[str]]:
    """Attempt a task up to retries+1 times. Retries exist for *transient*
    failures (locked file, busy port); a logic error will fail every time —
    that is what the test suite is for (Module 07), not the scheduler."""
    attempts: list[str] = []
    for attempt in range(1, retries + 2):
        started = time.time()
        try:
            fn()
            attempts.append(f"attempt {attempt}: ok ({time.time() - started:.2f}s)")
            return "success", attempts
        except SystemExit as exc:
            attempts.append(f"attempt {attempt}: {exc}")
        except Exception as exc:
            attempts.append(f"attempt {attempt}: {type(exc).__name__}: {exc}")
        if attempt <= retries:
            time.sleep(backoff)
    return "failed", attempts


def write_alert(run_id: str, task: str, attempts: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    ALERT.write_text(
        f"""# ALERT - training workflow failed

| | |
|---|---|
| run | `{run_id}` |
| failed task | **{task}** |
| attempts | {len(attempts)} |

## What happened

```
{chr(10).join(attempts)}
```

## What to do

1. Read the last line above: retries already covered transient causes.
2. Reproduce locally: `python -m pipe.run --force`.
3. Fix, then re-run this tick: `python -m orchestrate.flow --once`.

_Generated automatically. This file is the workflow's voice: an unattended
run must never fail silently._
""",
        encoding="utf-8",
    )


def tick(trigger: str, retries: int, backoff: float) -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    state = load_json(STATE, {})
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    needed, reason = work_needed(state)
    if not needed:
        record = {
            "run_id": run_id, "trigger": trigger, "status": "no_new_data",
            "reason": reason, "at": now(), "data_sha": data_sha(),
        }
        RUNS.open("a", encoding="utf-8").write(json.dumps(record) + "\n")
        print(f"tick {run_id}: skipped - {reason}")
        return 0

    print(f"tick {run_id}: work needed ({reason})")
    started = time.time()
    results: dict[str, dict] = {}
    status = "success"
    failed_task = None

    for name, fn in TASKS:
        task_status, attempts = run_task(fn, retries, backoff)
        results[name] = {"status": task_status, "attempts": attempts}
        print(f"  {name:9} {task_status}  ({len(attempts)} attempt(s))")
        if task_status == "failed":
            status = "failed"
            failed_task = name
            break                      # downstream stages must not run

    duration = round(time.time() - started, 2)
    record = {
        "run_id": run_id, "trigger": trigger, "status": status,
        "at": now(), "duration_s": duration,
        "data_sha": data_sha(), "tasks": results,
    }
    RUNS.open("a", encoding="utf-8").write(json.dumps(record) + "\n")

    if status == "failed":
        write_alert(run_id, failed_task, results[failed_task]["attempts"])
        print(f"tick {run_id}: FAILED at '{failed_task}' - see orch_out/ALERT.md")
        return 1

    STATE.write_text(
        json.dumps({"status": "success", "data_sha": data_sha(),
                    "last_run": run_id}, indent=2),
        encoding="utf-8",
    )
    if ALERT.exists():
        ALERT.unlink()                 # a recovered system stops shouting
    print(f"tick {run_id}: success in {duration}s")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="python -m orchestrate.flow",
        description="Scheduled training workflow with retries and history",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--once", action="store_true", help="run exactly one tick")
    mode.add_argument("--every", type=int, metavar="SECONDS",
                      help="poll on an interval (loop until --max-runs)")
    mode.add_argument("--list", action="store_true", help="show the task graph")
    parser.add_argument("--max-runs", type=int, default=3,
                        help="stop the --every loop after N ticks (default 3)")
    parser.add_argument("--retries", type=int, default=2,
                        help="retries per task before failing (default 2)")
    parser.add_argument("--backoff", type=float, default=1.0,
                        help="seconds between retries (default 1)")
    args = parser.parse_args()

    if args.list:
        print("task graph (linear, mirrors Module 08):")
        for i, (name, _) in enumerate(TASKS):
            print(f"  {i + 1}. {name}")
        print("schedule: --every N s | --once")
        print(f"retries: {args.retries} with {args.backoff}s backoff")
        print("history: orch_out/runs.jsonl   alert: orch_out/ALERT.md")
        return 0

    if args.every:
        print(f"scheduler started: every {args.every}s, "
              f"max {args.max_runs} ticks (Ctrl+C to stop)")
        exit_code = 0
        for i in range(args.max_runs):
            exit_code = tick("schedule", args.retries, args.backoff) or exit_code
            if i < args.max_runs - 1:
                time.sleep(args.every)
        return exit_code

    return tick("once", args.retries, args.backoff)


if __name__ == "__main__":
    raise SystemExit(main())