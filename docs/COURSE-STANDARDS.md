# Course Standards and Conventions

This document is the single source of truth for how content in this repository is written, named, and organised. Every lesson, lab, and assessment must follow it. It is written for **content authors**, not for students; students start at [About](about/index.md).

**Contents**
1. [Course-writing standards](#1-course-writing-standards)
2. [Vocabulary rules](#2-vocabulary-rules)
3. [Labelling rules](#3-labelling-rules)
4. [Reproducibility and ethics rules](#4-reproducibility-and-ethics-rules)
5. [Filename and path conventions](#5-filename-and-path-conventions)
6. [Markdown conventions](#6-markdown-conventions)
7. [Target repository structure](#7-target-repository-structure)
8. [Content lifecycle (definition of done)](#8-content-lifecycle-definition-of-done)

---

## 1. Course-writing standards

### Voice and audience
- **Student-facing, not lecture notes.** Write to the reader as "you". Assume no lecturer is present to clarify anything.
- **No assumed context.** A reader who has completed only the previous module must be able to follow the current one.
- **Second person for instructions** ("Run the verification step"), third person for explanations ("The trainer estimates…").
- Avoid idioms, humour that dates, and unexplained abbreviations.

### Lesson structure (every lesson file)
```markdown
# Lesson NN — Title

## Learning objectives        ← 3–5 observable outcomes ("Given X, you will be able to Y")
## Why this matters           ← 1 short paragraph of real-world motivation
## Vocabulary                 ← new terms defined here, before use
## Explanation                ← the teaching content, worked examples included
## Worked example             ← complete, runnable, with expected output
## Check yourself             ← 3–5 short questions with an answers block or link
## Summary
## Further reading            ← links to primary/free sources
```

### Difficulty progression
Matches the 17-module syllabus ([syllabus/detailed-syllabus.md](syllabus/detailed-syllabus.md)):
- Modules 01–05: **beginner**. Short steps, heavy scaffolding, one new concept at a time.
- Modules 06–12: **intermediate**. More inference required, fewer step-by-step directions.
- Modules 13–17: **advanced**. Open-ended decisions, design trade-offs, production constraints.

### Length and pacing
- Target 1,500–3,000 words per lesson; split longer material into a second lesson rather than one oversized file.
- Every lesson must be completable in 20–45 minutes, or it must state a longer time estimate with the ⏱️ label.

### Scenario realism
- Labs use one recurring fictional organisation (defined in the module README) with realistic, non-sensitive data.
- Never use real personal data, credentials, or proprietary datasets.

---

## 2. Vocabulary rules

- **Define before use.** The first time any technical term appears in a module, it must be defined — in a Vocabulary section, a footnote, or a link to the course glossary.
- **One canonical term per concept.** Pick either "experiment tracking" or "run tracking" and use it everywhere; note synonyms once.
- On first use, put the term in **bold** with its definition inline if the concept is small, e.g. "**Drift** is a change in the statistical properties of production data over time."- New terms must also be added to the glossary ([glossary/index.md](glossary/index.md))
  in the same change that introduces them.
- Spell out an abbreviation on first use: "Continuous integration (CI)".

---

## 3. Labelling rules

Use these emoji labels consistently. They are defined for students in [About](about/index.md).

| Label | Use for |
|---|---|
| 🪟 | A command or step written for **Windows 11 + PowerShell** (the primary path) |
| 🐧 | The equivalent command for **Linux / macOS** (bash/zsh) |
| ☁️ | Any step requiring an **external cloud service or account** — always optional |
| 💲 | Any step with a **real monetary cost** beyond a free tier |
| ⚠️ | **Resource-heavy**: >5 GB disk, >8 GB RAM, heavy CPU, or >10 min runtime |
| ✅ | A **verification/checkpoint** step with stated expected output |
| ⏱️ | A **time estimate** that exceeds the normal 45-minute lesson budget |
| 📜 | Content drawn from an **external source** (must carry attribution) |

Rules:
- PowerShell commands are always shown in fenced blocks labelled `powershell`; Linux/macOS equivalents in blocks labelled `bash`, immediately after, with a one-line note on any difference.
- Never present a cloud or paid step as required. Required-path steps must run locally with free tools.
- A resource-heavy step must state the cost up front ("⚠️ Downloads ~3 GB, needs 8 GB RAM").

---

## 4. Reproducibility and ethics rules

- Every example that generates numbers sets and records its **random seed**; the seed and library versions appear in the worked example's expected output.
- Every dataset used must state its **licence**, **source URL**, and whether it is synthetic or real.
- Prefer synthetic or openly licensed data. If a dataset requires an account, label it ☁️ and provide a local/synthetic alternative.
- Every lab must include a **Cleanup** step that returns the learner's machine to its starting state.
- State expected outputs so results can be compared across machines.
- Ethical use: note intended use, known biases, and any privacy considerations for data used in examples (a short "Ethics note" block).

---

## 5. Filename and path conventions

- **Case:** all lowercase.
- **Word separator:** hyphen (`-`); no spaces, no underscores in new paths.
- **Language:** English, ASCII where possible.
- **Extensions:** `.md` for Markdown, `.py` for Python, `.ipynb` for notebooks, `.yml`/`.yaml` for configuration.
- **Modules:** `modules/NN-kebab-case-slug/` where `NN` is a zero-padded two-digit number (`01` … `17`, matching the syllabus).
- **Lessons:** `modules/NN-slug/lessons/NN-topic.md` (lesson numbers are unique inside the module).
- **Labs:** `modules/NN-slug/labs/lab-NN-short-name.md`, with its code in `modules/NN-slug/labs/code/lab-NN-short-name/`.
- **Assessments:** `modules/NN-slug/assessments/quiz-NN-a.md`; answer keys in `.../assessments/keys/quiz-NN-a-KEY.md`.
- **Projects:** `modules/NN-slug/projects/project-short-name.md`.
- **Images:** `docs/assets/img/module-NN/topic.png`; reference with relative paths.
- **No ALL-CAPS file names** except `README.md`, `LICENSE`, and `CHANGELOG.md`.
- **Do not rename or delete existing files** without recording the reason in the change description.

---

## 6. Markdown conventions

- One `#` (H1) per file, matching the file's topic; nest headings without skipping levels.
- Fenced code blocks always carry a language tag (`powershell`, `bash`, `python`, `yaml`, `json`, `text`).
- Use tables for comparisons and label matrices; keep tables under ~5 columns for readability.
- Relative links only, always tested before publishing (no broken links — see [§8](#8-content-lifecycle-definition-of-done)).
- Screenshots are optional; text and code must remain complete without them.
- Callouts use this pattern:
  ```markdown
  > ⚠️ **Resource-heavy:** downloads ~3 GB and needs 8 GB RAM.
  ```

---

## 7. Target repository structure

This is the end-state layout the course is being built toward. Items marked ✅ exist today;
the rest are created as their phase lands (see [ROADMAP.md](ROADMAP.md)). Module
pages and the syllabus family live under `docs/` because `docs/` is also the
source of the MkDocs website — see [reference-guides/website-development.md](reference-guides/website-development.md).

```
MLOps/
├── README.md                      ✅ student-facing landing page, outcomes, syllabus summary
├── LICENSE                        ⬜ added in a later phase
├── .gitignore                     ⬜ Python/OS/editor ignores
├── docs/
│   ├── syllabus/
│   │   ├── course-overview.md     ✅ purpose, audience, design principles
│   │   ├── detailed-syllabus.md   ✅ all 17 modules specified
│   │   ├── learning-outcomes.md   ✅ course-level outcomes + module mapping
│   │   ├── tool-selection-guide.md✅ tool rationale and free/local alternatives
│   │   ├── assessment-framework.md✅ suggested self-study assessment scheme
│   │   └── course-project-map.md  ✅ mini-projects, capstone, portfolio
│   ├── learning-roadmap/
│   │   └── index.md               ✅ student study order, gates, milestones
│   ├── prerequisites/
│   │   └── index.md               ✅ skills, software, accounts, pre-flight checklist
│   ├── COURSE-STANDARDS.md        ✅ this file
│   ├── ROADMAP.md                 ✅ phase-by-phase build plan
│   ├── PREREQUISITES.md           ✅ pointer stub → prerequisites/index.md
│   ├── index.md                   ✅ student landing page (site home)
│   ├── start-here/
│   │   ├── index.md               ✅ first-day learning guide
│   │   └── progress-checklist.md  ✅ Markdown progress tracker
│   ├── glossary/index.md          ✅ canonical definitions of all course terms
│   ├── troubleshooting/index.md   ✅ common errors → cause → fix, cross-referenced by labs
│   ├── resources/index.md         ✅ curated external learning resources
│   ├── about/index.md             ✅ instructor identity, credits, licence status
│   ├── labs/index.md              ✅ every guided lab reachable from navigation
│   ├── projects/index.md          ✅ mini-projects and the capstone
│   ├── assessments/index.md       ✅ assessment scheme entry point
│   ├── reference-guides/
│   │   ├── website-development.md ✅ contributor guide to the MkDocs site
│   │   ├── github-pages-deployment.md ✅ publishing procedure (owner action only)
│   │   └── local-preview.md       ✅ build and preview the site locally
│   ├── FAQ.md                     ⬜ student questions
│   ├── TEMPLATES/
│   │   ├── LAB-TEMPLATE.md        ✅ standard laboratory template
│   │   └── ASSESSMENT-TEMPLATE.md ✅ standard assessment template
│   ├── assets/img/                ⬜ diagrams and screenshots (create on first use)
│   └── modules/                   ✅ one folder per module, from the syllabus:
│   │   ├── 01-introduction-mlops-lifecycle/
│   │   ├── 02-python-git-cli-environments/
│   │   ├── 03-ml-project-technical-debt/
│   │   ├── 04-data-quality-validation-versioning/
│   │   ├── 05-reproducible-training-pipelines/
│   │   ├── 06-experiment-tracking-mlflow/
│   │   ├── 07-testing-for-ml/
│   │   ├── 08-pipeline-automation/
│   │   ├── 09-model-artifacts-registry/
│   │   ├── 10-model-serving-fastapi/
│   │   ├── 11-docker-containers/
│   │   ├── 12-cicd-github-actions/
│   │   ├── 13-orchestration-scheduled-pipelines/
│   │   ├── 14-monitoring-drift-retraining/
│   │   ├── 15-security-privacy-governance/
│   │   ├── 16-cloud-kubernetes-scaling/
│   │   └── 17-capstone/
├── mkdocs.yml                     ✅ site configuration and navigation
├── requirements-docs.txt          ✅ website build dependencies
├── datasets/                      ⬜ small, openly licensed or synthetic course data
├── scripts/                       ⬜ course utility scripts (verification, scaffolding)
└── .github/
    └── workflows/                 ⬜ repo CI: link checking and Markdown lint
```

Module slugs are taken from the syllabus; when creating a folder, keep its number
and use the kebab-case slug above.

Each module directory, when created, follows this shape:

```
modules/NN-slug/
├── README.md          module overview, objectives, map of its files, estimated time
├── lessons/           teaching content, one file per lesson
├── labs/              realistic laboratory scenarios (+ labs/code/ for runnable material)
├── assessments/       quizzes and assignments (+ keys/)
└── projects/          larger graded work (later modules only)
```

---

## 8. Content lifecycle (definition of done)

New content is "done" only when **all** of the following are true:

- [ ] It follows the lesson, lab, or assessment template exactly.
- [ ] Every new technical term is defined before first use and added to `docs/glossary/index.md`.
- [ ] Every command carries the correct OS label, and PowerShell/Linux variants are both present where applicable.
- [ ] Every required-path step runs locally with free, open-source tooling; cloud/paid steps are labelled ☁️/💲 and optional.
- [ ] Seeds, dataset licences, expected outputs, cleanup steps, and an ethics note are present.
- [ ] All commands and code blocks have been executed and their output checked (evidence, not assumption).
- [ ] All internal links resolve (checked with the repository's link checker or a manual pass).
- [ ] Filenames and headings match [§5](#5-filename-and-path-conventions) and [§6](#6-markdown-conventions).
- [ ] No deployment, installation, or build instructions were added to the root `README.md` — they belong in `docs/`.

**Verification before completion:** never describe content as finished, correct, or passing without having run the relevant check and read its output in the same working session.
