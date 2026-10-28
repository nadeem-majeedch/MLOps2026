# Problem Statement Template

> **How to use this file:** copy it to `PROBLEM.md` at the root of your
> project (capstone milestone **C1**). Delete the italic guidance lines.
> Every numbered section must contain your words — a section left with the
> guidance text still in it counts as *Not yet* for that criterion
> ([rubric](../assessments/rubrics-checklists.md#project-rubric)).
> Companion templates: [architecture](ARCHITECTURE-DIAGRAM-TEMPLATE.md) ·
> [experiments](EXPERIMENT-RECORD-TEMPLATE.md) ·
> [report](FINAL-PROJECT-REPORT-TEMPLATE.md).

---

```markdown
# Problem statement — <system name>

**Author:** <name> · **Date:** <YYYY-MM-DD> · **Version:** 0.1 (draft for C1)
**Status:** draft | approved | superseded

## 1. The problem, in plain language
*One paragraph a non-technical stakeholder could repeat back to you. Who has
the problem, how often, and what it costs them today (time, money, risk).*

## 2. Who is affected — and who could be harmed
*Intended users, and the people who are affected by the output but are not
the users. Name one misuse you are explicitly designing against.*

## 3. Why ML is (or is not) the right tool
*What specifically about this problem needs prediction rather than a rule, a
query, or a person? If a trivial baseline solves it, say so — that is a
strong answer, not a weak one.*

## 4. Success criteria (measurable)
| Goal | Metric | Threshold | Measured on | Why this threshold |
|---|---|---|---|---|
| e.g. catch at-risk cases | recall @ operating threshold | ≥ 0.60 | held-out test set | cost of a missed case ≈ 5× a false alarm |
| e.g. usable in a workflow | p95 latency | ≤ 200 ms | local load test | matches the caller's SLA |
| e.g. refuse to ship bad models | quality gate | passes all criteria | CI | see §7 |

*At least one ML metric AND one operational metric. State the baseline you
must beat.*

## 5. Data
*Source (synthetic generator / open dataset with exact URL and licence),
approximate size, schema in one table, and how it will be versioned
(procedure + where the hash lives). No private personal data — ever.
See datasets README in the repository root.*

## 6. Scope
**In (MVP):** *3–5 bullets — the smallest end-to-end system that proves the
problem.*
**Out:** *3–5 bullets you deliberately defer, each with a one-line reason.*
**Optional extensions:** *labelled with extra cost/effort, not required to
pass.*

## 7. Risks and constraints
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| e.g. leakage in features | … | … | feature audit + test |
| e.g. drift after launch | … | … | monitoring plan (link) |

*Technical, data/privacy, and operational risks each considered.*

## 8. Deliverables
*Link the checklist: PROBLEM.md (this), EXPERIMENTS.md, EVIDENCE/, DEPLOYMENT.md,
MONITORING.md, REPORT.md, REFLECTION.md.*

## 9. References
*Module pages, labs, and tool docs you are building on — this statement must
connect to the course, not float free of it.*
```

**Self-check before submitting:** someone who has never met you can answer
"what, for whom, how good is good enough, with what data, and what could go
wrong" — using only this document.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*