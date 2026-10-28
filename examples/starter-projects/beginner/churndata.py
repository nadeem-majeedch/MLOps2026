"""Deterministic synthetic churn data for the BEGINNER starter project.

    python churndata.py            # writes data/customers.csv (500 rows)

Everything is generated from a fixed seed, so two runs produce the same
file — the same property the course's reproducibility labs exercise.
No real personal data: IDs are synthetic (BGN-0001 …).
"""

from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE / "data" / "customers.csv"
SEED = 20261101
ROWS = 500
COLUMNS = ["customer_id", "tenure_months", "monthly_charges",
           "support_calls", "contract_type", "churned"]


def generate(rows: int = ROWS, seed: int = SEED) -> pd.DataFrame:
    """Build the dataset. Pure function: same arguments -> same frame."""
    rng = np.random.default_rng(seed)
    tenure = rng.integers(1, 60, rows)
    charges = np.round(rng.normal(70, 25, rows).clip(15, 160), 2)
    calls = rng.integers(0, 10, rows)
    contract = rng.choice(["monthly", "one_year", "two_year"], rows,
                          p=[0.5, 0.3, 0.2])
    logits = (-0.04 * tenure - 0.03 * calls + 0.012 * (charges - 70)
              + np.where(contract == "monthly", 0.8, -0.3))
    churned = (logits + rng.normal(0, 0.9, rows) > 0).astype(int)
    return pd.DataFrame({
        "customer_id": [f"BGN-{i:04d}" for i in range(1, rows + 1)],
        "tenure_months": tenure,
        "monthly_charges": charges,
        "support_calls": calls,
        "contract_type": contract,
        "churned": churned,
    })


def save(df: pd.DataFrame, path: pathlib.Path = DATA) -> pathlib.Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path


def load(path: pathlib.Path = DATA) -> pd.DataFrame:
    """Load the dataset, generating it first if it does not exist yet."""
    if not path.exists():
        save(generate(), path)
    return pd.read_csv(path)


def main() -> None:
    path = save(generate())
    print(f"wrote {path.relative_to(HERE)} ({ROWS} rows, seed {SEED})")


if __name__ == "__main__":
    main()
