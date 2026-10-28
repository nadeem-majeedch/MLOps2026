"""Training, evaluation, fairness audit, tracking (Modules 05/06/07/14/15).

    python -m src.train --config config.yaml --data data/support.csv

What it does, in order (the anti-leakage discipline):
  1. split train / validation / test (seeded, stratified);
  2. fit baseline AND challenger on train;
  3. compare both on VALIDATION, pick the winner, freeze the threshold;
  4. evaluate the winner on TEST exactly once;
  5. audit fairness across the configured group;
  6. write artifacts/, append a run to runs.jsonl (experiment tracking).

Outputs:
  artifacts/model.joblib   artifacts/metrics.json   artifacts/fairness.json
  artifacts/evaluation.json  runs.jsonl
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
from datetime import UTC, datetime

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline

from src import features as F

ROOT = pathlib.Path(__file__).resolve().parent.parent
ARTIFACTS = ROOT / "artifacts"
RUNS = ROOT / "runs.jsonl"


def build_model(config: dict, family: str):
    m = config["model"]
    if family == "logistic":
        return LogisticRegression(
            C=m["C"], max_iter=m["max_iter"], random_state=config["seed"]
        )
    if family == "gradient_boosting":
        return GradientBoostingClassifier(
            n_estimators=m["n_estimators"], learning_rate=m["learning_rate"],
            max_depth=m["max_depth"], random_state=config["seed"],
        )
    raise ValueError(f"unknown model family: {family!r}")


def score(pipeline, x: pd.DataFrame, y: pd.Series, threshold: float) -> dict:
    proba = pipeline.predict_proba(x)[:, 1]
    pred = (proba >= threshold).astype(int)
    return {
        "roc_auc": round(float(roc_auc_score(y, proba)), 4),
        "accuracy": round(float(accuracy_score(y, pred)), 4),
        "precision": round(float(precision_score(y, pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y, pred)), 4),
        "f1": round(float(f1_score(y, pred, zero_division=0)), 4),
    }, proba, pred


def fairness_audit(
    x: pd.DataFrame, pred: np.ndarray, group: str, max_gap: float
) -> dict:
    rates = {}
    for value in sorted(x[group].unique()):
        mask = x[group] == value
        rates[str(value)] = round(float(pred[mask].mean()), 4)
    gap = round(abs(max(rates.values()) - min(rates.values())), 4)
    return {
        "group": group,
        "selection_rate_by_group": rates,
        "selection_rate_gap": gap,
        "max_allowed_gap": max_gap,
        "within_target": bool(gap <= max_gap),
        "caveat": "Selection-rate parity is ONE fairness definition; a gap "
                  "over target is a prompt to investigate, not proof of bias.",
    }


def append_run(record: dict) -> None:
    RUNS.open("a", encoding="utf-8").write(json.dumps(record) + "\n")


def train(config_path: str, data_path: str, families: list[str] | None = None) -> dict:
    config = F.load_config(config_path)
    df = F.load_data(data_path)
    x, y = F.split_xy(df, config)
    x_train, x_val, x_test, y_train, y_val, y_test = F.train_val_test_split(
        x, y, config
    )
    families = families or [config["model"]["family"], config["model"]["challenger"]]

    # --- stage 3: compare on VALIDATION only (AUC is threshold-free) ----
    candidates: dict = {}
    val_table: dict = {}
    for family in families:
        pipe = Pipeline(
            [("prep", F.build_preprocessor(config)), ("model", build_model(config, family))]
        )
        pipe.fit(x_train, y_train)
        proba = pipe.predict_proba(x_val)[:, 1]
        val_table[family] = {
            "roc_auc": round(float(roc_auc_score(y_val, proba)), 4)
        }
        candidates[family] = pipe

    winner = max(val_table, key=lambda f: val_table[f]["roc_auc"])
    pipeline = candidates[winner]

    # --- freeze the operating point on VALIDATION -----------------------
    configured = config["model"]["threshold"]
    if configured == "auto":
        val_proba = pipeline.predict_proba(x_val)[:, 1]
        best_f1, threshold = -1.0, 0.5
        for candidate in np.arange(0.05, 0.95, 0.05):
            preds = (val_proba >= candidate).astype(int)
            f1 = f1_score(y_val, preds, zero_division=0)
            if f1 > best_f1 + 1e-9:
                best_f1, threshold = float(f1), round(float(candidate), 2)
    else:
        threshold = float(configured)

    # --- stage 4: TEST touched exactly once -----------------------------
    test_metrics, _, test_pred = score(pipeline, x_test, y_test, threshold)

    # --- stage 5: fairness audit on the test split ----------------------
    fairness = fairness_audit(
        x_test, test_pred, config["fairness"]["audit_group"],
        float(config["fairness"]["max_selection_rate_gap"]),
    )

    # --- gate -----------------------------------------------------------
    floor = float(config["quality"]["roc_auc_floor"])
    evaluation = {
        "roc_auc": test_metrics["roc_auc"],
        "floor": floor,
        "passed": bool(test_metrics["roc_auc"] >= floor),
        "by": "roc_auc >= floor on the single held-out test split",
    }

    # --- persist --------------------------------------------------------
    ARTIFACTS.mkdir(exist_ok=True)
    joblib.dump(pipeline, ARTIFACTS / "model.joblib")
    data_sha = hashlib.sha256(pathlib.Path(data_path).read_bytes()).hexdigest()[:16]
    metrics = {
        **test_metrics,
        "winner": winner,
        "threshold": threshold,
        "n_train": len(x_train),
        "n_val": len(x_val),
        "n_test": len(x_test),
        "seed": config["seed"],
        "validation_by_family": val_table,
        "data_sha256": data_sha,
    }
    (ARTIFACTS / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    (ARTIFACTS / "fairness.json").write_text(json.dumps(fairness, indent=2), encoding="utf-8")
    (ARTIFACTS / "evaluation.json").write_text(json.dumps(evaluation, indent=2), encoding="utf-8")

    append_run({
        "run_id": datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ"),
        "at": datetime.now(UTC).isoformat(timespec="seconds"),
        "data_sha256": data_sha,
        "params": {k: config["model"][k] for k in
                   ("family", "challenger", "C", "threshold")},
        "validation_by_family": val_table,
        "test_metrics": test_metrics,
        "gate_passed": evaluation["passed"],
    })
    return metrics


def main() -> int:
    parser = argparse.ArgumentParser(description="Train the support model")
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--data", default="data/support.csv")
    args = parser.parse_args()

    metrics = train(args.config, args.data)
    print(json.dumps({k: v for k, v in metrics.items()
                      if k not in ("validation_by_family",)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())