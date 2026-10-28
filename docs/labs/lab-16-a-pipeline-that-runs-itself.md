# LAB-16 — A Pipeline That Runs Itself

## 1. Lab identity

| | |
|---|---|
| **Lab ID** | **LAB-16** |
| **Difficulty / topic** | 🚀 Advanced · Scheduling & unattended workflows |
| **Prerequisite module** | [13 — Workflow orchestration and scheduled pipelines](../modules/13-orchestration-scheduled-pipelines/index.md) · LAB-05 recommended |
| **Fixture** | `examples/labs/lab-16/tick_runner.py` |
| **Estimated time** | 105 minutes · free, local, offline · ⚠️ OS scheduling needs Task Scheduler/cron (free) |

## 2. Scenario and background

The model must retrain nightly — unattended. `tick_runner.py` is a
working miniature: every tick runs the same job, retries with backoff,
appends to `runs.jsonl`, raises `ALERT.md` when a tick exhausts its
attempts, and **clears the alert when a later tick succeeds**. You will
run it with an injected failure, read the evidence like an operator,
then wire it to the OS scheduler and design the monitoring that tells a
human what happened — without anyone watching a terminal.

## 3. Learning objectives

By the end you can:

1. Run a scheduled job with retries, history, and alert lifecycle
   (raise → notify → clear).
2. Read a run history: attempts, statuses, recovery — and state the
   system's health from files alone.
3. Schedule with Task Scheduler (🪟) or cron (🐧) and prove the OS ran
   it, not you.
4. Decide honestly when a tick runner is enough and an orchestrator
   (Airflow/Prefect/MLflow Projects) earns its weight.

## 4. Prerequisites and estimated time

- Module 13 read; `python make_data.py` run once (the job reads it).
- **105 min** (observe 25 · schedule 30 · monitoring 25 · trade-off 15 ·
  write-up 10).

## 5. Student task statement

Execute the failure→recovery drill with `--fail-tick`, present the
`runs.jsonl` evidence (failed attempts, alert raised, recovery, alert
cleared), then schedule the runner with the OS (Task Scheduler or cron)
for a short interval, prove **two unattended ticks** with timestamps you
did not trigger, and write the trade-off note: tick runner vs
orchestrator, with the threshold at which you'd switch.

## 6. Required dataset and setup instructions

```powershell
# 🪟 Windows — PowerShell — from examples/labs/lab-16
python make_data.py 2>$null          # if data/ missing (run from ../)
python tick_runner.py --ticks 3 --interval 0.2 --fail-tick 2
```
Real observed (authoring machine):
```text
tick 1: success on attempt 1
tick 2: attempt 1/2/3 failed (injected fault (synthetic outage))
        ALERT raised -> ALERT.md
tick 3: success on attempt 1
        ALERT cleared
history: 2/5 successful attempts in runs.jsonl
alert file: absent (cleared by the recovery tick)
```

## 7. Starter files

| File | Role |
|---|---|
| `tick_runner.py` | working runner: retries, `runs.jsonl`, `ALERT.md` lifecycle |
| `runs.jsonl`, `ALERT.md` | generated evidence |
| `monitoring-note.md` | **you write it** (what a human is alerted, how, when) |

## 8. Numbered implementation steps

**Step 1 — The drill.** Run §6 command; capture full output.
✅ Checkpoint: the four-phase story (ok → failed×3 → alert → recovery →
cleared) in one paste.

**Step 2 — Read the history like an operator.** From `runs.jsonl` alone
(no console): total attempts, failures per tick, recovery time between
alert and clear. ✅ three numbers written.

**Step 3 — Damage variant.** Re-run with `--ticks 2 --fail-tick 2` so
the *last* tick fails: ✅ `ALERT.md` **remains** (no recovery) — read it
and write the exact next action you'd take at 03:00.

**Step 4 — Schedule it (OS level).** 🪟 Task Scheduler: `schtasks`
one-liner or GUI — every 2 minutes, run `python tick_runner.py --ticks 1`;
🐧 cron: `* * * * * cd … && python tick_runner.py --ticks 1`.
✅ proof the OS ran it: `runs.jsonl` gains ticks **at times you did not
trigger** (paste two consecutive entries with timestamps + `schtasks /query /v` or `grep CRON` evidence).

**Step 5 — Monitoring note.** Who gets `ALERT.md`? Design the path:
file → (email/webhook/chat — describe, don't implement paid parts) →
human; include alert fatigue rules (only raise on final failure, clear
on recovery — the runner already models both).
✅ monitoring-note.md with the chain + one escalation rule.

**Step 6 — Trade-off note.** Table: tick runner (this lab) vs
orchestrator (Module 13's tooling): retries, dependencies between tasks,
backfills, UI, multi-machine — and the *threshold* that would make you
switch (e.g. "≥3 dependent tasks or a second machine").
✅ written with a specific trigger, not vibes.

**Step 7 — Unschedule.** Remove the scheduled task (§15) and prove it's
gone (`schtasks /query /tn …` error / crontab empty).

## 9. Commands and expected results

| Command | Expected |
|---|---|
| `python tick_runner.py --ticks 3 --interval 0.2 --fail-tick 2` | 5 attempt records; alert raised then cleared; `2/5 successful` |
| `… --ticks 2 --fail-tick 2` | **ALERT.md persists** (no recovery tick) |
| `python -c "import json;print(len(open('runs.jsonl').readlines()))"` | count grows per run |
| scheduled ticks (OS) | ≥2 entries with timestamps you didn't trigger |
| `python tick_runner.py --ticks 1` (manual) | success; clears any standing alert |

## 10. Acceptance criteria (objective)

- [ ] Failure→recovery drill output pasted (all four phases).
- [ ] Operator reading: attempts / failures / recovery time from the log
      alone.
- [ ] Last-tick-fails variant: standing `ALERT.md` captured with your
      03:00 action.
- [ ] OS-scheduled run proven with **unattended** timestamps + scheduler
      query evidence.
- [ ] Monitoring note: alert chain + escalation rule.
- [ ] Trade-off note with a concrete switch threshold.
- [ ] Task unscheduled and verified gone.

## 11. Troubleshooting and recovery

| Symptom | Cause | Fix |
|---|---|---|
| scheduled tick never appears | task points at wrong python/cwd | use the absolute interpreter path; `cd` inside the task action (the log path is script-relative) |
| `runs.jsonl` unchanged from scheduler | `PYTHONPATH`/venv not active in scheduled context | call the venv's `python.exe` explicitly |
| alert never clears | recovery tick didn't run, or `set_alert(None)` not reached | run a clean tick; check §8 Step 3's opposite case |
| history full of failures after testing | injected-fault runs left standing alert | run one clean `--ticks 1` before submitting |
| cannot delete task | wrong name/path | `schtasks /query` to list, then `/delete /f` |

## 12. Reflection questions

1. The runner retries 3× per tick: what failure does *retry* help, and
   which does it make worse? Give one example of each.
2. `ALERT.md` is a file. What must be true before that file becomes a
   page someone's phone buzzes for — and what would you *not* wake
   someone for?
3. Two machines, two scheduled scripts, one shared dataset: name the
   first thing your tick runner breaks — and the Module 13 tool that
   fixes it.

## 13. Optional challenge tasks

1. Add a `--max-ticks-per-day` budget (cost/rate guardrail).
2. Emit `health.json` (last success age, failure streak) that a monitor
   can poll.
3. Backfill: run missed ticks for a simulated 3-day gap — and discover
   why ordering matters.

## 14. Rubric / checklist

| Points | Criterion |
|---|---|
| 3 | drill evidence, all four phases |
| 2 | operator numbers from logs alone |
| 3 | standing-alert variant + 03:00 action |
| 3 | OS scheduling proven with unattended timestamps |
| 2 | monitoring note (chain + escalation rule) |
| 2 | trade-off note with concrete threshold |
| **15** | **total** · ≥11 = pass |

## 15. Cleanup

```powershell
# 🪟 FIRST unschedule:
schtasks /query /tn "MLOpsLab16" 2>$null
schtasks /delete /tn "MLOpsLab16" /f      # 🐧 crontab -e and remove the line
cd examples\labs\lab-16
Remove-Item runs.jsonl, ALERT.md -ErrorAction SilentlyContinue
Remove-Item -Recurse out -ErrorAction SilentlyContinue
```

---

**After attempting:** a reference monitoring note + trade-off table live
in [`examples/labs/solutions/lab-16/`](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/labs/solutions/lab-16).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../about/index.md).*