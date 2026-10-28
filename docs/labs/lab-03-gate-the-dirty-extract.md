# LAB-03 — Gate the Dirty Extract

## 1. Lab identity

| | |
|---|---|
| **Lab ID** | **LAB-03** |
| **Difficulty / topic** | 🌱 Beginner · Data quality & validation |
| **Prerequisite module** | [04 — Data quality, validation, and versioning](../modules/04-data-quality-validation-versioning/index.md) |
| **Fixture** | `examples/labs/lab-03/check_data.py` + `examples/labs/data/customers_dirty.csv` |
| **Estimated time** | 105 minutes · free, local, offline |

## 2. Scenario and background

Monday, 08:40: the upstream team "renamed a column". Your pipeline
consumed the new extract anyway, trained on it, and produced a model
nobody trusts. The extract `customers_dirty.csv` carries five seeded
defect classes — missing values, invalid ranges, duplicate records,
schema drift, and a bad label domain — plus a dtype trap. Two checks in
`check_data.py` are already written (your worked examples); four are
stubs that raise `NotImplementedError`. A gate that cannot fail is not a
gate.

## 3. Learning objectives

By the end you can:

1. Write validation checks that fail loudly, with counts and column names.
2. Cover the five defect classes plus dtype coercion traps.
3. Make validation a **pipeline stage** (exit codes), not a log message.
4. Decide, and defend, what the expected schema contract should be when
   the source itself changed.

## 4. Prerequisites and estimated time

- Module 04 read; pandas comfort (`.isna()`, boolean masks).
- `cd examples/labs && python make_data.py` (generates the dirty file).
- **105 min** (read 15 · implement 50 · evidence 25 · reflection 15).

## 5. Student task statement

Finish the four stub checks in `check_data.py` so that
`python check_data.py --strict` exits **1** and reports **every seeded
defect class** by name and count — then write the one-paragraph ruling on
the schema change: should the gate accept `promo_flag`/no `support_calls`
as the new contract, or reject until the pipeline is updated?

## 6. Required dataset and setup instructions

```powershell
# 🪟 Windows — PowerShell
cd examples\labs
python make_data.py
cd lab-03
python check_data.py            # the "before" state
python check_data.py --strict ; echo "exit=$LASTEXITCODE"
```
🐧: `… && python check_data.py --strict; echo "exit=$?"`.

Real "before" output: **5 errors, 4 check(s) not implemented**, exit 1.

## 7. Starter files

| File | Role |
|---|---|
| `check_data.py` | 2 implemented checks (examples) + 4 stubs (your task) |
| `../data/customers_dirty.csv` | 603 rows carrying the seeded defects |
| `../data/customers_clean.csv` | control: same generator, no defects |

## 8. Numbered implementation steps

**Step 1 — Inventory by eye.** Load the dirty CSV in three lines of
pandas; eyeball `head()`, `dtypes`, `isna().sum()`, duplicated ids.
✅ Checkpoint: you can name at least four of the five classes before
running any check.

**Step 2 — Understand the examples.** Read `check_missing` and
`check_ranges`: note count + column + severity prefix (`ERROR`).
✅ Checkpoint: your stubs will follow the same output shape.

**Step 3 — Implement `check_duplicates`.** Duplicate `customer_id` rows
*and* fully duplicated records (both exist). ✅ finds **3** duplicate ids.

**Step 4 — Implement `check_label_domain`.** `churned ∈ {0,1}` only.
✅ finds the row with `churned = 7`.

**Step 5 — Implement `check_schema`.** Compare columns to
`EXPECTED_COLUMNS`; report missing/unexpected (order matters — say so).
✅ names `support_calls` gone and `promo_flag` new (as drift, per your
ruling).

**Step 6 — Implement `check_cardinality`.** `contract_type` must be one
of `monthly|one_year|two_year` — catching the empty cells as domain
errors in addition to the missing-value errors.
✅ checkpoint: `--strict` output names **all five classes**; count the
`ERROR` lines (expected ≥ 9).

**Step 7 — Write the ruling.** Schema change: accept-as-new-contract vs
reject-until-updated — one paragraph with the safer default justified.

## 9. Commands and expected results

| Command | Expected |
|---|---|
| `python check_data.py` (as shipped) | `5 error(s), 4 check(s) not implemented` |
| `python check_data.py --strict` (finished) | all five classes reported with counts; exit 1 |
| `python check_data.py --csv ../data/customers_clean.csv --strict` | 0 errors — **the control must pass** |
| `python -m pytest -q` (your tests, optional but graded in §13) | green |

## 10. Acceptance criteria (objective)

- [ ] All four stubs implemented; no `NotImplementedError` remains.
- [ ] `--strict` on the dirty file reports each class: missing · range ·
      duplicates · label domain · schema · cardinality, with counts.
- [ ] Control run on `customers_clean.csv` exits **0** (no false alarms).
- [ ] One named false-positive you *deliberately* suppress, with reasoning
      (empty `contract_type` shows up twice — deduplicate or justify).
- [ ] Schema ruling paragraph written.

## 11. Troubleshooting and recovery

| Symptom | Cause | Fix |
|---|---|---|
| control file reports errors | checks tuned to the dirty file only | bounds/domains must come from the contract, not from what you observed |
| dtype check double-counts NaN | `to_numeric(errors="coerce")` turns empty cells NaN too | subtract genuine nulls (the shipped example shows how) |
| schema check passes but drift missed | only "missing" checked, not "unexpected" | both directions must be reported |
| exit code always 0 | `--strict` not passed, or errors counted as strings | `echo "exit=$LASTEXITCODE"` right after the call |

## 12. Reflection questions

1. Which defect class would have broken training *loudest*, and which
   would have failed *silently*? Why the difference?
2. A new month's extract has a legitimately new column. What process —
   not code — keeps that from becoming an outage?
3. Where is the line between validation and transformation? Name one
   defect you should **never** auto-fix.

## 13. Optional challenge tasks

1. Add pytest coverage: one test per defect class using tiny inline
   DataFrames (no file I/O).
2. Emit a machine-readable `validation_report.json` next to the console
   output.
3. Wire the gate into `examples/labs/lab-05/pipeline_flawed.py` as its
   first stage.

## 14. Rubric / checklist

| Points | Criterion |
|---|---|
| 6 | four stubs implemented, all five classes reported with counts |
| 3 | control run clean (false-alarm discipline) |
| 2 | duplicate-id and full-record duplication both handled |
| 2 | schema ruling paragraph with a justified default |
| 2 | output readable: severity, column, count on every line |
| **15** | **total** · ≥12 = pass |

## 15. Cleanup

```powershell
Remove-Item validation_report.json -ErrorAction SilentlyContinue
Remove-Item -Recurse __pycache__ -ErrorAction SilentlyContinue
```
The datasets are regenerable — never edit them by hand.

---

**After attempting:** a complete reference gate lives in
[`examples/labs/solutions/lab-03/`](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/labs/solutions/lab-03).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../about/index.md).*