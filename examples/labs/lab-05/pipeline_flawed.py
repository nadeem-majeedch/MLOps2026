"""LAB 05 fixture — a four-stage pipeline that is NOT deterministic.

    python pipeline_flawed.py            # prepare -> features -> train -> evaluate
    python pipeline_flawed.py --out out2 # second copy, for comparing hashes

Stages write real files into --out:
    prepared.csv   features.csv   model.joblib   metrics.json   manifest.json

Determinism contract the lab requires (the reason this file exists):
    two runs over the same inputs  =>  every output byte-identical.

Three spots in the code are marked "suspicious" with comments ending in
"..." — decide which of them actually break the contract (not all of them
do), fix them in YOUR copy, then prove it with hashes.
See ../solutions/lab-05/ afterwards.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import time

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE.parent / "data" / "customers_clean.csv"


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stage_prepare(out: pathlib.Path) -> pathlib.Path:
    df = pd.read_csv(DATA)
    target = out / "prepared.csv"
    df.to_csv(target, index=False, lineterminator="\n")
    return target


def stage_features(out: pathlib.Path) -> pathlib.Path:
    df = pd.read_csv(out / "prepared.csv")
    # DEFECT 1 (or is it?): which columns exist is discovered from the
    #            directory... (sorted() today — is that guaranteed?)
    discovered = sorted(p.stem for p in out.glob("*.csv"))
    columns = [c for c in df.columns if c not in ("churned", "customer_id")]
    x = pd.get_dummies(df[columns], columns=["contract_type"])
    x.attrs["discovered_inputs"] = discovered
    x.to_csv(out / "features.csv", index=False, lineterminator="\n")
    return out / "features.csv"


def stage_train(out: pathlib.Path) -> pathlib.Path:
    x = pd.read_csv(out / "features.csv")
    y = pd.read_csv(out / "prepared.csv")["churned"]
    # DEFECT 2: the seed is "the clock"...
    seed = int(time.time())
    x_tr, x_te, y_tr, y_te = train_test_split(
        x, y, test_size=0.25, stratify=y, random_state=seed
    )
    model = LogisticRegression(max_iter=1000)
    model.fit(x_tr, y_tr)
    joblib.dump(model, out / "model.joblib")
    proba = model.predict_proba(x_te)[:, 1]
    metrics = {"roc_auc": float(roc_auc_score(y_te, proba)), "seed": seed}
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2),
                                      encoding="utf-8")
    return out / "model.joblib"


def stage_evaluate(out: pathlib.Path) -> pathlib.Path:
    metrics = json.loads((out / "metrics.json").read_text(encoding="utf-8"))
    manifest = {
        "outputs": {p.name: sha256(p) for p in sorted(out.iterdir())
                    if p.is_file() and p.name != "manifest.json"},
        # DEFECT 3: "when did this run" is baked into the artifact...
        "run_finished_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "roc_auc": metrics["roc_auc"],
    }
    path = out / "manifest.json"
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="lab 05 flawed pipeline")
    parser.add_argument("--out", default=str(HERE / "out"))
    args = parser.parse_args(argv)
    out = pathlib.Path(args.out)
    out.mkdir(exist_ok=True)

    for stage in (stage_prepare, stage_features, stage_train, stage_evaluate):
        produced = stage(out)
        print(f"[{stage.__name__:15}] -> {produced.name}")

    digest = sha256(out / "manifest.json")
    print(f"manifest sha256[0:16] = {digest}")
    print("run it again: same bytes? (that is the whole lab)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())