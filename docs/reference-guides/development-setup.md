# Development Setup

Everything needed to work on **this repository's documentation and examples**
on your own machine. Students who only want to *read* the course need none of
this — they read the published site or the Markdown on GitHub.

**Platform:** 🪟 Windows 11 + PowerShell (primary) · 🐧 Linux/macOS
alternatives given for every command.

---

## 1. What you need

| Software | Required? | Version | Why |
|---|---|---|---|
| **Python** | yes | **3.10 or newer** (course verified on **3.14.7**) | MkDocs and every example script |
| **pip** | yes | ships with Python | installing dependencies |
| **Git** | yes (contributors) | any current | cloning, branches, PRs |
| A text editor | yes | e.g. VS Code | editing Markdown/YAML |
| **ruff** | for lint checks | installed as `ruff==0.15.1` (see §3) | the repository's lint standard (`ruff.toml`) |
| Docker / kubectl / a cloud account | **no** | — | only for optional labs; **never** for the docs workflow |

Check what you have:

```powershell
# 🪟 PowerShell
python --version        # ✅ expect 3.10+ (authoring machine: Python 3.14.7)
git --version
```
```bash
# 🐧 Linux/macOS
python3 --version && git --version
```

> **Windows note:** if `python` opens the Microsoft Store instead of printing a
> version, install Python from python.org and tick *Add to PATH*, then reopen
> the terminal.

---

## 2. Create a virtual environment

A virtual environment (venv) keeps this project's packages separate from your
system Python — the single most effective reproducibility habit in the course.

```powershell
# 🪟 Windows — from the repository root
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If activation is refused with *running scripts is disabled*, run once (for
this shell only — no administrator rights needed):

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

```bash
# 🐧 Linux / macOS — from the repository root
python3 -m venv .venv
source .venv/bin/activate
```

**You are in the venv when** the prompt shows `(.venv)` (or `.venv` in the
path). Confirm with `python -c "import sys; print(sys.prefix)"` — it must
point inside `.venv`.

```powershell
deactivate        # leave the venv (any platform)
```

`.venv/` is already in `.gitignore` — it is never committed. To reset
everything, delete the folder and start again; nothing else depends on it.

---

## 3. Install the documentation dependencies

The website needs exactly two files: `requirements-docs.txt` (the
dependencies) and `mkdocs.yml` (the configuration).

```powershell
# 🪟 PowerShell — venv active
python -m pip install --upgrade pip
python -m pip install -r requirements-docs.txt
python -m mkdocs --version
```
```bash
# 🐧 Linux / macOS
python -m pip install --upgrade pip
python -m pip install -r requirements-docs.txt
python -m mkdocs --version
```

✅ **Expect output like** `python -m mkdocs, version 1.6.1 …` with
`mkdocs-material 9.8.0` — that is what the authoring machine reports; the
file allows `mkdocs>=1.6,<2.0` and `mkdocs-material>=9.5,<10.0`.

### Optional: lint and test dependencies

```powershell
python -m pip install ruff==0.15.1 pytest==9.1.1
```

The example projects under `examples/` each carry their own pinned
`requirements.txt`; install one only when you intend to run it:

```powershell
python -m pip install -r examples\starter-projects\beginner\requirements.txt
```

---

## 4. Verify the setup (two commands)

```powershell
python scripts/check_course.py     # ✅ four [PASS] lines, exit 0
python -m mkdocs build --strict    # ✅ exit 0, site/ created
```

If both pass, you are set up. The next step is
[local preview](local-preview.md); the full check suite lives in
[build and validation](build-and-validation.md).

---

## 5. House rules for this repository

- **Never put credentials in the repo.** No tokens, no `.env` files, no
  cloud keys — this course needs none of them to build or validate.
- **Never run `mkdocs gh-deploy`** or any command that performs git
  operations on your behalf: deployment is the repository owner's
  deliberate action via GitHub Actions
  ([details](github-pages-deployment.md)).
- **Technical documentation lives under `docs/`** — never add install or
  build instructions to the root student-facing `README.md`.

---

**Related:** [Local preview](local-preview.md) ·
[Build and validation](build-and-validation.md) ·
[Troubleshooting builds](troubleshooting-builds.md) ·
[Maintenance](maintenance.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*