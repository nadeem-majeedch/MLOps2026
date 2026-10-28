# Independent challenge — Module 14

> Do this **without** step-by-step help. Target **75 minutes**.

---

## 1. The scenario

Your monitoring ran for a month and produced **four** alerts: two the team
acted on (one correctly, one wasted a day), one nobody noticed for a week, and
one that was pure noise. You have been asked to fix the *policy*, not the
charts.

## 2. Tasks

1. **Reproduce two false alarms.** Using the course's tools, produce at least
   two alert-worthy outputs that are *not* real degradation — candidates:
   self-comparison (`drift --check` of a snapshot against itself), a tiny
   window (log 30 records and measure AUC), a re-snapshotted reference after
   a shift ("moving the baseline"). For each: the output, the mechanism, and
   the one-line rule that would suppress it.
2. **Reproduce the missed alert.** Construct the *INVESTIGATE* quadrant:
   degraded labels with **no** drift (hint: keep inputs identical and change
   labels — `log_predictions.py` is editable; document your edit). Paste
   `performance` + `decision` output and explain why this case is more
   dangerous than a drift alarm, and who must own it.
3. **Threshold revision with evidence.** Take your four "alerts" (the two from
   task 1, the two decisions from the lab) and propose revised thresholds or
   an extra condition. Present as a before/after table: *alert → your rule →
   which of the four now fires*. Each change needs one sentence of
   justification and one sentence of **cost** (what genuine incident might now
   be missed?).
4. **The retraining rule, written precisely.** One paragraph defining when
   your system asks a human to retrain — it must include: minimum evidence,
   what is explicitly *not* sufficient, the rollback precondition, and who is
   notified. Then point to the exact code/decision quadrant enforcing it.
5. **Privacy pass (Module 15 preview).** Review your `predictions.jsonl`
   line-by-line for what you would *not* want leaked: name two fields at
   risk in a realistic deployment (not this synthetic set), and the logging
   change each would demand (drop / hash / aggregate / sample).

## 3. Deliverables

- `false-alarms.md` — task 1, with outputs.
- `missed-alert.md` — task 2, with outputs and your edit disclosed.
- `thresholds.md` — task 3's before/after table.
- `retraining-rule.md` — task 4.
- `privacy-notes.md` — task 5.
- Full `python -m pytest` (still green) — monitoring changes must not break
  the suite (your new threshold logic needs a test if you changed code).

## 4. Self-check (feedback criteria)

| Grade | Looks like |
|---|---|
| **Excellent (4)** | Two genuine false alarms reproduced with mechanism; INVESTIGATE quadrant real and explained; before/after table covers all four cases with costs stated; retraining rule precise and code-referenced; privacy fields concrete |
| **Proficient (3)** | Tasks 1–4 done with evidence; privacy thinner |
| **Developing (2)** | Only one false alarm; no before/after comparison |
| **Not yet (1)** | Claims without pasted outputs, or suite broken |

**The point of this challenge:** the most valuable monitoring skill is
*distinguishing a real incident from a statistical artifact* — and being able
to prove which one you have.

---

**Next:** [knowledge-check.md](knowledge-check.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*