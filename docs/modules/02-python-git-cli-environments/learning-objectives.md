# Learning objectives — Module 02

## Objectives

| ID | By the end of this module you can… | Prove it by… |
|---|---|---|
| **LO 2.1** | Navigate a project folder and run programs from PowerShell (🪟) and bash (🐧) | Running the lab's commands from both shells, or explaining the equivalent |
| **LO 2.2** | Create and activate an isolated Python environment and pin installed package versions | A fresh `.venv` built from `pyproject.toml` with `pip freeze` output recorded |
| **LO 2.3** | Use Git to snapshot work, inspect history, and branch for an experiment | A repository with ≥5 meaningful commits and one merged experiment branch |
| **LO 2.4** | Reproduce a colleague's result from a fresh clone using only the recorded setup | The lab's rebuild task: clone → install → run → identical output |

## What "good" looks like

- **Pass:** a clean machine (or clean folder) can be rebuilt from your repository
  and reproduce the stated output, with no undocumented step.
- **Not yet:** rebuilding requires you to remember something you never wrote down.
  That is precisely the failure this module exists to remove.

## Vocabulary you must be able to use after this module

**CLI / shell**, **PowerShell**, **bash**, **working directory**, **path**,
**virtual environment**, **interpreter**, **dependency**, **lock file**,
**pin**, **version control**, **repository**, **commit**, **staging area**,
**branch**, **merge**, **conflict**, **`.gitignore`**, **reproducible
environment**, **semantic versioning**.

Defined in [concepts.md](concepts.md); collected in the course
[glossary](../../glossary/index.md).

## How this module is assessed

- **Practical lab** (graded): the environment rebuild with two deliberate
  breakages fixed — [lab.md](lab.md) §9.
- **Knowledge check:** 10 questions — [knowledge-check.md](knowledge-check.md).

---

[← Module overview](index.md) · [Concepts →](concepts.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*