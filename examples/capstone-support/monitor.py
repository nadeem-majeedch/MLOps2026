"""Monitoring for the capstone (Modules 14 + 17).

    python monitor.py snapshot                 # store today's reference
    python monitor.py log                      # score a baseline window
    python monitor.py log --shifted --labels   # replay a shifted window
    python monitor.py drift                    # PSI vs reference -> report
    python monitor.py performance              # labels -> AUC vs floor
    python monitor.py decision                 # 2x2 matrix -> decision.md

The four stages answer four different questions, in order — drift alone never
authorises a retrain (the Module 14 lesson, restated in capstone form).
"""

from __future__ import annotations

import argparse
import json
import pathlib

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

from src import features as F

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "monitoring_out"
REF = OUT / "reference.csv"
LOG = OUT / "predictions.jsonl"
NUMERIC = ["attendance_rate", "prior_score", "lms_logins",
           "missed_assessments", "assignment_rate"]
PSI_STRONG, PSI_MODERATE = 0.20, 0.10


def psi(reference: np.ndarray, current: np.ndarray) -> float:
    edges = np.unique(np.quantile(reference, np.linspace(0, 1, 11)))
    if len(edges) < 3:
        return 0.0
    edges[0], edges[-1] = -np.inf, np.inf
    ref = np.clip(np.histogram(reference, bins=edges)[0].astype(float), 1e-4, None)
    cur = np.clip(np.histogram(current, bins=edges)[0].astype(float), 1e-4, None)
    ref, cur = ref / ref.sum(), cur / cur.sum()
    return float(np.sum((cur - ref) * np.log(cur / ref)))


def load_model():
    from service.app import resolve_model

    state = resolve_model()
    if state["model"] is None:
        raise SystemExit("no model: run `python pipeline.py` first")
    return state


def cmd_snapshot(_: argparse.Namespace) -> int:
    OUT.mkdir(exist_ok=True)
    pd.read_csv(ROOT / "data" / "support.csv").to_csv(REF, index=False)
    print("reference written -> monitoring_out/reference.csv")
    return 0


def cmd_log(args: argparse.Namespace) -> int:
    config = F.load_config(ROOT / "config.yaml")
    df = pd.read_csv(ROOT / "data" / "support.csv").sample(
        n=400, random_state=7).reset_index(drop=True)
    scenario = "baseline"
    if args.shifted:                       # replayed distribution shift
        rng = np.random.default_rng(11)
        df["attendance_rate"] = np.clip(
            df["attendance_rate"] - rng.normal(0.08, 0.03, len(df)), 0.3, 1.0).round(3)
        df["assignment_rate"] = np.clip(
            df["assignment_rate"] - rng.normal(0.10, 0.04, len(df)), 0.0, 1.0).round(3)
        df["missed_assessments"] = np.clip(
            df["missed_assessments"] + rng.poisson(1.5, len(df)), 0, 30)
        scenario = "shifted"

    state = load_model()
    proba = state["model"].predict_proba(df[F.feature_columns(config)])[:, 1]
    OUT.mkdir(exist_ok=True)
    with LOG.open("a", encoding="utf-8") as fh:
        for i, row in df.iterrows():
            fh.write(json.dumps({
                "scenario": scenario,
                "attendance_rate": float(row["attendance_rate"]),
                "prior_score": float(row["prior_score"]),
                "lms_logins": int(row["lms_logins"]),
                "missed_assessments": int(row["missed_assessments"]),
                "assignment_rate": float(row["assignment_rate"]),
                "device_access": int(row["device_access"]),
                "support_probability": round(float(proba[i]), 4),
                "flag_for_support": int(proba[i] >= state["threshold"]),
                "model_version": state["version"],
                "actual": int(row["at_risk"]) if args.labels else None,
            }) + "\n")
    print(f"logged {len(df)} predictions scenario={scenario} "
          f"labels={'yes' if args.labels else 'not yet'}")
    return 0


def cmd_drift(_: argparse.Namespace) -> int:
    if not REF.exists():
        raise SystemExit("no reference: python monitor.py snapshot first")
    if not LOG.exists():
        raise SystemExit("no predictions: python monitor.py log first")
    ref = pd.read_csv(REF)
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines()]
    window = pd.DataFrame([r for r in rows if r["scenario"] == "shifted"] or rows)
    scenario = "shifted" if any(r["scenario"] == "shifted" for r in rows) else "baseline"

    features = []
    for col in NUMERIC:
        value = psi(ref[col].to_numpy(), window[col].to_numpy())
        verdict = ("strong" if value > PSI_STRONG
                   else "moderate" if value > PSI_MODERATE else "stable")
        features.append({"feature": col, "psi": round(value, 4), "verdict": verdict})

    strong = [f["feature"] for f in features if f["verdict"] == "strong"]
    report = {
        "scenario": scenario, "window_rows": len(window),
        "reference_rows": len(ref),
        "overall": "DRIFT DETECTED" if strong else "stable",
        "strong": strong, "features": features,
        "caveat": "Inputs moved - NOT a claim about accuracy. Labels decide.",
    }
    (OUT / "drift_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    for f in features:
        print(f"  {f['feature']:20} psi={f['psi']:<7} {f['verdict']}")
    print(f"overall: {report['overall']} -> monitoring_out/drift_report.json")
    return 0


def cmd_performance(_: argparse.Namespace) -> int:
    if not LOG.exists():
        raise SystemExit("no predictions logged")
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines()]
    labelled = pd.DataFrame([r for r in rows if r.get("actual") is not None])
    if labelled.empty:
        raise SystemExit("no labelled records yet - accuracy cannot be measured")
    metrics = json.loads((ROOT / "artifacts" / "metrics.json").read_text(encoding="utf-8"))
    floor = float(F.load_config(ROOT / "config.yaml")
                  .get("quality", {}).get("roc_auc_floor", 0.0))
    results = {}
    for scenario, group in labelled.groupby("scenario"):
        auc = float(roc_auc_score(group["actual"], group["support_probability"]))
        results[scenario] = {"roc_auc": round(auc, 4),
                             "drop_vs_reference": round(metrics["roc_auc"] - auc, 4),
                             "degraded": bool(auc < floor or metrics["roc_auc"] - auc > 0.05)}
    report = {"reference_roc_auc": metrics["roc_auc"], "floor": floor,
              "scenarios": results}
    (OUT / "performance_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    for name, r in results.items():
        print(f"  {name:10} auc={r['roc_auc']} drop={r['drop_vs_reference']} "
              f"{'DEGRADED' if r['degraded'] else 'within tolerance'}")
    return 0


def cmd_decision(_: argparse.Namespace) -> int:
    drift_path = OUT / "drift_report.json"
    if not drift_path.exists():
        raise SystemExit("run `python monitor.py drift` first")
    drift = json.loads(drift_path.read_text(encoding="utf-8"))
    perf_path = OUT / "performance_report.json"
    degraded = False
    if perf_path.exists():
        perf = json.loads(perf_path.read_text(encoding="utf-8"))
        latest = list(perf["scenarios"].values())[-1] if perf["scenarios"] else None
        degraded = bool(latest and latest["degraded"])

    drifted = drift["overall"] == "DRIFT DETECTED"
    matrix = {
        (False, False): "KEEP", (True, False): "MONITOR",
        (False, True): "INVESTIGATE", (True, True): "RETRAIN CANDIDATE",
    }
    action = matrix[(drifted, degraded)]
    text = f"""# Capstone monitoring decision

| input | value |
|---|---|
| drift | {drift['overall']} (strong: {', '.join(drift['strong']) or 'none'}) |
| labels + degradation | {"yes" if degraded else "no / labels absent"} |

## Decision: **{action}**

{"Drift alone never authorises a retrain - keep watching until labels agree." if action == "MONITOR" else
 "Evidence agrees: run `python pipeline.py --clean`, check the gate, register a new release, and know your rollback before promoting." if action == "RETRAIN CANDIDATE" else
 "Labels fell without input drift: suspect labelling or pipeline, not the world." if action == "INVESTIGATE" else
 "Nothing moved and nothing fell. Continue routine monitoring."}

_A script recommends; a human decides (Module 14's rule, restated here)._
"""
    (OUT / "decision.md").write_text(text, encoding="utf-8")
    print(f"decision: {action} -> monitoring_out/decision.md")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="python monitor.py")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("snapshot", help="store the reference distribution").set_defaults(fn=cmd_snapshot)

    p = sub.add_parser("log", help="score a window into predictions.jsonl")
    p.add_argument("--shifted", action="store_true", help="replay a shifted window")
    p.add_argument("--labels", action="store_true", help="ground truth available")
    p.set_defaults(fn=cmd_log)

    sub.add_parser("drift", help="PSI drift report").set_defaults(fn=cmd_drift)
    sub.add_parser("performance", help="AUC vs reference (labels required)").set_defaults(fn=cmd_performance)
    sub.add_parser("decision", help="apply the 2x2 decision matrix").set_defaults(fn=cmd_decision)

    args = parser.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())