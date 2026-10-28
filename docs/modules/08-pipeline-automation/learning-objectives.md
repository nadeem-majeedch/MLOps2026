# Learning objectives — Module 08

By the end of this module you can do the following, each with the evidence
listed beside it. These map to the syllabus outcomes
[LO 8.1–8.4](../../syllabus/detailed-syllabus.md#module-08-pipeline-automation-and-workflow-dependencies).

| # | You can… | You prove it by… |
|---|---|---|
| **8.1** | Express a multi-stage ML workflow as declared tasks with explicit inputs, outputs, and dependencies | `python -m pipe.run --list` printing your own graph, and a second run resolving the same topological order |
| **8.2** | Re-run only the stages whose inputs changed (incremental execution) | A run log where unchanged stages print `SKIP (up to date)` and a changed one prints `RUN` |
| **8.3** | Recover from a failed stage and prove the workflow resumes correctly | A run that exits `1` with `FAILED` + `BLOCKED` lines, a `failed` entry in `manifest.json`, and a follow-up run that picks up where it stopped |
| **8.4** | Rebuild the entire pipeline from scratch on a clean machine with one command | `python -m pipe.run --clean` producing `pipe_out/report.md` with hashes matching your previous clean build |

## Supporting skills

- Explain *why* a stage is skipped: name the three inputs to that decision
  (input file hashes, stage source hash, output file hashes).
- Distinguish **idempotent** ("safe to run twice") from **incremental**
  ("skipped when nothing changed") — the runner needs both.
- Describe the artefact flow: which file each stage reads and writes, and what
  breaks if one stage writes to the wrong place.

## Self-check questions

Before the lab, you should be able to answer without looking:

1. In what order does the runner execute `report, evaluate, train, features, validate, generate`?
2. What makes a stage re-run after you only *deleted* one of its output files?
3. Why do downstream stages print `BLOCKED` instead of attempting to run?
4. What is stored in `manifest.json`, and who reads it?

*(Answers appear in [knowledge-check.md](knowledge-check.md) — attempt first.)*

---

[← Module 08 index](index.md) · [Next: concepts →](concepts.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*