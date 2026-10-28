"""Dataset generation and validation — the intermediate starter's data
contract.

    df = generate()                 # 800 synthetic rows, fixed seed
    problems = validate(df)         # [] means the contract holds
    validated(df)                   # raises DataValidationError if not

`validate()` is the same idea as the course's data-quality labs: a
dataset either meets a written contract or it is refused — never
"partially accepted with a warning nobody reads".
"""

from __future__ import annotations

import numpy as np
import pandas as pd

SEED = 20261102
ROWS = 800
COLUMNS = ["customer_id", "tenure_months", "monthly_charges",
           "support_calls", "contract_type", "churned"]

# the contract: column -> (type hint, inclusive bounds) for numeric columns
NUMERIC_BOUNDS = {
    "tenure_months": (1, 72),
    "monthly_charges": (15.0, 160.0),
    "support_calls": (0, 20),
}
CATEGORIES = {"contract_type": {"monthly", "one_year", "two_year"}}


class DataValidationError(ValueError):
    """The dataset violates the contract; `problems` says exactly how."""

    def __init__(self, problems: list[str]) -> None:
        self.problems = problems
        super().__init__("data contract violated:\n  - "
                         + "\n  - ".join(problems))


def generate(rows: int = ROWS, seed: int = SEED) -> pd.DataFrame:
    """Pure function: same arguments produce the same frame."""
    rng = np.random.default_rng(seed)
    tenure = rng.integers(1, 72, rows)
    charges = np.round(rng.normal(70, 25, rows).clip(15, 160), 2)
    calls = rng.integers(0, 10, rows)
    contract = rng.choice(["monthly", "one_year", "two_year"], rows,
                          p=[0.5, 0.3, 0.2])
    logits = (-0.04 * tenure - 0.03 * calls + 0.012 * (charges - 70)
              + np.where(contract == "monthly", 0.8, -0.3))
    churned = (logits + rng.normal(0, 0.9, rows) > 0).astype(int)
    return pd.DataFrame({
        "customer_id": [f"INT-{i:04d}" for i in range(1, rows + 1)],
        "tenure_months": tenure,
        "monthly_charges": charges,
        "support_calls": calls,
        "contract_type": contract,
        "churned": churned,
    })


def validate(df: pd.DataFrame) -> list[str]:
    """Return a list of contract violations — empty list means PASS."""
    problems: list[str] = []

    missing = [c for c in COLUMNS if c not in df.columns]
    if missing:
        problems.append(f"required columns missing: {missing}")
        return problems                      # everything else needs them

    extra = [c for c in df.columns if c not in COLUMNS]
    if extra:
        problems.append(f"unexpected columns (schema drift?): {extra}")

    if df.isna().any().any():
        bad = df.columns[df.isna().any()].tolist()
        problems.append(f"null values in columns: {bad}")

    for column, (low, high) in NUMERIC_BOUNDS.items():
        if not pd.api.types.is_numeric_dtype(df[column]):
            problems.append(f"{column}: expected numeric, got "
                            f"{df[column].dtype}")
            continue
        if df[column].min() < low or df[column].max() > high:
            problems.append(
                f"{column}: values outside [{low}, {high}] "
                f"(min={df[column].min()}, max={df[column].max()})")

    for column, allowed in CATEGORIES.items():
        stray = set(df[column].unique()) - allowed
        if stray:
            problems.append(f"{column}: unknown categories {sorted(stray)}")

    duplicates = int(df["customer_id"].duplicated().sum())
    if duplicates:
        problems.append(f"customer_id: {duplicates} duplicate key(s)")

    if not set(df["churned"].unique()) <= {0, 1}:
        problems.append("churned: target must be 0 or 1")
    elif df["churned"].mean() < 0.05 or df["churned"].mean() > 0.95:
        problems.append("churned: target balance outside [5%, 95%] — "
                        "a near-constant target makes metrics meaningless")

    return problems


def validated(df: pd.DataFrame) -> pd.DataFrame:
    """Raise DataValidationError on any violation; return df otherwise."""
    problems = validate(df)
    if problems:
        raise DataValidationError(problems)
    return df
