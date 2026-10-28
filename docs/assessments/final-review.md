# Final review and exam-preparation guide

How to revise this whole course into something you can actually recall and
apply — whether your "exam" is a university paper, a job interview, or your
own capstone defence.

> ⚠️ **Illustrative self-study guidance — not an official university exam
> regulation or published paper.** Timings and pass marks are suggestions;
> instructors must map them to their own assessment regulations.

---

## 1. What "ready" looks like

You are ready when you can, without notes:

1. **Explain** every term in the [glossary](../glossary/index.md) in one
   sentence, and every stage of the lifecycle with its artefacts.
2. **Execute** the tool workflows: environment setup, data validation,
   tracked experiment, gate refusal, serving, container, CI, monitoring,
   rollback — each from memory, with the expected output.
3. **Judge**: given a scenario (drift, red CI, bad release, suspicious
   numbers), name the evidence you would collect and the decision you would
   make — with flip-conditions.
4. **Defend**: answer "why this way and not that" for your own capstone
   choices.

---

## 2. The revision map

| If you are weak on… | Re-read (in this order) | Then practise |
|---|---|---|
| Vocabulary, lifecycle, roles | [01](../modules/01-introduction-mlops-lifecycle/index.md), [03](../modules/03-ml-project-technical-debt/index.md) | [Bank 01](question-banks/q01-fundamentals.md), LAB-01/02 |
| Environments, seeds, data | [02](../modules/02-python-git-cli-environments/index.md), [04](../modules/04-data-quality-validation-versioning/index.md), [05](../modules/05-reproducible-training-pipelines/index.md) | [Bank 02](question-banks/q02-reproducibility-data-versioning.md), LAB-03/04/05 |
| Metrics, baselines, tracking, registries | [06](../modules/06-experiment-tracking-mlflow/index.md), [09](../modules/09-model-artifacts-registry/index.md) | [Bank 03](question-banks/q03-experiment-tracking-evaluation.md), LAB-06/09 |
| Tests, leakage, gates, pipelines | [07](../modules/07-testing-for-ml/index.md), [08](../modules/08-pipeline-automation/index.md) | [Bank 04](question-banks/q04-testing-automation.md), LAB-07/08 |
| APIs, Docker | [10](../modules/10-model-serving-fastapi/index.md), [11](../modules/11-docker-containers/index.md) | [Bank 05](question-banks/q05-apis-containers.md), LAB-10/11/12 |
| CI, orchestration | [12](../modules/12-cicd-github-actions/index.md), [13](../modules/13-orchestration-scheduled-pipelines/index.md) | [Bank 06](question-banks/q06-cicd-orchestration.md), LAB-14/16 |
| Monitoring, drift, decisions | [14](../modules/14-monitoring-drift-retraining/index.md) | [Bank 07](question-banks/q07-monitoring-drift.md), LAB-17/18 |
| Security, privacy, fairness | [15](../modules/15-security-privacy-governance/index.md) | [Bank 08](question-banks/q08-security-governance.md), LAB-19 |
| Cloud, Kubernetes, scaling | [16](../modules/16-cloud-kubernetes-scaling/index.md) | [Bank 09](question-banks/q09-cloud-advanced-operations.md) |
| Pull it all together | [17](../modules/17-capstone/index.md) | [Capstone assessment](capstone-assessment.md), LAB-20 |

---

## 3. A 14-day revision plan (suggested, adjustable)

| Days | Focus | Daily session (~60–90 min) |
|---|---|---|
| 1–2 | Foundations | re-read modules 01–03 → bank 01 closed book → mark → fix misses |
| 3–4 | Data & reproducibility | modules 02/04/05 → bank 02 → re-run LAB-03 or LAB-05 cold |
| 5–6 | Tracking & evaluation | modules 06/09 → bank 03 → redo MP2 selection memo from memory |
| 7 | Testing & automation | modules 07/08 → bank 04 → re-derive the leakage test |
| 8 | Serving & containers | modules 10/11 → bank 05 → rebuild lab-10 service from scratch |
| 9 | CI & orchestration | modules 12/13 → bank 06 → rewrite your workflow YAML cold |
| 10 | Monitoring | module 14 → bank 07 → fill the 2×2 for LAB-18's numbers |
| 11 | Security & cloud | modules 15/16 → banks 08–09 → verdict paragraph, timed |
| 12 | **Mock exam** (see §4) | 2 hours, closed book, all nine banks' Part E + one debug |
| 13 | Weak-spot repair | only the questions you missed, with written reasons |
| 14 | Defence rehearsal | full walkthrough + [LAB-20](../labs/lab-20-incident-day.md) fault injection, timed |

**Method notes (evidence-based, not motivational):** active recall (answer
before looking) beats re-reading; spacing beats cramming; interleaving
question types beats blocking by topic; and every session should end with one
*executed* command — this course is graded on evidence, not recognition.

---

## 4. Build your own mock exam (2 hours)

Draw from the [question banks](question-banks/index.md) — 90 questions exist;
a mock is a sample, not the pool:

| Section | Source | Time | Marks (illustrative) |
|---|---|---|---|
| A — 15 multiple choice, mixed banks | Part A of any banks | 25 min | 15 |
| B — 4 short answers | Part B | 30 min | 12 |
| C — 1 debugging, unseen (re-type one of the snippets into your editor and fix it for real) | Part C | 20 min | 8 |
| D — 1 architecture diagram, described in prose if not drawn | Part D | 15 min | 5 |
| E — 2 scenarios, **timed**, with flip-conditions required | Part E | 30 min | 10 |

Suggested pass: **≥ 70%** *and* both scenario answers containing an explicit
decision + evidence + flip-condition. Grade with the
[rubric bands](rubrics-checklists.md); mark every question you guessed.

---

## 5. Practical performance check (do, don't recite)

Timed, cold, no notes — these are the "lab practicals" of a self-study exam:

- [ ] From an empty folder: environment → pinned install → train → metrics
      (20 min, [beginner starter](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/starter-projects/beginner)
      level).
- [ ] Break a dataset so validation refuses it, name every violation (10 min).
- [ ] Serve a model with three endpoints and fail five malformed requests
      correctly (25 min).
- [ ] Stage → promote → verify → roll back a model, explain each output
      (10 min).
- [ ] Read a drift report and write the 2×2 decision with flip-conditions
      (10 min).
- [ ] Inject a fault, detect it with your own tooling, restore, prove
      recovery ([LAB-20](../labs/lab-20-incident-day.md)) (30 min).

---

## 6. Day-before and day-of checklists

**Day before**
- [ ] Stop adding content; review evidence paths only.
- [ ] Confirm every claim in your report has a transcript behind it.
- [ ] Re-run the full suite once; note the count (`pytest -q`).
- [ ] Prepare the one-page summary: architecture, thresholds, three biggest
      risks.
- [ ] Sleep — recall is a physiological feature.

**Day of**
- [ ] Read each question fully; note the *actual* verb (explain vs decide vs
      execute).
- [ ] Answer the secure marks first; budget time for scenarios last.
- [ ] For any "what would you do" question: evidence → decision →
      flip-conditions, in that order.
- [ ] Never leave a claimed-but-unrun experiment implied — label `NOT RUN`.

**After**
- [ ] Add the misses and their reasons to your reflection; update the
      [progress checklist](../start-here/progress-checklist.md).

---

**Related:** [question banks](question-banks/index.md) ·
[module practice](module-practice.md) · [mini-projects](mini-projects.md) ·
[rubrics](rubrics-checklists.md) · [capstone assessment](capstone-assessment.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*