# Worked example — the workflow, parsed and executed

**What was verified where.** The authoring environment has no GitHub runner,
so `actions/checkout` etc. did not execute there. What **was** executed: the
YAML parsed and structurally asserted, and **every `run:` command in the
workflow executed locally** with real output shown below. Nothing is invented;
the GitHub-hosted portion is marked accordingly.

---

## 1. ✅ The workflow parses, with asserted structure

```powershell
python -c "import yaml; ..."
```

```text
name: ci
on: {'push': {'branches': ['main']}, 'pull_request': {'branches': ['main']}}
permissions: {'contents': 'read'}
jobs: ['lint', 'test', 'ml-validate']
  lint: 4 steps -> ['actions/checkout@v4', 'actions/setup-python@v5',
                    'Install lint tooling', 'Ruff check']
  test: 6 steps -> [..., 'Install dependencies', 'Generate the synthetic dataset (deterministic)',
                    'Run the test suite', 'Upload coverage report']
  ml-validate: 6 steps -> [..., 'Train once (cheap, CPU-only, ~1 s)',
                    'Validate data contract and quality floor']
STRUCTURE OK
```

The assertions checked: exactly three jobs, `permissions == {contents: read}`,
and the expected step names in order — i.e. the structure concepts §2 teaches
is machine-verified, not eyeballed.

## 2. ✅ Job `lint` — the same two commands CI runs

```powershell
ruff check .
```

```text
All checks passed!
```

*(Worth knowing: this first failed with four genuine findings — an unused
`numpy` import in the legacy notebook, an unused `Pipeline` import in
`src/features.py`, an unused `load_config` import in a test, and a stray `f`
prefix. They were fixed, not suppressed — CI had already done its job.)*

## 3. ✅ Job `test` — generate, then test with coverage

```powershell
python generate_data.py      # "rows written: 2000"
python -m pytest --cov=src --cov-report=term-missing
```

```text
-----------------------------------------------
src\__init__.py       0      0   100%
src\features.py      24      0   100%
src\train.py         43     11    74%   46-54, 100-107, 111
src\validate.py      45     14    69%   42, 84-97, 101
-----------------------------------------------
TOTAL               112     25    78%
34 passed, 1 warning in 5.77s
```

(The `upload-artifact` step is GitHub-only: on a runner it ships `.coverage`
to the run page. Locally the terminal report plays that role.)

## 4. ✅ Job `ml-validate` — passing case

```powershell
python ml_check.py
```

```text
data contract: 7/7 checks passed
quality floor: roc_auc 0.7163 >= 0.7 ? yes

ML VALIDATION PASSED
exit=0
```

## 5. ✅ Job `ml-validate` — the blocking case (this is the point)

With `data/corrupt/missing.csv` swapped in for the training extract:

```text
data contract: 5/7 checks passed
quality floor: roc_auc 0.7163 >= 0.7 ? yes

ML VALIDATION FAILED
  - data check failed: no_missing_values
  - data check failed: value_ranges
exit=1
```

Restored, it printed `ML VALIDATION PASSED` again. **Exit 1 is the entire
mechanism**: a merge-targeting job with a non-zero exit blocks the PR — the
model/data layer now has the same veto as a failing unit test (LO 12.2).

Note what *didn't* happen: no retraining, no long run — validation stayed
fast and deterministic (concepts §3).

## 6. 🧪 On GitHub (when you run it there)

With this file pushed to a repository, the GitHub-hosted steps are the
platform's: `checkout` fetches the commit, `setup-python` provisions 3.14 with
a pip cache keyed on `requirements-docker.txt`, then the **exact same `run:`
commands from §2–§5 execute on an Ubuntu VM**. Acceptance signals to look
for: three green checks on the commit; on a deliberate failure, the red job
names the layer; the coverage artifact downloadable from the run page.

If you have no account, the local transcript above *is* the verification —
every command the workflow runs was run, and its exit codes captured. The
platform adds scheduling and UI, not new logic (concepts §7).

---

**Next:** [lab.md](lab.md) — cause a red run yourself, then fix it.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*