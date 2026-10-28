# Module 04 — Data quality, validation, and data versioning

!!! success "Module complete"
    Lessons, worked example, lab, independent challenge, knowledge check (with
    answers), troubleshooting, and references are all written.

**Stage:** Foundations (beginner) · **Estimated effort:** 8 h · **Depends on:** 02, 03 · **Next:** 05

---

## What this module is about

Code has compilers and tests; data has… nothing, by default. A renamed column, a
locale that writes `1,234`, a silently re-exported CSV — each one breaks an ML
pipeline *after* the code has already passed its checks.

This module teaches two defences:

1. **Data validation** — declare what your data must satisfy, then fail loudly
   when it does not. You will write checks that catch three seeded defects.
2. **Data versioning** — freeze the exact bytes an experiment used, so "which
   data produced this result?" has an answer. Taught as a *principle* first
   (hashes), then as a tool (DVC) — because you already know Git from Module 02.

## How to study this module (in order)

| # | File | What it does | Time |
|---|---|---|---|
| 1 | [learning-objectives.md](learning-objectives.md) | What you must be able to do, and how you prove it | 10 min |
| 2 | [concepts.md](concepts.md) | Validation, schemas, contracts, versioning, lineage — principle before tool | 120 min |
| 3 | [worked-example.md](worked-example.md) | Your validator run against four real files, with actual output | 35 min |
| 4 | [lab.md](lab.md) | **Guided lab:** gate the incoming dataset (catch three defects, then version it) | 120 min |
| 5 | [independent-challenge.md](independent-challenge.md) | Design a data contract for data you choose | 55 min |
| 6 | [knowledge-check.md](knowledge-check.md) | 10 questions with reasoning | 30 min |
| 7 | [troubleshooting.md](troubleshooting.md) | pandas, CSV, and DVC problems (including a real DVC refusal) | as needed |
| 8 | [references.md](references.md) | pandas, pandera, Great Expectations, DVC docs | optional |

## Before you start

- Module 02 (environment + Git) and Module 03 (project structure) completed.
- Python with pandas; DVC is installed for the lab's second half
  (`python -m dvc --version` must print a version).
- **Order matters:** DVC is introduced *after* Git and data reproducibility,
  because it is a Git-shaped tool for a data-shaped problem.

## Evidence you should produce

1. A validation report for three extracts: one passes, two fail with readable messages.
2. A versioned dataset: a `.dvc` pointer file whose recorded hash matches your file.
3. A written data contract (challenge) with schema, thresholds, and licence.

---

[← Module 03](../03-ml-project-technical-debt/index.md) · [Full syllabus](../../syllabus/detailed-syllabus.md#module-04-data-quality-validation-and-data-versioning) · [Module 05 →](../05-reproducible-training-pipelines/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*