# Learning objectives — Module 05

## Objectives

| ID | By the end of this module you can… | Prove it by… |
|---|---|---|
| **LO 5.1** | Build a training pipeline with separated stages: validate data → features → train → evaluate → persist | Your `src/` layout where each stage is its own function/module, invoked by one entry point |
| **LO 5.2** | Control an experiment entirely from configuration (YAML), including the random seed | A `config.yaml` that fully determines a run; a config diff producing a predictable change |
| **LO 5.3** | Demonstrate reproducibility by producing identical metrics from two independent runs | Two runs with equal metrics **and** an identical model-file hash |
| **LO 5.4** | Engineer simple features and explain why feature definitions must live in code, not notebooks | Your feature function, plus a written explanation of the train/serve-skew risk it prevents |

## What "good" looks like

- **Pass:** `python -m src.train` twice ⇒ identical metrics JSON and identical
  model hash; and changing one config value changes *only* what it should.
- **Not yet:** metrics match but the hash differs (something unseeded), or a
  "reproducible" run needs a manual step you did not write down.

## Vocabulary you must be able to use after this module

**pipeline**, **stage**, **preprocessing**, **feature engineering**,
**feature leakage**, **train/serve skew**, **random seed**, **stratified split**,
**configuration file**, **baseline**, **challenger**, **accuracy vs. ROC AUC vs.
F1**, **class imbalance**, **threshold**, **model persistence**,
**ColumnTransformer / sklearn Pipeline**.

## How this module is assessed

- **Practical lab** (graded): reproducibility proof + config experiment —
  [lab.md](lab.md) §9.
- **Knowledge check:** 10 questions — [knowledge-check.md](knowledge-check.md).

!!! note "A finding you will reproduce, not take on trust"
    In the shared example, the logistic-regression **baseline** scores
    ROC AUC **0.7163** while gradient boosting scores **0.6431** — the fancy model
    loses. Both numbers were produced by running the code; you will reproduce them
    yourself in the worked example. Expect to be surprised; that is the lesson.

---

[← Module overview](index.md) · [Concepts →](concepts.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*