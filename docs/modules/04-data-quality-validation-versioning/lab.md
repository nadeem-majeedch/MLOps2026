# Lab 04 — Gate the incoming dataset

## 1. Scenario and business problem

Lahore Retail Co.'s warehouse exports a daily customer extract. Historically it
has been loaded straight into training. This week it arrived three times: one
good file and two broken ones. Nobody noticed for two days, and the model trained
on one of the broken extracts.

**Business problem:** data arrives from outside your control, so it must be
*proven* good before it is used — and the exact bytes a model was trained on must
be recoverable afterwards.

## 2. Skills practised

- Writing schema, completeness, uniqueness, range, domain, and target checks.
- Diagnosing which check should have fired, and reading a failure report.
- Freezing a dataset with a content hash and restoring it byte-for-byte.
- Reading DVC's refusal (and deciding when `--force` is justified).

## 3. Prerequisites

- [concepts.md](concepts.md) read (§1–§5).
- Module 02 lab completed (Git habits); Module 03 lab completed (project layout).
- pandas available; DVC installed: `python -m dvc --version` → prints a version.

## 4. Required tools and estimated time

| Item | Detail |
|---|---|
| Tools | Python 3.10+, pandas, DVC (free, local), PowerShell 🪟 / bash 🐧 |
| Cost | Free, local, **no cloud account** (DVC's local cache only) |
| ⚠️ Resource-heavy | none — DVC cache for a 60 KB file is negligible |
| ⏱️ Estimated time | 120 minutes (70 validation + 50 versioning) |

## 5. Input data and how to obtain it

Generated locally by the shared example (no download, works offline):

```powershell
# 🪟 Windows / PowerShell — from examples/churn
python generate_data.py
```

```bash
python3 generate_data.py
```

Actual output:

```text
rows written: 2000
churn rate:   0.091
  data\raw\churn.csv  (60,755 bytes)
  data\raw\churn_day2.csv  (60,707 bytes)
  data\corrupt\bad_types.csv  (60,931 bytes)
  data\corrupt\duplicates.csv  (63,034 bytes)
  data\corrupt\missing.csv  (60,161 bytes)
```

Five files: three known-bad, two known-good.

## 6. Directory layout

```
examples/churn/
├── generate_data.py       # produces all five files, deterministically
├── src/validate.py        # the seven checks (yours to read and extend)
├── data/
│   ├── raw/               # good extracts
│   └── corrupt/           # the three seeded defects
└── (later) churn.csv.dvc  # the pointer file you create
```

## 7. Setup and execution steps

**Part A — Validation**

**Step 1 — Run the validator on the good file.**

```powershell
python -m src.validate --data data/raw/churn.csv
```

✅ **Checkpoint:** `7/7 checks passed`, exit code `0`
(`echo $LASTEXITCODE` 🪟 / `echo $?` 🐧).

**Step 2 — Run it on all three broken files.** Record the actual summary line
and exit code for each:

```powershell
python -m src.validate --data data/corrupt/missing.csv
python -m src.validate --data data/corrupt/duplicates.csv
python -m src.validate --data data/corrupt/bad_types.csv
```

Expected (verified): `5/7`, `6/7`, `5/7` checks passed, each exit code `1`.
✅ **Checkpoint:** your table lists which check failed for each file.

**Step 3 — Predict before you run.** For each broken file, write down *which
check you expect to fail and why* — then compare with Step 2. Any surprise is a
gap in your mental model of validation (the `bad_types` one is deliberately
surprising: read worked-example §5).

**Step 4 — Add one check of your own.** Write an eighth check that catches
something the current seven would let through — e.g. a row-count expectation
(`rows` between 1,900 and 2,100) or `tenure_months <= 120`. Document what real
failure it would have caught.

```powershell
# 🪟 rerun after your edit — all four files again
python -m src.validate --data data/raw/churn.csv
```

✅ **Checkpoint:** good file still 8/8; broken files still fail.

**Part B — Versioning**

**Step 5 — Initialise DVC.** From `examples/churn/`:

```powershell
python -m dvc init --no-scm
```

> `--no-scm` is only because this folder is not itself a Git repository. Inside a
> real project (Module 02's), you would run `python -m dvc init` and let DVC
> integrate with Git.

✅ **Checkpoint:** `.dvc/` folder exists (`Test-Path .venv`-style check on `.dvc`).

**Step 6 — Freeze the good file.**

```powershell
python -m dvc add data/raw/churn.csv
Get-Content data\raw\churn.csv.dvc
```

Expected content (the hash is deterministic for these bytes):

```text
outs:
- md5: 18df7e78d2f419439cdc4b98a592ab99
  size: 60755
  hash: md5
  path: churn.csv
```

✅ **Checkpoint:** the recorded MD5 equals your file's hash
(`md5sum data/raw/churn.csv` 🐧 or `Get-FileHash -Algorithm MD5` 🪟).

**Step 7 — Confirm a clean state.**

```powershell
python -m dvc status
```

Expected: `Data and pipelines are up to date.`

**Step 8 — Break the data on purpose, then detect it.**

```powershell
Add-Content data\raw\churn.csv "junk,row`n1,2"
python -m dvc status
```

Expected shape:

```text
data\raw\churn.csv.dvc:
	changed outs:
		modified:           data\raw\churn.csv
```

**Step 9 — Restore, and meet the safety check.**

```powershell
python -m dvc checkout            # expect a REFUSAL (see below)
python -m dvc checkout --force    # the explicit consent
```

The refusal (actual output):

```text
ERROR: Can't remove the following unsaved files without confirmation. Use `--force` to force.
C:\...\data\raw\churn.csv
```

✅ **Checkpoint:** after `--force`, your hash is `18df7e78…` again.

**Think:** why does DVC refuse? Because your local edit might be something you
wanted. State in your report the condition under which `--force` is safe (*"the
file is regenerable and the pointer is committed"*).

**Step 10 — Write the dataset card** (5–10 lines): source (synthetic, generated),
licence (CC0), size, schema, target balance (0.091), known limitations (synthetic
distribution, no missing values by construction, only five features).

## 8. Expected outputs and verification

| Step | Expected | Verify |
|---|---|---|
| 1 | `7/7 checks passed`, exit 0 | printed summary + exit code |
| 2 | `5/7`, `6/7`, `5/7`, each exit 1 | your recorded table |
| 4 | Your new check passes good / fails bad | re-run all four files |
| 6 | MD5 `18df7e78…`, size 60755 | pointer file vs. `md5sum` |
| 7 | `up to date` | `dvc status` |
| 8 | `modified: data\raw\churn.csv` | `dvc status` |
| 9 | refusal, then restore; hash matches again | `md5sum` after `--force` |

## 9. Acceptance criteria

- [ ] All four files validated; results recorded with exit codes.
- [ ] Every failing check identified with the *cause*, not just the name.
- [ ] One new check added, justified by a real failure scenario.
- [ ] `.dvc` pointer created and its MD5 verified against the actual file.
- [ ] Detection + refusal + `--force` restore all observed, with `--force`
      safety condition written down.
- [ ] Dataset card completed.
- [ ] Cleanup run (§11) and everything filed as `modules/04/`.

## 10. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `ModuleNotFoundError: dvc` | Not installed in this interpreter | `python -m pip install dvc` (⚠️ a large install) |
| `dvc: command not found` 🐧/🪟 | Console script not on PATH | Use `python -m dvc …` everywhere — this is what the labs do |
| `Can't remove the following unsaved files` | Local file modified without consent | Expected — inspect, then `python -m dvc checkout --force` |
| Hash differs from `18df7e78…` | Different file, edited data, or regenerated with a changed script | Regenerate with `python generate_data.py`; never hand-edit data |
| `dvc init` complains about Git | Running inside a Git-less folder | Use `dvc init --no-scm` (or `git init` first, in your own project) |
| Validator says everything passes on a corrupt file | Your added check is not reached (early `return`) or tests the wrong column | Re-read `run_checks` — the early return skips checks when columns are missing |
| `permission denied` writing `.dvc/` | Read-only or locked folder | Check folder attributes; run from the project root |

More: [troubleshooting.md](troubleshooting.md) ·
[course troubleshooting](../../troubleshooting/index.md).

## 11. Cleanup

```powershell
# 🪟 from examples/churn
Remove-Item -Recurse .dvc, .dvcignore, data\raw\churn.csv.dvc, data\.gitignore -ErrorAction SilentlyContinue
python generate_data.py
```

```bash
# 🐧 from examples/churn
rm -rf .dvc .dvcignore data/raw/churn.csv.dvc data/.gitignore
python3 generate_data.py
```

✅ **Verify:** `python generate_data.py` prints `rows written: 2000`, and
`python -m src.validate --data data/raw/churn.csv` is back to `7/7`.
Your validator edits (Step 4) and dataset card (Step 10) are the parts you keep.

## 12. Optional extension tasks

1. **DVC remote (☁️ optional):** add a local or cloud remote
   (`dvc remote add -d …`) and push/pull — then remove it and prove the local
   cache still works. Never a graded requirement.
2. **pandera port:** rewrite the seven checks with
   [pandera](https://unionai.github.io/pandera/) types and compare lines of code.
3. **Day 2:** validate `churn_day2.csv` and diff it against day 1 — which
   columns changed, and does any change cross a threshold?
4. **CI preview:** write the one-line command that a CI job would run to gate a
   pull request (you will wire it in Module 12).

---

**Next:** [independent-challenge.md](independent-challenge.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*