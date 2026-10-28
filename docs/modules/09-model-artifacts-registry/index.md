# Module 09 — Model artifacts, registries, promotion, and lifecycle management

!!! success "Module complete"
    Lessons, worked example, lab, independent challenge, knowledge check (with
    answers), troubleshooting, and references are all written.

**Stage:** Intermediate · **Estimated effort:** 8 h · **Depends on:** 06, 08 · **Next:** 10

---

## What this module is about

A trained model is not a file — it is a **file plus the story of how it was
made and whether it is allowed to serve**. This module builds that story into
a working registry:

| Concept | What you build here |
|---|---|
| **Artefact** | `model.joblib` + metrics + data hash + gate result, stored together per version |
| **Version** | `v001`, `v002`, `v003` — immutable, never edited in place |
| **Lineage** | which data, config, and gate produced each version |
| **Promotion** | `development → staging → production`, one step at a time, refused without a passed gate |
| **Rollback** | `python -m registry rollback production` — a recorded, one-command way back |
| **Lifecycle** | stages, history, retirement — with a human approving every move |

Everything runs on **plain local files** so it works offline. The module is
explicit about where the local demonstration stops and where a real remote
registry service (MLflow Model Registry behind a tracking server) begins.

## How to study this module (in order)

| # | File | What it does | Time |
|---|---|---|---|
| 1 | [learning-objectives.md](learning-objectives.md) | What you must be able to do, and how you prove it | 10 min |
| 2 | [concepts.md](concepts.md) | Artefacts, lineage, stages, promotion, rollback, model cards | 110 min |
| 3 | [worked-example.md](worked-example.md) | Real registry runs: refusals, promotion, rollback, audit trail | 40 min |
| 4 | [lab.md](lab.md) | **Guided lab:** ship v1, prepare the rollback | 130 min |
| 5 | [independent-challenge.md](independent-challenge.md) | Write the model card and defend two promotion decisions | 75 min |
| 6 | [knowledge-check.md](knowledge-check.md) | 10 questions with reasoning | 30 min |
| 7 | [troubleshooting.md](troubleshooting.md) | Refused promotions, lost pointers, missing lineage | as needed |
| 8 | [references.md](references.md) | MLflow registry docs, model-card and ML-validation sources | optional |

## Before you start

- Module 08 complete: `python -m pipe.run --clean` produces a gated report.
- You know where `pipe_out/` and `config.yaml` live.
- Free, local, no accounts. (The MLflow *remote* registry is ☁️ optional reading.)

## Evidence you should produce

1. A populated registry: ≥2 registered versions with lineage metadata.
2. The full promotion + rollback transcript, including **both refusals**
   (skipping a stage, and promoting an ungated version).
3. A model card for the production version covering intended use, limits,
   evaluation, and the rollback command.

---

[← Module 08: Pipeline automation](../08-pipeline-automation/index.md) · [Full syllabus](../../syllabus/detailed-syllabus.md#module-09-model-artifacts-registries-promotion-and-lifecycle-management) · [Module 10 →](../10-model-serving-fastapi/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*