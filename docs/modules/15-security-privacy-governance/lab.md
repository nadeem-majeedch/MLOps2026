# Lab 15 — Audit before someone else does

## 1. Scenario and business problem

You have joined the team maintaining the support early-alert API. An internal
review is in three hours. Someone has already read the code and muttered
"this service has problems" — your job is to find them **with evidence**,
fix what you can today, and put what you cannot fix into a written risk
register with an owner.

**Business problem:** turn vague unease into a numbered, defensible audit:
scanned findings, failing→passing tests, a measured fairness gap, and a
residual-risk document. Every artefact is something a reviewer can check.

## 2. Skills practising

- Running a secret scan and reading its output without panic.
- Writing a five-line threat model (assets → threats → controls).
- Repairing: env-based secrets, PII-free logging, request authentication,
  integrity-checked deserialization, one fair decision rule.
- Turning red tests into green tests as *evidence*, not ritual.
- Measuring a fairness gap on real numbers and stating its limits.
- Producing a risk register an auditor would accept.

## 3. Prerequisites

- [concepts.md](concepts.md) read (§1–§6); Modules 10 and 14 completed
  (you have served an API and produced a prediction log).
- The capstone baseline window exists (fairness step uses it):
  ```powershell
  # 🪟 from examples/capstone-support
  python monitor.py snapshot && python monitor.py log
  ```
- Free, local, no accounts. gitleaks is **optional** (§7 extras).

## 4. Required tools and estimated time

| Item | Detail |
|---|---|
| Tools | Python 3.10+ with fastapi/pydantic/pytest (already used since Module 10) |
| Cost | Free, local, offline |
| ⚠️ Resource-heavy | none — fixture is ~100 lines, tests run in ~1 s |
| ⏱️ Estimated time | 150 minutes (including the threat-model writing) |

## 5. Input data and how to obtain it

No dataset to download: the fixture **is** the input.

```powershell
# 🪟 from examples/security-lab
python scan_secrets.py flawed        # ✅ expect: 2 findings, exit code 1
python make_model.py                 # ✅ expect: wrote flawed/model.pkl (+ .sha256)
```

🐧 Linux/macOS: identical commands.

## 6. Directory layout

```
examples/security-lab/
├── flawed/                # audit target (shipped broken)
│   ├── config.py          # defects: hard-coded key, DB credentials
│   └── service.py         # defects: PII logs, no auth, pickle, group threshold
├── tests/test_fixes.py    # skips until fixed/ exists
├── scan_secrets.py        # R1 sensitive assignment / R2 URL credentials
├── make_model.py          # toy model + sha256 sidecar
└── fixed/                 # YOU create this: cp -r flawed fixed
```

## 7. Setup and execution steps

**Step 1 — Threat model first (20 min).** On one page, answer concepts §1's
four questions *about `flawed/`* before touching any code: three assets,
five threats (one per defect, in your own words), one control each.
✅ **Checkpoint:** your fifth line reads roughly "group-dependent threshold →
one global rule + measured gap" — i.e. you predicted the lab.

**Step 2 — Scan and stage.**
```powershell
python scan_secrets.py flawed            # ✅ 2 findings, exit 1
Copy-Item -Recurse flawed fixed          # 🐧 cp -r flawed fixed
python make_model.py
python -m pytest tests/test_fixes.py -q  # ✅ RED: 6 failed, 1 passed
```
Optional industry tool (free): `gitleaks detect --source .` — compare the
finding lists and write one sentence on how they differ.
✅ **Checkpoint:** you can name why `test_correct_key_is_accepted` passes
while the service is still broken.

**Step 3 — Fix defect 1 (secrets).** In `fixed/config.py`, read
`SERVICE_API_KEY` and `DATABASE_URL` from `os.environ`; raise a clear error
if a required secret is missing. Confirm no literal survives:
```powershell
python scan_secrets.py fixed             # ✅ clean
```
✅ **Checkpoint:** `test_config_reads_secrets_from_the_environment` green.

**Step 4 — Fix defect 3 (authentication).** Require header `X-API-Key` to
equal the environment key on `POST /predict`; return **401** otherwise.
✅ **Checkpoint:** both auth tests green (`401`, `403` allowed for wrong key,
`200` for the right one).

**Step 5 — Fix defect 2 (PII in logs).** Remove `email` from every log
statement; keep only the pseudonymous `student_ref` (+ non-identifying
operational fields).
✅ **Checkpoint:** `test_email_never_reaches_the_log` green — the captured
log text contains neither `amina@example.edu` nor `amina`.

**Step 6 — Fix defect 4 (unsafe deserialization).** Before `pickle.load`,
verify `sha256(model bytes) == expected digest` from the `.sha256` sidecar
written by `make_model.py`; raise a clear `RuntimeError` on mismatch.
Tamper drill (real expected output from the course run):
```powershell
# flip one byte, then load
# RuntimeError: model bytes do not match the recorded sha256 - refusing to
# deserialize (integrity check failed)
```
✅ **Checkpoint:** `test_model_loading_is_integrity_checked` green.

**Step 7 — Fix defect 5 (group-dependent threshold).** One global threshold
(0.25) for every record; `device_access` must not influence the decision.
✅ **Checkpoint:** `test_threshold_does_not_depend_on_group` green; full run:

```text
python -m pytest tests/test_fixes.py   ->  7 passed, 1 warning in 0.83s
```

**Step 8 — Quantify the fairness gap (LO 15.3).** Using the capstone's
baseline window, compute both rules' selection rates (the exact snippet and
its output are in [worked-example.md §4](worked-example.md#4-quantify-defect-5-same-window-two-rules)):
```text
group-dependent (flawed): rates={0: 0.0,     1: 0.127}  gap=0.1270
single threshold (fixed): rates={0: 0.1935, 1: 0.127}   gap=0.0665
```
✅ **Checkpoint:** you can explain *why* group 0's flawed rate is exactly
0.0 — and write the two caveats from concepts §5 that still apply at 0.0665.

**Step 9 — Risk register (governance evidence).** Create `RISK-REGISTER.md`
with columns: risk · likelihood · impact · mitigation · **owner** · residual
status. Minimum five rows (the five defects), each marked *resolved* or
*accepted-with-reason*. Add one row for something **not** fixable today
(e.g. "no rate limiting → DoS exposure: accepted, scheduled next sprint").
✅ **Checkpoint:** no row has an empty owner; accepted rows have reasons.

## 8. Expected outputs and verification methods

| Artefact | Verification |
|---|---|
| `scan_secrets.py fixed` | `clean: 3 file(s), no findings`, exit 0 |
| fix tests | `7 passed` (from `6 failed, 1 passed`) |
| tamper drill | `RuntimeError … integrity check failed` |
| fairness computation | gaps `0.1270` → `0.0665`, groups 93/307 |
| `RISK-REGISTER.md` | five+ rows, owners, ≥1 accepted-with-reason |

## 9. Acceptance criteria (✅ Lab 15 complete)

1. Threat model page exists with assets, threats, controls — one line each.
2. Scanner exits 0 on `fixed/` and you quoted the earlier exit-1 output.
3. **All 7 fix tests pass**, and you can point to the red run before it.
4. Captured logs from a real request contain no email address.
5. Tampered model file refused, with the exact error recorded.
6. Fairness gap computed twice (0.1270 vs 0.0665) with both caveats written.
7. Risk register: owners, residual risks, one documented acceptance.

## 10. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `1 skipped` and nothing else | `fixed/` does not exist | Step 2's `Copy-Item -Recurse flawed fixed` |
| `ModuleNotFoundError: fixed` | copied inside the wrong folder | `fixed/` must sit **next to** `flawed/` |
| 401 on the correct key | key compared before env is read / header name typo | header is exactly `X-API-Key`; env `SERVICE_API_KEY` set in the test fixture |
| `caplog` empty | assertions before the request | send the request inside `caplog.at_level(logging.INFO)` |
| `integrity_checked` still red | source uses `pickle` without `hashlib`+`sha256` | verify digest *before* loading |
| scanner flags your own test file | R1 sees a literal in a string | expected — scan the folder under audit (`flawed/`, `fixed/`), not the whole repo |
| `FileNotFoundError: model.pkl` | skipped `make_model.py` | Step 2 |

More general problems: [course troubleshooting](../../troubleshooting/index.md).

## 11. Cleanup

```powershell
Remove-Item -Recurse fixed             # 🐧 rm -rf fixed   (keep it if you want the evidence)
Remove-Item flawed\model.pkl*          # 🧹 rm flawed/model.pkl*
```
Keep `RISK-REGISTER.md` — Module 17's capstone reuses it. The scanned values
in `flawed/` are **fakes on purpose**; there is nothing to rotate anywhere.

## 12. Debrief and ethics note

- You repaired five *representative* defects; real audits also cover rate
  limiting, dependency CVEs, and access control at the data layer.
- The fairness step shows a mechanism removing a **systematic exclusion** —
  that is the ethical weight behind a metric that looks like arithmetic.
- The `--ack` pattern from §5 of the worked example is about
  **accountability**: the goal is not zero risk (impossible) but *named,
  owned, decided* risk.
- Legal material in concepts §6 is informational context, not legal advice.

## 13. Stretch goals (optional)

1. Install gitleaks and scan a **cloned copy** of this repository's example
   folders — compare working-tree vs history findings.
2. Add rate limiting to `/predict` (in-memory token bucket) and a test for
   it — closing your risk register's last open row.
3. Extend `scan_secrets.py` with a third rule (e.g. private-key blocks
   `-----BEGIN`) and prove it on a fixture you build.

---

[← Worked example](worked-example.md) · [Next: independent challenge →](independent-challenge.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*