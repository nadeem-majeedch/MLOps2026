# Worked example — the same analysis, twice

Both runs below were executed on the reference machine in `examples/churn/`. The
point of this example is the **last line of each block**: two very different
artefacts, one identical number.

---

## 1. The legacy notebook (before)

Open `legacy/analysis.ipynb` and run its cells. Actual output of the code cells:

```text
(2000, 6)
  customer_id  tenure_months  ...  support_tickets churn
0     C100000             13  ...                1     0
...

churn rate 0.091
overall churn rate is 0.091
contract_type
monthly     982
one_year    596
two_year    422
Name: count, dtype: int64
accuracy 0.886
saved model.pkl
```

**Four defects you should be able to name now** (concepts §3):

| In the notebook | Defect type |
|---|---|
| `churn rate` and `overall churn rate is` — the same calculation, written twice | Single-source-of-truth violation (one of them will rot) |
| `test_size=0.25`, `random_state=7`, `n_estimators=500` buried in cells | Configuration debt — no reason recorded for any of them |
| Cells depend on `df` and `contract_map` existing from earlier cells | Hidden state — rerun out of order and results change |
| `pickle.dump(model, open('model.pkl','wb'))` writes into whatever folder you ran from | Side effect with an undeclared location; a 13 MB file nobody can attribute |

Also notice: the notebook's seed (7) and split (0.25) differ from the course's
`config.yaml` (seed 42, split 0.20). Neither is "wrong" — but **nobody chose**,
and that is the debt.

## 2. The refactored project (after)

```
03-refactor/
├── config.yaml     # seed 7, test_size 0.25, n_estimators 500 — the notebook's values
├── pipeline.py     # five small functions, no side effects on import
└── run.py          # the single entry point
```

Actual code shape (abbreviated — read the files for the full version):

```python
# pipeline.py — each function does one thing and returns it
def load_data(csv_path): ...
def add_features(df): ...
def split(frame, config): ...          # seed and split come from config
def fit_and_score(x_train, ...): ...
def churn_rate(df, target): float: ... # defined once, used everywhere

# run.py — the entry point a stranger can run
frame = add_features(load_data(DATA))
print(f"churn rate: {churn_rate(frame, 'target'):.3f}")
```

Run it:

```powershell
# 🪟 Windows / PowerShell — from examples/churn/03-refactor
python run.py
```

Actual output:

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

✅ **Checkpoint:** `churn rate 0.091`, counts `982 / 596 / 422`,
`accuracy 0.8860` — **identical to the notebook**. The refactor changed
*structure*, not *results*. That is the acceptance test for any refactor: if
numbers move, you changed behaviour and must say so deliberately.

## 3. What changed, and which debt it repaid

| Change | Debt repaid |
|---|---|
| Numbers moved to `config.yaml`, with their original values | Configuration debt — now the values can be argued with |
| Calculations live in named functions | Hidden state and duplication — importable, testable, reusable |
| One entry point (`run.py`) | Pipeline sprawl — no guessing which cell is "the job" |
| `DATA` path computed, not pasted | Data-dependency debt — one place to fix when the path moves |
| `src`/`legacy` separation | Entanglement — the old notebook can be deleted later without touching live code |
| No file written during a run | Undeclared side effect removed — artefacts will be explicit from Module 05 |

## 4. Reproducibility you can demonstrate

```powershell
# 🪟 run it twice and compare
python run.py
python run.py
```

Both runs print `accuracy: 0.8860`. The randomness is fixed by
`random_state` in `config.yaml`, so the number is a *property of the project*, not
of the session. Module 05 strengthens this to a file-hash comparison.

## 5. Why `legacy/` stays

Deleting the notebook would be tidier — and would destroy the evidence of how
the numbers were first produced. Keep it, keep it out of the import path, and
say in the README that `run.py` supersedes it. When a project reaches production
(M09), that provenance question ("where did this number come from?") becomes a
registry entry.

---

**Next:** [lab.md](lab.md) — do the restructure yourself, and grade it against acceptance criteria.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*