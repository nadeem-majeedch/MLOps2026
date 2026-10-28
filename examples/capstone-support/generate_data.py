"""Generate the synthetic student-support dataset (capstone, Module 17).

    python generate_data.py

**Scenario (public interest):** a college wants an *early-support* flag that
helps counsellors offer help to students who are struggling — not to penalise
anyone. Output: data/support.csv (3,000 rows, synthetic, CC0).

**Ethics & provenance:**
  * Every row is generated from a documented formula with a fixed seed —
    no real student, school, or personal record exists in this file.
  * The synthetic id (`student_ref`) is a bare sequence; there are no names,
    emails, national ids, or free text.
  * `term_end_flag` is a deliberate LEAKAGE TRAP: it is derived from the
    outcome after the term ends. It exists in the CSV so the course can prove
    the pipeline refuses to use it (config + validation + a regression test).

Deterministic: same seed -> byte-identical file (sha256 stable across runs).
"""

from __future__ import annotations

import hashlib
import pathlib

import numpy as np
import pandas as pd

SEED = 20261026
ROWS = 3000
ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "data"


def build_frame(seed: int = SEED, rows: int = ROWS) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    attendance = np.clip(rng.normal(0.87, 0.13, rows), 0.30, 1.0).round(3)
    prior_score = np.clip(rng.normal(68.0, 14.0, rows), 20, 100).round(1)
    lms_logins = np.clip(rng.poisson(7, rows) + 1, 1, 60)
    missed = np.clip(rng.poisson(1.1, rows), 0, 15)
    assignment_rate = np.clip(rng.normal(0.76, 0.19, rows), 0.0, 1.0).round(3)
    device_access = rng.binomial(1, 0.78, rows)   # 1 = reliable device at home

    # Latent support need — a plain, documented formula, not magic.
    effect = (
        -2.6
        + 4.2 * (0.87 - attendance)          # low attendance raises risk
        - 0.040 * (prior_score - 68.0)       # weaker prior results raise risk
        + 0.20 * missed                      # missed assessments raise risk
        - 3.0 * (assignment_rate - 0.76)     # late/missing work raises risk
        + 0.12 * (7 - lms_logins)            # disengagement raises risk
        + 0.55 * (1 - device_access)         # access disadvantage (small effect)
    )
    at_risk = (rng.uniform(size=rows) < 1.0 / (1.0 + np.exp(-effect))).astype(int)

    # LEAKAGE TRAP: known only AFTER the term — never a feature.
    term_end_flag = np.where(
        rng.uniform(size=rows) < (0.92 * at_risk + 0.05 * (1 - at_risk)), 1, 0
    )

    return pd.DataFrame(
        {
            "student_ref": [f"S{100000 + i}" for i in range(rows)],
            "attendance_rate": attendance,
            "prior_score": prior_score,
            "lms_logins": lms_logins.astype(int),
            "missed_assessments": missed.astype(int),
            "assignment_rate": assignment_rate,
            "device_access": device_access.astype(int),
            "term_end_flag": term_end_flag.astype(int),
            "at_risk": at_risk,
        }
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = build_frame()
    path = OUT / "support.csv"
    df.to_csv(path, index=False)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
    print(f"rows written:  {len(df)}")
    print(f"at_risk rate:  {df['at_risk'].mean():.3f}")
    print(f"device_access: {df['device_access'].mean():.3f} have a device")
    print(f"file:          {path.name}  sha256[0:16]={digest}")


if __name__ == "__main__":
    main()