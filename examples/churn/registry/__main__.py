"""Registry CLI (Module 09) — see registry/__init__.py for the command list."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import shutil
import sys
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parent.parent
REG = ROOT / "registry_store"
INDEX = REG / "index.json"

STAGES = ("development", "staging", "production", "archived")
# Promotion order: a version may only move forward one step at a time.
ORDER = ["development", "staging", "production"]


# --------------------------------------------------------------- helpers
def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load() -> dict:
    if INDEX.exists():
        return json.loads(INDEX.read_text(encoding="utf-8"))
    return {"versions": {}, "stages": {}, "history": []}


def save(index: dict) -> None:
    REG.mkdir(parents=True, exist_ok=True)
    INDEX.write_text(json.dumps(index, indent=2), encoding="utf-8")


def require_version(index: dict, name: str) -> dict:
    if name not in index["versions"]:
        sys.exit(f"no such version: {name} (try: python -m registry list)")
    return index["versions"][name]


def next_id(index: dict) -> str:
    n = len(index["versions"]) + 1
    while f"v{n:03d}" in index["versions"]:
        n += 1
    return f"v{n:03d}"


# ------------------------------------------------------------- commands
def cmd_register(args: argparse.Namespace) -> int:
    index = load()
    model = pathlib.Path(args.model)
    metrics_path = pathlib.Path(args.metrics)
    data = pathlib.Path(args.data)

    for p, what in ((model, "model"), (metrics_path, "metrics"), (data, "data")):
        if not p.exists():
            sys.exit(f"missing {what} file: {p}")

    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))

    # The quality gate result (Module 08) travels with the version: promotion
    # to production is refused unless this version actually passed it.
    gate = {"passed": None, "source": "no evaluation.json provided"}
    eval_path = pathlib.Path(args.evaluation)
    if eval_path.exists():
        evaluation = json.loads(eval_path.read_text(encoding="utf-8"))
        gate = {"passed": bool(evaluation["passed"]),
                "source": eval_path.name,
                "detail": f"roc_auc {evaluation['roc_auc']} vs floor {evaluation['floor']}"}

    vid = next_id(index)
    vdir = REG / vid
    vdir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(model, vdir / model.name)

    metadata = {
        "id": vid,
        "created_at": now(),
        "stage": "development",
        "note": args.note,
        "model_file": model.name,
        "model_sha256": sha256(model)[:16],
        "data_sha256": sha256(data)[:16],
        "data_file": str(data),
        "metrics": metrics,
        "gate": gate,
        "previous_version": max(index["versions"]) if index["versions"] else None,
    }
    (vdir / "metadata.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )

    index["versions"][vid] = metadata
    index["history"].append(
        {"at": now(), "action": "register", "version": vid, "by": args.by}
    )
    save(index)
    print(f"registered {vid}  model={metadata['model_sha256']}  "
          f"roc_auc={metrics.get('roc_auc')}  gate={gate['passed']}")
    return 0


def cmd_list(_: argparse.Namespace) -> int:
    index = load()
    if not index["versions"]:
        print("registry is empty")
        return 0
    print(f"{'version':9} {'created':21} {'stage':12} {'roc_auc':8} gate   note")
    for vid, m in index["versions"].items():
        print(f"{vid:9} {m['created_at']:21} {m['stage']:12} "
              f"{m['metrics'].get('roc_auc')!s:8} {m['gate']['passed']!s:6} "
              f"{m['note']}")
    print("\nstage pointers:", json.dumps(index["stages"]))
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    index = load()
    print(json.dumps(require_version(index, args.version), indent=2))
    return 0


def cmd_stage(args: argparse.Namespace) -> int:
    index = load()
    meta = require_version(index, args.version)
    target = args.target
    current = meta["stage"]

    if target not in STAGES:
        sys.exit(f"unknown stage {target!r}; choose from {', '.join(STAGES)}")

    # --- approval rule -------------------------------------------------
    if target == "production" and meta["gate"]["passed"] is not True:
        sys.exit(f"refused: {args.version} never passed its quality gate "
                 f"({meta['gate']['source']}) - production requires a passed gate")

    if (target in ORDER and current in ORDER
            and ORDER.index(target) > ORDER.index(current) + 1):
            sys.exit(f"refused: {args.version} is '{current}' and may only move "
                     f"one step at a time (next step: "
                     f"{ORDER[ORDER.index(current) + 1]})")

    previous_production = index["stages"].get("production")
    meta["stage"] = target
    index["stages"][target] = args.version
    if target == "production" and previous_production and previous_production != args.version:
        index["stages"]["previous_production"] = previous_production

    index["history"].append(
        {"at": now(), "action": "stage", "version": args.version,
         "from": current, "to": target, "by": args.by}
    )
    save(index)
    print(f"{args.version}: {current} -> {target}")
    if target == "production" and previous_production:
        print(f"  production was {previous_production} "
              f"(rollback: python -m registry rollback production)")
    return 0


def cmd_rollback(args: argparse.Namespace) -> int:
    index = load()
    stage = args.stage
    current = index["stages"].get(stage)
    if not current:
        sys.exit(f"nothing to roll back: no version is in '{stage}'")
    if stage == "production":
        previous = index["stages"].get("previous_production")
        if not previous:
            sys.exit("no recorded previous production version to roll back to")
        index["stages"]["production"] = previous
        index["stages"]["previous_production"] = current
        # the demoted model returns to staging, like a failed release would
        index["versions"][current]["stage"] = "staging"
        index["versions"][previous]["stage"] = "production"
        action = "rollback"
    else:
        sys.exit(f"rollback implemented for 'production' only (got '{stage}')")

    index["history"].append(
        {"at": now(), "action": action, "stage": stage,
         "from": current, "to": previous, "by": args.by}
    )
    save(index)
    print(f"rollback: {stage} {current} -> {previous}")
    return 0


def cmd_get(args: argparse.Namespace) -> int:
    index = load()
    vid = index["stages"].get(args.stage)
    if not vid:
        sys.exit(f"no version is in stage '{args.stage}'")
    m = index["versions"][vid]
    path = REG / vid / m["model_file"]
    print(path)
    return 0


def cmd_history(_: argparse.Namespace) -> int:
    index = load()
    for entry in index["history"]:
        print("  ".join(f"{k}={v}" for k, v in entry.items()))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m registry",
        description="Local model registry: register, stage, promote, roll back",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("register", help="record a new model version")
    p.add_argument("--model", required=True)
    p.add_argument("--metrics", required=True)
    p.add_argument("--data", default="data/raw/churn.csv")
    p.add_argument("--evaluation", default="pipe_out/evaluation.json")
    p.add_argument("--note", default="")
    p.add_argument("--by", default="student")
    p.set_defaults(fn=cmd_register)

    p = sub.add_parser("list", help="all versions and stage pointers")
    p.set_defaults(fn=cmd_list)

    p = sub.add_parser("show", help="metadata of one version")
    p.add_argument("version")
    p.set_defaults(fn=cmd_show)

    p = sub.add_parser("stage", help="move a version to a stage")
    p.add_argument("version")
    p.add_argument("target", choices=STAGES)
    p.add_argument("--by", default="student")
    p.set_defaults(fn=cmd_stage)

    p = sub.add_parser("rollback", help="revert a stage pointer")
    p.add_argument("stage")
    p.add_argument("--by", default="student")
    p.set_defaults(fn=cmd_rollback)

    p = sub.add_parser("get", help="print the model file path in a stage")
    p.add_argument("stage")
    p.set_defaults(fn=cmd_get)

    p = sub.add_parser("history", help="audit trail of all actions")
    p.set_defaults(fn=cmd_history)

    args = parser.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())