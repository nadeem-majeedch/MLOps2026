# LAB-18 — reference solution

> Attempt the lab first. This is the answer key, not the assignment.

## Verified seed evidence (authoring machine, after a fresh re-seed)

```text
$ python runs_ledger.py list
id   state      auc     p95_ms  err%   released
v1   superseded 0.7841  38      0.2    2026-09-28T09:00:00+00:00
v2   current    0.7613  118     2.6    2026-10-22T09:00:00+00:00

serving: v2

$ python runs_ledger.py show v2
{ … "window": {"days_served": 4, "mean_auc": 0.7302, "alerts": 6,
  "note": "PSI 0.31 on monthly_charges; two timeout spikes during
  the evening peak"}, "state": "current" }

$ python runs_ledger.py history
no decisions recorded yet
```

## The numbers, side by side

| | v1 (superseded) | v2 (current) | direction |
|---|---|---|---|
| ROC AUC (offline) | 0.7841 | 0.7613 | worse |
| recall | 0.41 | 0.47 | **better** |
| p95 latency | 38 ms | 118 ms | 3× worse |
| error rate | 0.2 % | 2.6 % | 13× worse |
| live mean AUC (window) | 0.7798 over 21 d, 0 alerts | 0.7302 over 4 d, **6 alerts** | worse |
| drift | PSI 0.04 | PSI 0.31 on `monthly_charges` | worse |
| reliability | stable | two timeout spikes, evening peak | worse |

## The decision — model answer with reasoning

**Roll back v2 → v1, then fix forward.** The reasoning chain, not the
button, is the grade:

1. Live performance fell (0.7798 → 0.7302 mean AUC in the window) —
   that is *measured* degradation, not a hunch.
2. Reliability degraded in production: p95 latency ×3, errors ×13,
   6 alerts, timeout spikes at peak — users feel this now.
3. v1 is **known-good**: 21 days, 0 alerts, PSI 0.04. Rolling back is a
   low-risk move to a demonstrated state.
4. Recall gain (0.47 vs 0.41) is real but does **not** outweigh three
   simultaneous regressions; and a model that times out during peak
   delivers *fewer* predictions, so the recall advantage may not even
   survive contact with traffic.
5. Rollback ≠ giving up: the follow-up ticket is to diagnose the PSI 0.31
   feature shift + latency regression and re-promote v3 with a canary.

```text
$ python runs_ledger.py decide --rollback v2 --reason "mean_auc 0.7798->0.7302, 6 alerts, p95 38->118ms, err 0.2->2.6%; v1 known-good; fix forward"
```

**The defensible minority position** ("ride it out") must state explicit
conditions: hold only if the recall gain is the primary business KPI *and*
you cap the blast radius (canary %, latency SLO, auto-rollback threshold)
*and* you can live with 2.6 % errors until the PSI investigation lands.
A decision without flip-conditions is an opinion.

## Why the reason string matters

`history.jsonl` is the audit trail: `who/what/when/why`. Ten weeks later
nobody remembers your reasoning — the file does. An empty or vague
reason fails the lab's acceptance criteria even if the command worked.

## Cleanup / fresh attempts

```powershell
# 🪟 — the ledger persists by design; reset to the seed state:
Remove-Item ledger.json, history.jsonl -ErrorAction SilentlyContinue
```
```bash
# 🐧
rm -f ledger.json history.jsonl
```
Deleting `ledger.json` re-seeds both releases on the next run (verified).

## Common wrong answers

- Rolling back because "the chart looks worse" without the numbers.
- Choosing ride-out with no thresholds or expiry.
- Deleting `history.jsonl` before submitting — you deleted your evidence.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../../docs/about/index.md).*
