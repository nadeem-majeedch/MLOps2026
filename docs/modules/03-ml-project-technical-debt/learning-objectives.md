# Learning objectives — Module 03

## Objectives

| ID | By the end of this module you can… | Prove it by… |
|---|---|---|
| **LO 3.1** | Apply a standard ML repository layout (data, src, notebooks, models, tests, docs) | Your restructured project matching the layout, with every folder explained |
| **LO 3.2** | Classify examples of ML technical debt (data dependencies, entanglement, undeclared consumers, configuration debt) | A debt audit listing ≥5 items, each with type, cost, and staged fix |
| **LO 3.3** | Convert an exploratory notebook into a maintainable project without losing results | `python run.py` reproducing the notebook's exact number |
| **LO 3.4** | Justify each structural decision in a short design note | A one-page note where every "why" is answered, not asserted |

## What "good" looks like

- **Pass:** the number the notebook produced is reproduced by a single command
  from a clean checkout, the layout follows the convention, and your design note
  explains at least three decisions by their *cost* if reversed.
- **Not yet:** the refactored project "works" but the numbers changed, or the
  README is required to run it. Refactor again — the result must survive being
  handed to someone else.

## Vocabulary you must be able to use after this module

**technical debt**, **entanglement**, **hidden feedback loop**,
**undeclared data dependency**, **configuration debt**, **notebook hygiene**,
**separation of concerns**, **entry point**, **single source of truth**,
**data dictionary**, **magic number**, **side effect**.

## How this module is assessed

- **Practical (graded):** the restructure against the rubric in
  [assessment-framework.md](../../syllabus/assessment-framework.md#6-project-rubric-mini-projects) —
  this module also delivers **mini-project MP1**.
- **Knowledge check:** 10 questions — [knowledge-check.md](knowledge-check.md).

---

[← Module overview](index.md) · [Concepts →](concepts.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*