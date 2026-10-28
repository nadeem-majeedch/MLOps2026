# Local Preview

How to build and preview the course website on your own machine. Contributors
use this; students can read the same Markdown directly on GitHub or on the
published site.

**Platform:** 🪟 Windows 11 + PowerShell (primary) · 🐧 Linux/macOS alternatives given.
**First time here?** Start with [development setup](development-setup.md) —
what to install, how to create the virtual environment, and how to verify it.
This page assumes that is done.

---

## 1. One-time setup

```powershell
# 🪟 Windows — from the repository root
python --version                 # ✅ expect 3.10 or newer
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-docs.txt
mkdocs --version                 # ✅ expect 1.6.x and material 9.x
```

```bash
# 🐧 Linux / macOS equivalent
python3 --version                # ✅ expect 3.10 or newer
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-docs.txt
mkdocs --version                 # ✅ expect 1.6.x and material 9.x
```

## 2. Preview while editing

```powershell
# 🪟 PowerShell
python -m mkdocs serve
```

```bash
# 🐧 Linux / macOS
python -m mkdocs serve
```

Then open <http://127.0.0.1:8000/>. The server reloads when a file changes.

- **Port already in use?** Another process owns 8000 — stop it, or run
  `mkdocs serve -a 127.0.0.1:8001`.
- **Serving from a different folder?** Run the command from the repository root,
  the folder that contains `mkdocs.yml`.

## 3. Build (what CI will run)

```powershell
# 🪟 PowerShell — strict build: warnings become errors
python -m mkdocs build --strict
```

```bash
# 🐧 Linux / macOS
python -m mkdocs build --strict
```

✅ **Expect:** exit code 0, no warnings, and a freshly generated `site/` folder.
`site/` is build output — it is excluded by `.gitignore` and must never be
committed. The full check suite (links, anchors, navigation, lint, tests)
lives in [build and validation](build-and-validation.md).

Check the built site locally:

```powershell
# 🪟 PowerShell — serve the built output instead of the source
python -m http.server 8080 --directory site
```

## 4. Common build problems

| Symptom | Cause | Fix |
|---|---|---|
| `mkdocs: command not found` | Dependencies not installed, or venv inactive | Re-run step 1; confirm `mkdocs --version` inside the venv |
| Warning: link to a file not found | Link points outside `docs/`, or a renamed file | Fix the relative path (see [website development](website-development.md) §2) |
| Warning: page not found in nav | New page not added to `nav` | Add it to `mkdocs.yml` |
| Build picks up stray files | Junk folders inside `docs/` | Check `docs/`; only Markdown and assets belong there |
| Styling missing when opening `site/index.html` directly | Opening files via `file://` | Serve the folder over HTTP as in step 3 |
| Anything else | — | The full symptom→cause→fix tables live in [troubleshooting builds](troubleshooting-builds.md) |

## 5. Keep the source honest

The site is only a rendering of Markdown. If a page is broken as plain text on
GitHub, it is broken — fix the Markdown, not the CSS.

## 6. If you are about to commit or push

Run the local workflow equivalent first — the same commands CI runs:
[build and validation §5](build-and-validation.md#5-local-workflow-equivalent-run-this-before-you-commit-or-push).
Never push a build you have not run locally, and never commit `site/`.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*