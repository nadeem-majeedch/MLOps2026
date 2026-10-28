# Lab 17 — Production readiness review

## 1. Scenario and business problem

A candidate system is in front of you: the capstone reference
(`examples/capstone-support/`) or — at this stage of the course — **your
own capstone**. Management wants a **go / no-go** before anything is
called "deployed". Your job is not to demo; it is to *review*: run the
checklist, file issues with evidence, repair what you can, and write down
what you cannot.

**Business problem:** readiness is a decision, not a feeling. The review
process is the guided element — the build was the previous sixteen
modules' job.

## 2. Skills practising

- Running a production readiness review (PRR) from a fixed checklist.
- Converting each checklist line into a *command and an expected result*.
- Filing issues: severity, evidence, owner — then fixing or accepting.
- Fault injection through the system's own detection paths, and recovery
  with documented commands only.
- Writing a post-incident review that a non-author could act on.

## 3. Prerequisites

- Modules 01–16 complete (or at minimum: 07 tests, 09 registry, 10 API,
  12 CI, 14 monitoring read and run at least once).
- [concepts.md](concepts.md) §§2, 5, 6, 9 read.
- Reference implementation runnable: `python pipeline.py` green.
- Free, local, no accounts. ⚠️ Docker/Kubernetes steps are conditional —
  label them *not run* if your machine lacks the tools (same honesty rule
  as Module 16).

## 4. Required tools and estimated time

| Item | Detail |
|---|---|
| Tools | Python 3.10+, the repo's example folders |
| Cost | Free, local, offline |
| ⚠️ Resource-heavy | none (conditional Docker step if available) |
| 🕐 Estimated time | 180 minutes (review 90 + fault injection 45 + write-up 45) |

## 5. Input data and how to obtain it

The reference implementation's own artefacts:

```powershell
# 🪟 from examples/capstone-support
python generate_data.py && python pipeline.py
python -m pytest -q                 # ✅ expect 30 passed
```
🐧 Linux/macOS: identical commands.

## 6. Directory layout (what you are reviewing)

```
examples/capstone-support/
├── config.yaml            # every knob: seed, features, gate floor, fairness target
├── generate_data.py       # provenance: deterministic, seeded
├── src/                   # validate / features / train
├── pipeline.py            # 5 stages + gate + report.md (hashes)
├── tests/                 # 30 tests: data, leakage, model, API, release
├── service/               # FastAPI: health, model-info, predict (+ /docs)
├── Dockerfile             # ⚠️ conditional: needs Docker
├── .github/workflows/…    # at repo root — ⚠️ runs only after a push
├── monitor.py             # drift → performance → decision
├── release.py             # register / promote(+ack) / rollback / history
└── README.md              # the claim sheet you are verifying
```

## 7. Setup and execution steps

**Step 1 — Scope the review (10 min).** Copy the checklist in §8 into
`PRR.md`. For each line, write the **command** you will run. Rule: a line
without a command is an opinion, not a check.
✅ **Checkpoint:** every row has a command or an explicit `n/a — reason`.

**Step 2 — Run the checklist against the reference (40 min).** Execute
each command; paste real output next to each row; verdict per row:
PASS / FAIL / NOT RUN (reason). Known-good baselines to compare against:
pipeline all-ok, `30 passed`, `All checks passed!` (ruff), the refusal +
`--ack` sequence, the MONITOR decision (see
[worked-example.md](worked-example.md) for the exact transcripts).
✅ **Checkpoint:** `PRR.md` has ≥15 rows with verdicts; at least the two
⚠️ rows read `NOT RUN — Docker unavailable` / `NOT RUN — requires push`.

**Step 3 — File issues (15 min).** Any FAIL gets: id, severity
(blocker/major/minor), evidence (command + output), suggested fix, owner.
Three issues are *findable in the reference as shipped* — e.g. its Docker
and CI steps are unexecuted on the authoring machine; the fairness gap is
over target by design. Finding those is not a trick: it is the review
working as intended.
✅ **Checkpoint:** ≥3 filed issues; blockers distinguished from majors.

**Step 4 — Repair what you can (20 min).** Fix one *minor* issue in your
review target end-to-end (rerun its check → green → paste). Accept one
issue *with reason and owner* (risk register row from Module 15 if this
is your own system).
✅ **Checkpoint:** one red→green pair, one documented acceptance.

**Step 5 — Fault injection (45 min, LO 17.4).** Choose **one** fault and
run it through detection, using only documented commands to recover:

| Fault | Injection (reference paths) | Detection must come from… | Recovery |
|---|---|---|---|
| A corrupt data | truncate `data/support.csv` rows / mangle a column | `pipeline.py` validation stage | `python generate_data.py` then re-run |
| B bad model | lower the floor above the AUC (edit `roc_auc_floor: 0.99`) | the **gate** refusing + `report.md` | restore config; explain why gate exists |
| C governance | `python release.py promote r001` without `--ack` | the **refusal** + history unchanged | promote with ack, or roll back |
| D process | kill the API mid-request | client error → restart | documented restart; `/health` OK again |

✅ **Checkpoint:** detection quoted from the tool (not from you watching),
recovery transcript pasted, and `POSTMORTEM.md` written: timeline,
what the fault cost, what would have caught it *earlier*.

**Step 6 — Rollback rehearsal (20 min).** Against your own capstone (or
the reference if that is your target): register a release, promote it,
change to another, then `python release.py rollback` — the audit trail
must show both movements. If you took Module 16 Path A, add
`kubectl rollout undo` evidence.
✅ **Checkpoint:** `release.py history` shows promote → rollback lines.

**Step 7 — Write the go/no-go (20 min).** One page: verdict, blockers
(list), accepted risks (with owners), conditions for the next review.
Rules: no verdict without evidence links; **no "deployed"** language for
anything not actually deployed.
✅ **Checkpoint:** a reader can tell exactly what was, and was not,
reviewed — including the NOT RUN rows.

## 8. The production readiness checklist

| # | Area | Check (command form) | Verdict |
|---|---|---|---|
| 1 | Data | regenerate data; hashes match `data_sha256`? (`pipeline.py` line 1) | |
| 2 | Validation | feed bad input; does `src/validate.py` refuse? | |
| 3 | Reproducibility | clean folder → documented commands → metrics within declared tolerance | |
| 4 | Gate | `roc_auc_floor` enforced in `report.md` + CI gate job? | |
| 5 | Tests | `python -m pytest -q` → all green; at least one test fails when you seed a bug | |
| 6 | Lint | `python -m ruff check .` | |
| 7 | Tracking | `runs.jsonl` last line matches the artefacts you see? | |
| 8 | Release governance | refusal without ack? history complete? rollback rehearsed? | |
| 9 | API | `/health`, `/model-info`, `/predict` verified live; 422 for bad input | |
| 10 | Docs vs reality | every README command run verbatim — did any lie? | |
| 11 | Container | ⚠️ `docker build` + run + health (or NOT RUN + reason) | |
| 12 | CI | ⚠️ workflow green after push / gate blocks a bad change (or NOT RUN) | |
| 13 | Monitoring | drift + performance + decision regenerated from scratch | |
| 14 | Security | `scan_secrets.py` clean on your code; no secrets in git; API auth decision documented | |
| 15 | Fairness/governance | metrics reported with caveats; over-target → ack path or mitigation | |
| 16 | Lineage | any release → dataset + commit, answered from files alone | |
| 17 | Evidence | every README claim links to a log/artifact | |
| 18 | Teardown/cleanup | documented commands return the machine to pre-lab state | |

## 9. Expected outputs and verification methods

| Artefact | Verification |
|---|---|
| `PRR.md` | ≥18 rows, each PASS/FAIL/NOT RUN **with command + output** |
| Issues | ≥3 filed: severity, evidence, fix, owner |
| One repair | red→green rerun pasted |
| `POSTMORTEM.md` | timeline + detection source + recovery + earlier-catcher |
| Rollback rehearsal | `release.py history` lines (promote + rollback) |
| Go/no-go | blockers vs accepted risks explicit; NOT RUN rows visible |

## 10. Acceptance criteria (✅ Lab 17 complete)

1. Completed checklist with real outputs (or honest NOT RUN rows).
2. ≥3 issues filed; ≥1 repaired with a red→green transcript; ≥1 accepted
   with reason and owner.
3. One fault injected, **detected by the system's own tooling**, recovered
   with documented commands only.
4. Post-incident note written, including what would catch it earlier.
5. Rollback rehearsed and visible in the audit history.
6. Go/no-go verdict with evidence links — no unverified "it works".

## 11. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Checklist rows all "opinion" | skipped Step 1's command-writing rule | rewrite rows as commands; no command → `n/a — reason` |
| Fault A not detected | validation runs before you corrupted, or cache skipped stage | re-run `python pipeline.py` after tampering; use `--clean`-style full re-run |
| Fault B "passes" | floor still below AUC | the injection is the *floor above* AUC — check `report.md` says FAIL |
| `30 passed` becomes failures | you edited the reference while reviewing | `git` isn't yours to reset — restore the file by hand; your edits belong in *your* capstone |
| Docker/CI rows blocked | tools unavailable | mark NOT RUN with the reason — the rubric accepts labelled gaps, not invented runs |
| Rollback says "nothing to roll back to" | only one release ever promoted | register + promote a second release first |

Course-wide issues: [troubleshooting](../../troubleshooting/index.md).

## 12. Cleanup

```powershell
# 🪟 from examples/capstone-support
python -c "import pathlib; [p.unlink() for p in pathlib.Path('monitoring_out').glob('*') if p.is_file()]"   # optional: fresh monitoring
# restore any config you edited for fault B; delete PRR/POSTMORTEM drafts you don't keep
```
Keep `PRR.md`, `POSTMORTEM.md`, and the evidence — they feed your
[capstone self-assessment](../../projects/capstone-self-assessment.md).

## 13. Debrief and ethics note

- The review's honesty is the deliverable: **NOT RUN + reason** beats a
  fabricated PASS, every time — the course's evidence rule at its loudest.
- The reference's over-target fairness gap is *documented*, not hidden;
  shipping-with-signature (Module 15) vs blocking are both legitimate
  engineering decisions — *silence* is not.
- A review that files no issues on a system you didn't build usually
  means the review was too gentle, not that the system is perfect.

## 14. Stretch goals (optional)

1. Swap PRR sheets with a classmate's capstone (peer review — the course's
   external-moderation proxy in
   [assessment-framework §8](../../syllabus/assessment-framework.md)).
2. Add an SLO with a measuring script (e.g. 95% of scheduled ticks green
   over a day) and let it run for 24 hours.
3. Take fault **E**: a dependency upgrade — bump one pinned version, run
   the suite, and write up what broke (supply chain, Module 15 §3).

---

[← Worked example](worked-example.md) · [Next: independent challenge →](independent-challenge.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*