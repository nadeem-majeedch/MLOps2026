# Detailed Syllabus — Module by Module

The complete specification of all 17 modules: outcomes, background, vocabulary,
tools, effort, laboratory scenarios, independent challenges, assessment methods,
dependencies, expected evidence, and free/local alternatives.

**How to read this document**
- **Track:** Beginner (01–05) · Intermediate (06–12) · Advanced (13–17).
- **Effort** is total student hours for the module: lessons + guided lab +
  independent challenge + assessment. It is an estimate, not a deadline.
- Every tool listed is free and runs locally unless marked ☁️ (account needed) or
  💲 (costs money). The required path never needs either.
- Vocabulary terms are defined one-line here and in full in the course glossary
  ([glossary](../glossary/index.md)).
- Lab and assessment structure follows
  [../TEMPLATES/LAB-TEMPLATE.md](../TEMPLATES/LAB-TEMPLATE.md) and
  [../TEMPLATES/ASSESSMENT-TEMPLATE.md](../TEMPLATES/ASSESSMENT-TEMPLATE.md).

**Prerequisite to all modules:** [../prerequisites/index.md](../prerequisites/index.md).

---

## Module 01: Introduction to MLOps and the ML lifecycle

**Track:** Beginner · **Effort:** 6 h · **Depends on:** nothing (entry module) · **Next:** 02

### Learning outcomes
- LO 1.1 Describe the stages of the ML lifecycle from data acquisition to monitoring and retirement.
- LO 1.2 Explain, in plain language, why a model that works in a notebook can still fail in production.
- LO 1.3 Distinguish MLOps from DevOps and name at least five ways ML systems differ from conventional software.
- LO 1.4 Draw and annotate an end-to-end MLOps architecture diagram.

### Required background
- Basic Python literacy; no ML or operations experience required.
- Comfort reading English technical prose; terminal use is *not* required yet.

### Key concepts and vocabulary
**MLOps**, **ML lifecycle**, **training vs. inference**, **model**, **feature**,
**pipeline**, **experiment**, **reproducibility**, **technical debt**,
**concept drift**, **model registry**, **serving**, **monitoring**, **feedback loop**,
**DevOps**, **continuous integration/deployment** (defined at overview level only).

### Tools and why they are used
| Tool | Why |
|---|---|
| A worked example repository (small, public, read-only) | Real code makes abstract failure modes concrete |
| Any diagram tool (draw.io, Excalidraw, pen & paper) | Drawing the architecture is the learning activity |

### Guided laboratory scenario
**Lab 01 — Autopsy of a failed model launch.** You are handed the story, artifacts,
and incident timeline of a fictional "loan-approval model" that decayed silently in
production. Read the provided logs and metric snapshots, annotate the lifecycle
diagram with where each failure originated, and produce a one-page incident summary.
✅ Verification: your summary names at least three distinct root causes, each tied
to a lifecycle stage.

### Independent practical challenge
Find a public postmortem or paper about an ML system failure and write a 400-word
analysis mapping it onto the lifecycle diagram from the lessons.

### Assessment method
Knowledge check (10 short-answer questions on vocabulary and lifecycle stages) +
the graded annotated diagram.

### Evidence to produce
Annotated lifecycle diagram (image or markdown), incident summary, glossary entries
for every new term.

### Free / local alternative
Entirely offline: all scenario material ships with the module. No accounts, no
downloads beyond the repository itself.

---

## Module 02: Python, Git, CLI, and reproducible environments

**Track:** Beginner · **Effort:** 8 h · **Depends on:** 01 · **Next:** 03

### Learning outcomes
- LO 2.1 Navigate a project folder and run programs from PowerShell (🪟) and bash (🐧).
- LO 2.2 Create and activate an isolated Python environment and pin installed package versions.
- LO 2.3 Use Git to snapshot work, inspect history, and branch for an experiment.
- LO 2.4 Reproduce a colleague's result from a fresh clone using only the recorded setup.

### Required background
- Variables, functions, loops, and simple classes in Python; willingness to type commands.

### Key concepts and vocabulary
**CLI/shell**, **PowerShell**, **path**, **virtual environment**, **dependency**,
**lock file**, **version control**, **commit**, **branch**, **merge conflict**,
**`.gitignore`**, **reproducible environment**, **package**, **semantic versioning**.

### Tools and why they are used
| Tool | Why |
|---|---|
| Python 3.10–3.12 | Course language; small, free, ubiquitous |
| PowerShell 5.1/7 (🪟 primary), bash (🐧 alt) | Built into the platforms; no extra install |
| Git + a GitHub account (free) | Universal version control; later CI modules need it |
| `venv` (built in) and `uv` (fast, free) | Two ways to isolate dependencies; `uv` is the modern default, `venv` the standard fallback |
| VS Code (or any editor) | Free, first-class Python + terminal support |

### Guided laboratory scenario
**Lab 02 — Rebuild a teammate's environment.** Given only a Git repository with
`pyproject.toml`/lock file and a README, clone it, create the environment, run the
script, and fix two deliberate breakages (a missing dependency, an ignored file
that should have been committed). ✅ Verification: the script prints its recorded
expected output; `git status` is clean.

### Independent practical challenge
Take an old analysis script of your own: move it into a new Git repository, pin its
dependencies, add a sensible `.gitignore`, and have a classmate (or yourself on
another machine) reproduce it from scratch.

### Assessment method
Practical lab (graded on reproducibility of the rebuild) + 8-question knowledge
check on Git and environment vocabulary.

### Evidence to produce
Git repository with meaningful history, pinned environment file, README with
reproduction steps, lab report of the two fixes.

### Free / local alternative
Everything is free and local. GitHub is the only account; a local `git init`
without any hosting works for grading purposes if you prefer no account.

---

## Module 03: Organizing an ML project and understanding technical debt

**Track:** Beginner · **Effort:** 7 h · **Depends on:** 02 · **Next:** 04

### Learning outcomes
- LO 3.1 Apply a standard ML repository layout (data, src, notebooks, models, tests, docs).
- LO 3.2 Classify examples of ML technical debt (data dependencies, entanglement, undeclared consumers, configuration debt).
- LO 3.3 Convert an exploratory notebook into a maintainable project without losing results.
- LO 3.4 Justify each structural decision in a short design note.

### Required background
- Module 02 (Git, CLI, environments) completed; basic Python.

### Key concepts and vocabulary
**Technical debt**, **entanglement**, **hidden feedback loop**,
**undeclared data dependency**, **notebook hygiene**, **separation of concerns**,
**configuration vs. code**, **reproducible entry point**, **data dictionary**.

### Tools and why they are used
| Tool | Why |
|---|---|
| Cookiecutter-style project template (free) | Gives a proven layout; the module teaches *why* each folder exists |
| `jupytext` or `nbstripout` (free) | Keeps notebooks reviewable in Git (no output noise) |
| Git, VS Code | Continuation of Module 02 |

### Guided laboratory scenario
**Lab 03 — Rescue the spaghetti notebook.** You inherit a single 400-cell notebook
that trains a model and prints "accuracy = 0.91". Restructure it into a proper
project: `src/` modules, a config file, a data folder, a `run.py` entry point, and
a README. ✅ Verification: `python run.py` reproduces 0.91 from a clean checkout.

### Independent practical challenge
Write a one-page "technical debt audit" of any ML code you have (or a provided
sample): list each debt item, its cause, its cost, and a staged fix.

### Assessment method
Graded repository restructuring against the rubric in
[assessment-framework.md](assessment-framework.md) (reproducibility, structure,
documentation) + short-answer debt classification quiz.

### Evidence to produce
Restructured repository, design note justifying the layout, debt audit list.

### Free / local alternative
All tools free and local; no account beyond optional Git hosting.

---

## Module 04: Data quality, validation, and data versioning

**Track:** Beginner · **Effort:** 8 h · **Depends on:** 02, 03 · **Next:** 05

### Learning outcomes
- LO 4.1 Write automated schema and statistical checks for a tabular dataset.
- LO 4.2 Detect and report common data problems: missing values, type drift, out-of-range values, duplicate keys, train/serving skew.
- LO 4.3 Version a dataset so an experiment can be re-run on byte-identical inputs.
- LO 4.4 Document a dataset's source, licence, and known limitations.

### Required background
- pandas basics; Git; Module 02–03 completed.

### Key concepts and vocabulary
**Data validation**, **schema**, **data drift vs. schema violation**,
**dataset versioning**, **data lineage**, **immutable data snapshot**,
**train/serve skew**, **data contract**, **dataset card**.

### Tools and why they are used
| Tool | Why |
|---|---|
| pandas | Ubiquitous tabular analysis, free |
| **pandera** (primary) | Fast, typed, code-first schema validation that drops into pytest |
| Great Expectations (alternative, free OSS) | Richer reports and suites — heavier setup; explained as "when you outgrow pandera" |
| **DVC** (Data Version Control, free OSS) | Versions datasets and pipelines with Git-like semantics without storing data in Git |
| Git LFS / plain checksums | Minimal fallback to explain the mechanics of data versioning |

### Guided laboratory scenario
**Lab 04 — Gate the incoming dataset.** A fictional retailer's daily sales extract
arrives as CSV. You write validation rules (columns, types, ranges, key uniqueness),
run them against three provided extracts — one good, two corrupted — and version
the clean extract with DVC. ✅ Verification: validation fails loudly on the two bad
extracts with human-readable messages; `dvc repro`/checkout restores the identical
file hash.

### Independent practical challenge
Define a data contract for a dataset of your choosing: schema, quality thresholds,
licence, and a versioning policy — then implement it and break it on purpose.

### Assessment method
Practical lab (validation suite catches all seeded defects) + knowledge check on
versioning and lineage concepts.

### Evidence to produce
Validation script and its pass/fail reports for three extracts, versioned dataset
with recorded hash, dataset card.

### Free / local alternative
DVC works fully offline with local storage as the "remote"; no cloud bucket
required. Cloud remotes (☁️) are shown only as an optional extension.

---

## Module 05: Reproducible model training and pipeline design

**Track:** Beginner · **Effort:** 8 h · **Depends on:** 04 · **Next:** 06

### Learning outcomes
- LO 5.1 Build a training pipeline with separated stages: validate data → features → train → evaluate → persist.
- LO 5.2 Control an experiment entirely from configuration (YAML), including the random seed.
- LO 5.3 Demonstrate reproducibility by producing identical metrics from two independent runs.
- LO 5.4 Engineer simple features and explain why feature definitions must live in code, not notebooks.

### Required background
- scikit-learn-level modelling familiarity (train/test split, accuracy), pandas, Git.

### Key concepts and vocabulary
**Pipeline**, **preprocessing vs. training step**, **random seed**,
**configuration file**, **feature engineering**, **feature leakage**,
**cross-validation vs. holdout**, **baseline model**, **model persistence (joblib)**,
**evaluation metrics**.

### Tools and why they are used
| Tool | Why |
|---|---|
| scikit-learn | Small, fast, CPU-only, ideal for teaching pipeline mechanics |
| `sklearn.pipeline.Pipeline` | Encodes the whole training path so preprocessing cannot leak |
| YAML + a typed config loader | Makes runs reproducible and diffable; Hydra introduced as the "next step up" |
| joblib / pickle | Standard model serialization at this stage; ONNX mentioned as an interoperability option |

### Guided laboratory scenario
**Lab 05 — Same seed, same model.** Build a configurable training pipeline for a
churn dataset (synthetic, CC0). Run it twice from a clean checkout with the same
config and compare metrics and model hashes; then change one config value and show
the expected difference. ✅ Verification: run A and run B metrics match to the
recorded tolerance; the divergence run differs.

### Independent practical challenge
Add a new feature to the pipeline behind a config flag, justify the change in two
paragraphs, and prove that disabling the flag restores the original results.

### Assessment method
Practical lab graded on demonstrated reproducibility + short rubric-scored design
note + knowledge check on leakage and seeds.

### Evidence to produce
Config files, pipeline code, side-by-side run outputs with hashes, feature change note.

### Free / local alternative
Entirely local and CPU-only; no accounts. Optional cloud training (☁️) is discussed
but never required.

---

## Module 06: Experiment tracking and model evaluation using MLflow

**Track:** Intermediate · **Effort:** 8 h · **Depends on:** 05 · **Next:** 07

### Learning outcomes
- LO 6.1 Instrument a training run to log parameters, metrics, artifacts, and source version.
- LO 6.2 Compare runs, identify the best configuration, and justify the choice beyond a single metric.
- LO 6.3 Evaluate against a baseline with appropriate metrics for the problem type and class balance.
- LO 6.4 Run an MLflow tracking server locally and browse its UI.

### Required background
- Modules 04–05; basic statistics (precision/recall/accuracy).

### Key concepts and vocabulary
**Experiment tracking**, **run**, **parameter vs. metric vs. artifact**,
**baseline**, **metric selection**, **overfitting vs. underfitting**,
**model lineage**, **MLflow tracking server**, **experiment comparison**,
**artifact store**.

### Tools and why they are used
| Tool | Why |
|---|---|
| **MLflow Tracking** (free OSS) | Standard, Python-native, runs fully locally with a SQLite backend |
| scikit-learn continuation | Keeps the modelling load low so attention stays on tracking |
| Optional: Optuna for hyperparameter search (free OSS) | Shows automated search once manual comparison is understood |

**Why MLflow and not a hosted tracker?** Hosted trackers (Weights & Biases ☁️,
Neptune ☁️) are convenient but require accounts and limit data privacy; MLflow gives
the same concepts locally. The module explains when a hosted tracker becomes worth it.

### Guided laboratory scenario
**Lab 06 — Ten runs, one decision.** Run a small hyperparameter sweep over the
Module 05 pipeline, all tracked in MLflow. Produce a comparison table, pick a
champion, and defend it against a challenger that scores higher on accuracy but
worse on the metric that matters for the business case. ✅ Verification: the
tracking UI shows ≥10 runs with parameters, metrics, and artifacts; your write-up
justifies the choice with evidence.

### Independent practical challenge
Re-run your best configuration from Module 05's clean checkout and confirm the
logged metric reproduces within tolerance — then explain any discrepancy.

### Assessment method
Practical lab (tracking complete and correct) + graded evaluation rationale
(rubric: metric choice, baseline comparison, conclusion supported by data).

### Evidence to produce
MLflow run history (export/screenshot), comparison table, one-page model selection memo.

### Free / local alternative
MLflow local server — free, no account. Hosted trackers appear only as ☁️
alternatives with their trade-offs.

---

## Module 07: Unit, data, model, integration, and regression testing

**Track:** Intermediate · **Effort:** 8 h · **Depends on:** 05, 06 · **Next:** 08

### Learning outcomes
- LO 7.1 Write unit tests for the functions in an ML pipeline, including failure-path tests.
- LO 7.2 Write data tests (schema, distribution sanity) and model tests (performance floors, invariance).
- LO 7.3 Build an integration test that runs a miniature end-to-end pipeline.
- LO 7.4 Add a regression test that fails when a metric degrades beyond a threshold, and use coverage to find untested code.

### Required background
- Modules 02–06; willingness to read Python tracebacks.

### Key concepts and vocabulary
**Unit test**, **data test**, **model test**, **integration test**,
**regression test**, **test fixture**, **coverage**, **performance floor**,
**invariance/robustness test**, **deterministic vs. flaky test**, **CI-ready suite**.

### Tools and why they are used
| Tool | Why |
|---|---|
| **pytest** (free OSS) | De-facto standard; fixtures map neatly onto datasets |
| `pytest-cov` | Coverage numbers you can act on |
| pandera (from Module 04) | Reused for data tests — one tool, deepened |
| Deepchecks / Great Expectations | Named as richer alternatives when suites grow |

### Guided laboratory scenario
**Lab 07 — Build the safety net.** Take the Module 05 pipeline and build a layered
test suite: 6+ unit tests, 3 data tests, 2 model tests (including a performance
floor), 1 integration test, and 1 deliberately failing regression test that you then
fix. ✅ Verification: `pytest` passes green with the failing test removed from the
expectations; coverage report attached.

### Independent practical challenge
Break the pipeline in three subtle ways (silent type coercion, shuffled labels,
leaky feature) and show which of your tests catches each — and add a test for any
that slip through.

### Assessment method
Practical lab graded against measurable criteria (test counts by type, green run,
coverage ≥ a stated target, all three seeded bugs caught) + knowledge check.

### Evidence to produce
Test suite, coverage report, bug-catch matrix (bug → test that caught it).

### Free / local alternative
Entirely local and free; no accounts.

---

## Module 08: Pipeline automation and workflow dependencies

**Track:** Intermediate · **Effort:** 8 h · **Depends on:** 07 · **Next:** 09

### Learning outcomes
- LO 8.1 Express a multi-stage ML workflow as declared tasks with explicit inputs, outputs, and dependencies.
- LO 8.2 Re-run only the stages whose inputs changed (incremental execution).
- LO 8.3 Recover from a failed stage and prove the workflow resumes correctly.
- LO 8.4 Rebuild the entire pipeline from scratch on a clean machine with one command.

### Required background
- Modules 02–07; basic command line.

### Key concepts and vocabulary
**Task dependency**, **DAG (directed acyclic graph)**, **incremental rebuild**,
**caching/intermediate artifacts**, **idempotency**, **build target**,
**pipeline as code**, **environment parity**.

### Tools and why they are used
| Tool | Why |
|---|---|
| **Make** (primary; free) | Tiny, universal, dependency thinking made explicit |
| **Snakemake** (free OSS) | Same idea with bio/data-science-friendly rules — explained as the scalable variant |
| **DVC pipeline** (free OSS, from Module 04) | Ties dependency graphs to data versions — the ML-specific option |
| `python -m` scripts | Fallback showing that "a pipeline" can just be disciplined scripts |

**Why this order?** Make teaches the mental model in 30 lines; heavier orchestrators
arrive properly in Module 13.

### Guided laboratory scenario
**Lab 08 — One command to rebuild everything.** Declare the validate → features →
train → evaluate → report workflow as a dependency graph. Modify a raw data file and
show that only downstream stages re-run; then delete all intermediate artefacts and
rebuild from zero. ✅ Verification: `make all` (🪟/🐧 equivalent shown) completes
with the recorded final report hash.

### Independent practical challenge
Add a new stage (e.g., a fairness report) to the dependency graph and demonstrate
correct incremental behaviour when the config, the data, and the code change.

### Assessment method
Practical lab (clean rebuild + incremental correctness + failure recovery) +
knowledge check on DAGs and idempotency.

### Evidence to produce
Build file, logs of the three runs (incremental, full rebuild, failure recovery),
final artefact hashes.

### Free / local alternative
All options free and local; no accounts.

---

## Module 09: Model artifacts, registries, promotion, and lifecycle management

**Track:** Intermediate · **Effort:** 8 h · **Depends on:** 06, 08 · **Next:** 10

### Learning outcomes
- LO 9.1 Package a model with everything needed to use it (weights, preprocessing, metadata, signature).
- LO 9.2 Register a model and record its lineage: data version, code commit, parameters, metrics.
- LO 9.3 Promote a model through staging to production using an explicit, reversible transition.
- LO 9.4 Write a model card covering intended use, limitations, and evaluation.

### Required background
- Modules 05–08 (tracking, testing, pipelines).

### Key concepts and vocabulary
**Model artifact**, **bundle/package**, **model registry**, **stage**
(Staging/Production/Archived), **promotion**, **rollback**, **lineage/provenance**,
**model card**, **serving signature**, **semantic versioning of models**,
**feature store (concept)**.

### Tools and why they are used
| Tool | Why |
|---|---|
| **MLflow Model Registry** (free, local) | Continues Module 06's stack; registry + lineage in one place |
| joblib/sklearn flavour, ONNX (mentioned) | Formats and their trade-offs |
| Model card template (free) | Documentation that travels with the model |
| DVC/`dvc.yaml` | Alternative lightweight "registry" for file-level versioning |

**Feature stores** are introduced here as *optional* content: what they solve
(consistency between training and serving features), why small teams usually start
without one, and which free options exist.

### Guided laboratory scenario
**Lab 09 — Ship v1, prepare the rollback.** Register your Module 06 champion model,
promote it to Staging, verify it loads and predicts, promote to Production, then
practise a rollback to the previous version after a simulated defect is discovered.
✅ Verification: registry shows the stage history; a consumer script resolves
"Production" and returns the expected predictions for both versions.

### Independent practical challenge
Produce a complete lineage record for your model (data hash → commit → run ID →
registry version) and a model card reviewed against the rubric in
[assessment-framework.md](assessment-framework.md).

### Assessment method
Practical lab (promotion and rollback executed correctly) + graded model card +
knowledge check on registry lifecycle.

### Evidence to produce
Registry stage history, lineage record, model card, rollback test output.

### Free / local alternative
MLflow registry runs locally with a SQLite backend — free, no account. Hosted
registries (Databricks, AWS SageMaker Model Registry ☁️/💲) appear only for contrast.

---

## Module 10: Model serving and REST APIs using FastAPI

**Track:** Intermediate · **Effort:** 9 h · **Depends on:** 09 · **Next:** 11

### Learning outcomes
- LO 10.1 Expose a registered model through a versioned REST API with input validation and clear error responses.
- LO 10.2 Distinguish batch, online (synchronous), and streaming inference and justify the choice for a scenario.
- LO 10.3 Test the API automatically, including malformed-input and latency checks.
- LO 10.4 Measure and report throughput/latency of your endpoint honestly.

### Required background
- Modules 02, 09; HTTP basics (what a request/response is).

### Key concepts and vocabulary
**REST**, **endpoint**, **request/response**, **status code**, **payload/schema**,
**synchronous vs. batch inference**, **latency vs. throughput**, **p95 latency**,
**API versioning**, **health check**, **graceful failure**.

### Tools and why they are used
| Tool | Why |
|---|---|
| **FastAPI** (free OSS) | Automatic validation and docs from type hints; teaches good API habits by default |
| Pydantic | Validation as declarations, not hand-written checks |
| uvicorn | ASGI server that runs it locally |
| `httpx`/`pytest` `TestClient` | Automated tests from Module 07, reused |
| Flask (alternative) | Explained: older, simpler, no built-in validation/docs — trade-off discussion |

### Guided laboratory scenario
**Lab 10 — Serve a trained model to an application.** Build `/predict`, `/health`,
and `/model-info` endpoints for the Module 09 model, with schema validation and a
documented error body. Write automated tests for good input, missing fields,
wrong types, and an empty batch. ✅ Verification: all tests pass; OpenAPI docs
load locally; your own measured p50/max latency is recorded with a caveat.

### Independent practical challenge
Implement a batch prediction mode (CSV in → CSV out), compare its cost profile with
the online endpoint for 100k rows, and recommend which to use and why.

### Assessment method
Practical lab (endpoint correctness + test suite + measured latency) + short
design justification (rubric-scored).

### Evidence to produce
API source, test output, endpoint documentation, latency/throughput measurements.

### Free / local alternative
Runs entirely locally; no account. ☁️ options (managed endpoints) are discussed only
in Module 16.

---

## Module 11: Docker images, containers, and deployment environments

**Track:** Intermediate · **Effort:** 9 h · **Depends on:** 10 · **Next:** 12

### Learning outcomes
- LO 11.1 Write a Dockerfile that packages the Module 10 API with its exact dependencies.
- LO 11.2 Explain images, containers, layers, tags, and digests — and why "it works on my machine" ends.
- LO 11.3 Build, run, stop, and inspect containers; read logs; persist data deliberately.
- LO 11.4 Reproduce the service in a second environment from the image alone.

### Required background
- Module 10 (a working API); Module 02 command line.

### Key concepts and vocabulary
**Image vs. container**, **layer**, **tag vs. digest**, **Dockerfile**,
**base image**, **build context**, **volume/bind mount**, **port mapping**,
**container registry (concept)**, **12-factor app**, **environment parity**,
**image scanning (concept)**.

### Tools and why they are used
| Tool | Why |
|---|---|
| **Docker** (free for students/small use) | Industry standard; WSL 2 backend on Windows 11 |
| **Podman** (free OSS, daemonless, rootless) | The no-cost-alternative path if Docker Desktop licensing or installation is a problem |
| docker compose | Multi-service local runs (API + tracking server) |
| Hadolint (free) | Lints Dockerfiles — a first taste of automated review |

### Guided laboratory scenario
**Lab 11 — Same bytes, two places.** Containerise the Module 10 API, record the
image digest, run it locally and verify the API tests pass against the container;
then delete the local environment and rebuild from the image alone. ✅ Verification:
identical test results, recorded digest, container health check passing.

### Independent practical challenge
Shrink the image (multi-stage build or slim base) and quantify the improvement in
size and startup time; note the trade-offs you introduced.

### Assessment method
Practical lab (build + run + reproducibility) + knowledge check on image mechanics +
graded size-optimisation note.

### Evidence to produce
Dockerfile with comments, image digest, container run/test logs, before/after size figures.

### Free / local alternative
Docker is free here; **Podman** is the fully free/open, licence-safe substitute —
all exercises are written to work with either. No cloud registry is required; a
local registry is demonstrated instead (☁️ alternatives noted).

---

## Module 12: CI/CD and ML validation workflows using GitHub Actions

**Track:** Intermediate · **Effort:** 9 h · **Depends on:** 07, 11 · **Next:** 13

### Learning outcomes
- LO 12.1 Build a CI workflow that runs linting, tests, and data/model validation on every push and pull request.
- LO 12.2 Add an ML validation job (performance floor, data checks) that blocks a bad model from merging.
- LO 12.3 Add a build/publish job for container images with sensible caching and versioning.
- LO 12.4 Diagnose a failing workflow from its logs and fix it.

### Required background
- Modules 07 (pytest) and 11 (containers); a GitHub account (free).

### Key concepts and vocabulary
**Continuous integration (CI)**, **continuous delivery/deployment (CD)**,
**workflow/job/step**, **runner**, **trigger/event**, **pull request gate**,
**cache**, **artifact vs. artifact upload**, **secret**, **environment protection**,
**rollback (CI/CD view)**, **MLOps validation gate**.

### Tools and why they are used
| Tool | Why |
|---|---|
| **GitHub Actions** (free for public repos) | The repository's natural CI; YAML workflows |
| **`act`** (free OSS) | Runs workflows locally in containers — the local/no-account equivalent |
| pytest, pandera, MLflow | Existing gates reused — CI is orchestration, not new tooling |
| Ruff (free) | Fast lint/format gate |

### Guided laboratory scenario
**Lab 12 — Block a defective model release.** Wire your lint, test suite, and ML
validation gate into a pull-request workflow. Run every job's commands locally,
then cause each failure on purpose (lint, test, ML gate) and watch each blocked.
✅ Verification: one red run per layer, each diagnosed from its log, followed by
a green run you produced by fixing the cause.

### Independent practical challenge
Add a scheduled nightly validation run, and a matrix build across two Python
versions — then explain in writing what each costs in runner minutes.

### Assessment method
Practical lab (two observable PR outcomes + a fixed red build) + knowledge check on
CI/CD vocabulary and secrets.

### Evidence to produce
Workflow YAML, run histories (one failed, one passed), analysis of the failure and fix.

### Free / local alternative
Public repositories get free Actions minutes; `act` gives a fully local run with no
account. GitLab CI/Gitea are named as equivalents if GitHub is unavailable (☁️).

---

## Module 13: Workflow orchestration and scheduled pipelines

**Track:** Advanced · **Effort:** 10 h · **Depends on:** 08, 12 · **Next:** 14

### Learning outcomes
- LO 13.1 Convert the Module 08 build graph into an orchestrated workflow with retries, timeouts, and logging.
- LO 13.2 Schedule daily/weekly runs and trigger a run from an event.
- LO 13.3 Handle failure deliberately: alerting, dead-letter behaviour, idempotent re-runs.
- LO 13.4 Compare orchestrators (Airflow vs. Prefect vs. Dagster vs. hosted) and justify a choice for a given context.

### Required background
- Modules 08 (dependencies) and 12 (automation); Python.

### Key concepts and vocabulary
**Orchestrator**, **schedule/trigger**, **backfill**, **retry policy**,
**timeout**, **idempotent re-run**, **task state/observability**, **concurrency**,
**secrets in orchestration**, **managed vs. self-hosted**.

### Tools and why they are used
| Tool | Why |
|---|---|
| **Windows Task Scheduler / cron (🐧)** | The zero-dependency baseline everyone should understand first |
| **Prefect** (free OSS, local server) | Python-native, gentle learning curve for the primary path |
| Apache Airflow (free OSS) | Industry reference — ⚠️ heavier (Docker, ~2 GB+), presented as the "when teams grow" option |
| Dagster (free OSS) | Asset-centric alternative, discussed in the comparison |

### Guided laboratory scenario
**Lab 13 — A pipeline that runs itself.** Schedule the Module 08 pipeline to run
nightly with Prefect (or Task Scheduler at baseline), inject a failure, observe
retries and the alert, then re-run safely. ✅ Verification: two consecutive scheduled
runs complete; the injected failure is logged, retried, and reported; re-run produces
no duplicated outputs.

### Independent practical challenge
Design the orchestration for a two-stage system (hourly scoring, weekly retraining)
on paper — triggers, retries, backfill, and failure policy — then implement the
cheapest version of it locally.

### Assessment method
Practical lab (scheduled success + handled failure + safe re-run) + graded design
comparison (rubric: criteria justified, trade-offs stated).

### Evidence to produce
Workflow definitions, scheduler logs showing success/failure/retry, comparison memo.

### Free / local alternative
Task Scheduler/cron and local Prefect are free and account-free. ☁️ managed
orchestrators (Cloud Composer, Azure Data Factory 💲) are contrast only.

---

## Module 14: Prediction monitoring, data drift, model drift, and retraining

**Track:** Advanced · **Effort:** 10 h · **Depends on:** 09, 13 · **Next:** 15

### Learning outcomes
- LO 14.1 Instrument predictions and inputs for monitoring: what to log, at what rate, and why.
- LO 14.2 Detect data (covariate) drift and concept/performance drift with defensible thresholds.
- LO 14.3 Distinguish drift from seasonal variation, sampling noise, and measurement change.
- LO 14.4 Trigger and evaluate a retraining run from monitoring evidence, and decide when *not* to retrain.

### Required background
- Modules 06 (metrics), 09 (registry), 13 (scheduled runs); basic statistics.

### Key concepts and vocabulary
**Prediction monitoring**, **data/covariate drift**, **concept drift**,
**label drift**, **performance decay**, **baseline window**, **threshold/alert**,
**PSI/KS/JS divergence (concept level)**, **retraining trigger**, **champion/challenger**,
**feedback loop**, **monitoring coverage**.

### Tools and why they are used
| Tool | Why |
|---|---|
| **Evidently AI** (free OSS) | Drift reports from pandas dataframes in minutes, fully local |
| scikit-learn + saved baselines | Reference distributions from Module 06 runs |
| Prometheus + Grafana (free OSS) | ⚠️ Optional deep dive for live metric dashboards; runs locally |
| MLflow | Logs retraining runs and links them to the drift event |

### Guided laboratory scenario
**Lab 14 — Catch the drift, then decide like an engineer.** Instrument predictions,
snapshot a reference, inject a synthetic distribution shift, and generate drift
and performance reports; then produce decisions for both the
drift-without-degradation case and the degraded case, with thresholds cited.
✅ Verification: two decision memos (MONITOR and RETRAIN CANDIDATE) citing
measured numbers, plus the rehearsed rollback precondition.

### Independent practical challenge
Build a "false alarm" case: data that looks like drift but is a known seasonal
pattern — then design the control that tells them apart.

### Assessment method
Practical lab (two detections + evidence-based decision) + graded retraining memo
(rubric: correct diagnosis, threshold justification, cost-aware recommendation).

### Evidence to produce
Drift reports, threshold configuration, retraining run comparison, decision memo.

### Free / local alternative
Evidently, MLflow, and local Prometheus/Grafana are all free and account-free.
Hosted monitoring (Grafana Cloud ☁️, Datadog 💲) appears only as a comparison.

---

## Module 15: Security, privacy, governance, fairness, and responsible deployment

**Track:** Advanced · **Effort:** 10 h · **Depends on:** 10, 14 · **Next:** 16

### Learning outcomes
- LO 15.1 Find and fix the common security failures in an ML service: leaked secrets, unauthenticated endpoints, unsafe deserialization, prompt/input injection into preprocessing.
- LO 15.2 Apply privacy basics: minimisation, anonymisation/pseudonymisation, and what must never be logged.
- LO 15.3 Measure group fairness on a test case, interpret the result, and state its limits.
- LO 15.4 Produce governance artefacts: model card, data sheet, risk register, and an audit trail.

### Required background
- Modules 10–12; awareness that personal data exists and is regulated.

### Key concepts and vocabulary
**Threat model**, **secrets vs. configuration**, **least privilege**,
**input validation**, **unsafe deserialization/pickle**, **PII**,
**data minimisation**, **anonymisation**, **fairness metric**,
**bias vs. variance (social sense)**, **model card**, **datasheet**,
**audit trail/lineage**, **responsible release**, **GDPR/Act overview (concepts only)**.

### Tools and why they are used
| Tool | Why |
|---|---|
| **gitleaks** (free OSS) | Scans history for committed secrets — immediately actionable |
| Python `secrets`/`keyring`, `.env` patterns | Correct local secret handling |
| **fairlearn** (free OSS) | Group fairness metrics in plain pandas/Python |
| Model card + datasheet templates | The documentation layer of governance |
| GitHub Actions secret scanning | Shows the CI enforcement point (free) |

### Guided laboratory scenario
**Lab 15 — Audit before someone else does.** Given a deliberately flawed ML service
(hard-coded API key in history, PII in logs, no auth check, unsafe `pickle.load`,
unfair outcome across groups), you: scan for secrets and purge them, stop logging
PII, add authentication to the endpoint, replace unsafe loading, and quantify the
fairness gap — then write a risk register of what remains. ✅ Verification: secret
scan is clean, tests confirm the endpoint rejects unauthenticated calls, fairness
report and risk register delivered.

### Independent practical challenge
Write an incident-response runbook for your own capstone system: what to do if the
model leaks data, degrades, or is queried maliciously — including rollback steps.

### Assessment method
Practical lab (five fixes demonstrated by re-running checks) + graded risk register
and model card + knowledge check on privacy and fairness concepts.

### Evidence to produce
Clean secret-scan report, auth tests, fairness report, model card, risk register.

### Free / local alternative
All tools free and local. Legal texts are described conceptually — the course gives
informational context, not legal advice. Cloud compliance services are ☁️ and optional.

---

## Module 16: Cloud deployment concepts, Kubernetes, scaling, and reliability

**Track:** Advanced · **Effort:** 12 h · **Depends on:** 11, 13 · **Next:** 17

### Learning outcomes
- LO 16.1 Explain core cloud models (IaaS/PaaS/serverless, regions, managed services) and map each course technique to its managed equivalent.
- LO 16.2 Deploy the containerised API to a local Kubernetes cluster and reason about deployments, services, replicas, and rollouts.
- LO 16.3 Design for scaling and reliability: horizontal scaling, health checks, autoscaling, graceful degradation, rollback.
- LO 16.4 Estimate the cost of a small production deployment and name the levers that control it.
- LO 16.5 (Optional ☁️) Apply infrastructure-as-code principles to a real free-tier account.

### Required background
- Modules 11 (containers) and 13 (scheduled workflows); Module 12 recommended.

### Key concepts and vocabulary
**IaaS/PaaS/serverless**, **region/zone**, **managed service**, **container
orchestration**, **pod/deployment/service/ingress**, **replica**, **rolling update**,
**autoscaling (HPA)**, **health probe**, **SLA/SLO/SLI**, **graceful degradation**,
**blue/green & canary**, **rollback**, **infrastructure as code (IaC)**,
**statelessness**, **cost drivers**.

### Tools and why they are used
| Tool | Why |
|---|---|
| **kind** or **minikube** (free OSS) | A real Kubernetes API on your laptop — no cloud account |
| `kubectl` | The universal control interface |
| Docker Compose | Contrast case: when orchestration is overkill |
| **Terraform** (free OSS) | IaC concepts; applied only against local or free-tier providers, or used read-only |
| Cloud provider free tiers ☁️/💲 | AWS/GCP/Azure demonstrations as *optional* modules with hard cost warnings |

### Guided laboratory scenario
**Lab 16 — Run it like a service.** Deploy the Module 11 image to a local kind
cluster with 2 replicas, health probes, and a rolling update; then break the
container and watch the self-healing behaviour. Measure the update as a rollout and
practise a rollback. ⚠️ Resource-heavy: Kubernetes needs ~4 GB RAM and several GB
of disk. ✅ Verification: pods reach ready state, an injected crash is replaced,
rollout rollback restores the previous version.

### Independent practical challenge
Write a one-page scaling and cost plan for serving 100 requests/second: replica
counts, resource limits, likely monthly cost with a published price sheet, and two
ways to halve that cost.

### Assessment method
Practical lab (deploy, break, heal, roll back) + graded design/cost document +
knowledge check on cloud and reliability vocabulary.

### Evidence to produce
Manifests, `kubectl` transcripts, rollout/rollback evidence, cost estimate.

### Free / local alternative
kind/minikube + Compose cover the whole graded path locally. Real cloud deployment is
**☁️ optional** with free-tier-only choices and explicit 💲 warnings; any paid step
must be tear-down-documented so no student is left with a bill.

---

## Module 17: Advanced MLOps capstone integrating the entire lifecycle

**Track:** Advanced · **Effort:** 20–25 h · **Depends on:** all of 01–16 · **Ends the course**

### Learning outcomes
- LO 17.1 Take an idea to a deployed, monitored ML system: data → validation → versioning → training → tracking → tests → registry → API → container → CI → scheduling → monitoring → governance.
- LO 17.2 Make and defend end-to-end design decisions, including at least two explicitly rejected alternatives.
- LO 17.3 Demonstrate reproducibility to a third party using only the repository.
- LO 17.4 Operate the system under a fault-injection exercise and recover with a documented rollback.

### Required background
- All previous modules; the capstone is where they are combined, not re-taught.

### Key concepts and vocabulary
No new vocabulary is introduced — the capstone is deliberately integrative. It
consolidates **end-to-end lineage**, **production readiness review**, **SLOs**,
**runbook**, and **post-incident review**.

### Tools and why they are used
The full course stack, chosen by you and justified in a design document. The
default (all free/local): Python, Git, DVC, scikit-learn, MLflow, pytest, Make,
FastAPI, Docker/Podman, GitHub Actions, Prefect/Task Scheduler, Evidently,
fairlearn, kind.

### Guided laboratory scenario
**Lab 17 — Production readiness review.** The capstone ships with a review
checklist derived from all previous rubrics. You run your own system through it,
file issues, and fix them — the guided element is the review process, not the build.

### Independent practical challenge
**Capstone project:** a complete, self-built MLOps system for a problem of your own
choosing (see [course-project-map.md](course-project-map.md) for milestones,
evidence, and rubric).

### Assessment method
Integrated capstone rubric: reproducibility, automated quality gates, deployment
correctness, monitoring evidence, governance documentation, and the written design
defence. Weights in [assessment-framework.md](assessment-framework.md).

### Evidence to produce
Portfolio: full repository, evidence bundle (logs, reports, run histories, registry
history, drift reports), design document, defence write-up, and a video/text demo.

### Free / local alternative
The default capstone runs entirely locally and free. A cloud-hosted variant is an
optional extension (☁️/💲) with a mandatory teardown plan.

---

## Supporting topics map

Cross-cutting topics requested for the course and where they are taught:

| Supporting topic | Module | Status |
|---|---|---|
| Feature engineering | 05 | Essential |
| Feature stores (what/why/when to skip) | 09 (concept), 14 (serving consistency) | Optional |
| Infrastructure as code | 16 | Optional / advanced |
| Secrets management | 12 (CI secrets), 15 (full treatment) | Essential |
| Model lineage / provenance | 06 (capture), 09 (record), 15 (audit) | Essential |
| Rollback | 09 (model), 12 (deployment), 16 (cluster) | Essential |
| Reproducibility | 02 (environments), 05 (training), 06 (runs), 17 (demonstrated) | Essential thread |
| Cost management | 08 (compute awareness), 11 (image size), 16 (full treatment) | Essential in 16 |
| Data/privacy regulation (conceptual) | 15 | Essential concepts, no legal advice |
| GPU/accelerated training | — | Not covered; the course deliberately uses small CPU workloads |

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*
