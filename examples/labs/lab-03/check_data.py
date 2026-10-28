"""LAB 03 fixture — the data gate you finish. Runs today, catches little.

    python check_data.py                 # reads ../data/customers_dirty.csv
    python check_data.py --csv PATH      # any extract
    python check_data.py --strict        # exit 1 when any ERROR is found

Two checks are implemented as worked examples. Four are yours to write
(the spec below tells you exactly what must be caught). Today's output on
the dirty extract is the "before" you must improve on — the lab's
acceptance criteria name every defect class the finished gate must find.
"""

from __future__ import annotations

import argparse
import pathlib
import sys

import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
DEFAULT_CSV = HERE.parent / "data" / "customers_dirty.csv"
EXPECTED_COLUMNS = ["customer_id", "tenure_months", "monthly_charges",
                    "promo_flag", "contract_type", "churned"]
# NOTE the expected schema already reflects the *current* source contract:
# `support_calls` is gone and `promo_flag` arrived (the change that broke
# last month's pipeline). Students decide whether that is a finding.


def check_missing(df: pd.DataFrame) -> list[str]:
    """IMPLEMENTED (example 1): empty/NaN cells in any column."""
    findings = []
    for col in df.columns:
        n_missing = int(df[col].isna().sum())
        if n_missing:
            findings.append(f"ERROR missing: {n_missing} empty values in {col!r}")
    return findings


def check_ranges(df: pd.DataFrame) -> list[str]:
    """IMPLEMENTED (example 2): numeric columns must sit in sane bounds."""
    findings = []
    bounds = {"tenure_months": (0, 120), "monthly_charges": (0, 500)}
    for col, (lo, hi) in bounds.items():
        values = pd.to_numeric(df[col], errors="coerce")
        bad = int(((values < lo) | (values > hi)).sum())
        unparseable = int(values.isna().sum() - df[col].isna().sum())
        if bad:
            findings.append(f"ERROR range: {bad} values of {col!r} outside [{lo}, {hi}]")
        if unparseable > 0:
            findings.append(f"ERROR dtype: {unparseable} non-numeric values in {col!r}")
    return findings


def check_duplicates(df: pd.DataFrame) -> list[str]:
    """YOURS: duplicate customer_id rows AND fully duplicated records."""
    raise NotImplementedError("student task: duplicate detection")


def check_label_domain(df: pd.DataFrame) -> list[str]:
    """YOURS: churned must be exactly {0, 1} — nothing else."""
    raise NotImplementedError("student task: label domain check")


def check_schema(df: pd.DataFrame) -> list[str]:
    """YOURS: columns must match EXPECTED_COLUMNS exactly (names + order)."""
    raise NotImplementedError("student task: schema contract check")


def check_cardinality(df: pd.DataFrame) -> list[str]:
    """YOURS: contract_type must be one of the three known values."""
    raise NotImplementedError("student task: categorical domain check")


CHECKS = [check_missing, check_ranges, check_duplicates,
          check_label_domain, check_schema, check_cardinality]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="lab 03 data gate")
    parser.add_argument("--csv", default=str(DEFAULT_CSV))
    parser.add_argument("--strict", action="store_true",
                        help="exit 1 if any ERROR was reported")
    args = parser.parse_args(argv)

    try:
        df = pd.read_csv(args.csv)
    except Exception as exc:  # unreadable file is itself a finding
        print(f"FATAL cannot read {args.csv}: {exc}")
        return 2

    print(f"rows={len(df)} cols={list(df.columns)}")
    errors, skipped = 0, 0
    for check in CHECKS:
        name = check.__name__
        try:
            findings = check(df)
        except NotImplementedError as exc:
            skipped += 1
            print(f"[NOT IMPLEMENTED] {name}: {exc}")
            continue
        for line in findings:
            errors += line.startswith("ERROR")
            print(f"[{name}] {line}")

    print(f"\n{errors} error(s), {skipped} check(s) not implemented")
    if args.strict and (errors or skipped):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())