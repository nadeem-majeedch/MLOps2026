# Lab 08 — One command to rebuild everything

## 1. Scenario and business problem

Your team's model must be retrained whenever the weekly customer extract
changes. Today that happens because a named person remembers which commands to
run, in which order, on which machine. Last month they forgot the validation
step and shipped a model trained on a file with missing values.

**Business problem:** reproducibility that depends on memory is not
reproducibility. You will replace the shell history with a declared graph that
the machine executes, verifies, and refuses to skip gates on.

## 2. Skills practising

- Reading and modifying a dependency graph (inputs, outputs, order).
- Predicting which stages re-run after a specific change — then checking.
- Diagnosing a recorded failure and resuming correctly.
- Proving a clean rebuild is genuinely self-contained.

## 3. Prerequisites

- [concepts.md](concepts.md) read (§1–§5).
- Modules 05–07 completed; `python -m pytest` green in `examples/churn`.
- Free, local, no accounts.

## 4. Required tools and estimated time

| Item | Detail |
|---|---|
| Tools | Python 3.10+, the `pipe/` package (ships with the repo) |
| Cost | Free, local, offline |
| ⚠️ Resource-heavy | none — every run is under 1 second |
| ⏱️ Estimated time | 130 minutes |

## 5. Input data and how to obtain it

```powershell
# 🪟 from examples/churn
python generate_data.py        # ✅ "rows written: 2000"
python -m pytest               # ✅ green before you start
```

## 6. Directory layout

```
examples/churn/
├── pipe/
│   ├── __init__.py
│   ├── stages.py     # the six stage functions (the work)
│   └── run.py        # graph, hashing, manifest, CLI (the orchestration)
├── config.yaml       # knobs — incl. quality.roc_auc_floor (the gate)
├── data/raw/         # input (generated)
└── pipe_out/         # outputs + manifest.json (generated)
```

## 7. Setup and execution steps

**Step 1 — Read the graph.** `python -m pipe.run --list`. Draw it on paper with
inputs/outputs on each arrow. Name the two stages that are gates.
✅ **Checkpoint:** your drawing matches the CLI output; gates = `validate`, `evaluate`.

**Step 2 — Build and do nothing.** Run twice.

```powershell
python -m pipe.run       # first: six RUN lines
python -m pipe.run       # second: six SKIP lines
```

✅ **Checkpoint:** run 2 exits 0 with all six stages `SKIP`.

**Step 3 — Change one input.** Edit `config.yaml`: `test_size: 0.2` → `0.25`.
Predict which stages re-run *before* running. Then run.
✅ **Checkpoint:** your prediction matches (validate → report all re-run;
only `generate` skips — it does not read config).

**Step 4 — Change only code.** Edit a string inside `report()` in
`pipe/stages.py`, run, then revert the edit and run again.
✅ **Checkpoint:** exactly one stage ran each time (`report`).

**Step 5 — Break the gate, watch it refuse.** Set `roc_auc_floor: 0.99`, run.

```powershell
python -m pipe.run; echo "exit=$LASTEXITCODE"     # 🪟 PowerShell
```

Record: the `FAILED` line, the `BLOCKED` line, `exit=1`, and the `failed`
entry in `pipe_out/manifest.json` (`Get-Content pipe_out\manifest.json`).
✅ **Checkpoint:** `report` did NOT run; manifest error text names the numbers.

**Step 6 — Resume.** Restore the floor to `0.70`, run the *same* command.
✅ **Checkpoint:** exit 0; earlier stages re-ran (config changed), `report` may
skip if its inputs came back identical — note which happened and why.

**Step 7 — Tamper with an artefact.** Append a line to `pipe_out/features.csv`,
run, and observe which stages re-run and which skip (worked example §3 explains
why downstream still skips).

**Step 8 — Prove the clean rebuild.**

```powershell
python -m pipe.run --clean
```

Run it twice; hash `pipe_out/report.md` both times (`Get-FileHash` 🪟 /
`md5sum` 🐧) and confirm the metric section is identical.
✅ **Checkpoint:** two hashes equal — the pipeline needs nothing but its inputs.

**Step 9 — Write the run book**: the three commands a teammate needs, what
each exit code means, and where to look first when it fails.

## 8. Expected outputs and verification

| Step | Expected | Verify |
|---|---|---|
| 2 | `RUN` ×6, then `SKIP` ×6, exit 0 | console + `echo $LASTEXITCODE` |
| 3 | config change re-runs validate→report | run log vs your prediction |
| 4 | exactly `report` runs | run log |
| 5 | `FAILED` + `BLOCKED`, exit 1, manifest `failed` | manifest JSON |
| 6 | exit 0, resume completes | run log + exit code |
| 7 | tampered stage re-runs; downstream may skip | run log |
| 8 | two identical `report.md` hashes | `Get-FileHash` / `md5sum` |

## 9. Acceptance criteria

- [ ] All four observed behaviours above captured in your run book (logs, not memory).
- [ ] Manifest shows a real `failed` entry with its error message.
- [ ] Clean rebuild twice → identical `report.md` metric section.
- [ ] You correctly predicted the stage set for Steps 3 and 4 **before** running.
- [ ] Everything filed as `modules/08/`.

## 10. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Everything re-runs every time | An output written outside `pipe_out/`, or nondeterministic stage | Check declared `outputs` in `run.py`; make the stage deterministic |
| A stage skips when it should not | It reads a file not declared as input | Add it to `TASKS[...]` inputs — undeclared reads break the contract |
| `cycle in the dependency graph` | You wired a stage to its own descendant | Draw the graph; edges must point one way |
| `unknown task` on `--from` | Typo in the stage name | `python -m pipe.run --list` for exact names |
| `ModuleNotFoundError: pipe` | Wrong working directory | Run from `examples/churn` |
| Failure does not resume | You edited files between runs | That is fine — signatures recompute; just rerun |

More: [troubleshooting.md](troubleshooting.md) ·
[course troubleshooting](../../troubleshooting/index.md).

## 11. Cleanup

```powershell
# 🪟 from examples/churn — leaves the repo as you found it
Remove-Item -Recurse pipe_out -ErrorAction SilentlyContinue
python generate_data.py     # if you edited data/
git checkout -- config.yaml pipe/stages.py   # 🐧/🪟 if you keep a Git checkout
python -m pytest            # ✅ must still be green
```

## 12. Optional extension tasks

1. **Branching:** add a `fairness` stage that depends on `evaluate` and writes
   `pipe_out/fairness.json`, and a `report` that also consumes it.
2. **Cost-aware skipping:** time `train` and print estimated savings per week
   of incremental runs.
3. **Parallelism:** run two independent stages concurrently with
   `concurrent.futures` and prove the manifest stays consistent.

---

**Next:** [independent-challenge.md](independent-challenge.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*