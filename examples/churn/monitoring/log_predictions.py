"""Stage 1 - prediction logging (Module 14).

    python -m monitoring.log_predictions --scenario baseline --labels
    python -m monitoring.log_predictions --scenario shift
    python -m monitoring.log_predictions --scenario degrade --labels

Appends one JSON line per scored customer to monitoring/predictions.jsonl.

Scenarios (all synthetic, clearly labelled in every record):
  baseline  real training extract, honest retrospective scoring
  shift     features drift (charges +12%, contract mix, more tickets)
            but the churn RULE is unchanged -> ranking should survive
  degrade   features drift AND the churn rule changed -> ranking breaks

`--labels` marks that ground truth has arrived (in production labels are
delayed; a record without `actual` cannot say anything about accuracy).
"""

from __future__ import annotations

import argparse
import json
import pathlib
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from service.model import FEATURES, resolve_model

ROOT = pathlib.Path(__file__).resolve().parent.parent
MON = ROOT / "monitoring"
RAW = ROOT / "data" / "raw" / "churn.csv"
LOG = MON / "predictions.jsonl"

CONTRACTS = ["monthly", "one_year", "two_year"]
CONTRACT_EFFECT = {"monthly": 0.9, "one_year": 0.2, "two_year": -0.3}


def churn_rule(df: pd.DataFrame) -> np.ndarray:
    """The synthetic world's TRUE rule (same formula as generate_data.py)."""
    effect = np.array([CONTRACT_EFFECT[c] for c in df["contract_type"]])
    logit = (
        -2.2
        + 0.035 * (df["monthly_charges"] - 65.0)
        + 0.25 * df["support_tickets"]
        - 0.03 * df["tenure_months"]
        + effect
    )
    rng = np.random.default_rng(7)
    return (rng.uniform(size=len(df)) < 1.0 / (1.0 + np.exp(-logit))).astype(int)


def broken_rule(df: pd.DataFrame, rng: np.random.Generator) -> np.ndarray:
    """A changed world: contract no longer protects, charges barely matter."""
    logit = -1.5 + 0.10 * df["support_tickets"] - 0.01 * df["tenure_months"]
    noise = rng.normal(0, 1.8, size=len(df))
    return (rng.uniform(size=len(df)) < 1.0 / (1.0 + np.exp(-(logit + noise)))).astype(int)


def build_window(scenario: str, n: int = 400, seed: int = 99) -> pd.DataFrame:
    base = pd.read_csv(RAW)
    window = base.sample(n=n, random_state=seed).reset_index(drop=True)

    if scenario == "baseline":
        return window

    rng = np.random.default_rng(seed)
    # --- the world changes: distribution shift -------------------------
    shifted = window.copy()
    shifted["monthly_charges"] = (
        shifted["monthly_charges"] * 1.12 + rng.normal(0, 4, n)
    ).round(2)
    shifted["support_tickets"] = np.clip(
        shifted["support_tickets"] + rng.poisson(1.0, n), 0, 50
    )
    shifted["contract_type"] = rng.choice(CONTRACTS, size=n, p=[0.75, 0.15, 0.10])

    if scenario == "shift":
        # same churn rule, new distribution: labels follow the new features
        shifted["churn"] = churn_rule(shifted)
        return shifted

    if scenario == "degrade":
        # the rule itself changed too (a competitor's promotion worked)
        shifted["churn"] = broken_rule(shifted, rng)
        return shifted

    raise SystemExit(f"unknown scenario: {scenario!r}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Score a window and log it")
    parser.add_argument("--scenario", required=True,
                        choices=["baseline", "shift", "degrade"])
    parser.add_argument("--labels", action="store_true",
                        help="ground truth has arrived for this window")
    parser.add_argument("--append", action="store_true",
                        help="append instead of replacing the log")
    args = parser.parse_args()

    window = build_window(args.scenario)
    state = resolve_model()
    if state["model"] is None:
        raise SystemExit("no model: run `python -m pipe.run` first")

    frame = window[list(FEATURES["numeric"]) + list(FEATURES["categorical"])]
    proba = state["model"].predict_proba(frame)[:, 1]

    MON.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    mode = "a" if args.append or LOG.exists() and args.scenario != "baseline" else "w"
    if args.scenario == "baseline" and not args.append:
        mode = "w"                        # a new baseline replaces old records

    written = 0
    with LOG.open(mode, encoding="utf-8") as fh:
        for i, row in window.iterrows():
            record = {
                "ts": ts,
                "scenario": args.scenario,
                "customer_id": row["customer_id"],
                "tenure_months": int(row["tenure_months"]),
                "monthly_charges": float(row["monthly_charges"]),
                "support_tickets": int(row["support_tickets"]),
                "contract_type": row["contract_type"],
                "churn_probability": round(float(proba[i]), 4),
                "churn_pred": int(proba[i] >= 0.5),
                "model_version": state["version"],
                "actual": int(row["churn"]) if args.labels else None,
            }
            fh.write(json.dumps(record) + "\n")
            written += 1

    print(f"logged {written} predictions  scenario={args.scenario}  "
          f"labels={'yes' if args.labels else 'not yet'}  -> monitoring/predictions.jsonl")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())