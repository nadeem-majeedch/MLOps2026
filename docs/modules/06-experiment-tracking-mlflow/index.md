# Module 06 — Experiment tracking and model evaluation using MLflow

!!! success "Module complete"
    Lessons, worked example, lab, independent challenge, knowledge check (with
    answers), troubleshooting, and references are all written.

**Stage:** Intermediate · **Estimated effort:** 8 h · **Depends on:** 05 · **Next:** 07

---

## What this module is about

Once runs are reproducible, the next question is comparative: *which configuration
was best, on what data, and why did we choose it?* Answering that honestly
requires **experiment tracking** — a systematic record of parameters, metrics,
artefacts, and decisions.

You will run MLflow **entirely locally** (no account, no cloud), log real runs,
compare them, and write a model-selection memo that a sceptical reader can check.
Along the way you will meet a real-world wrinkle: MLflow 3.x no longer accepts the
old plain-folder tracking backend, so the course uses a local SQLite database —
same machine, same zero cost, current behaviour.

## How to study this module (in order)

| # | File | What it does | Time |
|---|---|---|---|
| 1 | [learning-objectives.md](learning-objectives.md) | What you must be able to do, and how you prove it | 10 min |
| 2 | [concepts.md](concepts.md) | Runs, parameters/metrics/artifacts, evaluation discipline, MLflow locally | 120 min |
| 3 | [worked-example.md](worked-example.md) | Two real logged runs and the comparison query, actual output | 40 min |
| 4 | [lab.md](lab.md) | **Guided lab:** ten runs, one decision | 120 min |
| 5 | [independent-challenge.md](independent-challenge.md) | Reproduce your best run from a clean checkout and explain any drift | 55 min |
| 6 | [knowledge-check.md](knowledge-check.md) | 10 questions with reasoning | 30 min |
| 7 | [troubleshooting.md](troubleshooting.md) | Tracking-server, run, and query problems | as needed |
| 8 | [references.md](references.md) | MLflow docs and evaluation reading | optional |

## Before you start

- Module 05 completed — you need a working, reproducible training pipeline.
- `python -c "import mlflow; print(mlflow.__version__)"` must print a version
  (the course materials were verified with **MLflow 3.17.2**).
- Free and local: the tracking store is a file/SQLite database in your project
  folder. Nothing is uploaded anywhere.

## Evidence you should produce

1. An MLflow experiment with **≥10 runs**, each with parameters and metrics.
2. A comparison table and a one-page selection memo: chosen model, metric,
   baseline, and the reason — evidence-linked.
3. Your knowledge-check score.

---

[← Module 05](../05-reproducible-training-pipelines/index.md) · [Full syllabus](../../syllabus/detailed-syllabus.md#module-06-experiment-tracking-and-model-evaluation-using-mlflow) · [Module 07 →](../07-testing-for-ml/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*