# Troubleshooting — Module 13

Symptom → likely cause → fix. See the
[course troubleshooting hub](../../troubleshooting/index.md) for Python issues.

---

## 1. Scheduler behaviour

| Symptom | Likely cause | Fix |
|---|---|---|
| Ticks always `no_new_data` even though "something changed" | The hash covers `data/raw/churn.csv` only | Change that file (or the path your state records) — `state.json` shows which hash is stored |
| `--every` runs all ticks instantly | Sleep happens **between** ticks, and skip-ticks are fast | Expected; look at the timestamp spacing in `runs.jsonl` |
| OS task fires, no new history | Task's working directory differs (relative paths) | Set working directory in the task; verify by `Get-Item orch_out\runs.jsonl` mtime / `ls -l` |
| Two schedulers running at once | A leftover `--every` loop **plus** Task Scheduler | Run `Get-Process python` / `ps aux | grep orchestrate`; kill the duplicate — double runs are the classic source of racing writes |
| Ctrl+C doesn't stop it | Signal handling in a long `time.sleep` | Wait for the current sleep to end, or close the terminal; note it as a design limitation if it persists |

## 2. Retries and failures

| Symptom | Likely cause | Fix |
|---|---|---|
| Every failure takes 3 attempts | Deterministic error exhausting `--retries 2` | Read the attempts: **identical strings** = fix the cause (concepts §3); do not raise retries |
| A transient failure didn't succeed on retry | Backoff too short for the resource (port still held, lock still held) | Increase `--backoff`, or fix the release side; transient errors are often *time*-bound |
| Failure produces no `ALERT.md` | The run was skipped (`no_new_data`), or the process died hard (killed, power loss) | Only final task failures write alerts; hard kills leave the last `runs.jsonl` line unfinished — check for a truncated line |
| `runs.jsonl` has a truncated/garbled last line | Process killed mid-write | Harmless for reading (JSON-per-line): ignore the partial tail; append-only design tolerates it |

## 3. Alerts

| Symptom | Likely cause | Fix |
|---|---|---|
| Alert reappears immediately after you delete it | A new tick is still failing | Check the latest `runs.jsonl` record — deletion without fixing just re-creates it (correct behaviour) |
| Alert persists after a good run | The good run didn't reach `success` (an earlier task failed), or you're reading a stale copy | Recovery deletes ALERT **only on a successful tick**; confirm a `success` record exists after the failure |
| Alert never clears even though runs pass | You're looking at a different folder (task ran elsewhere) | Verify the task's working directory — same root cause as §1's "no new history" |

## 4. History questions

- **"When did we last retrain?"** — last record with `status: success` that
  actually ran tasks (not `no_new_data`), read its `at`.
- **"Are runs getting slower?"** — compare `duration_s` across records;
  rising time with the same data hash usually means machine load or a
  growing output folder, not the pipeline.
- **"Has this failed before?"** — grep `status.*failed` and read the attempt
  strings; recurrence changes the diagnosis from incident to chronic.

## 5. Choosing tools mid-incident

If you are fighting the runner itself (races, missed schedules, no visibility)
several times a week, that is the signal from concepts §7 — you have outgrown
level 2. Do **not** start by installing Airflow on the problem machine: first
write down which of {UI, multi-DAG, pools, SLAs, multi-user} you actually
need; the answer decides between level 3 platforms and a hosted option.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*