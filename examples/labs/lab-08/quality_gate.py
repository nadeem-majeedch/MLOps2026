"""LAB 08 fixture — a quality gate that lets the wrong model through.

    python quality_gate.py good_metrics.json     # expected: PASS (exit 0)
    python quality_gate.py bad_metrics.json      # expected: REFUSE (exit 1)
                                                   ...does it?

The gate reads the floor from gate_config.json and compares it against
the run's metrics. Two bugs (one logical, one structural) mean the bad
candidate sails through. Your tasks: write the pytest tests that fail
today, fix the gate, and show the pipeline-style exit codes.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
CONFIG = HERE / "gate_config.json"


def load(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def check(metrics: dict, config: dict) -> tuple[bool, list[str]]:
    findings: list[str] = []
    floor = config["roc_auc_floor"]

    # BUG 1 (logical): the comparison runs the wrong way — read it slowly.
    if metrics["roc_auc"] <= floor:
        findings.append(f"roc_auc {metrics['roc_auc']} <= floor {floor}: OK")
    else:
        findings.append(f"roc_auc {metrics['roc_auc']} > floor {floor}: hmm")

    # BUG 2 (structural): the config holds MORE required criteria than the
    # gate looks at — which ones are silently ignored? (compare the files)
    allowed = metrics["roc_auc"] <= floor
    return allowed, findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="lab 08 quality gate")
    parser.add_argument("metrics")
    args = parser.parse_args(argv)

    metrics = load(pathlib.Path(args.metrics))
    config = load(CONFIG)
    allowed, findings = check(metrics, config)

    print(f"model: {metrics['model']}   ({metrics.get('note', '')})")
    for line in findings:
        print(f"  {line}")
    if allowed:
        print("GATE: PASS — artefacts accepted for the next stage")
        return 0
    print("GATE: FAIL — pipeline stops here")
    return 1


if __name__ == "__main__":
    sys.exit(main())