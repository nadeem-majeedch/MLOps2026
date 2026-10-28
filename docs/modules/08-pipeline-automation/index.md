# Module 08 — Pipeline automation and workflow dependencies

!!! success "Module complete"
    Lessons, worked example, lab, independent challenge, knowledge check (with
    answers), troubleshooting, and references are all written.

**Stage:** Intermediate · **Estimated effort:** 8 h · **Depends on:** 07 · **Next:** 09

---

## What this module is about

Your pipeline works — but only when *you* remember the order of the commands.
This module turns those commands into a **declared workflow**: named stages,
explicit inputs and outputs, and dependencies the machine resolves for you.

You will build a real runner in the shared example (`pipe/`) that does four
things a human shell history cannot:

| Capability | What it means |
|---|---|
| **Dependency graph** | `evaluate` needs `train`; the runner knows, you don't have to |
| **Incremental execution** | a stage re-runs only when its inputs, its code, or its outputs changed |
| **Failure handling** | one failing stage stops the run, records why, and never runs downstream stages |
| **One-command rebuild** | `python -m pipe.run --clean` rebuilds everything from nothing |

The measured result you will reproduce: a six-stage graph where a second run
**skips all six stages in under a second**, and where editing one function
re-runs **exactly one** stage.

## How to study this module (in order)

| # | File | What it does | Time |
|---|---|---|---|
| 1 | [learning-objectives.md](learning-objectives.md) | What you must be able to do, and how you prove it | 10 min |
| 2 | [concepts.md](concepts.md) | Stages, DAGs, hashing, idempotency, artefact flow, gates | 110 min |
| 3 | [worked-example.md](worked-example.md) | Real runs: full build, skips, tamper, failure, resume | 45 min |
| 4 | [lab.md](lab.md) | **Guided lab:** one command to rebuild everything | 130 min |
| 5 | [independent-challenge.md](independent-challenge.md) | Add a stage to the graph and prove correct incremental behaviour | 75 min |
| 6 | [knowledge-check.md](knowledge-check.md) | 10 questions with reasoning | 30 min |
| 7 | [troubleshooting.md](troubleshooting.md) | Skips that should not skip, failures that will not resume | as needed |
| 8 | [references.md](references.md) | Make, Snakemake, Nextflow, DVC docs, and the papers | optional |

## Before you start

- Module 07 finished (its test suite protects the code you are about to automate).
- The example project runs: `python generate_data.py && python -m pytest` is green.
- Free, local, no accounts — the runner is plain Python (no Make required).

## Evidence you should produce

1. The three run logs: incremental (all SKIP), clean rebuild (all RUN), failure + resume.
2. Your `pipe_out/manifest.json` showing one recorded `failed` status with its error text.
3. The artefact hashes from `pipe_out/report.md`, reproducible on a second run.

---

[← Module 07: Testing for ML systems](../07-testing-for-ml/index.md) · [Full syllabus](../../syllabus/detailed-syllabus.md#module-08-pipeline-automation-and-workflow-dependencies) · [Module 09 →](../09-model-artifacts-registry/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*