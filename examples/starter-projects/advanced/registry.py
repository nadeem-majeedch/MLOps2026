"""Model registry — stage, promote, inspect, roll back.

    python registry.py stage                 # copy artefact -> versions/vNNN
    python registry.py list                  # versions + which one is live
    python registry.py promote v001          # make v001 current (records why)
    python registry.py rollback              # back to the previous version

State lives in `registry.json` next to this file; versions live in
`versions/<id>/`. Every recorded entry keeps the model's sha256, so a
silently-swapped file is detectable (`python registry.py verify`).

This is the *local* pattern from Modules 09/17 — a remote MLflow-style
registry adds server-side permissions and a UI, not different ideas.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import shutil
import sys
from datetime import datetime, timezone

HERE = pathlib.Path(__file__).resolve().parent
ARTIFACTS = HERE / "artifacts"
VERSIONS = HERE / "versions"
STATE = HERE / "registry.json"
FILES = ("model.joblib", "model_info.json")


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"current": None, "previous": None, "versions": {},
            "history": []}


def save_state(state: dict) -> None:
    STATE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def stage(note: str = "") -> str:
    if not (ARTIFACTS / "model.joblib").exists():
        raise SystemExit("no artefact — run `python train.py` first")
    state = load_state()
    number = 1 + max((int(v[1:]) for v in state["versions"]), default=0)
    vid = f"v{number:03d}"
    target = VERSIONS / vid
    target.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        shutil.copy2(ARTIFACTS / name, target / name)
    state["versions"][vid] = {
        "at": now(),
        "note": note or "staged",
        "sha256": sha256(target / "model.joblib"),
        "status": "staged",
    }
    state["history"].append({"at": now(), "action": "stage", "version": vid})
    save_state(state)
    print(f"staged {vid} (sha256 {state['versions'][vid]['sha256'][:16]}…)")
    return vid


def promote(vid: str) -> None:
    state = load_state()
    if vid not in state["versions"]:
        raise SystemExit(f"unknown version: {vid} (python registry.py list)")
    if state["current"]:
        state["versions"][state["current"]]["status"] = "superseded"
    state["previous"] = state["current"]
    state["current"] = vid
    state["versions"][vid]["status"] = "current"
    state["history"].append({"at": now(), "action": "promote", "version": vid})
    save_state(state)
    print(f"promoted {vid} -> current")


def rollback() -> None:
    state = load_state()
    if not state["previous"]:
        raise SystemExit("no previous version to roll back to")
    target, demoted = state["previous"], state["current"]
    promote(target)
    state = load_state()
    state["previous"] = demoted
    state["history"].append({"at": now(), "action": "rollback",
                             "from": demoted, "to": target})
    save_state(state)
    print(f"rolled back {demoted} -> {target}")


def verify() -> int:
    """Hash every staged version against the recorded sha256."""
    state = load_state()
    bad = 0
    for vid, meta in state["versions"].items():
        path = VERSIONS / vid / "model.joblib"
        if not path.exists():
            print(f"{vid}: MISSING file")
            bad += 1
        elif sha256(path) != meta["sha256"]:
            print(f"{vid}: MISMATCH — bytes changed since staging")
            bad += 1
        else:
            print(f"{vid}: ok ({meta['status']})")
    return 1 if bad else 0


def main(argv: list[str]) -> int:
    cmd = argv[0] if argv else "list"
    if cmd == "stage":
        stage(" ".join(argv[1:]) or "")
    elif cmd == "promote":
        if len(argv) < 2:
            raise SystemExit("usage: registry.py promote vNNN")
        promote(argv[1])
    elif cmd == "rollback":
        rollback()
    elif cmd == "verify":
        return verify()
    elif cmd == "list":
        state = load_state()
        if not state["versions"]:
            print("no versions yet — `python registry.py stage`")
        for vid, meta in state["versions"].items():
            live = "  <- current" if vid == state["current"] else ""
            print(f"{vid}  {meta['status']:10} {meta['at']}  "
                  f"{meta['sha256'][:16]}…{live}")
    else:
        raise SystemExit(f"unknown command: {cmd}\n"
                         "usage: registry.py {stage|list|promote|rollback|verify}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
