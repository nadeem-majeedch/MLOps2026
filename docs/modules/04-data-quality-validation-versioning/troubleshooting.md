# Troubleshooting — Module 04

Validation and DVC problems specific to this module. General Python/Git issues:
[course troubleshooting](../../troubleshooting/index.md),
[Module 02](../02-python-git-cli-environments/troubleshooting.md).

## 1. Validation results you did not expect

| Symptom | Likely cause | Fix |
|---|---|---|
| Corrupt file reports `7/7 checks passed` | You ran it on the wrong path, or the file was regenerated (it is clean again) | Check the exact path passed to `--data`; `python generate_data.py` restores the seeded defects |
| `column_types` passes on damaged data | pandas *infers* dtypes — numeric text parses as numbers, `n/a` becomes `NaN` | Expected (worked-example §5): test meaning via completeness/ranges, or read with explicit `dtype=` |
| `required_columns` FAIL then nothing else reported | The validator stops deliberately when columns are missing | Correct behaviour: downstream checks would be guesswork. Read `run_checks`' early return |
| `FileNotFoundError` | Wrong working directory | `Get-Location` / `pwd` must be `examples/churn`; then use `data/…` relative paths |
| Your new check never fires | It sits after the early `return`, or tests a column that does not exist | Put general checks after the column guard; print the value you are testing while debugging |
| Exit code always 0 | You are running the module without letting `sys.exit` propagate, or wrapped it in a try/except | Run `python -m src.validate --data …` directly, then `echo $LASTEXITCODE` |

## 2. DVC

| Symptom | Likely cause | Fix |
|---|---|---|
| `dvc: command not found` | Console script not on PATH | Use `python -m dvc …` — the course's standard form |
| `ModuleNotFoundError: No module named 'dvc'` | Not installed in the running interpreter | `python -m pip install dvc` (⚠️ large download), or fix the interpreter per Module 02 |
| `ERROR: Can't remove the following unsaved files without confirmation` | Working file modified since `dvc add` | Inspect the change; if disposable → `python -m dvc checkout --force`. **Never** `--force` when the local file might hold unrecorded work |
| `dvc status` reports changes after regenerating data | Regeneration is a change — that is the point | If the new data should be the version: `dvc add` again; if not: `dvc checkout --force` |
| `failed to lock ... .dvc/...` | Two DVC processes at once, or a crashed previous run | Delete the stale `.dvc/tmp/lock` file only if you are sure nothing else is running |
| `dvc init` says it needs Git | Folder is not a repository | Use `dvc init --no-scm`, or `git init` first in your own project (Module 02) |
| Hash mismatch after a "no-op" edit | Line endings or BOM changed the bytes | Do not hand-edit versioned data; regenerate or restore instead |

## 3. Conceptual blocks

| You are stuck because… | Reframe |
|---|---|
| "Which checks should I write?" | Start from what would cost you money or credibility if wrong — then encode each as a check with a count and a threshold |
| "Is this data drift or a bad file?" | One file malformed ⇒ validation (this module). Systematic shift over many days ⇒ drift (Module 14) |
| "Why version data if it is generated?" | Provenance: you must still prove *which* generator output an experiment used. Regeneration with a changed script is a new version |
| "Is a contract worth writing if I am alone?" | The contract is you-tomorrow. It also becomes the CI gate in Module 12 |
| "Do I need a DVC remote?" | Not for this course. Local cache + pointer files cover every graded requirement |

## 4. If the lab's expected outputs do not match

1. Regenerate the data first (`python generate_data.py`) — the fixtures are
   deterministic; MD5 `18df7e78…` is the known-good fingerprint.
2. Check your pandas version and note it in your report
   (`python -c "import pandas; print(pandas.__version__)"`).
3. If outputs still differ, that is a course bug — report it with the module
   number, the command, and your actual output.

---

[← Knowledge check](knowledge-check.md) · [References →](references.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*