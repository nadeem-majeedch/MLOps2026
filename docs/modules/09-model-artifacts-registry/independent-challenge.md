# Independent challenge — Module 09

> Do this **without** step-by-step help. Target **75 minutes**.

---

## 1. The scenario

You are the reviewer, not the author. A colleague registered three versions and
promoted `v002` to production. Your job: audit the registry and write the
model card for what is actually serving.

## 2. Tasks

1. **Audit the trail.** From `index.json` and `history` alone (do not trust
   `list`), answer in writing:
   - What is in production now, and what was production immediately before it?
   - Which version was registered without a passing gate, and is it currently
     reachable from production? Why or why not?
   - Was any promotion rule violated? Quote the evidence line.
2. **Reproduce the state.** Delete `registry_store/` and rebuild the exact same
   three-version history yourself (register → promote → promote → register
   ungated), producing `history` output that matches the audit conclusions.
   Record any step where the system *refused* you.
3. **Break it honestly (one attempt).** Find any way to get an ungated version
   into production. If you cannot, write three sentences on why the design
   prevents it. If you can, you have found a real defect: write it up as an
   issue (symptom, reproduction, severity, proposed fix) and do **not** hide it.
4. **Model card under adversarial conditions.** Write the card for the current
   production version, but assume the reader is the legal/compliance reviewer:
   every metric needs its context (population, threshold, window), and
   §7 must name the exact rollback command with its observed output.
5. **One design argument.** 150 words: should `rollback` be limited to the
   *immediately* previous version (as now) or allowed to jump to any earlier
   version? Argue one side, acknowledging the strongest objection.

## 3. Deliverables

- `audit.md` (task 1, with quoted evidence lines)
- `history-rebuild.md` (task 2 transcript)
- `issue.md` **or** `why-it-is-safe.md` (task 3)
- `model-card.md` (task 4)
- `rollback-argument.md` (task 5)

## 4. Self-check (feedback criteria)

| Grade | Looks like |
|---|---|
| **Excellent (4)** | Audit cites exact history lines; rebuild matches; task 3 completed honestly either way; card meets lab §9 with contextualised metrics; argument names a real trade-off |
| **Proficient (3)** | Audit + rebuild correct; card complete; argument thin |
| **Developing (2)** | Answers read from `list` only, or rebuild diverges silently |
| **Not yet (1)** | Missing audit or card |

**The integrity rule applies:** if you could not reproduce it, you do not
understand it yet — say so in the write-up rather than smoothing it over.

---

**Next:** [knowledge-check.md](knowledge-check.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*