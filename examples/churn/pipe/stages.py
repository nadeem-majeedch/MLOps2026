"""The six pipeline stages (Module 08).

Each stage is a plain function with one job:

    generate -> validate -> features -> train -> evaluate -> report

Rules every stage follows:
  * reads only its declared inputs (config + files produced upstream),
  * writes only its declared outputs,
  * is deterministic: same inputs, byte-identical outputs,
  * raises (fails loudly) rather than returning partial results.
"""

from __future__ import annotations

import hashlib
import json
import pathlib

import joblib
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

import generate_data
from src import features as F
from src import validate as V

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "pipe_out"
CONFIG = ROOT / "config.yaml"
RAW = ROOT / "data" / "raw" / "churn.csv"


def _read_config() -> dict:
    return F.load_config(CONFIG)


def _sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


# ---------------------------------------------------------------- stage 1
def generate() -> None:
    """Create the raw extract (idempotent: same seed, byte-identical file)."""
    if not RAW.exists():
        generate_data.main()


# ---------------------------------------------------------------- stage 2
def validate() -> None:
    """Data contract gate: every check must pass or the stage raises."""
    df = pd.read_csv(RAW)
    checks = V.run_checks(df)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "validate.json").write_text(
        json.dumps(checks, indent=2), encoding="utf-8"
    )
    failed = [c for c in checks if not c.get("ok")]
    if failed:
        names = ", ".join(c["name"] for c in failed)
        raise SystemExit(f"data contract violated: {names}")


# ---------------------------------------------------------------- stage 3
def features() -> None:
    """Turn validated raw data into the modelling table (features + target)."""
    cfg = _read_config()
    df = F.load_data(RAW)
    x, y = F.split_xy(df, cfg)
    table = x.copy()
    table[cfg["features"]["target"]] = y
    table.to_csv(OUT / "features.csv", index=False)


# ---------------------------------------------------------------- stage 4
def train() -> None:
    """Fit the model declared in config and record its hold-out metrics."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import Pipeline

    cfg = _read_config()
    table = pd.read_csv(OUT / "features.csv")
    x = table.drop(columns=[cfg["features"]["target"]])
    y = table[cfg["features"]["target"]]
    x_tr, x_te, y_tr, y_te = train_test_split(
        x, y,
        test_size=cfg["test_size"],
        random_state=cfg["seed"],
        stratify=y,
    )
    pipe = Pipeline(
        [
            ("prep", F.build_preprocessor(cfg)),
            ("clf", LogisticRegression(max_iter=1000, random_state=cfg["seed"])),
        ]
    )
    pipe.fit(x_tr, y_tr)
    proba = pipe.predict_proba(x_te)[:, 1]
    pred = (proba >= 0.5).astype(int)
    metrics = {
        "roc_auc": round(float(roc_auc_score(y_te, proba)), 4),
        "accuracy": round(float(accuracy_score(y_te, pred)), 4),
        "precision": round(float(precision_score(y_te, pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_te, pred)), 4),
        "f1": round(float(f1_score(y_te, pred)), 4),
        "positive_rate_test": round(float(y_te.mean()), 4),
        "n_train": len(x_tr),
        "n_test": len(x_te),
        "seed": cfg["seed"],
    }
    joblib.dump(pipe, OUT / "model.joblib")
    (OUT / "train_metrics.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )


# ---------------------------------------------------------------- stage 5
def evaluate() -> None:
    """Quality gate: the model must beat the floor declared in config."""
    cfg = _read_config()
    floor = float(cfg.get("quality", {}).get("roc_auc_floor", 0.0))
    metrics = json.loads((OUT / "train_metrics.json").read_text(encoding="utf-8"))
    passed = metrics["roc_auc"] >= floor
    evaluation = {
        "roc_auc": metrics["roc_auc"],
        "floor": floor,
        "passed": passed,
        "by": "roc_auc >= floor",
    }
    (OUT / "evaluation.json").write_text(
        json.dumps(evaluation, indent=2), encoding="utf-8"
    )
    if not passed:
        raise SystemExit(
            f"quality gate failed: roc_auc {metrics['roc_auc']} < floor {floor}"
        )


# ---------------------------------------------------------------- stage 6
def report() -> None:
    """Human-readable summary with the hashes of every artefact."""
    metrics = json.loads((OUT / "train_metrics.json").read_text(encoding="utf-8"))
    evaluation = json.loads((OUT / "evaluation.json").read_text(encoding="utf-8"))
    rows = "\n".join(
        f"| {k} | {v} |"
        for k, v in metrics.items()
        if isinstance(v, (int, float))
    )
    artefacts = "\n".join(
        f"| `{p.name}` | `{_sha256(p)}` |"
        for p in sorted(OUT.glob("*"))
        if p.is_file() and p.name != "report.md"
    )
    text = f"""# Pipeline report)

**Gate:** {'PASS' if evaluation['passed'] else 'FAIL'}
(roc_auc {evaluation['roc_auc']} vs floor {evaluation['floor']})

## Metrics

| metric | value |
|---|---|
{rows}

## Artefacts (sha256, first 16 chars)

| file | hash |
|---|---|
{artefacts}
"""
    (OUT / "report.md").write_text(text, encoding="utf-8")