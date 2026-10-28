# Independent challenge — Module 10

> Do this **without** step-by-step help. Target **75 minutes**.

---

## 1. The scenario

The application team reports two needs you did not design for:
(a) they must pin the API version so a future change cannot break their client,
and (b) their ops dashboard needs a *timing* number it can chart.

## 2. Tasks

1. **Add `POST /v1/predict`.** Same behaviour as `/predict`, reachable only
   under the versioned path, documented separately in `/docs`. State in
   writing which of the two paths you would tell a *new* client to use and why.
2. **Add `GET /v1/metrics`.** Returns, from the running process itself:
   `requests_total`, `records_scored`, `error_422_total`, and
   `model_version` — counters that survive as long as the process lives.
   (In-memory counters are fine; name the limitation.)
3. **Tests first, then implementation** for both additions: at minimum, a 200
   test, a 422 test, and a counter-increment test each. All previous tests
   must stay green (`python -m pytest`).
4. **An error that is *not* 422 and not 503:** make an unknown route return a
   JSON body with `"error": "unknown endpoint"` instead of FastAPI's default
   detail shape — by writing an exception handler, **not** by editing every
   route. Show the curl output for `POST /nope`.
5. **Latency comparison, honestly measured:** p50/max for (a) one record, (b)
   100 records in one call, using the method of your choice. State the method,
   the sample count, and **two** reasons your numbers understate production
   behaviour.

## 3. Deliverables

- Code diff (tasks 1, 2, 4) and test file additions (task 3).
- Full `python -m pytest` output (should be ≥ your previous count, all green).
- `curl` transcripts for: `/v1/predict` success, a 422, and `/nope`.
- `latency.md` (task 5) with method, numbers, caveats.

## 4. Self-check (feedback criteria)

| Grade | Looks like |
|---|---|
| **Excellent (4)** | Both routes tested *before* reuse of existing patterns; counters correct including on 422; `/nope` handled centrally; latency numbers with method + two real caveats; versioning argument references caller stability |
| **Proficient (3)** | Routes + tests working; latency measured; caveats thin |
| **Developing (2)** | Works but tests duplicated/weak, or counters don't count errors |
| **Not yet (1)** | Existing tests broke, or a 500 appears anywhere |

**Design rule to respect:** do not duplicate the scoring logic across the two
routes — one handler calling one function. Duplication here becomes a
divergent bug in production.

---

**Next:** [knowledge-check.md](knowledge-check.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*