"""LAB 02 fixture — "the notebook export". Runs. Works. Nobody can maintain it.

    python analysis_monolith.py

This file *is* the exercise: a one-shot analysis that grew into production.
Everything is global, logic is copy-pasted per segment, thresholds are
magic numbers, and the same CSV is re-read three times. It runs today —
that is exactly why nobody dares touch it.

Refactor target (your repo, your structure):
    customer_analysis/
      io.py        loading + schema
      features.py  derived columns (ONE implementation)
      report.py    aggregation + rendering
      __main__.py  CLI
    tests/         the behaviour you must not change

Verification: the refactored CLI must reproduce this file's report exactly
(capture it first:  python analysis_monolith.py > baseline_report.txt).
"""

from __future__ import annotations

import pathlib

import pandas as pd

PATH = pathlib.Path(__file__).resolve().parent.parent / "data" / "customers_clean.csv"

df = pd.read_csv(PATH)  # global #1 — and it gets read again below...

# ---- segment 1: monthly customers ------------------------------------
m = df[df["contract_type"] == "monthly"].copy()
m["risk"] = (m["support_calls"] > 3) | (m["tenure_months"] < 6)
monthly_total = len(m)
monthly_risk = int(m["risk"].sum())
monthly_avg_charges = round(float(m["monthly_charges"].mean()), 2)
monthly_churn_rate = round(float(m["churned"].mean()), 3)

# ---- segment 2: one-year customers (copy-paste of segment 1) ---------
df2 = pd.read_csv(PATH)  # global #2, re-read for no reason
o = df2[df2["contract_type"] == "one_year"].copy()
o["risk"] = (o["support_calls"] > 3) | (o["tenure_months"] < 6)  # same rule, again
one_total = len(o)
one_risk = int(o["risk"].sum())
one_avg_charges = round(float(o["monthly_charges"].mean()), 2)
one_churn_rate = round(float(o["churned"].mean()), 3)

# ---- segment 3: two-year customers (copy-paste again) ----------------
df3 = pd.read_csv(PATH)  # global #3
t = df3[df3["contract_type"] == "two_year"].copy()
t["risk"] = (t["support_calls"] > 3) | (t["tenure_months"] < 6)  # and again
two_total = len(t)
two_risk = int(t["risk"].sum())
two_avg_charges = round(float(t["monthly_charges"].mean()), 2)
two_churn_rate = round(float(t["churned"].mean()), 3)

# ---- summary (magic numbers everywhere) ------------------------------
print("== customer risk snapshot ==")
print(f"monthly : n={monthly_total:3d}  risk={monthly_risk:3d} "
      f"({monthly_risk / monthly_total:.1%})  avg={monthly_avg_charges}  "
      f"churn={monthly_churn_rate:.1%}")
print(f"one_year: n={one_total:3d}  risk={one_risk:3d} "
      f"({one_risk / one_total:.1%})  avg={one_avg_charges}  "
      f"churn={one_churn_rate:.1%}")
print(f"two_year: n={two_total:3d}  risk={two_risk:3d} "
      f"({two_risk / two_total:.1%})  avg={two_avg_charges}  "
      f"churn={two_churn_rate:.1%}")

total_risk = monthly_risk + one_risk + two_risk  # "add the copies up"
overall_flagged = total_risk
print(f"flagged for outreach: {overall_flagged} "
      f"({overall_flagged / len(df):.1%} of {len(df)} customers)")

# the number leadership actually asks for, hardcoded from an old email
TARGET_FLAG_PCT = 0.18  # ???
if overall_flagged / len(df) > TARGET_FLAG_PCT:
    print(f"over target ({TARGET_FLAG_PCT:.0%}) — trim the outreach list")
else:
    print(f"within target ({TARGET_FLAG_PCT:.0%})")