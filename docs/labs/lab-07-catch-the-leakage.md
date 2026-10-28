# LAB-07 — Catch the Leakage

## 1. Lab identity

| | |
|---|---|
| **Lab ID** | **LAB-07** |
| **Difficulty / topic** | 🔧 Intermediate · Testing for ML (leakage & preprocessing) |
| **Prerequisite module** | [07 — Unit, data, model, integration, regression testing](../modules/07-testing-for-ml/index.md) + [05](../modules/05-reproducible-training-pipelines/index.md) |
| **Fixture** | `examples/labs/lab-07/leaky_model.py` |
| **Estimated time** | 120 minutes · free, local, offline |

## 2. Scenario and background

A demo model reports `roc_auc = 1.0000` on the customer dataset. Perfect.
Someone is already drafting the release note. Three seeded defects make
that number possible: two features that *know the answer*, preprocessing
fitted on data it should not see, and an "evaluation" that scores the
training set. Your job is not to admire the score — it is to build the
**tests that make this impossible to repeat silently**.

## 3. Learning objectives

By the end you can:

1. Recognise three classic leakage classes: target-derived features,
   fit-scope errors (preprocessing before split), and holdout misuse.
2. Write pytest tests that **fail against the leaky implementation** and
   pass against a corrected one (red→green evidence).
3. Reframe a script into testable functions (seams) without changing
   behaviour you intend to keep.
4. State what a "too good" metric should trigger before any celebration.

## 4. Prerequisites and estimated time

- Modules 05 + 07 read; `pytest` available (verified 9.1.1).
- `python examples/labs/make_data.py`.
- **120 min** (reproduce 15 · seams 25 · tests 55 · fix 15 · write-up 10).

## 5. Student task statement

Create `fixed.py` (a corrected, importable version of the leaky logic)
and `test_leakage.py` with **≥4 tests** that (a) FAIL when pointed at
`leaky_model` as shipped, and (b) PASS against `fixed.py`. Deliver the
red and green transcripts plus a short explanation of each defect's real
name and its blast radius.

## 6. Required dataset and setup instructions

```powershell
# 🪟 Windows — PowerShell
cd examples\labs\lab-07
python leaky_model.py
# ✅ "reported roc_auc = 1.0000" + "suspiciously good."
```
That 1.0000 is your starting red flag.

## 7. Starter files

| File | Role |
|---|---|
| `leaky_model.py` | the audit target (runs; looks brilliant; is wrong) |
| `test_leakage.py` | **you write it** (spec + starter patterns in solutions) |
| `fixed.py` | **you write it** (the corrected implementation) |

## 8. Numbered implementation steps

**Step 1 — Name the smell, quantify it.** Run the script; record the
AUC. Then compute the honest baseline: same features **minus** the
suspicious enrichment columns, proper train/test split, seeded model.
✅ Checkpoint: you have two numbers (leaky vs honest) and can state the
gap in one line.

**Step 2 — Find all three.** Checklist to walk: (i) *when* does each
feature become known relative to the prediction moment? (ii) where is
`fit()` called, and on which rows? (iii) where does the reported metric
come from — which rows?
✅ Checkpoint: three defects written with their standard names
(target leakage · preprocessing leakage · evaluation-on-train).

**Step 3 — Create seams.** Restructure into functions
(`load()`, `build_features(df)`, `split(X, y)`, `fit(train)`,
`evaluate(model, holdout)`) inside `fixed.py`. Behaviour you *keep*:
same model family, same metrics format.

**Step 4 — Write the tests (the deliverable).** ≥4, e.g.:
- feature list must not contain any post-outcome column (guard list);
- `fit` receives only training rows (pass a sentinel: holdout rows must
  not influence scaler statistics — assert scaler mean ≠ full-data mean
  or use a spy);
- `evaluate` is computed on rows never passed to `fit` (assert disjoint
  indices);
- honest AUC is below a sanity ceiling (e.g. `< 0.95`) — a "too good"
  tripwire.

✅ Red first: run them against the shipped module → FAIL. Paste it.

**Step 5 — Go green.** Point the same tests at `fixed.py` → PASS.
✅ Checkpoint: both transcripts in `evidence.md`.

**Step 6 — Write the blast radius.** For each defect: what decision it
would have corrupted (release? threshold? business claim?).

## 9. Commands and expected results

| Command | Expected |
|---|---|
| `python leaky_model.py` | `reported roc_auc = 1.1000…` → real: **1.0000**, "suspiciously good" |
| `python -m pytest test_leakage.py -v` (as shipped target) | **FAILURES** — your tests catch the three defects |
| same command against `fixed.py` | **all pass** |
| honest re-computation (Step 1) | AUC materially below 1.0 (record yours) |

## 10. Acceptance criteria (objective)

- [ ] Three defects named with standard terminology.
- [ ] ≥4 tests: red transcript (against shipped code) pasted.
- [ ] Same tests green against `fixed.py`; both transcripts kept.
- [ ] Honest-vs-leaky metric gap recorded with numbers.
- [ ] Blast-radius paragraph: one line per defect.
- [ ] Tripwire test (sanity ceiling on reported AUC) included.

## 11. Troubleshooting and recovery

| Symptom | Cause | Fix |
|---|---|---|
| tests pass against the leaky code too | assertions too weak (e.g. only checking output shape) | assert *relationships*: disjoint indices, feature guard-list, fit-scope |
| cannot import `leaky_model` for tests | script executes on import | wrap the work in functions; or load via `importlib` and monkeypatch |
| `fixed.py` AUC still ~1.0 | an enrichment column survives | re-check feature list and `load()` — the hint columns are obvious once listed |
| pandas `get_dummies` column mismatch between versions of the code | feature sets diverged | pin the column order in one place (Module 05 lesson) |

## 12. Reflection questions

1. Which of the three defects would a *code review* likely catch, and
   which needs a *test*? Why?
2. The enrichment columns are plausible ("retention offers are real!").
   What process question — not code — prevents them entering training?
3. Where do you draw the "prediction moment" line in your own domain
   example? Name one feature that is safe only if refreshed hourly.

## 13. Optional challenge tasks

1. Add a `pytest` fixture that builds a tiny synthetic frame with a
   guaranteed perfect-leak column — a detector for future leaks.
2. Implement a "leak audit" helper: given a feature list and a knowledge
   timeline, flag features known only post-outcome.
3. Re-run the honest baseline with 5 seeds and report mean ± std — does
   the honest number still support a release?

## 14. Rubric / checklist

| Points | Criterion |
|---|---|
| 3 | three defects correctly named and located |
| 5 | ≥4 tests with genuine red (pasted) |
| 4 | same tests green against `fixed.py` |
| 2 | honest-vs-leaky numbers recorded |
| 2 | blast radius per defect |
| **16** | **total** · ≥12 = pass |

## 15. Cleanup

```powershell
cd examples\labs\lab-07
Remove-Item evidence.md -ErrorAction SilentlyContinue   # keep it if submitting
Remove-Item -Recurse __pycache__, .pytest_cache -ErrorAction SilentlyContinue
```

---

**After attempting:** reference tests + a corrected implementation live in
[`examples/labs/solutions/lab-07/`](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/labs/solutions/lab-07).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../about/index.md).*