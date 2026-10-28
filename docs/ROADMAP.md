# Roadmap — Build Plan

The course is being written in phases. This file records what exists, what comes
next, and in what order. Students do not need it; it is the working plan for
content production. Status is updated **in the same change** that lands the work.

**Repository status at last update:** syllabus, site architecture, and MkDocs
website complete; **all 17 module lesson sets (01–17) written in full**; three
runnable example projects (`examples/churn`, `examples/security-lab`,
`examples/capstone-support`) plus Kubernetes manifests (`examples/k8s/`).
website complete; **Modules 01–14 written in full** (lessons, worked examples,
labs, independent challenges, knowledge checks with answers, troubleshooting,
references) with a shared example project in `examples/churn/` (pipeline,
registry, FastAPI service, CI workflow, scheduler, monitoring) and CI at
`.github/workflows/ci.yml`; Modules 15–17 are specification-only; Phase 3
scaffolding items (LICENSE, glossary back-fill, datasets/) still open.

---

## Phase 0 — Audit and foundations ✅ complete

- [x] Inspected the workspace, Git state, existing content, docs, and workflows
- [x] Produced the audit report (see "Audit summary" below)
- [x] Defined the target repository structure and content conventions
- [x] Created the lab and assessment templates
- [x] Created the student prerequisites page
- [x] Created the course landing page (`README.md`)

### Audit summary (25 October 2026)

- **Local workspace:** the working directory contained no files other than
  application metadata (`.freebuff/`) — no README, no modules, no docs, no
  workflows, and **no Git repository** (`.git` absent).
- **Remote repository:** `github.com/nadeem-majeedch/MLOps` exists but is
  **empty** (GitHub reports "This repository is empty"; `git ls-remote` returned
  no refs).
- **Conclusion:** there is **no existing course content to preserve**, no
  incomplete work, and no broken references. All content starts from zero.
- **Risk:** because this directory is not a Git checkout, files written here are
  untracked until the instructor connects it to the repository (the instructor
  performs all Git operations — see rule 1 of the project brief).

---

## Phase 1 — Course architecture and syllabus ✅ complete

- [x] `docs/syllabus/course-overview.md` — purpose, audience, design principles, module sequence
- [x] `docs/syllabus/detailed-syllabus.md` — all 17 modules fully specified
- [x] `docs/syllabus/learning-outcomes.md` — CLOs with evidence table and module mapping
- [x] `docs/syllabus/tool-selection-guide.md` — tool rationale, alternatives, free/local paths
- [x] `docs/syllabus/assessment-framework.md` — four assessment layers + rubrics (suggested self-study framework)
- [x] `docs/syllabus/course-project-map.md` — MP1–MP5, capstone milestones C1–C7, portfolio
- [x] `docs/learning-roadmap/index.md` — student study order, gates, milestones
- [x] `docs/prerequisites/index.md` — migrated and updated for the 17-module sequence
- [x] Root `README.md` rewritten: student-facing description, outcomes, syllabus summary
- [x] Cross-references updated to the 17-module structure

## Phase 2 — Student experience and course website ✅ complete

- [x] `docs/index.md` — student landing page (site home)
- [x] `docs/start-here/index.md` — first-day learning guide
- [x] `docs/start-here/progress-checklist.md` — Markdown progress tracker (17 modules + MP1–5 + capstone)
- [x] `docs/glossary/index.md` — growing glossary seeded with core MLOps vocabulary
- [x] `docs/troubleshooting/index.md` — common student problems, symptom → cause → fix
- [x] `docs/resources/index.md` — curated, mostly-free learning resources
- [x] `docs/about/index.md` — instructor identity, credits, licence status (site metadata + About)
- [x] `docs/labs/index.md`, `docs/projects/index.md`, `docs/assessments/index.md` — navigation sections
- [x] `docs/modules/01…17/index.md` — 17 module pages generated from the syllabus
- [x] `mkdocs.yml` (MkDocs + Material) with nine-section `nav`, search, highlighting, prev/next links
- [x] `requirements-docs.txt`, `.gitignore` (excludes generated `site/`)
- [x] Technical docs: `docs/reference-guides/{website-development,github-pages-deployment,local-preview}.md`
- [x] Links repaired so nothing points outside `docs/`; strict build + link check run

**Exit criteria:** a student can open the site, find their way in the first day,
understand the whole course, and reach every module and lab from the navigation.

---

## Phase 3 — Scaffolding and tooling 🟡 partially complete

- [ ] `LICENSE` (decide and add)
- [ ] Extend `.gitignore` for Python/OS/editor noise (website entries already present)
- [x] Seed `docs/glossary/index.md` further from real module text (85 entries;
      added Module 15–17 vocabulary: threat model, blast radius, PRR, pod,
      readiness/liveness, request vs limit, risk register, …)
- [ ] `docs/FAQ.md` (student questions, assembled from real friction)
- [ ] Consolidated `CREDITS` detail for datasets and external sources (currently in `docs/about/index.md`)
- [x] `datasets/` with lab data — **superseded**: every example now generates its
      own deterministic synthetic data in place (`generate_data.py` pattern),
      which is more honest than a checked-in CSV
- [x] `.github/workflows/` link-check + `mkdocs build --strict` on every push —
      **partially**: CI exists for the examples (`.github/workflows/ci.yml` for
      `examples/churn`, `capstone.yml` for `examples/capstone-support`, both
      lint+test+gate, least-privilege, credential-free); a docs CI job
      (`mkdocs build --strict` + link check) is still open

**Exit criteria:** a student cloning the repo sees an honest map of the course with
licensing settled and CI enforcing the site.

## Phase 4 — Beginner track (Modules 01–05) ✅ complete

- [x] 01 Introduction to MLOps and the ML lifecycle
- [x] 02 Python, Git, CLI, and reproducible environments
- [x] 03 Organizing an ML project and understanding technical debt (→ MP1)
- [x] 04 Data quality, validation, and data versioning
- [x] 05 Reproducible model training and pipeline design
- [x] All nine learning components per module, built from the templates
- [x] Shared example project `examples/churn/` introduced (used by every module)

**Exit criteria:** every lesson passes the §8 definition of done; every lab has
been executed end-to-end on Windows 11 and its expected output recorded.

## Phase 5 — Intermediate track (Modules 06–12) ✅ complete

- [x] 06 Experiment tracking with MLflow (→ MP2)
- [x] 07 Testing for ML systems
- [x] 08 Pipeline automation and workflow dependencies
- [x] 09 Model artifacts, registry, promotion (→ MP3)
- [x] 10 Model serving and REST APIs with FastAPI
- [x] 11 Docker images and containers
- [x] 12 CI/CD with GitHub Actions (→ MP4)

## Phase 6 — Advanced track (Modules 13–17) ✅ complete

- [x] 13 Workflow orchestration and scheduled pipelines
- [x] 14 Monitoring, drift, and retraining (→ MP5)
- [x] 15 Security, privacy, governance, fairness — incl. threat-model lab
      (`examples/security-lab/`: install-free scanner, 5 seeded defects,
      red run 6 failed → fixed run 7 passed, tamper drill, real fairness gaps)
- [x] 16 Cloud concepts, Kubernetes, scaling, reliability — incl.
      `examples/k8s/` manifests (YAML-verified; cluster execution is the
      student's lab — authoring machine has no Docker/kind/kubectl; Path B
      documented for machines without tooling)
- [x] 17 Capstone with rubric and fault-injection review — incl. the full
      reference implementation `examples/capstone-support/` (30 tests green,
      5-stage pipeline, gate + `--ack` governance, live API, monitoring
      decision, release/rollback) and the four deliverables under
      `docs/projects/` (specification, checklist, rubric worksheet,
      self-assessment)

## Phase 7 — Hardening and release ⬜ next

- [ ] Cross-link audit; troubleshooting and FAQ assembled from lab friction points
- [ ] External review pass; accessibility check on diagrams and tables
- [ ] Docs CI: `mkdocs build --strict` + link check on every push
- [ ] First publication to GitHub Pages (owner action — see
      `docs/reference-guides/github-pages-deployment.md`)
- [ ] Tag a release; announce as a self-study course

---

## Ordering rules

1. Module content may land while Phase 3 scaffolding is open, but LICENSE, the
   glossary back-fill, and the CI link check must land before Phase 7 publication.
2. Content lands in module order; a later module may not assume an unwritten
   earlier one.
3. Templates change only with a documented reason — a template edit ripples
   across every existing file.
4. The syllabus is the contract: if module content diverges from
   `docs/syllabus/detailed-syllabus.md`, update the syllabus in the same change —
   and regenerate the affected `docs/modules/NN-*/index.md` page.
5. Every content change must pass `mkdocs build --strict` and the link check.