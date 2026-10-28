# Capstone specification

**Deliverable 1 of the capstone set.** Read this before writing any code.
It defines scope, the sixteen required parts, the dataset rules, and the
minimum viable implementation versus optional production-grade extensions.

> Assessment is the **[capstone rubric](../syllabus/assessment-framework.md#7-capstone-rubric)** —
> a *suggested self-study framework*, not an official university grading
> scheme. Track progress on the
> [task checklist](capstone-checklist.md).

---

## 1. What the capstone is

A complete, self-built MLOps system for **a problem you choose**, that a
third party can reproduce from your repository alone — and that you can
break and recover on purpose, with evidence. It **integrates** Modules
01–16; it does not introduce tools the course never taught.

Working through it: [Module 17](../modules/17-capstone/index.md), with the
reference implementation in `examples/capstone-support/`.

## 2. Scenario selection (all five rules must pass)

1. **No real personal records.** Real student/patient/employee data is
   prohibited. Use synthetic generation (the `generate_data.py` pattern)
   or openly licensed public data (e.g. UCI/OpenML tabular sets).
2. **Licence written down** — dataset licence + your code licence, in the
   datasheet (Module 15).
3. **CPU-sized** — trains in minutes locally; no GPU, no paid API.
4. **Success metric fixed in advance** — a floor in config *before* the
   first training run; a gate chosen afterwards is decoration.
5. **A human makes the final decision** — the model informs, never
   decides; the model card says so.

Approved families (syllabus): student-support risk on **synthetic**
educational data · equipment-failure prediction on synthetic sensor data ·
a public tabular classification dataset.

## 3. The sixteen required parts (MVP)

| # | Part | Forged in | Minimum acceptance (measurable) |
|---|---|---|---|
| 1 | Problem statement + measurable success criteria | 01, 17 | one-page statement; metric + floor in config |
| 2 | Dataset provenance + validation | 04 | generator or licensed source documented; validation refuses a mutated row |
| 3 | Reproducible preprocessing + training | 05 | same seed → same artefact hash, demonstrated |
| 4 | Train/val/test separation + leakage prevention | 05 | forbidden columns asserted in code; test set touched once |
| 5 | Baseline model + documented metrics | 06 | baseline vs challenger compared on validation; test metrics recorded |
| 6 | Experiment tracking + model metadata | 06 | run history file/MLflow with params, metrics, data hash |
| 7 | Automated data, model, and API tests | 07 | suite green; one deliberately seeded bug proven caught |
| 8 | Artifact management + release approval | 09 | refusal without gate pass; promotion recorded; rollback rehearsed |
| 9 | REST API (FastAPI) | 10 | `/health`, `/predict`, validation errors, live-verified |
| 10 | Docker packaging | 11 | image builds & serves (or labelled NOT RUN + reason) |
| 11 | CI validation (GitHub Actions) | 12 | lint + tests + gate jobs; a bad change demonstrably blocked |
| 12 | Prediction logging + monitoring | 14 | log with model version; reference window stored |
| 13 | Drift analysis + retraining decision | 14 | drift report + performance report + a written decision |
| 14 | Rollback + recovery | 09 | rollback executed, visible in audit history |
| 15 | Security, privacy, limitations, governance | 15 | clean secret scan; auth decision documented; model card + risk register |
| 16 | Architecture diagram + full documentation | 17 | diagram matching reality; README commands all run verbatim |

## 4. Minimum viable vs production-grade extensions

**MVP = all sixteen parts**, local, free, one machine. The rubric grades
MVP; extensions are for learning depth, never at MVP's expense
([concepts §3](../modules/17-capstone/concepts.md)).

| Extension (optional, pick ≥1 after MVP is green) | Modules |
|---|---|
| Feature-store-style shared feature definitions with train/serve parity test | 09, 14 |
| Force the RETRAIN quadrant end to end (drift **and** degradation) | 14 |
| Orchestrator upgrade (Prefect/Dockerised cron) with written trade-off | 13 |
| Local Kubernetes serving: 2 replicas, probes, `rollout undo` evidence | 16 |
| IaC + free-tier cloud deployment (☁️/💲 — teardown plan **before** setup) | 16 |

## 5. Starter project structure

Bootstrap by *copying patterns*, not the reference's answers:

```
my-capstone/
├── README.md                 # every command, run verbatim, outputs pasted
├── config.yaml               # seed, features, gate floor, fairness target
├── generate_data.py          # synthetic/open data, deterministic
├── src/
│   ├── validate.py           # contract + leakage guard        (M04)
│   ├── features.py           # features + split hygiene        (M05)
│   └── train.py              # train/eval/fairness + tracking  (M05/06/15)
├── pipeline.py               # stages + gate + report          (M08)
├── tests/                    # data, leakage, model, API, release (M07)
├── service/                  # FastAPI app + entry point       (M10)
├── Dockerfile                # pinned, healthcheck             (M11)
├── monitor.py                # log → drift → performance → decision (M14)
├── release.py                # register / promote+ack / rollback (M09/15)
├── .github/workflows/ci.yml  # lint + tests + gate             (M12)
├── docs/
│   ├── model-card.md         datasheet.md  risk-register.md
│   ├── architecture.md       runbook.md
│   └── evidence/             # every claim's log/report lives here
└── evidence/                 # PRR, postmortems, transcripts, hashes
```

Each annotation `(Mxx)` is the module whose lab produced that pattern.
`examples/capstone-support/` is the worked reference for every line.

## 6. Verification commands (reproducible acceptance)

Run from a **clean clone** and record output (protocol:
[Module 17 concepts §8](../modules/17-capstone/concepts.md)):

```powershell
# 🪟 Windows — PowerShell, repository root of YOUR capstone
python generate_data.py            # deterministic; note the data hash
python pipeline.py                 # gate PASS line in report.md
python -m pytest -q                # all green; seeded-bug proof recorded
python -m ruff check .
python release.py register --note v1
python release.py promote r001     # must REFUSE if gate/fairness says so
python -m service                  # /health, /predict verified live
python monitor.py snapshot && python monitor.py log --shifted --labels
python monitor.py drift && python monitor.py performance && python monitor.py decision
python release.py rollback         # must appear in: python release.py history
```

Declare your tolerance **before** running elsewhere (e.g. AUC ±0.01).
Docker/CI steps get the honest ⚠️ label if unexecuted on your machine.

## 7. Deliverables checklist (the bundle)

- [x] This specification (completed as your own document, scenario filled in)
- [x] [Task checklist](capstone-checklist.md) — C1–C7 with evidence
- [x] Starter structure (§5) — built out in your repository
- [x] Reproducible data-generation script (`generate_data.py` pattern)
- [x] Working reference implementation to learn from (`examples/capstone-support/`)
- [x] Independent extension requirements (§4)
- [x] Automated tests + verification commands (§6)
- [x] [Rubric with measurable criteria](../syllabus/assessment-framework.md#7-capstone-rubric)
- [x] [Self-assessment + reflection](capstone-self-assessment.md)

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*