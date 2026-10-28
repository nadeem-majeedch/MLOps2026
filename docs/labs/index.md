# Laboratories

Labs are where the course is actually learned — reading is preparation,
labs are the work. This page indexes **two collections**:

1. **The 20 laboratory exercises** (below) — standalone, scenario-driven
   practicals under `docs/labs/` with executable fixtures under
   [`examples/labs/`](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/labs).
   Each one is grouped by difficulty and topic, and links to its
   prerequisite module and its fixture.
2. **The 17 module guided labs** (further down) — one short guided lab
   inside every module page, following the
   [lab template](../TEMPLATES/LAB-TEMPLATE.md).

Reference answers for the 20 exercises live **separately**, in
[`examples/labs/solutions/`](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/labs/solutions) —
attempt a lab fully before opening its answer key.

---

## The 20 laboratory exercises

**Lab anatomy** (identical in every lab): identity table → scenario →
objectives → prerequisites/time → task → setup → numbered steps →
commands & expected results → ✅ acceptance criteria → troubleshooting →
reflection → optional challenge → cleanup → rubric.

### 🌱 Beginner — foundations (labs 01–05)

| Lab | Title | Topic | Prerequisite module | Fixture |
|---|---|---|---|---|
| [01](lab-01-reproducibility-detective.md) | Reproducibility detective | Reproducibility | [02 — Python, Git, CLI, environments](../modules/02-python-git-cli-environments/index.md) (then [05](../modules/05-reproducible-training-pipelines/index.md)) | `examples/labs/lab-01/` |
| [02](lab-02-untangle-the-notebook.md) | Untangle the notebook | Project structure & technical debt | [03 — ML project structure](../modules/03-ml-project-technical-debt/index.md) | `examples/labs/lab-02/` |
| [03](lab-03-gate-the-dirty-extract.md) | Gate the dirty extract | Data quality & validation | [04 — Data quality, validation](../modules/04-data-quality-validation-versioning/index.md) | `examples/labs/lab-03/` + `examples/labs/data/customers_dirty.csv` |
| [04](lab-04-version-it-and-prove-it.md) | Version it and prove it | Data versioning & reproducibility | [04 — Data versioning](../modules/04-data-quality-validation-versioning/index.md) | `examples/labs/make_data.py` + shared datasets |
| [05](lab-05-deterministic-by-construction.md) | Deterministic by construction | Pipeline design (🌱→🔧) | [05 — Reproducible training](../modules/05-reproducible-training-pipelines/index.md) · LAB-01 first | `examples/labs/lab-05/` |

### 🔧 Intermediate — tracking, testing, shipping (labs 06–13)

| Lab | Title | Topic | Prerequisite module | Fixture |
|---|---|---|---|---|
| [06](lab-06-ten-runs-one-decision.md) | Ten runs, one decision | Experiment tracking (MLflow) | [06 — Experiment tracking](../modules/06-experiment-tracking-mlflow/index.md) | `examples/labs/` shared data + MLflow |
| [07](lab-07-catch-the-leakage.md) | Catch the leakage | Testing: leakage & preprocessing | [07 — Testing for ML](../modules/07-testing-for-ml/index.md) + [05](../modules/05-reproducible-training-pipelines/index.md) | `examples/labs/lab-07/leaky_model.py` |
| [08](lab-08-the-gate-that-must-refuse.md) | The gate that must refuse | Quality gates & pipeline automation | [06](../modules/06-experiment-tracking-mlflow/index.md) + [08 — Pipeline automation](../modules/08-pipeline-automation/index.md) | `examples/labs/lab-08/` |
| [09](lab-09-staged-verified-released.md) | Staged, verified, released | Model artefacts & release candidates | [09 — Artifacts & registries](../modules/09-model-artifacts-registry/index.md) | `examples/labs/lab-09/` |
| [10](lab-10-serve-it.md) | Serve it | Model serving & REST APIs | [10 — FastAPI serving](../modules/10-model-serving-fastapi/index.md) | `examples/labs/lab-10/` |
| [11](lab-11-malformed-requests-autopsy.md) | Malformed-requests autopsy | API robustness & error design | [10 — FastAPI serving](../modules/10-model-serving-fastapi/index.md) | `examples/labs/lab-11/` |
| [12](lab-12-ship-the-image.md) | Ship the image | Containers & reproducible environments | [11 — Docker](../modules/11-docker-containers/index.md) · LAB-10 first | `examples/labs/lab-12/requirements.txt` + your LAB-10 service |
| [13](lab-13-dependency-time-bomb.md) | The dependency time bomb | Dependency incompatibility & automated tests | [02 — Environments](../modules/02-python-git-cli-environments/index.md) + [12 — CI/CD](../modules/12-cicd-github-actions/index.md) | `examples/labs/lab-13/` |

### 🚀 Advanced — operations, governance, incident response (labs 14–20)

| Lab | Title | Topic | Prerequisite module | Fixture |
|---|---|---|---|---|
| [14](lab-14-the-machine-checks-your-work.md) | The machine checks your work | CI/CD with GitHub Actions | [12 — CI/CD](../modules/12-cicd-github-actions/index.md) · LAB-07/13 first | your lab folder (or `examples/labs/lab-14/` scaffold) |
| [15](lab-15-nothing-ships-unchecked.md) | Nothing ships unchecked | Release validation & governance | [09 — Registries](../modules/09-model-artifacts-registry/index.md) + [15 — Security & governance](../modules/15-security-privacy-governance/index.md) · **LAB-08 first** | `examples/labs/lab-15/` |
| [16](lab-16-a-pipeline-that-runs-itself.md) | A pipeline that runs itself | Scheduling & unattended workflows | [13 — Orchestration](../modules/13-orchestration-scheduled-pipelines/index.md) · LAB-05 first | `examples/labs/lab-16/tick_runner.py` |
| [17](lab-17-read-the-drift-not-the-chart.md) | Read the drift, not the chart | Prediction logs & drift analysis | [14 — Monitoring & drift](../modules/14-monitoring-drift-retraining/index.md) | `examples/capstone-support/monitoring_out/` + `examples/labs/data/` |
| [18](lab-18-rollback-or-ride-it-out.md) | Rollback or ride it out | Performance regression & rollback | [14 — Monitoring](../modules/14-monitoring-drift-retraining/index.md) + [09 — Registry & rollback](../modules/09-model-artifacts-registry/index.md) | `examples/labs/lab-18/` |
| [19](lab-19-deployment-security-review.md) | Deployment security review | Security & privacy review | [15 — Security & governance](../modules/15-security-privacy-governance/index.md) (Module 10 assumed) | `examples/security-lab/` + `examples/capstone-support/` |
| [20](lab-20-incident-day.md) | Incident day | Full-lifecycle incident exercise | [17 — Capstone](../modules/17-capstone/index.md) · labs 01–19 are its ingredients | `examples/labs/lab-20/inject_fault.py` + `examples/capstone-support/` |

**Suggested path:** work in order 01 → 20; each row's prerequisite is
the minimum, and later labs deliberately reuse earlier fixtures (the
shared synthetic datasets in `examples/labs/data/`, the churn example in
`examples/churn/`, and the capstone project in
`examples/capstone-support/`).

---

## The 17 module guided labs

Every module also ships one shorter guided lab on its own page:

| Lab | Module | Scenario | Status |
|---|---|---|---|
| [Lab 01](../modules/01-introduction-mlops-lifecycle/lab.md) | 01 | Autopsy of a failed model launch | ✅ Ready |
| [Lab 02](../modules/02-python-git-cli-environments/lab.md) | 02 | Rebuild a teammate's environment | ✅ Ready |
| [Lab 03](../modules/03-ml-project-technical-debt/lab.md) | 03 | Rescue the spaghetti notebook | ✅ Ready |
| [Lab 04](../modules/04-data-quality-validation-versioning/lab.md) | 04 | Gate the incoming dataset | ✅ Ready |
| [Lab 05](../modules/05-reproducible-training-pipelines/lab.md) | 05 | Same seed, same model | ✅ Ready |
| [Lab 06](../modules/06-experiment-tracking-mlflow/lab.md) | 06 | Ten runs, one decision | ✅ Ready |
| [Lab 07](../modules/07-testing-for-ml/lab.md) | 07 | Build the safety net | ✅ Ready |
| [Lab 08](../modules/08-pipeline-automation/lab.md) | 08 | One command to rebuild everything | ✅ Ready |
| [Lab 09](../modules/09-model-artifacts-registry/lab.md) | 09 | Ship v1, prepare the rollback | ✅ Ready |
| [Lab 10](../modules/10-model-serving-fastapi/lab.md) | 10 | Serve a trained model to an application | ✅ Ready |
| [Lab 11](../modules/11-docker-containers/lab.md) | 11 | Same bytes, two places | ✅ Ready |
| [Lab 12](../modules/12-cicd-github-actions/lab.md) | 12 | Block a defective model release | ✅ Ready |
| [Lab 13](../modules/13-orchestration-scheduled-pipelines/lab.md) | 13 | A pipeline that runs itself | ✅ Ready |
| [Lab 14](../modules/14-monitoring-drift-retraining/lab.md) | 14 | Catch the drift, then decide like an engineer | ✅ Ready |
| [Lab 15](../modules/15-security-privacy-governance/lab.md) | 15 | Audit before someone else does | ✅ Ready |
| [Lab 16](../modules/16-cloud-kubernetes-scaling/lab.md) | 16 | Run it like a service ⚠️ | ✅ Ready (⚠️ needs Docker/kind/kubectl; Path B if absent) |
| [Lab 17](../modules/17-capstone/lab.md) | 17 | Production readiness review | ✅ Ready |

"✅ Ready" means the full lab page exists and can be worked through now — it
opens directly from the table. **All 17 module labs and all 20 laboratory
exercises are ready.**

---

## Ground rules for every lab

- **🪟 Primary path is Windows 11 + PowerShell**, with 🐧 Linux/macOS equivalents
  shown wherever the command differs.
- **Nothing graded needs an account or a credit card.** ☁️/💲 steps are labelled
  and always optional.
- **Every lab ends with cleanup** so your machine returns to its starting state.
- **Never tick a ✅ you have not run.** The verification step is the whole point:
  it is what tells you the work actually happened.
- **Never paste someone else's transcript as your own** — expected outputs in
  the lab pages come from the authoring machine; your machine's output is the
  evidence that counts.

## Before your first lab

Complete the [pre-flight checklist](../prerequisites/index.md), then read
[Start Here](../start-here/index.md).

---

## Help, solutions, and the glossary

- **Stuck?** Use the lab's own troubleshooting section first, then the
  [site troubleshooting guide](../troubleshooting/index.md).
- **Reference solutions** for all 20 laboratory exercises live separately in
  `examples/labs/solutions/` (repository folder, not part of the site) —
  attempt the lab **before** opening them.
- Every term used in a lab is defined in the [glossary](../glossary/index.md).

## Final self-check (before the capstone)

- [ ] I completed the guided laboratories for modules 01–17 and can show my evidence folder.
- [ ] I attempted labs 18–20 as integration practice.
- [ ] I can explain *why* each ✅ verification step exists, not just that it passed.
- [ ] I have a portfolio entry for every lab (command + output + interpretation).
- [ ] I know which labs I found hardest — that list is my revision plan.

*Next: [Learning roadmap](../learning-roadmap/index.md) ·
[Capstone](../modules/17-capstone/index.md)*

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*
