"""LAB 15 fixture — release validation with a hole in it.

    python gate_lab.py candidate_good.json       # passes (it should)
    python gate_lab.py candidate_defective.json   # ...should FAIL, does it?

The validation exists, the criteria are written down, and the code checks
the wrong one(s). Two candidate files ship with the fixture; the defective
candidate is *defective in one dimension only* (read both JSON files and
the criteria below before running).

Your task: make the gate enforce EVERY release criterion from
release_criteria.json — then demonstrate both candidates behaving
correctly, and add the regression test that keeps the hole closed.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
CRITERIA = HERE / "release_criteria.json"


def load(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate(candidate: dict, criteria: dict) -> tuple[bool, list[str]]:
    """Return (allowed, findings).

    BUG: only ONE of the criteria is consulted — the others are read from
    the file but never compared. (Which one is checked? Run the defective
    candidate and infer it.)
    """
    findings = []

    if candidate["roc_auc"] >= criteria["min_roc_auc"]:
        findings.append(f"roc_auc {candidate['roc_auc']} >= "
                        f"{criteria['min_roc_auc']}")
    else:
        findings.append(f"roc_auc {candidate['roc_auc']} < "
                        f"{criteria['min_roc_auc']}  <-- below floor")

    # The remaining criteria — present in the file, absent from the logic:
    #   min_recall, max_drift_psi, tests_green, data_contract_ok
    # ...students wire them up (lab.md step 4).

    allowed = candidate["roc_auc"] >= criteria["min_roc_auc"]
    return allowed, findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="lab 15 release gate")
    parser.add_argument("candidate")
    args = parser.parse_args(argv)

    candidate = load(pathlib.Path(args.candidate))
    criteria = load(CRITERIA)
    allowed, findings = evaluate(candidate, criteria)

    print(f"candidate: {candidate['name']}  ({candidate['note']})")
    for line in findings:
        print(f"  {line}")
    if allowed:
        print("VERDICT: PASS — approved for release")
        return 0
    print("VERDICT: REFUSED — must not ship")
    return 1


if __name__ == "__main__":
    sys.exit(main())