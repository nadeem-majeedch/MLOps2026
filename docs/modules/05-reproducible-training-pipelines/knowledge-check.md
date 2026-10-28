# Knowledge check — Module 05

Attempt every question first. **10 questions · ~30 minutes · open book.**
Suggested pass mark **7/10**, with no question about leakage or metrics wrong.

---

## Part A — Recall

**Q1.** List the five stages of the course's training pipeline and say what each
stage's output is.

**Q2.** Define: *feature leakage*, *train/serve skew*, *random seed*, *baseline*,
*stratified split*.

**Q3.** Name four sources of non-determinism that a seed does **not** fix, with
one fix each.

**Q4.** Which values belong in `config.yaml`, and what is the test for whether
something should be code instead?

## Part B — Comprehension

**Q5.** A colleague fits `StandardScaler` on the full dataset before splitting,
arguing "the scaler only looks at statistics". Explain the defect and its
consequences in production.

**Q6.** The baseline reports `accuracy 0.91`, `f1 0.0`, `roc_auc 0.7163`.
Explain each number, and say which one you would put in a report to the business
— and why the other two would mislead.

**Q7.** Two runs produce identical metrics but different model hashes. Is the
pipeline reproducible? What do you check next?

**Q8.** Changing only the seed moved AUC from 0.7163 to 0.7418. What does this
tell you about trusting a single run's number?

## Part C — Application

**Q9.** Write the exact commands (🪟 and 🐧) to: validate the data, train,
and compare the artefact hash against a value you recorded earlier. What is your
pass criterion?

**Q10.** You must add a feature that depends on data only available an hour
after scoring time. Which stage does it belong in, what happens if you put it
where the current features are, and what is the symptom in production?

---

# Answers and reasoning

**Q1 — 1 point (0.2 each).**
Validate (a pass/fail report) → features (a feature matrix and split indices) →
train (a fitted pipeline object) → evaluate (a metrics dict) → persist
(`model.joblib` + `metrics.json`).
*Reasoning:* naming outputs forces the input/output contract that later stages
(Module 07 tests, Module 08 scheduling) depend on.

**Q2 — 1 point (0.25 each).**
*Feature leakage* = information available at training but not at prediction time
entering the features (or test data influencing training statistics).
*Train/serve skew* = training and serving preparing data differently.
*Random seed* = a value initialising pseudo-randomness so runs repeat.
*Baseline* = the simplest credible reference a new model must beat.
*Stratified split* = a split preserving the target's class proportions.
*Reasoning:* leakage and skew are the two ML-specific failure modes this module's
design prevents structurally.

**Q3 — 1 point (0.25 each).**
Dependency versions → lock file; changed input bytes → data versioning;
unordered iteration → sort explicitly; parallel accumulation → fix thread counts;
platform/BLAS differences → same pinned platform or metric tolerance.
*Reasoning:* this list is the bridge between Modules 02 and 04 — reproducibility
is a property of the *whole* environment.

**Q4 — 1 point.**
Config holds values you would sweep, compare, or justify (seed, split size,
hyperparameters, paths, thresholds). Test: *could editing this silently
invalidate the meaning of past runs?* If yes, it is logic → code under tests.
*Reasoning:* wrong classification is what makes configs rot into secret code.

**Q5 — 1 point.**
The scaler learns mean/variance from data it should not see — test statistics
leak into training, so reported performance is optimistically biased and does
not reflect unseen data. In production, serving scales with *training*
statistics while the live distribution differs → systematic skew.
Cure: preprocessing inside the `Pipeline`, so `fit` only ever sees the training
partition.
*Reasoning:* the bug is invisible in code review and only visible in the gap
between offline and online numbers.

**Q6 — 1 point.**
Accuracy 0.91 = the majority-class rate; it says the model found no churners
(the "always predict no churn" model scores identically). F1 0.0 = at a 0.5
threshold, zero churners were predicted — no precision/recall to balance. AUC
0.7163 = the model *ranks* churners above non-churners ~72% of the time, which
is real signal. Report AUC (or recall at a contact budget), because the business
question is "who should we contact", not "how many rows are right".
*Reasoning:* metric choice is a claim about the decision being supported.

**Q7 — 1 point.**
Not yet — matching metrics can hide invisible differences (rounded metrics are
coarse). Next: check unseeded randomness in every stochastic step, then
dependency versions and input hashes; re-run after each fix until the bytes match.
*Reasoning:* hash equality is the strict claim; metric equality is the weak one.

**Q8 — 1 point.**
That single-run numbers are dominated by sampling variance here: with 400 test
rows and ~36 positives, the split itself moves AUC by ~0.03. Therefore: report
distributions (repeated runs or cross-validation), state the split and seed, and
never treat a one-run delta as an improvement claim.
*Reasoning:* this is the empirical motivation for Experiment tracking (M06).

**Q9 — 1 point (½ per shell, ½ for pass criterion).**
🪟:
```powershell
python -m src.validate --data data/raw/churn.csv
python -m src.train --config config.yaml --data data/raw/churn.csv
(Get-FileHash artifacts\model.joblib -Algorithm MD5).Hash.ToLower()
```
🐧: `python3 -m src.validate …`, `python3 -m src.train …`, `md5sum artifacts/model.joblib`.
Pass criterion: validation exits 0, metrics match the recorded values exactly,
and the hash equals the previously recorded hash.
*Reasoning:* validation gates the run; the hash is the verifiable identity claim.

**Q10 — 1 point.**
It belongs **outside** the online feature set — a batch/offline feature computed
at training time from late-arriving data, or excluded entirely. Putting it with
the online features means serving cannot compute it (or computes a stale
approximation) → train/serve skew: offline metrics look fine, live performance
degrades immediately after deployment. Symptom in production: unexplained quality
drop with clean dashboards — detected by Module 14's drift monitoring.
*Reasoning:* feature availability *in time* is part of the feature's definition —
the contract Module 09's registry records.

---

## Marking and next steps

| Score | Action |
|---|---|
| **9–10** | Proceed to Module 06 |
| **7–8** | Re-read the missed sections, then continue |
| **5–6** | Redo lab steps 1–5, then re-take |
| **< 5** | Re-read concepts §3–§5 and re-run the worked example first |

File your score as `modules/05/knowledge-check.md`.

---

[← Module overview](index.md) · [Troubleshooting →](troubleshooting.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*