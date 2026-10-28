# Security lab fixture — deliberately flawed service

> **This code is broken on purpose.** It exists so Lab 15 (Module 15) can be
> audited and repaired. Never copy `flawed/` into a real system.

Five seeded defects, all documented in [flawed/service.py](flawed/service.py)
and [flawed/config.py](flawed/config.py):

| # | Defect | Where |
|---|---|---|
| 1 | Hard-coded service key + DB credentials in source | `flawed/config.py` |
| 2 | PII (email) written to logs | `flawed/service.py` `predict` |
| 3 | No authentication on the endpoint | `flawed/service.py` `predict` |
| 4 | Unverified `pickle.load` | `flawed/service.py` `load_model` |
| 5 | Group-dependent decision threshold | `flawed/service.py` `flag_for_support` |

## The lab loop (all commands from this folder)

```powershell
# 🪟 Windows — PowerShell
python scan_secrets.py flawed            # exit 1: two findings (defect 1)
python make_model.py                     # toy model.pkl for the service
Copy-Item -Recurse flawed fixed          # 🐧 cp -r flawed fixed
python -m pytest tests/test_fixes.py     # RED   - 6 failed, 1 passed
# ... apply the fixes in lab.md ...
python -m pytest tests/test_fixes.py     # GREEN - 7 passed
python scan_secrets.py fixed             # clean: no findings
```

`tests/test_fixes.py` **skips** on a fresh clone (there is no `fixed/` yet) —
that skip is the honest state of an undone exercise, not a broken build.

## Verified results (authoring machine, Python 3.14)

| Check | Result |
|---|---|
| `python scan_secrets.py flawed` | exit 1 — `R1` key assignment + `R2` URL credentials |
| `pytest` on a fresh clone | 1 skipped |
| `pytest` before fixing (`fixed/` = copy of `flawed/`) | **6 failed, 1 passed** |
| `pytest` after the five fixes | **7 passed** |
| `python scan_secrets.py fixed` | clean, exit 0 |
| Tamper test: one byte flipped in `model.pkl` | `RuntimeError: model bytes do not match the recorded sha256 - refusing to deserialize` |

## Layout

```
security-lab/
├── flawed/            # the audit target (shipped broken)
├── tests/test_fixes.py  # skip until fixed/ exists; red → green
├── scan_secrets.py    # install-free scanner (gitleaks is the optional pro tool)
├── make_model.py      # toy model.pkl + sha256 sidecar
└── README.md
```

The `fixed/` folder is **not shipped** — creating it correctly *is* the lab.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../../docs/about/index.md).*