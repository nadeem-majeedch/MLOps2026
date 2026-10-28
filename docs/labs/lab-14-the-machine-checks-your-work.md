# LAB-14 — The Machine Checks Your Work

## 1. Lab identity

| | |
|---|---|
| **Lab ID** | **LAB-14** |
| **Difficulty / topic** | 🚀 Advanced · CI/CD with GitHub Actions |
| **Prerequisite module** | [12 — CI/CD and ML validation with GitHub Actions](../modules/12-cicd-github-actions/index.md) · LAB-07/LAB-13 recommended |
| **Fixture** | your lab folder (or `examples/labs/lab-14/` scaffold) |
| **Estimated time** | 120 minutes · GitHub Actions is **free for public repos** · ⚠️ evidence requires *your* push (your action, per project rules) |

## 2. Scenario and background

Your tests are green — on *your* machine. The team needs the machine to
check: every push runs lint + tests + a lightweight ML validation, with
least privilege, no credentials, and a **failing** pipeline anyone can
reproduce locally. You will author the workflow, rehearse every command
locally first (so CI failures are never a surprise), then push and
capture real run evidence — or complete **Path B** (local rehearsal
only, honestly labelled) if you cannot push.

## 3. Learning objectives

By the end you can:

1. Write a workflow: triggers, jobs, steps, pinned action versions,
   `permissions: contents: read`.
2. Rehearse CI commands locally so failures are diagnosed *before* push.
3. Make CI **fail on purpose once** (a seeded defect) and paste that run
   — green that has never been red proves nothing.
4. Handle secrets correctly: none in YAML; injection only via
   `secrets.*` at runtime — and say why no secret is needed here anyway.

## 4. Prerequisites and estimated time

- Module 12 read; LAB-07 or LAB-13 suite available (your tests matter).
- A GitHub repo **you own** for Path A (free account). Path B needs
  nothing but this machine.
- **120 min** (rehearse 30 · author 30 · green run 15 · red run 20 ·
  write-up 25).

## 5. Student task statement

**Path A:** deliver `.github/workflows/lab-14.yml` in *your* repository
with jobs `lint`, `test`, `ml-validate`; evidence = one green run URL,
one **red** run (seeded defect, then revert), and a write-up of the
least-privilege and secret decisions.
**Path B:** deliver `CI-REHEARSAL.md`: the exact workflow you *would*
push plus local transcripts proving every step command works (and one
that fails on the seeded defect) — labelled **NOT RUN on GitHub**.

## 6. Required dataset and setup instructions

```powershell
# 🪟 Windows — PowerShell — rehearse FIRST, in your lab folder
python -m ruff check .            # ✅ exit 0 (repo standard: ruff.toml)
python -m pytest -q               # ✅ your suite green
python -m pip freeze > ci-freeze.txt   # record the environment CI must reproduce
```
Reference workflows to crib from: `.github/workflows/ci.yml` (churn) and
`.github/workflows/capstone.yml` (capstone) — both ship in this repo.

## 7. Starter files

| File | Role |
|---|---|
| `examples/labs/lab-14/` | optional scaffold folder (put your workflow there for Path B) |
| repo workflows above | working, least-privilege examples |
| `.github/workflows/lab-14.yml` | **you write it** (Path A, in your repo) |

## 8. Numbered implementation steps

**Step 1 — Rehearse every command locally** (§6) and paste outputs.
✅ Checkpoint: each command has a local exit code — CI will run *exactly*
these.

**Step 2 — Author the workflow**: triggers (`push`/`pull_request`),
`permissions: contents: read`, three jobs mirroring Step 1, Python
setup with pip cache keyed on your requirements file.
✅ YAML validates (`python -c "import yaml; yaml.safe_load(open('.github/workflows/lab-14.yml'))"`).

**Step 3 — Path A: push; Path B: local dry-run.** Path A: Actions tab →
run appears → wait for green. Path B: run each job's commands in order
as a scripted sequence (`ci-local.ps1`) and paste the transcript.
✅ green evidence (URL or local transcript).

**Step 4 — The red run (both paths).** Seed a defect (make a test fail
deliberately or break a function), push (A) / run the script (B), capture
the failure naming the job; revert; confirm green again.
✅ red + re-green evidence.

**Step 5 — Secrets & permissions write-up:** why `contents: read` is
enough; where a secret *would* go (`env:` from `secrets.X`, never YAML
literals); confirm you have **no** secrets configured for this workflow.

**Step 6 — Failure-reading note:** paste the first real error line from
your red run and explain how the log localised it (job → step → command).

## 9. Commands and expected results

| Command | Expected |
|---|---|
| `python -m ruff check .` | `All checks passed!` exit 0 |
| `python -m pytest -q` | all pass; exit 0 |
| YAML validation of your workflow | parses without error |
| seeded-defect run | **fails**, naming job + step + command |
| after revert | green again |
| ⚠️ GitHub run (Path A) | green check on the run page (URL pasted) |
| Path B | `CI-REHEARSAL.md` with `NOT RUN on GitHub` label |

## 10. Acceptance criteria (objective)

- [ ] Workflow file with triggers, 3 jobs, pinned action versions,
      `permissions: contents: read` (or Path B equivalent + local proof).
- [ ] Local rehearsal transcript for every CI command.
- [ ] **Red run evidence** (seeded defect) + revert to green.
- [ ] Secrets write-up: none in YAML; injection path described; none
      configured.
- [ ] Failure-reading note localising the red run's error.
- [ ] Everything not executed is labelled NOT RUN (no invented URLs).

## 11. Troubleshooting and recovery

| Symptom | Cause | Fix |
|---|---|---|
| workflow file not listed on GitHub | wrong path/filename (must be `.github/workflows/*.yml`) | move it; Actions tab refreshes on push |
| job fails at install | CI env ≠ local (missing dep or version) | reinstall from the pinned file you use locally; paste `pip freeze` diff |
| lint passes locally, fails in CI | different tool version | pin the linter version in the job (the repo's workflows pin `ruff==0.15.1`) |
| cache step errors | cache key path wrong | key on the requirements file that actually exists |
| no red run possible (green forever) | you skipped the seeding step | it is graded — seed, capture, revert |
| cannot push (Path A unavailable) | no repo of your own | Path B is the graded path; label honestly |

## 12. Reflection questions

1. Your workflow needs `contents: write` for something. What review
   question must be asked before granting it?
2. CI green ≠ code correct: name one class of defect CI will never catch
   and where Module 07's layers *would*.
3. "Rehearse locally first" saved which step from becoming a 2 a.m.
   mystery? Describe the failure class it eliminates.

## 13. Optional challenge tasks

1. Add a path filter so docs-only changes skip the ML job.
2. Upload the test report as a build artefact (`actions/upload-artifact`).
3. Add a `pull_request` gate that requires the green run before merge —
   describe the repo setting (you control it in *your* repo).

## 14. Rubric / checklist

| Points | Criterion |
|---|---|
| 4 | workflow: triggers + 3 jobs + pinned versions + least privilege |
| 3 | every step rehearsed locally with pasted exits |
| 4 | red run captured + revert to green |
| 3 | secrets/permissions write-up accurate |
| 2 | honest labelling (Path B / no invented URLs) |
| **16** | **total** · ≥12 = pass |

## 15. Cleanup

```powershell
cd <your lab folder>
Remove-Item ci-freeze.txt, ci-local.ps1 -ErrorAction SilentlyContinue   # if not submitting
# Path A: the seeded-defect branch must be deleted after capture
git log --oneline -3        # verify only intended commits remain
```
Nothing in *this* repository was pushed — your work lives in your repo.

---

**After attempting:** a reference workflow + rehearsal script live in
[`examples/labs/solutions/lab-14/`](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/labs/solutions/lab-14)
(⚠️ the workflow itself is YAML-validated only — CI runs belong to *your*
push).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../about/index.md).*