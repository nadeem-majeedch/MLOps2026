# LAB-08 — reference solution

> Attempt the lab first. This is the answer key, not the assignment.

## Step 1 — the inverted behaviour, as shipped (verified)

```text
python quality_gate.py bad_metrics.json
  model: gbdt-v0-attempt   (below the floor on the held-out test split)
    roc_auc 0.6128 <= floor 0.75: OK
  GATE: PASS — artefacts accepted for the next stage     exit=0   ← WRONG

python quality_gate.py good_metrics.json
  model: logreg-baseline   (clears every configured criterion)
    roc_auc 0.8021 > floor 0.75: hmm
  GATE: FAIL — pipeline stops here                        exit=1   ← WRONG
```

A gate that passes failures and fails successes is worse than no gate:
it manufactures confidence.

## Step 2 — criteria consulted vs criteria declared

`gate_config.json` declares **4** criteria (plus a `note`):

| key | consulted by the shipped code? |
|---|---|
| `roc_auc_floor` | ✅ yes — **but with the comparison inverted** |
| `min_recall` | ❌ ignored |
| `max_drift_psi` | ❌ ignored |
| `require_tests_green` | ❌ ignored |

So: **1 of 4 consulted, and the one it consults is backwards.**

## Step 3/4 — the fix (shape of the answer)

```python
def check(metrics: dict, config: dict) -> tuple[bool, list[str]]:
    results = []
    results.append(("roc_auc_floor",
                    metrics["roc_auc"] >= config["roc_auc_floor"],
                    f"roc_auc {metrics['roc_auc']} >= {config['roc_auc_floor']}"))
    results.append(("min_recall",
                    metrics["recall"] >= config["min_recall"], ...))
    results.append(("max_drift_psi",
                    metrics["drift_psi"] <= config["max_drift_psi"], ...))
    results.append(("require_tests_green",
                    metrics["tests_passed"] is True, ...))
    allowed = all(passed for _, passed, _ in results)   # ALL must hold
    return allowed, [f"[{'ok' if p else 'FAIL'}] {n}" for n, p, _ in results]
```

One source of truth for the verdict: `allowed = all(results)`. The
troubleshooting table in the lab calls this out — recomputing the
aggregate from a subset is how the "good candidate still fails" bug
survives review.

## Red tests first (what they must show)

```text
test_bad_candidate_refused     → FAILED before the fix, passed after
test_good_candidate_accepted   → FAILED before the fix, passed after
test_each_config_key_enforced  → four sub-cases (recall, drift, tests, auc)
```

## Step 5 — the proof

```text
good      → exit 0, PASS, every criterion listed
defective → exit 1, FAIL, each violated criterion NAMED
            (recall collapsed, drift strong, tests red, contract broken —
             not just "auc")
```

## Reasoning checkpoints (model answers)

- **Why must a gate name the violated criterion?** An exit code stops
  the pipeline; a *reason* starts the repair. "FAIL" alone converts a
  three-minute fix into a two-hour investigation.
- **ALL vs ANY:** ANY-must-hold inverts the original bug one level up.
  Release criteria are conjunctive by nature — you ship only if every
  condition holds.
- **Why tests before the fix?** The red run *is* the proof the gate
  could fail; without it, "it works now" is an anecdote.

## Common wrong answers

- Fixing only the comparison direction — 3 of 4 criteria still ignored.
- Comparing `>` where the contract says `>=` (boundary model at exactly
  0.75 must pass `roc_auc_floor`).
- Letting the gate print the verdict but exit 0 regardless — a pipeline
  only obeys exit codes.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../../docs/about/index.md).*