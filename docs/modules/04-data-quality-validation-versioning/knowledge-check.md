# Knowledge check — Module 04

Attempt every question first. **10 questions · ~30 minutes · open book.**
Suggested pass mark **7/10**, with no question about versioning wrong.

---

## Part A — Recall

**Q1.** Name the six *structural* check families from concepts §2 and give one
example of each.

**Q2.** Define: *data contract*, *dataset card*, *data lineage*, *content hash*.

**Q3.** Why does Git handle code well but data badly? Give two reasons.

**Q4.** Map these Git commands to their DVC equivalents: `git init`,
`git add`, `git status`, `git checkout`.

## Part B — Comprehension

**Q5.** In the lab, `column_types` **passed** on the file with damaged
`monthly_charges`, yet the file was clearly broken. Explain why the check passed
and what this teaches about writing validation.

**Q6.** A validation failure prints `[FAIL] range` with no counts. Why is that a
defect in the validator rather than a minor annoyance?

**Q7.** `dvc checkout` refused to restore a modified file without `--force`.
Under what condition is `--force` safe, and under what condition is it reckless?

**Q8.** Your dataset legitimately changes every day. How can experiments remain
reproducible? Describe the mechanism, not the tool.

## Part C — Application

**Q9.** A CSV arrives with correct columns, no nulls, unique keys — but the
`churn` column now contains values `0`, `1`, and `2`. Which checks catch this?
Which currently would not, and what would you add?

**Q10.** Walk through the evidence chain you could present, six months from now,
to answer: *"Which data produced this model?"* Name every artefact involved.

---

# Answers and reasoning

**Q1 — 1 point (0.15 per family, capped at 1).**
Schema (required columns present), completeness (null counts), uniqueness
(`customer_id` duplicates), range (`tenure_months >= 0`), domain
(`contract_type ∈ {monthly, one_year, two_year}`), target sanity (binary target,
positive rate 0.02–0.50).
*Reasoning:* these are cheap and deterministic — the checks that belong in every
run; distribution checks need a baseline and belong to Module 14.

**Q2 — 1 point (0.25 each).**
*Data contract* = agreed, pre-hoc specification of schema, quality, owner, and
cadence. *Dataset card* = documentation of origin, licence, limitations, and
intended use. *Data lineage* = the recorded path data took from source to use.
*Content hash* = a short fingerprint of exact bytes, equal only for identical files.
*Reasoning:* contract = promise before; card = description always; lineage =
trace afterwards; hash = the mechanism that makes the other three checkable.

**Q3 — 1 point (0.5 per reason).**
Size (every clone carries every historical version) and change semantics (data
changes without code changes; you want snapshots by date, not diffs of
gigabytes). Also: data often shouldn't be public in a repo's history.
*Reasoning:* these are exactly the gaps DVC's pointer-plus-cache design fills.

**Q4 — 1 point (0.25 each).**
`dvc init` · `dvc add <file>` · `dvc status` · `dvc checkout`.
*Reasoning:* DVC's value is that the mental model transfers; if you know Git,
you are 80% productive on day one.

**Q5 — 1 point.**
pandas *infers* dtypes when reading CSV: numeric-looking text was parsed as
numbers, and `"n/a"` became `NaN` — so the dtype was legitimately numeric while
the *content* was damaged. Lesson: check meaning (completeness, ranges, domains),
and if you need a guarantee, read with an explicit `dtype=` — never assume a
parser's convenience is a validation strategy.
*Reasoning:* this is why multiple independent check families exist.

**Q6 — 1 point.**
Because the message must say *what* failed, *where*, and *how many* — the reader
(potentially you, at 3 a.m.) needs enough information to act without re-running
analysis. A bare `[FAIL]` converts a 30-second fix into an investigation.
*Reasoning:* error messages are part of the validator's interface, not an
afterthought.

**Q7 — 1 point (0.5 each).**
Safe when the local modification is disposable and regenerable — you know the
pointer represents what you want, and the edit adds no value (e.g. injected test
junk). Reckless when the local file contains work not recorded anywhere — the
refusal exists precisely because DVC cannot know which case you are in.
*Reasoning:* the tool delegates the judgement to you; that is what `--force`
means.

**Q8 — 1 point.**
Immutability + addressing: each day's extract is written as a *new* version and
never edited in place; experiments reference a specific version by hash; the
pointer is committed alongside the code, so re-running with the same pointers
restores the same bytes. Daily data changes do not disturb yesterday's version
because nothing overwrites it.
*Reasoning:* versioning is about *identity*, not about whether data changes.

**Q9 — 1 point.**
`target_sane` catches it: `set(df["churn"].unique()) <= {0, 1}` fails when `2`
appears. None of the structural checks for columns/nulls/uniqueness would notice.
What is missing is an explicit domain check per column (the same family applied
to the target) and, ideally, a documented target definition in the contract.
*Reasoning:* every column's domain should be declared — targets are columns too.

**Q10 — 1 point.**
The chain: (1) model artefact → (2) the run that produced it (config, metrics,
run id — Module 06) → (3) the code commit (Git) → (4) the `.dvc` pointer file
committed with it → (5) the hash → (6) the restored bytes (or the DVC cache /
remote). Each link is an artefact you already produce in this course; the
registry (Module 09) simply stores the chain next to the model.
*Reasoning:* being able to enumerate the chain is the point of doing steps in
order — a missing link is visible immediately.

---

## Marking and next steps

| Score | Action |
|---|---|
| **9–10** | Proceed to Module 05 |
| **7–8** | Re-read the missed sections, then continue |
| **5–6** | Redo lab Part B (steps 5–9), then re-take |
| **< 5** | Re-read concepts §1–§4 and re-run the worked example first |

File your score as `modules/04/knowledge-check.md`.

---

[← Module overview](index.md) · [Troubleshooting →](troubleshooting.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*