# Concepts — Module 01

The teaching content for this module. Read it in order: every term is defined
before it is used, and nothing later assumes something you have not seen yet.

---

## 1. What we are actually building

A **machine-learning (ML) model** is a mathematical object that maps inputs to
predictions. Training a model means finding its internal parameters from data.
Using a trained model to make predictions on new data is called **inference**.

That sentence is the easy part. The hard part — and the reason this course
exists — is everything around it:

> A model is not a product. A *system that produces and uses predictions
> reliably* is the product.

The system around a model includes: the data it was trained on, the code that
trained it, the tests that check it, the service that answers requests with it,
the monitoring that notices when it goes wrong, and the process that decides
when to retrain or retire it.

**Vocabulary used so far** — read once, we will keep using them:

| Term | Meaning |
|---|---|
| **Model** | The trained mathematical object (weights/parameters) |
| **Training** | The process of fitting a model to data |
| **Inference** | Using a trained model to predict on new data |
| **Feature** | An input variable given to the model (e.g. `tenure_months`) |
| **Prediction / score** | What the model outputs for an input |
| **ML system** | Model + data + code + service + monitoring + process |

---

## 2. The ML lifecycle

Every ML system goes through the same stages, in a loop rather than a line:

```
        ┌──────────────────────────────────────────────────────────┐
        │                                                          │
        ▼                                                          │
  1. DATA ──► 2. VALIDATE & ──► 3. TRAIN & ──► 4. EVALUATE ──► 5. REGISTER │
     collect     VERSION           EXPERIMENT      vs. baseline   & PROMOTE│
                                                                      │
        ┌─────────────────────────────────────────────────────────────┘
        ▼
  6. PACKAGE & ──► 7. SERVE ──► 8. MONITOR ──► 9. RETIRE / ── back to 1
  DEPLOY           (API/batch)   (data, drift,   RETRAIN
                                  performance)
```

1. **Data** — raw inputs arrive (files, tables, events). Someone owns them.
2. **Validate & version** — check the data is what you expect, then freeze a
   copy so the run can be repeated later. *(Modules 04)*
3. **Train & experiment** — try configurations, recording each attempt. *(05, 06)*
4. **Evaluate** — compare against a **baseline** (a simple reference result) on
   metrics that matter for the actual decision. *(06)*
5. **Register & promote** — record the chosen model with its lineage, then move
   it deliberately toward production. *(09)*
6. **Package & deploy** — freeze the code and environment so it runs elsewhere.
   *(11, 12)*
7. **Serve** — answer prediction requests, online (one request → one answer) or
   in batch (a file of rows → a file of answers). *(10)*
8. **Monitor** — watch input quality, prediction quality, and system health. *(14)*
9. **Retire or retrain** — replace the model when evidence says to, not on a
   hunch. *(14)*

**Why a loop?** Because reality moves: the world changes, so the data changes,
so the model decays, so the cycle restarts. A system with no loop is a system
that silently rots — which is exactly the incident in this module's lab.

!!! note "Tool-specific vs. general"
    The *stages* are a general principle — every MLOps framework, paper, and
    vendor agrees on them. The *tools* in parentheses are this course's choices;
    the same stages appear in other tools with different names. Learn the
    stage, and any tool's documentation will make sense.

---

## 3. MLOps, and how it differs from DevOps

**MLOps** is the set of practices that makes the lifecycle above repeatable,
auditable, and observable — so that shipping an ML change is boring instead of
heroic.

**DevOps** is the equivalent discipline for conventional software: automate
building, testing, and releasing so changes flow safely and quickly.

The engineering instincts transfer. What does *not* transfer is that ML adds
three things ordinary software does not have:

| | Conventional software | ML systems |
|---|---|---|
| **What changes** | Code you wrote | Code **and data you did not write** |
| **How it breaks** | A crash or a wrong output you can see | A **silent quality decay**: the code runs fine, the answer gets worse |
| **How you test it** | Assert the correct output | Assert *quality* — a statistical threshold that can be flaky |
| **What "done" means** | Feature works | Feature works **and** stays accurate as the world moves |
| **Who is affected** | Users of the feature | Users of the feature **plus** whoever the predictions are about |
| **Feedback** | Immediate (errors reported) | Delayed (labels arrive days or weeks later) |

Five concrete consequences you will meet later in this course:

1. **Data is an input dependency.** Software breaks if code is wrong; ML breaks
   if the *data* is wrong even when the code is perfect → data validation (M04).
2. **Experiments must be recorded.** "Which run produced this model?" must have
   an answer → experiment tracking (M06).
3. **Tests are thresholds, not certainties.** "AUC ≥ 0.70" can fail because the
   data moved, not because someone broke the code → testing (M07).
4. **Deployment is a bet on the future.** You must be able to undo it →
   registries and rollback (M09, M12).
5. **Monitoring must watch quality, not only uptime.** A service answering
   perfectly-wrong predictions is "healthy" by normal dashboards → drift
   monitoring (M14).

---

## 4. What failure actually looks like

The lab's incident is fiction, but every failure in it is standard. The five
families:

1. **Silent quality decay.** The model's accuracy falls while every system
   dashboard stays green. Nobody was measuring *model quality* in production.
2. **Irreproducibility.** Nobody can say which code, data, and configuration
   produced the model that is serving traffic — so nobody can debug it.
3. **Train/serve skew.** Training and serving prepare data differently, so the
   model receives inputs it never saw during training.
4. **No rollback point.** The new model replaced the old one in place. When it
   turned out to be worse, there was nothing to return to.
5. **Organisational gaps.** A change shipped in a chat message, with no review,
   no owner, and no recorded reason. Tools did not fail; process did.

!!! warning "The important insight"
    Most ML production failures are **not exotic**. They are missing boring
    things: a version, a test, a threshold, an owner, a rollback. This course
    is mostly about installing the boring things early and cheaply.

---

## 5. Reproducibility — the foundation of everything else

**Reproducibility** means: given the same inputs, code, and configuration, a run
produces the same result — today, next month, and on someone else's machine.

It sounds obvious and is almost never true by default, because of four leaks:

| Leak | Example | Fixed by |
|---|---|---|
| Randomness | Unseeded splits, shuffles, initialisation | Set and record the seed (M05) |
| Environment | "It works with pandas 3.0, not 3.1" | Pin dependency versions (M02) |
| Data | The file changed since the last run | Version the dataset (M04) |
| Code | Uncommitted changes on someone's laptop | Version control with clean history (M02) |

You will *demonstrate* reproducibility in Module 05 by running the same training
twice and comparing hashes — and in this module you only need to accept the
claim that without it, every other guarantee in an ML system is unverifiable:
you cannot re-check a model you cannot re-create.

---

## 6. Technical debt — a preview

**Technical debt** is the future cost of a shortcut taken today. In ML systems
it takes forms that ordinary software rarely sees: data dependencies nobody
declared, features entangled with one another, experimental code quietly running
in production, and pipelines held together by manual steps.

Module 03 is entirely about this. Here you only need the framing: every shortcut
in the lifecycle is a loan, and interest accrues whenever the world moves.

---

## 7. Vocabulary check

Before continuing, you should be able to define each of these in one sentence
*without looking*:

model · training · inference · feature · prediction · ML system · MLOps ·
DevOps · ML lifecycle · reproducibility · baseline · technical debt ·
train/serve skew · silent decay · rollback

Any you cannot define: re-read §1–§5, then add your own wording to your
[glossary](../../glossary/index.md) notes. Writing a definition in your own words
is the fastest way to actually learn one.

---

## Check yourself

1. In the lifecycle diagram, which two stages would have prevented the lab's
   incident outright — and which one would have limited its damage?
2. A service answers every request in 20 ms and has 100% uptime. Its predictions
   are now worthless. Which row of the DevOps comparison explains this?
3. Name the four leaks that break reproducibility, and one fix for each.
4. Why is "the model passed all tests" a weaker statement than it sounds?

*(Answers are in [knowledge-check.md](knowledge-check.md) — attempt them there first.)*

---

**Next:** [worked-example.md](worked-example.md) — a real analysis of the incident data, run on this machine.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*