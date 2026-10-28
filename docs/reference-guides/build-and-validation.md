# Build and Validation

How to build the static site, check broken links and navigation, and run
**the exact checks CI runs** — locally, before you commit or push.

**Prerequisite:** [development setup](development-setup.md) completed
(venv active, `requirements-docs.txt` installed).

---

## 1. Build the static website

```powershell
# 🪟 PowerShell — from the repository root
python -m mkdocs build --strict
```
```bash
# 🐧 Linux / macOS
python -m mkdocs build --strict
```

- `mkdocs build` writes the whole site into `site/` (generated output —
  git-ignored, never committed).
- `--strict` **turns warnings into a failed build**: a broken link, a nav
  entry pointing at a missing file, or a config problem exits non-zero
  instead of shipping a broken page. This is the gate CI uses too.
- ✅ **Expect:** exit code 0 and a populated `site/` folder.

Preview the *built* output (what students will actually receive):

```powershell
python -m http.server 8080 --directory site      # http://127.0.0.1:8080/
```

For day-to-day editing use [`mkdocs serve`](local-preview.md) instead — it
reloads on save and serves the source directly.

---

## 2. Checking broken links and navigation

Three layers, from fastest to most complete:

**Layer 1 — MkDocs itself.** `mkdocs build --strict` fails on *warnings*:
links to missing files and nav entries pointing at nonexistent pages are
warnings, so strict catches them. One honest caveat, verified against
MkDocs 1.6 behaviour: **missing anchors are reported at INFO level by
default**, so strict alone does *not* fail on a wrong `#fragment`.

**Layer 2 — the course integrity script.** Because of that caveat (and
because the course has its own structural rules), this repository ships a
dependency-free checker:

```powershell
python scripts/check_course.py
```

| Check | What it proves |
|---|---|
| `navigation` | every `nav` entry exists; every module `index.md` and every standalone lab page is actually in `nav` (invisible pages are defects) |
| `links+anchors` | every relative Markdown link inside `docs/` resolves **and** every `#anchor` matches a real heading (or an explicit `{ #id }`) |
| `module sections` | the 17 module folders each ship the nine required files and `index.md` starts with an H1 |
| `python syntax` | every `.py` under `examples/` and `scripts/` compiles |

✅ **Expect:** four `[PASS]` lines and exit 0. On failure it prints each
finding with its file, and exits 1 — exactly what CI does (the same file
runs in `.github/workflows/validate-course.yml`).

**Layer 3 — the theme's optional stricter validation.** MkDocs 1.6 lets you
promote anchor/omitted-file notices from INFO to warnings in `mkdocs.yml`:

```yaml
validation:
  links:
    anchors: warn
  nav:
    omitted_files: warn
```

This is **deliberately not enabled** here: the course's nav intentionally
lists entry pages only (module sub-pages are reached through in-page
links), so `omitted_files: warn` would fail every build. Enable `anchors:
warn` if you want MkDocs itself to double-check what `check_course.py`
already checks — and fix whatever it then reports.

---

## 3. The other two checks

```powershell
python -m ruff check .            # lint standard defined in ruff.toml
python -m pytest -q               # (run inside an example folder — see below)
```

Test suites live with the code they test:

```powershell
cd examples\starter-projects\beginner ; python -m pytest -q ; cd ..\..\..
cd examples\capstone-support         ; python -m pytest -q ; cd ..\..
```

`examples/churn` additionally needs its data generated first
(`python generate_data.py`) — see that folder's README.

---

## 4. What each workflow will run

| Workflow | Trigger | Jobs | Publishes anything? |
|---|---|---|---|
| [`validate-course.yml`](https://github.com/nadeem-majeedch/MLOps/blob/main/.github/workflows/validate-course.yml) | push + PR to `main` | `integrity` (the script above), `lint-and-tests` (ruff + starter suites) | **No** — `contents: read` only |
| [`pages.yml`](https://github.com/nadeem-majeedch/MLOps/blob/main/.github/workflows/pages.yml) | push + PR to `main` | `build` (`mkdocs --strict`); `deploy` **only on push to main** | Deploy job only, and only once the owner enables Pages ([procedure](github-pages-deployment.md)) |
| `ci.yml` / `capstone.yml` | push + PR (existing) | churn / capstone lint, tests, ML validation | No |

---

## 5. Local workflow equivalent — run this before you commit or push

Copy-paste, root of the repository, venv active:

```powershell
# 🪟 PowerShell — the pre-push gate (mirrors CI step for step)
python scripts/check_course.py              # links, anchors, nav, sections, syntax
python -m ruff check .                      # repository lint standard
python -m pytest examples/starter-projects/beginner -q
python -m pytest examples/starter-projects/intermediate -q
python -m pytest examples/starter-projects/advanced -q
python -m mkdocs build --strict             # the same build CI performs
```
```bash
# 🐧 Linux/macOS — identical commands
python scripts/check_course.py && python -m ruff check . && \
python -m pytest examples/starter-projects/{beginner,intermediate,advanced} -q && \
python -m mkdocs build --strict
```

**Rule:** never commit with a red step, and never push a build you have not
run locally. `site/` is regenerated by CI — do not commit it.

---

## 6. Definition of done for any website change

- [ ] `python scripts/check_course.py` → four `[PASS]`, exit 0
- [ ] `python -m ruff check .` → `All checks passed!`
- [ ] affected test suites green (paste the count, not "it worked")
- [ ] `python -m mkdocs build --strict` → exit 0, no warnings
- [ ] new pages added to `nav` in `mkdocs.yml`
- [ ] `site/` and `.venv/` untouched by `git status`

---

**Related:** [Development setup](development-setup.md) ·
[Local preview](local-preview.md) ·
[Troubleshooting builds](troubleshooting-builds.md) ·
[Maintenance](maintenance.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*