# Pre-publication checklist

**Owner-only steps** before this course goes public at
`https://nadeem-majeedch.github.io/MLOps/`. Work top to bottom; each item is
either a decision, a manual action, or a verification. The audit already ran
the technical checks — their evidence is in
[final-quality-report.md](final-quality-report.md).

> ⚠️ Nothing in this checklist was performed by the audit. Committing,
> pushing, deploying, and changing repository settings are owner actions only.

---

## A. Decisions (cannot be automated)

- [ ] **Licence chosen and `LICENSE` file added** at the repository root
      (currently none — the README says "ask the instructor before
      redistributing"). Pick terms deliberately: content licence ≠ code licence.
- [ ] **Instructor information approved** as printed in
      [About](../about/index.md) and the root README:
      *Engr. Dr. Muhammad Nadeem Majeed, Professor, Department of Data Science
      (PUCIT), University of the Punjab, Lahore, Pakistan* — no other
      credentials, contacts, or approvals are claimed anywhere.
- [ ] **Assessment wording stays illustrative** — weights and rubrics are
      labelled a *suggested self-study framework*, not university grading
      policy. Spot-check:
      `find docs/assessments -name "*.md" | xargs grep -l "illustrative"`.

## B. Verify from a real clone (this audit ran on a git-less copy)

```powershell
# 🪟 PowerShell — from a fresh clone of the repository
python scripts/check_course.py            # ✅ 4/4 PASS
python -m mkdocs build --strict           # ✅ exit 0, no warnings
python -m pytest examples/starter-projects -q   # ✅ 26 passed
git status                                # ✅ only the files you intend to commit
git diff --stat                           # review before committing
```

```bash
# 🐧 Linux/macOS — identical commands
```

- [ ] `git status` shows only intended files (no `.venv/`, `site/`, `*.log`,
      `*.joblib`, `runs.jsonl` — all covered by `.gitignore`).
- [ ] No secrets in the diff: re-run the scan from
      [final-quality-report.md §4-J](final-quality-report.md).

## C. Commit and push (owner-only)

```powershell
git add -A
git commit -m "Add final quality report, known limitations, pre-publication checklist"
git push origin main
```

- [ ] Push is to the **primary branch** (`main`) — that is what the workflows
      trigger on.

## D. One-time GitHub repository settings (manual)

1. [ ] **Settings → Pages → Source = "GitHub Actions"**
      (required; without it the build succeeds and the *deploy* job fails —
      that failure is the intended signal, see
      [github-pages-deployment.md](github-pages-deployment.md) §4).
2. [ ] *(Optional hardening)* **Settings → Environments → `github-pages`** →
      add required reviewers / restrict to `main`.
3. [ ] *(Optional)* **Settings → Actions → General** →
      "Allow `MLOps` actions" and read-only workflow permissions, matching the
      minimal `permissions: contents: read` in the workflow files.

## E. First CI runs (verify, do not assume)

- [ ] **`pages.yml`** — PR run: `build` job green with
      `python -m mkdocs build --strict`. Push to `main`: `build` **and**
      `deploy` green; the run shows "Artifact deployment" success.
- [ ] **`validate-course.yml`** — `integrity` (4 checks), `lint`,
      `tests` (3 folders), `docs-build` all green.
- [ ] **`ci.yml` / `capstone.yml`** — churn and capstone jobs green
      (these run `ruff` + `pytest` in their folders).
- [ ] No workflow run shows a step that uses a personal token or a secret that
      is not part of the repository configuration.

## F. Published-site smoke test

- [ ] `https://nadeem-majeedch.github.io/MLOps/` loads with styling
      (a blank unstyled page means wrong base path — see
      [troubleshooting-builds.md](troubleshooting-builds.md) Part B).
- [ ] Nav works across the three stages; a module page opens its lab, knowledge
      check, and troubleshooting links.
- [ ] `[Site home page]` on the root README resolves to the published landing
      page; anchor links jump correctly.
- [ ] Browser console has **no 404s** for CSS/JS/images.
- [ ] Mobile width (narrow window) renders the sidebar sensibly.

## G. Student-path spot check (cold read)

- [ ] Open [Start Here](../start-here/index.md) as a stranger: prerequisites →
      roadmap → Module 01 — no step assumes an instructor, an account, or a
      paid tool.
- [ ] One lab executed end-to-end on a second machine/venv (fresh
      `python -m pip install -r`), following only the documented commands.
- [ ] Labels (🪟 🐧 ☁️ 💲 ⚠️ ✅) explained on the
      [course home page](../index.md) match their use in labs.

## H. After publication

- [ ] Watch the first student-reported issue; record it in
      [docs/ROADMAP.md](../ROADMAP.md) style.
- [ ] Schedule dependency review per [maintenance.md](maintenance.md)
      (one package at a time, before/after versions recorded).
- [ ] Calendar reminder: **Material for MkDocs EOL 2027-05-05** — plan the
      migration before that date.

---

**Rollback:** reverting a bad publication is `git revert <sha>` + push (the
workflow rebuilds). Taking the site offline is *Settings → Pages → Source →
"Deploy from a branch"* disabled or unpublish — the repository itself is
unaffected.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md). See also: [Final quality report](final-quality-report.md)
· [Known limitations](known-limitations.md)*
