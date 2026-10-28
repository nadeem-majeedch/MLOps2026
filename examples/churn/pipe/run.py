"""Pipeline runner (Module 08): dependency resolution, incremental
execution, failure handling, and an auditable manifest.

    python -m pipe.run              # run (skips stages that are up to date)
    python -m pipe.run --list       # show the DAG
    python -m pipe.run --force      # re-run every stage
    python -m pipe.run --clean      # delete outputs, then run everything
    python -m pipe.run --from train # force one stage (and everything downstream)

Exit code 0 = every stage green; 1 = a stage failed (rerun the same command
to resume: finished stages are skipped, the failed one retries).
"""

from __future__ import annotations

import argparse
import hashlib
import inspect
import json
import pathlib
import shutil
import sys
import time
from datetime import datetime, timezone

from pipe import stages

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "pipe_out"
MANIFEST = OUT / "manifest.json"

# name -> (depends-on, inputs, outputs, function)
TASKS: dict[str, tuple[list[str], list[str], list[str], callable]] = {
    "generate": (
        [],
        [],
        ["data/raw/churn.csv"],
        stages.generate,
    ),
    "validate": (
        ["generate"],
        ["data/raw/churn.csv", "config.yaml"],
        ["pipe_out/validate.json"],
        stages.validate,
    ),
    "features": (
        ["validate"],
        ["pipe_out/validate.json", "config.yaml"],
        ["pipe_out/features.csv"],
        stages.features,
    ),
    "train": (
        ["features"],
        ["pipe_out/features.csv", "config.yaml"],
        ["pipe_out/model.joblib", "pipe_out/train_metrics.json"],
        stages.train,
    ),
    "evaluate": (
        ["train"],
        ["pipe_out/model.joblib", "pipe_out/train_metrics.json", "config.yaml"],
        ["pipe_out/evaluation.json"],
        stages.evaluate,
    ),
    "report": (
        ["evaluate"],
        ["pipe_out/evaluation.json", "pipe_out/train_metrics.json"],
        ["pipe_out/report.md"],
        stages.report,
    ),
}


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def code_hash(fn) -> str:
    """Hash of the stage's own source: change the code, re-run the stage."""
    src = inspect.getsource(fn).encode()
    return hashlib.sha256(src).hexdigest()[:16]


def order() -> list[str]:
    """Topological order of the declared DAG (raises on cycles/unknown deps)."""
    seen: set[str] = set()
    visiting: set[str] = set()
    result: list[str] = []

    def visit(name: str) -> None:
        if name in seen:
            return
        if name in visiting:
            raise SystemExit(f"cycle in the dependency graph at '{name}'")
        if name not in TASKS:
            raise SystemExit(f"unknown task '{name}'")
        visiting.add(name)
        for dep in TASKS[name][0]:
            visit(dep)
        visiting.discard(name)
        seen.add(name)
        result.append(name)

    for name in TASKS:
        visit(name)
    return result


def load_manifest() -> dict:
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {}


def save_manifest(manifest: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def signature(name: str) -> dict:
    """Everything a stage depends on: input files, its own code, and the
    exact bytes of its outputs (so hand-edited or deleted outputs count as
    "changed", just like a changed input)."""
    _deps, inputs, outputs, fn = TASKS[name]
    sig = {
        "inputs": {
            p: sha256(ROOT / p) for p in inputs if (ROOT / p).exists()
        },
        "code": code_hash(fn),
        "outputs": {
            p: sha256(ROOT / p) for p in outputs if (ROOT / p).exists()
        },
    }
    return sig


def up_to_date(name: str, manifest: dict) -> bool:
    prev = manifest.get(name)
    if not prev or prev.get("status") != "success":
        return False
    if not all((ROOT / p).exists() for p in TASKS[name][2]):
        return False          # a missing output means the stage must re-run
    return prev.get("signature") == signature(name)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the churn pipeline DAG")
    parser.add_argument("--list", action="store_true", help="show the DAG and exit")
    parser.add_argument("--force", action="store_true", help="re-run every stage")
    parser.add_argument("--clean", action="store_true", help="delete pipe_out first")
    parser.add_argument(
        "--from", dest="start", metavar="STAGE",
        help="force this stage (and let downstream re-run as inputs change)",
    )
    args = parser.parse_args()

    plan = order()

    if args.list:
        for i, name in enumerate(plan, 1):
            deps, inputs, outputs, _ = TASKS[name]
            print(f"{i}. {name:9} <- {', '.join(deps) or '(entry)'}")
            for p in inputs:
                print(f"      in : {p}")
            for p in outputs:
                print(f"      out: {p}")
        return 0

    if args.clean and OUT.exists():
        shutil.rmtree(OUT)
        print(f"removed {OUT.relative_to(ROOT)}/")

    manifest = load_manifest()
    if args.start:
        if args.start not in TASKS:
            print(f"unknown stage '{args.start}'", file=sys.stderr)
            return 1
        # force this stage to re-run
        manifest.pop(args.start, None)

    failures: list[str] = []
    print(f"pipeline: {' -> '.join(plan)}\n")
    for i, name in enumerate(plan, 1):
        if not failures and not args.force and up_to_date(name, manifest):
            print(f"[{i}/{len(plan)}] {name:9} SKIP  (up to date)")
            continue

        started = time.time()
        print(f"[{i}/{len(plan)}] {name:9} RUN   ...", end="", flush=True)
        try:
            TASKS[name][3]()
            duration = round(time.time() - started, 2)
            manifest[name] = {
                "status": "success",
                "finished_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "duration_s": duration,
                "signature": signature(name),
            }
            save_manifest(manifest)
            print(f" ok ({duration}s)")
        except SystemExit as exc:          # a gate that refused the data
            duration = round(time.time() - started, 2)
            manifest[name] = {
                "status": "failed",
                "finished_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "duration_s": duration,
                "error": str(exc),
            }
            save_manifest(manifest)
            print(f" FAILED: {exc}")
            failures.append(name)
        except Exception as exc:           # an unexpected crash
            duration = round(time.time() - started, 2)
            manifest[name] = {
                "status": "failed",
                "finished_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "duration_s": duration,
                "error": f"{type(exc).__name__}: {exc}",
            }
            save_manifest(manifest)
            print(f" FAILED: {type(exc).__name__}: {exc}")
            failures.append(name)

        if failures:
            # downstream stages must not run on a broken upstream
            for skipped in plan[i:]:
                print(f"[{i + plan[i:].index(skipped) + 1}/{len(plan)}] "
                      f"{skipped:9} BLOCKED (upstream '{name}' failed)")
            break

    if failures:
        print(f"\npipeline FAILED at '{failures[0]}' - "
              "rerun the same command to resume from there.")
        return 1
    print("\npipeline complete - see pipe_out/report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())