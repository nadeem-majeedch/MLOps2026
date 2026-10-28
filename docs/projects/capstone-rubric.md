# Capstone rubric — self-scoring worksheet

**Deliverable 3 of the capstone set.** The authoritative rubric lives in
the [assessment framework §7](../syllabus/assessment-framework.md#7-capstone-rubric)
(single source of truth — weights and acceptance criteria change there
first). This page is the **worksheet** you fill in: score each criterion,
paste the evidence path, and record the self-grade. It is a *suggested
self-study framework*, **not an official university grading scheme**.

Score each criterion: **1.0** meets · **0.5** developing · **0** not yet.
Weighted total = Σ (score × weight). Maximum = **1.00**.

---

## The scoring table

| Criterion | Weight | Meets means (measure it) | Score | Evidence path |
|---|---|---|---|---|
| End-to-end reproducibility **(hard)** | 20% | clean clone → documented commands → metrics within your pre-declared tolerance | ___ | |
| Automated quality gates **(hard)** | 15% | tests + data validation + ML gate green in CI on final commit; ≥1 gate proven to block a bad change | ___ | |
| Serving & packaging correctness | 15% | API passes its suite from a container built by the documented command; image digest recorded (or ⚠️ NOT RUN, honestly) | ___ | |
| Orchestration & scheduling | 10% | unattended scheduled runs; a forced failure retried/logged and recoverable | ___ | |
| Monitoring & drift response | 15% | drift + performance reports from replayed data; retraining decision justified with numbers | ___ | |
| Security, privacy, fairness, governance | 10% | clean secret scan; unauthenticated access rejected (or decision documented); fairness reported with caveats; model card + risk register present | ___ | |
| Design defence | 10% | ≥2 *rejected* alternatives with reasons (real, specific, conditional); rollback plan written **and** tested once | ___ | |
| Evidence bundle quality | 5% | every claim in the write-up links to a log/report/artifact | ___ | |

**Weighted total: ____ / 1.00**

## Hard-condition gate (applies before the total counts)

- [ ] Reproducibility = 1.0 **and** quality gates = 1.0?
      → total stands.
- [ ] Either is < 1.0?
      → the capstone is **capped at Developing (≤ 0.5)** no matter what
      the arithmetic says. Record the gap and re-attempt that criterion.

## Banding (self-study interpretation)

| Total | Band | Meaning |
|---|---|---|
| ≥ 0.85 | Distinction-equivalent | defence-ready; extensions can deepen it |
| 0.70–0.84 | Merit-equivalent | solid system; name three improvements and close them |
| 0.55–0.69 | Pass-equivalent | working core; evidence or governance is thin — re-run Lab 17's review |
| < 0.55 | Re-attempt | revisit the modules behind your weakest criteria (rubric rows → module map in [Module 17 references](../modules/17-capstone/references.md)) |

## Scoring honesty rules

1. Every "meets" needs a **file path** a stranger can open.
2. Fabricated or paraphrased-for-convenience evidence scores **0** for
   that criterion — and invalidates the bundle's trust.
3. Score once cold; re-score after a cooling-off period; keep **both**
   worksheets (progress is evidence —
   [framework §8](../syllabus/assessment-framework.md#8-feedback-and-re-assessment-self-study)).
4. Optional but strongest: swap bundles with a classmate and grade each
   other (peer review proxy for external moderation).

---

[Capstone specification](capstone-specification.md) ·
[Task checklist](capstone-checklist.md) ·
[Self-assessment & reflection](capstone-self-assessment.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*