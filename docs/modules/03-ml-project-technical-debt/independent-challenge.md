# Independent challenge — Module 03

No step-by-step help. The lab gave you one notebook to rescue; this task asks you
to judge structure in code you did not write.

## The task

Write a **one-page technical-debt audit** of a real codebase — yours, or a small
public ML repository you respect.

### Step 1 — Choose and read

Pick a codebase of roughly 200–2,000 lines. (Your Module 02 project is a fine
choice; a public repository with notebooks is better.) Read it for 30 minutes
without changing anything.

### Step 2 — Classify at least five debt items

| # | What you found (quote or file:line) | Debt type (concepts §2) | Cost: what will it take to change later? |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |

Allowed types: data-dependency, entanglement, hidden feedback loop, undeclared
consumer, configuration, glue code, pipeline sprawl — plus "not debt" if you
decide an apparent shortcut is actually fine (justify it).

### Step 3 — Stage the fixes

Order the five items into three waves:

1. **Fix now** (cheap and prevents silent failures),
2. **Fix this month** (costly if deferred),
3. **Accept deliberately** (write the reason debt is being kept).

### Step 4 — Defend one hard call

Pick the item you were tempted to "fix now" but rejected, or vice versa, and
argue it in ≤6 lines.

## Acceptance criteria

- [ ] ≥5 items, each with a **quoted location** (file and line, or cell number) —
      no abstract claims like "the code is messy".
- [ ] Every item has a **type** from the taxonomy and a **cost**, not a moral judgement.
- [ ] At least one item is ML-specific (data dependency, feedback loop, or
      undeclared consumer) — not just generic code smell.
- [ ] Three fix waves exist and the "accept" wave contains a written justification.
- [ ] The hard-call defence names the trade-off, not just the preference.
- [ ] Filed in your portfolio as `modules/03/debt-audit.md`.

## How to self-mark

| Level | Signal |
|---|---|
| **Meets** | An engineer could act on your waves tomorrow; costs are specific ("changing X touches N files and risks Y") |
| **Developing** | Items are real but typed loosely, or costs are vague ("hard to maintain") |
| **Not yet** | Items are opinions without locations, or no ML-specific debt found |

## If you get stuck

1. Grep for numbers in code: `grep -rn "[0-9]\+\.[0-9]" src/` — configuration
   debt is always hiding in literals.
2. Grep for file paths and column names — data-dependency debt lives in strings.
3. Ask of each notebook: *what would break if I ran the cells out of order?*
4. Ask of each script: *what has to happen manually before this runs?* — every
   answer is glue code.

---

**Next:** [knowledge-check.md](knowledge-check.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*