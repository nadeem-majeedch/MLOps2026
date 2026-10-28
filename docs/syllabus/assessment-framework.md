# Assessment Framework

> ⚠️ **Suggested self-study framework — not an official university grading scheme.**
> This document is a self-assessment design for independent learners. It is not an
> approved syllabus, credit-bearing assessment, or examination regulation of any
> university. Instructors who adopt it should map it to their own regulations.

The framework gives four layers of assessment — knowledge checks, practical labs,
progressive mini-projects, and an integrated capstone — plus rubrics with
**measurable** acceptance criteria so you can grade your own work honestly.

---

## 1. Assessment layers

| Layer | Frequency | Purpose | Weight (suggested) |
|---|---|---|---|
| **1. Knowledge checks** | End of each lesson cluster | Confirm vocabulary and concepts before touching tooling | 15% |
| **2. Practical labs** | 1–2 per module | Prove you can execute and verify | 35% |
| **3. Progressive mini-projects** | Modules 03, 06, 09, 12, 14 | Integrate 2–3 modules into something real | 25% |
| **4. Integrated capstone** | Module 17 | Demonstrate the whole lifecycle end-to-end | 25% |

Suggested thresholds for self-grading (you may set your own):

| Result | Overall | Hard conditions |
|---|---|---|
| **Distinction** | ≥ 85% | Every rubric's "meets" level on all capstone criteria |
| **Merit** | ≥ 70% | No rubric below "developing"; capstone passes |
| **Pass** | ≥ 50% | All essential labs verified at least once |
| **Not yet** | < 50% | Re-run the failed labs; re-assess |

**Integrity rule:** never record a check as passed without having run it and read
the output. Evidence without execution is not evidence.

---

## 2. Layer 1 — Knowledge checks

- 8–12 questions per module: definitions, matching, short scenarios,
  "what breaks first?" reasoning.
- Format: open-book (the course is open-book by design), answered in writing.
- Self-marking: answers provided in `keys/` after you attempt them; you must
  attempt first.
- Coverage rule: every learning outcome in
  [detailed-syllabus.md](detailed-syllabus.md) maps to ≥1 question; every question
  maps to an outcome.
- **Meets:** ≥ 70% correct after your first attempt. **Developing:** 50–69% —
  re-read flagged items. **Not yet:** < 50% — re-study the module's lessons.

## 3. Layer 2 — Practical labs

Each lab is graded against the shared lab rubric below (template:
[../TEMPLATES/LAB-TEMPLATE.md](../TEMPLATES/LAB-TEMPLATE.md)).

| Criterion | Meets (full marks) | Developing (½) | Not yet (0) | Measurable acceptance |
|---|---|---|---|---|
| **Execution** | All tasks completed on a clean run | Completed with hints | Did not complete | ✅ verification step output matches the stated expectation |
| **Reproducibility** | Identical result on a second run from clean checkout | Works but versions/seeds undocumented | Fails on rerun | Second run matches stated output/hash exactly |
| **Verification discipline** | All ✅ checkpoints run and recorded | Some run | None run | Every checkpoint has recorded output |
| **Troubleshooting** | Each failure documented: symptom → cause → fix | Fixes found, causes unclear | Failures left unresolved | ≥1 documented failure/fix, or an explicit "no failures" log |
| **Cleanup & hygiene** | Machine returned to start; repo committed | Partial cleanup | Mess left behind | `git status` clean; no stray processes/files |
| **Documentation** | Commands, versions, and rationale recorded | Commands recorded, rationale thin | Undocumented | A third party could repeat it from your write-up alone |

## 4. Layer 3 — Progressive mini-projects

Five integration points, each building on the last and feeding the capstone
(details and deliverables: [course-project-map.md](course-project-map.md)):

| Mini-project | After module | Integrates | Core acceptance criteria (measurable) |
|---|---|---|---|
| **MP1 — Reproducible project skeleton** | 03 | 01–03 | Fresh clone → one command reproduces documented output; structure matches the standard layout; README explains every folder |
| **MP2 — Tracked, justified model** | 06 | 04–06 | ≥10 tracked runs; dataset versioned; final choice justified against a baseline with metrics |
| **MP3 — Tested pipeline** | 09 | 07–09 | Test suite green with ≥80% line coverage; a seeded regression is caught; model registered with lineage |
| **MP4 — Automated delivery** | 12 | 10–12 | API containerised and passing tests in CI; a deliberately broken PR is blocked by a gate; a passing PR is merged |
| **MP5 — Monitored system** | 14 | 13–14 | Scheduled run executes; injected drift detected above threshold; retraining triggered and compared |

**Grading:** each mini-project uses the project rubric (§6) with the criteria
relevant to its stage; weights shrink as the capstone grows.

## 5. Layer 4 — Integrated capstone

Full description: [course-project-map.md](course-project-map.md). Graded by the
capstone rubric in §7. Submission must include the evidence bundle; a demo without
reproducible evidence cannot pass.

---

## 6. Project rubric (mini-projects)

| Criterion | Meets (full) | Developing (½) | Not yet (0) |
|---|---|---|---|
| **Requirement coverage** | All stated acceptance criteria demonstrably met | ≥70% met | <70% |
| **Reproducibility** | Clean-machine rerun reproduces stated results | Reruns with manual fixes | Cannot rerun |
| **Quality gates** | Tests/lint/validation all green in the repo | Some gates green | No gates |
| **Design justification** | ≥2 alternatives considered with trade-offs stated | Alternatives listed, trade-offs thin | No justification |
| **Documentation** | Setup, run, verify, cleanup all documented | Partial | Missing |
| **Evidence completeness** | Every claim backed by a log/report/artifact | Most claims | Claims unsupported |

## 7. Capstone rubric

| Criterion | Weight | Meets (full marks) — measurable acceptance |
|---|---|---|
| **End-to-end reproducibility** | 20% | A third party runs one documented command sequence from a clean clone and obtains your stated metrics within the declared tolerance |
| **Automated quality gates** | 15% | Tests, data validation, and an ML performance gate run in CI and are green on the final commit; at least one gate demonstrably blocks a bad change |
| **Serving & packaging correctness** | 15% | API passes its test suite from a container built by the documented command; image digest recorded |
| **Orchestration & scheduling** | 10% | Pipeline runs unattended on a schedule; a forced failure is retried/logged and recoverable |
| **Monitoring & drift response** | 15% | Drift reports generated from replayed data; a retraining decision is made and justified with evidence |
| **Security, privacy, fairness, governance** | 10% | Secret scan clean; unauthenticated access rejected; fairness metrics reported; model card + risk register present |
| **Design defence** | 10% | ≥2 rejected alternatives named with reasons; rollback plan written and tested once |
| **Evidence bundle quality** | 5% | Every claim in the write-up links to a log, report, or artifact in the bundle |

**Hard conditions:** reproducibility and quality gates must both reach "meets" —
otherwise the capstone is capped at "Developing" regardless of total score.

---

## 8. Feedback and re-assessment (self-study)

1. Attempt → record evidence → self-grade against the rubric → note gaps.
2. Re-attempt after a cooling-off period; keep both attempts (progress is evidence).
3. Where a rubric feels ambiguous, that ambiguity is a course bug — report it as an
   issue so the wording improves.
4. Peer review (optional): swap evidence bundles with a classmate and grade each
   other using these rubrics — the strongest available proxy for external moderation.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*
