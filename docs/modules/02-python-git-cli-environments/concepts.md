# Concepts — Module 02

Three mechanics, in the order you need them: the **command line**, the
**environment**, and **version control**. Each is small on its own; together they
are the difference between "works on my machine" and "works".

---

## 1. The command line

A **shell** is a program that takes the commands you type and runs other
programs. The **command-line interface (CLI)** is the whole arrangement: you
type, it executes, and the answer comes back as text.

Two shells matter in this course:

| Shell | Platform | Style | Label |
|---|---|---|---|
| **PowerShell** | Windows (built in) | `Verb-Noun` cmdlets: `Get-Location`, `Get-ChildItem` | 🪟 primary |
| **bash** | Linux/macOS (built in); Git Bash on Windows | short verbs: `pwd`, `ls` | 🐧 alternative |

**Concepts you need (they are all the same idea):**

- **Working directory** — the folder your commands act on *right now*.
  `Get-Location` 🪟 / `pwd` 🐧 prints it. Almost every beginner bug is "I was in
  the wrong folder".
- **Path** — how a file is addressed: `\`-separated on Windows
  (`data\raw\churn.csv`), `/`-separated elsewhere (`data/raw/churn.csv`).
  Forward slashes usually work in Python on Windows; backslashes do not work in
  bash. Use `/` in code, and the right separator in shell commands.
- **Exit code** — every command returns a number: `0` means success, anything
  else is a failure reason. `echo $LASTEXITCODE` 🪟 / `echo $?` 🐧. Scripts and
  CI depend on this — you will use it constantly from Module 07 onward.
- **Running Python** — `python` runs the default interpreter; `py -3` is
  Windows' launcher for a specific version. A shell may have an interpreter you
  did not install (the Microsoft Store alias is the classic trap). The reliable
  check is `python -c "import sys; print(sys.executable)"`, which prints *exactly*
  which interpreter is answering.

!!! note "Why PowerShell is primary here"
    Because the course must work on a student's Windows 11 laptop with nothing
    installed. The 🐧 blocks are not decoration — the same task in bash is shown
    every time, because the *concepts* are identical and the *syntax* is not.

---

## 2. Environments: why two Pythons disagree

An **environment** is a Python installation plus the packages installed into it.
By default, everything you `pip install` goes into one shared location — so
project A and project B fight over package versions.

A **virtual environment** (`.venv/`) is a private, project-local environment:
its own interpreter copy, its own site-packages, and no effect on anything else.

**Activation** makes a shell use that environment:

```powershell
# 🪟 Windows
.\.venv\Scripts\Activate.ps1
```

```bash
# 🐧 Linux / macOS
source .venv/bin/activate
```

You can always bypass activation and address the interpreter directly — which is
what the course scripts do, because it cannot go wrong:

```powershell
# 🪟 unambiguous, no activation needed
.venv\Scripts\python -m pip install pandas
```

### Dependencies, versions, and pins

- A **dependency** is a package your project needs.
- A **version range** (`pandas>=2.0`) says "any compatible version" — good for
  *declaring* what you need.
- A **pin** (`pandas==3.1.0`) says "exactly this" — good for *reproducing* what
  you got.
- A **lock file** is the full, exact list of everything installed, so a rebuild
  produces the same environment.

!!! warning "The experiment you will run yourself"
    On the reference machine, the *system* Python had **pandas 3.0.6** while a
    freshly created `.venv` installed **pandas 3.1.0** — same laptop, same day,
    different results waiting to happen. That disagreement is exactly what pinning
    removes. You reproduce this in [worked-example.md](worked-example.md).

`pyproject.toml` declares your project's dependencies; `pip freeze > requirements.lock`
(or `uv pip compile`) turns what actually happened into pins. Module 05 makes
this concrete: the *same* code with *different* dependencies is a different
experiment.

---

## 3. Version control: Git

**Version control** records how files changed over time, so any state can be
recovered and any change explained. Git is the standard; the mental model matters
more than the commands.

| Concept | What it is | Everyday command 🪟/🐧 |
|---|---|---|
| **Repository** | The project folder plus its history (`.git/`) | `git init` (start), `git clone <url>` (copy) |
| **Snapshot (commit)** | A named, permanent point in history | `git commit -m "why, not what"` |
| **Staging area** | The shortlist of changes the next commit will include | `git add <file>`, `git status` |
| **Branch** | A movable label for a line of history, used to develop in parallel | `git branch <name>`, `git switch <name>` |
| **Merge** | Joining two lines of history | `git merge <branch>` |
| **Conflict** | Both branches changed the same lines; a human must choose | edit the marked file, `git add`, `git commit` |
| **Remote** | A copy of the repository elsewhere (GitHub) | `git push`, `git pull` |
| **`.gitignore`** | Rules for files Git must never track | patterns, one per line |

**Rules that prevent almost all beginner pain:**

1. **Commit small, commit often.** Each commit should be one coherent change
   with a message saying *why*.
2. **Never `git add -A` blindly.** Read `git status` first: generated data,
   secrets, and virtual environments must never enter history.
3. **History is shared; rewriting it is dangerous.** This course never asks you
   to force-push, and neither should you, on shared work.
4. **`git status` is your ground truth.** Confused? Run it. It tells you exactly
   what is staged, modified, or untracked.

**What Git does *not* version:** large data files. A 2 GB dataset should not be
committed — that is what data versioning (Module 04, DVC) is for. Learn the
boundary now: **Git versions code; DVC versions data.**

---

## 4. The reproducible-environment recipe

This is the workflow the lab drills:

1. Declare dependencies in `pyproject.toml` (ranges are fine here).
2. Create a fresh environment: `python -m venv .venv`.
3. Install your project into it: `.venv/Scripts/python -m pip install -e .`
   🪟 (or `python3 -m pip install -e .` 🐧).
4. Record exact versions: `.venv/Scripts/python -m pip freeze > requirements.lock`.
5. Commit `pyproject.toml`, `requirements.lock`, and `.gitignore` — never `.venv/`.
6. Verify with a command, not a memory: run your script/tests and compare output.

Steps 3–4 are where "it worked last week" is either destroyed or preserved.

---

## 5. Tool-specific behaviour vs. general principles

| General principle (portable) | Specific to this course's tools |
|---|---|
| Dependencies must be declared and pinned | `pyproject.toml` + `pip freeze`; `uv`, poetry, conda are equally valid |
| Environments must be isolated | `venv` activation syntax differs per OS; conda uses `conda activate` |
| History must be recoverable | Git's index/staging model is Git-specific — other VCSs have simpler models |
| Generated files must stay out of history | `.gitignore` patterns are Git syntax |
| The primary path here is Windows | 🐧 commands are the same ideas, different verbs |

Versions verified for this module: **Git 2.56**, **Python 3.14**, **Windows 11**.
If a flag differs on your machine, the official docs in
[references.md](references.md) win — and please report it as a course issue.

---

## Check yourself

1. You double-click a script and it "runs", but your changes have no effect.
   Which concept explains it — and which command tells you the truth?
2. What is the difference between `pandas>=2.0` and `pandas==3.1.0`, and which
   belongs in a lock file?
3. Why is `.venv/` in `.gitignore`, while `pyproject.toml` is not?
4. Your teammate committed a 400 MB data file. Which module's tool should have
   been used instead, and what do you do now?
5. What does an exit code of `1` tell you, and who uses it?

*(Answers in [knowledge-check.md](knowledge-check.md) — try there first.)*

---

**Next:** [worked-example.md](worked-example.md) — build an environment for real, then watch two environments disagree.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*