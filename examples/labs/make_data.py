"""Deterministic synthetic datasets for the laboratory collection.

    python make_data.py            # write every dataset into ./data
    python make_data.py --check    # regenerate and verify byte-identical output

Datasets (all synthetic — no real personal data, free to redistribute):

  customers_clean.csv    600 rows, healthy schema   (labs 04, 05, 06, 08,
                                                      09, 10, 12, 14, 16, 18)
  customers_dirty.csv    same shape + seeded defects (lab 03):
                             - missing values (NaN / empty strings)
                             - invalid ranges (negative, absurd magnitudes)
                             - exact duplicate rows
                             - schema drift (one column removed, one added)
  customers_shifted.csv  distribution-shifted window (lab 17):
                             charges and support_calls moved deliberately

Determinism: fixed seed, fixed row order, fixed float formatting — two runs
produce byte-identical files (that property is itself lab 04's subject).
"""

from __future__ import annotations

import argparse
import hashlib
import pathlib

import numpy as np
import pandas as pd

SEED = 20261026
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "data"
N = 600
COLUMNS = ["customer_id", "tenure_months", "monthly_charges",
           "support_calls", "contract_type", "churned"]


def base_frame() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    tenure = rng.integers(1, 72, N)
    charges = np.round(rng.normal(70, 25, N).clip(15, 160), 2)
    calls = rng.integers(0, 12, N)
    contract = rng.choice(["monthly", "one_year", "two_year"], N,
                          p=[0.5, 0.3, 0.2])
    # target: honest signal + a little noise (synthetic, obviously)
    logits = -0.04 * tenure - 0.035 * calls + 0.012 * (charges - 70) \
        + np.where(contract == "monthly", 0.8, -0.3)
    churned = (logits + rng.normal(0, 0.9, N) > 0).astype(int)
    return pd.DataFrame({
        "customer_id": [f"CUST-{i:04d}" for i in range(1, N + 1)],
        "tenure_months": tenure,
        "monthly_charges": charges,
        "support_calls": calls,
        "contract_type": contract,
        "churned": churned,
    })


def make_clean() -> pd.DataFrame:
    return base_frame()


def make_dirty(clean: pd.DataFrame) -> pd.DataFrame:
    """Same table, five seeded defect classes (lab 03's audit target)."""
    df = clean.copy()

    # 1. missing values — both flavours (NaN and empty string)
    df.loc[[7, 19, 42], "monthly_charges"] = np.nan
    df.loc[[11, 55], "contract_type"] = ""

    # 2. invalid ranges / absurd magnitudes
    df.loc[3, "tenure_months"] = -5                 # impossible: negative tenure
    df.loc[21, "monthly_charges"] = 99999.0         # impossible: magnitude
    df.loc[30, "churned"] = 7                       # impossible: label outside {0,1}

    # 3. exact duplicate records (including the id!)
    dupes = df.loc[[4, 5, 6]]
    df = pd.concat([df, dupes], ignore_index=True)

    # 4. schema drift: `support_calls` vanished, `promo_flag` appeared
    #    (this is what a source-system change looks like on Monday morning)
    df = df.drop(columns=["support_calls"])
    df.insert(3, "promo_flag", 0)
    df.loc[[8, 13, 21], "promo_flag"] = 1

    # 5. dtype drift: a numeric column arrives as text with units
    df["monthly_charges"] = df["monthly_charges"].astype(object)
    df.loc[60, "monthly_charges"] = "72.50 USD"

    return df


def make_shifted(clean: pd.DataFrame) -> pd.DataFrame:
    """Distribution-shifted window for drift labs (PSI >> thresholds)."""
    rng = np.random.default_rng(SEED + 1)
    df = clean.copy()
    df["monthly_charges"] = (df["monthly_charges"]
                             + rng.normal(18, 6, len(df))).clip(15, 200).round(2)
    df["support_calls"] = (df["support_calls"]
                           + rng.poisson(3, len(df))).clip(0, 30)
    df["tenure_months"] = (df["tenure_months"]
                           - rng.integers(0, 8, len(df))).clip(1, 72)
    # a new contract appears that the model never saw
    mask = rng.random(len(df)) < 0.15
    df.loc[mask, "contract_type"] = "prepaid"
    return df


def write_all() -> dict[str, str]:
    OUT.mkdir(exist_ok=True)
    clean = make_clean()
    frames = {
        "customers_clean.csv": clean,
        "customers_dirty.csv": make_dirty(clean),
        "customers_shifted.csv": make_shifted(clean),
    }
    digests: dict[str, str] = {}
    for name, frame in frames.items():
        path = OUT / name
        frame.to_csv(path, index=False, lineterminator="\n")
        digests[name] = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
    return digests


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="lab datasets")
    parser.add_argument("--check", action="store_true",
                        help="regenerate twice and verify byte-identical output")
    args = parser.parse_args(argv)

    if args.check:
        first = write_all()
        second = write_all()
        same = first == second
        for name, digest in first.items():
            print(f"{name:26} {digest}  {'OK' if first[name] == second[name] else 'DIFFERS'}")
        print("byte-identical across runs: " + ("YES" if same else "NO"))
        return 0 if same else 1

    for name, digest in write_all().items():
        print(f"wrote data/{name}  (sha16 {digest})")
    print("all synthetic, seeded — no personal data")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())