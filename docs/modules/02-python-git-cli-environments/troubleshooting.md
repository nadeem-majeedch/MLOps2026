# Troubleshooting — Module 02

Module-specific problems. Python/Git/CI-wide problems:
[course troubleshooting](../../troubleshooting/index.md).

## 1. "Which Python?" — the mother of all Module 02 bugs

Almost every failure below reduces to: **you are not running the interpreter you
think you are.** Diagnose first, fix second.

```powershell
# 🪟 the one command that ends the argument
python -c "import sys; print(sys.executable)"
.venv\Scripts\python -c "import sys; print(sys.executable)"
```

```bash
# 🐧 Linux / macOS
python3 -c "import sys; print(sys.executable)"
.venv/bin/python -c "import sys; print(sys.executable)"
```

| Symptom | Cause | Fix |
|---|---|---|
| `'python' is not recognized` | Not installed, or PATH not refreshed, or Store alias | `py -3 --version`; if that works, use `py -3` everywhere; install from python.org with *Add to PATH*, then open a **new** terminal |
| `python` opens the Microsoft Store | Windows app alias | Settings → Apps → Advanced app settings → App execution aliases → turn off the aliases for `python.exe` |
| Package installed but still `ModuleNotFoundError` | Installed into a different interpreter | Reinstall with the explicit path: `.venv\Scripts\python -m pip install <pkg>` |
| Activation blocked: `running scripts is disabled` | PowerShell execution policy | Do **not** weaken policy for the course — prefix commands with `.venv\Scripts\python` instead (this is what the labs do) |
| `.venv\Scripts\python` not found | venv created elsewhere, or wrong folder | `Test-Path .venv` — if `False`, re-run `python -m venv .venv` **inside** the project |

## 2. Installation problems

| Symptom | Cause | Fix |
|---|---|---|
| `Could not find a version that satisfies the requirement` | Package/version not available for your Python | Note the package name from the error; check its docs for supported Python versions; try without a strict version |
| Slow or interrupted downloads | Large wheels, flaky network | Re-run the command — pip caches what it already fetched (verified installs took ~8 min cold, seconds warm) |
| `SSL: CERTIFICATE_VERIFY_FAILED` | Corporate proxy/firewall | Configure pip for your proxy, or ask IT for the internal index — do not disable verification |
| Mixed results after a partial install | Environment left half-populated | `python -m venv --clear .venv` to start clean, then reinstall |

## 3. Git problems

| Symptom | Cause | Fix |
|---|---|---|
| `'git' is not recognized` | Not installed / PATH | Reopen the terminal; reinstall Git for Windows choosing *Git from the command line* |
| `not a git repository` | You are outside the repo | `Get-Location` and `Set-Location` into the project; `.git` must exist there |
| `*.pyc`, `.venv` staged accidentally | `.gitignore` added after the fact | `git rm -r --cached <path>` then commit the corrected `.gitignore` |
| Commit refused: `Please tell me who you are` | Identity not configured | `git config --global user.name "…"` and `user.email "…"` |
| `LF will be replaced by CRLF` warnings | Line-ending defaults on Windows | Harmless for this course; set `core.autocrlf` once if diffs look noisy |
| Detached/confusing state after an interrupted command | Partial operation | `git status` first — always. It states the current branch and what is staged |

## 4. Lab-specific

| Symptom | Cause | Fix |
|---|---|---|
| Tests pass for you but the "missing dependency" step does nothing | You reinstalled already, or the package is in the system env and your test runs there | Confirm `sys.executable` points at `.venv` *before* the test run |
| `git status` shows `data/` staged | `.gitignore` pattern missing | Add `data/raw/` and `data/corrupt/`, `git reset`, re-check |
| `19 passed` but expected fewer/more | Wrong folder or stale copies | Run from the folder containing `pyproject.toml`; delete stray `__pycache__` if unsure |
| Numbers differ from the worked example | Different pandas version | Compare `pip freeze` output against worked-example §5 |

## 5. When nothing works

1. State it in one sentence: *"When I run X, I expect Y, but I get Z."*
2. Re-run the last ✅ checkpoint you actually ran.
3. Search the exact error text (not your paraphrase).
4. Report course bugs as issues — quoting module and step — because ambiguous
   instructions are defects.

---

[← Knowledge check](knowledge-check.md) · [References →](references.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*