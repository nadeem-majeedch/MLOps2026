# Knowledge check — Module 07

## How to use this

1. Answer **in writing**, open book first, then closed book.
2. Mark yourself with the [answers](#answers) — **only after** committing to yours.
3. Target: **80% with justified reasoning**. Below that, re-read
   [concepts.md](concepts.md) §§1–5 before moving on.
4. This is self-assessment inside a suggested self-study framework — not an
   official university exam. See [assessment-framework](../../syllabus/assessment-framework.md).

---

## Questions

**Q1.** Name the five testing layers this course teaches, and give one example
assertion for each.

**Q2.** *(True/False, with justification)* "A test suite with 95% line coverage
is proven to be a good test suite."

**Q3.** A colleague writes `assert len(preds) > 0`. Explain, in two sentences,
why this is a weak test and rewrite it into a strong one for the churn pipeline.

**Q4.** What is the difference between an *invariance* test and an *oracle* test?
Give one of each from the churn suite.

**Q5.** State the property that makes a test **regression**-testing rather than
merely unit-testing, and name the churn test that satisfies it.

**Q6.** Your performance gate fails with
`roc_auc 0.6412 is below the floor 0.7000` after a dependency upgrade.
List the first three things you would check, in order, and say which of them
distinguishes "broken code" from "moved world".

**Q7.** Why must every gate you build have a test proving *the gate itself* can
fail? Name the churn test that plays this role.

**Q8.** Match each failure to its layer:

| Failure discovered | Layer that should have caught it |
|---|---|
| (a) A CSV column silently renamed upstream | ? |
| (b) Predictions differ between batches of 1 and 100 | ? |
| (c) The service returns 500 on valid input | ? |
| (d) A refactor halves recall unnoticed | ? |
| (e) `train.py`'s loop body never executes | ? |

**Q9.** In one sentence each: distinguish *code coverage*, *mutation testing*,
and *flakiness*. Which of the three would you measure with a number?

**Q10.** A test passes locally but fails in CI only when the whole suite runs.
Name the most likely class of defect and the standard fix.

---

## Answers

**Q1.** Unit (e.g. *"split_xy returns exactly the configured feature columns"*),
data (e.g. *"churn is 0 or 1 in every row"*), model (e.g. *"roc_auc ≥ floor"*),
integration (e.g. *"train → predict works end-to-end in one process"*), and
regression (e.g. *"same seed ⇒ same metrics"*, guarding against re-breaking
yesterday's behaviour). **Reasoning:** each layer guards a different failure
source — code logic, input contract, quality, wiring, and history — so no single
layer substitutes for the others. *(5/5)*

**Q2. False.** Coverage counts lines *executed*, not conditions *asserted*; a
suite of `assert True` over every line scores 100% and tests nothing.
Coverage is a map of where you have *not* looked. **Reasoning:** the course's
own 78% suite is more trustworthy than a hypothetical 100% suite of vacuous
tests, because its assertions have content. *(5/5)*

**Q3.** It asserts only that *something* came back — an empty-ish, wrong-valued
list still satisfies it, so it can never fail for the defects that matter.
Rewrite: `assert len(preds) == len(X) and set(np.unique(preds)) <= {0, 1}` —
now length, alignment, and label domain are all pinned. *(5/5)*

**Q4.** An *invariance* test asserts something that must **not change** under a
transformation (batching: *"predictions for one row equal the first row of
predictions for 100 rows"*). An *oracle* test asserts a **known correct answer**
computed independently (the floor: *"roc_auc on the held-out set ≥ 0.70"*,
a number justified by baseline experiments). *(5/5)*

**Q5.** A regression test pins **previously working behaviour** so it cannot
silently break again — it encodes history, not just correctness today. The
churn suite's `test_same_seed_gives_same_metrics` does this for the
determinism claim established in Module 05. *(5/5)*

**Q6.** In order: (1) *did our code change?* — `git status`/recent diff, which
separates code breakage from environment drift; (2) *did the environment change?*
— library versions (`pip freeze` vs the recorded lockfile), which is the
"moved world" case; (3) *did the data change?* — dataset hash vs the one the
floor was calibrated on. Only by checking (2) and (3) against recorded evidence
can you attribute the failure to code. **Reasoning:** a gate failure is a claim
that *something* changed; the triage enumerates the three things that can. *(5/5)*

**Q7.** Because a gate that has never rejected anything is indistinguishable
from a gate that is silently broken — you need proof it produces exit code 1
when it should. The churn suite's `test_validator_catches_the_seeded_defect`
(also the lab's seed-a-bug step) plays this role. *(5/5)*

**Q8.** (a) data · (b) model/invariance · (c) integration · (d) regression ·
(e) unit. **Reasoning:** each failure's *location* — input, math, wiring,
history, logic — points to the layer whose job that is. *(5/5)*

**Q9.** *Coverage* = fraction of lines executed (measurable as a percentage);
*mutation testing* = whether deliberately broken code gets caught (measurable as
a mutation score); *flakiness* = a test's pass/fail varying with no code change
(measurable as failure rate across repeated identical runs). You would put a
number on all three, but only coverage is the one people routinely misuse. *(4/5 —
the judgement clause is opinion; accept well-reasoned alternatives)*

**Q10.** Hidden **shared state** (or ordering dependence) between tests — one
test's files/globals/env leak into another. Fix: isolate every test
(`tmp_path`, fresh fixtures, no `chdir`/env mutation without restore) and make
tests order-independent. *(5/5)*

**Scoring:** /50 raw → ÷50 × 100. **80+ = ready to move on.** 60–79: re-read
[concepts.md](concepts.md) §§1–3 and redo Q4, Q6, Q8. Below 60: redo the lab's
Step 3 — nothing fixes this gap faster than watching tests catch real bugs.

---

**Next:** [troubleshooting.md](troubleshooting.md) ·
[Module 08 →](../08-pipeline-automation/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*