# Integrated capstone assessment

The capstone is the course's single integrated piece of work: one system,
built across Modules 06–17, that demonstrates **all** the layers at once.
This page is the *assessment view* of it — what is examined, how the evidence
fits together, and how to self-grade honestly. The build instructions live
elsewhere and are linked throughout.

> ⚠️ **Illustrative self-study assessment — not an official university
> examination or grading regulation.** Weights and bands below are proposed
> and illustrative; instructors must map them to their own regulations.

---

## 1. What is examined

| Component | What it demonstrates | Primary evidence | Where it is specified |
|---|---|---|---|
| **Specification & success criteria** | scoping, measurable goals | problem statement with metric + threshold | [capstone specification](../projects/capstone-specification.md), [problem-statement template](../TEMPLATES/PROBLEM-STATEMENT-TEMPLATE.md) |
| **Data foundation** | provenance, validation, privacy | dataset record + validation report passing | [datasets README](https://github.com/nadeem-majeedch/MLOps/blob/main/datasets/README.md), Module 04, [LAB-03](../labs/lab-03-gate-the-dirty-extract.md) |
| **Reproducible training** | environments, seeds, pipelines | two identical runs + manifest | Module 05, [LAB-05](../labs/lab-05-deterministic-by-construction.md), [experiment-record template](../TEMPLATES/EXPERIMENT-RECORD-TEMPLATE.md) |
| **Tracking & model selection** | justified decisions | run table + selection memo vs baseline | Module 06, [LAB-06](../labs/lab-06-ten-runs-one-decision.md), MP2 |
| **Testing & gates** | automated quality control | suite + coverage + a refusal transcript | Module 07/08, [LAB-07](../labs/lab-07-catch-the-leakage.md), [LAB-08](../labs/lab-08-the-gate-that-must-refuse.md), [test-evidence template](../TEMPLATES/TEST-EVIDENCE-TEMPLATE.md) |
| **Registry & release** | lineage, approval, rollback | staged/promoted versions + rollback rehearsal | Module 09, [LAB-09](../labs/lab-09-staged-verified-released.md), [LAB-15](../labs/lab-15-nothing-ships-unchecked.md) |
| **Serving & container** | API contract, packaging | service tests + container transcript (or labelled Path B) | Module 10/11, [LAB-10](../labs/lab-10-serve-it.md), [LAB-11](../labs/lab-11-malformed-requests-autopsy.md), [LAB-12](../labs/lab-12-ship-the-image.md), [deployment-checklist template](../TEMPLATES/DEPLOYMENT-CHECKLIST-TEMPLATE.md) |
| **CI automation** | machines, not memory | workflow + red-then-green evidence | Module 12, [LAB-14](../labs/lab-14-the-machine-checks-your-work.md) |
| **Monitoring & response** | noticing and acting | prediction log, drift reports, 2×2 decision | Module 14, [LAB-16](../labs/lab-16-a-pipeline-that-runs-itself.md)–[LAB-18](../labs/lab-18-rollback-or-ride-it-out.md), [monitoring-report template](../TEMPLATES/MONITORING-REPORT-TEMPLATE.md) |
| **Security, privacy, governance** | responsible deployment | review verdict + model card + risk register | Module 15, [LAB-19](../labs/lab-19-deployment-security-review.md), [bank 08](question-banks/q08-security-governance.md) |
| **Architecture & documentation** | systems thinking, communication | architecture diagram + final report | [architecture-diagram template](../TEMPLATES/ARCHITECTURE-DIAGRAM-TEMPLATE.md), [final-project-report template](../TEMPLATES/FINAL-PROJECT-REPORT-TEMPLATE.md) |
| **Defence** | ownership under pressure | walkthrough + **fault-injection runbook** | Module 17, [LAB-20](../labs/lab-20-incident-day.md) |

Milestone tracking (C1–C7, with evidence slots) lives in the
[capstone task checklist](../projects/capstone-checklist.md) — copy it into
your repository and keep it updated as you go.

---

## 2. Illustrative weighting

| Component group | Illustrative share |
|---|---|
| Data foundation + reproducible training + tracking | 25% |
| Testing, gates, registry, serving, container, CI | 30% |
| Monitoring, security/governance, documentation | 25% |
| Defence (including fault injection) | 20% |

> These numbers are a **proposal for self-study use**, not a published
> grading scheme. The binding version for this course remains the
> [assessment framework §7](../syllabus/assessment-framework.md#7-capstone-rubric).

---

## 3. Hard conditions (gate before any score counts)

From the [capstone rubric](../projects/capstone-rubric.md) — both must reach
*Meets* or the whole capstone is capped at *Developing*, regardless of how
nice the rest looks:

1. **End-to-end reproducibility** — fresh clone, documented steps, identical
   result (hash or metrics diff).
2. **Automated quality gates** — at least one gate that actually refuses a
   defective candidate (transcript of a refusal required).

A third practical condition used at defence time: **the system must survive a
fault you inject yourself** ([LAB-20](../labs/lab-20-incident-day.md)'s
pattern) and be restored with evidence.

---

## 4. Submission bundle (what "handing it in" means)

Assemble exactly these files (templates linked):

1. `PROBLEM.md` — [problem statement](../TEMPLATES/PROBLEM-STATEMENT-TEMPLATE.md)
2. `docs/architecture.md` — [architecture diagram](../TEMPLATES/ARCHITECTURE-DIAGRAM-TEMPLATE.md)
3. `EXPERIMENTS.md` — [experiment record](../TEMPLATES/EXPERIMENT-RECORD-TEMPLATE.md)
4. `EVIDENCE/tests/` — [test evidence](../TEMPLATES/TEST-EVIDENCE-TEMPLATE.md)
5. `DEPLOYMENT.md` — [deployment checklist](../TEMPLATES/DEPLOYMENT-CHECKLIST-TEMPLATE.md)
6. `MONITORING.md` — [monitoring report](../TEMPLATES/MONITORING-REPORT-TEMPLATE.md)
7. `REPORT.md` — [final project report](../TEMPLATES/FINAL-PROJECT-REPORT-TEMPLATE.md)
8. `REFLECTION.md` — answers to the
   [self-assessment questions](../projects/capstone-self-assessment.md)

**Integrity rule:** every transcript in the bundle must be one you ran, with
the machine it ran on. Fabricated evidence is an automatic *Not yet* — see
the [rubric](rubrics-checklists.md).

---

## 5. Defence format (self-study: say it out loud, alone is fine)

| Segment | Minutes | What you must show |
|---|---|---|
| Walkthrough | 10 | architecture → data → training → gate → serve → monitor, on the running system |
| Evidence spot-check | 5 | pick any two acceptance criteria and produce their transcripts live |
| **Fault injection** | 10 | break something (data or artefact), detect with your own tooling, restore, prove recovery |
| Questions | 5 | "why this threshold?", "what happens if the data shifts?", "who is harmed if this is wrong?" |

Practise with [LAB-20](../labs/lab-20-incident-day.md) — it *is* the fault
injection segment, rehearsed.

---

## 6. Self-grading protocol

1. Fill the [rubric worksheet](../projects/capstone-rubric.md) criterion by
   criterion, pasting the evidence path next to each score.
2. Check the two hard conditions **first**; if either fails, stop and fix.
3. Score the [practical rubric](rubrics-checklists.md) bands for the
   component groups in §2.
4. Answer the [reflection questions](../projects/capstone-self-assessment.md)
   honestly — a blunt 70 beats a polished 85 with hidden gaps.
5. Re-attempt after a cooling-off period; keep **both** attempts.

---

**Prerequisites for attempting this:** [question banks](question-banks/index.md)
01–09 at their suggested marks, all five [mini-projects](mini-projects.md), and
the module practice exercises for 14–17.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*