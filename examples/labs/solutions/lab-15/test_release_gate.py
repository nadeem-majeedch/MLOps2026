"""Regression tests for the LAB-15 release gate (starter — you finish it).

    cd examples/labs/lab-15
    copy ..\\..\\solutions\\lab-15\\test_release_gate.py .      # 🪟
    cp ../../solutions/lab-15/test_release_gate.py .           # 🐧
    python -m pytest test_release_gate.py -q

AS SHIPPED these tests FAIL (that is the hole you are closing).
After lab.md steps 3–4 they must be green — and stay green: the suite is
what stops the gate from silently losing a criterion again.

How it drives the CLI without assuming extra flags: each run copies
`gate_lab.py` into a temp directory next to the criteria file it should
use (the gate resolves `release_criteria.json` relative to its own
file), then runs `python gate_lab.py candidate.json` there. Exit codes
are the contract:

  0 = PASS (approved)   1 = REFUSED (failed a criterion)
  2 = FAIL CLOSED (the gate did not understand its own config)
"""

from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
# Works both where it lives (solutions/lab-15) and after you copy it
# next to the fixture (examples/labs/lab-15).
LAB = HERE if (HERE / "gate_lab.py").exists() \
    else HERE.parent.parent / "lab-15"
GATE = LAB / "gate_lab.py"
CRITERIA = LAB / "release_criteria.json"

GOOD = json.loads((LAB / "candidate_good.json").read_text(encoding="utf-8"))
DEFECTIVE = json.loads(
    (LAB / "candidate_defective.json").read_text(encoding="utf-8"))


def run_gate(candidate: dict, criteria: dict | None = None
             ) -> subprocess.CompletedProcess:
    """Run the gate as a real CLI in an isolated directory."""
    criteria = criteria if criteria is not None else \
        json.loads(CRITERIA.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        shutil.copy2(GATE, td / "gate_lab.py")
        (td / "release_criteria.json").write_text(
            json.dumps(criteria), encoding="utf-8")
        (td / "candidate.json").write_text(json.dumps(candidate),
                                           encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(td / "gate_lab.py"), "candidate.json"],
            capture_output=True, text=True, cwd=td)


def candidate_with(**overrides) -> dict:
    """Start from the good candidate, break exactly ONE dimension."""
    base = {k: v for k, v in GOOD.items() if k != "min_recall_check"}
    base.update(overrides)
    return base


def test_good_candidate_passes():
    r = run_gate(GOOD)
    assert r.returncode == 0, r.stdout + r.stderr


def test_defective_candidate_is_refused():
    """THE bug: as shipped this returns 0 (AUC alone is enough)."""
    r = run_gate(DEFECTIVE)
    assert r.returncode == 1, f"defective candidate was approved:\n{r.stdout}"


def test_low_recall_alone_is_refused():
    r = run_gate(candidate_with(name="low recall", recall=0.05))
    assert r.returncode == 1, r.stdout + r.stderr


def test_strong_drift_alone_is_refused():
    r = run_gate(candidate_with(name="drifty", drift_psi=0.47))
    assert r.returncode == 1, r.stdout + r.stderr


def test_red_tests_alone_are_refused():
    r = run_gate(candidate_with(name="red tests", tests_green=False))
    assert r.returncode == 1, r.stdout + r.stderr


def test_broken_contract_alone_is_refused():
    r = run_gate(candidate_with(name="broken contract",
                                data_contract_ok=False))
    assert r.returncode == 1, r.stdout + r.stderr


def test_unknown_criterion_fails_closed():
    """A criterion the gate cannot check must never be silently skipped."""
    criteria = json.loads(CRITERIA.read_text(encoding="utf-8"))
    criteria["max_latency_ms"] = 300          # new key, unknown to the gate
    r = run_gate(GOOD, criteria=criteria)
    assert r.returncode == 2, \
        f"unknown config key was ignored (expected exit 2):\n{r.stdout}"
    assert "max_latency_ms" in (r.stdout + r.stderr), \
        "the refusal must NAME the unknown key"


def test_findings_name_every_violated_criterion():
    r = run_gate(DEFECTIVE)
    # only the FINDINGS lines count — the candidate's own "note" text
    # (which mentions recall/drift/tests/contract) would fool a naive check
    findings = "\n".join(line for line in r.stdout.splitlines()
                         if line.startswith("  "))
    for word in ("recall", "drift", "tests", "contract"):
        assert word in findings, \
            f"violated criterion never listed in findings: {findings!r}"
