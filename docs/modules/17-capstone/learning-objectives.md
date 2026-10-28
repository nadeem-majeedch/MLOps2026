# Learning objectives — Module 17

Maps to syllabus outcomes
[LO 17.1–17.4](../../syllabus/detailed-syllabus.md#module-17-advanced-mlops-capstone-integrating-the-entire-lifecycle).

| # | You can… | You prove it by… |
|---|---|---|
| **17.1** | Take an idea to a deployed, monitored ML system: data → validation → versioning → training → tracking → tests → registry → API → container → CI → scheduling → monitoring → governance | A working repository where **every one of the 14 links** exists and is exercised — mapped in your design doc, with the module each link came from |
| **17.2** | Make and defend end-to-end design decisions, including at least two explicitly rejected alternatives | A design document containing ≥2 alternatives you *rejected*, each with the trade-off that decided it (not strawmen) |
| **17.3** | Demonstrate reproducibility to a third party using only the repository | Your **clean-clone run**: documented commands executed by someone/something other than you, metrics within your declared tolerance, hashes recorded |
| **17.4** | Operate the system under a fault-injection exercise and recover with a documented rollback | A fault-injection transcript: what you broke, how it was detected, the rollback/recovery command, the recovered state — plus the post-incident note |

## Supporting skills

- Scope an **MVP** against **production-grade extensions** honestly — the
  rubric grades the former; the latter is where learning goes deeper, not
  where points are won.
- Run a **production readiness review**: a checklist pass that *files
  issues* rather than a demo that hopes.
- Write **SLO**s a toy system can actually measure (e.g. "95% of `/health`
  checks succeed over 24 h of scheduled runs") and a **runbook** someone
  else can execute.
- Assemble an **evidence bundle** where every claim links to a log,
  report, or artifact — no claim survives unsupported.
- Explain **end-to-end lineage**: which data → which run → which release
  → which container, answerable from the repository alone.

## Self-check questions

1. Name the 14-link chain from memory, then check yourself against
   [concepts.md §1](concepts.md#1-the-chain-the-capstone-integrates).
2. Your system works on your laptop. Name two things that *must* still be
   demonstrated before "reproducible" is a fair word.
3. What single pair of rubric criteria can cap your capstone at
   "Developing" no matter how high everything else scores?

*(Answers in [knowledge-check.md](knowledge-check.md) — attempt first.)*

---

[← Module 17 index](index.md) · [Next: concepts →](concepts.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*