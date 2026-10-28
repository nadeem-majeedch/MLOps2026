# Troubleshooting — Module 07

Symptoms, real causes, and fixes for the testing module. See also the
[course-wide troubleshooting hub](../../troubleshooting/index.md).

---

## 1. Setup and collection

| Symptom | Likely cause | Fix |
|---|---|---|
| `pytest: command not found` / `'pytest' is not recognized` | Console scripts not on PATH | Run `python -m pytest` — always use the module form inside your environment |
| `ImportError: cannot import name 'segment'` | Tests run from wrong folder, or `src` not a package | Run from the folder containing `pyproject.toml`; ensure `src/` has `__init__.py` or is importable per Module 03's layout |
| `collected 0 items` / "no tests ran" | File not named `test_*.py`, or `testpaths` points elsewhere | Check naming convention and `[tool.pytest.ini_options] testpaths` |
| `ValueError: plugin already registered` | Two pytest installs (global + venv) | Activate the environment; `python -m pytest --version` shows the interpreter in use |

## 2. Failures and flakiness

| Symptom | Likely cause | Fix |
|---|---|---|
| Tests fail only when run **together**, pass alone | Shared state: a file, `os.chdir`, global variable, or env var mutated by another test | Give each test its own `tmp_path`; never chdir without restore; make tests independent |
| A test fails **intermittently** | Time, randomness, network, or dict/set ordering | Seed all randomness (`random_state`), freeze/stub time, remove network — a flaky test is a bug in the test |
| Performance floor fails at 0.7000 but passed yesterday, no code changed | Threshold set too close to measured noise | Measure spread across ≥5 seeds (lab extension 1) and set the floor below the worst-case spread |
| Floor fails after `pip install -U` | "Moved world": library version drift | Compare `pip freeze` against your recorded lockfile (Module 02); pin, don't chase |
| `test_same_seed_gives_same_metrics` fails on another machine | Unpinned thread counts / library nondeterminism | Pin versions; set thread env vars (`OMP_NUM_THREADS=1`) if needed; document the supported platform |
| Seeded bug #2 (removed `random_state`) is *not* caught | Determinism test compares loosely rounded metrics | Compare exact values or hashes of predictions |

## 3. Coverage questions

**"Coverage says 78% — is that bad?"** There is no universal number. Ask instead:
*which* lines are uncovered, and for each: test it or justify it. The course
suite deliberately leaves the CLI parser and report printer uncovered (manual
paths); that is a judgement, not an accident.

**Coverage dropped after I added code.** Expected — new code, new untested
lines. Add tests in the layer that matches what the new code does.

**`coverage: command not found`.** `python -m pytest --cov=src` requires
`pytest-cov`: `python -m pip install pytest-cov`.

## 4. Design smells in your own suite

- **Many tests, one assert each that can't fail** (`assert x is not None`) —
  rewrite as property assertions (see [independent-challenge.md](independent-challenge.md) task 4).
- **Testing the library, not your code** — `assert StandardScaler works` teaches
  nothing; test *your* glue, contracts, and thresholds.
- **Only happy-path data** — every schema test needs a partner that feeds a
  malformed file and expects rejection (the meta-test rule).
- **Suite slower than ~30 s** — profile with `pytest --durations=5`; usually
  repeated data loads (fix `scope="session"`) or training too many trees per test.

## 5. Still stuck?

1. Run the single failing test with `python -m pytest tests/test_x.py::test_name -vv`.
2. Read the **assertion message** — the course's tests put the numbers in them.
3. Bisect: `git stash` (or undo) recent changes and re-run — find the change that broke it.
4. Check [references.md](references.md) for pytest's own documentation on the
   error text you are seeing.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*