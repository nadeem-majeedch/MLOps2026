# Laboratory collection — shared harness (`examples/labs/`)

Executable material for the **20-lab laboratory collection** in
[docs/labs](../../docs/labs/index.md). Everything here is **synthetic,
deterministic, CPU-only, free, and offline**: no accounts, no credentials,
no personal data.

```
examples/labs/
├── README.md            # this file
├── make_data.py         # ONE generator for every dataset the labs need
├── data/                # generated (git-ignore-able; regenerate any time)
├── lab-01/ … lab-20/    # starter fixtures for the labs that need faulty code
└── solutions/           # REFERENCE SOLUTIONS — attempt the lab first!
```

## Quick start (any OS)

```powershell
# 🪟 Windows — PowerShell, from examples/labs
python make_data.py          # writes data/*.csv (deterministic, seeded 2026)
python make_data.py --check  # verifies regeneration is byte-identical
```

🐧 Linux/macOS: identical commands.

## Which labs have starter code here

| Lab | Folder | What ships broken / partial (the point of the exercise) |
|---|---|---|
| 01 | `lab-01/` | `train_nondeterministic.py` — two runs, two answers |
| 02 | `lab-02/` | `analysis_monolith.py` — a "notebook export" spaghetti |
| 03 | `data/customers_dirty.csv` | missing values, bad ranges, duplicates, schema drift |
| 04 | — | uses `data/customers_clean.csv` + git + hashes (no fixture) |
| 05 | `lab-05/` | `pipeline_flawed.py` — outputs differ run to run |
| 06 | — | MLflow local runs over `data/customers_clean.csv` |
| 07 | `lab-07/` | `leaky_model.py` — three leakage defects, on purpose |
| 08 | `lab-08/` | `quality_gate.py` — a gate students must finish + `bad_model.json` |
| 09 | `lab-09/` | `stager.py` — release-candidate staging without integrity checks |
| 10 | `lab-10/` | `train_model.py` (produces the model) + acceptance tests |
| 11 | `lab-11/` | `broken_service.py` — real validation bugs, replay script included |
| 12 | — | Dockerfile for the lab-10 service (build locally if Docker exists) |
| 13 | `lab-13/` | `legacy_numpy_code.py` + pins — a genuine version incompatibility |
| 14 | — | workflow file (YAML-validated here; runs only after *you* push) |
| 15 | `lab-15/` | `gate_lab.py` — release validation students complete |
| 16 | `lab-16/` | `tick_runner.py` — schedule + retry + log (runs anywhere) |
| 17 | — | analysis of `examples/capstone-support/monitoring_out/` logs |
| 18 | `lab-18/` | `runs_ledger.py` + two release candidates — decide, then roll back |
| 19 | — | audits `examples/security-lab/flawed/` from a deployment angle |
| 20 | — | fault injection into `examples/capstone-support/` |

Labs **without** a folder reuse the existing example projects
(`examples/churn`, `examples/capstone-support`, `examples/security-lab`) —
each lab names its sources in its *Setup* section.

## Rules this harness obeys

1. **Everything here was executed on the authoring machine** (Windows 11,
   Python 3.14) before being written up — labs state expected output from
   real runs. Anything not executed (Docker builds, GitHub Actions,
   Kubernetes) is labelled ⚠️ *NOT RUN* in the lab and the README.
2. **No secrets, no personal data.** The fake values in fixtures are
   obviously fake (`prod-secret-…` patterns are avoided so nothing
   resembles a real credential).
3. **Reference solutions live in `solutions/` only** — never linked from
   a lab's task steps. Open them *after* you attempt the work.
4. Regenerate everything at any time with `python make_data.py`; delete
   `data/` freely.

## Verification status (authoring machine)

| Item | Status |
|---|---|
| `make_data.py` (all datasets, byte-identical re-run) | ✅ executed |
| lab fixtures 01, 02, 03, 05, 07, 09, 10, 11, 13, 15, 16, 18 | ✅ executed (fault reproduced, fix verified) |
| lab 06 (MLflow 3.17.2), 17 (monitoring logs) | ✅ executed against installed tools |
| lab 12 (Docker), 14 (GitHub Actions), k8s parts | ⚠️ NOT RUN here — no Docker; CI runs only after a push |
| solutions' verification commands | ✅ executed per lab (see `solutions/README.md`) |

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../../docs/about/index.md).*