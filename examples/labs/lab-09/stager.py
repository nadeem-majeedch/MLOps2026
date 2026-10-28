"""LAB 09 fixture — release-candidate staging without integrity checking.

    python stager.py stage            # stage candidate rc-1 from build outputs
    python stager.py verify           # "verification" (deliberately weak)
    python stager.py list             # what is staged, and in what state
    python stager.py approve          # declare the RC releasable

The lifecycle works; the integrity story does not. `verify` proves the
files *exist* — nothing proves they are the bytes you staged. The lab's
task: build the tamper-proof version (sha256 recorded at stage time,
re-checked at verify/approve), and demonstrate that a corrupted artifact
is refused BEFORE it can be approved.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import shutil
from datetime import datetime, timezone

HERE = pathlib.Path(__file__).resolve().parent
BUILD = HERE / "build"        # produced by `python prepare_build.py`
STAGED = HERE / "staged"
MANIFEST = STAGED / "manifest.json"


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_manifest() -> dict:
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {"candidates": {}}


def save_manifest(state: dict) -> None:
    STAGED.mkdir(exist_ok=True)
    MANIFEST.write_text(json.dumps(state, indent=2), encoding="utf-8")


def cmd_stage(_: argparse.Namespace) -> int:
    if not BUILD.exists():
        raise SystemExit("no build/ — run `python prepare_build.py` first")
    state = load_manifest()
    rc = "rc-1"
    target = STAGED / rc
    target.mkdir(parents=True, exist_ok=True)
    files = {}
    for path in sorted(BUILD.iterdir()):
        shutil.copy2(path, target / path.name)
        files[path.name] = {"exists": True, "size": path.stat().st_size}
        # ^ "exists" is NOT integrity. that is the hole you close.
    state["candidates"][rc] = {"staged_at": now(), "files": files,
                               "state": "staged"}
    save_manifest(state)
    print(f"staged {rc}: {', '.join(sorted(files))}")
    return 0


def cmd_verify(_: argparse.Namespace) -> int:
    state = load_manifest()
    if not state["candidates"]:
        raise SystemExit("nothing staged (python stager.py stage)")
    for rc, record in state["candidates"].items():
        missing = [name for name in record["files"]
                   if not (STAGED / rc / name).exists()]
        status = "VERIFY OK" if not missing else f"VERIFY FAIL missing={missing}"
        print(f"{rc}: {status}   ({len(record['files'])} file(s))")
    return 0


def cmd_list(_: argparse.Namespace) -> int:
    state = load_manifest()
    if not state["candidates"]:
        print("no release candidates")
        return 0
    for rc, record in state["candidates"].items():
        print(f"{rc}  {record['state']:10} staged_at={record['staged_at']}")
    return 0


def cmd_approve(args: argparse.Namespace) -> int:
    state = load_manifest()
    rc = args.release_candidate
    if rc not in state["candidates"]:
        raise SystemExit(f"no such candidate: {rc} (python stager.py list)")
    # The approval relies on `verify` — which only checked existence.
    cmd_verify(args)
    state["candidates"][rc]["state"] = "approved"
    state["candidates"][rc]["approved_at"] = now()
    save_manifest(state)
    print(f"{rc} APPROVED for release — but did anyone check the BYTES?")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python stager.py")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("stage").set_defaults(fn=cmd_stage)
    sub.add_parser("verify").set_defaults(fn=cmd_verify)
    sub.add_parser("list").set_defaults(fn=cmd_list)
    p = sub.add_parser("approve")
    p.add_argument("release_candidate")
    p.set_defaults(fn=cmd_approve)
    args = parser.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())