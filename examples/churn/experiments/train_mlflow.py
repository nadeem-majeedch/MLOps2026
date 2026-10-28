"""Train the churn model with MLflow tracking (Module 06).

    python -m experiments.train_mlflow --config config.yaml --data data/raw/churn.csv

Every run is recorded locally: parameters, metrics, the model file, and the
experiment name. Nothing leaves your machine — this is the fully local,
no-account path.

*Tracking backend:* MLflow 3.x no longer accepts the old plain-folder
(`./mlruns`) file store, so this script uses a local SQLite database
(`mlflow.db`). Still 100% local, still no account — SQLite is part of Python's
ecosystem and needs no server.
"""

from __future__ import annotations

import argparse

import mlflow
import mlflow.sklearn

from src.features import load_config
from src.train import train


def main() -> None:
    parser = argparse.ArgumentParser(description="Train with MLflow tracking")
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--data", default="data/raw/churn.csv")
    parser.add_argument("--run-name", default=None)
    parser.add_argument("--family", default=None, help="override model.family (e.g. gradient_boosting)")
    args = parser.parse_args()

    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("churn-baseline")

    with mlflow.start_run(run_name=args.run_name) as run:
        metrics, pipeline = train(args.config, args.data, family=args.family)
        config = load_config(args.config)

        mlflow.log_params(
            {
                "model_family": metrics["model_family"],
                "seed": config["seed"],
                "test_size": config["test_size"],
                "n_train": metrics["n_train"],
                "n_test": metrics["n_test"],
            }
        )
        mlflow.log_metrics(
            {
                "accuracy": metrics["accuracy"],
                "roc_auc": metrics["roc_auc"],
                "f1": metrics["f1"],
            }
        )
        mlflow.log_artifact(args.config)
        mlflow.sklearn.log_model(pipeline, name="churn-model")

        print(f"run_id:   {run.info.run_id}")
        print("uri:      sqlite:///mlflow.db")
        print(f"metrics:  {metrics}")


if __name__ == "__main__":
    main()