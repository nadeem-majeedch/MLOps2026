"""LAB 16 fixture — a scheduled tick runner you can actually watch.

    python tick_runner.py --ticks 3 --interval 1
    python tick_runner.py --ticks 3 --fail-tick 2    # inject one failure
    python tick_runner.py --ticks 1                  # the recovery tick

Every tick runs the same job (a tiny deterministic "training" over the
shared dataset), appends to runs.jsonl, and writes ALERT.md when a tick
fails — clearing it again when a later tick succeeds. This is Module 13's
lesson in miniature, in one file that runs anywhere: no orchestrator, no
account, no daemon required (the lab's OS scheduling step wires it to
Task Scheduler / cron afterwards).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import time
from datetime import datetime, timezone

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE.parent / "data" / "customers_clean.csv"
RUNS = HERE / "runs.jsonl"
ALERT = HERE / "ALERT.md"
OUT = HERE / "out" / "summary.json"


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def job() -> dict:
    """The work: a deterministic summary that doubles as a smoke test."""
    raw = DATA.read_bytes()
    rows = len(raw.splitlines()) - 1
    digest = hashlib.sha256(raw).hexdigest()[:16]
    result = {"rows": rows, "data_sha16": digest, "ok": rows > 0}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def record(entry: dict) -> None:
    with RUNS.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")


def set_alert(text: str | None) -> None:
    if text is None:
        if ALERT.exists():
            ALERT.unlink()
            print("  ALERT cleared")
        return
    ALERT.write_text(f"# ALERT\n\n{now()}\n\n{text}\n", encoding="utf-8")
    print(f"  ALERT raised -> {ALERT.name}")


def run_tick(tick: int, fail: bool) -> bool:
    attempts, backoff = 3, 0.2
    for attempt in range(1, attempts + 1):
        started = time.time()
        try:
            if fail:
                raise RuntimeError("injected fault (synthetic outage)")
            result = job()
            record({"tick": tick, "at": now(), "attempt": attempt,
                    "status": "success", "duration_s":
                    round(time.time() - started, 3), **result})
            print(f"  tick {tick}: success on attempt {attempt}")
            return True
        except Exception as exc:
            record({"tick": tick, "at": now(), "attempt": attempt,
                    "status": "failed", "error": str(exc)})
            print(f"  tick {tick}: attempt {attempt} failed ({exc})")
            if attempt < attempts:
                time.sleep(backoff)
    set_alert(f"tick {tick} failed after {attempts} attempts — investigate "
              "(runbook: docs/labs/lab-16-*.md)")
    return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="lab 16 tick runner")
    parser.add_argument("--ticks", type=int, default=3)
    parser.add_argument("--interval", type=float, default=1.0,
                        help="seconds between ticks (0 for a fast demo)")
    parser.add_argument("--fail-tick", type=int, default=0,
                        help="inject failure into this tick number")
    args = parser.parse_args(argv)

    print(f"schedule: {args.ticks} tick(s) every {args.interval}s "
          f"(fail-tick={args.fail_tick or 'none'})")
    ok = True
    for tick in range(1, args.ticks + 1):
        print(f"[{now()}] tick {tick}/{args.ticks}")
        succeeded = run_tick(tick, fail=(tick == args.fail_tick))
        ok = succeeded if tick == args.ticks else ok or succeeded
        if succeeded:
            set_alert(None)          # recovery clears the alert
        if tick < args.ticks and args.interval:
            time.sleep(args.interval)
    history = [json.loads(line) for line in
               RUNS.read_text(encoding="utf-8").splitlines()]
    successes = sum(1 for h in history if h["status"] == "success")
    print(f"history: {successes}/{len(history)} successful attempts in "
          f"{RUNS.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())