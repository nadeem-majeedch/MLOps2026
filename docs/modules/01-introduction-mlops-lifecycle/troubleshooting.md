# Troubleshooting — Module 01

Problems specific to this module. For Python, Git, containers, or site problems,
use the [course troubleshooting page](../../troubleshooting/index.md).

## First habit

Read the **last line** of any error first — it names the actual problem. Above
it is only the trail. Then state your problem in one sentence: *"When I run X, I
expected Y, but I got Z."* Half of all fixes happen at that sentence.

## 1. Generating the incident data

| Symptom | Likely cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'pandas'` | The `python` you ran is not the one with pandas | `python -c "import pandas; print(pandas.__version__)"` — if that fails, install pandas in *this* interpreter: `python -m pip install pandas` 🪟/🐧 |
| `can't open file 'make_fixture.py'` | Wrong working directory | `Get-Location` 🪟 / `pwd` 🐧 — you must be inside `examples/churn/01-autopsy` |
| On Windows, `python` opens the Microsoft Store | The Store alias intercepts the command | Use `py -3 make_fixture.py`, or install Python from python.org with *Add to PATH* and open a new terminal |
| Output says 0 rows / empty file | Truncated or edited CSV | Re-run `python make_fixture.py`; it overwrites and is deterministic |

## 2. Running the pandas analysis

| Symptom | Likely cause | Fix |
|---|---|---|
| `FileNotFoundError: 'metrics_snapshot.csv'` | Kernel/script running in a different folder | Use full path: `pd.read_csv("01-autopsy/metrics_snapshot.csv")` or start your editor's terminal in the right folder |
| `ParserError` / a column read as text | The CSV was edited or has an extra line | Regenerate the file (§1); never hand-edit generated data |
| `model_version` has only `v2` | Data truncated | Regenerate; you must see both versions, 60 rows total |
| Your numbers differ from the worked example | A different or edited file | Regenerate and re-run — same seed ⇒ same numbers. If they *still* differ, note your pandas version: `python -c "import pandas; print(pandas.__version__)"` |
| `KeyError: 'churn'` (extension task) | Wrong file — that column is in `data/raw/churn.csv`, not the autopsy files | Use the right CSV; the autopsy metrics have `auc`, `missing_rate`, `drift_score` |

## 3. Conceptual blocks (not computer problems)

These are the confusions that stall beginners. If one of these is your problem,
no command will fix it.

| You are stuck because… | Reframe |
|---|---|
| "Everything feels like MLOps" | MLOps is not a tool list — it is the set of practices that keeps the *lifecycle loop* turning. Ask: which stage does this affect? |
| "The metrics look fine, so where is the bug?" | In ML, *aggregate* metrics can look fine while *segments* rot — compare periods (worked example §3) and check data quality, not only AUC |
| "Which stage does this failure belong to?" | Ask: *what artefact would have stopped it here?* A validation gate ⇒ validate stage; a registry entry ⇒ promote stage |
| "Is this a DevOps problem or an ML problem?" | Would a conventional test have caught it? If the failure is *quality over time*, it is an ML problem (monitoring) |
| "I can define the terms but cannot apply them" | Expected at this point — apply them in the lab and challenge, where the mapping table forces a decision |

## 4. If the lab's acceptance criteria feel ambiguous

That is a course bug, not your fault. Report it as a repository issue quoting the
module number and the exact criterion — ambiguity in an acceptance test is the
same defect as ambiguity in a code assertion.

## 5. Still stuck

1. Re-run the last ✅ checkpoint you *actually ran* (not the one you remember).
2. Search the exact error text, not your paraphrase of it.
3. Check [references.md](references.md) for the official documentation of the
   tool involved — official docs resolve most "why does it do that?" questions.
4. Ask for help with: exact command, exact error, your OS and Python version, and
   what you already tried.

---

[← Knowledge check](knowledge-check.md) · [References →](references.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*