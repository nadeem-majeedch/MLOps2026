# MLOps — A Self-Study Course for University Students

**Machine Learning Operations (MLOps)** is the set of practices that takes a machine-learning (ML) model from a laptop experiment to a system that runs reliably in production: versioned data and code, reproducible training, automated testing and deployment, monitoring, and governance.

This repository is a complete, self-study, beginner-to-advanced course in MLOps: **17 modules**, a guided laboratory in every module, progressive mini-projects, and an integrated capstone. It is written for students who will learn **on their own**, without an instructor in the room — every concept is explained before it is used, every exercise states what "done" looks like, and every laboratory includes troubleshooting guidance and a verification step.

> **Status:** **all 17 modules written in full** (lessons, worked examples, labs, challenges, knowledge checks with answers, troubleshooting, references), with a runnable reference implementation for the capstone (`examples/capstone-support/`). Follow the [learning roadmap](docs/learning-roadmap/index.md); see the [build roadmap](docs/ROADMAP.md) for contributor status.

---

## Intended audience

- **Primary:** undergraduate and graduate students who can write basic Python and want to learn how ML systems are built and operated in practice.
- **Also for:** instructors who want a ready-made lab course to adopt or adapt, and practitioners moving from modelling toward production work.
- **Not required:** prior Docker, Kubernetes, CI/CD, or cloud experience — those are taught in sequence. Entry requirements are listed in [docs/prerequisites/index.md](docs/prerequisites/index.md).

---

## What you will be able to do

On completing the course and capstone you will be able to (full list with evidence: [learning outcomes](docs/syllabus/learning-outcomes.md)):

1. Explain the ML lifecycle and why production ML systems fail without MLOps practices.
2. Build a reproducible, version-controlled ML project from an empty folder.
3. Validate and version data so any experiment can be re-run on identical inputs.
4. Train models reproducibly and track experiments with MLflow.
5. Test ML systems like software: unit, data, model, integration, and regression tests.
6. Automate pipelines with dependency-aware workflows and CI/CD on GitHub Actions.
7. Register, promote, and serve models behind a tested REST API in a container.
8. Monitor predictions for data and model drift, and justify retraining from evidence.
9. Apply security, privacy, fairness, and governance controls to an ML system.
10. Design for scaling and reliability, and integrate the entire lifecycle in a capstone.

---

## Syllabus summary

| Track | Modules | Focus | Effort |
|---|---|---|---|
| **Beginner** | 01–05 | ML lifecycle and vocabulary · Python, Git, CLI, reproducible environments · project structure and technical debt · data quality and versioning · reproducible training | ~37 h |
| **Intermediate** | 06–12 | Experiment tracking with MLflow · testing for ML · pipeline automation · model registry and promotion · FastAPI serving · Docker · CI/CD with GitHub Actions | ~61 h |
| **Advanced** | 13–17 | Orchestration and scheduling · monitoring, drift, retraining · security, privacy, governance, fairness · cloud, Kubernetes, scaling, reliability · capstone | ~64 h+ |

| Module | Title |
|---|---|
| 01 | Introduction to MLOps and the ML lifecycle |
| 02 | Python, Git, CLI, and reproducible environments |
| 03 | Organizing an ML project and understanding technical debt |
| 04 | Data quality, validation, and data versioning |
| 05 | Reproducible model training and pipeline design |
| 06 | Experiment tracking and model evaluation using MLflow |
| 07 | Unit, data, model, integration, and regression testing |
| 08 | Pipeline automation and workflow dependencies |
| 09 | Model artifacts, registries, promotion, and lifecycle management |
| 10 | Model serving and REST APIs using FastAPI |
| 11 | Docker images, containers, and deployment environments |
| 12 | CI/CD and ML validation workflows using GitHub Actions |
| 13 | Workflow orchestration and scheduled pipelines |
| 14 | Prediction monitoring, data drift, model drift, and retraining |
| 15 | Security, privacy, governance, fairness, and responsible deployment |
| 16 | Cloud deployment concepts, Kubernetes, scaling, and reliability |
| 17 | Advanced MLOps capstone integrating the entire lifecycle |

Full per-module detail — outcomes, background, vocabulary, tools, effort, laboratory scenario, challenge, assessment, dependencies, evidence, and free alternatives — is in the [detailed syllabus](docs/syllabus/detailed-syllabus.md).

---

## Course materials

| Document | What it gives you |
|---|---|
| [Site home page](docs/index.md) | The student landing page as it appears on the course website |
| [First-day guide](docs/start-here/index.md) | Exactly what to do on day one |
| [Course overview](docs/syllabus/course-overview.md) | Purpose, design principles, how a module is built |
| [Detailed syllabus](docs/syllabus/detailed-syllabus.md) | All 17 modules specified in full |
| [Learning outcomes](docs/syllabus/learning-outcomes.md) | Observable outcomes and the evidence for each |
| [Learning roadmap](docs/learning-roadmap/index.md) | Recommended order, time plan, milestones, gates |
| [Prerequisites](docs/prerequisites/index.md) | Skills, software, accounts, pre-flight checklist |
| [Tool selection guide](docs/syllabus/tool-selection-guide.md) | Every tool, why it is used, free/local alternatives |
| [Assessment framework](docs/syllabus/assessment-framework.md) | Suggested self-study assessment scheme and rubrics |
| [Course project map](docs/syllabus/course-project-map.md) | Mini-projects, capstone milestones, portfolio |
| [Standards for contributors](docs/COURSE-STANDARDS.md) | Writing, naming, and labelling conventions |
| [Learning resources](docs/resources/index.md) | Curated external reading and documentation |
| [Troubleshooting](docs/troubleshooting/index.md) | Symptom → cause → fix for common student problems |

### How to start

1. Complete the pre-flight checklist in [docs/prerequisites/index.md](docs/prerequisites/index.md).
2. Follow the study order in [docs/learning-roadmap/index.md](docs/learning-roadmap/index.md).
3. Open [Module 01](docs/modules/01-introduction-mlops-lifecycle/index.md) and work forward, keeping a portfolio of your evidence.

---

## Labels used throughout this course

Every command, task, and activity is labelled so you always know what it costs you:

| Label | Meaning |
|---|---|
| 🪟 **Windows / PowerShell** | The primary environment for this course: Windows 11 with PowerShell |
| 🐧 **Linux / macOS** | An equivalent command or step for other operating systems |
| ☁️ **Optional cloud** | Uses an external cloud service; an account is required; the course can be completed without it |
| 💲 **Paid** | Incurs a cost beyond a free tier — always optional, never required |
| ⚠️ **Resource-heavy** | Needs notable disk, memory, or CPU (or a long runtime); guidance is given |
| ✅ **Check yourself** | A verification step — run it and confirm the stated output before moving on |

Free and open-source tools and local execution are preferred everywhere. Nothing in the graded path requires a credit card.

---

## Assessment in one paragraph

Assessment is a **suggested self-study framework**, not an official university grading scheme: knowledge checks after each lesson cluster, a practical lab per module, five progressive mini-projects, and an integrated capstone — all graded with rubrics whose acceptance criteria you can check yourself. Details and weights: [assessment framework](docs/syllabus/assessment-framework.md).

---

## About the Instructor

**Engr. Dr. Muhammad Nadeem Majeed**
Professor
Department of Data Science, Punjab University College of Information Technology (PUCIT)
University of the Punjab, Lahore, Pakistan

This course is designed and maintained by Dr. Majeed as a public, self-study learning resource. Issue reports and constructive pull requests that follow [docs/COURSE-STANDARDS.md](docs/COURSE-STANDARDS.md) are welcome.

---

## License and reuse

Content in this repository is intended for free educational use. A license file will be added in a later phase; until then, ask the instructor before redistributing.
