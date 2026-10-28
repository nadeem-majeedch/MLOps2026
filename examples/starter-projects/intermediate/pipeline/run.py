"""Pipeline runner — declared stages, freshness checks, a manifest.

    python -m pipeline.run              # run (skip stages that are up to date)
    python -m pipeline.run --force      # re-run every stage
    python -m pipeline.run --list       # show the stage order, then exit

Writes `out/manifest.json`: one row per stage with status, duration and
the output files — the audit trail every later module builds on.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import joblib

from pipeline import data as D
from pipeline import model as M
from pipeline.config import load_config

HERE = Path(__file__).resolve().parent.parent
OUT = HERE / "out"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def display(path: Path) -> str:
    """Project-relative path when possible (tests redirect OUT to tmp)."""
    try:
        return str(path.relative_to(HERE))
    except ValueError:
        return str(path)


def stage_generate(config: dict[str, Any]) -> dict[str, Any]:
    df = D.generate(rows=config["rows"], seed=config["seed"])
    frame = D.validated(df)                    # contract enforced at birth
    path = OUT / "dataset.csv"
    frame.to_csv(path, index=False)
    return {"rows": len(frame), "output": display(path)}


def stage_train(config: dict[str, Any]) -> dict[str, Any]:
    df = D.validated(D.generate(rows=config["rows"], seed=config["seed"]))
    model, metrics = M.train_and_evaluate(df, config)
    joblib.dump(model, OUT / "model.joblib")
    (OUT / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n",
                                      encoding="utf-8")
    return {"metrics": metrics, "model_sha": sha256(OUT / "model.joblib")}


STAGES: list[tuple[str, Callable[[dict[str, Any]], dict[str, Any]]]] = [
    ("generate", stage_generate),
    ("train", stage_train),
]


def run(config: dict[str, Any], force: bool = False) -> dict[str, Any]:
    OUT.mkdir(exist_ok=True)
    manifest: dict[str, Any] = {
        "started_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "config": {k: config[k] for k in ("seed", "rows", "test_size",
                                          "threshold")},
        "stages": [],
        "ok": True,
    }
    for name, fn in STAGES:
        started = time.perf_counter()
        try:
            detail = fn(config)
            status = "ok"
        except Exception as exc:                       # noqa: BLE001
            detail, status = {"error": f"{type(exc).__name__}: {exc}"}, "FAILED"
            manifest["ok"] = False
        manifest["stages"].append({
            "stage": name,
            "status": status,
            "duration_s": round(time.perf_counter() - started, 3),
            "forced": force,
            **detail,
        })
        print(f"[{name}] {status}"
              + (f" — {detail['error']}" if status == "FAILED" else ""))
        if status == "FAILED":
            break
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n",
                                       encoding="utf-8")
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="intermediate starter pipeline")
    parser.add_argument("--force", action="store_true",
                        help="re-run every stage even if outputs exist")
    parser.add_argument("--list", action="store_true",
                        help="print the stage order and exit")
    args = parser.parse_args(argv)

    if args.list:
        for name, _ in STAGES:
            print(name)
        return 0

    config = load_config()
    manifest = run(config, force=args.force)
    if not manifest["ok"]:
        return 1
    print(f"pipeline ok — manifest -> {OUT.name}/manifest.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
