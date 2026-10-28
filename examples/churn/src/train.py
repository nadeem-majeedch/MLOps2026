"""Train and evaluate the churn model (Modules 05 and 06).

Run from the project folder:

    python -m src.train --config config.yaml --data data/raw/churn.csv

What it guarantees:

* everything that affects the result comes from `config.yaml`
* the seed is fixed, so two runs on the same data produce the same metrics
* the fitted pipeline (preprocessing + model) is saved as one object, so the
  exact transform used in training is the one used in serving
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline

from .features import build_preprocessor, load_config, load_data, split_data, split_xy


def build_model(config: dict, family: str | None = None):
    """Build the configured model. `family` lets an experiment override the config
    without editing it — that is how a baseline/challenger comparison is run."""
    family = family or config["model"]["family"]

    if family == "logistic":
        from sklearn.linear_model import LogisticRegression

        return LogisticRegression(
            random_state=config["seed"],
            C=config["model"]["C"],
            max_iter=config["model"]["max_iter"],
        )

    if family == "gradient_boosting":
        return GradientBoostingClassifier(
            random_state=config["seed"],
            n_estimators=config["model"]["n_estimators"],
            learning_rate=config["model"]["learning_rate"],
            max_depth=config["model"]["max_depth"],
        )

    raise ValueError(f"unknown model family: {family!r}")


def train(config_path: str, data_path: str, family: str | None = None) -> tuple[dict, Pipeline]:
    """Train, evaluate, persist. Returns (metrics, fitted_pipeline).

    The fitted pipeline is returned (not just saved) so experiment code can log
    the exact object that produced the numbers — artefacts must match metrics.
    """
    config = load_config(config_path)
    df = load_data(data_path)
    x, y = split_xy(df, config)
    x_train, x_test, y_train, y_test = split_data(x, y, config)

    pipeline = Pipeline(
        steps=[
            ("preprocess", build_preprocessor(config)),
            ("model", build_model(config, family=family)),
        ]
    )
    pipeline.fit(x_train, y_train)

    proba = pipeline.predict_proba(x_test)[:, 1]
    pred = (proba >= 0.5).astype(int)
    metrics = {
        "model_family": family or config["model"]["family"],
        "accuracy": round(float(accuracy_score(y_test, pred)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, proba)), 4),
        "f1": round(float(f1_score(y_test, pred)), 4),
        "positive_rate_test": round(float(y_test.mean()), 4),
        "n_train": len(x_train),
        "n_test": len(x_test),
        "seed": config["seed"],
    }

    out = Path(config["output"]["model_path"])
    out.parent.mkdir(parents=True, exist_ok=True)
    import joblib

    joblib.dump(pipeline, out)
    metrics_path = Path(config["output"]["metrics_path"])
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics, pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Train the churn model")
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--data", default="data/raw/churn.csv")
    parser.add_argument("--family", default=None, help="override model.family from the config")
    args = parser.parse_args()

    metrics, _pipeline = train(args.config, args.data, family=args.family)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()