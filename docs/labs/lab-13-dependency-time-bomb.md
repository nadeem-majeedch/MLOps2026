# LAB-13 — The Dependency Time Bomb

## 1. Lab identity

| | |
|---|---|
| **Lab ID** | **LAB-13** |
| **Difficulty / topic** | 🔧 Intermediate · Dependency incompatibility & automated tests |
| **Prerequisite module** | [02 — Python, Git, CLI, environments](../modules/02-python-git-cli-environments/index.md) + [12 — CI/CD](../modules/12-cicd-github-actions/index.md) |
| **Fixture** | `examples/labs/lab-13/` |
| **Estimated time** | 75 minutes · free, local, offline |

## 2. Scenario and background

A two-year-old internal tool was written when `numpy 1.23` was current.
Someone upgraded the shared environment to **numpy 2.5.3** — the tool
now crashes, and nobody knows why because nobody wrote a compatibility
test. The environment here reproduces that history exactly: the module
uses `np.float`, removed after its long deprecation, and the installed
numpy refuses it with a message that *tells you the fix*. This lab is
about turning an outage into a test.

## 3. Learning objectives

By the end you can:

1. Read a traceback as a diagnosis: which symbol, which version boundary,
   which official guidance.
2. Distinguish *code* incompatibility from *pin* incompatibility, and fix
   the right one.
3. Write a compatibility test that fails the moment an API disappears.
4. State a dependency policy: pins, ranges, upgrade cadence, who owns it.

## 4. Prerequisites and estimated time

- Module 02 (environments) read; pytest available.
- No dataset needed. `python -m pip show numpy` → `2.5.3` (environment
  fact — record it).
- **75 min** (reproduce 10 · diagnose 20 · fix 20 · policy 25).

## 5. Student task statement

Capture the red failure, fix `legacy_numpy_code.py` so the suite passes
on the **installed** stack without pinning numpy backwards, add a
compatibility test that guards the API you relied on, and write a
10-line dependency policy for the team (pins, who upgrades, how CI
catches this next time).

## 6. Required dataset and setup instructions

```powershell
# 🪟 Windows — PowerShell — from examples/labs/lab-13
python legacy_numpy_code.py
python -m pytest test_compat.py -v
```
Real observed: the script raises `AttributeError` pointing at numpy's
deprecation note; the suite reports **2 failed** with the same root
cause (numpy's own message names the replacement: use builtin `float`).

## 7. Starter files

| File | Role |
|---|---|
| `legacy_numpy_code.py` | the 2023-era code (`np.float`) |
| `test_compat.py` | 2 red tests = your starting evidence |
| `dependency_policy.md` | **you write it** (starter outline below) |

## 8. Numbered implementation steps

**Step 1 — Reproduce and capture.** Run both commands (§6); paste the
*relevant* traceback lines (symbol, removal note, numpy version).
✅ Checkpoint: you can name the version boundary in one sentence.

**Step 2 — Decide the fix class.** Two options: (a) pin numpy back to
`<1.24` — and lose every other package that needs modern numpy;
(b) fix the code for the installed stack. Write one line justifying your
choice (the lab demands (b)).
✅ rationale recorded *before* editing.

**Step 3 — Fix the code.** Replace the removed alias (and audit for
sibling aliases: `np.int`, `np.bool`, `np.object` — same family).
✅ `python -m pytest test_compat.py -q` → **2 passed**.

**Step 4 — Guard it.** Add `test_uses_supported_numpy_apis()` asserting
your fixed helper runs and, stronger, that the source no longer contains
removed aliases (a static tripwire for copy-paste regressions).
✅ suite now ≥3 tests, green.

**Step 5 — Prove the pipeline angle.** Simulate CI: run the suite from a
fresh shell/cwd; note the exact command CI would use
(`python -m pytest test_compat.py -q`) and its exit code.

**Step 6 — Write the policy** (`dependency_policy.md`, ~10 lines):
exact pins vs ranges (and where each belongs — note
`requirements-docker.txt` uses exact pins on purpose), upgrade cadence,
who approves, how CI detects breakage, and the "record installed
versions" habit (`pip freeze` artefact).

## 9. Commands and expected results

| Command | Expected |
|---|---|
| `python legacy_numpy_code.py` (before fix) | `AttributeError` naming `np.float` + official removal note |
| `python -m pytest test_compat.py -v` (before) | **2 failed** |
| after your fix | **≥3 passed** |
| `python -m pip show numpy` | environment record: `2.5.3` |
| rerun suite from another cwd | same result (path discipline) |

## 10. Acceptance criteria (objective)

- [ ] Red transcript pasted, with the version boundary named.
- [ ] Fix choice justified (code fixed, not environment downgraded).
- [ ] Suite green on the installed stack (≥3 tests incl. your guard).
- [ ] Source audit: no removed aliases anywhere in the file.
- [ ] `dependency_policy.md`: pins-vs-ranges, cadence, owner, CI check —
      8–15 lines, concrete for *this* repo.
- [ ] Exact CI command + exit code recorded.

## 11. Troubleshooting and recovery

| Symptom | Cause | Fix |
|---|---|---|
| tests still fail after fixing `np.float` | a sibling alias (`np.int`, `np.bool`) remains | grep the file for `np.` followed by builtin names |
| fix "works" but type changed | `np.float64` vs builtin `float` semantics | numpy's own note says builtin `float` is behaviour-preserving here — read it |
| suite passes locally, would fail in CI | CI installs from different pins | your policy must name the file CI installs from |
| tempted to pin numpy back | that blocks every modern dependency | write the cost line in your policy — this is the trap |

## 12. Reflection questions

1. The crash was *loud*. Name a dependency break that is silent, and the
   test that would catch it.
2. Ranges (`>=,<`) vs exact pins: where does each belong in this course's
   repo, and why does `requirements-docker.txt` pin exactly?
3. Who should own upgrades in a team of five — and what does "owner"
   mean when they are on leave?

## 13. Optional challenge tasks

1. Introduce a *second* incompatibility: an API renamed in
   scikit-learn-era code (write the failing test first).
2. Add a `pip check` step to your policy's CI snippet and run it locally.
3. Write a `compat_matrix.md`: package × version × what you rely on.

## 14. Rubric / checklist

| Points | Criterion |
|---|---|
| 3 | red evidence with version boundary named |
| 3 | code fixed, rationale recorded (no downgrades) |
| 4 | ≥3 tests green incl. static guard |
| 3 | dependency policy concrete and repo-specific |
| 2 | CI command + exit code recorded |
| **15** | **total** · ≥11 = pass |

## 15. Cleanup

```powershell
cd examples\labs\lab-13
Remove-Item -Recurse __pycache__, .pytest_cache -ErrorAction SilentlyContinue
# data/ not used by this lab; nothing else generated
```

---

**After attempting:** a reference fix + guard test live in
[`examples/labs/solutions/lab-13/`](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/labs/solutions/lab-13).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../about/index.md).*