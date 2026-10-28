# Lab 10 — Serve a trained model to an application

## 1. Scenario and business problem

The analytics team has a model and a registry; the application team needs to
*call* it from their CRM screen. They will send batches of customer records
and need predictable errors they can render to their users.

**Business problem:** an unversioned, unvalidated script that loads a pickle
per request cannot be called an API. You will stand up a tested, documented
endpoint whose failures are as informative as its successes.

## 2. Skills practising

- Starting/stopping a real server and probing it with HTTP tools.
- Reading status codes and error bodies as a *caller* would.
- Running and extending an API test suite.
- Measuring latency with a method you can defend.

## 3. Prerequisites

- [concepts.md](concepts.md) read (§1–§7).
- Module 09 completed (recommended: a `production` pointer to serve), or the
  training artefact as fallback.
- `python -m pytest` green.

## 4. Required tools and estimated time

| Item | Detail |
|---|---|
| Tools | Python 3.10+, `fastapi`, `uvicorn`, `httpx` (already used by the suite), curl or PowerShell |
| Cost | Free, local, no accounts, no deployment |
| ⚠️ Resource-heavy | none — one CPU, <200 MB |
| ⏱️ Estimated time | 140 minutes |

## 5. Input data and how to obtain it

```powershell
# 🪟 from examples/churn
python -m pipe.run          # ✅ model exists (pipe_out/model.joblib)
python -m registry list     # optional but recommended: a production version
python -m pytest tests/test_service.py    # ✅ 8 passed
```

## 6. Directory layout

```
examples/churn/
├── service/
│   ├── app.py          # endpoints, error handling, startup model load
│   ├── schemas.py      # the contract (pydantic)
│   ├── model.py        # registry pointer → artefact → none
│   └── __main__.py     # python -m service (HOST/PORT env vars)
└── tests/test_service.py
```

## 7. Setup and execution steps

**Step 1 — Read the contract before the code.** From `schemas.py`, write down:
allowed `contract_type` values, `tenure_months` range, and max batch size.
✅ **Checkpoint:** you can predict a 422 without sending it (tested in Step 4).

**Step 2 — Start and verify.**
```powershell
python -m service            # terminal 1
```
```powershell
curl -s http://127.0.0.1:8000/health          # 🪟: Invoke-RestMethod ...
```
✅ **Checkpoint:** `status` and a `model_version` you recognise.

**Step 3 — Score a real batch.** Send two records (worked example §3); confirm
one probability per record, `0.0 ≤ p ≤ 1.0`.

**Step 4 — Break it on purpose.** Send each of these and record status + body:
(a) `"contract_type":"lifetime"` · (b) `tenure_months: 0` ·
(c) `records: []` · (d) a record missing `monthly_charges`.
✅ **Checkpoint:** all four are 422 with the field named; none produced a 500.

**Step 5 — Read your own documentation.** Open `/docs` in a browser, run a
request from the UI, and confirm it matches curl's answer. Also fetch
`/model-info` and check the metrics against `pipe_out/train_metrics.json`.
✅ **Checkpoint:** docs and reality agree.

**Step 6 — The no-model case.** Stop the server; move `pipe_out`,
`artifacts`, and `registry_store` aside; restart; probe `/health` and
`/predict`. **Restore everything and restart.**
✅ **Checkpoint:** `degraded` health, 503 with instructions, no crash traceback.

**Step 7 — Measure honestly.** Time 50 sequential `POST /predict` calls and
record method + numbers:

```powershell
# 🪟 simple loop (PowerShell)
1..50 | ForEach-Object { (Measure-Command {
  Invoke-RestMethod -Uri http://127.0.0.1:8000/predict -Method Post `
    -ContentType 'application/json' -Body '{"records":[{"tenure_months":24,"monthly_charges":70.0,"support_tickets":2,"contract_type":"monthly"}]}'
}).TotalMilliseconds } | Sort-Object
```
Report **p50** (the 25th value of 50 sorted) and **max**, plus one caveat
("sequential, local, single record — not a load test").

**Step 8 — Run the suite with the server stopped** (tests must not need a
running server) and record the 8-test result.

**Step 9 — Write the caller's guide**: endpoint, method, one example payload,
status codes you observed (200/422/503), and what the app team should show
users for each.

## 8. Expected outputs and verification

| Step | Expected | Verify |
|---|---|---|
| 2 | `{"status":"ok","model_version":"..."}` | curl output |
| 3 | N predictions for N records | count matches input |
| 4 | 4 × 422, field named, **no 500** | status codes + bodies |
| 5 | `/docs` 200; metrics identical to `train_metrics.json` | side-by-side |
| 6 | `degraded` + 503 with `detail` steps | curl output |
| 7 | your own p50/max + caveat | your measurement note |
| 8 | `8 passed` with server stopped | pytest output |

## 9. Acceptance criteria

- [ ] Live transcript: health, valid batch, **four** invalid requests, all status codes recorded.
- [ ] No 500 at any point (a 500 means an unhandled path — fix, don't excuse).
- [ ] `/docs` checked against an actual curl response.
- [ ] Suite green with the server stopped.
- [ ] Latency note includes method, p50, max, and a caveat.
- [ ] Caller's guide filed as `modules/10/`.

## 10. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `Address already in use` | An older server still running | Find it: `Get-NetTCPConnection -LocalPort 8000` 🪟 / `lsof -i :8000` 🐧; stop that PID, or `PORT=8001 python -m service` |
| 422 on a request that "looks fine" | Type mismatch (`"70"` vs `70`), or a typo'd field name | Read the `detail` line — it names the field |
| 503 `no model loaded` | Registry/artefacts missing | `python -m pipe.run` (and promote a version), restart |
| Predictions differ from Module 06 metrics | You are scoring different data (a request, not the test set) | Expected: `/model-info` metrics are training-time, not per-request |
| Connection refused from another machine | Server binds `127.0.0.1` | By design (local lab). Module 11 changes `HOST` for containers |
| Tests hang | A test client trying to reach a live server | Tests use ASGI `TestClient` — they need **no** server; check you didn't add a network call |

More: [troubleshooting.md](troubleshooting.md).

## 11. Cleanup

```powershell
# terminal 1: Ctrl+C to stop the server
# 🪟 from examples/churn — if you moved folders aside in Step 6:
Move-Item pipe_out.moved pipe_out -ErrorAction SilentlyContinue
python -m pipe.run && python -m pytest   # ✅ 34 passed
Remove-Item service.log, bad.json -ErrorAction SilentlyContinue
```

## 12. Optional extension tasks

1. **Batching experiment:** compare 10 calls of 1 record vs 1 call of 10
   records; report measured totals and explain the round-trip overhead.
2. **Versioned path:** add `POST /v1/predict` that behaves identically and
   document why URL versioning matters to callers.
3. **Input limits under stress:** send 1001 records and confirm the 422 — then
   argue whether `max_length` should be 1000 or configurable.

---

**Next:** [independent-challenge.md](independent-challenge.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*