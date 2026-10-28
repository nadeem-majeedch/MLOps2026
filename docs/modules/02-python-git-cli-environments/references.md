# References — Module 02

## Official documentation (the sources of truth)

| Resource | What it is for |
|---|---|
| [Python venv](https://docs.python.org/3/library/venv.html) | Creating virtual environments — the standard library's own page |
| [Python packaging user guide](https://packaging.python.org/) | How projects declare dependencies (`pyproject.toml`) |
| [pip](https://pip.pypa.io/en/stable/) | The installer: `install`, `freeze`, `list`, `--requirement` |
| [uv](https://docs.astral.sh/uv/) | A fast, modern installer/environment manager (optional alternative — free, open source) |
| [Git](https://git-scm.com/doc) | Pro Git book (free) is the best single reference |
| [Git for Windows](https://gitforwindows.org/) | Includes Git Bash for 🐧-style commands |
| [PowerShell](https://learn.microsoft.com/powershell/) | The course's primary shell |
| [Semantic versioning](https://semver.org/) | What `1.4.2` actually promises |

## Free practice material

- [Oh My Zsh](https://ohmyz.sh/) / [PowerShell profile docs](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_profiles) — shell ergonomics, optional.
- [Learn Git Branching](https://learngitbranching.js.org/) — visual, interactive, free; excellent for the branch/merge mental model.

## Course material to keep open

- [glossary](../../glossary/index.md) — add your own wording for each new term
- [course troubleshooting](../../troubleshooting/index.md) — PATH, interpreter, and Git failures
- [resources](../../resources/index.md) — the wider curated list

## General principle vs. tool choice

| General principle | This course's choice | Alternatives |
|---|---|---|
| Isolate project dependencies | Python `venv` | conda/mamba, poetry, `uv` venvs |
| Declare dependencies in a file, not a chat message | `pyproject.toml` (+ `pip freeze` output as a lock) | `requirements.txt`, poetry.lock, uv.lock |
| Every change is recoverable | Git with small commits | any VCS — the habits transfer |
| Never commit generated files | `.gitignore` | repo-local excludes |
| One command to verify an environment | `python -c "import …"` checks in the lab | a Makefile target (Module 08) |

!!! note "Versions move, principles do not"
    Command syntax in this module was verified on Git 2.56, Python 3.14, and
    Windows 11. If a flag differs on your version, the official docs above are
    the authority — and tell us, so the course gets fixed.

---

[← Troubleshooting](troubleshooting.md) · [Module overview](index.md) · [Next: Module 03 →](../03-ml-project-technical-debt/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*