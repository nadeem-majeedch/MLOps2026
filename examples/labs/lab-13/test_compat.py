"""LAB 13 — the red test that finds the incompatibility.

    python -m pytest test_compat.py -v      # FAILS as shipped (expected!)

The failure you see is the diagnosis raw material: read the traceback,
note WHICH symbol broke and WHERE it was removed, then fix the code (not
the test) and make this suite green.
"""

from __future__ import annotations

import legacy_numpy_code as legacy


def test_bucket_charge_runs_on_a_modern_stack():
    assert legacy.bucket_charge(85.0) == "high"
    assert legacy.bucket_charge(40.0) == "low"


def test_summarise_is_numeric():
    summary = legacy.summarise([40.0, 85.0, 75.0])
    assert summary["mean"] > 0
    assert len(summary["buckets"]) == 3