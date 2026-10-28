"""LAB 20 fixture — inject and restore a fault in the capstone system.

    python inject_fault.py --list
    python inject_fault.py --fault data        # break the dataset
    python inject_fault.py --fault model        # corrupt the model bytes
    python inject_fault.py --restore           # put everything back

Operates on ../../capstone-support with timestamped backups, so the shared
reference project is never permanently touched:

  data   -> truncates data/support.csv AND renames one column, so the
            data contract (python -m src.validate) refuses it loudly
  model  -> truncates artifacts/model.joblib to 70% (an interrupted copy);
            loading must refuse it — see lab 20 for why tests won't

The incident exercise (lab 20) runs the fault, watches the system's OWN
tooling detect it (pipeline gate / service load / tests), recovers with
--restore, and proves the recovery by re-running the checks.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import shutil
import time

HERE = pathlib.Path(__file__).resolve().parent
CAPSTONE = HERE.parent.parent / "capstone-support"
BACKUP = HERE / "backup"
TARGETS = {
    "data": CAPSTONE / "data" / "support.csv",
    "model": CAPSTONE / "artifacts" / "model.joblib",
}
STATE = HERE / "injected_state.json"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="lab 20 fault injector")
    parser.add_argument("--fault", choices=sorted(TARGETS))
    parser.add_argument("--restore", action="store_true")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args(argv)

    if args.list:
        for name, path in TARGETS.items():
            exists = "present" if path.exists() else "MISSING"
            print(f"{name:6} -> {path.relative_to(CAPSTONE)} ({exists})")
        print("after injecting: run the detection path named in lab.md")
        return 0

    if args.restore:
        if not STATE.exists():
            raise SystemExit("nothing recorded as injected "
                             "(python inject_fault.py --list)")
        state = json.loads(STATE.read_text(encoding="utf-8"))
        for name, backup_name in state.items():
            shutil.copy2(BACKUP / backup_name, TARGETS[name])
            print(f"restored {name} <- backup/{backup_name}")
        STATE.unlink()
        print("restore complete — re-run the checks to prove recovery")
        return 0

    if not args.fault:
        parser.error("choose --fault {data,model} or --restore")

    target = TARGETS[args.fault]
    if not target.exists():
        raise SystemExit(f"missing target: {target} (run the capstone "
                         "`python generate_data.py && python pipeline.py`)")

    BACKUP.mkdir(exist_ok=True)
    backup_name = f"{args.fault}.bak.{int(time.time())}"
    shutil.copy2(target, BACKUP / backup_name)

    if args.fault == "data":
        lines = target.read_text(encoding="utf-8").splitlines(keepends=True)
        # keep the header, drop 40% of the rows, AND rename one column so the
        # data contract has something concrete to refuse (row loss alone would
        # silently pass every current check — see lab 20 reflection Q2).
        cut = max(2, int(len(lines) * 0.6))
        kept = [lines[0]] + lines[1:cut]
        kept[0] = kept[0].replace("attendance_rate", "attendance_rate_v2", 1)
        target.write_text("".join(kept), encoding="utf-8")
        print(f"data fault: support.csv truncated to {cut - 1} rows and "
              "column 'attendance_rate' renamed to 'attendance_rate_v2'")
    else:
        # Interrupted copy: a truncated file. Appended or mid-file garbage can
        # still load (joblib ignores trailing bytes) — verified during authoring —
        # while a truncation reliably makes joblib.load raise EOFError.
        blob = target.read_bytes()
        cut = int(len(blob) * 0.7)
        target.write_bytes(blob[:cut])
        print(f"model fault: artifacts/model.joblib truncated {len(blob)} -> "
              f"{cut} bytes (interrupted copy)")

    state = json.loads(STATE.read_text(encoding="utf-8")) \
        if STATE.exists() else {}
    state[args.fault] = backup_name
    STATE.write_text(json.dumps(state, indent=2), encoding="utf-8")
    print(f"backup -> backup/{backup_name}   restore with --restore")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())