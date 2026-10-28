# Learning objectives — Module 06

## Objectives

| ID | By the end of this module you can… | Prove it by… |
|---|---|---|
| **LO 6.1** | Instrument a training run to log parameters, metrics, artifacts, and source version | Your experiment showing ≥10 runs with complete parameter and metric sets |
| **LO 6.2** | Compare runs, identify the best configuration, and justify the choice beyond a single metric | A comparison table plus a memo naming the metric, the baseline, and the winner |
| **LO 6.3** | Evaluate against a baseline with appropriate metrics for the problem type and class balance | Written justification that acknowledges the 9%-positive class balance and the accuracy trap |
| **LO 6.4** | Run an MLflow tracking server locally and browse its UI | `mlflow server` started locally, your runs visible in the browser |

## What "good" looks like

- **Pass:** a stranger can open your experiment, see what was tried, and follow
  your memo to the exact run you chose — with the decision resting on a stated
  metric rather than on recency or fashion.
- **Not yet:** runs exist but parameters are missing, or the "best" run is chosen
  on accuracy alone under heavy class imbalance.

## Vocabulary you must be able to use after this module

**experiment tracking**, **run**, **parameter**, **metric**, **artifact**,
**tracking backend/store**, **tracking server**, **experiment vs. run**,
**artifact store**, **champion / challenger**, **model selection**,
**baseline**, **metric selection**, **lineage** (capture stage).

## How this module is assessed

- **Practical lab** (graded): ≥10 runs + comparison + memo —
  [lab.md](lab.md) §9. This module also delivers **mini-project MP2**.
- **Knowledge check:** 10 questions — [knowledge-check.md](knowledge-check.md).

!!! warning "Version-specific behaviour you will actually see"
    Verified with **MLflow 3.17.2**: the legacy plain-folder backend
    (`file:./mlruns`) is **rejected** with an explicit error; the course uses
    `sqlite:///mlflow.db`, which is still 100% local. The exact wording may
    change in future releases — the official docs in
    [references.md](references.md) are the authority.

---

[← Module overview](index.md) · [Concepts →](concepts.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*