# Module 07 — Unit, data, model, integration, and regression testing

!!! success "Module complete"
    Lessons, worked example, lab, independent challenge, knowledge check (with
    answers), troubleshooting, and references are all written.

**Stage:** Intermediate · **Estimated effort:** 8 h · **Depends on:** 05, 06 · **Next:** 08

---

## What this module is about

ML systems fail in ways conventional tests never see: the code runs, the types
are right, and the *answers* quietly get worse. This module builds the test
practices that catch exactly that — five kinds of test, in layers:

| Layer | Question it answers |
|---|---|
| **Unit** | Does this function do what its name says? |
| **Data** | Is the input what we claim it is? |
| **Model** | Is quality still above the floor we committed to? |
| **Integration** | Does the whole path work end to end? |
| **Regression** | Did a change make something worse than before? |

You will run a real suite in the shared example: **19 tests, passing in ~4
seconds**, with a coverage report — and you will watch a performance gate fail
on purpose, because a test you have never seen fail is a test you cannot trust.

## How to study this module (in order)

| # | File | What it does | Time |
|---|---|---|---|
| 1 | [learning-objectives.md](learning-objectives.md) | What you must be able to do, and how you prove it | 10 min |
| 2 | [concepts.md](concepts.md) | The five layers, fixtures, coverage, determinism, gates | 120 min |
| 3 | [worked-example.md](worked-example.md) | The real suite run, its coverage table, and a real failure | 40 min |
| 4 | [lab.md](lab.md) | **Guided lab:** build the safety net | 120 min |
| 5 | [independent-challenge.md](independent-challenge.md) | Audit a colleague's weak test suite, finish it, and prove a seeded bug is caught | 90 min |
| 6 | [knowledge-check.md](knowledge-check.md) | 10 questions with reasoning | 30 min |
| 7 | [troubleshooting.md](troubleshooting.md) | pytest failures, flaky tests, coverage confusion | as needed |
| 8 | [references.md](references.md) | pytest, coverage, and testing-for-ML sources | optional |

## Before you start

- Modules 05–06 completed (a working pipeline and tracked runs).
- `pytest` and `pytest-cov` installed (verified with pytest 9.1.1).
- Free, local, no accounts — the whole suite runs offline.

## Evidence you should produce

1. A test suite with counts by layer, a green run, and a coverage report.
2. A bug-catch matrix: three seeded defects → the test that caught each.
3. One documented failing run (your deliberate performance-gate failure) with
   its output.

---

[← Module 06](../06-experiment-tracking-mlflow/index.md) · [Full syllabus](../../syllabus/detailed-syllabus.md#module-07-unit-data-model-integration-and-regression-testing) · [Module 08 →](../08-pipeline-automation/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*