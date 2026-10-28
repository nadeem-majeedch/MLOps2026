# Knowledge check — Module 08

## How to use this

1. Answer **in writing**, closed book on the second pass.
2. Mark yourself with the [answers](#answers) only after committing to yours.
3. Target **80% with justified reasoning**. Below that, re-read
   [concepts.md](concepts.md) §§1–5 first.
4. Self-assessment inside a suggested self-study framework — not an official
   university exam. See [assessment framework](../../syllabus/assessment-framework.md).

---

## Questions

**Q1.** Order these stages using only the dependency declarations:
`report, evaluate, train, features, validate, generate`.

**Q2.** *(True/False + why)* "A pipeline is just a shell script with better formatting."

**Q3.** The runner skips a stage when three signature parts match. Name them
and give one example change that invalidates each.

**Q4.** After a failed `evaluate`, the console printed `BLOCKED` for `report`
while the manifest still showed `report: success` from an earlier run. Explain
how both statements are true, and why the console output is the one to trust
at that moment.

**Q5.** Give the difference, with one example each:
(a) idempotent, (b) incremental, (c) deterministic.

**Q6.** A teammate claims: "my pipeline is reproducible because it skips
unchanged stages." Which word of that sentence is wrong, and what single
command demonstrates the real property?

**Q7.** Why does `generate` skip while `validate` re-runs after you edit
`config.yaml`? Answer in terms of declared inputs, not in terms of what the
code happens to do.

**Q8.** The tampered `features.csv` re-ran `features`, yet `train` still
skipped. Explain the reasoning chain that makes skipping correct there.

**Q9.** State one situation where *you should not* build a declared graph, and
say what to use instead.

**Q10.** Which two stages in this pipeline are quality gates, what does each
refuse, and where is each threshold configured?

---

## Answers

**Q1.** `generate → validate → features → train → evaluate → report` (the only
topological order for this linear chain). *(5/5)*

**Q2. False.** A script states *steps*; a pipeline states *facts about the
work* — inputs, outputs, dependencies — from which order, skipping, blocking
and reporting are derived. Editing a script means re-verifying ordering by
reading; editing a graph means the runner re-derives it. *(5/5)*

**Q3.** (1) **input file hashes** — edit `config.yaml`; (2) **the stage's own
source hash** — edit the function body; (3) **output file hashes** — hand-edit
or delete an output. Each change forces exactly that stage to re-run. *(5/5)*

**Q4.** `report: success` is a *historical* record from the previous run; the
runner never re-ran it this time, so the entry was not rewritten. The console's
`BLOCKED` describes *this* run: with `evaluate` failed, `report` must not run.
The runner prints BLOCKED precisely because manifests legitimately contain
older successes — trusting that stale entry would publish an outdated report. *(5/5)*

**Q5.** **Idempotent:** running twice ≡ running once (our stages overwrite
their own outputs). **Incremental:** skipped when nothing it depends on changed
(the SKIP lines). **Deterministic:** same inputs → identical output bytes
(the reason signature comparison is sound at all). *(5/5)*

**Q6.** *Reproducible* is the wrong word: skipping is an optimisation about
*change detection*, not proof you can rebuild from nothing. The demonstration
is `python -m pipe.run --clean` — delete every derived file and rebuild from
raw inputs, twice, with matching hashes. *(5/5)*

**Q7.** Because `config.yaml` is not a declared input of `generate` (its only
output is the raw CSV, and its input set is empty), while every later stage
lists `config.yaml` among its inputs. The runner reasons from declarations
only — if `generate` secretly read config, the declaration would be a lie and
incremental execution would be wrong. *(5/5)*

**Q8.** `features` re-ran because *its* output bytes changed. It is
deterministic, so it rewrote the same bytes as before → `train`'s stored input
hash still matches → `train` correctly skips. If `features` were nondeterministic
the regenerated file would differ, `train`'s signature would mismatch, and
`train` would re-run. Determinism is what makes "skip after a tamper" safe. *(5/5)*

**Q9.** Three stages in a script you run once by hand — use a plain script (or
`make`) until order/skipping/audit actually bite. (Alternative accepted: a
one-liner in a notebook.) The trigger points are concept §8. *(4/5 — judgement,
accept well-argued alternatives)*

**Q10.** `validate` refuses bad data (thresholds: Module 04's checks, run by
`run_checks`), and `evaluate` refuses weak models
(`quality.roc_auc_floor` in `config.yaml` — set to 0.70, demonstrated failing
at 0.99). *(5/5)*

**Scoring:** /50 → ×2 = %. **80+ ready to move on.** 60–79: redo lab Steps 3–6.
Below 60: re-read concepts §2–§4 and re-run `--list` while reading `run.py`.

---

**Next:** [troubleshooting.md](troubleshooting.md) ·
[Module 09 →](../09-model-artifacts-registry/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*