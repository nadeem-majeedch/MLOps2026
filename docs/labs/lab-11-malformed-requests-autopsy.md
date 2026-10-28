# LAB-11 — Malformed Requests Autopsy

## 1. Lab identity

| | |
|---|---|
| **Lab ID** | **LAB-11** |
| **Difficulty / topic** | 🔧 Intermediate · API robustness & error design |
| **Prerequisite module** | [10 — Model serving with FastAPI](../modules/10-model-serving-fastapi/index.md) (LAB-10 first if you want to fix *your* service instead) |
| **Fixture** | `examples/labs/lab-11/` |
| **Estimated time** | 90 minutes · free, local, offline |

## 2. Scenario and background

Support tickets say "the API is weird": sometimes 500s, sometimes it
happily scores nonsense, and monitoring shows green while the service is
degraded. `broken_service.py` has no request model at all — a raw
`payload: dict` — and six real defects follow from that one sin.
`characterize.py` fires 10 representative requests (in-process, no server
needed) and prints OBSERVED vs EXPECTED. Your job: diagnose every
mismatch *in writing* before fixing a single line.

## 3. Learning objectives

By the end you can:

1. Characterise a service empirically (request battery → table) instead
   of reading code and hoping.
2. Classify failures: validation absent · crash (500) on bad input ·
   silently accepted garbage · wrong status semantics on degraded state.
3. Fix them with pydantic schemas + explicit status codes, and re-run the
   battery to 10/10.
4. Explain why "200 with an error body" breaks monitoring.

## 4. Prerequisites and estimated time

- Module 10 read; `characterize.py` runs with no dataset.
- **90 min** (characterise 20 · diagnosis 25 · fix 30 · evidence 15).

## 5. Student task statement

Produce `diagnosis.md`: the observed-vs-expected table with one line of
root cause and one line of impact per mismatch; then fix your copy of
`broken_service.py` (or refactor your LAB-10 service under the same
battery) until `characterize.py` prints **10/10 ok**, and add a pytest
regression test per defect class.

## 6. Required dataset and setup instructions

```powershell
# 🪟 Windows — PowerShell — from examples/labs/lab-11
python characterize.py
```
Real observed (authoring machine):
```text
[ok ] valid record              expected  200 observed  200
[FAIL] missing charges          expected  422 observed  500
[FAIL] negative tenure          expected  422 observed  200
[FAIL] charges out of range     expected  422 observed  200
[FAIL] zero tenure (div-by-0)   expected  422 observed  500
[FAIL] unknown contract         expected  422 observed  200
[FAIL] empty records            expected  422 observed  200
[FAIL] records not a list       expected  422 observed  500
[FAIL] no records key           expected  422 observed  500
[FAIL] health degraded          expected  503 observed  200
9/10 mismatches against the HTTP contract.
```

## 7. Starter files

| File | Role |
|---|---|
| `broken_service.py` | six defects (one root sin: no request model) |
| `characterize.py` | the request battery (expected column = contract) |
| `test_regressions.py` | **you write it** (starter in solutions) |

## 8. Numbered implementation steps

**Step 1 — Run the battery** (§6). Paste the full table.
✅ Checkpoint: 9/10 mismatches captured.

**Step 2 — Diagnose before fixing.** For each FAIL: root cause (one
line) + user-visible impact (one line). Group them: 500s from missing/
wrong-shaped input · accepted-out-of-range · empty batch · contract
coercion · degraded-health semantics.
✅ `diagnosis.md` has 9 entries.

**Step 3 — One fix kills most of them.** Introduce pydantic request
models: typed record (with bounds and enum), `records: list[Record]`
with `min_length=1`. Re-run the battery.
✅ Checkpoint: the five validation-driven rows flip to `ok`.

**Step 4 — Division guard.** `tenure_months = 0` must be rejected by the
schema (bounds), not guarded ad hoc in the formula.
✅ zero-tenure row flips to `ok`.

**Step 5 — Degraded semantics.** When `MODEL_MISSING=1`, `/health`
returns **503** (or `{"status":"degraded"}` with 200 — pick one, state
which and why; the battery expects 503).
✅ last row flips to `ok` → **10/10 ok**.

**Step 6 — Regression tests.** One pytest per defect class (5+): run the
battery in-process; assert `failures == 0`.
✅ `python -m pytest test_regressions.py -q` green.

**Step 7 — Live optional.** Start uvicorn and reproduce two cases with
curl (422 body shown) for a human-readable evidence file.

## 9. Commands and expected results

| Command | Expected |
|---|---|
| `python characterize.py` (as shipped) | `9/10 mismatches` |
| after your fixes | `0/10 mismatches` — **10/10 ok** |
| `python -m pytest test_regressions.py -q` | green |
| live: `curl` malformed body | HTTP 422, body names `tenure_months`/`monthly_charges` |
| live: `MODEL_MISSING=1` + `/health` | HTTP 503 (or documented alternative) |

## 10. Acceptance criteria (objective)

- [ ] Before-table captured (9/10 mismatches).
- [ ] `diagnosis.md`: cause + impact for each of the 9 rows.
- [ ] `characterize.py` prints **10/10 ok** after fixes.
- [ ] ≥5 regression tests, green.
- [ ] Health-semantics choice stated explicitly (and why monitoring
      cares).
- [ ] All defects fixed without changing the valid-case response shape
      (tests from LAB-10 still pass, if applicable).

## 11. Troubleshooting and recovery

| Symptom | Cause | Fix |
|---|---|---|
| a row still FAILs after schema added | route still takes `payload: dict` | change the signature to the pydantic model — FastAPI validates on the way in |
| tests fail with import error | battery imports `broken_service` by module name | keep the file name, or update one import line |
| health row expects 503 but you chose "degraded 200" | contract vs your choice | the battery encodes the lab contract — align, then argue your alternative in `diagnosis.md` |
| 422 body has no field name | error handler reformats poorly | keep FastAPI's `detail` entries (they carry `loc`/`msg`) |

## 12. Reflection questions

1. Which single defect would have been impossible without the raw-dict
   signature? Why?
2. "200 with error body" appeared twice (predict-degraded shape, health).
   What alert *fails to fire* because of it?
3. Where do you draw the line between 422 (your input) and 503 (my
   state)? Give a sentence you'd put in the API docs.

## 13. Optional challenge tasks

1. Add a request-ID header echoed in errors and logged — trace one 422
   end to end.
2. Rate-limit the endpoint (in-memory token bucket) with a test.
3. Run the battery against your **LAB-10** service — how many rows fail?
   Fix yours to 10/10 too (that's the real-world version of this lab).

## 14. Rubric / checklist

| Points | Criterion |
|---|---|
| 3 | before-table captured |
| 4 | diagnosis: cause + impact for all 9 rows |
| 4 | 10/10 ok after fixes (output pasted) |
| 3 | ≥5 regression tests green |
| 2 | health-semantics decision stated |
| **16** | **total** · ≥12 = pass |

## 15. Cleanup

```powershell
cd examples\labs\lab-11
Remove-Item -Recurse __pycache__, .pytest_cache -ErrorAction SilentlyContinue
# stop any live server with Ctrl+C; nothing listens by default (battery is in-process)
```

---

**After attempting:** a reference fixed service + regression tests live in
[`examples/labs/solutions/lab-11/`](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/labs/solutions/lab-11).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../about/index.md).*