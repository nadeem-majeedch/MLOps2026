# Course Learning Outcomes

This page defines what a student can **do** after completing the course. Module-level
outcomes live in [detailed-syllabus.md](detailed-syllabus.md); this page is the
programme-level view that every module outcome rolls up into.

**Audience:** university students self-studying with no instructor present.
**Level:** beginner → advanced production MLOps.
**Estimated total effort:** 150–190 hours across 17 modules plus a capstone
(see [../learning-roadmap/index.md](../learning-roadmap/index.md)).

---

## How to read these outcomes

Each outcome is written to be **observable and checkable**: it names an artefact you
produce or a command you can run, so you can prove the outcome to yourself without
anyone grading you. The "evidence" column tells you exactly what to keep in your
portfolio.

Action verbs follow Bloom's taxonomy: *explain* and *describe* are knowledge-level;
*build*, *configure*, and *validate* are application-level; *design*, *compare*, and
*evaluate* are analysis-level; *integrate* and *justify* are creation/evaluation-level.

---

## Course-level outcomes (CLOs)

On completion of all modules and the capstone, you will be able to:

| ID | Outcome | Bloom level | Proof of achievement |
|---|---|---|---|
| **CLO-1** | Explain the machine-learning (ML) lifecycle and articulate why MLOps practices reduce failure risk in production ML systems | Understand | Module 01 assessment + written lifecycle diagram |
| **CLO-2** | Create a reproducible development environment and version-controlled ML project from an empty folder | Apply | Module 02 lab artefacts: repository, pinned environment, README |
| **CLO-3** | Structure an ML project to limit technical debt, and justify each structural choice | Analyse | Module 03 project: annotated repository structure |
| **CLO-4** | Validate tabular data with automated checks and version datasets so any experiment can be re-run on identical inputs | Apply | Module 04 lab: validation report + versioned dataset |
| **CLO-5** | Build a configurable, reproducible training pipeline that yields the same model from the same inputs and seed | Apply | Module 05 lab: repeated run producing identical metrics |
| **CLO-6** | Track experiments, compare runs, and evaluate models with appropriate metrics and baselines using MLflow | Apply | Module 06 lab: MLflow run history and comparison |
| **CLO-7** | Design and run a test suite for ML systems covering unit, data, model, integration, and regression tests | Apply | Module 07 lab: passing pytest suite with coverage report |
| **CLO-8** | Automate a pipeline with explicit task dependencies and reproduce it on a clean machine | Apply | Module 08 lab: one-command pipeline rebuild |
| **CLO-9** | Package a trained model, register it, and move it through staging to production with recorded lineage | Apply | Module 09 lab: registry entry with stage transitions |
| **CLO-10** | Serve a model behind a versioned REST API and verify it with automated requests | Apply | Module 10 lab: running API with documented endpoints |
| **CLO-11** | Build an immutable container image and run the same artefact locally and in a second environment | Apply | Module 11 lab: image digest and container run log |
| **CLO-12** | Configure a CI/CD workflow that tests, builds, and validates an ML change automatically | Apply | Module 12 lab: green workflow run on a pull request |
| **CLO-13** | Orchestrate scheduled and event-driven pipelines with retries, logging, and failure handling | Apply | Module 13 lab: scheduled run and a deliberately failed run |
| **CLO-14** | Monitor predictions and data, detect data and model drift, and justify a retraining decision from evidence | Evaluate | Module 14 lab: drift report + retraining trigger decision |
| **CLO-15** | Apply security, privacy, fairness, and governance controls to an ML system and document residual risk | Evaluate | Module 15 lab: secrets audit, fairness report, model card |
| **CLO-16** | Design a deployment for scaling and reliability, estimate its cost, and plan a rollback | Evaluate | Module 16 design document + local Kubernetes exercise |
| **CLO-17** | Integrate the entire lifecycle into one working system, from data to monitored deployment, and defend its trade-offs | Create/Evaluate | Module 17 capstone: system, evidence bundle, written defence |

---

## Outcome → module map

| Module | Primary CLOs | Supporting CLOs |
|---|---|---|
| 01 Introduction to MLOps and the ML lifecycle | CLO-1 | — |
| 02 Python, Git, CLI, reproducible environments | CLO-2 | CLO-1 |
| 03 Organizing an ML project, technical debt | CLO-3 | CLO-2 |
| 04 Data quality, validation, data versioning | CLO-4 | CLO-2 |
| 05 Reproducible training and pipeline design | CLO-5 | CLO-4 |
| 06 Experiment tracking and evaluation with MLflow | CLO-6 | CLO-5 |
| 07 Unit, data, model, integration, regression testing | CLO-7 | CLO-5 |
| 08 Pipeline automation and workflow dependencies | CLO-8 | CLO-7 |
| 09 Model artifacts, registries, promotion, lifecycle | CLO-9 | CLO-6, CLO-8 |
| 10 Model serving and REST APIs with FastAPI | CLO-10 | CLO-9 |
| 11 Docker images, containers, deployment environments | CLO-11 | CLO-10 |
| 12 CI/CD and ML validation with GitHub Actions | CLO-12 | CLO-7, CLO-11 |
| 13 Workflow orchestration and scheduled pipelines | CLO-13 | CLO-8, CLO-12 |
| 14 Monitoring, drift, and retraining | CLO-14 | CLO-6, CLO-13 |
| 15 Security, privacy, governance, fairness | CLO-15 | CLO-10, CLO-14 |
| 16 Cloud, Kubernetes, scaling, reliability | CLO-16 | CLO-11, CLO-13 |
| 17 Capstone: the entire lifecycle | CLO-17 | all |

---

## Essential vs. optional outcomes

- **Essential (graded path):** CLO-1 through CLO-14. Achievable entirely locally
  with free, open-source tools and a free GitHub account.
- **Advanced (stretch):** CLO-15 and CLO-16 are assessed but their most demanding
  sub-outcomes (production Kubernetes, managed-cloud deployment) are optional
  extensions marked ☁️/💲.
- **Integrative:** CLO-17 is demonstrated through the
  [capstone](course-project-map.md).

---

## Measuring your own progress

1. After each module, compare your artefacts against the module's "Evidence"
   section in the [detailed syllabus](detailed-syllabus.md).
2. Keep a portfolio folder (your own Git repository) containing every evidence item.
3. Re-run older labs occasionally — reproducibility is itself an outcome, and a
   lab that no longer reproduces is a real finding to fix.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md) for instructor credits.*
