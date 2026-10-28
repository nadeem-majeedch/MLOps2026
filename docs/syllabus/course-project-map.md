# Course Project Map

How the practical work fits together: five progressive mini-projects, one
integrated capstone, and the evidence trail that ties every module to a portfolio
artefact.

**Why a map?** Self-study fails when exercises feel like isolated chores. Every
task here is a deliberately staged piece of one continuous system, so the work you
do in Module 04 is still doing a job for you in Module 17.

---

## 1. The through-line

A single recurring organisation runs through all scenarios: **Lahore Retail Co.**,
a mid-size retailer predicting customer churn and demand. Its fictional, synthetic
datasets ship with the course (CC0), and its story is the spine of every lab.

```
Data arrives ──► validated ──► versioned ──► trained ──► tracked ──► tested
     │                                                        │
     │                                                        ▼
monitored ◄── deployed ◄── containerised ◄── served ◄── registered
```

Each module adds one arrow. The capstone asks you to draw the whole diagram for a
system **you** build.

---

## 2. Progressive mini-projects

| # | After module | Mini-project | Integrates | Key acceptance criteria |
|---|---|---|---|---|
| **MP1** | 03 | Reproducible project skeleton | 01–03 | Fresh clone + one command reproduces documented output; standard layout; README explains every folder |
| **MP2** | 06 | Tracked, justified model | 04–06 | Dataset versioned; ≥10 tracked runs; champion chosen against a baseline with stated metrics |
| **MP3** | 09 | Tested pipeline with a registered model | 07–09 | Green suite ≥80% coverage; seeded regression caught; registry entry with full lineage + model card |
| **MP4** | 12 | Automated delivery | 10–12 | Containerised API passing tests in CI; broken PR blocked by a gate; clean PR merged |
| **MP5** | 14 | Monitored system | 13–14 | Scheduled run executes; injected drift detected above threshold; retraining triggered and compared |

**Reuse rule:** each mini-project *extends* the previous one's repository rather
than starting fresh — by MP5 you should own a single repo that has grown across
the whole course. That repo becomes the capstone seed.

---

## 3. Capstone (Module 17)

### 3.1 Choice of problem
Pick a problem you can defend: a real question you care about, or one of three
provided alternatives (churn, demand forecasting, ticket triage). Constraints:

- Tabular data that fits on your laptop (⚠️ the course is CPU-only by design).
- A dataset you can legally use (synthetic, CC0, or openly licensed) with a
  dataset card.
- A measurable outcome with a baseline you can beat.

### 3.2 Milestones and evidence

| Milestone | Due by | Deliverable | Evidence |
|---|---|---|---|
| **C1 — Proposal** | end of M06 | Problem statement, data source, success metric, risks | 1-page proposal + dataset card draft |
| **C2 — Data foundation** | end of M08 | Validated, versioned dataset + quality report | Validation reports, data hashes |
| **C3 — Training + tracking** | end of M09 | Reproducible pipeline, tracked runs, registered model | Run history, config files, registry entry |
| **C4 — Tested + served** | end of M12 | Test suite, API, container, CI workflow | Green CI runs, test report, image digest |
| **C5 — Automated + monitored** | end of M14 | Scheduled pipeline + drift monitoring + retriggered retraining | Scheduler logs, drift reports, retrain comparison |
| **C6 — Governed + documented** | end of M15 | Security fixes, fairness report, model card, risk register | Scan output, fairness metrics, governance docs |
| **C7 — Defence** | end of M17 | Design defence + rollback rehearsal + final evidence bundle | Written defence (≥2 rejected alternatives), rollback log |

**C7 fault-injection exercise:** during the defence you must break something on
purpose (bad data, failing container, injected drift) and recover using your own
runbook. A system that has never been broken has never been tested.

### 3.3 Capstone grading
Use the capstone rubric in [assessment-framework.md](assessment-framework.md) §7.
Hard conditions: end-to-end reproducibility **and** automated quality gates must
both reach "meets", otherwise the result is capped at "Developing".

---

## 4. Portfolio: what you keep

One Git repository (yours) containing:

```
portfolio/
├── modules/          evidence per module (logs, reports, diagrams)
├── mini-projects/    MP1–MP5, each a tagged state of the growing repo
├── capstone/         final system + evidence bundle
└── REFLECTION.md     what broke, what you would do differently
```

Evidence types you should be able to point to for every claim: command output,
test report, coverage number, run history, registry state, CI run, drift report,
cost estimate.

---

## 5. Optional extension tracks (not graded)

| Track | After | What it adds |
|---|---|---|
| ☁️ **Cloud deployment** | M16 | Deploy the capstone to a free-tier cloud account — with a mandatory teardown checklist |
| ☁️ **Experiment-sharing** | M06 | Publish run history via a hosted tracker's free tier |
| 📊 **Dashboard polish** | M14 | Grafana dashboards for the monitoring story |
| 📝 **Public write-up** | M17 | Turn the defence into a blog-style article for your portfolio |

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*
