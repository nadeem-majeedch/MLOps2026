# Capstone pipeline report

**Gate:** PASS
(roc_auc 0.7662 vs floor 0.75)

## Model selection (validation only; test touched once)

| family | validation roc_auc |
|---|---|
| logistic | 0.7575 |
| gradient_boosting | 0.7324 |

**Winner:** logistic · operating point threshold=0.25

## Test metrics (single pass)

| metric | value |
|---|---|
| roc_auc | 0.7662 |
| accuracy | 0.8233 |
| precision | 0.3438 |
| recall | 0.4342 |
| f1 | 0.3837 |

## Fairness audit (device_access)

| group value | selection rate |
|---|---|
| 0 | 0.2606 |
| 1 | 0.1288 |

**Gap 0.1318 (target ≤ 0.1) —**
**OVER TARGET: investigate and document before release**

## Artefacts

| file | sha256[0:16] |
|---|---|
| `evaluation.json` | `f020c11896799c01` |
| `fairness.json` | `1a02cd5433730fa6` |
| `metrics.json` | `9812feb999079165` |
| `model.joblib` | `e401cfa42d650b0b` |
