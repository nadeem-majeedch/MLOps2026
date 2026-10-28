# Starter project — Intermediate

A **validated, staged pipeline** with configuration, a data contract, a
manifest and 9 tests. This is the shape of every project from Module 05
onwards.

> One of three reusable templates in `examples/starter-projects/`:
> [beginner](../beginner/) → intermediate (this) → [advanced](../advanced/).

---

## What you get

| Piece | Role |
|---|---|
| `pipeline/config.py` | loads **and validates** `config.yaml` — bad values name the key and refuse to run |
| `pipeline/data.py` | deterministic generator + a **data contract**: missing columns, nulls, out-of-range values, duplicates, schema drift, target balance |
| `pipeline/model.py` | train/evaluate, every input validated first, metrics as a plain dict |
| `pipeline/run.py` | CLI runner: declared stages, failure handling, `out/manifest.json` audit trail |
| `config.yaml` | every tunable, out of the code |
| `test_pipeline.py` | 9 tests: config, contract (4 failure modes), end-to-end run, determinism |
| `requirements.txt` | exact pins |

**Scenario:** the same churn problem as the beginner starter, now built
the way a team would build it — because *the pipeline is the product*
(Modules 05, 07, 08).

---

## Execution guide

```powershell
# 🪟 Windows — PowerShell, from this folder
python -m pip install -r requirements.txt
python -m pipeline.run --list        # ✅ generate / train
python -m pipeline.run               # ✅ both stages ok, manifest written
python -m pipeline.run               # ✅ runs again (stages are idempotent)
python -m pytest -q                  # ✅ 9 passed
python -m ruff check .               # ✅ All checks passed!
```
```bash
# 🐧 Linux/macOS
python -m pip install -r requirements.txt
python -m pipeline.run --list && python -m pipeline.run && python -m pytest -q
```

### Expected output (authoring machine, Python 3.14 — re-run it yourself)

```text
$ python -m pipeline.run
[generate] ok
[train] ok
pipeline ok — manifest -> out/manifest.json

$ python -m pytest -q
.........                                                        [100%]
9 passed in 3.81s
```

### What the manifest looks like

`out/manifest.json` records config, per-stage status and duration, row
counts, the metrics, and a short hash of the model file:

```json
{
  "started_at": "2026-10-27T02:28:07+00:00",
  "config": {"seed": 20261102, "rows": 800, "test_size": 0.25, "threshold": 0.5},
  "stages": [
    {"stage": "generate", "status": "ok", "duration_s": 0.013,
     "forced": false, "rows": 800, "output": "out\\dataset.csv"},
    {"stage": "train", "status": "ok", "duration_s": 0.153,
     "metrics": {"roc_auc": 0.8641, "accuracy": 0.87, "precision": 0.7,
                 "recall": 0.4118, "threshold": 0.5, "seed": 20261102,
                 "rows": 800},
     "model_sha": "0e7af68e50146d08"}
  ],
  "ok": true
}
```

*(verbatim from a real run on the authoring machine; your timestamps and
hash differ — that is the point of hashing.)*

## Try breaking it (this is the actual exercise)

1. Set `test_size: 1.5` in `config.yaml` → run → read the exact
   `ConfigError` message. Which key does it name?
2. Edit `pipeline/data.py`'s output by adding a column to `generate()`
   → the contract now reports *unexpected columns*. That is schema drift
   caught before training, not after deployment.
3. Add a `validate` stage to `STAGES` in `run.py` that reads
   `out/dataset.csv` and re-checks the contract. Your tests already
   cover the function; now cover the wiring.

## Cleaning up

```powershell
# 🪟
Remove-Item -Recurse out, __pycache__, .pytest_cache -ErrorAction SilentlyContinue
```
```bash
# 🐧
rm -rf out __pycache__ .pytest_cache
```

## When to graduate

Move to the [advanced starter](../advanced/) when you can explain: why
the contract is checked *twice* (at generation and before training), what
the manifest is for once CI runs this on every push, and what breaks the
moment two people run the pipeline concurrently.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../../../docs/about/index.md).*
