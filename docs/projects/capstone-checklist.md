# Capstone task checklist

**Deliverable 2 of the capstone set.** Copy this into your repository as
`CHECKLIST.md` and tick items **with an evidence path** next to each — an
unticked box without a file is an ungraded claim. Milestones mirror the
[course project map](../syllabus/course-project-map.md); progress also
appears on the [progress checklist](../start-here/progress-checklist.md).

Legend: `evidence:` = file/log that proves it · `⚠️` = label honestly if
not executable on your machine.

---

## C1 — Proposal (by end of Module 06)

- [ ] Problem statement: who decides what, using this output (human in loop)
- [ ] Five selection rules checked off ([specification §2](capstone-specification.md))
- [ ] Success metric + floor written into `config.yaml` **before any training**
- [ ] Dataset source/licence recorded (or generator design for synthetic)
- [ ] Top-5 risks drafted (becomes the risk register seed)
  `evidence: proposal.md, config.yaml`

## C2 — Data foundation (by end of Module 08)

- [ ] `generate_data.py` or licensed download documented and deterministic
- [ ] Validation refuses a mutated row (test showing refusal)
- [ ] Data hash recorded; leakage-guard columns asserted
- [ ] First quality report (`report.md` or validation output)
  `evidence: data hash, refusal test, validation report`

## C3 — Training + tracking (by end of Module 09)

- [ ] Reproducible pipeline: same seed → same artefact hash (twice)
- [ ] Train/val/test split; test consumed exactly once
- [ ] Baseline vs challenger compared on validation; winner recorded
- [ ] Run history (`runs.jsonl` / MLflow) with params + data hash
- [ ] Registry/release entry for the champion with lineage
  `evidence: run history line, metrics.json, release record`

## C4 — Tested + served (by end of Module 12)

- [ ] Test suite: data, leakage, model-gate, API, release tests
- [ ] Seeded bug → the specific test that catches it (red transcript)
- [ ] API verified live: `/health`, `/predict`, 422 on bad input
- [ ] Container builds and serves ⚠️ (or NOT RUN + reason)
- [ ] CI workflow green on the final commit; gate demonstrably blocks a bad change
  `evidence: pytest output, curl transcript, CI run, image digest`

## C5 — Automated + monitored (by end of Module 14)

- [ ] Pipeline runs unattended on a schedule (OS scheduler logs)
- [ ] Forced failure retried/logged and recoverable
- [ ] Prediction log with model version; reference window stored
- [ ] Drift report from replayed data (thresholds cited)
- [ ] Written retraining decision (2×2 matrix) with numbers
  `evidence: scheduler log, drift_report, decision.md`

## C6 — Governed + documented (by end of Module 15)

- [ ] Secret scan clean on your code; no secrets in git history of your files
- [ ] Authentication decision implemented or documented-and-accepted
- [ ] Fairness metrics reported **with caveats**; over-target → ack or fix
- [ ] Model card (7 sections) + datasheet + risk register with owners
- [ ] Incident runbook written (Module 15 challenge output)
  `evidence: scan output, model-card.md, risk-register.md`

## C7 — Defence (Module 17)

- [ ] Architecture diagram matches reality (walk it, line by line)
- [ ] **Clean-clone reproducibility run** by someone/something other than
      you; tolerance declared beforehand
- [ ] **Fault injection** detected by your tooling, recovered with
      documented commands only
- [ ] Post-incident note (timeline, cost, earlier-catcher)
- [ ] Rollback rehearsed, visible in audit history
- [ ] Design document with **≥2 rejected alternatives** (real, specific,
      conditional)
- [ ] README commands run verbatim with outputs pasted — zero lies found
- [ ] Evidence bundle complete: every claim links to a file
- [ ] [Self-assessment](capstone-self-assessment.md) filled in honestly
  `evidence: PRR.md, POSTMORTEM.md, defence.md, evidence/`

---

## Hard conditions (check before claiming done)

- [ ] **End-to-end reproducibility** reaches *meets* (clean clone, documented
      sequence, stated tolerance)
- [ ] **Automated quality gates** reach *meets* (tests + validation + ML gate
      in CI, green on final commit, one gate proven to block)

Both must pass, or the capstone is capped at *Developing* — see the
[rubric](../syllabus/assessment-framework.md#7-capstone-rubric).

## Extension box (optional, after MVP green — pick ≥1)

- [ ] Feature-store-style train/serve parity test
- [ ] RETRAIN-quadrant end-to-end rehearsal
- [ ] Orchestrator upgrade + written trade-off
- [ ] Local Kubernetes serving with `rollout undo` evidence
- [ ] IaC + free-tier cloud (☁️/💲, teardown plan written **first**)

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*