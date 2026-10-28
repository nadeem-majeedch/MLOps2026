# LAB-20 — reference solution

> Attempt the lab first. This is the answer key, not the assignment.

## Verified incident transcripts (authoring machine, this session)

**Incident 1 — corrupted dataset** (`--fault data`):

```text
$ python inject_fault.py --fault data
data fault: support.csv truncated to 1799 rows and column 'attendance_rate' renamed to 'attendance_rate_v2'
backup -> backup/data.bak.<ts>   restore with --restore

$ python -m src.validate
  [FAIL] required_columns … missing: ['attendance_rate']
  … 6/8 checks passed            (exit 1)

$ python pipeline.py
[1/5] generate  RUN ... ok (0.00s)
[2/5] validate  RUN ... FAILED: data contract violated: required_columns, configured_columns_exist
[3/5] train     BLOCKED
[4/5] gate      BLOCKED
[5/5] report    BLOCKED
pipeline FAILED - fix the stage above, then rerun.
```

Recovery proof — **the same command turning green**:

```text
$ python inject_fault.py --restore
restored data <- backup/data.bak.<ts>
$ python -m src.validate     →  8/8 checks passed   (exit 0)
$ python pipeline.py         →  pipeline complete - see report.md
                              (data sha e814c91e3b33b2cd, metrics 9812feb999079165)
```

**Incident 2 — corrupted model artefact** (`--fault model`):

```text
$ python inject_fault.py --fault model
model fault: <bytes injected into artifacts/model.joblib>

$ python -c "import joblib; joblib.load('artifacts/model.joblib')"
EOFError                               ← detection path 1: it won't load

hash check: release.json model_sha256 = e401cfa42d650b0b (truncated)
            actual sha256            = 3837b945c334d441…  → MISMATCH
                                             ← detection path 2

$ python -m pytest -q
30 passed                              ← the BLIND SPOT (see below)

$ python -c "from service.app import resolve_model; print(resolve_model()['source'])"
releases/r001/model.joblib             ← serving unaffected: it loads the
                                         promoted copy, not artifacts/
```

Restore → `restored model <- backup/…`, and 8/8 + 30 passed + pipeline
complete again.

## The three questions this lab exists to answer

1. **Why did pytest stay green on a corrupted artefact?** Because the
   suite *re-trains* the model as part of its setup — the broken file is
   overwritten before any test loads it. Tests that heal the thing they
   are meant to check cannot detect its corruption. The lesson: a test
   that regenerates its subject must also assert **hash/integrity of the
   as-shipped artefact** separately (exactly what `release.json`'s
   `model_sha256` does).
2. **What is the blast radius?** Serving reads `releases/r001/…`
   (promoted, immutable-ish copy), training reads/writes
   `artifacts/…` (working copy). So a corrupted artefact breaks
   *retraining/rollback-from-artefact* but not the live endpoint —
   evidence: `resolve_model()['source']` still returns the promoted
   path. Say this split explicitly in your timeline.
3. **Why does the data fault matter more?** It is caught *upstream and
   automatically* (validate exits 1 → pipeline blocks stages 3–5), so no
   bad model can ever be produced. The model fault was caught only by
   two *manual* checks — that asymmetry is your follow-up action:
   wire the hash comparison into CI or the gate.

## Timeline structure (what earns the mark)

For **each** incident: detected-at (command + output), detected-by
(manual vs automated), blast radius (what broke / what didn't, with the
`resolve_model` evidence), recovery (exact restore command), and proof
of recovery (the same check turning green). One concrete follow-up each —
e.g. (1) add a `data_sha` assertion at pipeline start, (2) verify
`model_sha256` in the release gate / CI so corruption is caught
*without* remembering to run a command.

## Cleanup

```powershell
# 🪟 from examples/labs/lab-20
python inject_fault.py --restore       # if a fault is still injected
Remove-Item injected_state.json -ErrorAction SilentlyContinue
Remove-Item -Recurse backup -ErrorAction SilentlyContinue
```
```bash
# 🐧
python inject_fault.py --restore
rm -f injected_state.json && rm -rf backup
```

Acceptance bar: `git status` shows no `injected_state.json`, no `backup/`,
and every check is green.

## Common wrong answers

- Pasting these transcripts as your own — re-run them; the lab's rules
  (and this course's) require your machine's output.
- Calling the pytest result "the tests passed, so the artefact is fine" —
  it is the blind spot, not the confirmation.
- Restoring and skipping the re-run of the *same* command that failed —
  without that, you have a plausible story, not proof.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../../docs/about/index.md).*
