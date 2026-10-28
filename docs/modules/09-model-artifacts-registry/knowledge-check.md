# Knowledge check — Module 09

## How to use this

1. Answer in writing, closed book on the second pass.
2. Mark yourself with the [answers](#answers) only after committing.
3. Target **80% with justified reasoning**; below that re-read
   [concepts.md](concepts.md) §§1–5.
4. Self-assessment inside a suggested self-study framework — not an official
   university exam: [assessment framework](../../syllabus/assessment-framework.md).

---

## Questions

**Q1.** Name the four things that must travel together in a model artefact,
and give one concrete failure for each if it is missing.

**Q2.** *(True/False + why)* "Saving `model.pkl` is enough — everything else
can be regenerated later."

**Q3.** Your registry refuses `development → production`. State the two
different *kinds* of rule this registry enforces, with an example refusal
message for each.

**Q4.** Why is `gate=None` treated as "cannot promote" rather than "probably
fine"? Connect your answer to a real risk.

**Q5.** Describe the rollback mechanism in terms of **bytes** and **pointers**.
Why does the pointer move instead of copying files back?

**Q6.** A teammate edits `metadata.json` of a production version to fix a typo.
Explain the two ways this breaks the system's guarantees.

**Q7.** Local file registry vs remote registry service: name **two** features
you get only remotely, and **one** concept that is identical in both.

**Q8.** In one sentence each: model card, model signature, lineage.

**Q9.** The lab's model card §5 requires stating "precision@0.5 = 0". Why is
reporting that warty number an *improvement* over omitting it?

**Q10.** Your service's `/health` shows `model_version: artefact`. What does
that tell you about the registry, and what is the fix?

---

## Answers

**Q1.** (a) **fitted pipeline incl. preprocessing** — without it, raw rows are
scaled/encoded wrongly and predictions are garbage; (b) **signature** — the
caller cannot know which columns/types to send → 422s or silent misalignment;
(c) **metrics** — nobody can tell "good enough" from "any old model";
(d) **lineage** — you cannot answer which data produced it, so you cannot
reproduce or audit it. *(5/5)*

**Q2. False.** Regeneration requires the exact data bytes, config, library
versions, and code — the very things lineage records. "Regenerate later" is a
bet that your past is still intact; the artefact is what removes that bet.
(Preprocessing weights and random state cannot be regenerated from a bare
`.pkl` at all.) *(5/5)*

**Q3.** (1) **Lifecycle order** — one step at a time
(`refused: v002 is 'development' and may only move one step at a time`);
(2) **Approval gate** — quality evidence required
(`refused: v003 never passed its quality gate ... - production requires a
passed gate`). *(5/5)*

**Q4.** Unknown gate = an artefact whose quality was never measured —
promoting it converts *ignorance* into *serving*. Real risk: the version was
trained on broken data (a Module 04 defect) that the gate would have caught,
and users start receiving its predictions the moment it is promoted. *(5/5)*

**Q5.** The model bytes already exist for every version and never move;
promotion/rollback only rewrite the `production` pointer inside `index.json`.
Moving the pointer is atomic-ish, instant, and reversible; copying bytes back
would double storage, risk partial copies, and destroy the evidence that the
old release existed. *(5/5)*

**Q6.** (1) It breaks **immutability**: the hash recorded at registration no
longer matches the bytes, so lineage verification fails and "what served last
Tuesday?" becomes unanswerable. (2) It breaks **rollback safety**: if the edit
corrupts the file, the version you roll back *to* is exactly as broken as the
one you rolled back *from* — the escape hatch is compromised. *(5/5)*

**Q7.** Remote-only: multi-user **permissions/approval hooks**, and a **UI +
webhooks/aliases** for teams. Identical: **stages, promotion rules, lineage,
rollback** — the concepts this module practised. *(5/5)*

**Q8.** *Model card*: the human-facing document of intended use, limits and
evaluation. *Signature*: the machine-facing contract of expected inputs
(columns/types/ranges). *Lineage*: the traceable origin (data, config, metrics,
time, actor) of one version. *(5/5)*

**Q9.** Omitting it reports a model that *looks* deployable while hiding that
the default threshold predicts nothing — a reviewer would approve based on AUC
alone. Reporting it forces the threshold/calibration conversation now, and
demonstrates that the course measures honestly rather than decoratively. *(5/5)*

**Q10.** The registry produced no `production` pointer (empty or never
promoted), so the service fell back to the training artefact. Fix: register and
promote a version, then restart the service; `/health` should show `vNNN`. *(5/5)*

**Scoring:** /50 → ×2 = %. **80+ ready.** 60–79: redo lab Steps 3–4 and re-read
concepts §4–§5. Below 60: re-run the worked example end to end first.

---

**Next:** [troubleshooting.md](troubleshooting.md) ·
[Module 10 →](../10-model-serving-fastapi/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*