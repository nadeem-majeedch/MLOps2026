"""LAB 18 fixture — two release candidates and a ledger of what happened.

    python runs_ledger.py list           # what shipped, what is staged
    python runs_ledger.py show v2        # full evidence for one release
    python runs_ledger.py decide --rollback v2 --reason "..."   # YOUR call
    python runs_ledger.py history        # the audit trail

The evidence for the decision is all here: metrics, latency, error rate,
and the monitoring window that followed each release. v1 served for three
weeks; v2 has been live for four days. Read the numbers, then decide with
reasons — rollback is one command, but only after you can justify it.
"""

from __future__ import annotations

import argparse
import json
import pathlib
from datetime import datetime, timezone

HERE = pathlib.Path(__file__).resolve().parent
LEDGER = HERE / "ledger.json"
HISTORY = HERE / "history.jsonl"

SEED_LEDGER = {
    "current": "v2",
    "releases": {
        "v1": {
            "released_at": "2026-09-28T09:00:00+00:00",
            "model": "logreg-baseline", "auc": 0.7841,
            "recall": 0.41, "p95_latency_ms": 38, "error_rate_pct": 0.2,
            "window": {"days_served": 21, "mean_auc": 0.7798,
                       "alerts": 0,
                       "note": "stable; drift PSI 0.04 on all features"},
            "state": "superseded"
        },
        "v2": {
            "released_at": "2026-10-22T09:00:00+00:00",
            "model": "gbdt-challenger", "auc": 0.7613,
            "recall": 0.47, "p95_latency_ms": 118, "error_rate_pct": 2.6,
            "window": {"days_served": 4, "mean_auc": 0.7302,
                       "alerts": 6,
                       "note": "PSI 0.31 on monthly_charges; two timeout "
                               "spikes during the evening peak"},
            "state": "current"
        }
    }
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load() -> dict:
    if LEDGER.exists():
        return json.loads(LEDGER.read_text(encoding="utf-8"))
    LEDGER.write_text(json.dumps(SEED_LEDGER, indent=2), encoding="utf-8")
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def save(state: dict) -> None:
    LEDGER.write_text(json.dumps(state, indent=2), encoding="utf-8")


def log(entry: dict) -> None:
    with HISTORY.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")


def cmd_list(_: argparse.Namespace) -> int:
    state = load()
    print(f"{'id':4} {'state':10} {'auc':7} {'p95_ms':7} {'err%':6} released")
    for rid, r in state["releases"].items():
        print(f"{rid:4} {r['state']:10} {r['auc']:<7} "
              f"{r['p95_latency_ms']:<7} {r['error_rate_pct']:<6} "
              f"{r['released_at']}")
    print(f"\nserving: {state['current']}")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    state = load()
    if args.release not in state["releases"]:
        raise SystemExit(f"no such release: {args.release}")
    print(json.dumps(state["releases"][args.release], indent=2))
    return 0


def cmd_decide(args: argparse.Namespace) -> int:
    state = load()
    rid = args.release
    if rid not in state["releases"]:
        raise SystemExit(f"no such release: {rid}")
    if not args.reason or len(args.reason) < 10:
        raise SystemExit("a decision needs a real reason "
                         '(--reason "at least a sentence")')
    if args.rollback:
        previous = [k for k, v in state["releases"].items()
                    if v["state"] == "superseded"]
        if not previous:
            raise SystemExit("no previous release to roll back to")
        back_to = previous[-1]
        state["releases"][rid]["state"] = "rolled_back"
        state["releases"][back_to]["state"] = "current"
        state["current"] = back_to
        save(state)
        log({"at": now(), "action": "rollback", "from": rid, "to": back_to,
             "by": "student", "reason": args.reason})
        print(f"rolled back {rid} -> {back_to}; restart the serving process "
              "to load it")
    else:
        state["releases"][rid]["state"] = "kept"
        save(state)
        log({"at": now(), "action": "keep", "release": rid, "by": "student",
             "reason": args.reason})
        print(f"{rid} kept as-is; decision recorded")
    return 0


def cmd_history(_: argparse.Namespace) -> int:
    if not HISTORY.exists():
        print("no decisions recorded yet")
        return 0
    for line in HISTORY.read_text(encoding="utf-8").splitlines():
        print("  ".join(f"{k}={v}" for k, v in json.loads(line).items()))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python runs_ledger.py")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list").set_defaults(fn=cmd_list)
    p = sub.add_parser("show")
    p.add_argument("release")
    p.set_defaults(fn=cmd_show)
    p = sub.add_parser("decide")
    p.add_argument("release")
    p.add_argument("--rollback", action="store_true")
    p.add_argument("--reason", default="")
    p.set_defaults(fn=cmd_decide)
    sub.add_parser("history").set_defaults(fn=cmd_history)
    args = parser.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())