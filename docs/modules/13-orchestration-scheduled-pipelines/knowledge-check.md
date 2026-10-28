# Knowledge check — Module 13

## How to use this

1. Answer in writing, closed book on the second pass.
2. Mark with the [answers](#answers) only after committing.
3. Target **80% with justified reasoning**; below that re-read
   [concepts.md](concepts.md) §§1–§6.
4. Suggested self-study framework, not an official exam:
   [assessment framework](../../syllabus/assessment-framework.md).

---

## Questions

**Q1.** Your pipeline is three stages, run by one person, on a laptop. Which
automation level from concepts §1, and what would push you to the next level?

**Q2.** *(True/False + why)* "Orchestration makes a pipeline more correct."

**Q3.** The failure demo produced three attempts with **identical** error
strings. What class of failure is that, what should the response be, and what
would a *transient* failure's attempts look like instead?

**Q4.** Explain the `no_new_data` tick: what two conditions must hold, and
give two reasons an explicit skip record beats silence.

**Q5.** Why does the alert file get **deleted** on recovery? What failure mode
of alerting systems does that prevent?

**Q6.** Interval vs event triggering: one sentence each, and which the course
runner uses by default with one honest reason.

**Q7.** Name three things an orchestrator will *not* fix, citing the module
each belongs to.

**Q8.** What idempotency requirement does scheduling impose on the five
stages, and which Module 08 property already provides it?

**Q9.** For a single student's one pipeline, argue *against* installing
Airflow — then name the signal that would reverse your argument.

**Q10.** Where in this module's design does "secrets never in logs" resurface
(even though we have no secrets here)?

---

## Answers

**Q1.** Level 1 — a script (optionally one OS timer). Moving up is justified
by unattended scheduling, alerting needs, audit requirements, or wasted
re-runs — i.e. when at least two of concepts §1's conditions hold. *(5/5)*

**Q2. False.** Orchestration changes *when* and *whether* work runs, not
whether it is right: bad tests, weak gates, or broken data now fail
*on schedule, unattended* (concepts §8). Correctness comes from Modules 04,
07–09; orchestration amplifies whatever quality already exists. *(5/5)*

**Q3.** **Deterministic failure** (contract violation, bad config) — identical
inputs produce identical errors. Response: stop, read the first attempt,
fix the cause; do not raise retries. A transient failure's attempts would
*differ* (timeout at 1.0s, then success; or connection refused once, then
ok) — the evidence that retrying was right. *(5/5)*

**Q4.** Conditions: the last run succeeded **and** the data hash is
unchanged **and** outputs are intact. Reasons explicit beats silence: (1)
cost — no pointless retraining; (2) signal — a history you can distinguish
"worked" from "had nothing to do" from "failed" keeps humans trusting the log
(concepts §4). *(5/5)*

**Q5.** A recovered system stops shouting: if the alert persists after
resolution, people learn alerts are stale and start ignoring *all* of them —
the core of **alert fatigue**. Deleting on success makes alert presence mean
"currently broken", which is a state you can act on. *(5/5)*

**Q6.** *Interval*: fire every N seconds regardless of state (simple, may find
nothing to do). *Event*: fire when something changes (a file, a webhook).
Default here is **interval** because polling is simpler to teach, debug, and
run offline — event triggers (challenge task 3) are the natural upgrade. *(5/5)*

**Q7.** Weak/absent **tests** (Module 07), missing **data contracts and
gates** (Modules 04/08), absent **lineage/registry** (Module 09), and silent
**drift** (Module 14). Pick any three with the module named. *(5/5)*

**Q8.** Every task must be safe to run twice (a retried or re-scheduled tick
must converge to the same state). Module 08's **determinism + declared
outputs** already gives this: stages overwrite their own outputs with
identical bytes, which is also why the skip logic is sound. *(5/5)*

**Q9.** Airflow would add a scheduler process, a metadata DB, a web server and
ops burden to solve problems (multi-DAG, multi-team, SLAs) this student does
not have — cost without correspond­ing need, violating the course's
no-unnecessary-enterprise-complexity principle. **Reversal signal:** a second
and third pipeline appear, other people depend on their outputs, or a missed
run now has a real deadline attached. *(4/5 — judgement; accept reasoned
alternatives)*

**Q10.** The alert carries **diagnosis text (attempt errors) but never
payload dumps**, and history records hashes rather than contents
(concepts §5–§6) — the habit of "what goes into a durable, shared artefact"
is the same discipline that later keeps tokens out of logs (Module 12's
three-place rule). *(4/5 — interpretive; accept well-argued answers)*

**Scoring:** /50 → ×2 = %. **80+ ready.** 60–79: redo lab Steps 4 and 7.
Below 60: re-read concepts §1–§5 with the worked example alongside.

---

**Next:** [troubleshooting.md](troubleshooting.md) ·
[Module 14 →](../14-monitoring-drift-retraining/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*