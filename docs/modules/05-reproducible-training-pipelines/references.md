# References — Module 05

## Official documentation

| Resource | What it is for |
|---|---|
| [scikit-learn user guide](https://scikit-learn.org/stable/user_guide.html) | The pipeline, preprocessing, and model APIs used here |
| [scikit-learn: Pipeline](https://scikit-learn.org/stable/modules/compose.html#pipeline) | Why preprocessing belongs inside the estimator |
| [scikit-learn: random seeds / reproducibility](https://scikit-learn.org/stable/common_pitfalls.html) | The official list of pitfalls, including leakage and non-determinism |
| [scikit-learn metrics](https://scikit-learn.org/stable/modules/model_evaluation.html) | What each metric measures — and its assumptions |
| [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation) | Configuration parsing |
| [joblib](https://joblib.readthedocs.io/) | Persisting fitted pipelines |

## Primary reading

| Resource | Why it matters for this module |
|---|---|
| [Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml) — Google | Start simple, measure against a baseline, then iterate — the discipline this module practises |
| [scikit-learn common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html) | Leakage, non-deterministic pipelines, and train/test contamination, explained by the library authors |
| [Accuracy paradox / imbalanced data](https://scikit-learn.org/stable/modules/classification_imbalanced_data.html) | Why 0.91 accuracy can be worthless — measured in this module's example |

## Course material

- [glossary](../../glossary/index.md) — pipeline, leakage, baseline, threshold entries
- [Module 04 lab](../04-data-quality-validation-versioning/lab.md) — the validation gate your training depends on
- [Module 06](../06-experiment-tracking-mlflow/index.md) — where these metrics become tracked experiments

## General principle vs. tool choice

| General principle | Course choice | Alternatives |
|---|---|---|
| Stages with declared inputs/outputs | `src/features.py`, `src/train.py` | Prefect/Dagster flows (M13), Make targets (M08) |
| Preprocessing travels with the model | sklearn `Pipeline` | Column pipelines in other frameworks; manual transform bundles |
| Every random source seeded | `random_state` from config | `numpy.random.default_rng(seed)`, `torch.manual_seed` |
| Configuration outside code | `config.yaml` + PyYAML | Hydra/OmegaConf, argparse, environment variables |
| Metrics recorded with the artefact | `metrics.json` next to `model.joblib` | MLflow runs (Module 06) |
| Honest evaluation | baseline → challenger on a stated metric | cross-validation, bootstrap intervals |

---

[← Troubleshooting](troubleshooting.md) · [Module overview](index.md) · [Next: Module 06 →](../06-experiment-tracking-mlflow/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*