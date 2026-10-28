# Concepts — Module 14

*Vocabulary: monitoring, prediction log, reference window, covariate/data drift,
concept drift, performance degradation, PSI, KS test, threshold, alert,
human-in-the-loop, retraining policy, feedback delay, ground truth.*

---

## 1. Monitoring answers questions in order

Monitoring is not "charts on a wall". It is four questions, each with its own
evidence, in an order that prevents expensive mistakes:

```
1. What did we predict?          -> prediction log      (record)
2. Did the inputs change?        -> drift report        (statistics)
3. Did accuracy fall?            -> performance report  (labels required)
4. Should we retrain?            -> decision.md         (human approves)
```

Skipping from (2) to (4) is the classic, expensive error: retraining on drift
alone churns models, burns effort, and often *reduces* trust — because if
drift didn't actually hurt, the retrain "fixed" nothing and the next alert
loses credibility.

## 2. What to log (LO 14.1)

One JSON line per scored record (`monitoring/predictions.jsonl`):

| Field | Why |
|---|---|
| `ts` | windows and feedback delay |
| input features (`tenure_months`, `monthly_charges`, …) | the only way to measure input drift later |
| `churn_probability`, `churn_pred` | what the model actually said |
| `model_version` | which model said it (registry id — joins to Module 09 lineage) |
| `actual` | ground truth **when it arrives** — often `null` at logging time |

Design points worth internalising:
- **Labels are delayed** (billing cycles, cancellations) — `null` is a normal
  state, not an error; performance reporting *waits* for them.
- **Sampling vs full logging:** log everything at low volume (our case);
  sample or aggregate at high volume — and know that sampling hides rare
  events (Module 15 covers the privacy cost of logging everything instead).
- **Reference window:** the comparison baseline. We snapshot
  `monitoring/reference.csv` from training-era data; production systems
  usually use the *training distribution* or a recent known-good window —
  and must say which, because it changes what "drift" means.

## 3. Drift ≠ degradation (the module's thesis)

**Covariate / data drift** — the input distribution `P(X)` changed (people buy
different plans, prices rose, a new segment arrived).
**Concept drift** — the relationship `P(Y|X)` changed (the same contract now
churns differently, e.g. a competitor's offer changed behaviour).
**Performance degradation** — measured accuracy on labels fell.

The logical structure, stated precisely:

| Observation | What it proves | What it does NOT prove |
|---|---|---|
| Drift, no labels | the world moved | nothing about accuracy |
| Degradation, no drift | something is wrong (pipeline, labels, leakage) | that inputs changed |
| Drift **and** degradation | strongest case to retrain | *why* it degraded (needs investigation) |
| Neither | keep watching | that this will stay true |

Why drift alone proves nothing: a model whose decision boundary is far from
the shifted region keeps ranking perfectly well (our `shift` window scored
**higher** AUC than reference). Conversely, no drift with falling accuracy is
the *more* alarming case — the inputs look fine but the world's rules changed
(concept drift, or a labelling bug).

## 4. The statistics, and their honest limits

| Measure | Question it answers | Our threshold |
|---|---|---|
| **PSI** (population stability index, binned) | how far did the distribution move, in relative terms? | < 0.10 stable · 0.10–0.20 moderate · > 0.20 strong |
| **KS test** (two-sample) | is the difference larger than sampling noise would give? | p < 0.01 significant (with the statistic reported, not just p) |
| **Category mix shift** (chi-square + max proportion delta) | did categorical proportions move? | max delta > 0.10 or p < 0.01 |

Honesty rules (LO 14.3):
- **p-values scale with sample size** — with 100k rows everything is
  "significant". Always report effect size (PSI, KS statistic) beside p.
- **Window size sets resolution**: our 400-row windows make AUC *noisy* — the
  baseline window itself measured 0.6902 vs the full test set's 0.7163. A
  threshold below the noise floor produces false alarms (that is a *sampling
  noise* explanation, not drift).
- **Seasonality** looks like drift on short windows (monthly billing cycles).
  Before acting: compare against the *same window last period*, not just the
  overall reference.
- **Measurement change** (a unit bug, a schema rename, a new encoder) is
  "drift" that is really *your* pipeline's fault — check the contract
  (Module 04) before blaming the world.

## 5. Performance measurement when labels arrive (LO 14.2/14.4)

`monitoring/performance.py` joins labelled records per window and computes
ROC-AUC/accuracy/F1 against the **reference metrics** (0.7163) and the
**floor** (0.70). Two independent tripwires:
`degraded = (auc < floor) OR (drop_vs_reference > 0.05)`.

Why both: the floor catches "always bad"; the drop catches "bad *compared to
what we shipped*" even when still nominally above floor. And why neither can
run without labels: **the report is the only component allowed to claim the
model is wrong** — its authority comes from ground truth.

## 6. The decision matrix and the human

`monitoring/decision.py` applies an explicit policy:

| drift? | degraded? | action | Reason in one line |
|---|---|---|---|
| no | no | **KEEP** | nothing to see |
| yes | no | **MONITOR** | drift is a reason to *look*, not to retrain |
| no | yes | **INVESTIGATE** | labels fell without drift → suspect pipeline/labelling, not the world |
| yes | yes | **RETRAIN CANDIDATE** | evidence agrees; prepare the full Module 08→09 loop |

The output ends with a **human checklist** — evidence, pipeline+gate, register,
*rollback known before promoting*. Automation recommends; a person decides and
owns the decision. That is what "human-in-the-loop" means concretely here.

## 7. The retraining loop, end to end

```
decision: RETRAIN CANDIDATE
  → python -m pipe.run --clean        (retrain + gates, Module 08)
  → python ml_check.py                (CI-style release check, Module 12)
  → python -m registry register ...   (lineage, Module 09)
  → stage staging → production        (approval rules)
  → RESTORE PREPARED: python -m registry rollback production
  → restart service / rebuild image   (Modules 10–11)
  → watch the NEXT windows            (did it help? closes the loop)
```

Retraining without the rollback plan in hand is the mistake Module 09 exists
to prevent — the decision file forces you to write it down *first*.

## 8. What this module deliberately leaves out

- **Privacy of what you log** (identifiers, sensitive attributes, retention):
  Module 15 — the lab notes it, the treatment comes next.
- **Distributed-system metrics** (latency, saturation, error rates as
  first-class dashboards): Module 16.
- **Automatic retraining pipelines** with no human: offered only as advanced
  reading — the course's position is that the *decision* is a person's until
  the system's evidence loop has earned years of trust.

---

**Next:** [worked-example.md](worked-example.md) — the two windows and the two
decisions, from real runs.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*