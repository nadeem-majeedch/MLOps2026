# Starter project — Beginner

A complete, working ML project in **three files**. If you can run this and
explain every line, you are ready for the [intermediate starter](../intermediate/).

> One of three reusable templates in `examples/starter-projects/`:
> beginner (this) → intermediate → [advanced](../advanced/).

---

## What you get

| File | Role |
|---|---|
| `churndata.py` | deterministic synthetic dataset (generator + loader) |
| `config.yaml` | every tunable value, out of the code |
| `train.py` | train/test split → preprocessing → logistic regression → metrics |
| `test_starter.py` | 3 tests: schema, determinism, metric sanity |
| `requirements.txt` | exact pins, so your run matches everyone else's |

**Scenario:** a subscription business wants a baseline churn score.
The dataset is synthetic (500 rows, seed `20261101`) — no real personal
data, ever.

---

## Execution guide

```powershell
# 🪟 Windows — PowerShell, from this folder
python --version                    # ✅ 3.10 or newer
python -m pip install -r requirements.txt
python churndata.py                 # ✅ wrote data\customers.csv (500 rows, seed 20261101)
python train.py                     # ✅ metrics (see below)
python -m pytest -q                 # ✅ 3 passed
```
```bash
# 🐧 Linux/macOS
python -m pip install -r requirements.txt
python churndata.py && python train.py && python -m pytest -q
```

### Expected output (authoring machine, Python 3.14 — re-run it yourself)

```text
wrote data\customers.csv (500 rows, seed 20261101)
baseline churn model
  roc_auc      0.9142
  accuracy     0.88
  precision    0.8824
  recall       0.5357
  rows_train   375
  rows_test    125
  seed         20261101
artefacts -> out/
...
3 passed in 3.52s
```

**Read the numbers, don't just tick them:** recall 0.54 against precision
0.88 means the model misses roughly half the churners — a *fine* baseline
and a *terrible* churn-prevention tool. Naming that gap is the first
modelling judgement this course asks of you.

---

## How it is organised

```
beginner/
├── README.md          ← you are here (the execution guide)
├── requirements.txt   ← pinned dependencies
├── config.yaml        ← seed, split, threshold — no magic numbers in code
├── churndata.py       ← generate() / save() / load(); pure and deterministic
├── train.py           ← load config → train → evaluate → write out/metrics.json
├── test_starter.py    ← schema + determinism + metric-sanity tests
├── data/              ← generated (commit the CSV: it is 30 KB)
└── out/               ← generated model + metrics (never commit)
```

Rules demonstrated: **config not constants**, **pure data functions**,
**one command to reproduce** (`python train.py`), **tests that would fail
if any of that broke**.

## Cleaning up

```powershell
# 🪟
Remove-Item -Recurse data, out, __pycache__, .pytest_cache -ErrorAction SilentlyContinue
```
```bash
# 🐧
rm -rf data out __pycache__ .pytest_cache
```

## When to graduate

Move to the [intermediate starter](../intermediate/) when you can answer,
without looking: why is the split stratified? What would happen to your
metrics if `threshold` moved to 0.8? Which single line would you change to
try a different model?

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../../../docs/about/index.md).*
