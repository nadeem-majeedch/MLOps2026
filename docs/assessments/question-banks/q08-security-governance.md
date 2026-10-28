# Question bank 08 — Security and governance

**Covers:** Module [15 — Security, privacy, governance, fairness](../../modules/15-security-privacy-governance/index.md)
and the [security lab](../../labs/lab-19-deployment-security-review.md).
**Format:** 10 questions — multiple choice, short answer, debugging, architecture, scenario.
**Suggested check:** 7/10, with **S5** and **S10** correct.

> *Attempt first, then read the
> [reference solutions](../keys/question-banks-KEY.md).*

---

## Part A — Multiple choice

**S1.** A secret is found in a committed file. The correct response order is:

- (a) Delete the file, do nothing else
- (b) Remove it from source, **rotate the credential**, purge/accept the history
  exposure, then add a scanning guard
- (c) Rewrite history quietly and hope
- (d) Add it to `.gitignore`

**S2.** `pickle`/`joblib` loading of an untrusted model file is dangerous
because:

- (a) It's slow
- (b) Deserialisation can execute arbitrary code chosen by whoever made the
  file
- (c) It corrupts memory safely
- (d) It doesn't support numpy

**S3.** Least privilege for a CI workflow means:

- (a) `permissions: write-all` for convenience
- (b) The narrowest token scope that completes the job (e.g.
  `contents: read`)
- (c) No permissions key at all
- (d) Personal access tokens for everyone

**S4.** A fairness metric that differs by group means:

- (a) Nothing until a lawyer says so
- (b) You should measure it, document it, choose a threshold policy
  deliberately, and record who approved it — before deployment
- (c) Retrain until the difference is zero, always
- (d) Delete the protected attribute and the problem disappears

## Part B — Short answer

**S5.** Explain *model lineage* and *auditability* as engineering artefacts:
what files/records exist, and which question each one answers.

**S6.** What is the difference between logging a *pseudonymous* identifier and
logging raw PII, in terms of both risk and usefulness for monitoring?

**S7.** Name four things a threat model for an ML prediction API must state on
one page.

## Part C — Debugging

**S8.** The lab's flawed service has five seeded defects. Locate and classify
each (confidentiality / integrity / availability / fairness), and give the fix:

```python
API_KEY = "prod-secret-2f8a1c77b4e9d0136ac5"        # config.py:13
logger.info(f"user {email} scored {p} for {user}")   # predict()
@app.post("/predict")                                # no auth anywhere
model = pickle.load(open("model.pkl", "rb"))         # untrusted path
flag = 1 if p >= (0.35 if group == "A" else 0.25) else 0
```

## Part D — Architecture

**S9.** Draw a deployment with: client, API, model store, secret store,
monitoring. Mark every trust boundary and state the check that belongs on
each.

## Part E — Scenario

**S10.** Your review finds the scanner reports "clean" but you spot that a
model card omits intended-use limits, the container runs as root, and no one
can say which dataset trained the shipped model. Write the verdict paragraph:
severity of each, what must be fixed before deployment, what may be accepted
with an owner and a review date, and how you would phrase a *conditional*
approval.

---

**Next:** [reference solutions](../keys/question-banks-KEY.md) (bank 08), then
[bank 09](q09-cloud-advanced-operations.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../../about/index.md).*
