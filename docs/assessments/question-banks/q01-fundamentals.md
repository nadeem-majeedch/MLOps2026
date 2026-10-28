# Question bank 01 — MLOps fundamentals

**Covers:** Modules [01 — Introduction & ML lifecycle](../../modules/01-introduction-mlops-lifecycle/index.md)
and [03 — Project structure & technical debt](../../modules/03-ml-project-technical-debt/index.md).
**Format:** 10 questions — multiple choice, short answer, debugging, architecture, scenario.
**Suggested check:** 7/10, with **F3** and **F10** correct (the lifecycle and the
reproducibility questions are load-bearing).

> *Attempt every question in writing before opening the
> [reference solutions](../keys/question-banks-KEY.md) — the key explains the
> reasoning, which is the part worth reading.*

---

## Part A — Multiple choice

**F1.** A model is retrained weekly, but nobody can say which data or code
produced the model currently serving traffic. This is primarily a failure of:

- (a) model accuracy
- (b) lineage and versioning
- (c) feature engineering
- (d) inference latency

**F2.** Which statement about ML systems is *true*?

- (a) ML bugs are usually caught by the same tests as ordinary software
- (b) The data an ML system learned from can change its behaviour without any
  code change
- (c) An ML model's correctness can be fully verified before deployment
- (d) ML removes the need for monitoring

**F3.** Put these lifecycle stages in a sensible order:
evaluation · data collection · deployment · monitoring · retraining ·
experiment tracking · problem definition.

- (a) problem definition → data collection → experiment tracking → evaluation →
  deployment → monitoring → retraining
- (b) data collection → evaluation → problem definition → deployment →
  retraining → monitoring → experiment tracking
- (c) experiment tracking → problem definition → deployment → data collection →
  monitoring → evaluation → retraining
- (d) evaluation → problem definition → data collection → monitoring →
  deployment → retraining → experiment tracking

**F4.** "Our dashboard is green: 100% uptime, 40 ms responses." Why can this be
true while the model silently gets worse?

- (a) Dashboards are always wrong
- (b) Uptime and latency measure *software* health, not *model* quality
- (c) The monitoring team disabled alerts
- (d) ML models cannot get worse after deployment

## Part B — Short answer

**F5.** Define, each in one sentence: *training*, *inference*, *baseline*.

**F6.** Name four ways ML systems differ from conventional software, and give
one consequence of each.

**F7.** The course lists four "reproducibility leaks". Name any three and give
one concrete fix for each.

## Part C — Debugging

**F8.** This project layout came from a real student submission. List **five**
problems a new team member would hit, and for each, the folder/file where you
would expect the fix to live:

```
project/
├── Notebook final.ipynb
├── Notebook final (2).ipynb
├── data.csv
├── model.pkl
├── results.xlsx
├── main.py            # imports from ../shared/utils.py (not in the repo)
└── README.md          # "run Notebook final.ipynb"
```

## Part D — Architecture

**F9.** Draw (boxes and arrows, any tool) the minimum architecture that answers:
*"Which code, which data, and which parameters produced the model currently in
production?"* Label what is stored where, and which component you would query
to answer the question.

## Part E — Scenario

**F10.** A colleague says: "MLOps is just DevOps with Python — install CI, ship
containers, done." Give the **strongest version** of their argument, then
refute it with two specific examples from this course where ML changes the
answer entirely.

---

**Next:** check your answers against the
[reference solutions](../keys/question-banks-KEY.md) (bank 01), then either
re-read [Module 01 concepts](../../modules/01-introduction-mlops-lifecycle/concepts.md)
or continue to [bank 02](q02-reproducibility-data-versioning.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../../about/index.md).*
