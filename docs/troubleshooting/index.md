# Troubleshooting

Common student problems, their likely causes, and the fix — in the order you
should try them. Organised by where the pain usually appears.

**First habit to build:** read the *last* line of an error first. It names the
real problem; everything above it is the trail that got there.

---

## 1. The universal three steps

1. **Reproduce it** with the smallest possible command. If you cannot reproduce
   it, you cannot fix it.
2. **Read the error verbatim** — search the exact message, not your interpretation
   of it.
3. **Return to the last ✅ checkpoint that passed.** Everything after it is suspect.
   Re-running that checkpoint tells you where reality diverged from your notes.

---

## 2. Python and environments (Module 02 onward)

| Symptom | Likely cause | Fix |
|---|---|---|
| `'python' is not recognized` 🪟 | The Windows Store alias intercepts `python` | Use `py -3 --version`; install Python from python.org and tick *Add to PATH*; restart the terminal afterwards |
| Wrong Python version used | Multiple installations / wrong PATH order | `py -0` lists installs; use `py -3.12` explicitly or recreate the virtual environment with it |
| Virtual environment not activating 🪟 | Execution policy or wrong shell | Use `.\.venv\Scripts\Activate.ps1`; if blocked, open a new terminal rather than weakening policy globally |
| `ModuleNotFoundError: <name>` | Package installed into a different environment than the one running | Confirm `python -m pip show <name>` and `python -c "import sys; print(sys.executable)"` point at the same environment |
| pip fails with SSL/proxy errors | Corporate network, proxy, or VPN | Retry with `python -m pip install --upgrade pip`; if behind a proxy, configure pip's proxy setting rather than copying wheels from elsewhere |
| Two packages fight over versions | Loose version ranges | Reproduce from the lock file (Module 02 teaches this); do not hand-edit version pins to silence errors |

## 3. Git and GitHub (Module 02 onward)

| Symptom | Likely cause | Fix |
|---|---|---|
| `'git' is not recognized` | Not installed, or PATH not refreshed | Close and reopen the terminal; if still failing, reinstall Git for Windows with *Use Git from the command line* selected |
| Every line shows `^M` in diffs | Windows/Unix line-ending mismatch | Set `core.autocrlf` as the course describes and re-add the files; this is a one-time setup issue |
| Push rejected (`non-fast-forward`) | Someone (often you, in another window) committed first | `git pull --rebase` first, resolve, then push; never force-push to shared work |
| A file you expected to be tracked is missing | `.gitignore` rule, or it was never added | Check `git status --ignored`; add the file deliberately |
| Secret committed by mistake | Copied a key into config | Remove it from code **and** rotate the key; scanning and the correct pattern are taught in Modules 12 and 15 |

## 4. Data and training (Modules 04–06)

| Symptom | Likely cause | Fix |
|---|---|---|
| CSV column read as wrong type | Locale decimal commas, empty strings, BOM | Check `df.dtypes` and the first bytes of the file; specify `dtype`/`encoding` explicitly |
| Validation passes locally, fails in the lab | Different input file used | Compare checksums; the lab's ✅ step states which file to use |
| Two runs differ despite the same seed | Unseeded steps, parallelism, library version differences | Seed every stochastic step; pin versions; re-run with a single thread to isolate |
| Metrics look too good | Leakage or an evaluation mistake | Check that nothing derived from the target is in the features (M05); re-evaluate on a held-out split |
| DVC/`dvc repro` re-runs everything | Inputs changed, or outputs not declared | Inspect `dvc status`; verify file hashes match what the stage expects |

## 5. Tests, pipelines, and automation (Modules 07–08, 12–13)

| Symptom | Likely cause | Fix |
|---|---|---|
| `pytest: command not found` | Not installed in the active environment | `python -m pytest` always uses the right environment — prefer it |
| Tests pass locally, fail in CI | Different working directory, environment, or hidden file | Reproduce with a clean checkout; make the test depend only on committed files |
| `make` unavailable 🪟 | Make is not part of Windows | Use the PowerShell/bash alternative the lab gives, or run it under WSL/Git Bash |
| A pipeline re-runs every stage | Missing or wrong dependency declaration | Check your dependency graph's declared inputs/outputs (M08) |
| Workflow fails instantly with a YAML error | Indentation or a colon inside an unquoted string | Validate the YAML; GitHub shows the offending line in the run summary |

## 6. Serving and containers (Modules 10–11)

| Symptom | Likely cause | Fix |
|---|---|---|
| `address already in use` | A previous process still holds the port | Find it (`Get-NetTCPConnection -LocalPort 8000` 🪟 / `lsof -i :8000` 🐧) and stop that process, or start on another port |
| API works, tests fail | Tests running against a different URL/environment | Check the base URL the tests use and that the server is actually running |
| Docker daemon not running / WSL error | Backend not started or WSL 2 missing | Start Docker Desktop; if WSL errors persist, install/update WSL 2 as described in the prerequisites |
| Image builds on one machine, fails on another | Unpinned base image or a file outside the build context | Pin the base image by version/digest; check `.dockerignore` and build context |
| Container starts then exits | The process crashes on boot | Read `docker logs <name>` — the reason is in there, not in the build |

## 7. This website (MkDocs)

| Symptom | Likely cause | Fix |
|---|---|---|
| `mkdocs: command not found` | Dependencies not installed | Install from the dependency file — see [local preview](../reference-guides/local-preview.md) |
| Build warning about a link | A link points to a file outside `docs/` or to a renamed file | Fix the relative path; `mkdocs build --strict` turns warnings into failures |
| Page looks unstyled | Assets not built yet | Run `mkdocs serve` rather than opening Markdown files directly in a browser |
| A page exists but is missing from the menu | Not listed in `nav` | Add it to `mkdocs.yml` under the right section |

---

## 8. When nothing works

1. **State the problem precisely** in one sentence: *"When I run X, I expect Y, but
   I get Z."* Half of all fixes happen at this step.
2. **Check the last ✅ checkpoint you actually ran** (not the one you remember).
3. **Search the exact error text**, then the official docs page for the tool.
4. **Ask well**: include the exact command, the exact error, your OS, and what you
   already tried. Vague questions get vague answers.
5. **Report course bugs**: if the lab itself is wrong — a step that cannot work, a
   missing file, an expected output that never appears — that is our bug. Report it
   as a repository issue with the module number and step.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*
