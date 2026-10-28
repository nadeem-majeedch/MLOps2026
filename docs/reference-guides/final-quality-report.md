# Final quality report — release-readiness audit

**Audit date:** 2026-10-27 · **Auditor:** automated release-readiness audit (local working tree only)
**Repository:** `https://github.com/nadeem-majeedch/MLOps` · **Platform audited:** Windows 11, Python 3.14.7

> **Verdict: PASS WITH WARNINGS** — see [§9](#9-release-readiness-verdict).
> Content, integrity checks, tests, and the strict site build all pass. The
> warnings are environment gaps (Docker/kubectl/actionlint unavailable on this
> machine), owner-only steps (GitHub Pages setting, licence file), and
> deliberately failing teaching fixtures.

This report is **evidence-based**: every claim below comes from a command in
[§4](#4-exact-verification-commands) whose actual output is in
[§5](#5-actual-test-and-build-results). Nothing is marked verified that was
not executed on this machine.

---

## 1. Summary of completed content

| Area | State |
|---|---|
| Course modules | **17/17** complete — 9 required files each (index, learning objectives, concepts, worked example, guided lab, independent challenge, knowledge check with answers, troubleshooting, references); 5,391–8,274 words per module (~110k words total) |
| Standalone laboratories | **20/20** (`docs/labs/lab-01` … `lab-20`), each with scenario, objectives, prerequisites, time estimate, setup, numbered steps, commands + expected output, acceptance criteria, troubleshooting, reflection, optional challenge, cleanup, and a rubric/checklist |
| Module guided labs | **17/17**, one per module page, all marked ready |
| Executable material | `examples/churn/` (34 tests), `examples/capstone-support/` (30 tests + 3.5 s training run), 3 starter projects (26 tests), lab fixtures, security lab, reference solutions |
| Data | Fully synthetic and deterministic — `python make_data.py --check` proves byte-identical regeneration; `datasets/` is 12 KB |
| Website | MkDocs Material; strict build passes; project-site base path configured (`site_url: …/MLOps/`) |
| Assessment material | Question banks (9), mini-projects, capstone, rubrics, submission templates, keys kept separate in `docs/assessments/keys/` |
| Student onboarding | `start-here`, prerequisites pre-flight, learning roadmap, glossary, troubleshooting — no instructor intervention required |

---

## 2. Module and lab coverage

**Modules (Audit 1):** all 17 directories exist under `docs/modules/`, each with
exactly the 9 required files, each `index.md` with an H1. Word counts per
module: 5,391 (M10) … 8,274 (M16). `scripts/check_course.py`'s
`[PASS] module sections` re-verifies file presence and headings on demand.

**Labs (Audit 3):** all 20 lab documents matched every required section
category (13/13 each — checked by regex sweep over
`docs/labs/lab-*.md`): scenario, objectives, prerequisites, estimated time,
setup, numbered steps, expected results, acceptance criteria, troubleshooting,
reflection questions, optional challenge, cleanup, rubric/checklist. Lengths
1,050–2,001 words. The labs index groups them by difficulty
(foundation 01–05, intermediate 06–12, advanced 13–16, advanced+integration
17–20) and links each to its prerequisite module and fixture folder.

**Prerequisite chain:** every lab row in
[labs/index.md](../labs/index.md) names its prerequisite module and earlier
labs; the roadmap states "work in order 01 → 20".

---

## 3. Files created or changed during this audit

| File | Change | Why |
|---|---|---|
| `examples/starter-projects/conftest.py` | **created** | Repair: `train.py` exists in both beginner and advanced starters, so the documented combined command `pytest examples/starter-projects -q` loaded the wrong module and failed 5 tests. The hook loads each folder's own `train.py` before its test file is imported. |
| `docs/labs/index.md` | extended | Added reference-solutions/glossary help section, final self-check list before the capstone, roadmap cross-links (glossary was reachable only implicitly). |
| `docs/glossary/index.md` | extended | Added missing **G** (gate, Git, GitHub Actions, governance), **K** (kernel, Kubernetes), and **Q** (quality gate) sections — these terms are used throughout but had no entry. |
| `docs/learning-roadmap/index.md` | extended | New "Laboratories and practice materials" block linking the 20 labs and the assessment package, which the roadmap did not mention. |
| `docs/labs/lab-10-serve-it.md` | wording fix | It said the reference `app.py` "lives in `solutions/lab-10/`"; the code is a copy-ready block inside that folder's `README.md`. The link now points at the exact file. |
| `docs/reference-guides/final-quality-report.md` | **created** | This document (deliverable). |
| `docs/reference-guides/known-limitations.md` | **created** | Deliverable. |
| `docs/reference-guides/pre-publication-checklist.md` | **created** | Deliverable. |
| `mkdocs.yml` | nav extended | The three new reports added to the Reference guides nav section. |

No other files were modified. No commits, pushes, deployments, or history
changes were made (and see [§6](#6-checks-that-could-not-be-run): this
workspace copy contains no `.git` directory at all).

---

## 4. Exact verification commands

Run from the repository root, 🐧/🪟 identical unless noted.

```bash
# A. Course integrity (navigation, links+anchors, module sections, Python syntax)
python scripts/check_course.py

# B. Strict website build
python -m mkdocs build --strict

# C. Tests — starters (combined AND per folder)
python -m pytest examples/starter-projects -q
python -m pytest examples/starter-projects/beginner -q
python -m pytest examples/starter-projects/intermediate -q
python -m pytest examples/starter-projects/advanced -q

# D. Tests — churn example and capstone reference implementation
cd examples/churn          && python -m pytest tests -q ; cd ../..
cd examples/capstone-support && python -m pytest -q     ; cd ../..

# E. Tests — reference solutions and teaching fixtures
python -m pytest examples/labs/solutions/lab-11 -q
python -m pytest examples/labs/lab-13 examples/labs/solutions/lab-15 -q   # fails BY DESIGN
python -m pytest examples/labs/lab-10 examples/security-lab/tests -q -rs  # skips BY DESIGN

# F. Deterministic data generation (byte-identical check)
cd examples/labs && python make_data.py --check ; cd ../..

# G. Capstone model training (deterministic, 3.5 s)
cd examples/capstone-support && python -m src.train ; cd ../..

# H. Lint, dependency health, syntax
python -m ruff check examples/churn examples/capstone-support scripts examples/starter-projects
python -m pip check
python -m compileall -q examples/churn/src examples/capstone-support/src \
    examples/labs examples/security-lab examples/starter-projects scripts

# I. Workflow / config YAML parse
python -c "import yaml,glob; [yaml.safe_load(open(f,encoding='utf-8')) for f in glob.glob('.github/workflows/*.yml')+['mkdocs.yml']]; print('YAML OK')"

# J. Secret-pattern scan over the tree (excluding virtualenvs and caches)
grep -rInE "(AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|xox[baprs]-[A-Za-z0-9-]{10,})" \
  --exclude-dir=.venv --exclude-dir=__pycache__ --exclude-dir=site .

# K. Tool availability report
command -v docker; command -v kubectl; command -v actionlint
```

---

## 5. Actual test and build results

All outputs below were captured on 2026-10-27 during this audit.

| # | Check | Result |
|---|---|---|
| A | `scripts/check_course.py` | ✅ **PASS** — navigation, links+anchors, module sections, python syntax; exit 0 |
| B | `mkdocs build --strict` | ✅ **exit 0**, built in 6.2 s, **0 warnings** (the one "warning" string in the log is MkDocs' own 2.0-migration notice). 137 pages are INFO-listed as "not in nav" — by design, see §7. |
| C | starter tests, **combined** | ✅ **26 passed** (regression fix — previously 5 errors) |
| C | beginner / intermediate / advanced | ✅ 3 / 9 / 14 passed |
| D | `examples/churn` tests | ✅ **34 passed**, exit 0 (1 Starlette deprecation warning from FastAPI's TestClient) |
| D | `examples/capstone-support` tests | ✅ **30 passed**, exit 0 |
| E | `solutions/lab-11` (fixed service regression tests) | ✅ **5 passed** |
| E | `lab-13` + `solutions/lab-15` fixtures | ⚠️ **9 failed, 1 passed — by design**: `test_compat.py` ships with a removed `np.float` call, and `test_release_gate.py` states in its docstring "AS SHIPPED these tests FAIL (that is the hole you are closing)". The `solutions/lab-15/README.md` records the same expected state ("Verified as shipped: 7 failed, 1 passed"). |
| E | `lab-10` + `security-lab` tests | ⚠️ **2 skipped — by design**: skip reasons are `create app.py first (see lab.md step 4)` and `create fixed/ first (lab step 1)`; the students create those files. |
| F | `make_data.py --check` | ✅ 3 CSVs hash-verified, **byte-identical across runs: YES** |
| G | capstone training | ✅ exit 0 — 1,950/450/600 split, seed 20261026, data SHA-256 recorded |
| H | `ruff check` (churn, capstone, scripts, starters) | ✅ **All checks passed** |
| H | `pip check` | ✅ **No broken requirements found** |
| H | `compileall` (all example + script trees) | ✅ exit 0 |
| I | YAML parse — `ci.yml`, `capstone.yml`, `pages.yml`, `validate-course.yml`, `mkdocs.yml` | ✅ **5/5 valid** |
| J | Secret scan | ✅ **clean** (no AWS/GitHub/OpenAI/private-key/Slack patterns anywhere outside virtualenvs) |
| K | Tool availability | ⚠️ `docker` **not available**, `kubectl` **not available**, `actionlint` **not available**; Python 3.14.7, mkdocs 1.6.1, pytest 9.1.1, ruff 0.17.2, git 2.56.0, node 24.20.0, mlflow 3.17.2, dvc 3.67.1 **present** |
| — | Dependency pins vs installed | ✅ every `==` pin in all 7 requirements files matches the installed version |
| — | Large artifacts | ✅ no file >1 MB outside `.venv/`, `__pycache__/`, `site/`; `datasets/` = 12 KB; `site/` build output is gitignored |

---

## 6. Checks that could not be run

| Check | Reason | Consequence |
|---|---|---|
| `docker build` / container verification (Labs 12, 16; churn & capstone Dockerfiles) | Docker CLI not installed on this machine | Container builds are **unverified here**; the Dockerfiles were reviewed statically only |
| `kubectl` / kind cluster steps (Lab 16, Module 16) | `kubectl` not installed | Kubernetes path unverified here |
| `actionlint` on GitHub workflows | not installed; no other suitable validator present | Workflows are **YAML-parse-validated only**, not schema-validated |
| Git-level checks (tracked-file secret scan, `git status`, history review) | **this workspace copy has no `.git` directory** (`git rev-parse` → "not a git repository") | All file-level results above are filesystem-based; the owner must re-run `git status` / review the diff before pushing |
| GitHub Pages build & deploy | No push/deploy permitted by this phase | `pages.yml` runs for the first time on the owner's first push |
| MLflow UI / DVC end-to-end lab runs (Labs 04, 06) | Not executed in this audit pass | Packages are installed and importable (mlflow 3.17.2, dvc 3.67.1); the labs themselves were validated structurally, not executed |
| MkDocs anchor-level strictness | MkDocs 1.6 reports missing anchors as INFO, not WARNING, under `--strict` | Documented in [build-and-validation.md](build-and-validation.md); a deliberate opt-in `anchors: warn` is left to the owner |

---

## 7. Remaining defects and limitations

1. **No `LICENSE` file.** The root README states a licence "will be added in a
   later phase". Not misleading today, but publication without one leaves
   reuse terms undefined — **owner decision required**.
2. **Teaching fixtures fail on purpose.** Anyone running the whole test tree in
   one command will see 9 failures and 2 skips. They are correct-by-design and
   documented in their own docstrings and solution READMEs; they are *not*
   wired into any CI workflow (`validate-course.yml` runs only the three
   starter folders).
3. **137 pages are not in `mkdocs.yml` nav** (module sub-pages + the
   `PREREQUISITES.md` pointer stub). This is the authored structure — each is
   reachable from its module's `index.md`, which *is* in nav, and MkDocs logs
   this at INFO level only. Restructuring the nav was judged out of scope for
   an audit; flagged here for owner awareness.
4. **Material for MkDocs reaches end-of-life 2027-05-05** (observed in our own
   build log). Successor migration is already covered in
   [maintenance.md](maintenance.md).
5. **A local `examples/churn/.venv/` exists** on this machine (ignored by
   `.gitignore`, never tracked). Harmless, but it makes filesystem size
   measurements larger than the committed tree.
6. **Churn test run emits one upstream deprecation warning**
   (Starlette `testclient`/`httpx`), not caused by course code.

---

## 8. Manual steps the owner must perform before publication

1. **Add a `LICENSE`** (or state the terms explicitly) — decide the reuse model.
2. **Re-run the verification block** in §4 from a real git clone and review
   `git status` / `git diff` before committing (this workspace has no git
   metadata).
3. **Commit and push** to `main` (owner-only; this audit made no Git changes).
4. **GitHub → Settings → Pages → Source = "GitHub Actions"** — one-time; until
   it is set, `pages.yml` builds green while the deploy job fails by design.
5. **Watch the first Actions runs:** `pages.yml` (build on PR, deploy on push)
   and `validate-course.yml` (integrity + starter tests).
6. **Smoke-test the published site** using the checklist in
   [pre-publication-checklist.md](pre-publication-checklist.md).
7. **Optional hardening:** protect the `github-pages` environment with required
   reviewers; enable MkDocs `anchors: warn` after a first warning triage.
8. **On a Docker-equipped machine**, run the container checks (Lab 12, Lab 16,
   `examples/churn/Dockerfile`) to close the gap in §6.

---

## 9. Release-readiness verdict

> ## ⚠️ PASS WITH WARNINGS

**Why PASS:** all 17 modules and all 20 labs are complete and structurally
verified; course integrity, strict site build, lint, dependency health,
deterministic data generation, model training, and 95 student-facing tests
(26 + 34 + 30 + 5) all pass; no secrets, no oversized artifacts, README policy
and instructor information both clean.

**Why WARNINGS:** Docker/kubectl/actionlint were unavailable so container,
Kubernetes, and workflow-schema checks could not run here; this workspace has
no `.git`, so Git-level verification and publication remain owner actions;
there is no `LICENSE` yet; and several test fixtures fail by design (correctly
documented, but they will surprise anyone running the whole tree blindly).

No failure found during this audit was hidden, skipped, or worked around: the
one real defect found (the starter `train.py` collision) was repaired with a
test, and the deliberately-failing fixtures are reported in §5 exactly as they
behave.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md). See also: [Known limitations](known-limitations.md)
· [Pre-publication checklist](pre-publication-checklist.md)*
