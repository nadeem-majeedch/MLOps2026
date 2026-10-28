"""Stage 3 - performance after labels arrive (Module 14).

    python -m monitoring.performance

Joins the logged predictions with ground truth (`actual`) and measures the
model on the recent window, compared with the reference metrics and the
quality floor from config.yaml.

This is the ONLY script here that can say anything about accuracy: without
labels, drift is a suspicion, not a verdict.
"""

from __future__ import annotations

import json
import pathlib

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

from src import features as F

ROOT = pathlib.Path(__file__).resolve().parent.parent
MON = ROOT / "monitoring"
LOG = MON / "predictions.jsonl"
REFERENCE_METRICS = ROOT / "artifacts" / "metrics.json"
REPORT_JSON = MON / "performance_report.json"
REPORT_MD = MON / "performance_report.md"

MAX_AUC_DROP = 0.05


def main() -> int:
    if not LOG.exists():
        raise SystemExit("no predictions logged - run monitoring.log_predictions first")
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines()]
    df = pd.DataFrame(rows)
    labelled = df[df["actual"].notna()].copy()

    if labelled.empty:
        raise SystemExit(
            "no labelled records yet: accuracy cannot be measured. "
            "Wait for ground truth (this is normal in production)."
        )

    cfg = F.load_config(ROOT / "config.yaml")
    floor = float(cfg.get("quality", {}).get("roc_auc_floor", 0.0))
    reference = json.loads(REFERENCE_METRICS.read_text(encoding="utf-8"))
    ref_auc = reference["roc_auc"]

    scenarios = []
    for name, group in labelled.groupby("scenario"):
        auc = float(roc_auc_score(group["actual"], group["churn_probability"]))
        acc = float(accuracy_score(group["actual"], group["churn_pred"]))
        f1 = float(f1_score(group["actual"], group["churn_pred"], zero_division=0))
        drop = round(ref_auc - auc, 4)
        degraded = auc < floor or drop > MAX_AUC_DROP
        scenarios.append({
            "scenario": name,
            "window_ts": str(group["ts"].max()),
            "rows": len(group),
            "roc_auc": round(auc, 4),
            "accuracy": round(acc, 4),
            "f1": round(f1, 4),
            "drop_vs_reference": drop,
            "floor": floor,
            "degraded": bool(degraded),
        })

    report = {
        "reference_roc_auc": ref_auc,
        "floor": floor,
        "max_allowed_drop": MAX_AUC_DROP,
        "any_labelled": True,
        "scenarios": sorted(scenarios, key=lambda s: s["window_ts"]),
        "caveat": "Metrics here are measured on synthetic windows; on real "
                  "systems the same numbers come from logged predictions "
                  "joined to delayed outcomes.",
    }
    REPORT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines = ["# Performance report (labels arrived)", ""]
    lines += [
        (f"Reference ROC-AUC **{ref_auc}**, floor **{floor}**, "
         f"max tolerated drop **{MAX_AUC_DROP}**."),
        "",
        "| scenario | rows | roc_auc | accuracy | f1 | drop | verdict |",
        "|---|---|---|---|---|---|---|",
    ]
    for s in report["scenarios"]:
        verdict = "DEGRADED" if s["degraded"] else "within tolerance"
        lines.append(
            f"| {s['scenario']} | {s['rows']} | {s['roc_auc']} | {s['accuracy']} "
            f"| {s['f1']} | {s['drop_vs_reference']} | {verdict} |"
        )
    lines += ["", ("> Drift + no degradation means: do not retrain yet. "
                     "See monitoring/decision.md.")]
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    for s in report["scenarios"]:
        state = "DEGRADED" if s["degraded"] else "within tolerance"
        print(f"{s['scenario']:10} roc_auc={s['roc_auc']} "
              f"drop={s['drop_vs_reference']} -> {state}")
    print("-> monitoring/performance_report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())