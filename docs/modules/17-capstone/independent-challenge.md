# Independent challenge — Module 17: the capstone

> This is the course's final and largest piece of work: **a complete,
> self-built MLOps system** for a problem you choose. The lab reviewed a
> reference; the challenge builds yours. There is no step-by-step help —
> that is the point — but there are three documents you must not start
> without.

## 0. Read these first

1. [Capstone specification](../../projects/capstone-specification.md) —
   scope, the 16 required parts, MVP vs extensions.
2. [Task checklist](../../projects/capstone-checklist.md) — milestone by
   milestone (C1–C7), with evidence slots.
3. [Rubric](../../syllabus/assessment-framework.md#7-capstone-rubric) —
   how your own work will be graded, including the two **hard conditions**.

Track yourself on the [progress checklist](../../start-here/progress-checklist.md).

## 1. The scenario you choose

One of the approved families (specification §2), passing all five
selection rules — especially: **no real personal records**, licence
written down, trains on CPU in minutes, success metric fixed *before* you
train, and a human makes the final decision.

## 2. The 16 parts (all required for MVP)

| # | Part | Module that forged it | # | Part | Module |
|---|---|---|---|---|---|
| 1 | Problem + measurable success criteria | 01, 17 | 9 | FastAPI REST API | 10 |
| 2 | Dataset provenance + validation | 04 | 10 | Docker packaging | 11 |
| 3 | Reproducible preprocessing + training | 05 | 11 | CI validation (GitHub Actions) | 12 |
| 4 | Train/val/test + leakage prevention | 05 | 12 | Prediction logging + monitoring | 14 |
| 5 | Baseline + documented metrics | 06 | 13 | Drift analysis + retraining decision | 14 |
| 6 | Experiment tracking + metadata | 06 | 14 | Rollback + recovery | 09 |
| 7 | Automated data/model/API tests | 07 | 15 | Security, privacy, limitations, governance | 15 |
| 8 | Artifact management + release approval | 09 | 16 | Architecture diagram + full documentation | 17 |

If a part would require a tool the course never taught, you are outside
the syllabus — justify it as an extension or re-choose the approach.

## 3. Constraints (non-negotiable)

- **Free, local, ordinary computer.** No paid cloud account required for
  MVP completion. Cloud/Kubernetes = optional extension (☁️/💲, teardown
  plan written first).
- **Honest evidence only** — real transcripts, labelled NOT RUN where
  true. Fabricated logs are the one failure that invalidates everything.
- **Your own problem.** The reference implementation is a pattern
  language, not a fork: your data, your decisions, your defence.
- **Self-study assessment** — you grade yourself with the rubric; this is
  not an official university grade (see
  [assessment framework](../../syllabus/assessment-framework.md)).

## 4. Recommended rhythm (from the milestone map)

```
C1 proposal (end M06) ─► C2 data foundation (M08) ─► C3 training+tracking (M09)
        ─► C4 tested+served (M12) ─► C5 automated+monitored (M14)
        ─► C6 governed+documented (M15) ─► C7 defence+rollback (M17)
```

Each milestone lands evidence into your bundle *as you go* — assembling it
at the end is how evidence bundles become fiction.

## 5. The defence (what C7 actually is)

1. **Design document** with ≥2 *rejected* alternatives (concepts §7's
   three properties: real, specific, conditional).
2. **Reproducibility demonstration** to a third party using only the
   repository (concepts §8's protocol + declared tolerance).
3. **Fault injection** through your own detection paths, recovered with
   your runbook, followed by a post-incident note (lab Step 5's format).
4. **Evidence bundle**: every claim resolves to a file.

## 6. Independent extensions (after MVP is green — pick ≥1)

- **Feature-store-style export** (09/14): one feature definition shared by
  training and serving, with a test proving parity.
- **Force the RETRAIN quadrant** (14): degrade labels *and* drift inputs;
  drive retrain → gate → register → promote → rollback as one rehearsed
  sequence.
- **Orchestration upgrade** (13): replace the OS scheduler with
  Prefect/Dockerised cron — and write the trade-off that justified it.
- **Local Kubernetes serving** (16): your API behind 2 replicas with
  probes, `rollout undo` evidence. Path A tools required.
- **Infrastructure-as-code + free-tier cloud** (16, ☁️): teardown plan
  before setup, no paid tier.

## 7. The bar

The [rubric's](../../syllabus/assessment-framework.md#7-capstone-rubric)
hard conditions first: **end-to-end reproducibility** *and* **automated
quality gates** must both reach *meets* — anything less caps the capstone
at *Developing* regardless of total. Then weight the rest honestly,
starting from the self-assessment form
([capstone-self-assessment.md](../../projects/capstone-self-assessment.md)).

**Definition of done:** a stranger clones your repository, follows only
your documentation, watches a gate refuse a bad change, rolls something
back, and finds every claim you made — with your design defence explaining
*why*, not just *what*.

---

[← Lab](lab.md) · [Next: knowledge check →](knowledge-check.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*