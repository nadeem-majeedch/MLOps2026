# Module 15 — Security, privacy, governance, fairness, and responsible deployment

!!! success "Module complete"
    Lessons, worked example, lab, independent challenge, knowledge check (with
    answers), troubleshooting, and references are all written.

**Stage:** Advanced · **Estimated effort:** 10 h · **Depends on:** 10, 14 · **Next:** 16

---

## What this module is about

Every previous module made the system *work*. This module makes it
**defensible** — to a reviewer, to a regulator, and to the people the model
scores. You audit a deliberately broken service, repair it, and measure what
the original design did to one group of students:

```
threat model ─► secret scan ─► five fixes ─► fairness measured ─► risk register
 (what can go wrong)  (find it)   (close it)   (quantify harm)     (own the rest)
```

The module's two anchoring facts, both from real runs:

> The flawed rule flagged **0.0000** of group 0 in a 400-row window — while
> scoring normally for everyone else. And the capstone still ships with an
> over-target gap of **0.1318**, because a human signed `--ack` and the audit
> history says who.

Security here is not a checklist you pass once: the scanner finds strings,
the threat model finds design flaws, and the risk register admits what
neither found.

## How to study this module (in order)

| # | File | What it does | Time |
|---|---|---|---|
| 1 | [learning-objectives.md](learning-objectives.md) | What you must be able to do, and how you prove it | 10 min |
| 2 | [concepts.md](concepts.md) | Threat models, secrets, supply chain, privacy, fairness, governance, incident response | 150 min |
| 3 | [worked-example.md](worked-example.md) | Scan → red → green → quantify, with real transcripts | 45 min |
| 4 | [lab.md](lab.md) | **Guided lab:** audit before someone else does | 150 min |
| 5 | [independent-challenge.md](independent-challenge.md) | Write and drill an incident-response runbook | 105 min |
| 6 | [knowledge-check.md](knowledge-check.md) | 10 questions with reasoning | 30 min |
| 7 | [troubleshooting.md](troubleshooting.md) | Fixture, scanner, and concept confusions | as needed |
| 8 | [references.md](references.md) | OWASP, NIST, fairlearn, model cards, gitleaks | optional |

## Before you start

- Module 10 (you have run the FastAPI service) and Module 14 (you have a
  prediction log — the fairness step uses the capstone's baseline window).
- The fixture `examples/security-lab/` ships broken **on purpose**;
  `fixed/` is yours to create.
- Free, local, no accounts. gitleaks is optional; cloud compliance services
  are ☁️ and unnecessary. Legal material is informational context only.

## Evidence you should produce

1. A one-page threat model (assets → threats → controls) for the service.
2. Scanner output before (`exit 1`, two findings) and after (`clean`) your fixes.
3. The red run (`6 failed, 1 passed`) and the green run (`7 passed`).
4. Both fairness gaps with their caveats: **0.1270** vs **0.0665**.
5. `RISK-REGISTER.md` with owners and at least one documented acceptance.
6. The challenge runbook with real drill output (`release.py history`).

---

[← Module 14: Prediction monitoring, data drift, model drift, and retraining](../14-monitoring-drift-retraining/index.md) · [Full syllabus](../../syllabus/detailed-syllabus.md#module-15-security-privacy-governance-fairness-and-responsible-deployment) · [Module 16 →](../16-cloud-kubernetes-scaling/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../../about/index.md).*