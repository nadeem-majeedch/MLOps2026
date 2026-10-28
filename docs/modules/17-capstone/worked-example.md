# Worked example — Module 17: one chain, executed

Every transcript below was captured while running the reference
implementation [`examples/capstone-support/`](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/capstone-support)
on the authoring machine (Windows 11, Python 3.14). Two items are **not**
executed there and are marked ⚠️ — they are yours to run (or the
instructor's, after a push). Nothing here is simulated.

---

## 1. The chain in one folder

```
capstone-support/
 generate_data.py ─► data/support.csv ─► src/validate.py ─► src/train.py ─► pipeline.py
                                   (2 provenance)      (4 split hygiene)   (3,5 + gate)
                                                                                │
 tests/ ◄─── 7          service/ ◄── 9          Dockerfile ◄── 10            report.md
 (30 passed)            (FastAPI)               (⚠️ build)                   (hashes)
      │                       │
 .github/workflows/capstone.yml (11 ⚠️ runs on GitHub)      monitor.py (12,13,14)
      │                                                            │
 release.py ◄── 8  (register → refuse → ack → promote → history)   decision.md
```

## 2. Link 1–5: provenance → validation → training → gate

```powershell
python generate_data.py
python pipeline.py
```

**REAL output:**

```text
pipeline: generate -> validate -> train -> gate -> report

[1/5] generate  RUN ... ok (0.00s)
[2/5] validate  RUN ... ok (2.51s)
[3/5] train     RUN ... ok (0.68s)
[4/5] gate      RUN ... ok (0.00s)
[5/5] report    RUN ... ok (0.00s)

pipeline complete - see report.md (data sha e814c91e3b33b2cd, metrics 9812feb999079165)
```

The generated `report.md` (REAL excerpt) shows the discipline the earlier
modules demanded — **model selection on validation, test touched once**:

```text
**Gate:** PASS  (roc_auc 0.7662 vs floor 0.75)

| family             | validation roc_auc |
| logistic           | 0.7575             |
| gradient_boosting  | 0.7324             |
**Winner:** logistic · operating point threshold=0.25

| metric    | roc_auc | accuracy | precision | recall | f1     |
| test pass | 0.7662  | 0.8233   | 0.3438    | 0.4342 | 0.3837 |

**Gap 0.1318 (target ≤ 0.1) — OVER TARGET: investigate and document before release**
```

Read that last line: the gate passes **and** the fairness audit refuses to
be silent — exactly the two-axis picture from Module 15.

## 3. Link 6–7: tracking and tests

```powershell
Get-Content runs.jsonl -Tail 1        # 🐧 tail -1 runs.jsonl
python -m pytest -q
python -m ruff check .
```

**REAL output:**

```text
{"run_id": "2026…Z", "data_sha256": "e814c91e3b33b2cd", "params": {"family": "logistic",
 "challenger": "gradient_boosting", "C": 1.0, "threshold": "auto"},
 "test_metrics": {"roc_auc": 0.7662, ...}, "gate_passed": true}

30 passed, 1 warning in 2.73s        # 5 test files: data, leakage, model, API, release
All checks passed!                   # ruff
```

(The 1 warning is an upstream Starlette deprecation notice — informational.)

## 4. Link 8: the gate that refuses

```powershell
python release.py register --note "capstone v1"
python release.py promote r001                                # ← refused
python release.py promote r001 --ack "gap documented in risk register"
python release.py history | Select-Object -Last 2
```

**REAL output:**

```text
registered r001  roc_auc=0.7662  gate=True  fairness_ok=False
  note: fairness gap 0.1318 was OVER target at registration - promotion will need --ack
refused: r001 has an OVER-TARGET fairness gap (0.1318) - promote with --ack "reason recorded for the risk register"
r001 is now serving (was None)
  risk acceptance recorded: gap documented in risk register
at=2026-10-25T22:43:48+00:00  action=register  release=r001  by=student
at=2026-10-25T22:43:48+00:00  action=promote  release=r001  by=student  ack=gap documented in risk register
```

**The capstone's governance thesis:** refusal by code, release by human
signature, both written to the audit trail.

## 5. Link 9: serving the released model

```powershell
python -m service        # separate terminal
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d "{...}"
curl -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/docs
```

**REAL output:**

```text
{"status":"ok","model_version":"r001","model_source":"releases/r001/model.joblib"}
{"model_version":"r001","threshold":0.25,
 "intended_use":"Triage aid for human counsellors on synthetic-like data. Never the
 sole basis for any decision about a student.",
 "predictions":[
   {"support_probability":0.8562,"flag_for_support":1},
   {"support_probability":0.0066,"flag_for_support":0}]}
docs=200
```

Note what the response carries: **which release** is scoring, the frozen
**threshold**, and the **intended use** — lineage and governance in the
payload, not in a wiki.

## 6. Link 10–11: container and CI — the honest pair

- ⚠️ **Dockerfile** follows Module 11's pattern exactly (pinned deps,
  layer-cached install, `HEALTHCHECK`, exec-form CMD) — but **no image was
  built on the authoring machine: Docker is not installed there**. Verify
  with `docker build -t support-api:1.0 examples/capstone-support` on a
  machine that has it.
- ⚠️ **`.github/workflows/capstone.yml`** (lint / tests / train-and-gate
  jobs, `permissions: contents: read`, no credentials) — YAML-parsed and
  validated, but **workflows only execute on GitHub after a push**. Its
  gate job fails the build if `evaluation.json` reports `passed: false`.

Labeling unexecuted steps honestly is itself part of the evidence
discipline (concepts §8) — a claim you can't back is not evidence.

## 7. Link 12–14: monitoring and the decision

```powershell
python monitor.py snapshot
python monitor.py log
python monitor.py log --shifted --labels
python monitor.py drift
python monitor.py performance
python monitor.py decision
```

**REAL output:**

```text
reference written -> monitoring_out/reference.csv
logged 400 predictions scenario=baseline labels=not yet
logged 400 predictions scenario=shifted labels=yes
  attendance_rate      psi=0.8635  strong
  prior_score          psi=0.01    stable
  lms_logins           psi=0.0215  stable
  missed_assessments   psi=1.1786  strong
  assignment_rate      psi=0.4379  strong
overall: DRIFT DETECTED -> monitoring_out/drift_report.json
  shifted    auc=0.7712 drop=-0.005 within tolerance
decision: MONITOR -> monitoring_out/decision.md
```

**The capstone's sharpest number:** three features in *strong* drift, and
measured AUC **0.7712** — *above* the 0.7662 reference (drop −0.005).
Decision **MONITOR**. Fourteen links in, the system still refuses to
confuse "the world moved" with "we got worse" (Module 14's lesson,
now load-bearing).

## 8. Link 15–16: governance and documentation in one artefact

The `--ack` in §4, the `intended_use` in §5, the fairness block in §2, and
this page's chain diagram together *are* the governance + documentation
links: a model card and risk register hang off them (see
[capstone specification](../../projects/capstone-specification.md)).
The **lineage drill** (concepts §5) answers, from files alone:

```
serving r001 → model sha e401cfa42d650b0b → metrics 9812feb999079165
             → data sha e814c91e3b33b2cd (seed 20261026) → runs.jsonl entry → git commit
```

## 9. What you should copy from this walkthrough

1. **Transcripts, not adjectives.** Every claim above has a command and
   its output.
2. **Labels on unexecuted steps** (the two ⚠️s) — they build trust rather
   than eroding it.
3. **The refusal as a feature.** The most valuable output in the whole
   walkthrough is a command that *failed* correctly.
4. **Numbers that argue.** Gate pass + fairness over + drift-without-
   degradation — three real results that together demonstrate the entire
   course's thesis.

---

[← Concepts](concepts.md) · [Next: lab →](lab.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*