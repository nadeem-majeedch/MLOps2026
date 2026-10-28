# LAB-11 — reference solution

> Attempt the lab first. This is the answer key, not the assignment.

**Files in this folder:**

- `fixed_service.py` — the repaired service (reference). **Verified:** all
  10 characterisation rows return the expected status (200/422/503) on the
  authoring machine.
- `test_regressions.py` — the regression starter promised by lab.md §7.
  **Verified:** `5 passed` against `fixed_service`.
- this README — the diagnosis you must write in your own words.

## Verified characterisation transcript (authoring machine)

```text
== LAB 11 characterisation ==
[ok ] valid record               expected  200 observed  200
[FAIL] missing charges            expected  422 observed  500  | Internal Server Error
[FAIL] negative tenure            expected  422 observed  200  | {"predictions":[{"probability":0.0,"flag":0,"contract":"monthly"}]}
[FAIL] charges out of range       expected  422 observed  200  | {"predictions":[{"probability":0.0133,"flag":0,"contract":"monthly"}]}
[FAIL] zero tenure (div-by-0)     expected  422 observed  500  | Internal Server Error
[FAIL] unknown contract           expected  422 observed  200  | {"predictions":[{"probability":0.7383,"flag":1,"contract":"prepaid"}]}
[FAIL] empty records              expected  422 observed  200  | {"predictions":[]}
[FAIL] records not a list         expected  422 observed  500  | Internal Server Error
[FAIL] no records key             expected  422 observed  500  | Internal Server Error
[FAIL] health degraded            expected  503 observed  200  | {"error":"no model loaded","predictions_available":false}

9/10 mismatches against the HTTP contract.
Explain every FAIL before you fix anything (lab.md step 3).
```

## Autopsy: what each row proves (5 + 4 diagnosis)

**Group A — silent acceptance (observed 200, should be 422):**
`negative tenure`, `charges out of range`, `unknown contract`,
`empty records`. The service *scores garbage* — worse than crashing,
because a caller gets a confident number instead of an error.
**Cause:** no input constraints; handler accepts anything JSON-shaped.
**Fix:** Pydantic bounds/enums + `min_length=1` on the records list.

**Group B — crashes (observed 500):**
`missing charges`, `zero tenure`, `records not a list`,
`no records key`. **Cause:** unchecked indexing/attribute access and a
div-by-zero path; no schema layer at all.
**Fix:** the same Pydantic model — a missing key becomes a named 422
before your code ever runs. (500s are for *your* bugs, never for user
input.)

**Group C — lying health check:**
`health degraded` returned **200** with an error body. **Cause:**
status code chosen by convenience instead of by meaning.
**Fix:** 503 (or `status:"degraded"` with 200 **consistently** — pick one
meaning and keep it; the contract in this lab says 503).

## Why exactly 9 flipped and 1 stayed

After the fixes, the five validation-driven rows (Group A) flip to `ok`
— they are pure input-shape issues. The crash rows depend on *how* you
structured validation (they should also become 422), and the health row
needs an explicit status decision. Your write-up must state which rows
you changed code for and why the remaining `ok` row needed nothing.

## Reasoning checkpoints (model answers)

- **422 vs 500:** 422 = "you asked wrongly" (caller can fix it); 500 =
  "I broke" (you fix it). Misclassifying input errors as 500 destroys
  client retry logic and hides your own bugs in the same bucket.
- **Why characterise before fixing?** The transcript is the baseline;
  without it you cannot prove which rows flipped because of your change
  versus because of hope.
- **Does a probability of 0.0 for negative tenure mean the model is
  robust?** No — it means the pipeline coerced bad input into a plausible
  number. Silent coercion is a correctness bug with a friendly face.

## Common wrong answers

- Catching all exceptions → 200 with an "error" field (two wrongs).
- Validating only the happy path in the handler while the schema is
  unconstrained — next endpoint reintroduces the bug.
- Fixing the code but never re-running `characterize.py` — the flipped
  rows are your evidence.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../../docs/about/index.md).*