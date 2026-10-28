# Module 02 — Python, Git, CLI, and reproducible environments

!!! success "Module complete"
    Lessons, worked example, lab, independent challenge, knowledge check (with
    answers), troubleshooting, and references are all written.

**Stage:** Foundations (beginner) · **Estimated effort:** 8 h · **Depends on:** 01 · **Next:** 03

---

## What this module is about

Everything else in this course assumes you can answer one question with evidence:
*"if someone else ran my code, would they get my result?"* That requires three
mechanics — a **command line** to drive tools, a **version-controlled repository**
to freeze code, and an **isolated environment** to freeze dependencies.

This module is deliberately unglamorous. It is also the module students most
often skip and most often regret skipping.

## How to study this module (in order)

| # | File | What it does | Time |
|---|---|---|---|
| 1 | [learning-objectives.md](learning-objectives.md) | What you must be able to do, and how you prove it | 10 min |
| 2 | [concepts.md](concepts.md) | Shells, environments, dependency pinning, the Git mental model | 110 min |
| 3 | [worked-example.md](worked-example.md) | Build a real environment, and watch two environments disagree | 40 min |
| 4 | [lab.md](lab.md) | **Guided lab:** rebuild a teammate's environment from scratch | 110 min |
| 5 | [independent-challenge.md](independent-challenge.md) | Make an old script of yours reproducible | 60 min |
| 6 | [knowledge-check.md](knowledge-check.md) | 10 questions with reasoning | 30 min |
| 7 | [troubleshooting.md](troubleshooting.md) | venv, PATH, interpreter, and Git problems | as needed |
| 8 | [references.md](references.md) | Official docs for Python, pip, Git, and `uv` | optional |

## Before you start

- [Prerequisites](../../prerequisites/index.md): Python 3.10+, Git installed,
  comfort typing commands.
- Module 01 completed (lifecycle vocabulary).
- Free and local throughout: **no account is required for this module's graded
  path** — a GitHub account is only needed later (Module 12).

## Evidence you should produce

1. A repository containing a pinned environment (`pyproject.toml`) and a README
   that lets a stranger rebuild it.
2. A lab report of the two deliberate breakages you fixed, each with symptom →
   cause → fix.
3. Your knowledge-check score.

---

[← Module 01](../01-introduction-mlops-lifecycle/index.md) · [Full syllabus](../../syllabus/detailed-syllabus.md#module-02-python-git-cli-and-reproducible-environments) · [Module 03 →](../03-ml-project-technical-debt/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*