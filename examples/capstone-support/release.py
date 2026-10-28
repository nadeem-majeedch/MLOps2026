"""Release management: register, promote, rollback (Modules 09 + 15 + 17).

    python release.py register --note "v1"
    python release.py status
    python release.py promote r001 --ack "fairness gap documented, mitigations agreed"
    python release.py rollback

Governance rules enforced by code:
  * a release can only be promoted if its quality gate passed;
  * if the fairness audit was over target at registration, promotion needs an
    explicit --ack reason, recorded in the history (documented human risk
    acceptance — never silent);
  * rollback restores the previous release and is itself recorded.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import shutil
import sys
from datetime import UTC, datetime

ROOT = pathlib.Path(__file__).parent
ART = ROOT / "artifacts"
REL = ROOT / "releases"
STATE = ROOT / "release.json"


def now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def load() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"releases": {}, "current": None, "previous": None, "history": []}


def save(state: dict) -> None:
    STATE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def cmd_register(args: argparse.Namespace) -> int:
    state = load()
    evaluation = json.loads((ART / "evaluation.json").read_text(encoding="utf-8"))
    fairness = json.loads((ART / "fairness.json").read_text(encoding="utf-8"))
    metrics = json.loads((ART / "metrics.json").read_text(encoding="utf-8"))

    rid = f"r{len(state['releases']) + 1:03d}"
    rdir = REL / rid
    rdir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ART / "model.joblib", rdir / "model.joblib")
    for name in ("metrics.json", "fairness.json", "evaluation.json"):
        shutil.copy2(ART / name, rdir / name)

    record = {
        "id": rid,
        "at": now(),
        "note": args.note,
        "by": args.by,
        "gate": evaluation,
        "fairness_within_target": fairness["within_target"],
        "fairness_gap": fairness["selection_rate_gap"],
        "roc_auc": metrics["roc_auc"],
        "threshold": metrics["threshold"],
        "data_sha256": metrics["data_sha256"],
        "model_sha256": sha256(rdir / "model.joblib")[:16],
    }
    state["releases"][rid] = record
    state["history"].append({"at": now(), "action": "register",
                             "release": rid, "by": args.by})
    save(state)
    print(f"registered {rid}  roc_auc={record['roc_auc']}  "
          f"gate={evaluation['passed']}  fairness_ok={fairness['within_target']}")
    if not fairness["within_target"]:
        print(f"  note: fairness gap {record['fairness_gap']} was OVER target "
              f"at registration - promotion will need --ack")
    return 0


def cmd_promote(args: argparse.Namespace) -> int:
    state = load()
    rid = args.release
    if rid not in state["releases"]:
        sys.exit(f"no such release: {rid} (see: python release.py status)")
    record = state["releases"][rid]

    if not record["gate"]["passed"]:
        sys.exit(f"refused: {rid} never passed its quality gate")
    if not record["fairness_within_target"] and not args.ack:
        sys.exit(f"refused: {rid} has an OVER-TARGET fairness gap "
                 f"({record['fairness_gap']}) - promote with "
                 f'--ack "reason recorded for the risk register"')

    state["previous"] = state["current"]
    state["current"] = rid
    state["history"].append({"at": now(), "action": "promote", "release": rid,
                             "by": args.by, "ack": args.ack})
    save(state)
    print(f"{rid} is now serving (was {state['previous']})")
    if args.ack:
        print(f"  risk acceptance recorded: {args.ack}")
    if state["previous"]:
        print("  rollback: python release.py rollback")
    return 0


def cmd_rollback(_: argparse.Namespace) -> int:
    state = load()
    if not state["previous"]:
        sys.exit("nothing to roll back to (no previous release recorded)")
    old, current = state["previous"], state["current"]
    state["current"], state["previous"] = old, current
    state["history"].append({"at": now(), "action": "rollback",
                             "from": current, "to": old})
    save(state)
    print(f"rollback: serving {old} (was {current}) - restart the API to load it")
    return 0


def cmd_status(_: argparse.Namespace) -> int:
    state = load()
    if not state["releases"]:
        print("no releases yet (python release.py register --note ...)")
        return 0
    print(f"{'release':9} {'registered':21} {'auc':7} {'gate':6} {'fair':7} note")
    for rid, r in state["releases"].items():
        marker = "*" if rid == state["current"] else " "
        print(f"{marker}{rid:8} {r['at']:21} {r['roc_auc']:<7} "
              f"{r['gate']['passed']!s:6} "
              f"{r['fairness_within_target']!s:7} {r['note']}")
    print(f"\nserving: {state['current']}   previous: {state['previous']}")
    return 0


def cmd_history(_: argparse.Namespace) -> int:
    state = load()
    for entry in state["history"]:
        print("  ".join(f"{k}={v}" for k, v in entry.items()))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python release.py")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("register", help="snapshot artifacts as a release")
    p.add_argument("--note", default="")
    p.add_argument("--by", default="student")
    p.set_defaults(fn=cmd_register)

    p = sub.add_parser("status", help="list releases and the serving pointer")
    p.set_defaults(fn=cmd_status)

    p = sub.add_parser("promote", help="make a release serve")
    p.add_argument("release")
    p.add_argument("--ack", default="", help="risk acceptance for over-target fairness")
    p.add_argument("--by", default="student")
    p.set_defaults(fn=cmd_promote)

    p = sub.add_parser("rollback", help="restore the previous release")
    p.set_defaults(fn=cmd_rollback)

    p = sub.add_parser("history", help="audit trail")
    p.set_defaults(fn=cmd_history)

    args = parser.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())