# Concepts — Module 05

Four ideas carry this module: the **pipeline** as the unit of work,
**configuration** as the unit of intent, **seeds** as the unit of determinism, and
**evaluation against a baseline** as the unit of honesty.

---

## 1. Why a pipeline, not a script

A training run is a chain: validate data → build features → fit a model →
evaluate → persist. Written as one script, the chain still exists — it is just
invisible, which means you cannot test, cache, or re-run any part of it alone.

Separating stages buys you:

| Benefit | What it lets you do |
|---|---|
| **Testable** | Check feature construction without training (Module 07) |
| **Re-runnable** | Change the model, keep the features; change the data, keep everything else |
| **Auditable** | Point at the stage that differs when two runs disagree |
| **Automatable** | Later stages (08, 13) run each stage as a task with declared inputs/outputs |

```
config.yaml ──► validate ──► features ──► train ──► evaluate ──► artifacts/
                                   ▲            ▲
                             seed lives here   metrics land here
```

**Rule of thumb:** a stage is a function with inputs and outputs and *no
invisible dependencies*. If you cannot call it from a fresh Python session, it
is not a stage yet.

---

## 2. Configuration: the unit of intent

Configuration means: every value that affects a result lives in a file, with a
name, and is read at run time.

```yaml
seed: 42
test_size: 0.2
features:
  target: churn
  numeric: [tenure_months, monthly_charges, support_tickets]
  categorical: [contract_type]
model:
  family: logistic     # or gradient_boosting
```

What belongs in config: values you would sweep, compare, or justify
(seeds, sizes, hyperparameters, file paths, thresholds).
What does not: logic that, if edited, would invalidate the *meaning* of past
runs (how a feature is computed, how a split is stratified) — that belongs in
code, under tests.

**Why bother:** (1) a diff of `config.yaml` is a reviewable decision;
(2) two runs differ by exactly one visible line; (3) Module 06 logs this file
with every experiment, giving you lineage for free.

---

## 3. Seeds and determinism

A **random seed** initialises a pseudo-random generator. Same seed + same
inputs + same library versions ⇒ same outputs. Our pipeline seeds:

- the train/test split (`random_state`),
- the model's internal randomness (`random_state`),
- data generation itself (Module 04's generator).

**But a seed is necessary, not sufficient.** Sources of non-determinism a seed
does not fix:

| Source | Example | Fix |
|---|---|---|
| Dependency versions | pandas 3.0 vs 3.1 changes an operation | Pin versions (Module 02's lock file) |
| Input bytes | The CSV changed | Version data (Module 04) |
| Unordered iteration | Set/dict ordering affecting a calculation | Sort explicitly before order-dependent steps |
| Parallelism | Multi-threaded fitting with race-y accumulation | Fix thread counts where results must be bit-identical |
| Floating-point/platform | Different BLAS/CPU builds | Compare metrics with a tolerance, or hashes only on identical platforms |

That is why the module's proof is **two runs, one hash** — a hash comparison
catches everything a seed does not.

!!! note "Tool-specific vs. general"
    `random_state` is scikit-learn's vocabulary. PyTorch uses
    `torch.manual_seed`; NumPy uses a `Generator`. The principle — seed every
    source of randomness and record it — is universal, and Module 06 makes sure
    the seed is *recorded*, not just set.

---

## 4. Preprocessing belongs inside the model

The classic ML bug: fit a scaler on the **whole** dataset, then split. Test data
has leaked into training statistics — scores look great, then collapse in
production.

The cure is structural: put preprocessing and the model into **one object**.

```python
Pipeline([
    ("preprocess", ColumnTransformer([...scaling, one-hot...])),
    ("model", LogisticRegression(...)),
])
```

Consequences:

- **No leakage by construction** — `fit` only ever sees the training fold.
- **No train/serve skew** — serving loads the *same* object, so the transform
  used at inference is byte-identical to the one used in training.
- **One artefact to save** (§6).

**Feature engineering** (creating inputs from raw data) follows the same rule:
in code, in a module, never buried in a notebook cell — because the day you
reimplement it by hand for serving is the day train and serve diverge.

---

## 5. Evaluation: baselines, metrics, and a trap you can measure

### Baseline first

A **baseline** is the simplest credible reference: for this dataset, "predict
everyone stays" (majority class) or a logistic regression. Nothing is "good"
until it beats something.

### The metrics, and what each is blind to

| Metric | Question it answers | Blind spot |
|---|---|---|
| **Accuracy** | What fraction of predictions are right? | Collapses under imbalance — a model predicting "no churn" for all 400 test rows scores 0.91 while catching zero churners |
| **ROC AUC** | How well does the model *rank* positives above negatives? | Says nothing about the operating threshold or calibration |
| **F1** | Balance of precision and recall at a threshold | Ignores true negatives; depends on the threshold you chose |

### The trap, measured in this repository

Actual numbers from the shared example (400 test rows, 9% churn):

```text
model_family: logistic        accuracy: 0.91   roc_auc: 0.7163   f1: 0.0
majority baseline             accuracy: 0.91
```

Read that again: **accuracy equals the "predict nothing" baseline, F1 is zero —
yet the model ranks customers well (AUC 0.7163).** At a 0.5 threshold it simply
never crosses the line for a rare event.

Two conclusions you should carry forward:

1. Choosing a metric is a *decision about the business*, not a default. (A
   churn team cares about recall at a usable contact budget, not raw accuracy.)
2. The threshold is part of the model's behaviour and must be chosen, recorded,
   and tested — not inherited from `0.5`.

Module 06 turns this into tracked comparisons; Module 07 turns it into a
performance gate.

---

## 6. Persistence

Saving the fitted `Pipeline` (joblib here) writes preprocessing **and** model
into one artefact. Rules:

- Persist the **pipeline**, never the bare estimator — otherwise serving must
  re-implement your transforms.
- Save the **metrics next to the model** (the module writes `metrics.json`
  alongside), so a file cannot travel alone.
- Artefacts are generated: committed to *tracking*, not to Git
  (`.gitignore` already excludes `artifacts/`).

Formats: joblib/pickle are convenient and Python-only; ONNX exists for
cross-runtime use — a trade-off you revisit in Module 09, not a decision to make
now.

---

## 7. Check yourself

1. Why is fitting a scaler before the split a bug even though the code runs
   perfectly?
2. List four things a seed does **not** make reproducible.
3. The baseline model reports accuracy 0.91 and F1 0.0. Explain both numbers
   without using the word "bug".
4. What is the difference between a stage and a script, in one sentence?
5. Which values in the example's `config.yaml` are *decisions*, and which are
   *mechanics*? Would you move any to code?

*(Answers in [knowledge-check.md](knowledge-check.md).)*

---

**Next:** [worked-example.md](worked-example.md) — two runs, one hash; a seed change; and the baseline beating the fancy model.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*