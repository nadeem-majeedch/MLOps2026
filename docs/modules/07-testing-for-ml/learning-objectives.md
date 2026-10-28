# Learning objectives — Module 07

## Objectives

| ID | By the end of this module you can… | Prove it by… |
|---|---|---|
| **LO 7.1** | Write unit tests for the functions in an ML pipeline, including failure-path tests | ≥6 unit tests covering loading, splitting, and preprocessing behaviour |
| **LO 7.2** | Write data tests (schema, distribution sanity) and model tests (performance floors, invariance) | Data tests failing on a deliberately corrupted file; a floor test that fails when the threshold is unreachable |
| **LO 7.3** | Build an integration test that runs a miniature end-to-end pipeline | A test that goes CSV → train → artefacts → reload → predict |
| **LO 7.4** | Add a regression test that fails when a metric degrades, and use coverage to find untested code | A recorded failing run with its output, plus a coverage report with a written reading of the gaps |

## What "good" looks like

- **Pass:** the suite runs in seconds, is deterministic, and you can name which
  test guards which failure — including at least one test you have *seen fail*.
- **Not yet:** tests exist but you cannot say what they protect, or a seeded
  defect passes through all of them.

## Vocabulary you must be able to use after this module

**unit test**, **data test**, **model test**, **integration test**,
**regression test**, **performance floor**, **test fixture**, **coverage**,
**invariance test**, **deterministic test**, **flaky test**, **test gate**,
**assertion**, **seeded bug**, **CI-ready suite**.

## How this module is assessed

- **Practical lab** (graded): suite by layer + three seeded bugs caught + one
  documented failure — [lab.md](lab.md) §9.
- **Knowledge check:** 10 questions — [knowledge-check.md](knowledge-check.md).

!!! note "Verified baseline for this module"
    The course suite at the time of writing: **19 tests, 3.9 s, 78% line
    coverage of `src/`** (pytest 9.1.1, pytest-cov). Your target is not to match
    those numbers — it is to beat the *structure*: tests by layer, all green,
    with the gaps understood.

---

[← Module overview](index.md) · [Concepts →](concepts.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*