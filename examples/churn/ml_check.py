"""Lightweight ML validation (Modules 08/12) — the check CI runs.

    python ml_check.py          # exit 0 = safe to release, exit 1 = blocked

Two gates, both cheap enough to run on every push:
  1. the data contract on the training extract (reuses src.validate),
  2. the quality floor on the recorded training metrics (config quality.*).

Nothing here trains a model: CI validates, it does not retrain.
"""

from __future__ import annotations

import json
import pathlib
import sys

from src import features as F
from src import validate as V

ROOT = pathlib.Path(__file__).parent
DATA = ROOT / "data" / "raw" / "churn.csv"
METRICS = ROOT / "artifacts" / "metrics.json"


def main() -> int:
    problems: list[str] = []

    # --- gate 1: data contract ---------------------------------------
    if not DATA.exists():
        problems.append(f"missing training extract: {DATA.name}")
    else:
        import pandas as pd

        checks = V.run_checks(pd.read_csv(DATA))
        for c in checks:
            if not c.get("ok"):
                problems.append(f"data check failed: {c['name']}")
        print(f"data contract: {sum(1 for c in checks if c.get('ok'))}"
              f"/{len(checks)} checks passed")

    # --- gate 2: quality floor ----------------------------------------
    cfg = F.load_config(ROOT / "config.yaml")
    floor = float(cfg.get("quality", {}).get("roc_auc_floor", 0.0))
    if not METRICS.exists():
        problems.append("missing artifacts/metrics.json (run: python -m pipe.run)")
    else:
        metrics = json.loads(METRICS.read_text(encoding="utf-8"))
        auc = metrics.get("roc_auc", 0.0)
        print(f"quality floor: roc_auc {auc} >= {floor} ?", "yes" if auc >= floor else "NO")
        if auc < floor:
            problems.append(f"roc_auc {auc} is below the floor {floor}")

    if problems:
        print("\nML VALIDATION FAILED")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("\nML VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())