# Knowledge check — Module 01

**Attempt every question first, in writing, before you open the answers.**
Checking an answer you have not tried teaches you nothing — you will recognise
the right answer later and mistake recognition for knowledge.

- 10 questions · ~30 minutes · open book (the course is open-book by design)
- Suggested pass mark: **7/10**, with no question about the lifecycle stages wrong.

---

## Part A — Recall

**Q1.** List the nine stages of the ML lifecycle in order (concepts §2).

**Q2.** Define, each in one sentence: *training*, *inference*, *feature*,
*reproducibility*.

**Q3.** What is a **baseline** in model evaluation, and why is it needed before
you can call any result "good"?

**Q4.** Name five ways ML systems differ from conventional software.

## Part B — Comprehension

**Q5.** A colleague says: "Our service is healthy — 100% uptime, 40 ms
responses." Their model has been getting worse for two weeks. Which specific row
of the DevOps comparison explains why their dashboard is green?

**Q6.** The lab incident's `v3` model was promoted on 2026-08-11 and the first
threshold breach was on 2026-08-14, while the human noticed on 2026-08-24.
Explain what each of those three dates tells you.

**Q7.** For each of the four "reproducibility leaks" (concepts §5), give the leak
and one concrete fix.

**Q8.** Classify these as technical or organisational, and name the lifecycle
stage:
1. The training data file was silently replaced by a newer extract.
2. A model was deployed by direct upload from someone's laptop.
3. Nobody recorded which random seed produced the shipped model.

## Part C — Application

**Q9.** Your team ships a new churn model. Two weeks later, revenue from the
segment it scores has dropped 6%. Walk through the lifecycle: which stages do you
inspect first, in what order, and what evidence would you look for at each?

**Q10.** A friend argues that MLOps is "just DevOps with Python". Give the
strongest version of their argument, then refute it with two specific examples
from this course's later modules.

---

# Answers and reasoning

Attempt everything above first. Then mark yourself: 1 point per question,
0.5 for partially correct.

**Q1 — 1 point.**
Data → validate & version → train & experiment → evaluate → register & promote →
package & deploy → serve → monitor → retire/retrain (looping back to data).
*Reasoning:* the order matters because each stage consumes the previous stage's
output; a stage performed out of order is exactly what causes failures like
training on unvalidated data.

**Q2 — 1 point (0.5 each for two pairs).**
*Training* = fitting a model's parameters from data. *Inference* = using a
trained model to produce predictions. *Feature* = an input variable supplied to
the model. *Reproducibility* = same inputs, code, and configuration ⇒ same
result, on any machine, at any time.
*Reasoning:* the pairs that get confused — training and inference are different
moments in a model's life; "feature" is not "target".

**Q3 — 1 point.**
A baseline is the simplest credible reference result (a trivial rule, a
logistic regression, or last period's model) that everything else must beat.
Without it, a metric value has no meaning: AUC 0.72 might be excellent or
terrible depending on what the alternative is.
*Reasoning:* metrics are comparisons, not grades — this is why Module 06 insists
on baseline-vs-challenger evaluation.

**Q4 — 1 point (0.2 per correct item, max 1).**
Any five of: code **and data** change; failures are *silent quality decay*, not
crashes; tests are statistical thresholds and can be flaky; "done" is conditional
on a moving world; the people affected include those the predictions are *about*;
feedback/labels arrive late; experiments must be tracked to be repeatable.
*Reasoning:* each maps to a later module — data (M04), thresholds (M07),
monitoring (M14), tracking (M06).

**Q5 — 1 point.**
The row "How it breaks" — ML quality decays while the system keeps answering
correctly *formed* requests. Uptime and latency measure the plumbing, not the
answer's correctness; only *model-quality* monitoring (Module 14) would catch it.
*Reasoning:* the essential distinction: health ≠ accuracy.

**Q6 — 1 point (⅓ each).**
- **11 Aug** = the change event: a new model entered production with no registry
  entry or rollback point (a register/promote stage failure).
- **14 Aug** = earliest *machine-detectable* evidence: the monitor stage could
  have fired here, 3 days after the change.
- **24 Aug** = actual detection: 13 days after the change, by a human, at which
  point damage had accumulated.
*Reasoning:* separating change, detectability, and detection is how you quantify
what monitoring is worth.

**Q7 — 1 point (0.25 each).**
Randomness → set and record the seed (M05). Environment → pin exact dependency
versions in a lock file (M02). Data → version datasets with hashes/DVC (M04).
Code → version control with a clean, committed history (M02).
*Reasoning:* each leak has a distinct owner — that is why reproducibility needs
several practices, not one tool.

**Q8 — 1 point (⅓ each).**
1. *Technical*, stage: **validate & version** (a validation gate and a data
   version would have caught it).
2. *Organisational*, stage: **package & deploy** (no process forbidding it; the
   fix is CI/CD as a forced path, M12).
3. *Technical-leaning organisational*, stage: **train & experiment** (tracking
   records the seed automatically, M06).
*Reasoning:* misclassifying #2 as technical leads to buying tools to fix a
process problem.

**Q9 — 1 point.**
Ordered inspection with evidence: (1) **monitor** — drift and quality metrics for
the last two weeks; (2) **serve** — did inputs/latency change, any schema errors;
(3) **register & promote** — which model version is live, when promoted, versus
what was validated; (4) **validate & version** — did the data change or degrade;
(5) **train & experiment** — which run produced this model, on what data, with
what metrics. Evidence at each: dashboards, request logs, registry history,
validation reports, run history.
*Reasoning:* you inspect from the *most recent change backwards* — newest,
cheapest evidence first — and each stage returns a yes/no on "did this change".

**Q10 — 1 point.**
*Strongest version:* the mechanics are the same — version control, CI/CD,
containers, monitoring, on-call; the language differs, not the engineering.
*Refutation:* (a) in ML the artifact is *statistical* and must be gated by
threshold tests and data validation (M07), so CI must run data and model gates,
not just unit tests; (b) rollback in ML is a *registry promotion* backed by
lineage — which model, trained on which data — rather than redeploying a binary
(M09/M12); and (c) monitoring must measure answer quality against drifting data,
not only system health (M14).
*Reasoning:* the best rebuttals are concrete mechanisms, not slogans.

---

## Marking and next steps

| Score | Action |
|---|---|
| **9–10** | Objectives met — proceed to Module 02 |
| **7–8** | Re-read the sections behind the misses, then continue |
| **5–6** | Redo the lab's tasks 3–5, then re-take the check |
| **< 5** | Re-read concepts §1–§5 and worked-example before anything else |

Record your score and the questions you missed in your portfolio
(`modules/01/knowledge-check.md`) — later modules build directly on these terms.

---

[← Module overview](index.md) · [Troubleshooting →](troubleshooting.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*