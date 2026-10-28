"""LAB 13 fixture — code that worked in 2023 and crashes in this environment.

    python legacy_numpy_code.py        # crashes (that IS the exercise)
    python -m pytest test_compat.py -v # the red test students start from

The dependency story: this module was written against numpy 1.x, where
`np.float` still existed (deprecated 1.20, removed in 1.24). The
environment it now runs in has numpy 2.5.3 — installed versions are
printed by `python -m pip show numpy`. Automated tests catch the
incompatibility the moment they run: that is the lab's point — *tests,
not luck, find dependency breakage*.
"""

from __future__ import annotations

import numpy as np

VERSION_TARGET = "numpy>=1.20,<1.24   (where np.float still exists)"


def bucket_charge(value: float) -> str:
    """Legacy helper: bucket a charge onto a float boundary."""
    # Broken under numpy >= 1.24: np.float was removed.
    boundary = np.float(75.0)
    return "high" if np.float(value) >= boundary else "low"


def summarise(values: list[float]) -> dict:
    array = np.array(values, dtype=np.float64)
    return {
        "mean": float(np.mean(array)),
        "median": float(np.median(array)),
        "buckets": [bucket_charge(v) for v in values],
    }


def main() -> int:
    print(f"needs: {VERSION_TARGET}")
    print(f"installed: numpy {np.__version__}")
    print(summarise([40.0, 85.0, 75.0, 120.0]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())