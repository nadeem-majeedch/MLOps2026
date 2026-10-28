# Lab 03 — Rescue the spaghetti notebook

## 1. Scenario and business problem

A colleague left the team. Their last contribution is `legacy/analysis.ipynb`,
which "produces 0.886 accuracy — just run it". Management wants that analysis
turned into something the team can maintain: a project the next person can run,
read, and change without archaeology.

**Business problem:** the analysis exists, but the *capability* does not — the
number cannot be reproduced on demand, and nothing about it can be safely
changed.

## 2. Skills practised

- Extracting logic from notebook cells into importable functions.
- Moving hard-coded values into configuration **without changing results**.
- Establishing a single entry point and documenting it.
- Verifying a refactor by reproducing an exact number.

## 3. Prerequisites

- [concepts.md](concepts.md) read (§1–§5).
- Module 02 lab completed (environment + Git habits).
- Python with pandas/scikit-learn (Module 02 environment).

## 4. Required tools and estimated time

| Item | Detail |
|---|---|
| Tools | Python 3.10+, pandas, scikit-learn, PyYAML, an editor, Git |
| Cost | Free, local, no accounts |
| ⚠️ Resource-heavy | none (runs in seconds) |
| ⏱️ Estimated time | 100 minutes |

## 5. Input data and how to obtain it

The notebook reads `data/raw/churn.csv`, which is **generated**, not downloaded:

```powershell
# 🪟 Windows / PowerShell — from examples/churn
python generate_data.py
```

```bash
# 🐧 Linux / macOS
python3 generate_data.py
```

Expected (actual output):

```text
rows written: 2000
churn rate:   0.091
```

Then run the notebook to capture the number you must reproduce:

```powershell
# 🪟 run all cells of legacy/analysis.ipynb (in VS Code/Jupyter, or)
python -c "import json,sys; nb=json.load(open('legacy/analysis.ipynb')); \
[exec(compile(''.join(c['source']),'nb','exec'), {}) for c in nb['cells'] if c['cell_type']=='code']"
```

✅ **Checkpoint:** you see `accuracy 0.886`. Write it down — it is your target.

## 6. Directory layout (start and finish)

```
03-your-refactor/              # you create this as a copy or fresh folder
├── legacy/analysis.ipynb      # input: messy, but working
├── config.yaml                # YOU create: the notebook's numbers
├── pipeline.py                # YOU create: the logic, as functions
├── run.py                     # YOU create: the entry point
├── README.md                  # YOU create: the contract
└── data/raw/churn.csv         # generated (not committed)
```

## 7. Setup and execution steps

**Step 1 — Copy the starting material.**

```powershell
# 🪟 from the repository root
Copy-Item -Recurse examples\churn\legacy .\03-your-refactor\legacy
New-Item -ItemType Directory 03-your-refactor | Out-Null
Copy-Item examples\churn\generate_data.py, examples\churn\config.yaml 03-your-refactor\
Copy-Item -Recurse examples\churn\data 03-your-refactor\data
```

(Or create the folder by hand and copy just the notebook — the data copy is only
to avoid regenerating it twice.)

**Step 2 — Inventory the notebook.** List every cell and tag each line:
*logic*, *configuration*, *output*, or *redundant*.
✅ **Checkpoint:** your list names ≥1 item in each of the four categories.

**Step 3 — Extract configuration first.** Create `config.yaml` containing the
notebook's values with their names:

```yaml
seed: 7
test_size: 0.25
n_estimators: 500
features: [tenure_months, monthly_charges, support_tickets, contract_num]
```

**Step 4 — Extract functions.** One function per job: `load_data`, `add_features`,
`split`, `fit_and_score`, `churn_rate`. Rules: no printing inside functions, no
file writes inside functions, no reading globals.

**Step 5 — Write the entry point** `run.py`: load config → load data → transform
→ split → evaluate → print. This is the only file a stranger runs.

**Step 6 — Run and compare.**

```powershell
python run.py
```

Expected (this is the reference implementation's actual output; yours prints the
same key values):

```text
rows:            2000
churn rate:      0.091
contract counts:
contract_type
monthly     982
one_year    596
two_year    422
test size:       0.25 (seed 7)
accuracy:        0.8860
```

✅ **Checkpoint:** `accuracy 0.8860` matches your Step 2 number. If it does not,
you changed behaviour — see §10 (the usual culprits: split ratio, seed, feature
list, or dropping rows differently).

**Step 7 — Run it twice.** Both runs must print the same accuracy. If they
differ, some randomness is not seeded.

**Step 8 — Write `README.md`** answering the four contract questions (concepts §5):
what it does / what is needed / how to run it / what output to expect.

**Step 9 — Commit your work** (Module 02 habits): `git status` first, add the
files you intend, commit with a reason.

**Step 10 — Design note.** One page: for each structural decision, the cost of
*not* doing it. Example: *"Externalised configuration — otherwise every
experiment requires editing code, and we cannot tell which values produced a
result (see Module 06)."*

## 8. Expected outputs and verification

| Step | Expected | Verify |
|---|---|---|
| 2 | ≥1 item per category | Your inventory table |
| 6 | `accuracy 0.8860`, `churn rate 0.091`, counts `982/596/422` | Printed output compared with the notebook's |
| 7 | Two identical runs | Side-by-side output |
| 8 | A stranger can run it from README alone | Have someone (or your future self) do it without asking |
| 10 | ≥3 decisions with costs, not preferences | Count them |

A reference implementation exists at `examples/churn/03-refactor/` — **attempt
the restructure first**, then compare approaches if you are stuck.

## 9. Acceptance criteria

- [ ] `python run.py` reproduces `accuracy 0.8860` from a clean folder.
- [ ] No magic numbers remain in code — every value comes from `config.yaml`.
- [ ] `pipeline.py` can be imported without side effects (no files written, no
      model trained on import).
- [ ] README answers all four contract questions.
- [ ] Two consecutive runs produce identical output.
- [ ] Design note filed with ≥3 cost-based justifications.
- [ ] Everything above in your portfolio as `modules/03/`.

## 10. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `accuracy` differs from 0.8860 | Split ratio, seed, feature list, or row-dropping changed | Diff your `config.yaml` against §7 step 3; check `dropna` placement |
| `FileNotFoundError: data/raw/churn.csv` | Wrong working directory, or data not generated | `Get-Location` / `pwd`; run `python generate_data.py` |
| `ModuleNotFoundError: yaml` | Dependency missing from your environment | `.venv\Scripts\python -m pip install PyYAML` 🪟 / `.venv/bin/python …` 🐧 |
| Import errors when running `run.py` | `pipeline.py` not next to `run.py`, or module name clash | Check folder layout; `sys.path` insertion is shown in the reference `run.py` |
| Notebook outputs differ from the lab | Notebook ran out of order | Kernel → Restart & Run All before trusting a number |
| `model.pkl` appears in the folder | You ran the legacy save cell | Delete it; the refactor must not write files during a run |

More: [troubleshooting.md](troubleshooting.md) ·
[course troubleshooting](../../troubleshooting/index.md).

## 11. Cleanup

```powershell
# 🪟 from the parent of your folder
Remove-Item -Recurse 03-your-refactor
```

```bash
# 🐧
rm -rf 03-your-refactor
```

✅ Verify it is gone. The shared example (`examples/churn`) was not modified —
confirm with `git status` (or `Get-ChildItem examples\churn`).

## 12. Optional extension tasks

1. **Add a test:** write a one-line pytest test asserting the churn rate is 0.091 —
   a preview of Module 07.
2. **Parameterise:** add `--seed` to `run.py` and show two runs that differ.
3. **Notebook hygiene:** pair the legacy notebook with `jupytext` so it diffs
   cleanly, or strip outputs with `nbstripout` and commit.
4. **Layout comparison:** put your structure side by side with
   cookiecutter-data-science and write three sentences on which trade-offs you
   prefer and why.

---

**Next:** [independent-challenge.md](independent-challenge.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*