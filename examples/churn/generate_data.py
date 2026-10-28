"""Generate the synthetic Lahore Retail Co. churn dataset.

Deterministic by design: the same seed always produces byte-identical files.
Run it from this folder:

    python generate_data.py

Outputs (all synthetic, CC0):
    data/raw/churn.csv            the good dataset used by every later module
    data/raw/churn_day2.csv       the next day's extract (same distribution)
    data/corrupt/missing.csv      seeded defect: values missing in a column
    data/corrupt/bad_types.csv    seeded defect: numbers stored as text
    data/corrupt/duplicates.csv   seeded defect: duplicated customer keys
"""

from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd

SEED = 20261025
ROWS = 2_000

ROOT = pathlib.Path(__file__).parent
RAW = ROOT / "data" / "raw"
CORRUPT = ROOT / "data" / "corrupt"

CONTRACTS = ["monthly", "one_year", "two_year"]


def build_frame(seed: int = SEED, rows: int = ROWS) -> pd.DataFrame:
    """Build one synthetic customer table. Pure function: same input, same output."""
    rng = np.random.default_rng(seed)

    tenure = rng.integers(1, 72, size=rows)                 # months
    monthly = rng.normal(65.0, 20.0, size=rows).round(2)    # PKR-thousands per month
    monthly = np.clip(monthly, 15.0, 150.0)
    contract = rng.choice(CONTRACTS, size=rows, p=[0.5, 0.3, 0.2])
    tickets = rng.poisson(1.2, size=rows)                   # support calls / month

    # Latent churn propensity — a plain, documented formula, not magic.
    contract_effect = np.array(
        [{"monthly": 0.9, "one_year": 0.2, "two_year": -0.3}[c] for c in contract]
    )
    logit = (
        -2.2
        + 0.035 * (monthly - 65.0)
        + 0.25 * tickets
        - 0.03 * tenure
        + contract_effect
    )
    churn = (rng.uniform(size=rows) < 1.0 / (1.0 + np.exp(-logit))).astype(int)

    return pd.DataFrame(
        {
            "customer_id": [f"C{100000 + i}" for i in range(rows)],
            "tenure_months": tenure,
            "monthly_charges": monthly,
            "contract_type": contract,
            "support_tickets": tickets,
            "churn": churn,
        }
    )


def write_defects(df: pd.DataFrame) -> None:
    """Write three broken extracts used by the Module 04 validation lab."""

    missing = df.copy()
    missing.loc[missing.index[:120], "monthly_charges"] = np.nan      # 6% missing
    missing.to_csv(CORRUPT / "missing.csv", index=False)

    bad_types = df.copy()
    bad_types["monthly_charges"] = bad_types["monthly_charges"].map(
        lambda v: f"{v:,.2f}"                                        # text, with commas
    )
    bad_types.loc[bad_types.index[:15], "monthly_charges"] = "n/a"
    bad_types.to_csv(CORRUPT / "bad_types.csv", index=False)

    dupes = pd.concat([df, df.iloc[:75]], ignore_index=True)          # 75 duplicate keys
    dupes.to_csv(CORRUPT / "duplicates.csv", index=False)


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    CORRUPT.mkdir(parents=True, exist_ok=True)

    df = build_frame()
    df.to_csv(RAW / "churn.csv", index=False)

    build_frame(seed=SEED + 1).to_csv(RAW / "churn_day2.csv", index=False)
    write_defects(df)

    print(f"rows written: {len(df)}")
    print(f"churn rate:   {df['churn'].mean():.3f}")
    for path in sorted(RAW.glob("*.csv")) + sorted(CORRUPT.glob("*.csv")):
        size = path.stat().st_size
        print(f"  {path.relative_to(ROOT)}  ({size:,} bytes)")


if __name__ == "__main__":
    main()