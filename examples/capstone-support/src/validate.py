"""Data contract for the student-support dataset (Modules 04 + 17).

Run:  python -m src.validate            (exit 0 = contract holds)

Checks are explicit and countable — including the leakage guard: the
forbidden columns may EXIST in the file (they are legitimate for other
purposes) but the configured feature list must never reference them.
"""

from __future__ import annotations

import argparse
import json
import sys

import pandas as pd

from src import features as F

REQUIRED = [
    "student_ref", "attendance_rate", "prior_score", "lms_logins",
    "missed_assessments", "assignment_rate", "device_access",
    "term_end_flag", "at_risk",
]
NUMERIC_RANGES = {
    "attendance_rate": (0.0, 1.0),
    "prior_score": (0, 100),
    "lms_logins": (0, 100),
    "missed_assessments": (0, 30),
    "assignment_rate": (0.0, 1.0),
}


def run_checks(df: pd.DataFrame, config: dict) -> list[dict]:
    checks: list[dict] = []

    def add(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "ok": bool(ok), "detail": detail})

    missing_required = sorted(set(REQUIRED) - set(df.columns))
    add("required_columns", not missing_required,
        f"missing: {missing_required or 'none'} ({len(df.columns)} columns present)")

    feats = config["features"]
    configured = feats["numeric"] + feats["categorical"] + [feats["target"]]
    missing = [c for c in configured if c not in df.columns]
    add("configured_columns_exist", not missing, f"missing: {missing or 'none'}")

    # The guard applies to *features* — the target itself is allowed by name.
    feature_list = feats["numeric"] + feats["categorical"]
    forbidden = set(feats["forbidden"]) & set(feature_list)
    add("no_forbidden_features", not forbidden,
        f"leakage/id columns referenced: {sorted(forbidden) or 'none'}")

    # Only inspect columns that are actually present: a renamed/removed column
    # must show up as a named FAIL above, not crash the validator itself.
    modelled = [c for c in list(NUMERIC_RANGES) + ["at_risk"] if c in df.columns]
    nulls = int(df[modelled].isna().sum().sum()) if modelled else -1
    add("no_nulls_in_key_columns", nulls == 0, f"{nulls} null values")

    range_bad = []
    for col, (lo, hi) in NUMERIC_RANGES.items():
        if col in df.columns and not df[col].between(lo, hi).all():
            range_bad.append(col)
    add("value_ranges", not range_bad, f"out-of-range columns: {range_bad or 'none'}")

    dupes = int(df["student_ref"].duplicated().sum()) if "student_ref" in df else -1
    add("unique_student_ref", dupes == 0, f"{dupes} duplicate ids")

    rate = float(df["at_risk"].mean()) if "at_risk" in df else -1.0
    add("target_rate_sane", 0.02 <= rate <= 0.60, f"at_risk rate = {rate:.3f}")

    # Leakage trap must still BE in the file (the guard is meaningful only
    # when the tempting column is present).
    add("leakage_trap_present_for_testing",
        "term_end_flag" in df.columns,
        "term_end_flag exists to prove the pipeline refuses it")
    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the support dataset")
    parser.add_argument("--data", default="data/support.csv")
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--json", action="store_true", help="print checks as JSON")
    args = parser.parse_args()

    config = F.load_config(args.config)
    df = pd.read_csv(args.data)
    checks = run_checks(df, config)

    if args.json:
        print(json.dumps(checks, indent=2))
    else:
        for c in checks:
            print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']:32} {c['detail']}")
        print(f"\n{sum(1 for c in checks if c['ok'])}/{len(checks)} checks passed")

    return 0 if all(c["ok"] for c in checks) else 1


if __name__ == "__main__":
    sys.exit(main())