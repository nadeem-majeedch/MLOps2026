# Worked example — Module 15

Everything below is real output from the course fixture
[`examples/security-lab/`](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/security-lab)
(run on the authoring machine, Python 3.14). The walkthrough has four acts:
**scan → red → green → quantify**, and it ends with the governance decision
that ties this module to the capstone.

---

## 0. What we audit

```
examples/security-lab/
├── flawed/               # five seeded defects (the audit target)
│   ├── config.py         # defect 1: hard-coded key + DB credentials
│   └── service.py        # defects 2–5: PII logs, no auth, pickle, group threshold
├── scan_secrets.py       # two-rule, install-free scanner
├── make_model.py         # toy model.pkl + sha256 sidecar
└── tests/test_fixes.py   # skips until you create fixed/
```

## 1. The scan

```powershell
python scan_secrets.py flawed
```

```text
flawed\config.py:13: R1 sensitive assignment API_KEY = "prod-secret-2f8a1c77b4e9d0136ac5"
flawed\config.py:17: R2 credentials inside a URL: postgres://svc_admin:Tr0ub4dor-3@...

2 finding(s) in 3 file(s) - remove them, rotate the values, and move them to the
environment (lab.md step 2).
```

Exit code **1** — findings are a *failure*, so the scanner can gate CI
(Module 12's pattern). Two honest limitations, stated now:

- **Tool:** this scanner reads working-tree `.py` files. It does not walk
  git *history* — for that, `gitleaks` (free) is the standard tool.
- A clean scan proves *these two rules found nothing*. It is not a security
  certificate (threat models cover what scanners cannot see).

## 2. Red: the defects, as failing tests

```powershell
Copy-Item -Recurse flawed fixed      # 🐧 cp -r flawed fixed
python make_model.py
python -m pytest tests/test_fixes.py -q
```

```text
FAILED tests/test_fixes.py::test_config_reads_secrets_from_the_environment - ...
FAILED tests/test_fixes.py::test_unauthenticated_requests_are_rejected - Asse...
FAILED tests/test_fixes.py::test_wrong_key_is_rejected - assert 200 in (401, ...
FAILED tests/test_fixes.py::test_email_never_reaches_the_log - AssertionError...
FAILED tests/test_fixes.py::test_model_loading_is_integrity_checked - Asserti...
FAILED tests/test_fixes.py::test_threshold_does_not_depend_on_group - Asserti...
6 failed, 1 passed, 1 warning in 1.09s
```

Note the "1 passed": `test_correct_key_is_accepted` passes *for the wrong
reason* — an endpoint with **no** check accepts every key, including the
right one. That is why security suites always test the negative case too.

Reading each failure as a diagnosis:

| Failing test | Translates to |
|---|---|
| `…_environment` | secrets still in source (defect 1) |
| `unauthenticated…` / `wrong_key…` | endpoint is open (defect 3) |
| `email_never_reaches_the_log` | PII in log lines (defect 2) |
| `integrity_checked` | bare `pickle.load` (defect 4) |
| `threshold_does_not_depend_on_group` | group-dependent decision rule (defect 5) |

## 3. Green: the five fixes

The repaired copy (kept out of the repository — producing it *is* the lab)
changes exactly five things:

```python
# 1  config.py        secrets from the environment, fail loudly if missing
API_KEY = os.environ.get("SERVICE_API_KEY", "")

# 2  predict()        log the pseudonymous reference, never the email
logger.info("predict ref=%s attendance=%s", rec.student_ref, rec.attendance_rate)

# 3  predict()        require the key on every request
if not x_api_key or x_api_key != key:
    raise HTTPException(status_code=401, detail="missing or invalid API key")

# 4  load_model()     verify bytes BEFORE deserialising
actual = hashlib.sha256(target.read_bytes()).hexdigest()
if actual != expected:
    raise RuntimeError("model bytes do not match the recorded sha256 - refusing")

# 5  flag_for_support()  one threshold for everybody
THRESHOLD = 0.25
```

Verification, both commands and their real output:

```text
python -m pytest tests/test_fixes.py   ->  7 passed, 1 warning in 0.83s
python scan_secrets.py fixed           ->  clean: 3 file(s), no findings
```

And the integrity check under a tamper drill — one byte flipped in
`model.pkl`:

```text
OK: refused -> model bytes do not match the recorded sha256 - refusing to
deserialize (integrity check failed)
```

**Principle:** the tamper drill is the difference between *having a hash* and
*being protected by one*. A check that has never fired has never been tested
(Module 07's rule, restated for security).

## 4. Quantify defect 5: same window, two rules

Using the capstone's real baseline window
(`examples/capstone-support/monitoring_out/predictions.jsonl`, 400 scored
rows, groups 93 / 307), the selection-rate gap under each rule:

```text
rows: 400 counts: {0: 93, 1: 307}
group-dependent (flawed): rates={0: 0.0,     1: 0.127}  gap=0.1270
single threshold:         rates={0: 0.1935, 1: 0.127}   gap=0.0665
```

| Rule | group 0 | group 1 | gap | vs target 0.10 |
|---|---|---|---|---|
| flawed (0.25 / 0.60) | **0.0000** | 0.1270 | 0.1270 | over |
| fixed (0.25 for all) | 0.1935 | 0.1270 | 0.0665 | within |

Two readings, both required in your write-up:

1. The flawed rule flags **zero** students from group 0 — a service
   silently blind to one population. The gap is not academic.
2. The fixed rule still shows **0.0665** — residual, arising from genuine
   feature differences. Closing it to zero would itself be a *choice* with
   costs (which the caveats in concepts §5 require you to state). Within
   target ≠ fair; it means *within the definition we committed to*.

## 5. The governance decision (ties to the capstone)

The capstone's own audit is over target and **ships anyway — with a
signature**. Real output from `examples/capstone-support/`:

```text
registered r001  roc_auc=0.7662  gate=True  fairness_ok=False
  note: fairness gap 0.1318 was OVER target at registration - promotion will need --ack
refused: r001 has an OVER-TARGET fairness gap (0.1318) - promote with --ack "reason recorded for the risk register"
r001 is now serving (was None)
  risk acceptance recorded: gap documented in risk register
```

This is the module's thesis in one transcript: **governance is code that
refuses until a human takes responsibility, then writes it down.** The
engineers' options were: fix the gap, constrain the deployment, or accept it
explicitly — never "merge quietly".

---

**Your turn:** reproduce all four acts yourself in
[lab.md](lab.md). Checkpoints quote this file's outputs.

---

[← Concepts](concepts.md) · [Next: lab →](lab.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*