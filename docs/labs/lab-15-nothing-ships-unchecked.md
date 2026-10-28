# LAB-15 — Nothing Ships Unchecked

## 1. Lab identity

| | |
|---|---|
| **Lab ID** | **LAB-15** |
| **Difficulty / topic** | 🚀 Advanced · Release validation & governance |
| **Prerequisite module** | [09 — Artifacts, registries, promotion](../modules/09-model-artifacts-registry/index.md) + [15 — Security/privacy/governance](../modules/15-security-privacy-governance/index.md) · **LAB-08 first** |
| **Fixture** | `examples/labs/lab-15/` |
| **Estimated time** | 90 minutes · free, local, offline |

## 2. Scenario and background

The release criteria for the subscription-risk model are written down in
`release_criteria.json`: AUC floor, minimum recall, drift ceiling, tests
green, data contract intact. `gate_lab.py` is supposed to enforce them —
ALL of them. Today the **defective candidate** (AUC 0.841, recall 0.11,
PSI 0.47, red tests, broken contract) sails through with `VERDICT: PASS`.
LAB-08 taught you the single-metric gate; this lab is the full contract:
a release validator that fails closed on **every** criterion and proves
it with a regression test.

## 3. Learning objectives

By the end you can:

1. Implement multi-criteria validation where **all** criteria must hold,
   driven entirely by a config file (no criteria hard-coded).
2. Handle booleans, thresholds, and "unknown criteria" safely —
   fail closed when the config says something you don't understand.
3. Prove both directions: a genuinely-good candidate passes, a
   defective one is refused, with exit codes.
4. Explain the governance layer: who may override, and how an override
   is recorded (the `--ack` pattern from Module 09/15).

## 4. Prerequisites and estimated time

- LAB-08 completed (you know the failure modes); Module 15 §6 read.
- No dataset: candidates ship as JSON.
- **90 min** (reproduce 10 · implement 40 · tests 20 · governance note 20).

## 5. Student task statement

Fix `gate_lab.py` so every key in `release_criteria.json` is enforced:
`min_roc_auc`, `min_recall`, `max_drift_psi`, `tests_green_required`,
`data_contract_required` — plus **fail closed** on unknown criterion keys.
Deliver: both verdicts from the CLI with exit codes, `test_release_gate.py`
(≥5 tests: one per criterion + the unknown-key refusal), and a
governance note describing who could override a refusal and what must be
written down when they do.

## 6. Required dataset and setup instructions

```powershell
# 🪟 Windows — PowerShell — from examples/labs/lab-15
python gate_lab.py candidate_good.json      ; echo "exit=$LASTEXITCODE"
python gate_lab.py candidate_defective.json ; echo "exit=$LASTEXITCODE"
```
Real observed **as shipped** (the fault):
```text
good      → VERDICT: PASS  exit=0   (correct)
defective → VERDICT: PASS  exit=0   (WRONG — only AUC was consulted)
```

## 7. Starter files

| File | Role |
|---|---|
| `gate_lab.py` | one criterion implemented; the rest named but ignored |
| `release_criteria.json` | the contract (5 keys) |
| `candidate_good.json` / `candidate_defective.json` | control + fault |
| `test_release_gate.py` | **you write it** (starter in solutions) |

## 8. Numbered implementation steps

**Step 1 — Reproduce both verdicts** (§6). ✅ paste: defective passes.

**Step 2 — List the ignored keys.** Compare config keys to code paths.
✅ you can name each unenforced criterion with its required comparison
direction (min vs max!).

**Step 3 — Implement all criteria generically.** Drive checks from the
config: threshold keys → comparisons, `*_required` keys → equality with
the candidate's boolean. Collect `(criterion, passed, detail)` rows;
verdict = AND of all.
✅ defective now names *every* violated criterion and exits 1.

**Step 4 — Fail closed on unknowns.** If the config contains a key the
gate doesn't know → refuse with exit **2** and name the key (a criterion
you can't check must never be silently skipped — that is exactly the
class of bug you just fixed).

**Step 5 — Tests (≥5).** good → pass; defective → refused; each
individual criterion violated in isolation → refused (build tiny
candidate dicts); unknown config key → exit 2.
✅ `python -m pytest test_release_gate.py -q` green.

**Step 6 — CLI proof both ways**, exit codes captured.

**Step 7 — Governance note (the paragraph that makes this "advanced").**
Answer: (a) who may ship over a refusal, if anyone; (b) what the
override must record (who, why, expiry/review date — the `--ack` pattern
from `release.py`); (c) why a *config* change to loosen a criterion is a
reviewable event, not an edit. Reference the capstone's over-target
fairness `--ack` as a real worked precedent.

## 9. Commands and expected results

| Command | As shipped | After your fix |
|---|---|---|
| `python gate_lab.py candidate_good.json` | PASS, exit 0 | PASS, exit 0 |
| `python gate_lab.py candidate_defective.json` | PASS, exit 0 (**fault**) | **REFUSED, exit 1**, all violated criteria listed |
| config with an unknown key | ignored silently | exit **2**, key named |
| `python -m pytest test_release_gate.py -q` | (none yet) | ≥5 passed |

## 10. Acceptance criteria (objective)

- [ ] Before-fault captured (defective → PASS, exit 0).
- [ ] All five criteria enforced, driven by config (point at the code).
- [ ] Defective refused with each violated criterion named; exit 1.
- [ ] Unknown-criterion → exit 2 (fail closed) demonstrated.
- [ ] ≥5 tests, green, including isolated single-criterion failures.
- [ ] Governance note: override authority + record + config-change
      review, with the `--ack` precedent referenced.

## 11. Troubleshooting and recovery

| Symptom | Cause | Fix |
|---|---|---|
| good candidate now fails | comparison direction swapped for a max-criterion (`max_drift_psi` must use `<=`) | write each criterion's direction in a comment before coding |
| defective still passes | a `*_required` key never compared, or verdict computed from partial results | verdict = AND over *all* collected rows only |
| tests can't assert exit codes | calling the CLI only | test the pure `evaluate()` **and** one subprocess run |
| config key typo = silent pass | unknown keys not detected | inverse check: every config key must be claimed by a check (Step 4) |
| exit code lost in PowerShell | piped output | run the python call as its own statement |

## 12. Reflection questions

1. The defective candidate is *good on AUC*. What organisational habit
   makes single-metric wins ship — and which document counters it?
2. Fail-closed on unknown config keys: what breaks the day a colleague
   adds a valid criterion? How should they discover it (and why is that
   the right failure mode)?
3. If a human can always override, why bother with the gate at all?
   Answer with the words *audit trail* and *friction*.

## 13. Optional challenge tasks

1. Add `--ack "<reason>"` to the CLI: a refusal becomes shippable only
   with a reason ≥20 chars, recorded to `ack_log.jsonl` (the capstone
   pattern, now yours).
2. Emit `gate_report.json` for CI artefacts.
3. Make the gate read criteria from *two* files (model + deployment) and
   demonstrate precedence rules you define.

## 14. Rubric / checklist

| Points | Criterion |
|---|---|
| 2 | fault reproduced (before) |
| 5 | all five criteria enforced from config; direction correct |
| 3 | defective refused with per-criterion output, exit 1 |
| 2 | unknown criterion fails closed, exit 2 |
| 2 | ≥5 tests green |
| 2 | governance note substantive (`--ack` precedent) |
| **16** | **total** · ≥12 = pass |

## 15. Cleanup

```powershell
cd examples\labs\lab-15
Remove-Item gate_report.json, ack_log.jsonl -ErrorAction SilentlyContinue
Remove-Item -Recurse __pycache__, .pytest_cache -ErrorAction SilentlyContinue
```

---

**After attempting:** a reference complete gate + tests live in
[`examples/labs/solutions/lab-15/`](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/labs/solutions/lab-15).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../about/index.md).*