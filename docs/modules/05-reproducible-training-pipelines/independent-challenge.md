# Independent challenge — Module 05

No step-by-step help. You have run a pipeline someone else wrote; now extend one
and prove the extension behaves.

## The task

Add **one new feature** to the training pipeline, behind a configuration flag,
and demonstrate that the flag — not the code — governs its effect.

### Requirements

1. **The feature is yours to choose.** Sensible candidates on this dataset:
   `charges_per_month = monthly_charges / max(tenure_months, 1)`,
   `tickets_per_month = support_tickets / max(tenure_months, 1)`, or a banded
   `tenure_group`. It must be computed in `src/`, from existing columns only.
2. **It is governed by config:**
   ```yaml
   features:
     engineered: [charges_per_month]   # empty list = off
   ```
3. **Three runs, recorded:**

   | Run | Config | Predicted | Actual metrics |
   |---|---|---|---|
   | A | feature off | | |
   | B | feature on | | |
   | C | feature on, re-run | | |

4. **Reproducibility still holds:** run B twice and show identical hashes.
5. **A two-paragraph justification:** what the feature *means* for the business
   question, and what would falsify it (a concrete check you could run).

### Stretch (optional)

- Show the feature failing validation if `tenure_months` were 0 — where does
  your guard live, and why there?
- Prove the feature does not leak: confirm it uses only fields available at
  scoring time.

## Acceptance criteria

- [ ] Feature implemented in `src/`, not in a notebook or the entry point.
- [ ] Off-by-default: with `engineered: []`, output is **bit-identical** to the
      pre-challenge pipeline (hash comparison).
- [ ] On: metrics recorded, and run B repeated with an identical hash.
- [ ] Prediction column present in your table *before* results.
- [ ] Justification names a falsification test, not just a benefit.
- [ ] Filed as `modules/05/challenge-feature.md` with the config diff attached.

## How to self-mark

| Level | Signal |
|---|---|
| **Meets** | The flag fully governs the behaviour; off-state is provably unchanged; reasoning is testable |
| **Developing** | Works, but the off-state differs slightly (leakage into the pipeline?) or the justification is only optimistic |
| **Not yet** | Feature hardcoded, or reproducibility not re-proven after the change |

## If you get stuck

1. If "off" and "before" hashes differ, your feature runs even when disabled —
   check for unconditional code outside the config branch.
2. If B's two runs differ, the feature introduced randomness (sorting, set
   iteration) — find it the way the lab's Step 5 did.
3. If nothing changes with the flag on, the feature may be constant, or excluded
   from the ColumnTransformer's column list — print the feature matrix shape at
   each stage.

---

**Next:** [knowledge-check.md](knowledge-check.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*