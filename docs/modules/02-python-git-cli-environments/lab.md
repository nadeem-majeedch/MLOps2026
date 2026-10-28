# Lab 02 — Rebuild a teammate's environment

## 1. Scenario and business problem

A teammate has sent you their project folder and says: *"it works on my machine —
can you run the tests and tell me if the numbers match?"* There is no Slack
history, no call, and no chance to ask questions. You have only what they
committed.

**Business problem:** knowledge trapped in one person's head is a single point of
failure. If the rebuild only works when the author is present, the project is
not reproducible — it is merely remembered.

## 2. Skills practised

- Creating and using a virtual environment from a declared set of dependencies.
- Verifying an environment with version checks instead of assumptions.
- Using Git to inspect what was actually shared (and what was left out).
- Diagnosing two seeded failures: a missing dependency, and an untracked file.

## 3. Prerequisites

- [concepts.md](concepts.md) read (§1–§4).
- Python 3.10+ and Git installed — [prerequisites](../../prerequisites/index.md).

## 4. Required tools and estimated time

| Item | Detail |
|---|---|
| Tools | Python 3.10+, pip, Git, PowerShell 🪟 (or bash 🐧) |
| ⚠️ Resource-heavy | First dependency install can take 5–10 minutes and ~1.5 GB |
| Cost | Free, local, no accounts |
| ⏱️ Estimated time | 110 minutes |

## 5. Input data and how to obtain it

No download. Use the course's shared example project as your "teammate's
repository":

```powershell
# 🪟 Windows / PowerShell — from the repository root
Copy-Item -Recurse examples\churn .\lab02-rebuild
```

```bash
# 🐧 Linux / macOS
cp -r examples/churn lab02-rebuild
```

## 6. Directory layout (what you received)

```
lab02-rebuild/
├── pyproject.toml      # declares dependencies (the only instructions you get)
├── config.yaml         # project configuration
├── generate_data.py    # makes the dataset
├── src/                # the code
├── tests/              # the tests you must get passing
├── legacy/             # old notebook (ignore for now)
└── README.md           # how to run it
```

`.venv/`, `data/`, and `artifacts/` are **absent on purpose** — they are
generated, and a teammate should never send them.

## 7. Setup and execution steps

**Step 1 — Read the instructions you were given.** Open `pyproject.toml` and
`README.md`. Write down the exact dependency list.
✅ **Checkpoint:** you can name every package the project claims to need.

**Step 2 — Prove which interpreter you are about to use.**

```powershell
python --version
python -c "import sys; print(sys.executable)"
```

✅ Expect a version ≥3.10 and a system path.

**Step 3 — Create the environment.**

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
```

✅ **Checkpoint:** `Test-Path .venv\Scripts\python.exe` → `True`.

**Step 4 — Install the declared dependencies.**

```powershell
.venv\Scripts\python -m pip install pandas numpy scikit-learn PyYAML joblib pytest pytest-cov
```

⚠️ This is the slow step (5–10 minutes first time).

**Step 5 — Seeded failure #1: a missing dependency.**

```powershell
.venv\Scripts\python -m pytest
```

*If everything passes here, create the first breakage yourself so you can
practise the fix:* delete one package from the install line, e.g.
`.venv\Scripts\python -m pip uninstall -y PyYAML`, then re-run pytest.

Expected failure shape (yours names the missing module you removed):

```text
E       ModuleNotFoundError: No module named 'yaml'
=========================== short test summary info ===========================
FAILED tests/test_features.py::test_load_config_returns_expected_keys
1 failed, N passed
```

**Diagnose before you fix:** read the last line. Is it `ModuleNotFoundError`?
Then it is an environment problem, not a code problem. Confirm which
interpreter ran: the failure line names the test file, and `python -c "import yaml"`
will fail the same way in `.venv` while succeeding elsewhere — *that difference
is the diagnosis*.

✅ **Fix:** install into the environment you are actually using, with the
`.venv\Scripts\python -m pip install …` prefix — never plain `pip`.

**Step 6 — Seeded failure #2: a file that was never shared.**

A teammate's project fails because something needed was not committed. Create
the situation, then fix it:

```powershell
# 🪟 break it on purpose: remove the generated dataset the tests need
Remove-Item -Recurse data
.venv\Scripts\python -m pytest        # conftest regenerates data automatically — tests still pass
```

Now the real lesson: check what Git would actually track.

```powershell
git init
git add -A
git status --short
```

✅ **Checkpoint:** `.venv/`, `data/`, `artifacts/`, `mlruns/`, `mlflow.db` must
**not** appear (they are covered by `.gitignore`). If they do, the `.gitignore`
is wrong — fix it *before* the first commit, because history is forever.

The inverse failure — a file that *should* be tracked but is ignored — is the one
this lab grades. Verify with:

```powershell
git status --short --ignored
git check-ignore -v config.yaml       # must print nothing for files you need
```

✅ **Fix:** if a required file (e.g. `config.yaml`) is ignored, remove the
offending pattern from `.gitignore`, then confirm `git check-ignore -v <file>`
prints nothing.

**Step 7 — Record the environment you ended up with.**

```powershell
.venv\Scripts\python -m pip freeze > requirements.lock
Get-Content requirements.lock | Select-String 'pandas|scikit-learn|pytest'
```

**Step 8 — Verify the result end to end.**

```powershell
.venv\Scripts\python -m pytest; echo "exit=$LASTEXITCODE"
```

✅ **Checkpoint:** `19 passed`, `exit=0`.

**Step 9 — Write the rebuild report** (this is the graded artefact):

| Section | Content |
|---|---|
| Commands run | The exact sequence, copy-pasted |
| Failure #1 | Symptom → cause → fix (one line each) |
| Failure #2 | Symptom → cause → fix |
| Environment | Python version + `pip freeze` line for pandas |
| Verdict | Did your result match the teammate's claim? |

## 8. Expected outputs and verification

| Step | Expected | Verify by |
|---|---|---|
| 3 | `.venv` exists | `Test-Path .venv\Scripts\python.exe` → `True` |
| 4 | installs complete without errors | pip exits 0 |
| 5 | failing test names the missing module | pytest summary line |
| 6 | ignored paths excluded from staging | `git status --short` omits them |
| 7 | lock file lists exact versions | file contains `pandas==…` |
| 8 | `19 passed`, exit code `0` | printed summary + `echo $LASTEXITCODE` |

Command output shown as *"shape"* rather than literal text is deliberate: dates,
hashes, and counts legitimately differ on your machine. Any output the course
quotes as **actual** was captured from a real run on the reference machine.

## 9. Acceptance criteria

- [ ] Environment created from `pyproject.toml` alone — no undocumented step.
- [ ] Both seeded failures diagnosed and fixed, each written up as
      symptom → cause → fix.
- [ ] `pip freeze` output saved as `requirements.lock` and committed.
- [ ] `git status` clean, with generated paths confirmed **not** staged.
- [ ] Final run: `19 passed`, exit code 0, recorded in the report.
- [ ] Report filed in your portfolio as `modules/02/lab-report.md`.

## 10. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `'python' is not recognized` | Store alias / PATH | Use `py -3`; or reinstall from python.org with *Add to PATH*; open a **new** terminal |
| `Activate.ps1` blocked by policy | Execution policy | Skip activation — prefix every command with `.venv\Scripts\python` (this course always does) |
| Install takes forever / network errors | Slow index or proxy | Re-run; pip resumes from cache. Corporate proxy → configure pip's proxy setting |
| Tests fail with `ModuleNotFoundError` after install | Wrong interpreter | Compare `sys.executable` between the failing command and §4 |
| `git add` stages `.venv/` | `.gitignore` missing/incorrect | `git reset`, fix `.gitignore`, re-check with `git status --short` |
| Windows reports paths it cannot handle | Very long paths | Enable long paths, or keep the project shallow (`C:\lab02\…`) |

More: [module troubleshooting](troubleshooting.md) ·
[course troubleshooting](../../troubleshooting/index.md).

## 11. Cleanup

```powershell
# 🪟 from the folder that contains lab02-rebuild
Set-Location ..
Remove-Item -Recurse lab02-rebuild
```

```bash
# 🐧 from the parent folder
rm -rf lab02-rebuild
```

✅ Verify the folder is gone. Your original `examples/churn` was never modified —
confirm with `Get-ChildItem examples\churn` / `ls examples/churn`.

## 12. Optional extension tasks

1. **Rebuild from lock only:** delete `.venv`, install with
   `pip install -r requirements.lock`, and confirm the same test results.
2. **Two shells:** repeat steps 3–8 in Git Bash (🐧) and note which commands differ.
3. **Time it:** record how long a cold rebuild takes; this number becomes your
   justification (later) for caching in CI.
4. **`uv` comparison:** if you want a faster tool, redo the environment with
   [`uv`](https://docs.astral.sh/uv/) and compare wall-clock time.

---

**Next:** [independent-challenge.md](independent-challenge.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*