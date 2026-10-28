# LAB-20 — Incident Day: Detect, Contain, Recover

## 1. Lab identity

| | |
|---|---|
| **Lab ID** | **LAB-20** |
| **Difficulty / topic** | 🚀 Advanced · Full-lifecycle incident exercise (integration) |
| **Prerequisite module** | [17 — Capstone](../modules/17-capstone/index.md) · Labs 01–19 are its ingredients |
| **Fixture** | `examples/labs/lab-20/inject_fault.py` + `examples/capstone-support/` |
| **Estimated time** | 150 minutes · free, local, offline · no accounts |

## 2. Scenario and background

It is 03:40. Two things went wrong in the capstone system while nobody
was watching: the nightly extract landed **truncated with a renamed
column**, and the model artefact on disk is the residue of an
**interrupted copy**. The system must notice *both* — using only its own
tooling (data contract, tests, integrity records, service health) — and
you must restore it, prove the recovery, and write the timeline.

This is the integration lab: every guard you built in Labs 03, 08, 10,
15 and 18 either fires here or is honestly shown missing.

**Business problem:** the difference between a *system* and a *script*
is what happens at 03:40 when no developer is present.

## 3. Learning objectives

By the end you can:

1. Detect a corrupted dataset through the data contract — and explain
   why a pure row-loss (no schema change) slips through every current
   check.
2. Detect a corrupted model artefact through direct loading and a
   recorded `sha256`, and explain why the test suite **cannot** catch it
   (it retrains and silently heals the file).
3. State which layer protects serving during an artefact incident
   (the promoted release copy, not `artifacts/`).
4. Recover with an auditable trail: fault → detection → restore →
   re-verification, and prove recovery by re-running the *same* checks.
5. Write an incident timeline with detection gap, blast radius, and at
   least one follow-up action.

## 4. Prerequisites and estimated time

- Capstone green before you start:
  `python pipeline.py` completes and `python -m pytest -q` → 30 passed.
- Labs 03, 08, 10, 15, 18 read (or at least their verification sections).
- **150 min** (baseline 15 · data incident 35 · model incident 40 ·
  recovery proof 20 · timeline 25 · reflection 15).

## 5. Student task statement

Run the two faults **one at a time**. For each: detect it with the
system's own tooling (record the exact command and output), judge the
blast radius (what is affected, what is still serving), restore it, and
**prove recovery by re-running the detection command**. Then write
`incident-timeline.md`: what broke, how long it could have gone
unnoticed, how you knew, what you did, what you would add.

## 6. Required dataset and setup instructions

The capstone project ships with the injector; no downloads.

```powershell
# 🪟 Windows — PowerShell
cd examples\capstone-support
python pipeline.py          # ✅ must complete: "pipeline complete - see report.md"
python -m pytest -q         # ✅ 30 passed
cd ..\labs\lab-20
python inject_fault.py --list
```

```bash
# 🐧 Linux/macOS
cd examples/capstone-support
python pipeline.py && python -m pytest -q    # ✅ green baseline
cd ../labs/lab-20 && python inject_fault.py --list
```

✅ **Checkpoint:** `--list` shows `data` and `model` both `present`, and
no `injected_state.json` exists (a previous attempt left nothing behind).

## 7. Starter files

| File | Role |
|---|---|
| `inject_fault.py` | `--fault {data,model}` / `--restore` / `--list`; timestamped backups in `backup/` |
| `../../capstone-support/src/validate.py` | the data contract (detection for fault 1) |
| `../../capstone-support/release.json` | recorded `data_sha256` / `model_sha256` (detection for fault 2) |
| `../../capstone-support/service/app.py` | serving path (promoted release first) |
| `incident-timeline.md` | **you write it** |

**What each fault actually does** (verified during authoring — read the
source, don't trust the label):

- `data` — truncates `data/support.csv` to 60% of rows **and** renames
  `attendance_rate` → `attendance_rate_v2`.
- `model` — truncates `artifacts/model.joblib` to 70% of its bytes (an
  interrupted copy). Size changes; the file no longer unpickles.

## 8. Numbered implementation steps

**Incident 1 — the extract**

**Step 1 — Inject.** `python inject_fault.py --fault data`
✅ Checkpoint: backup recorded in `backup/`, `injected_state.json` created.

**Step 2 — Detect with the contract.**
```powershell
cd ..\..\capstone-support
python -m src.validate      # ✅ exit 1: FAIL required_columns, FAIL configured_columns_exist (6/8)
```
✅ **Checkpoint:** the *named* failures mention `attendance_rate`
explicitly — a clean contract violation, not a crash.

**Step 3 — See the pipeline refuse.**
```powershell
python pipeline.py
```
✅ **Checkpoint:** `[2/5] validate RUN ... FAILED: data contract violated:
required_columns, configured_columns_exist` and stages 3–5 `BLOCKED`.

**Step 4 — Blast radius.** Write two lines: is the serving model
affected? Is the trained artefact affected? (Check `release.json` — the
recorded `data_sha256` still matches the *old* extract; nothing retrained.)

**Step 5 — Recover and prove it.**
```powershell
cd ..\labs\lab-20
python inject_fault.py --restore
cd ..\..\capstone-support
python -m src.validate      # ✅ 8/8 checks passed, exit 0
```
✅ **Checkpoint:** the *same* command that failed now passes — that is
what "recovery proven" means.

**Incident 2 — the artefact**

**Step 6 — Inject.**
```powershell
cd ..\labs\lab-20
python inject_fault.py --fault model
```
✅ Checkpoint: output says `truncated 3361 -> 2352 bytes` (your sizes may
differ if you retrained; record your own).

**Step 7 — Detect: direct load.**
```powershell
python -c "import joblib; joblib.load('artifacts/model.joblib')"
```
✅ **Checkpoint:** raises `EOFError` — refuse to serve what you cannot read.

**Step 8 — Detect: integrity record.**
```powershell
python -c "import hashlib,json,pathlib; p=pathlib.Path('artifacts/model.joblib'); print(hashlib.sha256(p.read_bytes()).hexdigest()[:16], json.loads(pathlib.Path('release.json').read_text())['releases']['r001']['model_sha256'])"
```
✅ **Checkpoint:** two different hashes → `MISMATCH` against the value
recorded at registration.

**Step 9 — The blind spot.** Now run `python -m pytest -q`.
✅ **Checkpoint — this one is deliberately surprising:** the suite
**passes (30)** — and if you re-check the hash afterwards it is *back to
the recorded value*. Explain in one paragraph: the `trained` fixture
retrains and rewrites `artifacts/model.joblib`, so the tests exercised a
freshly trained model, not your corrupted file. Unit tests retrain;
they are not artefact-integrity checks.

**Step 10 — Serving judgement.** `python -c "from service.app import
resolve_model; s=resolve_model(); print(s['version'], s['source'])"`
✅ **Checkpoint:** `r001 releases/r001/model.joblib` — serving reads the
**promoted copy**, so the blast radius of this incident is
"training artefact on disk", not "users being served garbage". Write
that distinction down; it decides the severity.

**Step 11 — Recover and prove it.**
```powershell
cd ..\labs\lab-20
python inject_fault.py --restore
cd ..\..\capstone-support
python -c "import joblib; joblib.load('artifacts/model.joblib'); print('loads ok')"   # ✅ loads ok
python -m pytest -q        # ✅ 30 passed
python pipeline.py         # ✅ pipeline complete
```

**Step 12 — Timeline.** Write `incident-timeline.md`: for each incident —
detection command + output, detection gap (could it have gone unnoticed?
for the data fault answer the row-loss question honestly), blast
radius, restore command, proof command, and one follow-up action
(e.g. "add a min-row check", "verify `model_sha256` at service load").

## 9. Commands and expected results

| Command | Expected (authoring machine, Python 3.14) |
|---|---|
| `python -m src.validate` (after `--fault data`) | `FAIL required_columns … missing: ['attendance_rate']`, `6/8 checks passed`, exit 1 |
| `python pipeline.py` (after `--fault data`) | `[2/5] validate … FAILED`, stages 3–5 `BLOCKED` |
| `python -c "import joblib; joblib.load('artifacts/model.joblib')"` (after `--fault model`) | raises `EOFError` |
| hash-vs-`release.json` comparison | recorded ≠ actual → `MISMATCH` |
| `python -m pytest -q` (after `--fault model`) | **30 passed** — and the artefact is retrained in the process (the lesson) |
| `resolve_model()` output | `r001 releases/r001/model.joblib` — serving unaffected |
| after `--restore` | `8/8 checks passed`, `loads ok`, `30 passed`, `pipeline complete` |

*(Real outputs from the lab authoring machine. Re-run them yourself;
never tick a box on my transcript.)*

## 10. Acceptance criteria (objective)

- [ ] Baseline captured first (pipeline complete + 30 passed).
- [ ] Data fault detected by `src.validate` — named failures, exit 1 —
      and blocked by `pipeline.py` at stage 2.
- [ ] Data recovery proven by the *same* command turning green (8/8).
- [ ] Model fault detected two ways: `EOFError` on load **and**
      hash mismatch against `release.json`.
- [ ] The pytest blind spot explained in writing (retraining heals the file).
- [ ] Serving-vs-artefact blast radius stated, evidenced by `resolve_model()`.
- [ ] `incident-timeline.md` complete for both incidents, with one
      follow-up action each.
- [ ] Repository left clean: no `injected_state.json`, all checks green.

## 11. Troubleshooting and recovery

| Symptom | Cause | Fix |
|---|---|---|
| `nothing recorded as injected` on `--restore` | you already restored, or state file deleted | `python inject_fault.py --list`; worst case: `git status` and restore the two files from Git |
| data fault "passes" all checks | you expected row loss alone to fail | by design it doesn't — no min-row check exists; that is reflection Q1, not a bug |
| `missing target: …` | capstone data/artefacts absent | `cd examples/capstone-support && python generate_data.py && python pipeline.py` |
| hash comparison shows `match` after pytest | pytest retrained and healed the artefact | do the check **before** pytest (Step 8), or delete `injected_state.json` knowledge and re-inject |
| `resolve_model()` raises EOFError | you corrupted `releases/…` by hand, or `release.json` points at the artefact | `python release.py status`; restore from `backup/` |
| pipeline retrains during recovery | expected — `train` is a pipeline stage | confirm with `python release.py status` that the serving pointer never moved |
| backup/ has many files | every injection keeps a timestamped copy | safe to delete after you submit (cleanup §15) |

## 12. Reflection questions

1. **Detection gap:** a pure truncation (same schema, fewer rows) passed
   8/8 checks in authoring. What single check would catch it, and what
   false alarms would it create?
2. Why should an integrity check live at *load* time rather than only at
   *registration* time? Name the attack or accident that only the former
   catches.
3. The test suite passed while the artefact was broken. Rewrite the
   suite's contract in one sentence so this can't recur (what should
   `test_model.py` promise instead of "training works"?).
4. Estimate the detection gap for each incident in this lab: how long
   could it run unnoticed in a system that only checks dashboards?
5. Which single guard from Labs 01–19 earned its keep today, and which
   one would you add?

## 13. Optional challenge tasks

1. **Close gap 1:** add a `min_rows` check to `src/validate.py` with a
   justified threshold, then prove a pure truncation is now caught
   (inject, manually drop rows, run the contract).
2. **Close gap 2:** verify `release.json`'s `model_sha256` inside
   `resolve_model()` before `joblib.load`, plus a test using a corrupted
   temp copy (never the real artefact).
3. **Escalate:** copy `releases/r001/model.joblib` aside, truncate it,
   and watch the service *fail to boot* — then restore. Compare this
   blast radius with Incident 2's and write the one-line rule that
   tells an on-call engineer which happened.
4. **Rehearse the rollback:** combine with LAB-18 — decide, execute,
   and record the recovery as a single timeline.

## 14. Rubric / checklist

| Points | Criterion |
|---|---|
| 2 | green baseline captured before injecting |
| 4 | data incident: named contract failure + pipeline block + proven recovery |
| 4 | model incident: two independent detections (load + hash) |
| 4 | pytest blind spot explained correctly (retraining heals) |
| 3 | blast radius: serving (release copy) vs artefact, evidenced |
| 3 | timeline complete, both incidents, follow-up actions |
| 2 | repo clean at the end (no injected state, checks green) |
| **22** | **total** · ≥17 = pass |

## 15. Cleanup

```powershell
# 🪟 — confirm zero injected state, then drop the backups
cd examples\labs\lab-20
python inject_fault.py --list                 # both targets present, no state file
Remove-Item injected_state.json -ErrorAction SilentlyContinue
Remove-Item -Recurse backup -ErrorAction SilentlyContinue
cd ..\..\capstone-support
python -m src.validate ; python -m pytest -q  # ✅ 8/8, 30 passed
```

```bash
# 🐧
cd examples/labs/lab-20
python inject_fault.py --list
rm -f injected_state.json && rm -rf backup
cd ../../capstone-support && python -m src.validate && python -m pytest -q
```

*(Submit `incident-timeline.md` before deleting anything else.)*

---

**After attempting:** a reference timeline and detection transcript live
in [`examples/labs/solutions/lab-20/`](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/labs/solutions/lab-20).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../about/index.md).*