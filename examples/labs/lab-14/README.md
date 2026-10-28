# LAB-14 scaffold — where your workflow lives (Path B)

This folder is an **optional** place to keep the GitHub Actions workflow
you write for [LAB-14 — The machine checks your work](../../../docs/labs/lab-14-the-machine-checks-your-work.md).

| File | Role |
|---|---|
| `lab-14.yml` | starter workflow — adapt it, then move it to `.github/workflows/` in *your* repository (Path A) or keep it here as your Path B deliverable |
| `CI-REHEARSAL.md` | your local proof: every command below, with its exit code |

## Rehearse locally first (both paths)

```powershell
# 🪟 Windows — PowerShell, from your lab folder
python -m ruff check .            # ✅ exit 0 (repo standard: ruff.toml)
python -m pytest -q               # ✅ your suite green
python -m pip freeze > ci-freeze.txt
```
```bash
# 🐧 Linux/macOS
python -m ruff check .
python -m pytest -q
python -m pip freeze > ci-freeze.txt
```

Reference workflows that already ship in this repository:

- `.github/workflows/ci.yml` — lint + tests + ML validation for `examples/churn/`
- `.github/workflows/capstone.yml` — the capstone's checks

**Honesty rule:** if you did not push it and did not see a green run,
your `CI-REHEARSAL.md` says `NOT RUN on GitHub`. Never invent a run URL.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../../docs/about/index.md).*
