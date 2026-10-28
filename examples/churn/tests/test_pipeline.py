"""Integration test: does the whole path work end-to-end? (Module 07)

Where unit tests look at one function, this test exercises
CSV → validation → training → artefacts → loading → predicting,
which is exactly the path production will take.
"""

from __future__ import annotations

import json


def test_end_to_end_train_then_serve(config, data_path, tmp_path):
    import joblib
    import pandas as pd

    from src.train import train

    cfg = dict(config)
    cfg["output"] = {
        "model_path": str(tmp_path / "model.joblib"),
        "metrics_path": str(tmp_path / "metrics.json"),
    }
    cfg_path = tmp_path / "config.yaml"
    cfg_path.write_text(__import__("yaml").safe_dump(cfg), encoding="utf-8")

    metrics, _ = train(str(cfg_path), str(data_path))

    # the artefacts the pipeline promised were written
    assert (tmp_path / "model.joblib").exists()
    on_disk = json.loads((tmp_path / "metrics.json").read_text(encoding="utf-8"))
    assert on_disk == metrics

    # a fresh load of the saved model can serve predictions from raw rows
    model = joblib.load(tmp_path / "model.joblib")
    raw = pd.read_csv(data_path).head(5)
    x = raw[config["features"]["numeric"] + config["features"]["categorical"]]
    proba = model.predict_proba(x)[:, 1]
    assert len(proba) == 5
    assert set(raw["contract_type"]) - {"monthly", "one_year", "two_year"} == set()


def test_validation_blocks_bad_data(config, data_path, tmp_path):
    """The gate that CI will use: bad input must not produce a model."""
    import pandas as pd

    from src.validate import run_checks

    bad = pd.read_csv(data_path.parents[1] / "corrupt" / "missing.csv")
    results = run_checks(bad)
    assert any(not r["ok"] for r in results), "validator failed to reject bad data"