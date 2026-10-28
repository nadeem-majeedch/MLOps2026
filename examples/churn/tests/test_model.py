"""Model tests: does the model behave acceptably? (Module 07)

Three kinds of model test:

1. **Performance floor** — quality below a threshold fails the build. This is the
   gate that stops a bad model reaching production.
2. **Sanity/invariance** — outputs are structurally plausible (probabilities in
   [0, 1], batching does not change individual predictions).
3. **Determinism** — the same seed and data give the same predictions.

Thresholds here are honest for this dataset: the test set has ~36 positive
examples, so a tight floor would be flaky. A floor is a *policy* you choose, not
a fact you discover — see concepts.md.
"""

from __future__ import annotations

import numpy as np

from src.train import train

ROC_AUC_FLOOR = 0.70


def test_roc_auc_above_performance_floor(config, data_path, tmp_path):
    cfg = _config_in(tmp_path, config)
    metrics, _ = train(str(cfg), str(data_path))
    assert metrics["roc_auc"] >= ROC_AUC_FLOOR, (
        f"roc_auc {metrics['roc_auc']} is below the floor {ROC_AUC_FLOOR}"
    )


def test_accuracy_at_least_matches_majority_baseline(config, data_path, tmp_path):
    """Accuracy must not be *worse* than 'always predict the majority class'.

    Note the assertion is `>=`, and with this dataset it passes with equality:
    at a 0.5 threshold the baseline model predicts 'no churn' for everyone, which
    scores 0.91 accuracy — exactly the majority baseline. That is the lesson:
    accuracy alone proves nothing under class imbalance. The gate that actually
    protects the build is the ROC AUC floor above.
    """
    cfg = _config_in(tmp_path, config)
    metrics, _ = train(str(cfg), str(data_path))
    majority = 1 - float(metrics["positive_rate_test"])
    assert metrics["accuracy"] >= majority


def test_probabilities_are_well_formed(config, data_path, tmp_path):
    import pandas as pd

    cfg = _config_in(tmp_path, config)
    _metrics, model = train(str(cfg), str(data_path))

    sample = pd.read_csv(data_path).head(20)
    x = sample[config["features"]["numeric"] + config["features"]["categorical"]]
    proba = model.predict_proba(x)[:, 1]
    assert np.all((proba >= 0.0) & (proba <= 1.0))
    assert not np.any(np.isnan(proba))


def test_batching_does_not_change_predictions(config, data_path, tmp_path):
    import pandas as pd

    cfg = _config_in(tmp_path, config)
    _, pipeline = train(str(cfg), str(data_path))
    frame = pd.read_csv(data_path).head(40)
    x = frame[config["features"]["numeric"] + config["features"]["categorical"]]

    all_at_once = pipeline.predict_proba(x)[:, 1]
    one_by_one = np.array([pipeline.predict_proba(x.iloc[i : i + 1])[0, 1] for i in range(len(x))])
    assert np.allclose(all_at_once, one_by_one, atol=1e-9)


def test_same_seed_gives_same_metrics(config, data_path, tmp_path):
    cfg = _config_in(tmp_path, config)
    first, _ = train(str(cfg), str(data_path))
    second, _ = train(str(cfg), str(data_path))
    assert first == second, "the pipeline is not reproducible"


def _config_in(tmp_path, config: dict):
    """Write a copy of the config whose outputs land in tmp_path."""
    import yaml

    cfg = dict(config)
    cfg["output"] = {
        "model_path": str(tmp_path / "model.joblib"),
        "metrics_path": str(tmp_path / "metrics.json"),
    }
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(cfg), encoding="utf-8")
    return path