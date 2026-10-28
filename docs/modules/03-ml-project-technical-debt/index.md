# Module 03 — Organizing an ML project and understanding technical debt

!!! success "Module complete"
    Lessons, worked example, lab, independent challenge, knowledge check (with
    answers), troubleshooting, and references are all written.

**Stage:** Foundations (beginner) · **Estimated effort:** 7 h · **Depends on:** 02 · **Next:** 04

---

## What this module is about

The difference between a script that works and a project that lasts is
**structure**: where code lives, where configuration lives, what the single
entry point is, and what a stranger reads first. Poor structure is not a style
issue — it is **technical debt**, and in ML it compounds faster than anywhere
else because the data underneath keeps moving.

This module takes a real messy notebook from the course's shared project and
turns it into a small, honest repository — without changing a single number it
produces.

## How to study this module (in order)

| # | File | What it does | Time |
|---|---|---|---|
| 1 | [learning-objectives.md](learning-objectives.md) | What you must be able to do, and how you prove it | 10 min |
| 2 | [concepts.md](concepts.md) | Structure rationale, the technical-debt taxonomy, notebook hygiene | 100 min |
| 3 | [worked-example.md](worked-example.md) | The same analysis as notebook and as a project — identical numbers | 40 min |
| 4 | [lab.md](lab.md) | **Guided lab:** rescue the spaghetti notebook | 100 min |
| 5 | [independent-challenge.md](independent-challenge.md) | Audit a real codebase for ML technical debt | 50 min |
| 6 | [knowledge-check.md](knowledge-check.md) | 10 questions with reasoning | 30 min |
| 7 | [troubleshooting.md](troubleshooting.md) | Path, import, and notebook problems | as needed |
| 8 | [references.md](references.md) | The debt papers and project-layout references | optional |

## Before you start

- Module 02 completed — you must be able to create an environment and commit with Git.
- The shared example's notebook: [`examples/churn/legacy/analysis.ipynb`](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/churn/legacy)
  (a deliberately messy but **working** file — it produces a real number you must match).
- Free, local, no accounts.

## Evidence you should produce

1. The restructured project: `run.py` reproducing the notebook's number from a
   clean checkout (the lab states it exactly).
2. A one-page design note justifying each structural choice.
3. A technical-debt audit list (challenge) with cause → cost → staged fix.

---

[← Module 02](../02-python-git-cli-environments/index.md) · [Full syllabus](../../syllabus/detailed-syllabus.md#module-03-organizing-an-ml-project-and-understanding-technical-debt) · [Module 04 →](../04-data-quality-validation-versioning/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*