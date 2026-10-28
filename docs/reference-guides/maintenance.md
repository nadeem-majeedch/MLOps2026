# Maintenance

Keeping the site, its dependencies and its workflows healthy over time —
and changing any of them without breaking the build.

**Golden rule:** everything here is reproducible from source, so every
change is small, verified, and revertable. Validate before you commit
([build and validation](build-and-validation.md) §5), and let the owner
deploy ([procedure](github-pages-deployment.md)).

---

## 1. What needs maintaining, and when

| Thing | Cadence | Check |
|---|---|---|
| Content & navigation | every content change | `python scripts/check_course.py` |
| Python docs dependencies | monthly, or when a build warns | §2 below |
| GitHub Actions major versions | quarterly, or when a run warns of deprecation | §3 below |
| External links (URLs outside the repo) | twice a year | manual — internal checks only automate what is inside `docs/` |
| Course structure (modules, labs, nav) | at the end of every content phase | §4 below |
| Secrets/credentials | never — none exist for this workflow | confirm `.gitignore` still excludes `.env`, logs, `site/` |

---

## 2. Updating documentation dependencies safely

`requirements-docs.txt` currently allows **ranges** for the two website
packages, and CI/example code uses **exact pins** — deliberately:

```text
mkdocs>=1.6,<2.0          # ranges: the site must survive patch releases
mkdocs-material>=9.5,<10.0
```

**Procedure (one change at a time):**

1. Record the baseline inside your venv:
   ```powershell
   python -m pip list | Select-String "mkdocs|material"   # 🪟
   pip list | grep -i mkdocs                              # 🐧
   ```
2. Upgrade **one** package:
   ```powershell
   python -m pip install --upgrade "mkdocs>=1.6,<2.0"
   ```
3. Run the full local gate: `check_course` → `ruff` → tests →
   `mkdocs build --strict`.
4. Preview the site once by eye (`mkdocs serve`, check nav, search, dark
   mode, one deep page).
5. Commit the dependency change **only if everything is green**; include
   the before/after versions in the commit message.
6. If anything breaks: `python -m pip install "mkdocs==<old version>"`,
   confirm green again, then investigate from the release notes.

**Major upgrades (read first, upgrade second)**

- **MkDocs 1.x → 2.x:** the `<2.0` cap is intentional. Before lifting it,
  read the 2.x release notes, upgrade on a branch, and treat *any* new
  warning as a blocker. Lift the cap only in the same commit that makes
  the build green.
- **Material for MkDocs lifecycle:** builds on the authoring machine show
  a notice that Material for MkDocs reaches end of life on **5 May 2027**,
  with *Zensical* named as its maintained successor. When that date
  approaches (or when you upgrade), verify the current state on the theme's
  official site and plan the migration on a branch — do not switch themes
  on `main`.
- **Python:** the workflows pin `python-version: "3.14"`. Bump it only
  after the examples still pass locally on the new version.

**Never update by deleting the version constraints** to "see what
resolves" — a green build from an uncontrolled resolution is luck, not
reproducibility.

---

## 3. Updating GitHub Actions

Current majors in use (2026) — check each action's release page before
changing them:

| Action | In workflow | Current major |
|---|---|---|
| `actions/checkout` | all four workflows | v7 |
| `actions/setup-python` | all four workflows | v7 |
| `actions/configure-pages` | `pages.yml` | v5 |
| `actions/upload-pages-artifact` | `pages.yml` | v4 |
| `actions/deploy-pages` | `pages.yml` | v4 |
| `ruff==0.15.1` / `pytest==9.1.1` (pip pins) | `ci.yml`, `validate-course.yml` | keep identical across workflows |

Rules: change **one action per PR**; a PR run is the test (that is what
`pull_request:` triggers are for); never downgrade a major "because it
worked before" without a written justification comment in the workflow.
Deploy-related changes only take effect after a push to `main` and still
require the owner's Pages setting — validate them on a PR first.

---

## 4. Structural maintenance

- **Adding a page:** create it under `docs/`, add it to `nav`, run
  `python scripts/check_course.py` (it fails if a module/lab page is
  missing from `nav`).
- **Adding or renumbering a module:** update `nav`, the labs index, the
  module's previous/next links, and the syllabus — all in one change
  ([website development](website-development.md) §3).
- **Syllabus edits:** the module index pages were generated from
  `docs/syllabus/detailed-syllabus.md`; sync them, then re-run the checks
  (§6 there).
- **Definition of done:** the six-box list at the end of
  [build and validation](build-and-validation.md).

---

## 5. Rollback

Because the site is generated, rollback is ordinary Git:

```powershell
git log --oneline -5           # identify the offending change
git revert <sha>               # 🪟/🐧 — a revert commit, never a force-push
# re-run the local gate, push; Pages rebuilds from source on push to main
```

- **Never** edit files under `site/` — it is regenerated on every build and
  edits there are lost and untraceable.
- **Never** run `mkdocs gh-deploy` or push to a `gh-pages` branch to
  "undo" something: both perform git operations from the wrong place. The
  workflow on `main` *is* the deployment path.
- If a bad site is already published, reverting `main` is the fix; the
  next green run re-publishes the good version.

---

## 6. Standing safety rules

1. No secrets or tokens in workflows, configs, or docs — the pages and
   validation workflows need **none** (`contents: read` only).
2. `site/`, `.venv/`, logs, and generated model binaries stay out of Git
   (see `.gitignore` and the repository's `datasets/README.md`).
3. Root `README.md` stays student-facing: no install, build, or deploy
   instructions there.
4. Deployments are owner actions, taken deliberately — CI validates, the
   owner publishes.

---

**Related:** [Build and validation](build-and-validation.md) ·
[Troubleshooting builds](troubleshooting-builds.md) ·
[Development setup](development-setup.md) ·
[GitHub Pages deployment](github-pages-deployment.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*