# Knowledge check — Module 02

Attempt every question first. **10 questions · ~30 minutes · open book.**
Suggested pass mark **7/10**, with no question about environments wrong.

---

## Part A — Recall

**Q1.** Define: *virtual environment*, *dependency*, *lock file*, *pin*.

**Q2.** What do these print, and why would you care?
`python -c "import sys; print(sys.executable)"`

**Q3.** Explain the four areas Git distinguishes: working directory, staging
area, repository (history), and remote.

**Q4.** What belongs in `.gitignore` for a Python ML project? Name four things
and justify one.

## Part B — Comprehension

**Q5.** On one laptop, `pandas==3.0.6` is installed system-wide while a fresh
`.venv` gets `pandas==3.1.0`. Why can this change your results, and which single
file prevents the surprise?

**Q6.** A teammate runs `pip install -r requirements.txt` and their tests still
fail with `ModuleNotFoundError`. Give two possible causes and the command that
distinguishes them.

**Q7.** Why is `git add -A` dangerous on an ML project, and what should you do
instead?

**Q8.** Your teammate commits code but never `.gitignore`s `data/raw/`, so a 400 MB
CSV enters history. Why is this worse than it looks, and which Module 04 tool is
the correct home for that file?

## Part C — Application

**Q9.** Write the exact command sequence (🪟 PowerShell **and** 🐧 bash) that
creates an environment, installs a project, records the lock file, and runs its
tests, from a fresh clone.

**Q10.** Your script runs fine for you and produces a different number for a
colleague. Walk through, in order, the four reproducibility leaks from Module 01
and state which check you would run for each.

---

# Answers and reasoning

**Q1 — 1 point.**
*Virtual environment* = a project-local Python installation (own interpreter copy
and site-packages). *Dependency* = a package your project needs. *Pin* = an exact
version (`==3.1.0`). *Lock file* = the complete list of exact versions actually
installed, sufficient to rebuild the environment.
*Reasoning:* a declaration (`pyproject.toml`) expresses intent; a lock expresses
fact. Reproducibility needs both.

**Q2 — 1 point.**
It prints the full path of the interpreter that is actually running — the only
reliable answer to "which Python am I using?".
*Reasoning:* `which python`/`where.exe` tell you what *could* run; `sys.executable`
tells you what *did*. Every environment bug resolves to a disagreement between
the two.

**Q3 — 1 point.**
Working directory = files as they currently are. Staging area = the shortlist for
the next commit. Repository/history = committed snapshots, permanent and shared.
Remote = another copy (e.g. GitHub) you sync with push/pull.
*Reasoning:* confusion here causes "why is my change not in the commit?" (not
staged) and "why is my file in Git?" (staged accidentally).

**Q4 — 1 point (¼ each + justification).**
`.venv/` (huge, machine-specific, rebuildable); generated data
(`data/raw/`, `data/corrupt/`) — *justification: regenerable from a script, and
bloats clones*; artefacts (`artifacts/`, `mlruns/`, `*.joblib`, `model.pkl`);
environment noise (`__pycache__/`, `.pytest_cache/`, `.coverage`).
*Reasoning:* the test is "can it be recreated, and does it belong in a diff?"

**Q5 — 1 point.**
Different environments install different versions by default; library behaviour
can change between versions, so the same code may produce different numbers.
`requirements.lock` (plus `pyproject.toml`) prevents it by pinning what is used.
*Reasoning:* this is exactly the observed disagreement in
[worked-example.md](worked-example.md) §6.

**Q6 — 1 point (0.5 per cause).**
(a) The install ran in a *different* interpreter than the tests — check
`sys.executable` for both. (b) The package genuinely is not in the requirements
file (never declared) — check the file, then `pip install` into the correct
environment. The distinguishing command: run
`.venv\Scripts\python -c "import <pkg>"` 🪟 / `.venv/bin/python -c "import <pkg>"` 🐧.

**Q7 — 1 point.**
It stages *everything*, including virtual environments, generated data, secrets,
and artefacts — which pollute history permanently and may leak credentials.
Instead: `git status`, then `git add <specific paths>`.
*Reasoning:* history is append-only in normal use; the cost of a careless add is
paid forever (and secrets are rotated in Module 15).

**Q8 — 1 point.**
Worse than it looks because Git keeps every version of that blob forever — clone
size, CI checkout time, and GitHub's file limits all suffer, and history cannot
be cheaply rewritten without disturbing collaborators.
Correct home: **DVC** (Module 04), which versions data outside Git while Git
keeps the small pointer file.
*Reasoning:* boundary rule — Git versions code, DVC versions data.

**Q9 — 1 point (½ per shell).**
🪟:
```powershell
git clone <url> myproj; Set-Location myproj
python -m venv .venv
.venv\Scripts\python -m pip install -e ".[dev]"
.venv\Scripts\python -m pip freeze > requirements.lock
.venv\Scripts\python -m pytest; echo $LASTEXITCODE
```
🐧: replace with `cd myproj`, `python3 -m venv .venv`,
`.venv/bin/python -m pip …`, `echo $?`.
*Reasoning:* every install/run must name the same interpreter; that single habit
prevents the entire class of "works on my machine".

**Q10 — 1 point (0.25 each).**
Randomness → check `random_state`/seed is set and recorded. Environment →
compare the two `pip freeze` files. Data → compare file hashes/versions (M04).
Code → `git log`/`git status` to see whether the running code matches the
committed code. If all four match, the difference must be in inputs you have not
thought of — external services, platform — which you then isolate.
*Reasoning:* a systematic checklist beats random guessing; this order goes from
cheapest to check to most expensive.

---

## Marking and next steps

| Score | Action |
|---|---|
| **9–10** | Proceed to Module 03 |
| **7–8** | Re-read the missed concepts sections, then continue |
| **5–6** | Redo the lab from step 3 with a *fresh* `.venv`, then re-take |
| **< 5** | Re-read concepts §2–§3 and re-run the worked example first |

File your score in the portfolio (`modules/02/knowledge-check.md`).

---

[← Module overview](index.md) · [Troubleshooting →](troubleshooting.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*