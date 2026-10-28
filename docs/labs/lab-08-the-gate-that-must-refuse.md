# LAB-08 — The Gate That Must Refuse

## 1. Lab identity

| | |
|---|---|
| **Lab ID** | **LAB-08** |
| **Difficulty / topic** | 🔧 Intermediate · Quality gates & pipeline automation |
| **Prerequisite module** | [06 — Experiment tracking](../modules/06-experiment-tracking-mlflow/index.md) + [08 — Pipeline automation](../modules/08-pipeline-automation/index.md) |
| **Fixture** | `examples/labs/lab-08/` |
| **Estimated time** | 75 minutes · free, local, offline |

## 2. Scenario and background

Your pipeline has a quality gate: `quality_gate.py` reads
`gate_config.json` (the team's definition of "good enough") and exits
non-zero to stop the build. Except the bad candidate — `roc_auc 0.6128`,
far below the `0.75` floor — just walked through it: `GATE: PASS`, exit
0. Two bugs (one a reversed comparison, one silently ignored criteria)
make the gate decorative. In production this is the difference between
"CI blocked the release" and "the release blocked nothing".

## 3. Learning objectives

By the end you can:

1. Implement a gate as a **contract**: every configured criterion is
   evaluated; any violation → non-zero exit.
2. Write tests for a *refusal* path (the behaviour almost nobody tests).
3. Read a gate failure the way a pipeline does — by exit code, not by
   vibes.
4. Distinguish gate logic from criteria storage (who owns "good enough"?).

## 4. Prerequisites and estimated time

- Module 08 read; LAB-05 recommended (exit-code discipline).
- No dataset needed (metrics files ship with the fixture).
- **75 min** (reproduce 10 · tests 30 · fix 20 · evidence 15).

## 5. Student task statement

Prove the gate is broken, write ≥3 pytest tests that fail as shipped
(refusal of the bad candidate, acceptance of the good one, every
configured criterion enforced), fix `quality_gate.py`, and demonstrate
both exit codes from the command line. Include a pipeline snippet showing
where the gate sits and what stops when it fails.

## 6. Required dataset and setup instructions

```powershell
# 🪟 Windows — PowerShell
cd examples\labs\lab-08
python quality_gate.py good_metrics.json ; echo "exit=$LASTEXITCODE"
python quality_gate.py bad_metrics.json  ; echo "exit=$LASTEXITCODE"
```
🐧: `…; echo "exit=$?"`.

Real observed (the bug):
```text
good  → GATE: FAIL  exit=1     <-- wrong direction
bad   → GATE: PASS  exit=0     <-- wrong direction
```

## 7. Starter files

| File | Role |
|---|---|
| `quality_gate.py` | the buggy gate (2 defects, both commented) |
| `good_metrics.json` / `bad_metrics.json` | the candidates |
| `gate_config.json` | the criteria — note how many keys the code uses |
| `test_gate.py` | **you write it** (starter assertions in solutions) |

## 8. Numbered implementation steps

**Step 1 — Reproduce both verdicts.** Run both candidates; paste exits.
✅ Checkpoint: inverted behaviour captured.

**Step 2 — Count the criteria.** How many keys in `gate_config.json`
does the code actually consult? ✅ write the number and the ignored keys.

**Step 3 — Write red tests.** At minimum:
(a) bad candidate → exit code 1 / `allowed is False`;
(b) good candidate → exit 0;
(c) for **each** config key: a candidate violating it must be refused
(dogfood `bad_metrics.json`'s recall/drift/tests fields).
✅ `python -m pytest test_gate.py -q` → FAILURES pasted.

**Step 4 — Fix the gate.** Correct comparison direction; evaluate every
criterion; aggregate with ALL-must-hold (a list of `(name, passed, detail)`).
✅ re-run tests → green.

**Step 5 — Command-line proof.**
```text
good → exit 0 (PASS) ; bad → exit 1 (FAIL, each violated criterion named)
```
✅ both outputs pasted.

**Step 6 — Place it in a pipeline.** Two lines of shell showing the gate
stage and what a non-zero exit blocks (`pipeline aborts before artefacts
are published` — Module 08 vocabulary).

## 9. Commands and expected results

| Command | Expected after your fix |
|---|---|
| `python quality_gate.py good_metrics.json` | `GATE: PASS`, exit **0** |
| `python quality_gate.py bad_metrics.json` | `GATE: FAIL`, exit **1**, violated criteria listed |
| `python -m pytest test_gate.py -q` | all green (≥3 tests) |
| gate inside a pipeline command chain (`gate && publish`) | publish skipped when gate exits 1 |

## 10. Acceptance criteria (objective)

- [ ] Broken behaviour reproduced with both exit codes (before/after).
- [ ] Ignored config criteria identified by name.
- [ ] ≥3 tests, red transcript then green transcript.
- [ ] Every `gate_config.json` key enforced by logic.
- [ ] Failure output names each violated criterion (machine-usable).
- [ ] Pipeline placement snippet written.

## 11. Troubleshooting and recovery

| Symptom | Cause | Fix |
|---|---|---|
| tests can't see exit codes | calling the script instead of importing `check()` | test the pure function `check()` *and* one subprocess run |
| good candidate still fails | you inverted once but forgot the aggregate `allowed` | compute verdict from the collected per-criterion results only — one source of truth |
| criterion keys renamed | gate reads different keys than config writes | load keys dynamically; fail loudly when a configured key is unknown |
| `echo exit=$LASTEXITCODE` shows 0 always | PowerShell pipeline swallowed it | run the python call as its own statement first |

## 12. Reflection questions

1. Why should the gate *list* every violated criterion instead of just
   failing? Answer from the operator's point of view at 2 a.m.
2. Who should own `gate_config.json` — the data scientist who trains, or
   the team? What changes when the answer is "the team"?
3. A gate that fails on a *flaky* metric causes "gate fatigue". Name one
   criterion that belongs in a gate and one that belongs in a report.

## 13. Optional challenge tasks

1. Add `--strict-config`: exit 2 if config contains keys the gate does
   not understand (closing the silent-ignore class forever).
2. Emit `gate_report.json` alongside console output for CI artefacts.
3. Seed a regression: change the gate back to `<=` in a copy and watch
   your tests catch it (paste the red).

## 14. Rubric / checklist

| Points | Criterion |
|---|---|
| 2 | both broken exits demonstrated (before) |
| 3 | ≥3 tests with red→green transcripts |
| 4 | all config criteria enforced; ignored keys named |
| 3 | failure output lists violated criteria |
| 2 | pipeline placement snippet |
| **14** | **total** · ≥11 = pass |

## 15. Cleanup

```powershell
cd examples\labs\lab-08
Remove-Item gate_report.json -ErrorAction SilentlyContinue
Remove-Item -Recurse __pycache__, .pytest_cache -ErrorAction SilentlyContinue
```

---

**After attempting:** a reference fixed gate + tests live in
[`examples/labs/solutions/lab-08/`](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/labs/solutions/lab-08).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../about/index.md).*