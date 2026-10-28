# Lab 05 — Same seed, same model

## 1. Scenario and business problem

A regulator (or a sceptical colleague) asks: *"Prove that the model you reported
yesterday is the model you can produce today."* You have the project from Module
03/04: a dataset, a config, and a training script.

**Business problem:** if a result cannot be regenerated on demand, it cannot be
audited, debugged, or trusted — and every later guarantee (tests, CI, registries)
is built on that foundation.

## 2. Skills practised

- Running a configurable training pipeline end to end.
- Proving reproducibility with **hash comparison**, not eyeballing.
- Isolating one config change and predicting its effect before running it.
- Diagnosing a deliberately broken determinism, and explaining *why* it broke.

## 3. Prerequisites

- [concepts.md](concepts.md) read (§1–§5).
- Modules 02–04 labs completed (environment, structure, validated data).
- pandas + scikit-learn + PyYAML installed in your environment.

## 4. Required tools and estimated time

| Item | Detail |
|---|---|
| Tools | Python 3.10+, scikit-learn, PyYAML, joblib, an MD5 tool |
| Cost | Free, local, CPU-only — no GPU, no cloud, no account |
| ⏱️ Estimated time | 110 minutes |
| ⚠️ Resource-heavy | none (each run takes a few seconds) |

## 5. Input data and how to obtain it

```powershell
# 🪟 Windows / PowerShell — from examples/churn
python generate_data.py
python -m src.validate --data data/raw/churn.csv    # ✅ must be 7/7 first
```

```bash
python3 generate_data.py && python3 -m src.validate --data data/raw/churn.csv
```

✅ **Checkpoint:** `7/7 checks passed`. Never train on data that has not passed
its gate.

## 6. Directory layout

```
examples/churn/
├── config.yaml           # the experiment's full description
├── src/
│   ├── features.py       # load, transform, split
│   └── train.py          # build pipeline → fit → evaluate → persist
├── data/raw/churn.csv    # validated input (generated)
└── artifacts/            # model.joblib + metrics.json (generated, not committed)
```

## 7. Setup and execution steps

**Step 1 — Baseline run and fingerprint.**

```powershell
python -m src.train --config config.yaml --data data/raw/churn.csv
(Get-FileHash artifacts\model.joblib -Algorithm MD5).Hash.ToLower()   # 🪟
# md5sum artifacts/model.joblib                                       # 🐧
```

Expected (actual on the reference machine): metrics
`accuracy 0.91 · roc_auc 0.7163 · f1 0.0 · seed 42`; hash
`8a172026a7f5f015194cb14b6bd55159`.

✅ **Checkpoint:** you wrote the hash down.

**Step 2 — Run again. Compare.**

```powershell
python -m src.train --config config.yaml --data data/raw/churn.csv
(Get-FileHash artifacts\model.joblib -Algorithm MD5).Hash.ToLower()
```

✅ **Checkpoint:** identical metrics **and** identical hash. If metrics match but
the hash differs, stop and read §10 — something is still random.

**Step 3 — Predict, then change one value.** Edit a *copy* of the config:
`seed: 42` → `seed: 4242`. Before running, write your prediction: which numbers
move, and by roughly how much?

```powershell
python -m src.train --config _seed4242.yaml --data data/raw/churn.csv
```

Expected (actual): `roc_auc 0.7418`, accuracy still `0.91`, seed `4242`.
✅ **Checkpoint:** compare your prediction with the result and explain any gap in
one sentence.

**Step 4 — Change the model family.**

```powershell
python -m src.train --config config.yaml --data data/raw/churn.csv --family gradient_boosting
```

Expected (actual): `roc_auc 0.6431`, `accuracy 0.9`, `f1 0.0476`.
✅ **Checkpoint:** write down which model wins on which metric — and on the metric
you would defend to a business.

**Step 5 — Break determinism on purpose.** Make a copy of `src/train.py` with
`random_state=config["seed"]` removed from the model constructor (keep a copy of
the original!). Run twice, compare hashes.

Expected: metrics may still *look* close, but the hash differs run to run.

✅ **Checkpoint:** you observed a case where metrics-round-to-same but bytes-differ.
Restore the original file; confirm a clean two-run match again (Step 2).

**Step 6 — Document the config experiment.** Table in your report:

| Change | Predicted effect | Actual effect | Why |
|---|---|---|---|
| seed 42→4242 | | | |
| family logistic→gb | | | |
| removed `random_state` | | | |

**Step 7 — Prove it from a clean checkout.** Delete `artifacts/`, regenerate data
if needed, run again.

```powershell
Remove-Item -Recurse artifacts -ErrorAction SilentlyContinue
python -m src.train --config config.yaml --data data/raw/churn.csv
```

✅ **Checkpoint:** same hash as Step 1 — this is the "fresh clone" claim of the
course's reproducibility promise.

## 8. Expected outputs and verification

| Step | Expected (actual, reference machine) | Verify |
|---|---|---|
| 1 | `roc_auc 0.7163`, hash `8a172026…` | printed metrics + hash tool |
| 2 | Identical metrics and hash | side-by-side |
| 3 | `roc_auc 0.7418`, seed `4242` | printed JSON |
| 4 | `roc_auc 0.6431` for gradient boosting | printed JSON |
| 5 | Hash differs across runs | two hashes compared |
| 7 | Hash matches Step 1 | hash comparison |

> Numbers are quoted because they were *measured*, on this dataset, with these
> pinned versions. If yours differ materially with identical inputs, record your
> pandas/sklearn versions — that difference is itself a Module 02 finding.

## 9. Acceptance criteria

- [ ] Two consecutive runs: identical metrics **and** identical model hash.
- [ ] Config experiment table completed with predictions *before* results.
- [ ] Broken-determinism experiment performed and the original restored
      (final run matches Step 1's hash).
- [ ] Baseline vs. challenger written up: metric chosen, winner named, reason
      tied to the business question (not to model fashion).
- [ ] Clean-checkout run reproduces the same hash.
- [ ] All evidence filed as `modules/05/`.

## 10. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Metrics match, hashes differ | Unseeded randomness, unordered iteration, or nondeterministic parallelism | Seed every stochastic step; sort before order-dependent operations; pin library versions |
| Hash differs between machines | Different library/BLAS builds | Compare metrics with tolerance instead; reproducibility is claimed *within* a pinned environment |
| `FileNotFoundError: data/raw/churn.csv` | Wrong folder / data not generated | `Get-Location`/`pwd`, then `python generate_data.py` |
| `ModuleNotFoundError: yaml` | Wrong interpreter | `.venv\Scripts\python -m pip install PyYAML` 🪟 |
| `KeyError: 'model'` after editing config | YAML indentation broke the structure | Check nesting with `python -c "import yaml,pprint;pprint.pprint(yaml.safe_load(open('config.yaml')))"` |
| AUC wildly different from 0.7163 | Different data (regenerated/edited) or different versions | Compare data MD5 (`18df7e78…`) and `pip freeze` |
| `convergence` warnings | Model hit iteration limits | Not fatal here; if it appears, note `max_iter` in config and the warning text in your report |

More: [troubleshooting.md](troubleshooting.md) ·
[course troubleshooting](../../troubleshooting/index.md).

## 11. Cleanup

```powershell
# 🪟 from examples/churn — keep code and config, remove run products
Remove-Item -Recurse artifacts, __pycache__ -ErrorAction SilentlyContinue
Remove-Item _seed4242.yaml, _tmp.yaml -ErrorAction SilentlyContinue
python generate_data.py     # if you regenerated data, this restores known-good bytes
```

```bash
# 🐧
rm -rf artifacts __pycache__ _seed4242.yaml _tmp.yaml
python3 generate_data.py
```

✅ Verify: a fresh run reproduces hash `8a172026…`, and
`python -m src.validate --data data/raw/churn.csv` reports `7/7`.

## 12. Optional extension tasks

1. **Sweep `test_size`:** 0.1 / 0.2 / 0.3 — how much does AUC move? Write the
   sentence you would tell a manager about single-run metrics.
2. **Two datasets:** run against `churn_day2.csv` and compare — same config,
   new data. Which metrics moved, and does anything suggest drift? (Module 14.)
3. **Cross-validation:** replace the single split with 5-fold CV and compare the
   spread of AUC. What does that say about the 0.7163?
4. **Add a stage:** wire `src.validate.py` into the training entry point so
   training refuses to start on invalid data.

---

**Next:** [independent-challenge.md](independent-challenge.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*