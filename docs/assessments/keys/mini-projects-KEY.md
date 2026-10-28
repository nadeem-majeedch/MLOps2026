# Reference-solution notes — mini-projects MP1–MP5

> 🔑 **REFERENCE SOLUTIONS (approach, not a script to paste).** Attempt the
> [specification](../mini-projects.md) first. These notes explain *how a
> strong submission thinks* and *why the design decisions matter* — the part
> a rubric actually rewards. Where your approach differs but the evidence
> chain holds, yours may be better: say so in your write-up.

---

## MP1 — Reproducible project skeleton

**Reference approach.** Start from the [beginner starter](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/starter-projects/beginner);
move files into the standard layout; make the entry point
`python run.py` do data → train → metrics; pin dependencies; write the README
last, by following your own instructions on a clean copy.

**Decisions worth reasoning about**
- *Why one command, not three?* Because three commands is three places to
  forget a step; the single entry point is the executable form of your
  documentation.
- *Why prove a second run matches?* Determinism is the foundation every later
  claim rests on (MP2's comparison is meaningless without it). Show a hash,
  not "it looked the same".
- *Why is reaching outside the repo a graded failure?* An out-of-repo import
  is the exact defect that makes "works on my machine" true forever.

**Common weak spots:** README describes folders that don't exist; metrics
provenance missing (no seed/date recorded); tests exist but never run in the
documented command.

---

## MP2 — Tracked, justified model

**Reference approach.** Generate a versioned dataset with a hash; write the
selection rule *first* (e.g. "highest ROC-AUC among runs with recall ≥ 0.40,
tie-break by lower latency"); run 10+ hyperparameter/feature variants; pick by
the rule; evaluate the winner once on the held-out test set; write the memo.

**Decisions worth reasoning about**
- *Why pre-declare the rule?* Ten runs is ten chances to cherry-pick. The
  rule converts selection from taste into procedure — and it is the single
  most common difference between a defensible and an indefensible MP2.
- *Why only the winner sees the test set?* Every additional look at the test
  set optimises against it; a memo that reports test metrics for all ten runs
  has quietly turned test into validation.
- *Why record the dataset hash with the run?* A tracked number without its
  data identity cannot be reproduced or defended later.

**Common weak spots:** accuracy on an imbalanced target as the headline;
"10 runs" that vary nothing; no baseline row in the comparison table.

---

## MP3 — Tested pipeline with a registered model

**Reference approach.** Lift the intermediate starter's stage structure; add
a gate module that reads criteria from a config file and evaluates *every*
key (threshold keys → inequalities with direction, `*_required` keys →
equality); tests for each criterion violated in isolation; registry with
sha256 recorded at stage time and re-verified at load/promotion.

**Decisions worth reasoning about**
- *Why config-driven checks instead of hand-coded ifs?* A criterion that
  exists only in code drifts from the criteria file; a criterion that exists
  only in the file and is never compared is exactly the Lab 15 bug — the
  fail-closed exit `2` is what stops that class of error from being silent.
- *Why ≥80% coverage on pipeline code specifically?* Whole-repo coverage is
  gamed by test files themselves; pipeline code is where silent data damage
  happens.
- *Why rehearse rollback during MP3, not later?* A registry you have never
  rolled back is an untested claim — the capstone's hard condition depends on
  it.

**Common weak spots:** gate refuses but names only the first violation;
coverage number includes tests; registry entry without provenance (no run id
or data hash).

---

## MP4 — Automated delivery

**Reference approach.** FastAPI contract exactly as Lab 10 specifies (Pydantic
bounds, `min_length=1`, 422 handler that names fields); model loaded once at
import; Dockerfile with deps before code, `HOST=0.0.0.0`, exec-form CMD,
healthcheck; CI with three jobs, pinned action tags, `contents: read`, and
reports uploaded `if: always()`.

**Decisions worth reasoning about**
- *Why test through `TestClient`, not a running server?* It exercises the
  real ASGI app deterministically in CI, where no port is guaranteed.
- *Why is the red-run demonstration graded?* Anyone can show green; showing
  that the pipeline **fails when it should** is the only proof the gate has
  teeth.
- *Why `if: always()` on artefact upload?* The evidence you need most is the
  evidence produced by the run that failed.
- *Path B honesty:* an unrun build claimed as run is a integrity failure of
  the whole submission — a labelled NOT RUN costs a little; a fabricated log
  costs everything.

**Common weak spots:** 422 without field names; secrets referenced from YAML
instead of platform settings; container works only because the model was
bind-mounted from the host.

---

## MP5 — Monitored system

**Reference approach.** Schedule the tick runner, capture the JSONL rows you
didn't trigger, then unschedule; record a reference window with dates; log
predictions; produce a drift report for in-distribution traffic (stable) and a
shifted window (strong); write the 2×2 memo with decision + flip-conditions.

**Decisions worth reasoning about**
- *Why both windows?* Stable-on-normal proves the monitor isn't simply
  noisy; strong-on-shifted proves it isn't simply broken. One without the
  other demonstrates nothing.
- *Why dates on the reference window?* Without them you cannot distinguish
  seasonality from drift — the most common false alarm in real monitoring.
- *Why flip-conditions in the memo?* A decision without the numbers that
  would reverse it is an opinion. The rubric looks for exactly that sentence.
- *Why must the schedule be removed?* An orphaned cron job is an unattended
  mutation of someone's machine — cleanup is part of doing the work.

**Common weak spots:** "drift detected → retrain scheduled" (the module's
cardinal sin); threshold values copied from a blog with no justification;
alert with no stated response.

---

**Self-assessment:** score each MP with the
[project rubric](../rubrics-checklists.md#project-rubric), record the band per
criterion, and keep the failed first attempt alongside the improved one —
progress is itself evidence. Then work the
[integrated capstone assessment](../capstone-assessment.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../../about/index.md).*