# Independent challenge — Module 15

> No step-by-step help this time. The lab gave you the pattern; this is where
> you prove you own it. Time yourself: target **90 minutes** of writing plus
> one **15-minute drill**.

---

## 1. The scenario

You are the only engineer responsible for the support early-alert system
(capstone, Modules 09/10/14: `release.py`, the FastAPI service, `monitor.py`).
At 09:40 on Monday:

- a routine log review shows **scoring requests every second from an IP you
  do not recognise**;
- at 09:52 a colleague forwards an email: **a student's address appeared in
  a pasted log snippet** in someone's ticket;
- at 10:05 CI fails: **`model.pkl` on the server no longer matches its
  recorded sha256**.

Three incidents, one morning, one of you.

## 2. Your deliverable: `RUNBOOK-incident-response.md`

Write the runbook your future team will actually follow. Required sections:

1. **Detection** — which signals arrive where (monitoring alert, scanner,
   hash mismatch), and who is paged.
2. **Containment steps** — numbered, copy-pasteable, for each of the three
   threads above. At least one must be a real command from this course
   (hint: key revocation *and* `python release.py rollback`).
3. **Assessment** — how you determine blast radius using lineage: which
   dataset (`data_sha256`), which run, which release, which requests.
4. **Notification** — who decides, who informs whom, and by when (roles, not
   names; note that this is a human decision the code cannot make).
5. **Recovery** — the exact gates a fixed build must pass before serving
   again (name them: tests? quality gate? re-registration?).
6. **Post-incident review** — the template: timeline, root cause, five
   whys, preventive actions with owners.
7. **Rehearsal schedule** — when the team drills this, and the fault you
   will inject next time.

## 3. The drill (evidence, not prose)

Execute **one** containment path against your own capstone system:

```powershell
# 🪟 from examples/capstone-support
python release.py register --note "pre-drill"
# tamper: flip one byte in artifacts/model.joblib, restart the service or
# run the integrity check your service performs
python release.py rollback
python release.py history        # your audit trail must show what happened
```

Paste the real terminal output into the runbook's drill section. If your
service does not yet verify integrity, *that is a finding* — add it to the
risk register with an owner (you).

## 4. Grading yourself (the bar)

Your runbook passes if a teammate could execute it **without asking you a
single question**:

- every step is a command or a decision with a named role — no "investigate
  further" without saying how;
- the three threads each get a containment action within the first section;
- rollback appears *before* recovery, and recovery re-states the gates;
- the drill output is real, with timestamps, and the rollback shows in
  `release.py history`.

## 5. Stretch (optional, +15 min)

Write the one-paragraph **external notice** for thread 2 (the leaked
address): what happened, what data, what you are doing, what affected people
should do. Rule: no minimising language, no blame, no speculation about
impact you have not verified.

---

[← Lab](lab.md) · [Next: knowledge check →](knowledge-check.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*