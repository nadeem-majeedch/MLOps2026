# Knowledge check — Module 12

## How to use this

1. Answer in writing, closed book on the second pass.
2. Mark with the [answers](#answers) only after committing.
3. Target **80% with justified reasoning**; below that re-read
   [concepts.md](concepts.md) §§1–§6.
4. Suggested self-study framework, not an official exam:
   [assessment framework](../../syllabus/assessment-framework.md).

---

## Questions

**Q1.** In one line each: CI, continuous delivery, continuous deployment.
Which one does `ci.yml` implement?

**Q2.** List the three jobs and say what *layer of failure* each one names.

**Q3.** *(True/False + why)* "Jobs run one after another because YAML lists
them in order."

**Q4.** What do `permissions: contents: read` and `concurrency/cancel-in-progress`
each buy you? One security answer, one cost/time answer.

**Q5.** `ml_check.py` validates instead of retraining. Give two reasons this
is the right shape for CI (concepts §3), and one thing it *cannot* catch that
another process must.

**Q6.** State the three-place rule for secrets and point to the line in
`ci.yml` that proves none is needed here.

**Q7.** A run fails in `test` at step "Run the test suite". Describe your
first three moves, and explain why "run the exact command locally" is step one.

**Q8.** The cache is keyed on `requirements-docker.txt`. When does it hit,
when does it miss, and why is a miss never a *correctness* problem?

**Q9.** Why does the workflow generate data with `python generate_data.py`
inside CI rather than committing the CSV?

**Q10.** Name one thing this workflow deliberately does NOT do, and name the
module(s) that will.

---

## Answers

**Q1.** *CI*: build + check every change automatically before merge.
*Continuous delivery*: every passing change is packaged and ready to ship, with
a human pressing the button. *Continuous deployment*: shipping is also
automatic. `ci.yml` implements **CI** — it stops at validation (concepts §1,
§8). *(5/5)*

**Q2.** `lint` → code hygiene (style, unused imports); `test` → logic defects
(34 tests across all layers); `ml-validate` → **data/model** defects (contract
violations, quality below floor). The mapping is the module's core message:
three different failure classes, three different red names. *(5/5)*

**Q3. False.** Jobs are independent VMs and start **in parallel**; YAML order
is presentation. Serialisation only happens through an explicit `needs:`
dependency (which we deliberately do not add — parallel is faster, and failure
still names the layer). *(5/5)*

**Q4.** `contents: read` = the run token can fetch the code and nothing else —
a compromised or buggy workflow cannot push/rewrite your repo (security).
`cancel-in-progress` = a newer push cancels the obsolete older run, saving
runner minutes and your attention (cost/time). *(5/5)*

**Q5.** (1) Speed: CI must stay in seconds–low minutes or people ignore it;
(2) determinism: repeated training would produce noisy/flaky gates.
**Cannot catch:** a model that trained *fine* on today's data but is weak —
because validation checks recorded metrics/contract, not fresh experiments;
that belongs to scheduled evaluation (Module 13) and live monitoring
(Module 14). *(5/5)*

**Q6.** Never in **source** (YAML/code/Dockerfile), never in **logs**
(echoing/globally-visible output), never on **runner disk as a file**. Evidence
none is needed: `permissions: contents: read` and zero `${{ secrets.* }}`
references — the workflow only reads the checkout and runs local commands. *(5/5)*

**Q7.** (1) Identify job+step+first error line from the log; (2) run that exact
command locally in the same working directory — it reproduces in seconds and
gives an interactive debugger if needed; (3) fix, re-run locally, then re-run
the workflow (or just push). Local reproduction is step one because CI is
*composed of local commands* — the platform adds scheduling, not new logic. *(5/5)*

**Q8.** Hit: the requirements file is unchanged, so pip downloads are reused.
Miss: any pin change (or a different key input) → full reinstall, slower run.
Never a correctness issue: the cache only affects *how* packages arrive, not
*which* versions — the pin file decides versions either way. *(5/5)*

**Q9.** Because committing 2,000 derived rows invites drift (edited data
without a code change), bloats the repo, and hides the generator as the source
of truth — while CI regenerating deterministically *proves* the seed-to-data
path still works (itself a regression test). Data versioning for real datasets
is Module 04's DVC territory. *(5/5)*

**Q10.** It does **not build/publish an image** (LO 12.3's sketch) and does
**not deploy** anything — deployment/targets/credentials belong to Modules
15–16, with the capstone integrating them. *(5/5)*

**Scoring:** /50 → ×2 = %. **80+ ready.** 60–79: redo lab Steps 5–9.
Below 60: re-read concepts §2–§5 and re-read `ci.yml` alongside it.

---

**Next:** [troubleshooting.md](troubleshooting.md) ·
[Module 13 →](../13-orchestration-scheduled-pipelines/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*