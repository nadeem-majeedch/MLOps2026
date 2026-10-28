"""Intermediate starter — a small, validated, staged training pipeline.

    python -m pipeline.run            # run every stage, write a manifest
    python -m pipeline.run --force    # ignore freshness, re-run everything
    python -m pipeline.run --list     # show the stages

Stages (each reads only its declared inputs and writes only its outputs,
and every frame is checked against the data contract before training):

    generate  -> write out/dataset.csv (contract enforced by `data.validated`)
    train     -> train + evaluate, write out/model.joblib and out/metrics.json

Run it from this folder (the parent of `pipeline/`).
"""
