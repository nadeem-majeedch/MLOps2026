"""Model loading (Module 10): resolve once at startup, never per request.

Order of preference:
  1. the model the registry says is in 'production'  (Module 09),
  2. the training artefact artifacts/model.joblib     (Modules 05/08).

If neither exists the service still *starts* — but /predict answers 503 with
a message telling you exactly what to run first. A service that crashes on
boot hides the problem; a service that explains it teaches.
"""

from __future__ import annotations

import hashlib
import json
import pathlib

import joblib

ROOT = pathlib.Path(__file__).resolve().parent.parent
REG_INDEX = ROOT / "registry_store" / "index.json"
ARTEFACT = ROOT / "artifacts" / "model.joblib"
ARTEFACT_METRICS = ROOT / "artifacts" / "metrics.json"

THRESHOLD = 0.5

FEATURES = {
    "numeric": ["tenure_months", "monthly_charges", "support_tickets"],
    "categorical": ["contract_type"],
}


def resolve_model() -> dict:
    """Return {'model': estimator | None, 'version': str, 'source': str, ...}."""
    # --- 1. registry production pointer -------------------------------
    if REG_INDEX.exists():
        index = json.loads(REG_INDEX.read_text(encoding="utf-8"))
        vid = index.get("stages", {}).get("production")
        if vid:
            meta_path = ROOT / "registry_store" / vid / "metadata.json"
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            path = ROOT / "registry_store" / vid / meta["model_file"]
            if path.exists():
                return {
                    "model": joblib.load(path),
                    "version": vid,
                    "source": str(path.relative_to(ROOT)),
                    "sha256": meta["model_sha256"],
                    "metrics": meta["metrics"],
                    "gate": meta["gate"],
                }

    # --- 2. training artefact ------------------------------------------
    if ARTEFACT.exists():
        metrics = {}
        if ARTEFACT_METRICS.exists():
            metrics = json.loads(ARTEFACT_METRICS.read_text(encoding="utf-8"))
        return {
            "model": joblib.load(ARTEFACT),
            "version": "artefact",
            "source": str(ARTEFACT.relative_to(ROOT)),
            "sha256": hashlib.sha256(ARTEFACT.read_bytes()).hexdigest()[:16],
            "metrics": metrics,
            "gate": {"passed": None, "source": "not registered"},
        }

    # --- 3. nothing to serve -------------------------------------------
    return {
        "model": None,
        "version": "none",
        "source": "none",
        "sha256": "",
        "metrics": {},
        "gate": {"passed": None, "source": "no model"},
    }