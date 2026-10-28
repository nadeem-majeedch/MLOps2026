# Knowledge check — Module 14

## How to use this

1. Answer in writing, closed book on the second pass.
2. Mark with the [answers](#answers) only after committing.
3. Target **80% with justified reasoning**; below that re-read
   [concepts.md](concepts.md) §§1–§6 — this module's reasoning is its core
   skill.
4. Suggested self-study framework, not an official exam:
   [assessment framework](../../syllabus/assessment-framework.md).

---

## Questions

**Q1.** Name the four questions of the monitoring chain, in order, with the
artifact that answers each.

**Q2.** *(True/False + why)* "Strong drift detected → retrain immediately."

**Q3.** Define **covariate shift** vs **concept drift**. Which one can the
drift report detect without labels, and which requires `actual`?

**Q4.** The lab's baseline window measured AUC 0.6902 while the reference test
set measured 0.7163 (same model, floor 0.70). Explain the gap with three
numbers, and name the alert-design consequence.

**Q5.** Why is only `performance.py` permitted to claim "the model is wrong"?
What must exist before it can run at all?

**Q6.** Fill the matrix: for each cell give the action and one sentence why.

| drift? | degraded? | action |
|---|---|---|
| no | no | ? |
| yes | no | ? |
| no | yes | ? |
| yes | yes | ? |

**Q7.** In the shift window, AUC **rose** (0.7578) under strong drift. Give the
statistical reason (`P(X)` vs `P(Y|X)`), and one realistic production
situation with the same shape.

**Q8.** What are the two tripwires for `degraded`, and why does the design use
both instead of the floor alone?

**Q9.** List the retraining loop's steps from decision to promotion, and name
the step that must be done **before** promoting.

**Q10.** Your drift report fires every single day for two weeks. State the
conceptual problem (with the term) and the first two things you would check.

---

## Answers

**Q1.** (1) *What did we predict?* → `predictions.jsonl`; (2) *Did inputs
change?* → drift report; (3) *Did accuracy fall?* → performance report;
(4) *Should we retrain?* → `decision.md` with the human checklist. The order
is the design: later questions may only use evidence from earlier ones. *(5/5)*

**Q2. False.** Drift proves the input distribution moved — nothing about
correctness. Our own `shift` window showed strong drift (PSI 0.5877) **and**
improved AUC (0.7578); retraining there would have burned a day to fix a
non-problem, and cheapened the next real alert. The decision is **MONITOR**
until labels disagree. *(5/5)*

**Q3.** *Covariate shift*: `P(X)` changes (inputs differ from training).
*Concept drift*: `P(Y|X)` changes (the relationship itself changed). The drift
report detects covariate shift only (it never sees labels); concept drift
requires `actual` — it shows up as falling AUC *without* necessarily moving
`P(X)` (the INVESTIGATE quadrant). *(5/5)*

**Q4.** Reference test AUC **0.7163**, window AUC **0.6902**, floor **0.70** —
a 0.026 gap from sampling only 400 rows differently, straddling a floor set
0.016 below the true value. Consequence: any single-window threshold near the
floor will false-alarm at this sample size — use effect-size + drop thresholds,
larger/multiple windows, or confirm over consecutive windows before alerting. *(5/5)*

**Q5.** Because its authority comes from **ground truth**: it joins predictions
to `actual`. Without labels it cannot run at all — it raises "no labelled
records yet". Every other component speaks about *inputs* or *process*;
conflating those with accuracy is precisely the error this module prevents. *(5/5)*

**Q6.** no/no → **KEEP** (nothing moved, nothing fell); yes/no → **MONITOR**
(drift is a reason to look, not to act — prove harm first); no/yes →
**INVESTIGATE** (labels fell without input change → suspect labelling,
pipeline, leakage — not the world); yes/yes → **RETRAIN CANDIDATE** (two
independent evidence sources agree; full loop + rollback first). *(5/5)*

**Q7.** The shift changed `P(X)` (feature mix) but left `P(Y|X)` intact — the
model's ranking function still separates classes, sometimes better in the new
region. Real example: marketing raises prices → customers' spend
distribution moves (drift), but the relationship between contract type and
churn is unchanged → accuracy holds. *(5/5)*

**Q8.** Tripwires: `auc < floor (0.70)` and `drop_vs_reference > 0.05`. Both
because each fails alone: the floor misses a model that *was* 0.95 and fell to
0.75 (still "passing", clearly broken for the business), and the drop rule
misses a model that shipped already-weak and stays weak. *(5/5)*

**Q9.** `pipe.run --clean` → gate check → `registry register` (lineage) →
stage to staging → production. **Before promoting:** the rollback path must be
known and rehearsed (`registry rollback production` present in history) — the
decision checklist enforces writing it down first. *(5/5)*

**Q10.** **Alert fatigue** — signals that never rest get ignored, so the real
incident will be missed too. First checks: (1) is it one feature repeatedly
over threshold (a measurement/schema change — Module 04 contract), and (2) is
the reference snapshot stale relative to the current regime (or re-snapshotted
after a shift — "moving the baseline"). Then compare effect sizes against the
PSI thresholds before touching them. *(5/5)*

**Scoring:** /50 → ×2 = %. **80+ ready.** 60–79: redo lab Steps 4–6.
Below 60: re-read concepts §1–§4 with the worked example's §6 table in view.

---

**Next:** [troubleshooting.md](troubleshooting.md) ·
[Module 15 →](../15-security-privacy-governance/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*