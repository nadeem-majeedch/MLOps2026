# Learning Roadmap

Your study plan through the course: recommended order, time budget, milestones,
and how to keep momentum when life gets busy.

- **Total effort:** ~150–190 hours (17 modules + capstone).
- **Pace suggestion:** 6–8 hours/week → about **5 months**; 10 h/week → ~3.5 months.
- **Golden rule:** work in order. Each module assumes the previous ones.

Prerequisites and the pre-flight checklist:
[../prerequisites/index.md](../prerequisites/index.md) ·
Full module detail: [../syllabus/detailed-syllabus.md](../syllabus/detailed-syllabus.md)

---

## 1. The route at a glance

```
BEGINNER         01 ─► 02 ─► 03 ─► 04 ─► 05      foundations & reproducibility
                              │
INTERMEDIATE     06 ─► 07 ─► 08 ─► 09 ─► 10 ─► 11 ─► 12      track → test → serve → automate
                                                                    │
ADVANCED         13 ─► 14 ─► 15 ─► 16 ─► 17                      operate → secure → scale → integrate
```

Each stage has its own navigation section on this site: Foundations, Intermediate,
and Advanced — every module in a stage is listed there.

| Stage | Modules | Hours | You leave able to… |
|---|---|---|---|
| 🌱 **Beginner** (warm-up) | 01–05 | ~37 | Build a reproducible, structured, versioned training project |
| 🔧 **Intermediate** (build) | 06–12 | ~61 | Track, test, register, serve, containerise, and auto-test it |
| 🚀 **Advanced** (produce) | 13–17 | ~64+ | Schedule, monitor, secure, scale, and defend a full ML system |

---

## 2. Module-by-module plan

| # | Module | Effort | Content emphasis | Gate before moving on |
|---|---|---|---|---|
| 01 | Introduction to MLOps and the ML lifecycle | 6 h | **Essential** concepts | Annotated lifecycle diagram + quiz |
| 02 | Python, Git, CLI, reproducible environments | 8 h | **Essential** | Clean-checkout rebuild works |
| 03 | Organizing an ML project, technical debt | 7 h | **Essential** | **MP1** accepted |
| 04 | Data quality, validation, data versioning | 8 h | **Essential** | 3 extracts validated; dataset versioned |
| 05 | Reproducible training and pipeline design | 8 h | **Essential** (feature stores ⬜ optional) | Two runs produce identical metrics |
| 06 | Experiment tracking with MLflow | 8 h | **Essential** | **MP2** accepted |
| 07 | Testing for ML systems | 8 h | **Essential** | Green suite incl. regression test |
| 08 | Pipeline automation and dependencies | 8 h | **Essential** | One-command clean rebuild |
| 09 | Model artifacts, registry, promotion | 8 h | **Essential** (feature store ⬜ optional) | **MP3** accepted |
| 10 | Model serving and REST APIs (FastAPI) | 9 h | **Essential** | API tests green |
| 11 | Docker images and containers | 9 h | **Essential** | Container reproduces API tests |
| 12 | CI/CD with GitHub Actions | 9 h | **Essential** | **MP4** accepted (one blocked PR) |
| 13 | Orchestration and scheduled pipelines | 10 h | **Essential** | Scheduled run + handled failure |
| 14 | Monitoring, drift, retraining | 10 h | **Essential** | **MP5** accepted |
| 15 | Security, privacy, governance, fairness | 10 h | **Essential** (regulation depth ⬜ optional) | Five fixes demonstrated |
| 16 | Cloud, Kubernetes, scaling, reliability | 12 h | Local K8s **essential**; real cloud ☁️ **optional** | Deploy → break → heal → roll back |
| 17 | Capstone | 20–25 h | **Integrative** | Capstone rubric "meets" on hard conditions |

**Content markers:** **Essential** = graded, must-do · **Optional** = enriches,
skippable without gaps · **Advanced/optional** = stretch, safe to defer.

---

## 3. Milestones worth celebrating

| After | Milestone | What you can show |
|---|---|---|
| M02 | *"I can reproduce anything"* | A stranger can rebuild your environment |
| M06 | *"My experiments are legible"* | Run history that justifies a model choice |
| M09 | *"My model has paperwork"* | Registered model with lineage and a model card |
| M12 | *"The machine checks my work"* | CI that blocks a bad change for you |
| M14 | *"The system watches itself"* | Drift detection that triggers retraining |
| M17 | *"I built the whole thing"* | A defended, monitored, reproducible ML system |

---

## 4. Weekly rhythm (suggested)

1. **Read** the module's lessons (concept first — no tools yet).
2. **Do** the guided lab, running every ✅ checkpoint and recording output.
3. **Attempt** the independent challenge without step-by-step help.
4. **Self-assess** with the knowledge check and rubric
   ([../syllabus/assessment-framework.md](../syllabus/assessment-framework.md)).
5. **File** your evidence in the portfolio, then update this roadmap's gate.

### Laboratories and practice materials

Each module has a **guided lab** on its own page (step 2 above). In addition,
the repository ships **20 standalone laboratory exercises** — scenario-driven,
with fixtures, acceptance criteria, cleanup, and separately-stored reference
solutions — indexed by difficulty and topic in
[../labs/index.md](../labs/index.md). Knowledge-check banks, mini-project
specs, rubrics, and submission templates live under
[../assessments/](../assessments/index.md). A sensible rhythm: do the module
guided lab inside its week, and work the matching standalone lab as that
week's practice.

### If you fall behind
- Skip **optional** content first, never the guided lab.
- Do not skip gates: a module left half-verified becomes technical debt later.
- Re-entering after a break: re-run the last lab's verification step before
  continuing — it tells you what still works.

---

## 5. Health and cost warnings

- ⚠️ **Resource-heavy points:** Module 11 (several GB of images), Module 13 if you
  try Airflow, Module 16 (Kubernetes needs ~4 GB RAM). Check
  [../prerequisites/index.md](../prerequisites/index.md) before those weeks.
- 💲 **Cost:** the graded path costs nothing. Optional cloud steps always include a
  teardown checklist — read it *before* you start.
- 🕒 **Never binge before a gate.** Modules are built for 20–45 minute sessions;
  reproducibility work suffers when rushed.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*
