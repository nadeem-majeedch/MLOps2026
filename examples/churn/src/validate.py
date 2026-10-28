"""Data validation for the churn dataset (Module 04).

Checks are written in plain pandas on purpose: the *principle* — declare the
expectations your data must satisfy, then fail loudly when they are violated —
is what matters. pandera and Great Expectations are tools that express the same
principle with less boilerplate; see concepts.md.

    python -m src.validate --data data/raw/churn.csv

Exit code 0 = every check passed, 1 = at least one failed.
"""

from __future__ import annotations

import argparse
import sys

import pandas as pd

REQUIRED_COLUMNS = [
    "customer_id",
    "tenure_months",
    "monthly_charges",
    "contract_type",
    "support_tickets",
    "churn",
]
NUMERIC_COLUMNS = ["tenure_months", "monthly_charges", "support_tickets", "churn"]
ALLOWED_CONTRACTS = {"monthly", "one_year", "two_year"}


def run_checks(df: pd.DataFrame) -> list[dict]:
    """Return one result per check: {name, ok, detail}."""
    results: list[dict] = []

    def check(name: str, ok: bool, detail: str) -> None:
        results.append({"name": name, "ok": bool(ok), "detail": detail})

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    check("required_columns", not missing, f"missing columns: {missing or 'none'}")
    if missing:
        return results  # everything else would be guesswork

    non_numeric = [
        c
        for c in NUMERIC_COLUMNS
        if c in df and not pd.api.types.is_numeric_dtype(df[c])
    ]
    check("column_types", not non_numeric, f"non-numeric columns: {non_numeric or 'none'}")

    nulls = df[REQUIRED_COLUMNS].isna().sum()
    nulls = nulls[nulls > 0]
    check(
        "no_missing_values",
        nulls.empty,
        "columns with nulls: "
        + (", ".join(f"{c}={n}" for c, n in nulls.items()) if len(nulls) else "none"),
    )

    dupes = int(df["customer_id"].duplicated().sum())
    check("unique_customer_id", dupes == 0, f"duplicate keys: {dupes}")

    in_range = bool((df["tenure_months"] >= 0).all() and (df["monthly_charges"] > 0).all())
    check("value_ranges", in_range, "tenure_months >= 0 and monthly_charges > 0")

    bad_contracts = sorted(set(df["contract_type"].unique()) - ALLOWED_CONTRACTS)
    check(
        "allowed_contract_types",
        not bad_contracts,
        f"unexpected values: {bad_contracts or 'none'}",
    )

    target_ok = set(df["churn"].unique()) <= {0, 1}
    rate = float(df["churn"].mean())
    check(
        "target_sane",
        target_ok and 0.02 <= rate <= 0.50,
        f"target values ok={target_ok}, positive rate={rate:.3f} (accept 0.02..0.50)",
    )
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the churn dataset")
    parser.add_argument("--data", required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.data)
    results = run_checks(df)
    print(f"file: {args.data}   rows={len(df)}   checks={len(results)}\n")
    for r in results:
        mark = "PASS" if r["ok"] else "FAIL"
        print(f"  [{mark}] {r['name']:<24} {r['detail']}")

    failed = [r for r in results if not r["ok"]]
    print(f"\n{len(results) - len(failed)}/{len(results)} checks passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()