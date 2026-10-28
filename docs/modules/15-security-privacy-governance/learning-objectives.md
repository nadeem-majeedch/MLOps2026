# Learning objectives — Module 15

Maps to syllabus outcomes
[LO 15.1–15.4](../../syllabus/detailed-syllabus.md#module-15-security-privacy-governance-fairness-and-responsible-deployment).

| # | You can… | You prove it by… |
|---|---|---|
| **15.1** | Find and fix the common security failures in an ML service: leaked secrets, unauthenticated endpoints, unsafe deserialization, sensitive input smuggled into logs | Five fixes demonstrated on your `fixed/` copy: scanner clean, **7/7 fix tests green**, PII absent from captured logs, tampered model refused |
| **15.2** | Apply privacy basics — minimisation, pseudonymisation, and what must never be logged | A one-page logging policy for your service listing each field logged / not logged and why |
| **15.3** | Measure group fairness on a test case, interpret the result, and state its limits | Two selection-rate computations from the same 400-row window: **gap 0.1270** (group-dependent rule) vs **0.0665** (one threshold) — plus a paragraph on what neither number proves |
| **15.4** | Produce governance artefacts: model card, datasheet, risk register, audit trail | Your capstone's model card + risk register with owners, residual risks, and the documented `--ack` risk acceptance from `release.py` |

## Supporting skills

- Write a **threat model** in under an hour: assets, actors, entry points,
  one line per threat → one control each.
- Explain **secrets vs configuration** and why the boundary is about blast
  radius, not naming conventions.
- State the difference between *input validation*, *authentication*, and
  *authorization* — and which defect each of the lab's five bugs is.
- Describe **lineage**: why "which data and code produced the serving model"
  must be answerable in seconds, not days.
- Give the honest caveat attached to every fairness number: one metric is
  one lens, not a verdict.
- Frame legal/regulatory material (GDPR and similar) **conceptually** —
  this course gives orientation, not legal advice.

## Self-check questions

1. Your scanner comes back clean. Are you secure? What did it not look at?
2. A colleague says "our model is fair — the AUC is high". What is wrong
   with that sentence, in two sentences or fewer?
3. Model bytes changed on disk but metrics.json did not. Name the first
   control that should catch this, and where it lives.

*(Answers in [knowledge-check.md](knowledge-check.md) — attempt first.)*

---

[← Module 15 index](index.md) · [Next: concepts →](concepts.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*