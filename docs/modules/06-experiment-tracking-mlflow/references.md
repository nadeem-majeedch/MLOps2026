# References — Module 06

## Official documentation

| Resource | What it is for |
|---|---|
| [MLflow documentation](https://mlflow.org/docs/latest/index.html) | Tracking, runs, artifacts, models, registry (Module 09 continues on this stack) |
| [MLflow: Tracking Quickstart](https://mlflow.org/docs/latest/getting-started/intro-quickstart/index.html) | The canonical first run |
| [MLflow: Running a MLflow server](https://mlflow.org/docs/latest/gutorials-and-experiments/run-multiple-runs.html) (server/CLI reference) | Local UI on 127.0.0.1 |
| [MLflow: File store migration notice](https://mlflow.org/docs/latest/self-hosting/migrate-from-file-store) | Why `file:./mlruns` was rejected — the error you may see |
| [MLflow model flavours (scikit-learn)](https://mlflow.org/docs/latest/python_api/mlflow.sklearn.html) | `log_model` / `load_model` used in the lab |

## Evaluation and metric reading

| Resource | Why |
|---|---|
| [scikit-learn: model evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html) | Precise definitions and pitfalls of every metric used here |
| [scikit-learn: imbalanced classification](https://scikit-learn.org/stable/modules/classification_imbalanced_data.html) | Why accuracy misleads at 9% positives |
| [Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml) | Sequenced advice on measuring before optimising |
| [Model Cards](https://arxiv.org/pdf/1810.03993) | Where a model-selection decision eventually gets written down (M09/M15) |

## Alternatives (worth knowing about)

| Tool | Notes |
|---|---|
| [Weights & Biases](https://docs.wandb.ai/) ☁️ | Hosted; polished collaboration; free tier with account |
| [Aim](https://aimhub.io/) | Open-source, self-hosted experiment tracker |
| [Neptune](https://docs.neptune.ai/) ☁️ | Hosted experiment tracking |
| [DVC experiments](https://dvc.org/doc/user-guide/experiment-management) | Experiments built on the DVC you already know (M04) |

## Course material

- [glossary](../../glossary/index.md) — run, parameter, metric, artifact, champion
- [Module 05](../05-reproducible-training-pipelines/index.md) — the reproducible pipeline this module wraps
- [Module 09](../09-model-artifacts-registry/index.md) — where runs become registry entries
- [resources](../../resources/index.md) — curated wider reading

## General principle vs. tool choice

| General principle | Course choice | Alternatives |
|---|---|---|
| Every run is a record | MLflow local runs | CSV logs (baseline), Aim, W&B |
| Compare on a pre-stated metric | Written pre-registration in the lab | Weighted scorecards, decision records |
| Data referenced, not copied | DVC hash + config artifact | Object-store URIs with version ids (☁️) |
| Local-first, no account | SQLite backend + local artifacts | Hosted trackers (☁️, account + privacy trade-off) |
| Decision memo with run IDs | Markdown memo in the portfolio | Model card (M09), issue templates |

---

[← Troubleshooting](troubleshooting.md) · [Module overview](index.md) · [Next: Module 07 →](../07-testing-for-ml/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*