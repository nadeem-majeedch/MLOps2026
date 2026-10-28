# LAB-02 — Untangle the Notebook

## 1. Lab identity

| | |
|---|---|
| **Lab ID** | **LAB-02** |
| **Difficulty / topic** | 🌱 Beginner · Project structure & technical debt |
| **Prerequisite module** | [03 — ML project structure and technical debt](../modules/03-ml-project-technical-debt/index.md) |
| **Fixture** | `examples/labs/lab-02/` |
| **Estimated time** | 120 minutes · free, local, offline |

## 2. Scenario and background

The monthly "customer risk snapshot" comes from `analysis_monolith.py` —
a notebook export that grew legs: globals everywhere, the same logic
copy-pasted three times, magic numbers nobody can explain, and the CSV
read three separate times. It runs today (run it — it does). That is
exactly why nobody dares touch it: last quarter a "quick tweak" silently
changed the risk rule in one segment only. You are assigned to make it
maintainable **without changing what it prints**.

## 3. Learning objectives

By the end you can:

1. Separate an analysis into io / logic / reporting layers with one
   implementation per rule.
2. Preserve behaviour during refactoring using a captured baseline.
3. Replace magic numbers with named, sourced configuration.
4. Say what belongs in a notebook versus what belongs in a module.

## 4. Prerequisites and estimated time

- Module 03 read; comfortable with functions, imports, `pathlib`.
- Dataset: `cd examples/labs && python make_data.py` (once).
- **120 min** (baseline 10 · structure 60 · tests 35 · write-up 15).

## 5. Student task statement

Refactor the monolith into a small package (`customer_analysis/`) with a
CLI, **byte-identical output**, one shared risk rule, single-read data
loading, and a pytest suite proving the behaviour. Deliver: the package,
tests, a short design note (what moved where and why), and the baseline
comparison.

## 6. Required dataset and setup instructions

```powershell
# 🪟 Windows — PowerShell
cd examples\labs\lab-02
python analysis_monolith.py > baseline_report.txt   # ✅ capture FIRST
Get-Content baseline_report.txt                     # the reference output
```
🐧: `python analysis_monolith.py > baseline_report.txt`.

Real baseline (authoring machine): three segment rows
(`monthly n=294 … one_year n=184 … two_year n=122 …`), then
`flagged for outreach: 405 (67.5% of 600 customers)` and
`over target (18%) — trim the outreach list`.

## 7. Starter files

| File | Role |
|---|---|
| `analysis_monolith.py` | the monolith (runs today; the exercise) |
| `baseline_report.txt` | captured behaviour — your contract (you create it) |
| target layout | `customer_analysis/{io,features,report}.py`, `__main__.py`, `tests/` |

## 8. Numbered implementation steps

**Step 1 — Freeze behaviour.** Capture the baseline (§6).
✅ Checkpoint: file exists; note the two figures `405` and `67.5%`.

**Step 2 — Draw the seams.** List every distinct job in the monolith
(load · derive risk · aggregate · render). Decide the module each goes
in; write the map in your design note before coding.
✅ Checkpoint: map has no duplicated jobs (the three copy-pasted segments
must collapse to **one** risk function).

**Step 3 — Extract, one function at a time.** `io.load()` (single read),
`features.flag_risk(df)` (one rule), `report.summarise(df)` (grouped
aggregation), `report.render(summary)` (formatting).
✅ Checkpoint: `python -m customer_analysis` runs without errors.

**Step 4 — Diff against the baseline.**
```powershell
python -m customer_analysis > new_report.txt
fc baseline_report.txt new_report.txt    # 🐧 diff -u baseline_report.txt new_report.txt
```
✅ Checkpoint: **no differences**. If there are: fix code, never the
baseline.

**Step 5 — Kill the magic.** `TARGET_FLAG_PCT` moves to
`config.yaml` with a comment saying where the 18% came from (or an
explicit "unsourced — flagged as debt" note).

**Step 6 — Test the seams.** ≥4 tests: risk rule on known rows, loader
rejection of a wrong schema, aggregation counts summing to 600, render
containing the target line.
✅ Checkpoint: `python -m pytest -q` green.

## 9. Commands and expected results

| Command | Expected |
|---|---|
| `python analysis_monolith.py > baseline_report.txt` | baseline captured; ends with `over target (18%)` |
| `python -m customer_analysis > new_report.txt` | runs clean |
| `fc baseline_report.txt new_report.txt` | `FC: no differences encountered` |
| `python -m pytest -q` | all tests pass (≥4) |

## 10. Acceptance criteria (objective)

- [ ] Baseline captured *before* editing, pasted in your design note.
- [ ] Package structure exists with the four responsibilities separated.
- [ ] Risk rule implemented **once** (no per-segment copies).
- [ ] CSV read **once** per run.
- [ ] `fc`/`diff` shows zero differences between old and new output.
- [ ] `TARGET_FLAG_PCT` is named configuration with a sourced comment.
- [ ] ≥4 tests, green.

## 11. Troubleshooting and recovery

| Symptom | Cause | Fix |
|---|---|---|
| diff shows whitespace/line-ending noise | `>` on Windows + `lineterminator` | normalise both files before diffing, or compare stripped lines |
| counts differ by rows | a copy-pasted segment had a subtly different filter | diff the rules first — the baseline tells you *where* to look |
| `ModuleNotFoundError: customer_analysis` | package not next to cwd, or missing `__init__.py` | run from `lab-02/`; check folder layout |
| tests pass, CLI output differs | tests don't assert output | add a render/baseline test |

Recovery: if output drifts and you cannot find why, revert your package
file-by-file (keep the baseline!) until the diff clears, then redo the
last step more carefully.

## 12. Reflection questions

1. Which single change removed the most future bugs — and how would you
   justify it in one sentence to a manager?
2. What would you deliberately **leave** in a notebook next time, and why?
3. The monolith's `405 flagged` is 67.5% of customers — nobody can be
   contacted at that scale. Which module should own that limit, and what
   happens to your refactor when the business caps outreach at 18%?

## 13. Optional challenge tasks

1. Add a `--segment monthly` CLI filter without touching the rules.
2. Make the report render in Markdown (tests must still pin the numbers).
3. Compute technical-debt interest: list 5 defects of the monolith, each
   with a one-line "what it cost / what it could cost".

## 14. Rubric / checklist

| Points | Criterion |
|---|---|
| 3 | Baseline captured and used as the contract |
| 4 | Structure: four responsibilities, one risk implementation, single read |
| 4 | Byte-identical output (`fc`/`diff` evidence) |
| 2 | Configuration extracted and sourced |
| 3 | ≥4 meaningful tests, green |
| 2 | Design note: map + rationale, no weasel words |
| **18** | **total** · ≥14 = pass |

## 15. Cleanup

```powershell
cd examples\labs\lab-02
Remove-Item new_report.txt     # keep baseline_report.txt as evidence
Remove-Item -Recurse __pycache__ -ErrorAction SilentlyContinue
```

---

**After attempting:** a reference restructuring lives in
[`examples/labs/solutions/lab-02/`](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/labs/solutions/lab-02).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../about/index.md).*