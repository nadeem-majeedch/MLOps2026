# Lab 13 — A pipeline that runs itself

## 1. Scenario and business problem

Your retraining pipeline is trusted, but it only runs when someone remembers.
Twice this month the weekly extract arrived, nobody ran anything, and the
model went stale in silence — you found out from the business, not the system.

**Business problem:** make the pipeline run unattended, tell a human when it
fails (and *why*), keep a history of what it did, and avoid wasting compute on
weeks where nothing changed.

## 2. Skills practising

- Operating a scheduled runner: once, interval, with and without new data.
- Reading retry evidence and telling transient from deterministic failure.
- Producing and clearing an alert deliberately.
- Justifying an OS-level scheduler entry (cron / Task Scheduler).
- Choosing between levels of tooling for a stated scenario.

## 3. Prerequisites

- [concepts.md](concepts.md) read (§1–§7).
- Module 08's pipeline green (`python -m pipe.run --once` works).
- Free, local, no accounts (Airflow only if you choose extension 3).

## 4. Required tools and estimated time

| Item | Detail |
|---|---|
| Tools | Python 3.10+, the `orchestrate/` package; any OS scheduler for Step 5 |
| Cost | Free, local, offline |
| ⚠️ Resource-heavy | core path: none. Extension 3 (Airflow): ~1 GB disk — labelled, optional |
| ⏱️ Estimated time | 130 minutes |

## 5. Input data and how to obtain it

```powershell
# 🪟 from examples/churn
python generate_data.py            # ✅ baseline dataset present
python -m orchestrate.flow --once  # ✅ tick 1 succeeds
```

## 6. Directory layout

```
examples/churn/
├── orchestrate/
│   ├── __init__.py
│   └── flow.py        # schedule | retries | history | alerting around pipe stages
├── orch_out/          # generated: runs.jsonl, state.json, ALERT.md
└── pipe/              # the stages (unchanged from Module 08)
```

## 7. Setup and execution steps

**Step 1 — Read the graph and the policy.** Run `--list`; write the retry
policy and where history/alerts live.
✅ **Checkpoint:** `retries: 2 with 1.0s backoff` quoted from your own output.

**Step 2 — The two honest no-ops.**
```powershell
python -m orchestrate.flow --once    # tick: success or skip
python -m orchestrate.flow --once    # tick: "skipped - no new data..."
```
✅ **Checkpoint:** second tick prints the skip line, exit 0, and `runs.jsonl`
contains a `no_new_data` record.

**Step 3 — New data.** Swap in the day-2 extract
(`cp data/raw/churn_day2.csv data/raw/churn.csv` 🪟: `Copy-Item`), run once.
✅ **Checkpoint:** `work needed (new data detected)` and a full success tick.

**Step 4 — Break it and watch the machinery.**
```powershell
Copy-Item data/corrupt/missing.csv data/raw/churn.csv
python -m orchestrate.flow --once; echo "exit=$LASTEXITCODE"
Get-Content orch_out\ALERT.md -TotalCount 14
```
✅ **Checkpoint:** `failed (3 attempt(s))`, exit 1, ALERT names the task and
carries all three attempt strings. Then regenerate the data
(`python generate_data.py`), run again, and confirm **`ALERT.md` no longer exists**.

**Step 5 — Put it on a real schedule (once, safely).**
Write the entry that would run this every day at 02:00:

```powershell
# 🪟 Windows Task Scheduler (run once to prove it fires — then DELETE the task)
schtasks /Create /TN "mlops-pipeline-demo" /SC ONCE /ST 02:00 `
  /TR "powershell -Command cd $PWD; python -m orchestrate.flow --once"
# 🐧 crontab -e, then add:
# 0 2 * * * cd /path/to/examples/churn && python -m orchestrate.flow --once >> orch_out/cron.log 2>&1
```

For the demo, schedule it **one minute from now** instead of 02:00, wait for
the tick, verify a new line in `runs.jsonl`, then `schtasks /Delete /TN
"mlops-pipeline-demo"` (or remove the crontab line).
✅ **Checkpoint:** an OS-initiated tick in the history, and the task removed.

**Step 6 — Interval mode with a cap.** `python -m orchestrate.flow --every 5
--max-runs 3` and record the three tick results (worked example §8 shows the
no-op shape).

**Step 7 — Failure diagnosis.** From Step 4's ALERT attempts alone (without
re-running), answer: transient or deterministic? What evidence? What would
make you change that answer?
✅ **Checkpoint:** three identical strings = deterministic (concepts §3).

**Step 8 — Choose your tools.** For the scenario *"six unrelated pipelines,
three owners, SLA of 04:00, compliance needs run evidence for 12 months"*,
pick level 1/2/3 from concepts §1 and reject one named alternative — three
sentences each.

## 8. Expected outputs and verification

| Step | Expected | Verify |
|---|---|---|
| 2 | skip line + `no_new_data` history record | console + `runs.jsonl` |
| 3 | `new data detected` + success tick | console |
| 4 | 3 attempts, exit 1, ALERT with errors → then alert gone after recovery | ALERT file before/after |
| 5 | OS-created tick visible in history, task removed | `runs.jsonl` + task list |
| 6 | three capped ticks | console |
| 7–8 | written answers | your notes |

## 9. Acceptance criteria

- [ ] All five tick kinds observed: success, `no_new_data`, new-data success,
      failure + alert, recovery + alert cleared.
- [ ] `runs.jsonl` pasted as evidence (at least 4 records).
- [ ] ALERT.md content captured *before* recovery (with attempts).
- [ ] One OS scheduler entry written, executed once, and **removed**.
- [ ] Written tool verdict with a named rejected alternative.
- [ ] Everything filed as `modules/13/`.

## 10. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Ticks always say `no_new_data` after you changed data | A *different* file changed than the one hashed (`data/raw/churn.csv`) | Check which path the lab says to modify |
| ALERT.md never appears | Failure happened in a task before history init, or exception swallowed | Run with `--once` and read the console line; the runner writes ALERT on final failure only |
| ALERT.md persists after a good run | The recovery tick didn't actually succeed, or you're looking at an old file | Confirm a `success` record after the failure record; recovery deletes ALERT at write time |
| Scheduled task fires but no history | Task's working directory is wrong (relative paths) | Set the directory inside the task (`cd` in the command), verify `runs.jsonl` mtime |
| `--every` loop seems stuck | It's sleeping between ticks by design | Use `--max-runs`; Ctrl+C stops it |
| Retries make a bad run 3× slower | Deterministic failure exhausting retries (expected) | Read attempts: identical strings → fix the cause, don't raise retries |

More: [troubleshooting.md](troubleshooting.md).

## 11. Cleanup

```powershell
# 🪟 from examples/churn
schtasks /Delete /TN "mlops-pipeline-demo" /F -ErrorAction SilentlyContinue
python generate_data.py                  # restore the baseline extract
Remove-Item -Recurse orch_out -ErrorAction SilentlyContinue
python -m pipe.run --once && python -m pytest    # ✅ green
```

```bash
# 🐧 remove your crontab line, then as above
```

## 12. Optional extension tasks

1. **Event trigger:** watch the data folder (`watchdog`, or a loop hashing
   every 10 s) and run a tick only on change — compare tick counts against
   `--every 60` for one hour.
2. **Timeouts + jitter:** add a per-task timeout and randomised backoff;
   document what each would have prevented in Step 4.
3. **☁️/⚠️ Airflow probe (heavy):** install Airflow, model these five tasks as
   an Airflow DAG, and note honestly how much of your 200-line runner the
   platform replaced *and* what it added (UI, scheduler semantics, pools).

---

**Next:** [independent-challenge.md](independent-challenge.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*