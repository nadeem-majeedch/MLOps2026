# Mini-project specifications — MP1 to MP5

Five **progressive** specifications: each extends work you already did rather
than restarting. By MP5 you own one repository that has grown across the
course — and it is the natural seed for the
[capstone](capstone-assessment.md).

> ⚠️ **Illustrative assessment design — not an official university grading
> policy.** Suggested hours and weights below are **indicative**; instructors
> adopting this material must map it to their own regulations. Every MP is
> self-assessed with the [project rubric](rubrics-checklists.md#project-rubric)
> — attempt first, then compare with the
> [reference-solution notes](keys/mini-projects-KEY.md).

**Common rules for all five**

- **Free and local:** CPU-only, synthetic or openly-licensed data, no paid
  account. Cloud extras are optional extensions, labelled as such.
- **Evidence-before-claim:** acceptance criteria are met when you can show
  the command and its output.
- **Reuse a template when it helps:** the three
  [starter projects](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/starter-projects)
  exist exactly for this — note which one you started from and what you
  changed.
- **Docs are part of the deliverable**, not an afterthought: every MP needs
  a README section that lets a stranger reproduce your result.

---

## MP1 — Reproducible project skeleton
*After Module 03 · integrates modules 01–03 · suggested 4–6 hours*

**Scenario.** You inherit (or start) an ML project that "works on my
machine". Make it work on *any* machine with one documented command.

**Deliverables**
1. Repository in the [standard layout](../COURSE-STANDARDS.md#7-target-repository-structure)
   with every folder explained in `README.md`.
2. Pinned dependency file + virtual-environment setup instructions
   (🪟 PowerShell **and** 🐧 bash).
3. One entry point that regenerates data → trains → writes metrics.
4. A `CHANGELOG`-style note of what you changed from the inherited state.

**Acceptance criteria (measurable)**
- [ ] Fresh clone + documented setup + **one command** produces the
      documented metrics output (paste both).
- [ ] No import reaches outside the repository (grep your imports and show it).
- [ ] `python -m pytest -q` green from a clean checkout (≥1 test).
- [ ] A second run of the entry point yields **identical** metrics
      (`diff` or hash proof).

**Evidence table to submit:** command, output, screenshot/diff — one row per
criterion. Template: [test-evidence](../TEMPLATES/TEST-EVIDENCE-TEMPLATE.md).

**Related practice:** [LAB-01](../labs/lab-01-reproducibility-detective.md),
[LAB-02](../labs/lab-02-untangle-the-notebook.md),
Module 03 exercises.

---

## MP2 — Tracked, justified model
*After Module 06 · integrates modules 04–06 · suggested 5–7 hours*

**Scenario.** Ten experiments are about to be run by whoever remembers
them. Make the search legible and the final choice defensible.

**Deliverables**
1. Versioned dataset (hash + how to reproduce it) and a written data-quality
   note for the version you used.
2. **≥10 tracked runs** with parameters and metrics (MLflow locally, or the
   course's tracked-runs pattern if MLflow is unavailable — say which).
3. A selection memo: baseline vs candidates, the pre-declared rule you used,
   the winner, and why.
4. Metrics on a **held-out test set** for the winner only, reported with the
   trade-offs (e.g. precision/recall, not accuracy alone).

**Acceptance criteria**
- [ ] Dataset reproducible from a documented command; hash matches.
- [ ] 10+ runs visible with parameters (export or UI screenshot).
- [ ] Selection rule written *before* the winner is announced (show it).
- [ ] Test-set numbers reported once, with baseline comparison and one stated
      limitation.

**Related practice:** [LAB-06](../labs/lab-06-ten-runs-one-decision.md),
[bank 03](question-banks/q03-experiment-tracking-evaluation.md).

---

## MP3 — Tested pipeline with a registered model
*After Module 09 · integrates modules 07–09 · suggested 6–8 hours*

**Scenario.** The tracked winner must become a *release candidate* behind
tests and a gate.

**Deliverables**
1. Pipeline with declared stages and a manifest (reuse the intermediate
   starter's pattern).
2. Test suite covering data contract, one leakage guard, metric floor, and
   pipeline behaviour; **≥80% line coverage** on your pipeline code
   (`pytest --cov`).
3. A release gate: refuses on any violated criterion, names every violation,
   exits non-zero on refusal and (deliberately) `2` on unrecognised criteria.
4. A registry entry for the candidate: version id, hash, metrics, provenance
   (which run/data), and a rehearsal of **rollback** to the previous version.

**Acceptance criteria**
- [ ] `pytest --cov` report ≥80% for pipeline code (paste the summary).
- [ ] A deliberately defective candidate is **refused** with all reasons
      listed (paste the refusal).
- [ ] Gate exits `2` when the config contains an unknown criterion (paste).
- [ ] Registry shows stage → promote → rollback history (paste `list`/`history`).

**Related practice:** [LAB-08](../labs/lab-08-the-gate-that-must-refuse.md),
[LAB-09](../labs/lab-09-staged-verified-released.md),
[LAB-15](../labs/lab-15-nothing-ships-unchecked.md).

---

## MP4 — Automated delivery
*After Module 12 · integrates modules 10–12 · suggested 6–8 hours*

**Scenario.** The registered model must be servable and guarded by machines,
not memory.

**Deliverables**
1. A FastAPI service for your MP3 model with `/health`, `/model-info`,
   `/predict`, full validation (422 + field names), and tests (≥8).
2. A Dockerfile packaging service + artefact; build/run/curl transcript
   (or a labelled **Path B** written review if no runtime — never claim an
   unrun build).
3. A CI workflow: lint + tests + lightweight ML validation, pinned actions,
   `permissions: contents: read`, artefact upload, **no secrets**.
4. A red-run demonstration: seeded defect → CI red → revert → CI green (or
   `NOT RUN on GitHub` with the full local rehearsal).

**Acceptance criteria**
- [ ] Five malformed requests all return 422 with the offending field named.
- [ ] `/health` reachable from the **host** against the container (or Path B
      review completed with labelled gaps).
- [ ] Workflow file meets every rubric row (triggers, 3 jobs, pins,
      permissions, artefacts).
- [ ] Red-then-green evidence, honestly labelled.

**Related practice:** [LAB-10](../labs/lab-10-serve-it.md),
[LAB-12](../labs/lab-12-ship-the-image.md),
[LAB-14](../labs/lab-14-the-machine-checks-your-work.md).

---

## MP5 — Monitored system
*After Module 14 · integrates modules 13–14 · suggested 6–8 hours*

**Scenario.** The system runs unattended. Prove you would *notice* when it
degrades, and that you know what you would do about it.

**Deliverables**
1. A scheduled run (Task Scheduler / cron / tick runner) that executed at
   least twice **without you triggering it**, plus proof it is removed after.
2. Prediction logging with a recorded reference window (dates included).
3. A drift report on real logged traffic — including one **deliberately
   shifted** window — and a written 2×2 decision (drift × performance) with
   the cell you landed in and why.
4. A rollback/retrain decision memo: evidence checked, decision, and explicit
   flip-conditions.

**Acceptance criteria**
- [ ] ≥2 scheduled executions with timestamps you did not trigger (paste), and
      the unschedule command shown.
- [ ] Drift output on in-distribution traffic (stable) **and** on a shifted
      window (`--check` exit 1 or equivalent).
- [ ] The memo never claims "drift ⇒ accuracy fell" without labelled
      performance numbers.
- [ ] Monitoring plan: what is alerted, thresholds with justification, and
      who is paged.

**Related practice:** [LAB-16](../labs/lab-16-a-pipeline-that-runs-itself.md),
[LAB-17](../labs/lab-17-read-the-drift-not-the-chart.md),
[LAB-18](../labs/lab-18-rollback-or-ride-it-out.md).

---

## How these are judged (illustrative)

Each MP uses the [project rubric](rubrics-checklists.md#project-rubric) with
the same four criteria — *correctness, evidence, reproducibility,
communication* — banded as Exemplary / Meets / Developing / Not yet, with the
measurable acceptance criteria above as the "Meets" line. Suggested layer
weighting for the whole course stays as published in the
[assessment framework](../syllabus/assessment-framework.md) (labs 35%,
mini-projects 25%, knowledge checks 15%, capstone 25%) — **illustrative**.

**Next:** after each attempt, read the
[reference-solution notes](keys/mini-projects-KEY.md) — they explain the
design decisions, not just the checklist — then move to the
[integrated capstone assessment](capstone-assessment.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*