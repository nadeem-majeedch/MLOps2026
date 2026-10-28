# GitHub Pages Deployment (for the repository owner)

How the MkDocs site is published to GitHub Pages as a **project site** at
`https://nadeem-majeedch.github.io/MLOps/`, and what the repository already
contains versus what only you can do.

> ⚠️ **This page is a procedure, not an action.** Nothing in this repository
> has been deployed. No command in it has been run by anyone but you.
> Deployment and repository-settings changes belong to the instructor,
> deliberately, at a time of their choosing.

---

## 1. Three different "deployments" — do not confuse them

This course talks about deploying three unrelated things. Only **A** is
discussed on this page.

| | A. Static course website | B. Student ML model deployment | C. ML training & monitoring infrastructure |
|---|---|---|---|
| **What is published** | built HTML from `docs/` | a model + prediction API (FastAPI, container) | training pipelines, experiment trackers, drift monitors, schedulers |
| **Tooling in this repo** | MkDocs → GitHub Pages (`pages.yml`) | Modules 10–11 labs, `examples/capstone-support/service`, Dockerfiles | Modules 08/13/14 (`pipe/`, `monitor.py`, tick runner, MLflow) |
| **Where it runs** | GitHub's static hosting | your laptop, a container, or any host you choose | your laptop, a scheduler, or a cloud account |
| **Cost / accounts** | free for a public repo | depends on your host (local = free) | local = free; managed = paid |
| **What "deploy" means** | replace static files | restart a service pointing at a new model | roll out a pipeline/monitoring change |
| **Failure affects** | documentation readers | live predictions and users | automated retraining and alerting |

Sharing one repository does **not** make them one activity: the website
workflow never touches a model, and no model-serving command publishes the
site. Keep them separate in your write-ups, too.

---

## 2. Why the base path matters (part A)

The repository is named **`MLOps`**, so a project site is served from the
sub-path `/MLOps/`, not from the domain root. Getting this wrong produces
the classic blank page with unstyled text.

`mkdocs.yml` already records the correct address:

```yaml
site_url: https://nadeem-majeedch.github.io/MLOps/
```

Because all links in the content are **relative**, that one setting is
enough: MkDocs prefixes asset and page URLs correctly. Diagnosing a
*wrong* base path — including the "works locally, blank in production"
case — is covered with fixes in
[troubleshooting builds](troubleshooting-builds.md#part-b-wrong-base-path-in-production).

---

## 3. What is already in the repository

`.github/workflows/pages.yml` implements the official Actions-based Pages
deployment, verified against the
[GitHub Pages custom-workflow docs](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages):

| Property | How the workflow does it |
|---|---|
| Triggers | `push` and `pull_request` to `main` (+ manual dispatch) |
| Validation vs deployment | **separated**: the `build` job runs `mkdocs build --strict` on every event; `configure-pages`, the artifact upload, and the `deploy` job run **only on a push to `main`** |
| Untrusted code | a pull request can build but can never deploy — two independent guards: the step-level `if:` and the job-level `if:` |
| Permissions | top level `contents: read`; only the deploy job gets `pages: write` + `id-token: write` (the minimum GitHub documents for Pages) |
| Secrets | **none** — no token, no PAT, nothing to leak; deployment authenticates via the job's OIDC-scoped permissions |
| Settings assumptions | `configure-pages`/upload/deploy are skipped until Pages is enabled, so the build stays green before configuration |
| Action versions (current majors, 2026) | `actions/checkout@v7`, `actions/setup-python@v7`, `actions/configure-pages@v5`, `actions/upload-pages-artifact@v4`, `actions/deploy-pages@v4` |
| `mkdocs gh-deploy` | **not used, and must never be used here** — it performs git operations and can publish changes from CI |

---

## 4. One-time repository settings (manual, owner only)

1. GitHub → repository → **Settings → Pages**.
2. Under **Build and deployment → Source**, choose **GitHub Actions**.
3. Optionally protect the `github-pages` environment (Settings → Environments)
   so only `main` may deploy.

Until step 2 is done, pushes still **validate** the site (the `build` job)
but the deploy steps are skipped/fail with a settings message — that is
expected, not a bug. These changes are the instructor's to make; nothing in
this repository modifies them automatically.

---

## 5. Deploying

After §4, publishing is ordinary work:

```text
push to main  →  actions/runs  →  "pages" workflow
    build (mkdocs --strict)  →  upload artifact  →  deploy (github-pages environment)
site appears at https://nadeem-majeedch.github.io/MLOps/
```

You can also trigger it manually with **Actions → pages → Run workflow**
(`workflow_dispatch` is configured). The workflow's `concurrency` group
prevents two deployments racing, and `cancel-in-progress` is off for the
deploy path so a deployment is never killed mid-flight.

**Owner-only alternatives (explicitly out of scope here):** publishing from
a `gh-pages` branch or running `mkdocs gh-deploy` locally both perform git
operations; this project's rules forbid automating them, so the Actions
artifact flow is the supported path.

---

## 6. Pre-publication checklist

- [ ] `python scripts/check_course.py` → four `[PASS]` locally.
- [ ] `python -m mkdocs build --strict` → exit 0, zero warnings.
- [ ] `site_url` matches the real repository name (`MLOps`, case-sensitive).
- [ ] Every page reachable from `nav` (the script checks module/lab pages).
- [ ] No secrets, no `.env`, no `site/` or `.venv/` staged for commit.
- [ ] Root `README.md` still carries **no** install/build instructions —
      they belong in [development setup](development-setup.md).
- [ ] Settings → Pages → Source = GitHub Actions (§4).
- [ ] After the first run: manual smoke test of the URL — home page
      renders, CSS loads, search works, one deep link resolves.

---

## 7. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Deploy job skipped entirely | PR, or not a push to `main` | expected — deploys only from `main` |
| Deploy fails: Pages not enabled | §4 not done | owner sets Source → GitHub Actions |
| Blank page, no styling | wrong base path | see [troubleshooting builds](troubleshooting-builds.md#part-b-wrong-base-path-in-production) |
| Build job red | a new warning slipped in | run `python -m mkdocs build --strict` locally and read the warning |
| Old content still served | deployment finished after your refresh | check the Actions run, hard-refresh the browser |

---

**Related:** [Build and validation](build-and-validation.md) ·
[Troubleshooting builds](troubleshooting-builds.md) ·
[Maintenance](maintenance.md) ·
[Website development](website-development.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*