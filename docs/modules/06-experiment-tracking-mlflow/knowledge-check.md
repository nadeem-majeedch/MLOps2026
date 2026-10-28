# Knowledge check — Module 06

Attempt every question first. **10 questions · ~30 minutes · open book.**
Suggested pass mark **7/10**, with no question about metric selection wrong.

---

## Part A — Recall

**Q1.** List the five categories of information a complete run record contains,
with one example of each.

**Q2.** Define: *experiment*, *run*, *parameter*, *metric*, *artifact*,
*champion*, *challenger*.

**Q3.** What are the three MLflow pieces that can be local or hosted, and which
does this course run locally?

**Q4.** Name two things the course deliberately does **not** log into MLflow, and
say where each lives instead.

## Part B — Comprehension

**Q5.** MLflow 3.x rejects the legacy `file:./mlruns` backend. What did the
course do instead, and why is that still "local, free, no account"?

**Q6.** Your sweep's top run wins by 0.01 AUC. Module 05 measured ±0.03 movement
from the seed alone. What can you claim, and what must you do before claiming it?

**Q7.** Why is "the run with the highest accuracy" often the wrong answer on a
9%-positive dataset — reference the actual numbers from this course.

**Q8.** A teammate says tracking is just "saving your notebook's outputs in a
database". Give the strongest version of their argument, then refute it with two
capabilities tracking provides.

## Part C — Application

**Q9.** Write the pre-registration block for an experiment: the question, primary
metric, baseline, comparison rule, and fixed variables — for a scenario where
marketing can target 200 customers per campaign.

**Q10.** Six months later someone asks which data produced the champion model.
List the artefacts you would follow, in order, and which module created each.

---

# Answers and reasoning

**Q1 — 1 point (0.2 each).**
Parameters (seed, split, model settings) · metrics (AUC, accuracy, F1) ·
artifacts (config file, model file, plots) · source versions (git commit, data
hash) · status/timing (start, end, failure).
*Reasoning:* any missing category leaves a specific question unanswerable — the
mapping between category and question is the test.

**Q2 — 1 point (0.14 each, rounded).**
*Experiment* = named collection of related runs. *Run* = one execution with its
own params/metrics/artifacts. *Parameter* = chosen input. *Metric* = measured
output. *Artifact* = file produced. *Champion* = model currently justified for
use. *Challenger* = candidate being tested against it.
*Reasoning:* these are the shared vocabulary across all trackers, not just MLflow.

**Q3 — 1 point.**
Tracking backend/store, artifact store, and server/UI. The course runs all
locally: SQLite backend (`sqlite:///mlflow.db`), local `mlruns/` artifact folder,
and `mlflow server` on 127.0.0.1 when the UI is wanted.
*Reasoning:* recognising the three separable pieces is what lets you move between
local and hosted setups deliberately.

**Q4 — 1 point (0.5 each).**
Raw training data — it stays in `data/` versioned by DVC's hash (Module 04).
Source code — it stays in Git, identified by commit (Module 02). (Also
acceptable: secrets/environment files, which never enter either.)
*Reasoning:* trackers reference data and code by identity; storing copies would
bloat the store and risk leaking data.

**Q5 — 1 point.**
It switched the tracking URI to a local SQLite database
(`sqlite:///mlflow.db`). Still local because the database is a file in the
project folder; still free because SQLite ships with the Python ecosystem; no
account because nothing contacts a service — the server, when used, binds to
127.0.0.1.
*Reasoning:* "local" is about where bytes live and who can reach them, not about
which backend brand you use.

**Q6 — 1 point.**
Claim only that the run *is* higher in this sample. Before claiming an
improvement: re-run with multiple seeds (or cross-validation), report the spread,
and require the gain to exceed the measured noise band — or state a tolerance in
advance and test against it. If the gain cannot exceed noise, it is not a finding.
*Reasoning:* tracking exists to prevent exactly this over-claiming.

**Q7 — 1 point.**
Because accuracy rewards the majority class: this dataset is 9% churn, so
"predict nobody churns" scores 0.91 — and the actual baseline model does score
0.91 accuracy with F1 0.0, while its AUC (0.7163) shows genuine ranking ability.
Choosing on accuracy would rank a model that contacts nobody as "excellent".
The metric must follow the decision (recall/precision at a contact budget).
*Reasoning:* metric selection is a business claim, not a technical default.

**Q8 — 1 point.**
Strongest version: tracking *is* structured note-keeping — parameters, metrics,
and files, just stored per run rather than per notebook. Refutation: (1) it gives
*comparability* — a queryable table where runs are ordered by any metric, which
notebooks cannot do; (2) it gives *identity and lineage* — a run ID binding
config, data reference, and model artefact together, so a decision can be
audited and reproduced months later; (plus) it survives tooling changes and
separates human narrative from machine records.
*Reasoning:* the refutation must name capabilities, not vibes.

**Q9 — 1 point.**
A passing answer:
> **Question:** which model puts the most actual churners in the top 200 contacts?
> **Primary metric:** recall@200 (precision@200 as tie-breaker).
> **Baseline:** current champion run + majority/random ranking.
> **Rule:** challenger wins only if recall@200 improves ≥5% relative across ≥3
> seeds on the same data version.
> **Fixed:** data version, split strategy, seed set, feature set, threshold
> policy.
*Reasoning:* every element blocks a way of fooling yourself — that is the point
of pre-registration.

**Q10 — 1 point.**
(1) Model file in `artifacts/` (M05) → (2) run ID with params, metrics, and the
logged config artifact (M06) → (3) data hash in the config/pointer (M04) →
(4) git commit for the code (M02) → (5) restoring the exact bytes from DVC
(M04). At Module 09 this chain is stored beside the model in the registry.
*Reasoning:* being able to walk the chain in order proves the lifecycle's
guarantees are connected rather than decorative.

---

## Marking and next steps

| Score | Action |
|---|---|
| **9–10** | Proceed to Module 07 |
| **7–8** | Re-read the missed sections, then continue |
| **5–6** | Redo lab steps 1–6, then re-take |
| **< 5** | Re-read concepts §1–§4 and re-run the worked example first |

File your score as `modules/06/knowledge-check.md`.

---

[← Module overview](index.md) · [Troubleshooting →](troubleshooting.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*