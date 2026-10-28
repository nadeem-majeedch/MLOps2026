# Independent challenge — Module 12

> Do this **without** step-by-step help. Target **75 minutes**.

---

## 1. The scenario

You inherit a workflow that "works" but trusts itself too much: it never
cancels stale runs, gives its token write access it does not use, and has no
ML gate at all. A colleague also claims CI is slow "for no reason".

## 2. Tasks

1. **Diagnose a red run you caused.** Introduce a failure in *each* layer
   (lint / test / ml gate), and for each write the three-line diagnosis:
   *job → step → first error line*, plus the local command that reproduces it.
   Restore everything between attempts.
2. **Harden the file.** Starting from the shipped `ci.yml`, produce a diff
   that: (a) keeps least-privilege permissions, (b) keeps/justifies
   `concurrency`, (c) adds **one** new check you believe is worth its runtime.
   Justify (c) in three sentences, naming what bug it would have caught.
3. **Cost/speed audit.** For each of the five steps of the `test` job, label it
   *necessary* / *deferrable* / *redundant*, and state what you would move to a
   nightly run (a Module 13 preview) and why merging stays fast.
4. **Secrets drill (written).** A teammate pastes a token into a `run:` block
   "temporarily". Write: the three places it must never be, what an attacker
   with that token could do given `permissions: contents: read`, the exact
   remediation steps (revoke → rotate → history purge consideration), and the
   line in the workflow that limits the blast radius.
5. **The failed gate post-mortem.** With `roc_auc_floor: 0.99` (the lab's
   Step 8), write the incident note a teammate would read: symptom, failing
   command, root cause options (bad model vs bad floor), how you'd tell them
   apart, and the fix you chose.

## 3. Deliverables

- `diagnosis.md` — three red-run diagnoses with reproduction commands.
- `ci.diff` + `justification.md` — the hardening changes.
- `speed-audit.md` — the five-step labelling with a deferral proposal.
- `secrets-drill.md` — task 4 in full.
- `gate-postmortem.md` — task 5.

## 4. Self-check (feedback criteria)

| Grade | Looks like |
|---|---|
| **Excellent (4)** | All three diagnoses reproducible; hardening diff minimal and justified; speed audit distinguishes correctness checks from speed ones; secrets drill complete with remediation; post-mortem separates model vs floor with evidence |
| **Proficient (3)** | Diagnoses + hardening done; one section thin |
| **Developing (2)** | Only one layer diagnosed; diff without justification |
| **Not yet (1)** | No reproduction commands, or files were left broken |

**Integrity rule:** every claim about a red run needs its output pasted. If a
step didn't fail the way you expected, say exactly what happened instead —
unexpected CI behaviour is a finding, not a failure of your work.

---

**Next:** [knowledge-check.md](knowledge-check.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*