# Starter projects — three reusable templates

Pick the tier that matches where you are; each one is complete, tested,
and documented with **real output from the machine that wrote it**.

| Tier | Folder | What it teaches | Tests | Use it for |
|---|---|---|---|---|
| 🌱 **Beginner** | [`beginner/`](beginner/) | three-file project: config, deterministic data, train, sanity tests | 3 | Modules 01–03, your first mini-project (MP1) |
| 🔧 **Intermediate** | [`intermediate/`](intermediate/) | staged pipeline, data contract, manifest, 9 tests | 9 | Modules 04–08, MP2/MP3 |
| 🚀 **Advanced** | [`advanced/`](advanced/) | model registry, FastAPI service, prediction log, PSI drift monitor, Dockerfile | 14 | Modules 09–14, MP4/MP5, capstone seed |

All three run on a laptop, CPU-only, offline, with pinned dependencies
(`requirements.txt`) and synthetic data. Nothing needs an account or a
credit card.

## Quick start (any tier)

```powershell
# 🪟 Windows — PowerShell
cd examples\starter-projects\beginner
python -m pip install -r requirements.txt
python -m pytest -q
```
```bash
# 🐧 Linux/macOS
cd examples/starter-projects/beginner
python -m pip install -r requirements.txt
python -m pytest -q
```

Each folder's `README.md` is the full execution guide, with the expected
output and a cleanup section. Generated outputs (`out/`, `artifacts/`,
`versions/`, `logs/`, `registry.json`) are git-ignored — regenerate them,
never commit them.

## How they relate to the course

The three tiers are the *same* churn problem at increasing maturity, so
you can diff them file by file:

- `beginner/train.py` ↔ `intermediate/pipeline/model.py` — identical
  modelling recipe; the intermediate version adds validation around it.
- `intermediate/pipeline/run.py` ↔ `advanced/registry.py` — both write
  an audit trail; one records pipeline stages, the other records release
  decisions.
- `advanced/service/app.py` is Modules 10–11 in one file;
  `advanced/monitor.py` is Module 14 in miniature.

When a course lab says "start from a template", start here.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../../docs/about/index.md).*
