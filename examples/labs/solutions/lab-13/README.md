# LAB-13 — reference solution

> Attempt the lab first. This is the answer key, not the assignment.

## Verified red transcript (authoring machine, Python 3.14, NumPy 2.5.3)

```text
$ python -m pytest test_compat.py -q
FAILED test_compat.py::test_bucket_charge_runs_on_a_modern_stack - AttributeError: module 'numpy' has no attribute 'float'.
FAILED test_compat.py::test_summarise_is_numeric - AttributeError: module 'numpy' has no attribute 'float'.
2 failed in 0.35s
```

The error text itself names the boundary: `np.float` was deprecated in
**NumPy 1.20** and removed in **1.24** — on 2.5.3 it can only raise.

## Diagnosis (the reasoning checkpoints, model answers)

- **Why it worked before:** whoever wrote the code ran NumPy < 1.24,
  where `np.float` still resolved to the builtin `float`. The failure is
  not caused by *your* change — it was dormant in the repo, waiting for
  a newer environment.
- **Fix direction: change the code, not the environment.** Downgrading
  NumPy to <1.24 would be re-creating the time bomb (and 1.24 is three
  major versions behind — you would inherit every CVE fixed since).
  Replace `np.float` → `float`, `np.int` → `int`, `np.bool` → `bool`
  (builtins are what the aliases always pointed at).
- **`np.float64` vs `float`:** `np.float64` is a NumPy scalar *type*;
  the deprecated alias was the *builtin*. Pick `float` unless you
  specifically need a NumPy dtype — the error message says the same.

## What "green" looks like

```text
$ python -m pytest test_compat.py -q
3 passed        # the 2 shipped tests + the guard test YOU added
```

The guard test asserts, in one line, that no removed alias survives:
e.g. walk the module's source (`ast` or a simple `assert "np.float" not
in src`) or `assert not hasattr(np, "float") is False`-style canaries —
the point is a test that fails again the next time someone reintroduces
an alias.

## Source audit method

```powershell
# 🪟 PowerShell
Select-String -Path legacy_numpy_code.py -Pattern 'np\.(float|int|bool|object|str)\b'
# 🐧 Linux/macOS
grep -nE 'np\.(float|int|bool|object|str)\b' legacy_numpy_code.py
```

Expected after the fix: **no matches**.

## dependency_policy.md — what earns full marks

8–15 concrete lines, not boilerplate. Model answer skeleton:

1. **Pins vs ranges:** application dependencies *pinned* exactly in a
   lock/requirements file (this is what CI installs); ranges only in
   libraries you publish.
2. **Cadence:** scheduled refresh (e.g. monthly) + on-demand for
   security advisories — never "whenever someone notices".
3. **Owner:** a named person/team per dependency group.
4. **CI check:** a job that installs from the lock and runs the test
   suite, plus an outdated/advisory scan (e.g. `pip list --outdated`,
   `pip-audit`) allowed to fail loudly, not silently skipped.

## Common wrong answers

- Downgrading NumPy "to make it pass" — freezes the bomb, breaks the
  guard test's justification.
- Pasting my transcript without running it — the course's rule is
  evidence-before-claim; your numbers come from your machine.
- Writing the policy for a generic SaaS team instead of *this* repo.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../../docs/about/index.md).*