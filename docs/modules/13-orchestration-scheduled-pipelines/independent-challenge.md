# Independent challenge — Module 13

> Do this **without** step-by-step help. Target **75 minutes**.

---

## 1. The scenario

The team likes the runner but has three demands: the scheduler must catch up
after a laptop that was off, alerts must not repeat forever while a known issue
is being worked on, and a stakeholder wants retraining to start *when data
lands*, not on a clock.

## 2. Tasks

1. **Catch-up policy.** Implement `--catch-up` semantics: when the runner
   starts and finds ticks that were *missed* (compare last success time to
   now against the interval), it runs **one** consolidated tick and records it
   as `trigger: catch_up`. Write the policy in five lines: what counts as
   missed, why you run one tick instead of N, and what you refuse to catch up
   (failures older than what?).
2. **Alert suppression window.** Add `--silence 300`: after a failure, repeat
   failures within 300 s still update `runs.jsonl` but **do not rewrite the
   alert**, and a `silenced` marker records how many were folded in. Justify
   the design against alert fatigue (concepts §5) in three sentences.
3. **Event trigger.** Add `--watch`: poll the data hash every 5 s and fire a
   tick only when it changes, for 60 s (bounded — no infinite loop). Compare
   tick counts: `--every 5 --max-runs 12` vs `--watch` over the same minute,
   with data changed **once** midway. Paste both histories.
4. **Tool verdict with a real case.** Given: *"a hospital's nightly cohort
   extract, 12 dependent jobs, two teams, audit retention of 7 years"* — pick
   level 1/2/3 (concepts §1) and one named tool. Three arguments for your
   choice, **two for the strongest rejected option**, and one sentence on what
   your course runner could not legally/operationally do there.
5. **Failure-injection drill.** Make `train` fail *intermittently* (e.g. a
   deliberate locked-file simulation or a seeded random failure with
   `--retries`) so that retry actually earns its place: capture one run where
   attempt 2 succeeded, and one where all attempts failed. Both transcripts
   required — the second is what taught you the limits in concepts §3.

## 3. Deliverables

- Code diff for tasks 1–3, each with a written policy (task 1's five lines,
  task 2's three).
- Two history transcripts for task 3; two run transcripts for task 5.
- `tool-verdict.md` (task 4).
- Full `python -m pytest` output (nothing may break: 34+ still green).

## 4. Self-check (feedback criteria)

| Grade | Looks like |
|---|---|
| **Excellent (4)** | Catch-up policy bounded and justified; suppression updates history without spam; watch mode measured against interval with pasted evidence; tool verdict has 3-for and 2-against with named tool; both failure-injection transcripts present |
| **Proficient (3)** | Tasks 1–3 work with evidence; verdict present but thinner |
| **Developing (2)** | Only one mechanism implemented; no comparative measurement |
| **Not yet (1)** | Existing ticks/history broken, or claims without output |

**Constraint:** no new third-party dependencies for tasks 1–3 — this is
*design* practice inside the 200-line runner, not an installation exercise.

---

**Next:** [knowledge-check.md](knowledge-check.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*