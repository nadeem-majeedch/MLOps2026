# Tool Selection Guide

Why each tool was chosen, what alternatives exist, when to prefer them, and what
to do if a tool needs an account or money. This guide supports the design
principle **"explain why alternatives exist"** — a course that only shows one tool
trains dependency, not judgement.

**Cost legend:** **Free/local** = runs offline on your laptop · **Free, account**
= free service needing sign-up · **☁️** = cloud service · **💲** = real cost beyond
a free tier · **⚠️** = resource-heavy.

---

## 1. Selection principles

1. **Concept first, tool second** — a tool appears only after its problem is explained.
2. **One major new tool per module** — everything else is reuse or contrast.
3. **Prefer the local, free, open-source option** for anything on the graded path.
4. **Prefer the industry-standard option** when it is also free (learning value).
5. **Name the alternative even when unused** — so you recognise it later.
6. **Any account or cost is labelled and optional**, with a free equivalent given.

---

## 2. Core stack (used on the required path)

| Need | Chosen tool | Why this one | Free? | Alternatives to know |
|---|---|---|---|---|
| Language | Python 3.10–3.12 | Ubiquitous in ML; small examples run anywhere | Free/local | — |
| Editor | VS Code | Free, first-class Python/terminal/Git support | Free/local | PyCharm Community, Neovim, JupyterLab |
| Shell (primary) | PowerShell | Built into Windows 11; the course's tested platform | Free/local | CMD (avoid), Windows Terminal |
| Shell (alternative) | bash | Built into Linux/macOS; also via Git Bash on Windows | Free/local | zsh, fish |
| Version control | Git + GitHub | Universal; CI modules need GitHub specifically | Free/local (hosting: free account) | GitLab, Bitbucket, local-only `git init`, Gitea (self-hosted) |
| Environment/dependencies | `venv` + `uv` | `venv` is built in (baseline), `uv` is the modern fast default | Free/local | conda/mamba, poetry, pip-tools |
| Project scaffolding | Cookiecutter template | Proven layout; teaches folder purpose | Free/local | copier, hand-rolled structure |
| Data handling | pandas | Default tabular tool, huge ecosystem | Free/local | polars, duckdb (named as faster modern options) |
| Data validation | pandera | Code-first, typed, plugs into pytest — low ceremony | Free/local | Great Expectations (heavier, richer reports), Soda, tensorflow-data-validation |
| Data/pipeline versioning | DVC | Git-style versions for data and pipelines without bloating Git | Free/local | Git LFS, lakeFS, plain checksums + notes, Quilt |
| Modelling | scikit-learn | Fast, CPU-only, ideal for teaching pipeline mechanics | Free/local | XGBoost, PyTorch (later complexity not needed here) |
| Configuration | YAML + typed loader | Diffable, reproducible runs | Free/local | Hydra/OmegaConf (advanced), argparse, environment variables |
| Experiment tracking | MLflow (local server) | Standard, Python-native, fully local with SQLite backend | Free/local | Weights & Biases (☁️ free tier), Neptune (☁️), Aim, Comet, plain CSV logs |
| Testing | pytest (+ pytest-cov) | De-facto standard; fixtures map to datasets | Free/local | unittest, nose2 |
| Pipeline automation | Make | Teaches dependency thinking in ~30 lines | Free/local | Snakemake, DVC pipelines, just, shell scripts |
| Serving | FastAPI (+ Pydantic, uvicorn) | Validation and docs from type hints; teaches good API habits | Free/local | Flask, Django REST, BentoML, Seldon, Triton (heavyweight) |
| Packaging/deployment env | Docker (or Podman) | Industry standard; Podman is the daemonless, licence-free equivalent | Free/local | Podman, buildah, nerdctl |
| CI/CD | GitHub Actions | Natural home for the course repo; free minutes for public repos | Free/local (account) | GitLab CI, Jenkins, CircleCI, **`act`** for local runs |
| Local workflow runner | `act` | Runs Actions offline in containers — no account needed | Free/local | — |
| Scheduling (baseline) | Task Scheduler (🪟) / cron (🐧) | Zero dependencies; every engineer should know it | Free/local | systemd timers |
| Orchestration (primary) | Prefect (local server) | Python-native, gentle curve, runs locally | Free/local | Airflow (⚠️ heavier), Dagster, Metaflow, cloud orchestrators (☁️/💲) |
| Drift/monitoring reports | Evidently | DataFrame in, full report out, fully local | Free/local | whylogs, alibi-detect, Great Expectations shifts |
| Live dashboards (optional) | Prometheus + Grafana | Standard, self-hosted, free | Free/local (⚠️) | Grafana Cloud (☁️), Datadog (💲) |
| Fairness analysis | fairlearn | Simple API, pandas-friendly | Free/local | IBM AIF360, AI Fairness 360 dashboards |
| Secret scanning | gitleaks | Fast, local, history-aware | Free/local | trufflehog, GitHub secret scanning (free on GitHub) |
| Kubernetes (learning) | kind / minikube | Real Kubernetes API on a laptop — no cloud bill | Free/local (⚠️) | k3s, Docker Desktop K8s, managed clusters (☁️/💲) |
| IaC (concepts) | Terraform | Transferable HCL skills; free to plan/apply locally | Free/local | Pulumi, AWS CDK, CloudFormation, Ansible |

---

## 3. Tools that need an account or money — and the free path

| Tool/step | What it needs | Free/local equivalent used for grading |
|---|---|---|
| GitHub hosting & Actions | Free account (public repos get free CI minutes) | Local `git init` + `act` for CI; the graded outcomes do not require publishing |
| Docker Desktop | Free for students/personal use; licence for larger orgs | **Podman** — fully free, open source, runs all Module 11 exercises |
| Weights & Biases / Neptune | ☁️ account, usage limits on free tier | **MLflow local server** — same concepts, no account, data stays on your machine |
| Cloud deployment (M16) | ☁️ provider account; 💲 risk if resources are left running | **kind + Docker Compose** locally; cloud labs are optional with mandatory teardown steps |
| Managed Kubernetes | ☁️/💲 | **kind/minikube** — real API, zero cost |
| Hosted Grafana/Datadog | ☁️/💲 | **Self-hosted Prometheus + Grafana** (local, ⚠️ memory) |
| Databricks / SageMaker | ☁️/💲 | **MLflow + Docker + Prefect locally** |
| Kaggle datasets (some) | ☁️ account | Synthetic or CC0 datasets shipped in `datasets/` |

**Rule of the course:** no graded outcome depends on an account other than a free
GitHub account, and no graded outcome depends on spending money.

---

## 4. When to graduate to a different tool

| You outgrow… | Because… | Move to… |
|---|---|---|
| Manual run comparisons | Runs exceed what you can eyeball | MLflow tracking (M06) — already planned |
| pandera checks | Rules need rich suites, documented expectations | Great Expectations |
| Make | Tasks need retries, schedules, backfill | Prefect (M13), then Airflow if team grows |
| FastAPI + one container | Traffic, isolation, and scaling needs grow | Kubernetes (M16) |
| File-based model registry | Multiple teams, approvals, audit requirements | Hosted registry (☁️) or a self-hosted registry service |
| Local drift reports | Continuous, alerting-driven monitoring | Prometheus + Grafana, then a monitoring platform |
| Hand-written manifests | Environments multiply, drift between them | Terraform (M16) |

---

## 5. Version policy

- Pin **exact** versions in lab environments (lock files) so results reproduce.
- Record versions in every evidence bundle (Module 05 onward).
- Tools are upgraded only between course phases, never mid-module — labs and
  expected outputs must stay consistent.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*
