# Projects

The practical spine of the course: **five progressive mini-projects** that build on
each other, and one **integrated capstone**. Each extends the repository you
started earlier rather than starting from scratch — by Module 14 you own a single
repository that has grown across the whole course, and it becomes your capstone seed.

Full detail, deliverables, and evidence tables:
[course project map](../syllabus/course-project-map.md).

---

## Progressive mini-projects

| # | After | Project | Acceptance at a glance |
|---|---|---|---|
| **MP1** | Module 03 | [Reproducible project skeleton](../modules/03-ml-project-technical-debt/index.md) | Fresh clone + one command reproduces documented output |
| **MP2** | Module 06 | [Tracked, justified model](../modules/06-experiment-tracking-mlflow/index.md) | Dataset versioned, ≥10 tracked runs, champion justified against a baseline |
| **MP3** | Module 09 | [Tested pipeline with a registered model](../modules/09-model-artifacts-registry/index.md) | Green suite ≥80% coverage, seeded regression caught, model registered with lineage |
| **MP4** | Module 12 | [Automated delivery](../modules/12-cicd-github-actions/index.md) | Containerised API passing tests in CI; a broken PR is blocked |
| **MP5** | Module 14 | [Monitored system](../modules/14-monitoring-drift-retraining/index.md) | Scheduled run, injected drift detected, retraining triggered and compared |

Scoring uses the [project rubric](../syllabus/assessment-framework.md#6-project-rubric-mini-projects)
in the assessment framework.

---

## The capstone (Module 17)

A complete, self-built MLOps system for a problem you choose — data validation
through to a monitored, defensible deployment.

| Milestone | Due by | Deliverable |
|---|---|---|
| C1 Proposal | end of M06 | Problem statement, data source, success metric, risks |
| C2 Data foundation | end of M08 | Validated, versioned dataset + quality report |
| C3 Training + tracking | end of M09 | Reproducible pipeline, tracked runs, registered model |
| C4 Tested + served | end of M12 | Test suite, API, container, CI workflow |
| C5 Automated + monitored | end of M14 | Scheduled pipeline + drift monitoring + retrained model |
| C6 Governed + documented | end of M15 | Security fixes, fairness report, model card, risk register |
| C7 Defence | end of M17 | Design defence, rollback rehearsal, final evidence bundle |

**Hard conditions:** end-to-end reproducibility *and* automated quality gates must
both reach "meets", or the capstone is capped at "Developing" — see the
[capstone rubric](../syllabus/assessment-framework.md#7-capstone-rubric).

### Capstone deliverables (write your own, guided by these)

| Deliverable | What it is |
|---|---|
| [Capstone specification](capstone-specification.md) | scope, the 16 required parts, dataset rules, MVP vs extensions |
| [Task checklist](capstone-checklist.md) | C1–C7 milestones with evidence slots — copy into your repo |
| [Rubric worksheet](capstone-rubric.md) | self-scoring table with hard-condition gate and banding |
| [Self-assessment & reflection](capstone-self-assessment.md) | 17 honest reflection questions for `REFLECTION.md` |

A **complete worked reference** of all 16 parts lives in
[`examples/capstone-support/`](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/capstone-support)
— study its [walkthrough](../modules/17-capstone/worked-example.md), then
build your own problem, your own data, your own decisions.

The defence includes a **fault-injection exercise**: you break something on purpose
and recover using your own runbook. A system that has never been broken has never
been tested.

---

## Your portfolio

```
portfolio/
├── modules/          evidence per module (logs, reports, diagrams)
├── mini-projects/    MP1–MP5 as tagged states of the growing repo
├── capstone/         final system + evidence bundle
└── REFLECTION.md     what broke, what you would do differently
```

Track your milestones on the [progress checklist](../start-here/progress-checklist.md).

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*
