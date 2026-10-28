# LAB-19 — Before Someone Else Reviews It: Deployment Security & Privacy

## 1. Lab identity

| | |
|---|---|
| **Lab ID** | **LAB-19** |
| **Difficulty / topic** | 🚀 Advanced · Security & privacy review of a deployment |
| **Prerequisite module** | [15 — Security, privacy, governance](../modules/15-security-privacy-governance/index.md) (Module 10 serving also assumed) |
| **Fixtures** | `examples/security-lab/` (the calibration target) + `examples/capstone-support/` (the deployment under review) |
| **Estimated time** | 120 minutes · free, local, offline · no accounts |

## 2. Scenario and background

Your team is about to put the student-support API (the capstone service)
in front of real users. Nobody has reviewed it for security or privacy —
it "works", the tests are green, and green tests make people brave.

You are the reviewer. You have two artifacts: a deliberately broken toy
service (`security-lab/flawed/`) you will use to **calibrate your eye**,
and the real deployment (`capstone-support/`) you must actually audit and
sign off — or refuse to sign off — in writing.

**Business problem:** the cost of finding a defect in review is measured
in minutes; the same defect found after deployment is measured in incident
response, notifications, and trust.

## 3. Learning objectives

By the end you can:

1. Run an automated secret scan and interpret a clean *and* a dirty result.
2. Perform a structured manual review: authentication, authorization,
   deserialization, logging/PII, container posture, integrity checks.
3. Separate **findings** from **accepted risks** — each with a severity,
   an owner, and a condition for re-opening.
4. Write a review verdict a team can act on: fixed now, accepted in
   writing, or blocked.
5. State what the scanner *cannot* see, and cover the gap by hand.

## 4. Prerequisites and estimated time

- Module 15 read (§1 threat modelling, §3–§4 secrets & supply chain, §6 privacy).
- LAB-10 done (you know the service's endpoints).
- **120 min** (calibrate 25 · automated scan 15 · manual review 40 ·
  verdict 25 · reflection 15).

## 5. Student task statement

Produce `security-review.md` for `capstone-support/` containing:

1. The automated scan output for **both** fixtures (dirty + clean).
2. A findings table: **ID · location · severity (H/M/L) · why it matters ·
   fix or accepted-risk justification**.
3. The list of things the scanner cannot check, with the manual evidence
   you gathered for each.
4. A verdict: **ship / ship-with-conditions / block**, signed with today's
   date and the conditions.

## 6. Required dataset and setup instructions

No dataset to download — both fixtures ship with the repository, and the
capstone data is synthetic by construction.

```powershell
# 🪟 Windows — PowerShell — from the repository root
cd examples\security-lab
python scan_secrets.py flawed        # ✅ exit 1 — 2 findings (your calibration)
python scan_secrets.py ..\capstone-support   # ✅ exit 0 — clean
```

```bash
# 🐧 Linux/macOS — from the repository root
cd examples/security-lab
python scan_secrets.py flawed                 # exit 1 — 2 findings
python scan_secrets.py ../capstone-support    # exit 0 — clean
```

## 7. Starter files

| File | Role |
|---|---|
| `examples/security-lab/scan_secrets.py` | install-free scanner (regex rules `R1`/`R2`) |
| `examples/security-lab/flawed/` | calibration target — 5 seeded defects |
| `examples/security-lab/README.md` | what each defect is and where |
| `examples/capstone-support/service/app.py` | the deployment under review |
| `examples/capstone-support/monitor.py` | prediction logging (privacy surface) |
| `examples/capstone-support/Dockerfile` | container posture |
| `examples/capstone-support/tests/test_data.py` | privacy assertions already in CI |
| `security-review.md` | **you write it** |

## 8. Numbered implementation steps

**Step 1 — Calibrate on the broken service.** Run the scanner on
`flawed/`. ✅ **Checkpoint:** exit 1, two findings — a key assignment
(`R1`) and credentials inside a URL (`R2`). Read `flawed/config.py` and
`flawed/service.py`; confirm each of the five documented defects by eye.
You now know what a real finding looks like.

**Step 2 — Scan the deployment.** Run the scanner against
`capstone-support/`. ✅ **Checkpoint:** `clean: N file(s), no findings`,
exit 0. Write down, in your own words, **what this proves and what it
does not** (the scanner only knows two patterns — everything else is
yours to check).

**Step 3 — Authentication & exposure.** Open `service/__main__.py` and
`service/app.py`. Answer with file+line evidence: what is the default
bind host? What does `HOST=0.0.0.0` in the Dockerfile change? Which
endpoints require a credential? ✅ **Checkpoint:** written finding for
"no authentication on `/predict`", graded against *where it runs*, not
in the abstract.

**Step 4 — Deserialization integrity.** Find every `joblib.load`/`pickle`
use. Then check: `release.json` records `model_sha256` — does the service
verify it before loading? ✅ **Checkpoint:** a M/H finding: recorded
integrity is useless if nothing compares it (LAB-20 demonstrates the
failure this prevents).

**Step 5 — Logging & PII.** Read `monitor.py`'s log line schema and list
every field written per prediction. Cross-check
`tests/test_data.py`: which identifier columns are *asserted absent*
from the dataset? ✅ **Checkpoint:** statement of what the log retains,
what it deliberately excludes (`student_ref` and all direct identifiers),
and what policy it still lacks (retention/rotation).

**Step 6 — Container posture.** Read the Dockerfile: is there a `USER`?
Is the base pinned? Are `data/`, logs and state excluded by
`.dockerignore`? ✅ **Checkpoint:** findings for "runs as root" (M) and
any missing pins, each with the one-line fix.

**Step 7 — Fairness & disclosure.** `release.json` carries
`fairness_within_target: false` with a recorded gap. Where else is that
surfaced — does `/model-info` disclose intended use? ✅ **Checkpoint:**
note on whether a *disclosed, documented* limitation is a finding or an
accepted risk (justify with Module 15 §7).

**Step 8 — Verdict.** Fill the findings table, assign severities, write
`security-review.md` §4: **ship / ship-with-conditions / block** with
dated conditions. ✅ **Checkpoint:** every finding is either *fixed*
(show the diff) or *accepted* (named owner + reopen condition). Nothing
is silently dropped.

## 9. Commands and expected results

| Command | Expected (authoring machine, Python 3.14) |
|---|---|
| `python scan_secrets.py flawed` | exit 1 — `R1` key assignment + `R2` URL credentials |
| `python scan_secrets.py ../capstone-support` | `clean: … no findings`, exit 0 |
| `python -m pytest tests/test_data.py -q` | 5 passed (privacy assertions hold) |
| `python -m pytest -q` (capstone root) | 30 passed |
| `python -c "from service.app import resolve_model; print(resolve_model()['source'])"` | `releases/r001/model.joblib` — the promoted copy, not `artifacts/` |

*(These are real outputs from the lab authoring machine — re-run them
yourself; never tick a box on my transcript.)*

## 10. Acceptance criteria (objective)

- [ ] Scanner run on **both** fixtures, exit codes recorded (1 and 0).
- [ ] "What the scanner cannot see" list has ≥5 entries, each with
      manual evidence (file:line or command output).
- [ ] Findings table: ≥5 findings, each with severity + fix or accepted
      risk; no finding left unowned.
- [ ] PII/logging section names the logged fields *and* the asserted-absent
      identifiers from `test_data.py`.
- [ ] Container posture reviewed (USER, pinning, .dockerignore).
- [ ] Verdict written and dated with explicit conditions.
- [ ] Repository left clean: `git status` shows no secrets, no real data.

## 11. Troubleshooting and recovery

| Symptom | Cause | Fix |
|---|---|---|
| `scan_secrets: no such path: --help` | the tool takes a path, not flags | pass a directory: `python scan_secrets.py flawed` |
| Scanner reports 0 findings in `flawed/` | wrong working directory | run from `examples/security-lab/` |
| Scanner flags *your own* file | you pasted a real-looking key while experimenting | use obvious placeholders (`…`) and never write real values |
| `service/app.py` import fails | service dependencies missing | `pip install fastapi uvicorn pydantic scikit-learn pandas joblib` |
| You cannot find any findings in the deployment | you are reviewing "does it run", not "what if it is attacked" | re-read Module 15 §1 and walk the data flow: who can call what, with what, and what happens to what they send |
| Everything is marked HIGH | severity without criteria | define your scale first (data exposure / service integrity / availability), then rate |

## 12. Reflection questions

1. The deployment scanned clean. Name one real attack this scan would
   *never* have caught, and the review step that would.
2. "No authentication" is true for both `flawed/` and `capstone-support/`
   — yet you rated them differently. Explain, precisely, what makes the
   difference (hint: bind address, network boundary, stated intent).
3. A teammate says: "the tests are green, so it's secure." Write the
   two-sentence reply.
4. Where is the boundary between *your* review and a penetration test?
   What would you tell a manager who thinks this lab IS the latter?

## 13. Optional challenge tasks

1. Add a real integrity check: verify `release.json`'s `model_sha256`
   in `resolve_model()` before `joblib.load`, with a test that corrupts
   a copy of the artifact (the LAB-20 fixture shows the failure mode).
2. Add a `USER nobody` stage to a copy of the Dockerfile and rebuild —
   confirm the API still serves (`docker build`/`run`, optional; skip
   without Docker).
3. Write the one paragraph you would paste into the pull-request
   description so the *next* reviewer knows what was already checked.

## 14. Rubric / checklist

| Points | Criterion |
|---|---|
| 3 | both scans run; exit codes and output pasted |
| 4 | ≥5 findings, severity + fix/acceptance each, no orphan findings |
| 3 | "scanner blind spots" list with manual evidence |
| 3 | PII/logging analysis grounded in `monitor.py` + `test_data.py` |
| 2 | container posture reviewed |
| 3 | dated verdict with explicit conditions |
| **18** | **total** · ≥14 = pass |

## 15. Cleanup

```powershell
# 🪟 — nothing was modified in the fixtures; just remove your report
#      (submit it first!) and any scratch copies you made.
cd examples\security-lab
Remove-Item -Recurse -ErrorAction SilentlyContinue fixed, review-scratch
```

```bash
# 🐧
cd examples/security-lab && rm -rf fixed review-scratch
```

---

**After attempting:** a reference findings table + verdict live in
[`examples/labs/solutions/lab-19/`](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/labs/solutions/lab-19).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../about/index.md).*