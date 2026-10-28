"""Course secret scanner — Lab 15's deterministic, install-free check.

    python scan_secrets.py flawed          # audit a folder (exit 1 if findings)
    python scan_secrets.py ../churn        # audit a clean folder (exit 0)

Rules (deliberately simple, deliberately explainable):
  * R1  a name containing KEY / SECRET / TOKEN / PASSWORD / CREDENTIAL
        assigned a non-empty string literal;
  * R2  a connection string with inline credentials (scheme://user:pass@host).

This is a teaching scanner: readable, no dependencies, no network. The
industry-standard free alternative is gitleaks (optional, see lab.md step 2)
— it scans *history* and ships far more rules. Neither replaces not
committing secrets in the first place.

Exit codes: 0 = clean, 1 = findings, 2 = bad usage.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SENSITIVE_NAME = re.compile(
    r"\b[A-Z0-9_]*(?:API_KEY|SECRET|TOKEN|PASSWORD|CREDENTIAL)[A-Z0-9_]*\b"
)
ASSIGNMENT = re.compile(
    r"""(?P<name>[A-Z0-9_]+)\s*=\s*(?P<value>["'][^"']{7,}["'])"""
)
INLINE_CREDS = re.compile(r"\b[a-z][a-z0-9+.-]*://[^/\s:@]+:[^/\s@]+@")

# Literal values that are self-evidently placeholders (docs, tests).
PLACEHOLDERS = ("example", "unit-test", "changeme", "placeholder", "<your")


def scan_file(path: Path) -> list[str]:
    findings: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return findings
    for number, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith(("#", '"""')):
            continue
        low = stripped.lower()
        if any(p in low for p in PLACEHOLDERS):
            continue
        for match in ASSIGNMENT.finditer(stripped):
            if SENSITIVE_NAME.search(match.group("name")):
                findings.append(f"{path}:{number}: R1 sensitive assignment "
                                f"{match.group('name')} = {match.group('value')}")
        creds = INLINE_CREDS.search(stripped)
        if creds and not stripped.startswith("#"):
            findings.append(f"{path}:{number}: R2 credentials inside a URL: "
                            f"{creds.group(0)}...")
    return findings


def main(argv: list[str]) -> int:
    roots = [Path(a) for a in argv] or [Path(".")]
    files: list[Path] = []
    for root in roots:
        if root.is_file():
            files.append(root)
        elif root.is_dir():
            files.extend(p for p in sorted(root.rglob("*.py"))
                         if "__pycache__" not in p.parts)
        else:
            print(f"scan_secrets: no such path: {root}", file=sys.stderr)
            return 2

    findings = [f for path in files for f in scan_file(path)]
    for finding in findings:
        print(finding)
    if findings:
        print(f"\n{len(findings)} finding(s) in {len(files)} file(s) - "
              "remove them, rotate the values, and move them to the "
              "environment (lab.md step 2).")
        return 1
    print(f"clean: {len(files)} file(s), no findings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))