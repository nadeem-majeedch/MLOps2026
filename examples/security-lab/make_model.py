"""Create the toy `model.pkl` the flawed service loads (Lab 15 setup).

    python make_model.py

Writes `flawed/model.pkl` (and `fixed/model.pkl` if that folder exists):
a plain dict, so the pickle is harmless AND inspectable — the defect under
audit is the *unverified load*, not this particular payload.
"""

from __future__ import annotations

import hashlib
import pickle
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAYLOAD = {"score": 0.42, "trained_on": "synthetic-lab-fixture"}


def main() -> int:
    for folder in ("flawed", "fixed"):
        target = HERE / folder
        if target.is_dir():
            blob = (target / "model.pkl")
            with blob.open("wb") as fh:
                pickle.dump(PAYLOAD, fh)
            digest = hashlib.sha256(blob.read_bytes()).hexdigest()
            (target / "model.pkl.sha256").write_text(digest + "\n",
                                                      encoding="utf-8")
            print(f"wrote {folder}/model.pkl (+ .sha256 sidecar)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())