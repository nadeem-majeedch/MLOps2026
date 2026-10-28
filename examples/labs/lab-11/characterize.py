"""LAB 11 fixture — characterise the service with bad requests.

    python characterize.py

Sends 10 requests (no server needed: in-process TestClient) and prints a
table of OBSERVED vs EXPECTED status codes plus the actual bodies where
they disagree. The output below is your diagnosis worksheet — the lab
asks you to explain *each* mismatch before touching the code.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from broken_service import app

client = TestClient(app, raise_server_exceptions=False)

BASE = {"tenure_months": 12, "monthly_charges": 85.0,
        "support_calls": 4, "contract_type": "monthly"}

CASES = [
    ("valid record", "POST", "/predict", {"records": [BASE]}, 200),
    ("missing charges", "POST", "/predict",
     {"records": [{"tenure_months": 12, "contract_type": "monthly"}]}, 422),
    ("negative tenure", "POST", "/predict",
     {"records": [{**BASE, "tenure_months": -3}]}, 422),
    ("charges out of range", "POST", "/predict",
     {"records": [{**BASE, "monthly_charges": -20}]}, 422),
    ("zero tenure (div-by-0)", "POST", "/predict",
     {"records": [{**BASE, "tenure_months": 0}]}, 422),
    ("unknown contract", "POST", "/predict",
     {"records": [{**BASE, "contract_type": "prepaid"}]}, 422),
    ("empty records", "POST", "/predict", {"records": []}, 422),
    ("records not a list", "POST", "/predict", {"records": "yes"}, 422),
    ("no records key", "POST", "/predict", {"rows": []}, 422),
    ("health degraded", "ENV", "/health", None, 503),
]


def run_case(name: str, method: str, path: str, body, expected: int,
             env_degraded: bool = False) -> tuple[str, bool]:
    if env_degraded:
        import os
        os.environ["MODEL_MISSING"] = "1"
    try:
        if method == "POST":
            response = client.post(path, json=body)
        else:
            response = client.get(path)
        observed = response.status_code
        detail = response.text[:90]
    except Exception as exc:                       # client-side exception =
        observed, detail = "EXC", f"{type(exc).__name__}: {exc}"[:90]
    if env_degraded:
        import os
        os.environ.pop("MODEL_MISSING", None)
    ok = observed == expected
    status = "ok " if ok else "FAIL"
    print(f"[{status}] {name:26} expected {expected:>4} observed {observed:>4}"
          + ("" if ok else f"  | {detail}"))
    return name, ok


def main() -> int:
    print("== LAB 11 characterisation ==")
    failures = 0
    for case in CASES:
        name, method, path, body, expected = case
        degraded = name.startswith("health degraded")
        _, ok = run_case(name, method, path, body, expected, degraded)
        failures += not ok
    print(f"\n{failures}/{len(CASES)} mismatches against the HTTP contract.")
    print("Explain every FAIL before you fix anything (lab.md step 3).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())