"""Entry point for the refactored pipeline (Module 03).

    python run.py

Prints the numbers the legacy notebook printed, from one command that anyone
can run in a clean checkout.
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from pipeline import (
    add_features,
    churn_rate,
    fit_and_score,
    load_config,
    load_data,
    split,
)

ROOT = pathlib.Path(__file__).parent
# The dataset is generated one level up by generate_data.py — nothing is duplicated.
DATA = ROOT.parent / "data" / "raw" / "churn.csv"


def main() -> None:
    config = load_config(ROOT / "config.yaml")
    frame = add_features(load_data(DATA))
    frame["target"] = frame["churn"]

    print(f"rows:            {len(frame)}")
    print(f"churn rate:      {churn_rate(frame, 'target'):.3f}")
    print(f"contract counts:\n{frame['contract_type'].value_counts().to_string()}")

    x_train, x_test, y_train, y_test = split(frame, config)
    accuracy = fit_and_score(x_train, x_test, y_train, y_test, config)
    print(f"test size:       {config['test_size']} (seed {config['seed']})")
    print(f"accuracy:        {accuracy:.4f}")


if __name__ == "__main__":
    main()