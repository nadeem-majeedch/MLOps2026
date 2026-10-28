# LAB-15 — reference solution

> Attempt the lab first. This is the answer key, not the assignment.

**Files in this folder:** `test_release_gate.py` — the starter promised by
lab.md §7. **Verified as shipped: `7 failed, 1 passed`** (authoring
machine) — every criterion-specific assertion is red because the gate
only checks AUC; only the control case passes. After your fix the whole
file must be green.

## Verified as-shipped behaviour (authoring machine)

```text
$ python gate_lab.py candidate_good.json
candidate: good candidate  (every criterion genuinely met — the control case)
  roc_auc 0.802 >= 0.75
VERDICT: PASS — approved for release            (exit 0, correct)

$ python gate_lab.py candidate_defective.json
candidate: defective candidate  (strong on AUC, failing everywhere else …)
  roc_auc 0.841 >= 0.75
VERDICT: PASS — approved for release            (exit 0 — THE BUG)
```

The gate consulted **exactly one** of five criteria. `min_recall`,
`max_drift_psi`, `tests_green_required` and `data_contract_required`
are read from the config file and then never compared.

## The fix, in one idea

Drive every check from the config instead of hand-coding one:

| config key | comparison | direction |
|---|---|---|
| `min_roc_auc` | `candidate["roc_auc"] >= key` | minimum |
| `min_recall` | `candidate["recall"] >= key` | minimum |
| `max_drift_psi` | `candidate["drift_psi"] <= key` | **maximum** |
| `tests_green_required` | `candidate["tests_green"] == key` | equality |
| `data_contract_required` | `candidate["data_contract_ok"] == key` | equality |

Two families: *threshold keys* (`min_*`/`max_*` → inequality, and watch
the direction) and `*_required` keys (→ boolean equality). Collect a
`(criterion, passed, detail)` row per key, verdict = **AND of all rows**,
exit 1 when any row fails and **print every violated criterion**, not
just the first.

## Fail closed (step 4)

Walk the config's keys; any key the gate doesn't recognise → print
`unknown criterion: <key>` and exit **2**. The reasoning: a criterion you
cannot check is indistinguishable from one you checked and passed — and
that is precisely the class of bug you just removed. Exit codes now mean
three different things: 0 ship, 1 refuse, 2 *I don't understand the
rules*.

## Test design (starter explained)

- `run_gate()` shells out to the CLI so **exit codes** are asserted —
  a library-level test would miss a `sys.exit` bug.
- `candidate_with()` starts from the good candidate and breaks **one**
  dimension, so each criterion has its own proof.
- `test_defective_candidate_is_refused` and the fail-closed test are the
  two that fail as shipped.

## Governance paragraph (step 7 — what earns the "advanced" mark)

Model answers: (a) **no one ships over a refusal unilaterally** — an
override requires a second approver (two-person rule); (b) the override
records **who, why, which criterion, and an expiry/review date** — the
same `--ack` pattern `release.py` uses for over-target fairness alerts in
the capstone; (c) loosening a criterion in `release_criteria.json` is a
**reviewed change to policy**, not an edit: it must go through the same
pull-request + approval path as code, because a gate whose rules can be
quietly rewritten provides no guarantee at all.

## Common wrong answers

- `allowed = all(...)` over an empty list when a key is missing —
  vacuous truth: missing criteria would *pass*.
- Checking only `candidate.get(...)` with defaults — same silent-pass
  failure mode.
- Reporting only the first violated criterion — an operator then fixes
  one thing, re-runs, discovers the next; a release gate must show the
  full refusal in one shot.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../../docs/about/index.md).*
