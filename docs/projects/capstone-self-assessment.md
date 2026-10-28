# Capstone self-assessment and reflection

**Deliverable 4 of the capstone set.** Copy these questions into your
portfolio's `REFLECTION.md` and answer them in writing *after* filling in
the [rubric worksheet](capstone-rubric.md). Grading criterion for this
document: **honesty**. A polished page that hides gaps scores worse than a
blunt one that names them.

---

## Part A — Numbers (from your worksheet)

1. Weighted total: ____ / 1.00 — and the two hard conditions: reproducibility
   ____ · quality gates ____ (both must be 1.00 or the cap applies).
2. Strongest criterion (score + evidence path) and *why* it is strong.
3. Weakest criterion (score + evidence path) and the one-hour fix you
   could do today.

## Part B — The system

4. Walk the 14-link chain of *your* system in eight sentences or fewer.
   Where did it nearly break?
5. Which link did you understand *least* when you started the capstone,
   and what made it click (or not)?
6. Reproducibility: describe your clean-clone run — who ran it, the
   declared tolerance, the actual result, and every manual step you had
   to add along the way.
7. Fault injection: what you broke, how your tooling caught it, the exact
   recovery commands, and what would catch it *earlier* next time.

## Part C — Decisions and alternatives

8. Your two **rejected** alternatives: for each — the option, the
   deciding trade-off, and the condition under which you'd revisit.
9. The decision you would change with hindsight, and the evidence that
   would have informed it.
10. Where did the course's "concept before tooling" rule save you time?
    Where did it slow you down?

## Part D — Governance and people

11. Fairness: your measured gap, its caveats, and how your system handles
    an over-target result (fix vs documented `--ack`) — and who owns it.
12. Privacy: the three fields you decided **not** to log, and why.
13. One risk in your risk register that remains open: its owner, its
    trigger, and your response plan.

## Part E — Process and portfolio

14. Hours per week and total; where you under/over-estimated (the
    estimates in each module were predictions — grade them).
15. The three most expensive mistakes you made and the checks you now run
    because of them.
16. What you would build next, using this system as a base — and which
    [extension](capstone-specification.md#4-minimum-viable-vs-production-grade-extensions)
    you would do first and why.
17. If a classmate asked you whether to take this course: your honest
    two paragraphs.

---

## Reflection quality bar

| Trait | Looks like |
|---|---|
| **Specific** | "the gate refused at 0.7163 < 0.99 during fault B" — not "testing helped" |
| **Numbers** | scores, gaps, hours, tolerances — with units |
| **Blunt** | gaps named without softening; failures kept, not edited out |
| **Forward-looking** | each gap paired with a next action or a deliberate decision not to act |

---

[Capstone specification](capstone-specification.md) ·
[Task checklist](capstone-checklist.md) ·
[Rubric worksheet](capstone-rubric.md) ·
[Projects overview](index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*