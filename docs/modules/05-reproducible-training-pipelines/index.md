# Module 05 — Reproducible model training and pipeline design

!!! success "Module complete"
    Lessons, worked example, lab, independent challenge, knowledge check (with
    answers), troubleshooting, and references are all written.

**Stage:** Foundations (beginner) · **Estimated effort:** 8 h · **Depends on:** 04 · **Next:** 06

---

## What this module is about

This is where the course starts *building*: a training pipeline whose result is a
property of its inputs, not of the moment it ran. You will separate the stages
(validate → features → train → evaluate → persist), drive everything from a
configuration file, and **prove** reproducibility by running twice and comparing
hashes.

You will also meet a genuine modelling surprise that the shared example
deliberately contains: the simple baseline model **beats** the fancier one. That
is not a bug — it is the reason this course insists on baselines and evaluation
against them.

## How to study this module (in order)

| # | File | What it does | Time |
|---|---|---|---|
| 1 | [learning-objectives.md](learning-objectives.md) | What you must be able to do, and how you prove it | 10 min |
| 2 | [concepts.md](concepts.md) | Pipeline design, configuration, seeds, leakage, baselines and metrics | 120 min |
| 3 | [worked-example.md](worked-example.md) | Train twice, compare hashes, swap the model, read the metrics honestly | 40 min |
| 4 | [lab.md](lab.md) | **Guided lab:** same seed, same model | 110 min |
| 5 | [independent-challenge.md](independent-challenge.md) | Add a feature behind a config flag and prove the flag governs it | 55 min |
| 6 | [knowledge-check.md](knowledge-check.md) | 10 questions with reasoning | 30 min |
| 7 | [troubleshooting.md](troubleshooting.md) | Non-reproducible runs, sklearn errors, config mistakes | as needed |
| 8 | [references.md](references.md) | scikit-learn, PyYAML, and the ML-engineering sources | optional |

## Before you start

- Modules 02–04 completed (environment, structure, data validation).
- Python with pandas + scikit-learn + PyYAML (the Module 02 environment).
- Free, local, CPU-only — **no GPU, no cloud, no account**.

## Evidence you should produce

1. Two runs with byte-identical model files (the hash comparison output).
2. A metrics JSON showing baseline vs. challenger, with your written choice.
3. A config-diff experiment: one value changed, the effect isolated.

---

[← Module 04](../04-data-quality-validation-versioning/index.md) · [Full syllabus](../../syllabus/detailed-syllabus.md#module-05-reproducible-model-training-and-pipeline-design) · [Module 06 →](../06-experiment-tracking-mlflow/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*