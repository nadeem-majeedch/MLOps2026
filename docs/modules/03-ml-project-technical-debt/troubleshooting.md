# Troubleshooting — Module 03

Module-specific problems here; environment/Git problems in
[course troubleshooting](../../troubleshooting/index.md) or
[Module 02's page](../02-python-git-cli-environments/troubleshooting.md).

## 1. Running the notebook

| Symptom | Likely cause | Fix |
|---|---|---|
| `.ipynb` opens as JSON text | No notebook renderer | Install the Jupyter extension in VS Code, or `jupyter notebook` if you have Jupyter installed |
| Cells fail when run individually | Hidden state — cells depend on earlier runs | Kernel → *Restart & Run All*; treat any failure as a defect to fix in the refactor |
| Numbers differ from the lab | Stale state or different data | Restart kernel, run all; regenerate data with `python generate_data.py` |
| `model.pkl` appears afterwards | The notebook's save cell ran | Delete it — 13 MB of generated weight has no place in a repo |

## 2. Running the refactor

| Symptom | Likely cause | Fix |
|---|---|---|
| `accuracy` is not `0.8860` | Behaviour changed during refactor | Compare in this order: `config.yaml` values (seed 7, split 0.25, 500 trees) → feature list → `dropna` placement → split function |
| `ModuleNotFoundError: yaml` | PyYAML missing in the running interpreter | `.venv\Scripts\python -m pip install PyYAML` 🪟 / equivalent 🐧 — always prefix the `.venv` interpreter |
| `FileNotFoundError: data/raw/churn.csv` | Wrong working directory | `Get-Location` / `pwd` must be the project folder; regenerate data if absent |
| `ImportError: cannot import name 'pipeline'` | `pipeline.py` not beside `run.py`, or a same-named module earlier on the path | Check folder layout; rename if a stdlib/package name collides |
| Two runs give different accuracies | Some randomness not seeded | Search for `random`/`shuffle` without `random_state`; seed it via config |
| Tests (extension) collect nothing | Running from the wrong folder | Run from the folder containing `pyproject.toml` |

## 3. Structural confusion (design, not code)

| You are stuck because… | Reframe |
|---|---|
| "Which functions should I extract?" | Extract what is written twice, or what you would want to test in isolation |
| "Is this config or code?" | If editing it could silently invalidate past experiments, it is **code**; if it is a value you would sweep in an experiment, it is **config** |
| "How much structure is too much?" | Enough that a stranger can run it from the README — structure past that is optional and can wait for real need (Rule: do not build Module 08's machinery in Module 03) |
| "Should I delete the old notebook?" | Not yet: it is your evidence that the numbers match. Archive it, exclude it from imports, note it in the README |
| "My code has no debt, surely" | Grep for literals and paths (challenge §If you get stuck). Debt hides in strings |

## 4. If an acceptance criterion is ambiguous

That is a course defect, not your failure — report it as an issue quoting the
module and the exact wording. Ambiguous acceptance criteria are the same defect
as an ambiguous assertion in a test.

---

[← Knowledge check](knowledge-check.md) · [References →](references.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*