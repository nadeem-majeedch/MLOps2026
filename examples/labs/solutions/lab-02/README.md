# LAB-02 — reference solution

> Attempt the lab first. This is the answer key, not the assignment.

## The target figures (must survive the refactor unchanged)

Running the monolith as shipped:

```text
== customer risk snapshot ==
monthly : n=294  risk=204 (69.4%)  avg=68.98  churn=26.2%
one_year: n=184  risk=111 (60.3%)  avg=67.68  churn=4.3%
two_year: n=122  risk= 90 (73.8%)  avg=67.06  churn=4.9%
flagged for outreach: 405 (67.5% of 600 customers)
over target (18%) — trim the outreach list
```

The two checkpoint numbers are **405 flagged** and **67.5% of 600
customers**. Any refactor that changes either number is wrong — that is
what the "no differences" checkpoint protects.

## What the refactor must produce

A package you can run as a module:

```powershell
python -m customer_analysis     # ✅ runs, same numbers as the monolith
python -m pytest -q             # ✅ green
diff <(original output) <(new output)   # ✅ no differences
```

A shape that satisfies the lab (adapt names to what your lab doc asks):

```
customer_analysis/
├── __init__.py
├── __main__.py      # CLI entry: orchestrates the stages
├── load.py          # one job: read the extract
├── clean.py         # one job: fix types, drop nothing silently
├── score.py         # one job: risk rules
├── report.py        # one job: print the snapshot
└── config.py        # thresholds (18% target) in ONE place
tests/
└── test_analysis.py # golden-number tests: 405, 67.5%, per-contract rows
```

## Reasoning checkpoints (model answers)

- **Why three copy-pasted segments in the map?** The monolith repeats
  the same per-contract block — that is why a rule change must be made
  three times and is made twice. One function, called three times,
  removes the class of bug entirely.
- **Why does the golden output matter more than the tests being green?**
  Green tests only prove the new code does what the new code expects.
  The diff against the original output proves the *behaviour* survived
  the move — that is the actual acceptance criterion for a refactor.
- **Where must the 18% target live?** In `config.py`, once. A threshold
  buried inside a loop is technical debt with an interest rate.

## Common wrong answers

- "Refactored" by rewriting the logic and getting different numbers —
  a rewrite is not a refactor; the output must be identical.
- Deleting the awkward rows to make tests pass — behaviour change, not
  structure change.
- No golden test — the next refactor will silently break it again.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../../docs/about/index.md).*