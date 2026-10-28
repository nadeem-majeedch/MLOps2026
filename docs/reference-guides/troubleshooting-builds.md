# Troubleshooting Builds

Diagnosing two families of failure: **builds that fail** (Part A) and
**builds that succeed but publish a broken site** (Part B — wrong base
paths). Part C explains how to read a failing GitHub Actions run.

**First rule:** reproduce locally before touching anything.
`python -m mkdocs build --strict` from the repository root with the venv
active ([build and validation](build-and-validation.md)) — CI is just this
command on someone else's computer.

---

## Part A: the build itself fails

Read the **first** warning or traceback; later errors are usually
consequences. This table covers everything observed in this repository:

| Symptom | Likely cause | Fix |
|---|---|---|
| `mkdocs: command not found` / `python: command not found` | venv not active, or deps not installed | [development setup](development-setup.md) §2–3; confirm `python -m mkdocs --version` |
| Exit code 1, `Aborted with N warnings` | `--strict` did its job: a link/nav/config warning | the warning text names the file — fix the link or add the page to `nav` |
| `Doc file '…' contains a link '…', but the target … not found` | typo, renamed file, or a link that leaves `docs/` | relative links only, staying inside `docs/` (see [website development](website-development.md) §2) |
| `contains an unrecognized relative link '.', it was left as is` (INFO) | a link to `.` or an empty path | link to the actual file (`index.md`) |
| `INFO - The following pages exist … but are not included in the "nav"` | pages deliberately not listed (module sub-pages) | expected here — the course lists entry pages only; see [build and validation](build-and-validation.md) §2 |
| `found character that starts indentation error` / YAML parse error in `mkdocs.yml` | an unquoted `:` in a value, or tabs | quote the value (`name: "Text: with colon"`); YAML forbids tabs |
| `Config value 'theme' contains an invalid …` | theme package missing or wrong major | reinstall per `requirements-docs.txt`; keep `mkdocs-material>=9.5,<10.0` |
| Duplicate `nav` keys or missing page in nav after a move | file moved without updating `mkdocs.yml` | update `nav`, then rerun `check_course.py` |
| Build output contains junk pages/404s | stray files inside `docs/` | only Markdown and assets belong under `docs/` |
| Build works on CI, fails locally (or vice versa) | version drift | compare `python -m mkdocs --version` and `pip freeze`; both sides install from `requirements-docs.txt` |
| Windows console garbles output (`UnicodeEncodeError`) | legacy console encoding | `chcp 65001` or `python -X utf8 -m mkdocs build --strict` |
| Build seems stale after a crash | half-written `site/` | `Remove-Item -Recurse site` (🪟) / `rm -rf site` (🐧), rebuild |

**Triage sequence**

1. `python -m mkdocs build --strict` → read the first warning verbatim.
2. Still unclear? `python -m mkdocs build --verbose` for the full config
   and plugin trace.
3. Isolate **config** from **content**: revert your last change to
   `mkdocs.yml` and rebuild; if green, the config is the culprit.
4. Structural checks (links/anchors/nav/sections/syntax) in one command:
   `python scripts/check_course.py`.

---

## Part B: Wrong base path in production { #part-b-wrong-base-path-in-production }

The build is green locally, but the published page is blank, unstyled, or
full of 404s. This is always a **URL prefix** problem, and a project site
makes it likely: this repository publishes under
`https://nadeem-majeedch.github.io/MLOps/`, not `/`.

**Symptoms and what they mean**

| What you see | What it means |
|---|---|
| HTML loads, no styling, unstyled text | asset URLs point at `/css/...` instead of `/MLOps/css/...` → `site_url` wrong or pages served from a different path |
| Every navigation click 404s, home page fine | internal links absolute instead of relative, or `use_directory_urls` mismatch after a hosting change |
| CSS/JS 404 in the browser console | same as row 1 — check the exact failing URL's prefix |
| Search box empty/broken | `search` plugin assets under the wrong prefix, or an old cached page |

**Diagnosis, in order**

1. Open dev tools → Network → reload: **do the failing asset URLs carry
   `/MLOps/`?** If not, the base path never made it into the build.
2. Confirm the setting: `site_url: https://nadeem-majeedch.github.io/MLOps/`
   in `mkdocs.yml` (trailing slash, exact repository name, case-sensitive).
3. Rebuild and inspect one file: `site/index.html` — its `<link href>`
   values must start with `/MLOps/` (MkDocs writes them from `site_url`).
4. Check links in the *source*: content links must be relative
   (`[Glossary](../glossary/index.md)`), never root-absolute
   (`/glossary/`) — root-absolute breaks on any sub-path host.
5. Confirm the host is really serving from the sub-path (Settings → Pages
   shows the URL with `/MLOps`).

**Local reproduction of a sub-path deployment**

```powershell
# 🪟 PowerShell — serve the built site as if it lived under /MLOps/
Copy-Item -Recurse site _site_test\MLOps
python -m http.server 8080 --directory _site_test
# open http://127.0.0.1:8080/MLOps/  — styling must load from /MLOps/css/…
Remove-Item -Recurse _site_test
```

If the sub-path simulation renders correctly but production does not, the
problem is on the host side (wrong Pages source or a stale deployment),
not in your build.

---

## Part C: reading a failing Actions run

1. **Actions → workflow → run → failed job.** A red job, not the whole log.
2. **First failing step → first error line.** Steps after it are cascades.
3. Common mappings: `build` failing = a local-reproducible MkDocs warning;
   `integrity` failing = run `python scripts/check_course.py` locally;
   `lint-and-tests` failing = run the named `pytest` command locally;
   `deploy` failing with a settings/permission message = owner must set
   Settings → Pages → Source = GitHub Actions
   ([procedure](github-pages-deployment.md#4-one-time-repository-settings-manual-owner-only)).
4. The artifact-upload step failing means the *build* output was bad or
   absent — fix the build, not the upload.

**Never "fix" a red build by removing the check.** The gate exists to stop
broken pages reaching students; downgrade it only with a written reason in
the workflow comment.

---

**Related:** [Build and validation](build-and-validation.md) ·
[Local preview](local-preview.md) ·
[GitHub Pages deployment](github-pages-deployment.md) ·
[Maintenance](maintenance.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*