# Module 17 — Advanced MLOps capstone integrating the entire lifecycle

!!! success "Module complete"
    The capstone documentation is written: objectives, concepts, a verified
    end-to-end walkthrough, the production readiness review lab, the project
    brief, knowledge check (with answers), troubleshooting, and references —
    supported by the working reference implementation in
    `examples/capstone-support/` and the deliverables under
    [Projects](../../projects/index.md).

**Stage:** Advanced · **Estimated effort:** 20–25 h · **Depends on:** all of 01–16 · **Ends the course**

---

## What this module is about

Sixteen modules forged fourteen links. This module **welds them together**
— and then proves the chain holds, under review and under fault.

```
data ─► validate ─► train ─► gate ─► tests ─► release ─► API ─► container ─► CI
                                          │                              │
           governance, documentation, lineage ◄──────────────────────────┘
                                          │
            schedule ─► monitor ─► drift ─► decision ─► retrain / rollback
```

You meet two things in this module:

1. **A working reference implementation** (`examples/capstone-support/`) —
   a complete chain, executed, with real transcripts in
   [worked-example.md](worked-example.md) (including its honest ⚠️
   unexecuted steps: the Docker build and the GitHub Actions run).
2. **Your own capstone** — a different problem, your data, your decisions,
   graded against the
   [capstone rubric](../../syllabus/assessment-framework.md#7-capstone-rubric),
   guided by the [specification](../../projects/capstone-specification.md)
   and [checklist](../../projects/capstone-checklist.md).

No new tools appear here — five operating terms do:
**production readiness review, SLO, runbook, post-incident review,
end-to-end lineage.**

## How to study this module (in order)

| # | File | What it does | Time |
|---|---|---|---|
| 1 | [learning-objectives.md](learning-objectives.md) | What you must be able to do, and how you prove it | 10 min |
| 2 | [concepts.md](concepts.md) | The 14-link chain, MVP vs production, scenario rules, lineage, defence writing | 140 min |
| 3 | [worked-example.md](worked-example.md) | The reference chain executed — real transcripts end to end | 60 min |
| 4 | [lab.md](lab.md) | **Guided lab:** production readiness review + fault injection | 180 min |
| 5 | [independent-challenge.md](independent-challenge.md) | **The capstone project** (C1–C7) + independent extensions | 20–25 h |
| 6 | [knowledge-check.md](knowledge-check.md) | 10 integration questions with reasoning | 40 min |
| 7 | [troubleshooting.md](troubleshooting.md) | Integration, review, and scope problems | as needed |
| 8 | [references.md](references.md) | Map to every module's sources + defence literature | optional |

## Before you start

- Modules 01–16 complete (this module integrates, it does not re-teach).
- Reference runnable: `python generate_data.py && python pipeline.py` →
  gate PASS, `python -m pytest -q` → **30 passed**.
- **Free, local, ordinary computer** for the whole graded path. Cloud /
  Kubernetes deployment is an **optional ☁️/💲 extension** with a
  teardown plan written first. No real personal data, ever.

## Evidence you should produce (the final portfolio)

1. `PRR.md` — completed review with real outputs and honest NOT RUN rows.
2. ≥3 filed issues: one repaired (red→green), one accepted with owner.
3. Fault-injection transcript + `POSTMORTEM.md`.
4. Rollback rehearsal visible in `release.py history`.
5. Your own capstone: 16 parts, evidence bundle, design defence with
   ≥2 rejected alternatives, self-assessment form.

---

[← Module 16: Cloud deployment concepts, Kubernetes, scaling, and reliability](../16-cloud-kubernetes-scaling/index.md) · [Full syllabus](../../syllabus/detailed-syllabus.md#module-17-advanced-mlops-capstone-integrating-the-entire-lifecycle) · [Projects →](../../projects/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../../about/index.md).*