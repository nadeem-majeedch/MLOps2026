# LAB-10 — Serve It

## 1. Lab identity

| | |
|---|---|
| **Lab ID** | **LAB-10** |
| **Difficulty / topic** | 🔧 Intermediate · Model serving & REST APIs |
| **Prerequisite module** | [10 — Model serving and REST APIs with FastAPI](../modules/10-model-serving-fastapi/index.md) |
| **Fixture** | `examples/labs/lab-10/` (model trainer + acceptance tests) |
| **Estimated time** | 135 minutes · free, local, offline |

## 2. Scenario and background

The churn model trains fine in the pipeline; the product team wants it
over HTTP *today*. You are handed `train_model.py` (already produces
`model.joblib` + `model_info.json`) and `test_service.py` — the API
contract as executable acceptance tests. Your deliverable is `app.py`:
the smallest honest service that satisfies the contract, loads the model
once, and refuses bad input with **useful** 422s. The tests skip until
`app.py` exists — that skip is the honest state of an undone exercise.

## 3. Learning objectives

By the end you can:

1. Design request/response schemas with pydantic that encode the *data
   contract* (bounds, enums, non-empty batches).
2. Load a model once at startup and serve predictions deterministically.
3. Write error responses that name the offending field (a 422 a human
   can act on).
4. Drive development from acceptance tests (contract-first).

## 4. Prerequisites and estimated time

- Module 10 read; fastapi/pydantic installed (verified in the course env).
- **135 min** (model 10 · contract reading 15 · implement 70 · live run
  25 · write-up 15).

## 5. Student task statement

Create `examples/labs/lab-10/app.py` exposing FastAPI `app` so that all
10 acceptance tests pass, then run the service live and exercise
`/health`, `/model-info`, `/predict` (valid **and** malformed) with real
requests. Evidence: pytest green + curl transcript + your one-paragraph
API design note (why 422, why one model load, why threshold echoed).

## 6. Required dataset and setup instructions

```powershell
# 🪟 Windows — PowerShell — from examples/labs/lab-10
python train_model.py             # ✅ wrote model.joblib + model_info.json
python -m pytest test_service.py -v
# ✅ as shipped: 10 skipped  (reason: "create app.py first")
```

## 7. Starter files

| File | Role |
|---|---|
| `train_model.py` | produces the model + `model_info.json` (run first) |
| `test_service.py` | 10 acceptance tests = the contract (skip until `app.py`) |
| `app.py` | **you write it** — reference in solutions |

Contract summary (also in the test file): `GET /health`,
`GET /model-info`, `POST /predict` with `{"records": [...]}`, threshold
echoed as `0.5`, 422s naming the field, empty batch = 422.

## 8. Numbered implementation steps

**Step 1 — Train the model** (§6). ✅ files exist.

**Step 2 — Read the contract as a spec.** Skim the 10 tests; map each to
an endpoint/behaviour (a 4-row table). ✅ every test has a home.

**Step 3 — Schemas.** `tenure_months` 0–120, `monthly_charges` 0–500,
`support_calls` 0–50 int, `contract_type` enum of three; `records`
`min_length=1`. ✅ malformed input never reaches your scoring function.

**Step 4 — App.** Load `model.joblib` once at import/startup; three
routes; `/predict` returns probability + flag at threshold 0.5 and the
threshold itself.

**Step 5 — Make the tests green.**
```powershell
python -m pytest test_service.py -v     # ✅ 10 passed
```

**Step 6 — Live proof.**
```powershell
python -m uvicorn app:app --port 8010    # 🐧 same; or python -c "…" if preferred
curl http://127.0.0.1:8010/health
curl http://127.0.0.1:8010/predict -H "Content-Type: application/json" -d '{"records":[{"tenure_months":12,"monthly_charges":85,"support_calls":6,"contract_type":"monthly"}]}'
curl -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8010/predict -H "Content-Type: application/json" -d '{"records":[{"tenure_months":999,"contract_type":"monthly"}]}'
```
✅ 200 with probability; then **422** with `monthly_charges` named;
`/docs` renders (interactive Swagger).

**Step 7 — Design note** (why each contract choice), pasted into your
evidence file.

## 9. Commands and expected results

| Command | Expected |
|---|---|
| `python train_model.py` | `wrote model.joblib + model_info.json` |
| `python -m pytest test_service.py -v` (before) | **10 skipped** |
| same (after `app.py`) | **10 passed** |
| `curl …/health` | `{"status":"ok","model_loaded":true}` |
| `curl …/predict` (valid) | probability in [0,1], `flag` 0/1, `threshold: 0.5` |
| malformed predict | HTTP **422**, body names the missing field |
| `curl …/docs` | HTTP 200 (Swagger UI) |

## 10. Acceptance criteria (objective)

- [ ] `python -m pytest test_service.py -v` → **10 passed** (not skipped).
- [ ] Live run: health, predict (200), malformed (422 naming a field),
      `/docs` 200 — curl transcript pasted.
- [ ] Model loaded once (describe how you guarantee it — startup load).
- [ ] Determinism: same request twice → identical response (tests assert
      it; you re-verify live).
- [ ] Design note: 422 semantics, threshold echo, empty-batch rule.

## 11. Troubleshooting and recovery

| Symptom | Cause | Fix |
|---|---|---|
| tests still *skip* | no `app.py`, or no FastAPI `app` object in it | file must be named `app.py` in this folder and expose `app` |
| 422 but field not named | default FastAPI validation body | your schema names fields; tests search the serialised detail — keep field names intact |
| 500 instead of 422 | code runs before validation | let pydantic reject; never `payload["x"]` on raw dicts |
| model not found in CI/other cwd | relative path resolved from cwd | resolve paths from `pathlib.Path(__file__)` |
| tests pass, live curl fails | server runs from a different folder | `cd` to `lab-10` before uvicorn |

## 12. Reflection questions

1. Why is a 422 with a named field worth more than a 500 with a stack
   trace — from the *client team's* perspective?
2. Batch size: you accept up to 1000 records (capstone) or 3 (tests)?
   What breaks if you accept 10 million?
3. What exactly must be true before `/predict` may answer 200 on a
   cold start with a missing model? (Compare Module 10's 503 pattern.)

## 13. Optional challenge tasks

1. Add `POST /reload` guarded by an env-var secret (Module 15's rule —
   no literal in source) with a test proving 401 without it.
2. Log predictions to a JSONL file **without** the input fields (privacy
   discipline from Module 14/15) and prove it.
3. Benchmark p95 latency for 100 sequential calls; report the method.

## 14. Rubric / checklist

| Points | Criterion |
|---|---|
| 5 | `10 passed` — full acceptance suite |
| 4 | live transcript: 200 + 422-with-field + `/docs` |
| 3 | model loaded once; determinism re-verified live |
| 2 | design note with the three contract choices justified |
| **14** | **total** · ≥11 = pass |

## 15. Cleanup

```powershell
# stop uvicorn with Ctrl+C, then:
cd examples\labs\lab-10
Remove-Item -Recurse __pycache__, .pytest_cache -ErrorAction SilentlyContinue
# keep app.py + model.joblib: LAB-12 packages them
```

---

**After attempting:** the reference `app.py` (full code block, ready to
copy) lives in
[`examples/labs/solutions/lab-10/README.md`](https://github.com/nadeem-majeedch/MLOps/blob/main/examples/labs/solutions/lab-10/README.md),
together with its green run against the acceptance suite.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../about/index.md).*