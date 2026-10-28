# Course Overview

A complete, self-study, beginner-to-advanced course in **Machine Learning
Operations (MLOps)** for university students — 17 modules, a guided laboratory
per module, progressive mini-projects, and an integrated capstone.

**Instructor:** Engr. Dr. Muhammad Nadeem Majeed, Professor, Department of Data
Science (PUCIT), University of the Punjab, Lahore, Pakistan.

---

## 1. What MLOps is, and why this course exists

A model that performs well in a notebook is not yet a product. **MLOps** is the
set of practices that carries a model from experiment to a system that runs
reliably: versioned data and code, reproducible training, automated tests and
deployments, monitoring for degradation, and governance over what is released and
why.

Organisations fail at this in predictable ways: unreproducible results, silent
data quality problems, models that rot unnoticed, manual deployments that break,
and nobody able to say which code produced which model. This course teaches the
practices that prevent those failures — starting from an empty folder and ending
with a monitored, deployable system.

## 2. Intended audience

- **Primary:** undergraduate or graduate university students who can write basic
  Python and want to learn how ML systems are built and operated in practice.
- **Secondary:** instructors seeking a ready-made lab course; practitioners
  moving from modelling into production work.
- **Not required:** prior Docker, Kubernetes, CI/CD, or cloud experience. Those
  are taught in sequence.

Full entry requirements: [../prerequisites/index.md](../prerequisites/index.md).

## 3. Design principles

These principles govern every module; content that violates them gets rewritten.

1. **Concepts before tooling.** Every tool is preceded by the problem it solves,
   stated in plain language first.
2. **One major new tool at a time.** A module introduces at most one significant
   tool; the rest is reinforcement and practice.
3. **Alternatives are explained, not just listed.** When a tool is chosen, the
   module says what else exists, why it exists, and when you should prefer it.
4. **No unnecessary enterprise complexity for beginners.** Early modules run
   locally with a text editor and a terminal. Distributed systems, cloud, and
   orchestration arrive only after the fundamentals are solid.
5. **Advanced modules are genuinely advanced.** Modules 13–17 assume you can
   design systems and argue trade-offs, not just follow steps.
6. **Free and local by default.** Every required activity runs on a normal
   Windows 11 laptop with free, open-source tools. Cloud, paid, and
   resource-heavy steps are always labelled (☁️ 💲 ⚠️) and always optional.
7. **Reproducibility is graded behaviour.** Seeds, versions, expected outputs,
   and cleanup are part of every lab, not optional polish.
8. **Honest labelling.** Estimates, prerequisites, and costs are stated up front
   so you can plan — never discovered halfway through.

## 4. Level structure

| Track | Modules | Focus | Typical module effort |
|---|---|---|---|
| **Beginner** | 01–05 | Vocabulary, the ML lifecycle, Python/Git/CLI foundations, project structure, data quality, reproducible training | 6–8 h |
| **Intermediate** | 06–12 | Experiment tracking, testing, pipeline automation, registries, serving, containers, CI/CD | 8–10 h |
| **Advanced** | 13–17 | Orchestration, monitoring and drift, security and governance, cloud/Kubernetes/scaling, capstone | 10–25 h |

Content within each module is further marked **essential**, **optional**, or
**advanced** so you can choose depth when time is short.

## 5. Module sequence at a glance

| # | Module | Essential tools introduced | Effort |
|---|---|---|---|
| 01 | Introduction to MLOps and the ML lifecycle | — (concepts, diagrams) | 6 h |
| 02 | Python, Git, CLI, and reproducible environments | Python, Git, PowerShell, `venv`/`uv` | 8 h |
| 03 | Organizing an ML project and understanding technical debt | Project scaffolding, notebook hygiene | 7 h |
| 04 | Data quality, validation, and data versioning | pandas, pandera, DVC | 8 h |
| 05 | Reproducible model training and pipeline design | scikit-learn pipelines, YAML config | 8 h |
| 06 | Experiment tracking and model evaluation using MLflow | MLflow | 8 h |
| 07 | Unit, data, model, integration, and regression testing | pytest, coverage | 8 h |
| 08 | Pipeline automation and workflow dependencies | Make / Snakemake, DVC pipeline | 8 h |
| 09 | Model artifacts, registries, promotion, and lifecycle management | MLflow Model Registry, model cards | 8 h |
| 10 | Model serving and REST APIs using FastAPI | FastAPI, Pydantic, uvicorn | 9 h |
| 11 | Docker images, containers, and deployment environments | Docker / Podman | 9 h |
| 12 | CI/CD and ML validation workflows using GitHub Actions | GitHub Actions, `act` | 9 h |
| 13 | Workflow orchestration and scheduled pipelines | Prefect / cron / Task Scheduler | 10 h |
| 14 | Prediction monitoring, data drift, model drift, and retraining | Evidently, Prometheus + Grafana (optional) | 10 h |
| 15 | Security, privacy, governance, fairness, responsible deployment | gitleaks, fairlearn, model cards | 10 h |
| 16 | Cloud deployment concepts, Kubernetes, scaling, reliability | kind/minikube, Terraform (concepts), scaling drills | 12 h |
| 17 | Advanced MLOps capstone integrating the entire lifecycle | All of the above | 20–25 h |

Supporting topics — feature engineering and feature stores, infrastructure as
code, secrets management, model lineage, rollback, and cost management — are
embedded in the modules where they naturally belong; see
[detailed-syllabus.md](detailed-syllabus.md) § "Supporting topics map".

## 6. How a module is built

Every module contains the same five parts, so you always know what to expect:

| Part | What it gives you |
|---|---|
| **Lessons** | Concepts and vocabulary explained before any tool appears |
| **Guided lab** | A realistic scenario with numbered steps, expected output, troubleshooting, and cleanup |
| **Independent challenge** | An open-ended task you solve without step-by-step directions |
| **Assessment** | Knowledge check plus a practical, with rubrics and measurable acceptance criteria |
| **Evidence** | Artefacts you keep in your portfolio to prove each outcome |

Templates that enforce this shape:
[labs](../TEMPLATES/LAB-TEMPLATE.md) and
[assessments](../TEMPLATES/ASSESSMENT-TEMPLATE.md).

## 7. Assessment at a glance

Assessment is a **suggested self-study framework**, not an official university
grading scheme. It gives you knowledge checks, practical labs, progressive
mini-projects, an integrated capstone, and rubrics with measurable acceptance
criteria. Full detail: [assessment-framework.md](assessment-framework.md).

## 8. Where to start

1. Complete the pre-flight checklist in
   [../prerequisites/index.md](../prerequisites/index.md).
2. Follow the study order and milestones in
   [../learning-roadmap/index.md](../learning-roadmap/index.md).
3. Open Module 01 and work forward. Keep a portfolio repository as you go.

---

## Course materials index

| Document | Purpose |
|---|---|
| [learning-outcomes.md](learning-outcomes.md) | What you will be able to do, and the evidence for it |
| [detailed-syllabus.md](detailed-syllabus.md) | Full module-by-module specification (17 modules) |
| [learning-roadmap/index.md](../learning-roadmap/index.md) | Study order, milestones, time plan |
| [prerequisites/index.md](../prerequisites/index.md) | Skills, software, accounts, pre-flight checks |
| [tool-selection-guide.md](tool-selection-guide.md) | Every tool, why it is used, and free/local alternatives |
| [assessment-framework.md](assessment-framework.md) | Suggested self-study assessment scheme and rubrics |
| [course-project-map.md](course-project-map.md) | Mini-projects and capstone structure |
| [../COURSE-STANDARDS.md](../COURSE-STANDARDS.md) | Authoring and naming standards (contributors) |
| [../ROADMAP.md](../ROADMAP.md) | Build status of the course itself (contributors) |
