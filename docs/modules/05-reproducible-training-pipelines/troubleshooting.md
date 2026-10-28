# Troubleshooting — Module 05

Training and reproducibility problems. Environment/Git issues:
[course troubleshooting](../../troubleshooting/index.md),
[Module 02](../02-python-git-cli-environments/troubleshooting.md).

## 1. "It is not reproducible" — a decision tree

| Observation | Most likely cause | Check |
|---|---|---|
| Metrics differ a lot run to run | An unseeded split or model | grep for `train_test_split`/model constructors without `random_state` |
| Metrics identical, hash differs | A hidden stochastic step, unordered iteration, or parallelism | Seed every stochastic call; `sorted()` before order-dependent work; fix thread counts |
| Everything differs between machines | Different dependency versions | Compare `pip freeze` output (Module 02) |
| Results changed after regenerating data | Input bytes changed (script edited, seed changed) | Compare data MD5 against your recorded `18df7e78…` |
| Metrics identical on one machine, different on another | BLAS/platform floating-point differences | Claim reproducibility *within* a pinned environment; compare metrics with tolerance |

**Never "fix" a mismatch by loosening the claim.** Find the source; the exercise
exists precisely so you can.

## 2. Training errors

| Symptom | Likely cause | Fix |
|---|---|---|
| `ModuleNotFoundError: yaml` / `sklearn` | Wrong interpreter | `.venv\Scripts\python -m pip install …` 🪟 (Module 02's rule) |
| `FileNotFoundError: data/raw/churn.csv` | Wrong working directory | `Get-Location`/`pwd`, then regenerate data if missing |
| `KeyError: 'model'` / `'features'` | YAML structure broken by editing | `python -c "import yaml,pprint; pprint.pprint(yaml.safe_load(open('config.yaml')))"` to see what Python reads |
| `ValueError: y contains 1 class` | Data filtered to a single target value | Validate first (`7/7` gate); check filters and column names |
| `ConvergenceWarning` | Iteration limit reached for the estimator | Note it in your report; raise `max_iter` in config if it persists — do not ignore silently |
| `Permission denied` writing `artifacts/` | Read-only folder or locked file | Check attributes; delete the folder and rerun |
| Metrics JSON missing | Training failed after fitting, or config paths wrong | Check `output:` block in `config.yaml`; run with the same config you think you are using |

## 3. Config mistakes

| Symptom | Likely cause | Fix |
|---|---|---|
| Change had no effect | You edited a different copy, or the flag is unused by code | Confirm with `python -c "import yaml; print(yaml.safe_load(open('config.yaml'))['your_key'])"`; grep the code for that key |
| `--config` ignored | Default path used instead | Pass `--config <file>` explicitly; check the printed `seed` in the output matches your file |
| YAML parses but values are strings | Quoted numbers or tab indentation | Use spaces; unquoted numbers; validate with the print command above |
| Copy-pasted config drifts from the original | Two files, one truth | Keep experiments as *diffs* of a single config; name copies clearly and delete after |

## 4. Metric confusion

| You see… | It means… | Do not… |
|---|---|---|
| accuracy equal to the majority rate | The model found no positives at that threshold | Report it as performance |
| f1 = 0.0 with decent AUC | Threshold 0.5 too high for a rare event | Conclude the model is broken — choose and record a threshold |
| AUC jumping ±0.03 between seeds | Sampling noise on a small test set | Declare a winner from one run (Module 06 exists for this) |
| Huge AUC (0.99+) | Possibly leakage | Check for target-derived features before celebrating |

## 5. Concept blocks

| Stuck because… | Reframe |
|---|---|
| "Which values go in config?" | Would you sweep it in an experiment? → config. Would editing it change what past runs *mean*? → code |
| "Is a hash mismatch a bug?" | It is a *finding*: something invisible changed. Hunt it; do not mask it |
| "Why is my baseline 'just' logistic?" | The baseline's job is to be fast, simple, and hard to beat — fancy baselines hide real regressions |
| "Should I save the model or the pipeline?" | Always the pipeline: serving must not re-implement your preprocessing |

## 6. If the lab's expected numbers do not match

1. Confirm data hash `18df7e78…` and validation `7/7`.
2. Record your versions: `python -c "import pandas, sklearn; print(pandas.__version__, sklearn.__version__)"`.
3. If numbers still differ with identical inputs and versions, that is a course
   bug — report it with command, output, and versions.

---

[← Knowledge check](knowledge-check.md) · [References →](references.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*