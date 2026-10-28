"""End-to-end capstone pipeline (Modules 08 + 17).

    python pipeline.py           # generate -> validate -> train -> gate -> report
    python pipeline.py --list    # show the stages
    python pipeline.py --clean   # delete generated state, rebuild everything

Exit 0 = every stage green (gate passed); 1 = a stage failed. Each stage prints
RUN/OK/FAILED so the transcript doubles as evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import shutil
import sys
import time

ROOT = pathlib.Path(__file__).parent
ART = ROOT / "artifacts"
DATA = ROOT / "data" / "support.csv"


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def stage_generate() -> None:
    if not DATA.exists():
        import generate_data
        generate_data.main()


def stage_validate() -> None:
    import pandas as pd

    from src import features as F
    from src.validate import run_checks

    config = F.load_config(ROOT / "config.yaml")
    failed = [c for c in run_checks(pd.read_csv(DATA), config) if not c["ok"]]
    if failed:
        raise SystemExit("data contract violated: "
                         + ", ".join(c["name"] for c in failed))


def stage_train() -> None:
    from src.train import train

    metrics = train(str(ROOT / "config.yaml"), str(DATA))
    if not metrics:
        raise SystemExit("training produced no metrics")


def stage_gate() -> None:
    evaluation = json.loads((ART / "evaluation.json").read_text(encoding="utf-8"))
    if not evaluation["passed"]:
        raise SystemExit(
            f"quality gate failed: roc_auc {evaluation['roc_auc']} "
            f"< floor {evaluation['floor']}"
        )


def stage_report() -> None:
    metrics = json.loads((ART / "metrics.json").read_text(encoding="utf-8"))
    evaluation = json.loads((ART / "evaluation.json").read_text(encoding="utf-8"))
    fairness = json.loads((ART / "fairness.json").read_text(encoding="utf-8"))
    text = f"""# Capstone pipeline report

**Gate:** {'PASS' if evaluation['passed'] else 'FAIL'}
(roc_auc {evaluation['roc_auc']} vs floor {evaluation['floor']})

## Model selection (validation only; test touched once)

| family | validation roc_auc |
|---|---|
{chr(10).join(f"| {f} | {m['roc_auc']} |" for f, m in metrics['validation_by_family'].items())}

**Winner:** {metrics['winner']} · operating point threshold={metrics['threshold']}

## Test metrics (single pass)

| metric | value |
|---|---|
| roc_auc | {metrics['roc_auc']} |
| accuracy | {metrics['accuracy']} |
| precision | {metrics['precision']} |
| recall | {metrics['recall']} |
| f1 | {metrics['f1']} |

## Fairness audit ({fairness['group']})

| group value | selection rate |
|---|---|
{chr(10).join(f"| {k} | {v} |" for k, v in fairness['selection_rate_by_group'].items())}

**Gap {fairness['selection_rate_gap']} (target ≤ {fairness['max_allowed_gap']}) —**
**{"within target" if fairness['within_target'] else "OVER TARGET: investigate and document before release"}**

## Artefacts

| file | sha256[0:16] |
|---|---|
{chr(10).join(f"| `{p.name}` | `{sha256(p)}` |" for p in sorted(ART.glob('*.json'))) + chr(10) + f"| `model.joblib` | `{sha256(ART / 'model.joblib')}` |"}
"""
    (ROOT / "report.md").write_text(text, encoding="utf-8")


STAGES = [
    ("generate", stage_generate),
    ("validate", stage_validate),
    ("train", stage_train),
    ("gate", stage_gate),
    ("report", stage_report),
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the capstone pipeline")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--clean", action="store_true",
                        help="delete generated state first")
    args = parser.parse_args()

    if args.list:
        for i, (name, _) in enumerate(STAGES, 1):
            print(f"{i}. {name}")
        return 0

    if args.clean:
        for target in ("artifacts", "pipe_out", "release.json", "releases",
                       "monitoring_out", "report.md"):
            path = ROOT / target
            if path.is_dir():
                shutil.rmtree(path)
            elif path.exists():
                path.unlink()
        print("cleaned generated state (data/ and runs.jsonl kept)")

    print(f"pipeline: {' -> '.join(n for n, _ in STAGES)}\n")
    failed = False
    for i, (name, fn) in enumerate(STAGES, 1):
        if failed:
            print(f"[{i}/{len(STAGES)}] {name:9} BLOCKED")
            continue
        started = time.time()
        print(f"[{i}/{len(STAGES)}] {name:9} RUN ...", end="", flush=True)
        try:
            fn()
            print(f" ok ({time.time() - started:.2f}s)")
        except SystemExit as exc:
            print(f" FAILED: {exc}")
            failed = True
        except Exception as exc:  # noqa: BLE001 - report any crash uniformly
            print(f" FAILED: {type(exc).__name__}: {exc}")
            failed = True

    if failed:
        print("\npipeline FAILED - fix the stage above, then rerun.")
        return 1
    print(f"\npipeline complete - see report.md "
          f"(data sha {sha256(DATA)}, metrics {sha256(ART / 'metrics.json')})")
    return 0


if __name__ == "__main__":
    sys.exit(main())