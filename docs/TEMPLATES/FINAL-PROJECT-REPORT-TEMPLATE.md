# Final Project Report Template

> **How to use this file:** copy it to `REPORT.md` — the last document you
> write, the first one anyone reads. It **summarises** evidence that already
> exists in `PROBLEM.md`, `EXPERIMENTS.md`, `EVIDENCE/`, `DEPLOYMENT.md` and
> `MONITORING.md`; do not invent numbers here that are not in those files.
> Pair with [self-assessment/reflection](../projects/capstone-self-assessment.md).
> Delete italic guidance lines.

---

```markdown
# Final project report — <system name>

**Author:** <name> · **Date:** <YYYY-MM-DD> · **Course:** MLOps self-study
**Repository:** <link> · **Demo:** <how to run it in one command>

## 1. Executive summary
*≤150 words: the problem, your solution, the headline metric vs baseline,
and the single biggest limitation. A reader who stops here should not be
misled by the rest.*

## 2. Problem & success criteria
*Condense PROBLEM.md §1, §4 — table of goal / metric / threshold / achieved.
Tick which criteria were met and which were not (yes, some may not be).*

## 3. System architecture
*Embed/link the diagram; three sentences on the most important design
decision and what it cost you (link architecture.md §5).*

## 4. Data
*Source + licence, version/hash, validation summary (pass/fail counts), and
the leakage trap you refused, if any. Link the datasets record.*

## 5. Experiments & model selection
*Link EXPERIMENTS.md; state the pre-declared rule and its mechanical
outcome; report test metrics ONCE with baseline comparison.*

## 6. Quality engineering
*Test count and what they cover; the gate that refuses (paste one refusal);
coverage number if claimed; CI summary including a red run if you produced
one. All numbers must trace to EVIDENCE/.*

## 7. Delivery
*API contract summary, container/Path-B status (honestly labelled), deploy
checklist verdict, and the rollback rehearsal output.*

## 8. Operations: monitoring & response
*Link MONITORING.md; report the 2×2 cell you last landed in and your
flip-conditions.*

## 9. Security, privacy & governance
*Secrets handling, data/PII posture, fairness measurement if applicable,
model card/intended use, and your dated deployment verdict.*

## 10. Results against success criteria
| criterion | threshold | achieved | met? | evidence path |
|---|---|---|---|---|
| … | … | … | ✅ / ⚠️ / ❌ | `EVIDENCE/…` |

## 11. What I would do differently
*≥3 items, each with the specific thing you would change and why — not
"test more".*

## 12. Reproduction
*Exact commands, fresh clone to full result, with expected outputs — the
hard condition lives or dies here.*

## 13. Declaration
*I ran every command whose output appears in this report. Anything not run
is labelled NOT RUN. No real personal data appears anywhere in this project.*
**Signed:** <name, date>

## 14. References
*Modules, labs, tool documentation (with URLs) — distinguishing tool
behaviour from general principles where relevant.*
```

**Self-check:** read §1 and §10 only. Are they honest, complete, and
traceable? Assessors and future-you will read exactly those two sections
first — and then spot-check one evidence path at random.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*