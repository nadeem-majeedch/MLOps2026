# Independent challenge — Module 16

> No step-by-step help. Target **90 minutes**. Deliverable: a one-page
> scaling and cost plan — the artefact a manager actually buys.

---

## 1. The scenario

The support early-alert API has been demoed to the department. Leadership
asks: *"It's been fine on your laptop. What happens at 100 requests per
second? What does that cost?"* You own the answer.

Constraints you must respect:

- **100 requests/second sustained**, p95 latency not worse than 300 ms
  (assume the API currently answers a 2-record batch in ~10 ms locally —
  measured by you, state how);
- no credit-card commitment without a written decision;
- the model is a read-only artefact — the service is **stateless** (verify
  this claim in your plan; say what would break it);
- one person must be able to deploy your plan from the repository.

## 2. Deliverable: `SCALING-PLAN.md`

Required sections (each graded against the rubric below):

1. **Load model** — how 100 rps maps to CPU per request (show the
   arithmetic: rps × ms × cores), hence requests per pod you need.
2. **Topology** — replicas, CPU/memory requests, why *this* HPA shape
   (min/max/trigger) — using the worked formula from
   [worked-example.md §5](worked-example.md#5-cost-arithmetic-real-method-placeholder-price).
3. **Cost estimate** — one *published* price sheet, cited with its date;
   monthly total for steady state **and** at the HPA ceiling; label every
   number "estimate". Include storage and an egress assumption (state it).
4. **Two cost levers** — which two changes halve the number, with the
   before/after arithmetic (right-sizing? scheduled scaling? spot for
   batch retraining? pick and prove).
5. **Reliability** — probes, rollout (`maxUnavailable: 0`), rollback
   command, zone spread (or explicitly: single-zone accepted risk and why).
6. **What you did NOT do** — one paragraph: rejected alternatives
   (serverless? bigger pod? CDN in front of a batch API?) with reasons.
7. **Teardown** — if any part ever touches a cloud: the exact commands,
   written **before** any setup line (rule from concepts §9).

## 3. The bar (self-grade honestly)

| Criterion | Pass looks like |
|---|---|
| Arithmetic | rps→cores→replicas chain shown; no "about 3 pods" without the maths |
| Prices | real published figures with source + date; nothing invented |
| Levers | each lever quantified (halving shown, not asserted) |
| Reliability | `maxUnavailable: 0` rationale + one rollback command that you have actually run somewhere (lab) or explicitly marked *not yet run* |
| Honesty | every unexecuted claim labelled; local lab explicitly not a load test |

## 4. Optional load evidence (if you took Path A)

A real measurement beats every estimate: drive the local port-forward with
a simple load loop (`ab`, `wrk`, or a 10-line Python asyncio client),
report observed throughput and one latency percentile, and say plainly that
**one laptop port-forward is not a production benchmark** — it calibrates
assumptions, nothing more.

## 5. Stretch (+20 min)

Write the **scale-down story**: Black Friday is over (or: term ends, the
students leave). Show the plan returning cost to baseline: what scales in,
on what trigger, with what stabilization window — and the alarm that proves
it happened.

---

[← Lab](lab.md) · [Next: knowledge check →](knowledge-check.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*