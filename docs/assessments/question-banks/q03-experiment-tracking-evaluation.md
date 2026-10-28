# Question bank 03 — Experiment tracking and model evaluation

**Covers:** Modules [06 — Experiment tracking with MLflow](../../modules/06-experiment-tracking-mlflow/index.md),
[09 — Artifacts, registries, promotion](../../modules/09-model-artifacts-registry/index.md),
and evaluation material in [07 — Testing for ML](../../modules/07-testing-for-ml/index.md).
**Format:** 10 questions — multiple choice, short answer, debugging, architecture, scenario.
**Suggested check:** 7/10, with **E4** and **E10** correct.

> *Attempt first, then read the
> [reference solutions](../keys/question-banks-KEY.md).*

---

## Part A — Multiple choice

**E1.** A run is tracked with metrics but no parameters or code version. What
can you still conclude six months later?

- (a) Everything — the metric is enough
- (b) The score that was achieved, but not how to reproduce it
- (c) The exact commit that produced it
- (d) That the data was valid

**E2.** Best practice for choosing the *final* model?

- (a) Highest validation AUC of the ten runs
- (b) The last run before lunch
- (c) A pre-declared selection rule plus checks against a baseline and
  threshold, applied to held-out data
- (d) Whichever run has the most parameters

**E3.** What must an artefact registry record for a promotion to be defensible?

- (a) A filename
- (b) Version id, hash, source run, metrics, who promoted it and when
- (c) The model's accuracy only
- (d) The server IP

**E4.** Dataset shift means:

- (a) The model's architecture changed
- (b) The distribution of input data differs from what the model was trained on
- (c) The team moved offices
- (d) The learning rate was reduced

## Part B — Short answer

**E5.** State the difference between the *validation* set and the *test* set,
and what goes wrong if you tune against the test set for three weeks.

**E6.** For an imbalanced problem (2% positive), why is accuracy useless and
which two metrics would you report instead — with the trade-off between them?

**E7.** What does a tracked run's **artifact** store that a metric does not,
and why does that matter for promotion?

## Part C — Debugging

**E8.** This comparison table came from an experiment tracker. Identify **two**
methodological errors that make the comparison invalid, and say how to fix
each:

| run | data | split | model | AUC |
|---|---|---|---|---|
| 14 | v3 | random 80/20, seed 7 | logreg | 0.81 |
| 22 | v4 | first 80% train, last 20% test | gbdt | 0.86 |

## Part D — Architecture

**E9.** Draw the artefact flow: training run → tracked run → staged artefact →
promoted version → serving. Indicate where hashes are computed and where a
rollback would re-point.

## Part E — Scenario

**E10.** Your challenger model wins on AUC (0.86 vs 0.84) but has materially
worse recall on the minority class and 3× the latency. The business goal is
"catch as many at-risk customers as possible, quickly". Argue **for or
against** promotion, state what you would measure to decide, and describe the
conditions you would attach either way.

---

**Next:** [reference solutions](../keys/question-banks-KEY.md) (bank 03), then
[bank 04](q04-testing-automation.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../../about/index.md).*
