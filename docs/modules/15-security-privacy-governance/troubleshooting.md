# Troubleshooting — Module 15

Symptom → cause → fix. Try the fixes in order; if you are still stuck, the
[course troubleshooting page](../../troubleshooting/index.md) covers
environment-level problems.

## The lab fixture

| Symptom | Likely cause | Fix |
|---|---|---|
| `pytest` prints `1 skipped` and stops | `fixed/` doesn't exist yet | Lab step 2: `Copy-Item -Recurse flawed fixed` (`cp -r flawed fixed`) |
| `ModuleNotFoundError: No module named 'fixed'` | copy made in the wrong place or inside `flawed/` | `fixed/` must be a **sibling** of `flawed/` inside `examples/security-lab/` |
| Tests fail with `FileNotFoundError: model.pkl` | `make_model.py` not run after copying | `python make_model.py` (it writes `fixed/model.pkl` + `.sha256`) |
| `test_wrong_key_is_rejected` fails: `assert 200 in (401, 403)` | endpoint still has no auth, or the check runs after the work | check `X-API-Key` **before** loading/scoring; return 401 |
| Correct key still gets 401 | comparing against a hard-coded leftover, or header name mismatch | read `os.environ["SERVICE_API_KEY"]` at request time; header is exactly `X-API-Key` |
| `test_email_never_reaches_the_log` fails although you "removed it" | email still formatted into an f-string elsewhere (or in an exception path) | grep `fixed/` for `email` and for `@` |
| `caplog.text` empty | assertions ran before the request, or logger level below INFO | wrap the **request** in `caplog.at_level(logging.INFO)` |
| `test_model_loading_is_integrity_checked` red | `pickle` present without `hashlib` + `sha256` in the source | verify the sidecar digest before `pickle.load` |
| `RuntimeError: missing digest sidecar` at runtime | `make_model.py` was run before `fixed/` existed | re-run `python make_model.py` |
| Tampered file loads without error | check placed **after** `pickle.load`, or comparison inverted | hash first, raise on mismatch, load only then |

## The scanner

| Symptom | Likely cause | Fix |
|---|---|---|
| Scanner flags `tests/test_fixes.py` | R1 sees a literal string inside a test | scan the folder under audit: `python scan_secrets.py fixed` |
| Scanner finds nothing, but you expect a finding | looking at `fixed/` (clean) instead of `flawed/` | `python scan_secrets.py flawed` → exit 1 is the correct result |
| Scanner misses a secret in git history | by design: it reads working-tree `.py` files only | use `gitleaks detect --source .` (optional, free) |
| False negative: key named `TOKEN_VALUE` | R1 matches `TOKEN` inside uppercase names — if it doesn't fire, your name may be lowercase | rename to an uppercase `*_TOKEN` constant (good practice anyway) |
| Exit code always 0 in PowerShell | not checking `$LASTEXITCODE` | `python scan_secrets.py flawed; $LASTEXITCODE` → expect `1` |

## Concepts people get stuck on

| Confusion | Resolution |
|---|---|
| "Scan is clean, so we're secure" | scanners check strings in files; the threat model (concepts §1) covers design flaws scanners cannot see |
| "A high AUC means the model is fair" | quality and fairness are independent axes — Q8 of the knowledge check |
| "Gap 0.0665 = fair" | within *one committed target* on *one window*; concepts §5 lists what it does not prove |
| "Anonymise the email in the log" | prefer not logging it; a hashed email is still linkable — pseudonymous `ref` + retention is the practical fix |
| "Legal: is this GDPR-compliant?" | this course gives informational context only — a specialist decides in real deployments |

## Getting unstuck generally

1. Re-read the checkpoint text for the failing step — the expected output
   is quoted there and in [worked-example.md](worked-example.md).
2. Run one test, verbosely: `python -m pytest tests/test_fixes.py -v`.
3. Print what you assert against (source snippets, `caplog.text`, rates) —
   the failure message tells you which of the five defects remains.
4. Still stuck → [../../troubleshooting/index.md](../../troubleshooting/index.md)
   and [references.md](references.md).

---

[← Knowledge check](knowledge-check.md) · [Next: references →](references.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*