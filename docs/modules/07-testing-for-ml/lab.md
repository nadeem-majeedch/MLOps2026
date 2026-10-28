# Lab 07 — Build the safety net

## 1. Scenario and business problem

Your team's pipeline works — on your machine, today. Management wants it merged
so others can use it, and asks the only question that matters: *"what stops
someone breaking it next month?"*

**Business problem:** without automated tests, every ML change is a gamble paid
for in production. With them, the gamble moves to the pull request, where it is
cheap (Module 12 makes it involuntary).

## 2. Skills practising

- Writing tests in all five layers with meaningful assertions.
- Making a test *prove it can fail* (the meta-test for every gate).
- Reading coverage as a map of untested code.
- Diagnosing a failing performance gate: broken code or moved world?

## 3. Prerequisites

- [concepts.md](concepts.md) read (§1–§5).
- Modules 05–06 completed (pipeline + tracking).
- `pytest` and `pytest-cov` installed (`python -m pytest --version`).

## 4. Required tools and estimated time

| Item | Detail |
|---|---|
| Tools | Python, pytest, pytest-cov, your Module 05 pipeline |
| Cost | Free, local, no accounts |
| ⚠️ Resource-heavy | none — target suite runtime under 30 s |
| ⏱️ Estimated time | 120 minutes |

## 5. Input data and how to obtain it

```powershell
# 🪟 Windows / PowerShell — from examples/churn
python generate_data.py
python -m src.validate --data data/raw/churn.csv      # ✅ 7/7
python -m pytest                                      # ✅ 19 passed
```

(The suite's `conftest.py` regenerates data automatically on a fresh checkout —
verify that claim by deleting `data/` and re-running once.)

## 6. Directory layout

```
examples/churn/
├── tests/
│   ├── conftest.py        # shared fixtures (config, data_path, data)
│   ├── test_features.py   # unit
│   ├── test_data.py       # data
│   ├── test_model.py      # model + performance floor
│   └── test_pipeline.py   # integration
├── src/                   # the code under test
└── pyproject.toml         # pytest config lives here ([tool.pytest.ini_options])
```

## 7. Setup and execution steps

**Step 1 — Read the suite.** Open each test file and label every test with its
layer. Note the assertion messages.
✅ **Checkpoint:** you can say which layer each of the 19 tests belongs to.

**Step 2 — Extend it to your target.** Add tests until you have, at minimum:

| Layer | Minimum in your suite | Source of ideas |
|---|---|---|
| Unit | 6 | config loading, feature construction, split behaviour |
| Data | 6 | schema, nulls, uniqueness, ranges, domain, target balance |
| Model | 3 | performance floor, probability bounds, batching invariance |
| Integration | 2 | end-to-end train → serve; validation blocks bad data |
| Regression | 1 | determinism (same seed ⇒ same metrics) |

```powershell
python -m pytest -q
```

✅ **Checkpoint:** all green, exit code 0.

**Step 3 — Seed three bugs, catch three tests.** Introduce these one at a time
(revert immediately after each):

| # | Seed the bug by… | Expect the failure in |
|---|---|---|
| 1 | Changing `churn` to `1 - churn` inside the loader | model/data tests (floor or balance) |
| 2 | Removing `random_state` from the split | determinism regression test |
| 3 | Dropping `contract_type` from the feature list | unit test asserting configured columns |

For each: record the **exact failing test name** and the last line of its output.

✅ **Checkpoint:** a bug-catch matrix with three rows (bug → test → evidence).

**Step 4 — Document one real failure (the performance gate).** Raise your floor
above what the model reaches (temporarily set it to 0.99), run, capture the
output, restore the floor.

Expected shape (actual from the course's run):

```text
E       AssertionError: roc_auc 0.7163 is below the floor 0.99
1 failed in 2.93s
```

✅ **Checkpoint:** exit code 1 recorded, original floor restored, suite green again.

**Step 5 — Coverage, then judgement.**

```powershell
python -m pytest --cov=src --cov-report=term-missing
```

For each uncovered block, write one line: *test it* (and which layer) or *why
not* (e.g. "CLI argument parser — exercised manually"). The course's own gaps are
a useful comparison: `train.py` 74%, `validate.py` 69%, total 78%.

**Step 6 — Timing.** Record the suite's runtime. If it exceeds ~30 s, look for
repeated data loads (fixtute scope) or network access before adding hardware.

**Step 7 — Write the suite README section**: what the suite guards, how to run
it, how long it takes, and which tests are slowest.

## 8. Expected outputs and verification

| Step | Expected | Verify |
|---|---|---|
| Baseline | `19 passed` (~4 s), exit 0 | pytest summary |
| 2 | Your extended suite green | pytest summary with your counts |
| 3 | Each seeded bug fails a *named* test | failure output captured per bug |
| 4 | `1 failed` with the numbers in the message, exit 1 | captured output |
| 5 | Coverage table + a written decision per gap | your annotated report |
| 6 | Runtime recorded | pytest's own timing |

## 9. Acceptance criteria

- [ ] ≥6 unit, ≥6 data, ≥3 model, ≥2 integration, ≥1 regression test — all green.
- [ ] Bug-catch matrix: three seeded defects, each caught by a **named** test,
      with the failing output attached.
- [ ] One documented failing run of the performance gate (floor 0.99), including
      the exact message and exit code.
- [ ] Coverage report included **with a written judgement** for each uncovered
      block (test it / why not).
- [ ] Suite runtime recorded and under 30 seconds.
- [ ] At least one meta-test: a check proving your validator rejects known-bad data.
- [ ] Everything filed as `modules/07/`.

## 10. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `pytest: command not found` | Console script not on PATH | `python -m pytest` — always |
| Tests collect nothing | Wrong folder or config | Run from the folder with `pyproject.toml`; check `testpaths` |
| Tests fail only when run together | Shared state between tests | Give each test its own `tmp_path`; never write into shared folders |
| A test fails intermittently (flaky) | Unseeded randomness, time, ordering | Seed it, remove time/network, make it independent — a flaky test is a bug in the test |
| Coverage much lower than 78% | Running a subset, or missing `--cov=src` | Run the whole suite with `--cov=src` |
| Seeded bug #2 (removed seed) is *not* caught | Your determinism test compares rounded metrics only | Compare exact metrics or artefact hashes |
| Suite very slow | Data reloaded per test, or training 500 trees per test | `scope="session"` fixtures; keep model tests few and light |
| `ModuleNotFoundError` inside tests | Interpreter mismatch | Same rule as always: `python -m pytest` inside your environment |

More: [troubleshooting.md](troubleshooting.md) ·
[course troubleshooting](../../troubleshooting/index.md).

## 11. Cleanup

```powershell
# 🪟 from examples/churn
Remove-Item -Recurse .pytest_cache, __pycache__, src\__pycache__, tests\__pycache__, .coverage -ErrorAction SilentlyContinue
python generate_data.py     # if you deleted data/ in step 5
```

```bash
# 🐧
rm -rf .pytest_cache __pycache__ src/__pycache__ tests/__pycache__ .coverage
```

✅ Verify: `python -m pytest` is green on a clean run. Your test files, bug-catch
matrix, and coverage report are the evidence you keep.

## 12. Optional extension tasks

1. **Threshold realism:** run the floor test with three seeds and report the AUC
   spread — then justify a floor that is not flaky.
2. **Property-based testing:** add a `hypothesis` test that any generated valid
   frame passes `split_xy`'s column contract.
3. **Mutation check:** deliberately break one assertion and confirm pytest
   reports it — proving your *reporting* works, not just your tests.
4. **Speed:** measure per-test durations (`pytest --durations=5`) and eliminate
   the slowest one.

---

**Next:** [independent-challenge.md](independent-challenge.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*