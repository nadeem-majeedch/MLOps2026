# Knowledge check — Module 15

## How to use this

1. Answer **in writing**, open book first, then closed book.
2. Mark yourself with the [answers](#answers) — **only after** committing to
   yours.
3. Target: **80% with justified reasoning**. Below that, re-read
   [concepts.md](concepts.md) §§1–6 before moving on.
4. Self-assessment inside a *suggested self-study framework* — not an
   official university exam. See
   [assessment-framework](../../syllabus/assessment-framework.md).

---

## Questions

**Q1.** In one sentence each: distinguish *authentication*,
*authorization*, and *input validation*. Which lab defect was which (or
none)?

**Q2.** Why is a database password inside a connection string a *secret*
even though the URL itself is configuration? What decides the boundary?

**Q3.** Your CI secret scan is clean. Give three attacks or failures it
does **not** address.

**Q4.** Explain to a teammate why `pickle.load` is dangerous *even when the
file comes from your own build*, and name the control that makes it
acceptable in the lab's fixed version.

**Q5.** A log line reads
`predict email=amina@example.edu ref=S-0007 score=0.81`. Identify every
privacy problem and give the replacement line.

**Q6.** Compute-then-interpret: with rates 0.1935 (group 0) and 0.1270
(group 1), what is the selection-rate gap? Is it within the course's 0.10
target? What does being within target **not** prove?

**Q7.** The flawed rule gave group 0 a flag rate of exactly 0.0000.
Explain the arithmetic, then the human consequence in one sentence.

**Q8.** Why does the capstone refuse promotion when fairness is over target
even though the gate (`roc_auc`) passed? What converts a refusal into a
shippable decision?

**Q9.** Name the four governance artefacts from concepts §6 and the one
question each answers for an auditor.

**Q10.** Order the incident-response phases for the three-thread scenario
in the independent challenge, and say which single action comes *first*.

---

## Answers

**A1.** *Authentication* = proving who you are (lab defect 3: no check at
all → the endpoint accepted anonymous callers). *Authorization* = whether
that identity may do *this* (no defect of its own here — note the gap in
your risk register!). *Input validation* = rejecting malformed data before
it reaches logic (the pydantic `ge/le` constraints are already right in the
flawed code — validation existed while authentication did not, a classic
miscalibration of effort).

**A2.** Because its *blast radius* is external: the string grants power over
a live database, so a public diff is an incident. The deciding question is
"does leaking this force a response outside this repository?" — not whether
the value sits in the middle of a longer string.

**A3.** Any three: unauthenticated endpoints; PII in logs; unfair decision
rules; tampered model bytes; DoS via unbounded inputs; vulnerabilities in
dependencies; insider access. Scanners see *strings in files*, not design
flaws — hence the threat model.

**A4.** Pickle does not store data, it stores instructions to rebuild
objects — loading runs Python code, so swapped bytes execute as your
service. "It came from our build" only holds until one link in that chain
(checkout, cache, shared drive) is writable by someone else. The lab's
control: verify the sha256 of the bytes against a recorded digest
*before* loading, so tampering fails closed — plus the tamper drill proving
the check fires.

**A5.** Two problems: the email (direct identifier) and the score attached
to it (a sensitive inference about a person). Replacement:
`predict ref=S-0007 score=0.81` — keep the pseudonymous reference for
debugging, drop the identifier; ideally also apply a retention limit to the
log itself.

**A6.** gap = |0.1935 − 0.1270| = **0.0665**, which is within the 0.10
target. Within target proves only parity on *this one metric, this one
window, this one group definition* — not fairness overall: other definitions
may disagree, residual gaps remain, the label itself may encode historical
disadvantage, and the number says nothing about whether either group is
being *helped*.

**A7.** Group 0's threshold was 0.60 while no record in that group scored
≥ 0.60 (their probabilities topped out below it), so zero crossed it —
meanwhile group 1's 0.25 threshold let 12.7% through. Human consequence: a
support service that never, in 400 real decisions, offered help to a single
student without a reliable device.

**A8.** The gate measures *quality* (roc_auc ≥ floor); the fairness audit
measures *impact on people*. They are independent axes — a model can be
accurate and systematically exclude a group. The refusal converts to a
shippable decision only by **explicit human risk acceptance**: an `--ack`
reason, recorded in the audit history with who and when
(`python release.py promote r001 --ack "…"`), never silently.

**A9.** Model card → *what is this model and where must it not be used?*
Datasheet → *where did the data come from and what are its limits?*
Risk register → *what could go wrong, who owns it, what is accepted?*
Audit trail/lineage → *which data, code, and decisions produced what is
serving right now?*

**A10.** Detect (log review, forwarded ticket, hash-mismatch failure) →
**contain first: revoke the exposed key and stop the suspect traffic**
(boundary of the two technical threads) → assess blast radius via lineage →
human notification decision → recover through the stated gates →
post-incident review. The first action is containment of the *live*
exposure (key revocation / `release.py rollback` for the model thread) —
assessment must not delay it.

---

**Scoring:** 8+ correct with reasoning → proceed to Module 16. 6–7 →
re-read concepts §§1–6 and retry Q3, Q6, Q8. ≤5 → redo the lab steps 1–9
first; the answers should then be obvious.

---

[← Independent challenge](independent-challenge.md) · [Next: troubleshooting →](troubleshooting.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*