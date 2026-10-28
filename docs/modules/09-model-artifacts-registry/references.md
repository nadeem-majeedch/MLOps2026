# References — Module 09

## Tool documentation

| Resource | Use it for |
|---|---|
| [MLflow Model Registry](https://mlflow.org/docs/latest/model-registry.html) | The canonical remote registry: stages/aliases, transitions, UI, model versioning |
| [MLflow Model Registry concepts](https://mlflow.org/docs/latest/model-registry.html#model-registry-workflows) | Registered models, versions, stages — the same vocabulary as this module |
| [joblib](https://joblib.readthedocs.io/) | How sklearn pipelines are serialised (and why `model.joblib` carries preprocessing too) |
| [DVC model management](https://dvc.org/doc/user-guide/model-management) | An alternative, data-lineage-first model store (ties to Module 04) |
| [sklearn `Pipeline`](https://scikit-learn.org/stable/modules/compose.html#pipeline) | Why one artefact must contain preprocessing + estimator |

## Model cards and ML validation

- **Mitchell et al. (2019), *Model Cards for Model Reporting*, FAT\*.**
  The origin of the structured card: intended use, evaluation, limitations,
  ethical considerations. Our lab's card headings follow this paper.
- **Breck et al. (2017), *The ML Test Score* (Google), MLSys** — where the
  "gate before serving" idea (and the registry's refusal rules) comes from.
- **Shankar et al. (2022), *Connected: Auditing and Improving Machine Learning
  Model Degradation*, KDD** — lineage + monitoring as one loop (foreshadows
  Module 14).

## Distinguishing tool-specific from general

| Claim | Kind |
|---|---|
| "Model versions should be immutable" | **General principle** |
| "Promote through stages; never skip review" | **General principle** (org-specific who approves) |
| "Rollback must be rehearsed before release" | **General principle** |
| "`python -m registry rollback production`" | **Course-specific CLI** |
| "MLflow stages are being replaced by aliases (`champion`/`challenger`)" | **Tool-specific and version-dependent** — check current MLflow docs |
| "`index.json` layout" | **Course-specific implementation** |

## Related course material

- Module 08 — produced the artefacts and gate results you register.
- Module 10 — the service that *reads* the production pointer.
- Module 12 — CI refusing to merge changes that break the gate.
- Module 15 — model cards as governance evidence.
- [Tool selection guide](../../syllabus/tool-selection-guide.md) — registry options.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*