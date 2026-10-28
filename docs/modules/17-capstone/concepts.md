# Concepts — Module 17

**No new tools in this module.** The capstone is deliberately integrative:
the vocabulary below is consolidation plus five operational terms
(**production readiness review, SLO, runbook, post-incident review,
end-to-end lineage**) that describe *operating* what you built.

---

## 1. The chain the capstone integrates

Fourteen links, each forged in an earlier module — nothing here is new,
everything here is *connected*:

```
 1 problem+criteria ─► 2 data provenance ─► 3 reproducible training ─► 4 split hygiene
        (01, 17)           (04)                  (05)                  (05)
                │                                                        │
 8 release+approval ◄── 7 automated tests ◄── 6 tracking/metadata ◄── 5 baseline+metrics
        (09, 15)              (07)                  (06)                  (06)
                │
 9 REST API ─► 10 Docker ─► 11 CI validation ─► 12 scheduled runs ─► 13 monitoring ─► 14 retrain/rollback
    (10)        (11)            (12)                (13)                (14)           (09, 14)
                     ╰────────────── governance wraps every link: security, privacy,
                                    fairness, documentation (15) + diagram & docs (17)
```

Two structural rules:

- **Integration, not novelty.** If a capstone step needs a tool the course
  never taught, you have left the syllabus — justify it as an extension or
  choose a different approach.
- **Gates are the glue.** Links 4, 7, and 8 are *refusal points* (data
  validation, tests, quality gate). A chain without gates is a demo.

## 2. The reference implementation

[`examples/capstone-support/`](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/capstone-support)
is a complete, executed instance of the chain — a student-support early
warning on **synthetic** data (no real student records, openly usable,
fully local). It exists so you can *read a working integration* before
building yours:

| Link(s) | Reference file | Verified behaviour (real runs) |
|---|---|---|
| 1–2 | `config.yaml`, `generate_data.py`, `src/validate.py` | deterministic data; contract enforced |
| 3–5 | `src/features.py`, `src/train.py`, `pipeline.py` | 5-stage run → `report.md`, AUC 0.7662 ≥ floor 0.75 |
| 6 | `runs.jsonl` | one tracked line per run |
| 7 | `tests/` (5 files) | **30 passed** |
| 8 | `release.py` | refusal without `--ack`; promotion recorded |
| 9 | `service/` | `/health` `/model-info` `/predict` + Swagger, all answered live |
| 10 | `Dockerfile` | Module 11 pattern (⚠️ build not executed here — no Docker on the authoring machine) |
| 11 | `.github/workflows/capstone.yml` | lint + tests + gate jobs (⚠️ runs only after you push) |
| 12 | `monitor.py` | scheduled-tick compatible; `runs.jsonl`-style history |
| 13–14 | `monitor.py` | drift → performance → decision; **MONITOR** with real numbers |
| 15–16 | fairness audit, model card hooks, README, this page's ASCII diagram | gap 0.1318 over target → `--ack` required |

**Study rule:** the reference is *evidence of feasibility*, not a template
to fork. Your capstone must be your own problem, your own data, your own
decisions — with the reference as your integration pattern language.

## 3. MVP vs production-grade extensions

The rubric grades a **minimum viable implementation** that runs, gates,
and can be reproduced. "Production-grade" extensions deepen learning but
are *explicitly optional*:

| Dimension | ✅ MVP (graded) | 🔶 Production-grade (optional extension) |
|---|---|---|
| Execution | one machine, local, free | multi-node, cloud (☁️/💲, teardown required) |
| Data | one validated dataset, hashed | DVC remotes, feature store |
| Serving | one container, one replica | canary/blue-green, autoscaling (16) |
| Tracking | `runs.jsonl` or local MLflow | tracked server + dashboard |
| Scheduling | OS task scheduler / cron (13) | Prefect/Airflow-style orchestrator |
| Monitoring | replayed windows + decision file | live alerting, on-call rotation |
| Security | env secrets, auth on API, scan | secret manager, RBAC, pen-test |
| Tests | data/model/API/release suites | mutation testing, load tests |

**Principle:** an unproven extension scores zero while *risking* the MVP's
points. Sequence: MVP green → defence-ready → then extend.

## 4. Choosing a scenario (ethics and licence first)

Suitable families (from the syllabus): student-support risk on
**synthetic** educational data · equipment-failure on synthetic sensor data
· a public tabular classification dataset (UCI/OpenML, licence checked).

Selection checklist — all must pass **before** milestone C1:

1. **No real personal records.** Real student/patient/employee data is
   out of scope for this course, full stop. Synthetic generation
   (`generate_data.py` pattern) or openly licensed public data only.
2. **Licence stated.** Dataset licence and your code's licence written
   down (datasheet, Module 15).
3. **CPU-sized.** Trains in minutes on a laptop; no GPU, no paid API.
4. **Measurable success.** A metric floor fixed *in advance* in config —
   e.g. `roc_auc_floor: 0.75` — because a gate you chose after seeing
   results is decoration.
5. **A human in the loop.** The output informs a *person's* decision;
   the model card states it is never an automated decision about anyone.

## 5. End-to-end lineage (the examiner's first question)

**Lineage** = the answerable chain *what is serving → what produced it*,
from the repository alone:

```
release.json: current=r001
  └─ releases/r001/model.joblib      sha256 recorded at registration
      └─ artifacts/metrics.json      data_sha256 = e814c91e3b33b2cd
          └─ data/support.csv        from generate_data.py, seed 20261026
              └─ runs.jsonl          run: params, metrics, gate_passed
                  └─ git commit      config.yaml + src/ at that run
```

Every hop is a hash or a recorded id (Module 08's manifest, Module 09's
record, Module 15's audit). **The defence drill:** ask a friend to name
any release's dataset and code version; your system answers in seconds.

## 6. Operating vocabulary (the five terms this module adds)

| Term | Definition you must use correctly | Where it lives |
|---|---|---|
| **Production readiness review (PRR)** | a checklist pass over a *candidate* system that files issues instead of demoing; go/no-go with named owners | [lab.md](lab.md) — you run one on the reference, then yours |
| **SLO** (service level objective) | a numeric target on a measurable service signal over a window | your design doc — must be measurable *on a toy system* (e.g. "≥95% of scheduled runs green over 24 h", "p95 latency < 300 ms on 2-record batches, measured locally") |
| **Runbook** | numbered recovery procedure a non-author can execute | `RUNBOOK.md` — the challenge (M15) already drafted yours |
| **Post-incident review** | blameless written account: timeline, cause, preventive actions with owners | after every fault injection — including the capstone's |
| **Evidence bundle** | the set of logs/reports/artifacts your write-up links to | `evidence/` — every claim in the defence must resolve to a file |

## 7. Writing a real design defence

The rubric wants **≥2 rejected alternatives with reasons**. A rejected
alternative is a design option you seriously considered and dropped for a
named trade-off — not a strawman:

```
Alternative: MLflow server instead of runs.jsonl for tracking.
Considered because: UI + queryable history.
Rejected because: a service process to run/maintain adds a failure mode
  the MVP does not need; runs.jsonl is greppable, diffable, zero-install.
Revisit when: runs exceed ~100s of experiments or a team shares them.
```

Three properties of a good rejection: **real** (you could have used it),
**specific** (the deciding trade-off, not "complexity"), and
**conditional** (when you would change your mind).

## 8. Reproducibility protocol (LO 17.3)

**Principle:** reproducibility is a claim about *other people's machines*.
The protocol:

1. Clean clone to a directory that has never seen your venv;
2. Run **only** the documented command sequence (no folklore steps);
3. Compare against your **declared tolerance** (e.g. AUC ±0.01 —
   declared *before* the run, because declaring after is fiction);
4. Record hashes (`data_sha256`, model sha) and the git commit;
5. Anything requiring manual fixing is a bug in *documentation* — fix the
   docs, not the transcript.

The reference implementation was exercised exactly this way on its
authoring machine; every transcript in
[worked-example.md](worked-example.md) is real, and its two unexecuted
items (Docker build, GitHub Actions run) are labelled as such. Copy that
labelling discipline.

## 9. Fault injection (LO 17.4)

Break something **on purpose**, through the normal detection path, and
recover with your own runbook. Design rules:

- pick a fault your system should catch (corrupt data → gate? bad model →
  quality floor? killed process → scheduler? wrong release → rollback?);
- detection must happen via *your tooling*, not by you watching;
- recovery uses documented commands only;
- end with a post-incident note: what the fault cost, what would have
  caught it earlier.

A system that has never been broken has never been tested (Module 07's
maxim — at capstone scale).

## 10. Evidence discipline

| Counts as evidence | Does not count |
|---|---|
| command output you actually ran | "it worked when I tried it" |
| generated reports (`report.md`, `drift_report.json`) | paraphrase of a report |
| CI run URLs / logs | a workflow file that *should* run |
| `release.py history` lines | "we had rollback" |
| screenshots **plus** the underlying log | screenshot alone |

The 5%-weighted *evidence bundle quality* criterion is the multiplier on
every other criterion: unsupported claims make supported ones unverifiable.

---

[← Learning objectives](learning-objectives.md) · [Next: worked example →](worked-example.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*