# Starter project — Advanced

A **registry-managed model behind a validated REST API**, with prediction
logging, a drift monitor and 14 tests. This is the shape of Modules 09–14
glued together.

> One of three reusable templates in `examples/starter-projects/`:
> [beginner](../beginner/) → [intermediate](../intermediate/) → advanced (this).

---

## What you get

| Piece | Role |
|---|---|
| `train.py` | trains and writes `artifacts/` + `data/reference.csv` (the drift baseline) |
| `registry.py` | **stage → promote → verify → rollback** with recorded sha256 hashes |
| `service/app.py` | FastAPI: `/health`, `/model-info`, `/predict` — model loaded once, Pydantic contract, 422-with-fieldname errors, append-only prediction log |
| `monitor.py` | PSI drift report comparing live traffic to the reference window; `--check` exits 1 on strong drift (CI-usable) |
| `config.yaml` | service host/port + monitoring thresholds |
| `Dockerfile` | container build (**not executed on the authoring machine — no container runtime there; run it yourself**) |
| `tests/` (2 files) | 14 tests: registry lifecycle, tamper detection, HTTP contract |

---

## Execution guide

```powershell
# 🪟 Windows — PowerShell, from this folder
python -m pip install -r requirements.txt

python train.py                     # ✅ artefacts written, roc_auc 0.8793
python registry.py stage "baseline" # ✅ staged v001 (sha256 c2142718e7ae016f…)
python registry.py promote v001     # ✅ promoted v001 -> current
python registry.py verify           # ✅ v001: ok (current)

python -m pytest -q                 # ✅ 14 passed
python -m service                   # then open http://127.0.0.1:8000/docs
python monitor.py                   # after scoring traffic (see below)
```
```bash
# 🐧 Linux/macOS
python -m pip install -r requirements.txt
python train.py && python registry.py stage "baseline" && python registry.py promote v001
python -m pytest -q && python -m service
```

### Verified outputs (authoring machine, Python 3.14 — re-run them yourself)

```text
$ python train.py
advanced starter — artefacts written
  roc_auc 0.8793  rows 1200
  artifacts/model.joblib + model_info.json + data/reference.csv

$ python registry.py list
v001  current    2026-10-27T02:36:13+00:00  c2142718e7ae016f…  <- current

$ python -m pytest -q
14 passed
```

**Traffic and drift** — score 300 in-distribution records through the API,
then run the monitor:

```text
$ python monitor.py
  tenure_months      psi=0.0405  stable
  monthly_charges    psi=0.021   stable
  support_calls      psi=0.0064  stable
overall: stable — no action
```

Score a **shifted** window (charges +45, +3 support calls) and the same
tool changes its mind — and `--check` fails, which is how you would wire
it into CI:

```text
$ python monitor.py --check
  tenure_months      psi=0.0345  stable
  monthly_charges    psi=0.5589  strong
  support_calls      psi=0.1415  moderate
overall: DRIFT DETECTED — investigate before retraining
exit code: 1
```

Note what the monitor does **not** say: it cannot claim accuracy fell —
it never saw a label. That is Module 14's lesson, built into the tool's
docstring.

## The rollback drill (do this one)

```powershell
python registry.py stage "second attempt"   # stages v002 from artifacts/
python registry.py promote v002
python registry.py rollback                 # back to v001, history recorded
python -m service                           # /health now reports v001
```

`/health` showing `model_version` is the external proof that a rollback
actually reached the running service — the same observability the
capstone's rollback rehearsal requires.

## Cleaning up

```powershell
# 🪟
Remove-Item -Recurse artifacts, versions, logs, data, out, __pycache__, .pytest_cache -ErrorAction SilentlyContinue
Remove-Item registry.json -ErrorAction SilentlyContinue
```
```bash
# 🐧
rm -rf artifacts versions logs data out registry.json __pycache__ .pytest_cache
```

## Where to take it next

- Add a **quality gate**: refuse to `promote` a version whose
  `model_info.json` metrics fall below a floor (Lab 08/15 pattern).
- Add **authentication** and a **non-root user** in the Dockerfile
  (Module 15 / Lab 19).
- Swap the local `registry.py` for a remote registry and compare what
  changes — permissions and a UI, not the ideas.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../../../docs/about/index.md).*
