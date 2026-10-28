"""Stage 2 - drift detection (Module 14).

    python -m monitoring.drift --snapshot      # record today's good data
    python -m monitoring.drift                 # compare latest window vs reference
    python -m monitoring.drift --check         # exit 1 if strong drift (for gates)

Measures, per feature:
  * KS test   (scipy)  - do the two samples come from the same distribution?
  * PSI       (custom) - how far did the distribution moved, in bins?
  * category mix (chi2) - for contract_type

PSI rule of thumb used here (documented, not magic):
    < 0.10 stable | 0.10-0.20 moderate | > 0.20 strong drift -> alert

IMPORTANT: this answers "did the inputs change?" - never "is the model bad?"
Drift without a performance report is a reason to LOOK, not to retrain.
"""

from __future__ import annotations

import argparse
import json
import pathlib

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, ks_2samp

ROOT = pathlib.Path(__file__).resolve().parent.parent
MON = ROOT / "monitoring"
RAW = ROOT / "data" / "raw" / "churn.csv"
REFERENCE = MON / "reference.csv"
LOG = MON / "predictions.jsonl"
REPORT_JSON = MON / "drift_report.json"
REPORT_MD = MON / "drift_report.md"

NUMERIC = ["tenure_months", "monthly_charges", "support_tickets"]
CATEGORICAL = ["contract_type"]

PSI_STRONG = 0.20
PSI_MODERATE = 0.10
BINS = 10


def psi(reference: np.ndarray, current: np.ndarray) -> float:
    """Population Stability Index over deciles of the reference sample."""
    edges = np.unique(np.quantile(reference, np.linspace(0, 1, BINS + 1)))
    if len(edges) < 3:
        return 0.0
    edges[0], edges[-1] = -np.inf, np.inf
    ref_counts = np.histogram(reference, bins=edges)[0].astype(float)
    cur_counts = np.histogram(current, bins=edges)[0].astype(float)
    ref_pct = np.clip(ref_counts / ref_counts.sum(), 1e-4, None)
    cur_pct = np.clip(cur_counts / cur_counts.sum(), 1e-4, None)
    return float(np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct)))


def verdict_for(psi_value: float, ks_p: float) -> str:
    if psi_value > PSI_STRONG:
        return "strong"
    if psi_value > PSI_MODERATE or ks_p < 0.01:
        return "moderate"
    return "stable"


def load_window(scenario: str | None) -> pd.DataFrame:
    if not LOG.exists():
        raise SystemExit("no predictions logged yet - run "
                         "`python -m monitoring.log_predictions` first")
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines()]
    if scenario is None:                       # latest scenario in the log
        scenario = rows[-1]["scenario"]
    chosen = [r for r in rows if r["scenario"] == scenario]
    if not chosen:
        raise SystemExit(f"no records for scenario {scenario!r}")
    return pd.DataFrame(chosen), scenario


def main() -> int:
    parser = argparse.ArgumentParser(description="Feature drift report")
    parser.add_argument("--snapshot", action="store_true",
                        help="store the current raw data as the reference")
    parser.add_argument("--scenario", default=None,
                        help="which logged window to test (default: latest)")
    parser.add_argument("--check", action="store_true",
                        help="exit 1 when any feature shows strong drift")
    args = parser.parse_args()

    if args.snapshot:
        MON.mkdir(parents=True, exist_ok=True)
        pd.read_csv(RAW).to_csv(REFERENCE, index=False)
        print(f"reference snapshot written -> monitoring/reference.csv "
              f"({len(pd.read_csv(REFERENCE))} rows)")
        return 0

    if not REFERENCE.exists():
        raise SystemExit("no reference: run `python -m monitoring.drift --snapshot` first")

    ref = pd.read_csv(REFERENCE)
    window, scenario = load_window(args.scenario)

    features = []
    for col in NUMERIC:
        stat = ks_2samp(ref[col].to_numpy(), window[col].to_numpy())
        p = psi(ref[col].to_numpy(), window[col].to_numpy())
        features.append({
            "feature": col, "kind": "numeric",
            "ks_statistic": round(float(stat.statistic), 4),
            "ks_pvalue": float(f"{stat.pvalue:.3g}"),
            "psi": round(p, 4),
            "verdict": verdict_for(p, stat.pvalue),
        })

    table = pd.crosstab(window["contract_type"], columns="n").reindex(
        CATEGORICAL, fill_value=0
    )
    categories = sorted(set(ref["contract_type"]) | set(window["contract_type"]))
    ref_counts = ref["contract_type"].value_counts().reindex(categories, fill_value=0)
    cur_counts = window["contract_type"].value_counts().reindex(categories, fill_value=0)
    chi2, p_cat, _, _ = chi2_contingency(
        np.array([ref_counts.values, cur_counts.values])
    )
    mix_shift = float(
        (cur_counts / cur_counts.sum() - ref_counts / ref_counts.sum()).abs().max()
    )
    features.append({
        "feature": "contract_type", "kind": "categorical",
        "chi2": round(float(chi2), 3), "pvalue": float(f"{p_cat:.3g}"),
        "max_mix_shift": round(mix_shift, 4),
        "verdict": "strong" if mix_shift > 0.10 or p_cat < 0.01 else "stable",
    })
    del table

    strong = [f["feature"] for f in features if f["verdict"] == "strong"]
    moderate = [f["feature"] for f in features if f["verdict"] == "moderate"]
    overall = "DRIFT DETECTED" if strong else (
        "moderate drift" if moderate else "stable"
    )

    report = {
        "scenario": scenario,
        "reference_rows": len(ref),
        "window_rows": len(window),
        "overall": overall,
        "strong": strong,
        "moderate": moderate,
        "thresholds": {"psi_strong": PSI_STRONG, "psi_moderate": PSI_MODERATE,
                       "ks_alpha": 0.01},
        "features": features,
        "caveat": "Drift shows inputs changed - it does NOT show the model "
                  "is wrong. Check monitoring/performance.py before acting.",
    }
    REPORT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines = [
        f"# Drift report - window `{scenario}`",
        "",
        (f"**Overall: {overall}** "
         f"({len(window)} rows vs {len(ref)} reference rows)"),
        "",
        "| feature | measure | value | verdict |",
        "|---|---|---|---|",
    ]
    for f in features:
        measure = "psi" if f["kind"] == "numeric" else "max mix shift"
        value = f.get("psi", f.get("max_mix_shift"))
        lines.append(f"| {f['feature']} | {measure} | {value} | {f['verdict']} |")
    lines += [
        "",
        f"> {report['caveat']}",
        "",
        ("Thresholds: PSI < 0.10 stable, 0.10-0.20 moderate, > 0.20 strong; "
         "KS p < 0.01 significant."),
    ]
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"overall: {overall}")
    for f in features:
        print(f"  {f['feature']:17} {f['verdict']:9} "
              f"psi={f.get('psi', '-')}")
    print("-> monitoring/drift_report.md")
    if args.check and strong:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())