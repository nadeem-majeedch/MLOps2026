# Independent challenge — Module 04

No step-by-step instructions. You have validated a dataset someone handed you;
now design the guarantee *before* it exists.

## The task

Define a **data contract** for a dataset you choose — a public CSV, a database
table you can export, or a file a friend produces — and implement it.

### What to produce

1. **The contract** (Markdown, ~1 page):
   - Owner and update cadence (who produces it, how often)
   - Schema: columns, types, allowed/null policy
   - Quality thresholds: uniqueness, ranges, row-count bounds, target balance if labelled
   - Licence and permitted uses
   - What happens on violation (who is notified, what stops)

2. **The implementation**: executable checks that encode the contract — plain
   pandas is fine; pandera if you prefer. It must exit non-zero on violation.

3. **Three negative tests**: prove your checker *fails* by violating your own
   contract on purpose (missing column, duplicate key, out-of-range value) —
   show each output.

4. **A dataset card** for the same dataset (source, licence, size, limitations,
   intended use, sensitive content: yes/no).

## Acceptance criteria

- [ ] Every schema field in the contract has a corresponding executable check —
      the two documents cannot disagree.
- [ ] Thresholds are **numbers with reasons** ("row count within ±10% of the
      trailing 7-day mean", not "roughly similar").
- [ ] Three negative tests demonstrated with actual failing output.
- [ ] Violation handling is specified (who/what stops), not "we would notice".
- [ ] Licence is verified, not assumed — cite where you read it.
- [ ] Filed as `modules/04/data-contract.md` + the check script + outputs.

## How to self-mark

| Level | Signal |
|---|---|
| **Meets** | A producer could implement against your contract without asking you a single question |
| **Developing** | Checks exist but thresholds are arbitrary, or the contract and code disagree somewhere |
| **Not yet** | Only "columns exist" checks, or no negative tests |

## If you get stuck

1. Start from your own lab's seven checks — then delete any that do not apply
   and add what your dataset actually threatens.
2. If you cannot decide a threshold, ask what the *consumer* of this data does
   with the column: thresholds come from consequences, not from aesthetics.
3. Remember the boundary: a contract governs structure and quality; a dataset
   card documents origin and fitness. Both, or neither.

---

**Next:** [knowledge-check.md](knowledge-check.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*