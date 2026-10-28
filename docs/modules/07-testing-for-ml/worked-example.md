# Worked example — the suite, its coverage, and a real failure

All output below is **actual** (pytest 9.1.1, pytest-cov, `examples/churn/`).

---

## 1. Inventory: what the suite already contains

```
tests/
├── conftest.py         # fixtures: config, data_path (auto-generates data), data
├── test_features.py    # 5 unit tests
├── test_data.py        # 7 data tests
├── test_model.py       # 5 model tests (incl. the performance floor)
└── test_pipeline.py    # 2 integration tests
```

**19 tests, five layers, one dataset.** Note what is *not* here: no network, no
GPU, no cloud — and nothing that needs more than a few seconds.

## 2. Run it

```powershell
# 🪟 Windows / PowerShell — from examples/churn
python -m pytest
```

Actual output:

```text
...................                                                      [100%]
19 passed in 3.91s
```

Exit code: **0**. (`python -m pytest` rather than bare `pytest` guarantees the
same interpreter as your environment — Module 02's lesson, applied.)

## 3. Run it with coverage

```powershell
python -m pytest --cov=src --cov-report=term-missing
```

Actual output:

```text
...................                                                      [100%]
=============================== tests coverage ================================
_______________ coverage: platform win32, python 3.14.7-final-0 _______________

Name              Stmts   Miss  Cover   Missing
-----------------------------------------------
src\__init__.py       0      0   100%
src\features.py      25      0   100%   (no misses)
src\train.py         43     11    74%   46-54, 100-107, 111
src\validate.py      45     14    69%   42, 84-97, 101
-----------------------------------------------
TOTAL               113     25    78%
19 passed in 3.91s
```

**How to read it (concepts §5):** the missing lines are the gradient-boosting
branch, the CLI argument parser, and the validator's report printer — all
deliberate or cosmetic. The number 78% is a *map*, not a grade.

## 4. Watch a gate fail — on purpose

A test you have never seen fail is a test you cannot trust. Here is a real
failure captured by raising the performance floor beyond what this model can
reach:

```text
>       assert m["roc_auc"] >= 0.99, f"roc_auc {m['roc_auc']} is below the floor 0.99"

E       AssertionError: roc_auc 0.7163 is below the floor 0.99
E       assert 0.7163 >= 0.99

tests\test_demo_fail.py:10: AssertionError
=========================== short test summary info ===========================
FAILED tests/test_demo_fail.py::test_floor_that_is_unreachable - AssertionErr...
1 failed in 2.93s
```

Exit code: **1**.

Three things to notice:

1. **The message carries the numbers.** `0.7163 is below 0.99` — you know the
   measured value, the threshold, and the file, without re-running anything.
   This is what our earlier error-message discussion was for.
2. **The failure is fast** (2.93 s): the gate costs nothing to run on every change.
3. **The suite returns exit 1**, which is exactly what CI (Module 12) needs to
   block a merge. Nothing else in the pipeline has to "know" anything.

*(The demo file was temporary and has been removed — but the practice it shows
is required in the lab.)*

## 5. What each layer in this suite actually asserts

| Test (representative) | Layer | The property it guards |
|---|---|---|
| `test_split_xy_returns_only_configured_features` | unit | The feature set is exactly what config declares — no silent extras |
| `test_split_is_deterministic` | unit | The same seed gives the same split (foundation of reproducibility) |
| `test_preprocessor_handles_unknown_categories` | unit | A never-seen category does not crash serving |
| `test_no_nulls_in_required_columns` | data | Module 04's contract, enforced as a test |
| `test_validator_catches_the_seeded_defect` | data | **The validator itself is tested** — it must reject a known-bad file |
| `test_roc_auc_above_performance_floor` | model / gate | Quality does not drop below the committed floor |
| `test_batching_does_not_change_predictions` | model (invariance) | Serving one row or many gives identical answers |
| `test_same_seed_gives_same_metrics` | regression | Determinism claim, re-checked every run |
| `test_end_to_end_train_then_serve` | integration | CSV → model → predictions works as one path |
| `test_validation_blocks_bad_data` | integration | Bad input cannot produce a model |

Note the meta-test: **`test_validator_catches_the_seeded_defect`** proves the
check can fail. Your lab must include at least one such test for every gate you
build — a gate that has never rejected anything is untested.

## 6. The pattern you will reuse

```python
def test_roc_auc_above_performance_floor(config, data_path, tmp_path):
    cfg = _config_in(tmp_path, config)          # isolated outputs
    metrics, _ = train(str(cfg), str(data_path))
    assert metrics["roc_auc"] >= ROC_AUC_FLOOR, (
        f"roc_auc {metrics['roc_auc']} is below the floor {ROC_AUC_FLOOR}"
    )
```

Four habits in nine lines: **threshold with its reasoning declared**, **inputs
from a fixture**, **outputs in `tmp_path` (no cross-test state)**, and an
**assertion message containing the evidence**.

---

**Next:** [lab.md](lab.md) — extend this suite, seed three bugs, and prove each one is caught.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*