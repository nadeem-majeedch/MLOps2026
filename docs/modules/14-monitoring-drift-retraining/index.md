# Module 14 — Prediction monitoring, data drift, model drift, and retraining

!!! success "Module complete"
    Lessons, worked example, lab, independent challenge, knowledge check (with
    answers), troubleshooting, and references are all written.

**Stage:** Advanced · **Estimated effort:** 10 h · **Depends on:** 09, 13 · **Next:** 15

---

## What this module is about

Everything so far made the model *deployable*. This module makes it
**watched** — and, crucially, makes your team competent at *not* retraining
when a chart twitches.

You will build the four-stage evidence chain in the shared example:

```
log predictions ─► drift report ─► performance report ─► decision (human approves)
 (what we scored)   (inputs moved?)  (accuracy dropped?)   (retrain / wait / investigate)
```

The module's central lesson is a distinction most dashboards blur:

> **Drift is evidence that the world changed. It is *not* evidence that the
> model got worse.** Only labels can tell you that.

Your worked example will show both cases from real runs: a window where
**strong drift** fired (PSI 0.59 on `support_tickets`) but measured AUC
*rose* — decision **MONITOR** — and a later window where drift **and** a real
AUC collapse (0.5384 vs floor 0.70) agreed — decision **RETRAIN CANDIDATE**,
with a human checklist and a rollback path before anything is promoted.

## How to study this module (in order)

| # | File | What it does | Time |
|---|---|---|---|
| 1 | [learning-objectives.md](learning-objectives.md) | What you must be able to do, and how you prove it | 10 min |
| 2 | [concepts.md](concepts.md) | What to log, drift vs degradation, thresholds, retraining policy | 130 min |
| 3 | [worked-example.md](worked-example.md) | Three real windows and the two decisions they produced | 50 min |
| 4 | [lab.md](lab.md) | **Guided lab:** detect a distribution shift and decide whether to retrain | 140 min |
| 5 | [independent-challenge.md](independent-challenge.md) | Hunt a false alarm, then design a threshold change | 75 min |
| 6 | [knowledge-check.md](knowledge-check.md) | 10 questions with reasoning | 30 min |
| 7 | [troubleshooting.md](troubleshooting.md) | No labels, noisy PSI, alert storms | as needed |
| 8 | [references.md](references.md) | Drift tests, Evidently/Whylogs, monitoring papers | optional |

## Before you start

- Module 09 (registry/rollback — the decision's final step uses it) and
  Module 13 (scheduled ticks — monitoring runs the same way).
- Understanding of Module 06's metrics and Module 08's gates.
- Free, local, no accounts — all three windows are synthetic and labelled as such.

## Evidence you should produce

1. A drift report for a shifted window (thresholds stated, not guessed).
2. A performance report proving the **drift-without-degradation** case *or*
   the degraded case — with your own numbers.
3. `decision.md` from both situations, plus one paragraph on why the first
   decision was *not* "retrain".

---

[← Module 13: Orchestration and scheduled pipelines](../13-orchestration-scheduled-pipelines/index.md) · [Full syllabus](../../syllabus/detailed-syllabus.md#module-14-prediction-monitoring-data-drift-model-drift-and-retraining) · [Module 15 →](../15-security-privacy-governance/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*