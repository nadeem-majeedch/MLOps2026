# Rubrics and self-assessment checklists

Practical, measurable rubrics for grading your own work, plus the checklists
that go with them. Everything here is **illustrative self-study material** —
not an official university grading policy. Instructors adopting this material
must map it to their own regulations.

> Binding weights for this course live in the
> [assessment framework](../syllabus/assessment-framework.md); this page is the
> *operational* version: bands you can actually score against, and tick-lists
> you can actually complete. Anchors used elsewhere: [project rubric](#project-rubric).

---

## 1. How to score honestly

1. Pick the evidence **before** picking the band. No transcript → the answer
   is automatically *Not yet*, no matter how good the write-up reads.
2. Score each criterion separately; never average away a zero — a *Not yet*
   on reproducibility or integrity caps the whole piece (see hard conditions
   in the [capstone assessment](capstone-assessment.md)).
3. Record the evidence path next to every band you award yourself.
4. Cooling-off rule: re-score after at least a day; keep both scores.

**Bands used throughout**

| Band | Meaning |
|---|---|
| **Exemplary** | Meets *and* something is generalised, documented, or tested beyond what was asked |
| **Meets** | The measurable acceptance criteria are all demonstrated with evidence |
| **Developing** | Partially demonstrated; evidence incomplete or not reproducible |
| **Not yet** | No acceptable evidence, or the claim was not actually executed |

---

## 2. Project rubric { #project-rubric }

Used for all five [mini-projects](mini-projects.md) and, in extended form, the
capstone. Four criteria, same everywhere — what changes per MP is the
*measurable acceptance line* in its specification.

| Criterion | Not yet | Developing | Meets | Exemplary |
|---|---|---|---|---|
| **Correctness** | Doesn't run, or produces wrong output | Runs but a stated requirement is unmet | Every acceptance criterion of the spec demonstrated | Criteria met **plus** an edge case handled/tested that the spec didn't demand |
| **Evidence** | Claims without transcripts | Transcripts exist but partial or unlabelled | Every criterion has a command + output, honestly labelled (incl. `NOT RUN` where true) | Evidence is organised so a stranger can verify it in minutes (paths, timestamps, machine noted) |
| **Reproducibility** | Only works on your machine | Works with hand-holding | Fresh clone + documented steps → identical result | Reproduction verified by *you on a second environment*, or automation proving it (hash comparison in CI) |
| **Communication** | No docs / docs that lie | Docs exist but drift from reality | README lets a newcomer complete the flow; decisions explained | Structure, naming and rationale so clear that review questions are answered before being asked |

**Scoring:** each criterion 0–3 (Not yet 0, Developing 1, Meets 2,
Exemplary 3) → /12 per MP. Illustrative interpretation: 10–12 Exemplary,
7–9 Meets, 4–6 Developing, ≤3 Not yet — and any *Not yet* on
Reproducibility or Evidence means **re-attempt regardless of total**.

---

## 3. Lab acceptance rubric

Applies to every lab under [Labs](../labs/index.md).

- [ ] All steps executed in order on **my** machine (no skipped steps, no
      pasted transcripts from the guide).
- [ ] Every ✅ checkpoint ticked only after seeing the expected output —
      deviations investigated, not ignored.
- [ ] Troubleshooting section used or consciously not needed (say which).
- [ ] Cleanup run to completion; repository/machine back to starting state.
- [ ] Reflection questions answered in writing (≥2 sentences each).
- [ ] Optional challenge attempted **or** a one-line reason skipped.

**Bands:** all six → Exemplary; first five → Meets; first three →
Developing; fewer → Not yet (redo the lab, not the tick-list).

---

## 4. Knowledge-check scoring (question banks & module checks)

- [ ] Attempted every question in writing before opening any key.
- [ ] Scored per the bank's suggested mark (typically 7/10) **and** its named
      load-bearing questions.
- [ ] For each miss: wrote down the *reason for the miss* (didn't know /
      misread / knew but couldn't articulate) — the remedy differs for all
      three.
- [ ] Re-attempt of missed questions a day later, closed book.

**Bands:** ≥ suggested mark with load-bearing correct → Exemplary; ≥ mark →
Meets; within 2 of the mark → Developing; below → Not yet (re-read the
module, re-attempt the whole bank).

---

## 5. Self-assessment checklists

### 5.1 Per-module checklist (run at the end of every module)

- [ ] Learning objectives: can state each one *without looking*.
- [ ] Vocabulary: every defined term still defined after the module ended.
- [ ] Knowledge check passed per §4.
- [ ] Module practice exercises completed with evidence
      ([module practice](module-practice.md)).
- [ ] Guided lab or standalone lab completed with cleanup.
- [ ] Portfolio entry filed (log/report/diagram) in `portfolio/modules/`.

### 5.2 Course-level readiness check (before starting the capstone)

- [ ] [Question banks](question-banks/index.md) 01–09 each at their suggested
      mark.
- [ ] [MP1–MP5](mini-projects.md) each scored ≥ *Meets* on all four rubric
      criteria.
- [ ] At least three labs re-attempted after a cooling-off period (evidence
      that the skill, not the memory, was retained).
- [ ] Can explain every term in the [glossary](../glossary/index.md) in one
      sentence each.
- [ ] A working runbook exists: from "something looks wrong" to "here is the
      evidence and the decision" ([LAB-18](../labs/lab-18-rollback-or-ride-it-out.md)
      pattern).

### 5.3 Submission checklist (any graded-looking deliverable)

- [ ] File names follow the course conventions
      ([standards §5](../COURSE-STANDARDS.md#5-filename-and-path-conventions)).
- [ ] Every number in the document traces to a transcript you ran.
- [ ] Everything unexecuted is labelled `NOT RUN` — no exceptions.
- [ ] No secrets, no real personal data, no licensed bytes committed
      ([datasets README](https://github.com/nadeem-majeedch/MLOps/blob/main/datasets/README.md)).
- [ ] Cleanup performed; generated outputs removed or git-ignored.
- [ ] Links inside the document resolve (click every one).

### 5.4 Final reflection prompts (pair with `REFLECTION.md`)

- [ ] What broke that I did not expect?
- [ ] Which acceptance criterion was hardest, and why?
- [ ] What would I delete from this project if I had to rebuild it?
- [ ] Which claim in my report am I least sure of — and what evidence would
      settle it?

---

## 6. Integrity rules (non-negotiable)

1. **Evidence before assertion.** A claim without an executed command behind
   it is a *Not yet*, however confident it sounds.
2. **Label the gaps.** `NOT RUN` costs a little; a fabricated log costs
   everything — it invalidates the whole submission.
3. **Attempt first, key second.** Solutions in
   [`keys/`](keys/question-banks-KEY.md) are for after, not instead.
4. **No real personal data, ever** — not in datasets, logs, screenshots or
   reports.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*