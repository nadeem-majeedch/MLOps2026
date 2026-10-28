# Knowledge check — Module 03

Attempt every question first. **10 questions · ~30 minutes · open book.**
Suggested pass mark **7/10**, with no question about notebook hygiene wrong.

---

## Part A — Recall

**Q1.** List the four contract questions a README must answer.

**Q2.** Define: *technical debt*, *entanglement*, *configuration debt*,
*undeclared consumer*.

**Q3.** Name the four notebook failure modes, and one fix for each.

**Q4.** What are the five rules that make the course project layout work
(concepts §1)?

## Part B — Comprehension

**Q5.** The legacy notebook computes the churn rate twice, two different ways.
Both print `0.091`. Why is this still a defect?

**Q6.** Why must importing a `src/` module have no side effects? Describe what
would break if `features.py` trained a model on import.

**Q7.** A refactor changes folder names but produces different accuracy. Under
the lab's rules, is that a successful refactor? Explain what you would do next.

**Q8.** Why is ML technical debt said to accrue faster than ordinary software
debt, even when nobody touches the code?

## Part C — Application

**Q9.** Your teammate's notebook has these cells, in order: (1) load CSV,
(2) train model, (3) define a helper function, (4) evaluate using the helper,
(5) print results. Cell 4 fails with `NameError` when run alone. Explain why,
name the failure mode, and describe the minimal reorganisation that removes it.

**Q10.** You have five minutes to justify structure to a manager who wants
features. Write the three-sentence argument, using a cost, not a principle.

---

# Answers and reasoning

**Q1 — 1 point.**
What it does; what must be installed; how to run it; what output to expect.
*Reasoning:* these are the four things a stranger needs to go from clone to
result without asking you — which is the definition of reproducible handover.

**Q2 — 1 point (0.25 each).**
*Technical debt* = the future cost of a shortcut taken today. *Entanglement* =
components so interdependent that changing one risks breaking others.
*Configuration debt* = behaviour-affecting values buried in code with no recorded
reason. *Undeclared consumer* = someone or something depending on your output
without having told you.
*Reasoning:* each type implies a different fix — that is why classification, not
vague "messiness", is the skill.

**Q3 — 1 point (0.25 each).**
Hidden state → restart-and-run-all discipline; extract logic to functions.
Logic trapped in cells → move to importable modules. Unreviewable diffs → strip
outputs / pair with jupytext. No entry point → one documented `run.py`.
*Reasoning:* each has a concrete mechanism — noticing without a fix is trivia.

**Q4 — 1 point (0.2 each, capped at 1).**
`src/` importable and side-effect free; one documented entry point; generated
artefacts excluded from version control; configuration outside code; `legacy/` is
reference only and never imported.
*Reasoning:* each rule prevents a specific failure mode you already met in
Modules 02–03.

**Q5 — 1 point.**
Two implementations of one fact can drift apart: the next person fixes one and
not the other, and a silent disagreement appears later. Two correct answers today
are two opportunities to be wrong tomorrow.
*Reasoning:* the defect is duplication of a *source of truth*, not the current
output.

**Q6 — 1 point.**
Imports are how tests, notebooks, and pipelines pull in your code; if importing
trains a model, then every test collection, every `import`, and every tool that
scans the module pays that cost — and results depend on *when* the import
happened. Minimal fix: training only runs from an explicit entry point.
*Reasoning:* this is the mechanism behind "pipelines that train three times per
run".

**Q7 — 1 point.**
No — the lab's acceptance criterion is reproducing `accuracy 0.8860`. A refactor
that changes results has changed behaviour, deliberately or not. Next: diff the
inputs (config, seed, split, features, row handling) against the original until
the number matches, or document the change as a decision with evidence.
*Reasoning:* separation of structure-change from behaviour-change is what makes
refactoring safe.

**Q8 — 1 point.**
Because the data underneath changes independently of the code: a new extract,
schema drift, or new categories degrades the system while every line of code
stays the same — so nobody sees the debt being incurred. Code debt needs a code
change; ML debt only needs time.
*Reasoning:* this is exactly why Module 04 (validation) and Module 14
(monitoring) exist.

**Q9 — 1 point.**
Cell 4 uses a helper defined in cell 3, so running it in isolation has no
definition — classic **hidden state**: meaning depends on execution order.
Minimal reorganisation: move the helper into a module (or cell 1, as a
definition cell), and organise the notebook as *definitions first, then
execution* — or, better, move the logic to `src/` and keep the notebook as a
thin driver.
*Reasoning:* hidden state is cured by making definitions precede use in
*structure*, not in memory.

**Q10 — 1 point.**
Any answer of this shape:
*"Right now, a new team member needs [me] a day to run this analysis. With one
command and a README, they run it in five minutes — and when the data changes,
the tests tell us instead of the client. The cost is about two hours now; the
cost of not doing it is every future handover, plus the last time we shipped a
number nobody could reproduce."*
*Reasoning:* cost + risk + reversibility beats principle in any conversation
about priorities.

---

## Marking and next steps

| Score | Action |
|---|---|
| **9–10** | Proceed to Module 04 |
| **7–8** | Re-read the missed sections, then continue |
| **5–6** | Complete the lab's steps 4–10, then re-take |
| **< 5** | Re-read concepts §1–§3 and re-run the worked example first |

File your score as `modules/03/knowledge-check.md` in your portfolio.

---

[← Module overview](index.md) · [Troubleshooting →](troubleshooting.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*