"""Drift monitor — compare live prediction traffic against a reference window.

    python monitor.py                 # PSI per feature + verdict (exit 0)
    python monitor.py --check         # exit 1 if any feature is "strong"

Inputs (both produced by the starter itself):
  * data/reference.csv    the window the model was validated on
  * logs/predictions.jsonl  what the service has actually scored

PSI (population stability index) is a distribution-distance number:
< 0.10 stable, 0.10–0.20 moderate, > 0.20 strong (thresholds in
config.yaml — the interpretation is a *convention*, not a law).

The course's Module 14 rule stands: **drift is a prompt to investigate,
not proof that accuracy fell.** This tool measures inputs only; it cannot
see labels. Pair it with a labelled performance check before retraining.
"""

from __future__ import annotations

import argparse
import json
import pathlib

import numpy as np
import pandas as pd
import yaml

HERE = pathlib.Path(__file__).resolve().parent
NUMERIC = ["tenure_months", "monthly_charges", "support_calls"]


def load_config(path: pathlib.Path = HERE / "config.yaml") -> dict:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def psi(reference: np.ndarray, current: np.ndarray) -> float:
    """Population Stability Index over deciles of the reference window."""
    edges = np.unique(np.quantile(reference, np.linspace(0, 1, 11)))
    if len(edges) < 3:
        return 0.0
    edges[0], edges[-1] = -np.inf, np.inf
    ref = np.clip(np.histogram(reference, bins=edges)[0].astype(float),
                  1e-4, None)
    cur = np.clip(np.histogram(current, bins=edges)[0].astype(float),
                  1e-4, None)
    ref, cur = ref / ref.sum(), cur / cur.sum()
    return float(np.sum((cur - ref) * np.log(cur / ref)))


def load_traffic(config: dict) -> pd.DataFrame | None:
    log = HERE / config["monitoring"]["log"]
    if not log.exists():
        return None
    rows = [json.loads(line) for line in log.read_text("utf-8").splitlines()
            if line.strip()]
    return pd.DataFrame(rows) if rows else None


def report(config: dict) -> tuple[list[tuple[str, float, str]], str]:
    reference = pd.read_csv(HERE / config["monitoring"]["reference"])
    traffic = load_traffic(config)
    if traffic is None or not set(NUMERIC) <= set(traffic.columns):
        return [], "no traffic yet — score some records first (/predict)"

    strong = float(config["monitoring"]["psi_strong"])
    moderate = float(config["monitoring"]["psi_moderate"])
    rows = []
    for column in NUMERIC:
        value = psi(reference[column].to_numpy(float),
                    traffic[column].to_numpy(float))
        verdict = ("strong" if value >= strong
                   else "moderate" if value >= moderate else "stable")
        rows.append((column, round(value, 4), verdict))

    any_strong = any(v == "strong" for _, _, v in rows)
    any_moderate = any(v == "moderate" for _, _, v in rows)
    verdict = ("DRIFT DETECTED — investigate before retraining"
               if any_strong else
               "moderate movement — monitor" if any_moderate else
               "stable — no action")
    return rows, verdict


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="advanced starter drift monitor")
    parser.add_argument("--check", action="store_true",
                        help="exit 1 if any feature is in strong drift")
    args = parser.parse_args(argv)

    config = load_config()
    rows, verdict = report(config)
    if not rows:
        print(verdict)
        return 0
    for column, value, state in rows:
        print(f"  {column:18} psi={value:<7} {state}")
    print(f"overall: {verdict}")
    if args.check and any(state == "strong" for _, _, state in rows):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
