# Question bank 04 — Testing and automation

**Covers:** Modules [07 — Testing for ML systems](../../modules/07-testing-for-ml/index.md)
and [08 — Pipeline automation](../../modules/08-pipeline-automation/index.md).
**Format:** 10 questions — multiple choice, short answer, debugging, architecture, scenario.
**Suggested check:** 7/10, with **T5** and **T10** correct.

> *Attempt first, then read the
> [reference solutions](../keys/question-banks-KEY.md).*

---

## Part A — Multiple choice

**T1.** Which test best catches *target leakage*?

- (a) A test asserting the model file exists
- (b) A test asserting no feature column is derived from the future/outcome
- (c) A test asserting `pytest` runs under 1 second
- (d) A test asserting the dataset has 1 000 rows

**T2.** A pipeline stage reads an input produced by a later stage. The runner
should:

- (a) Run them in whatever order the dictionary returns
- (b) Resolve the declared dependency graph and refuse to run the stage until
  its input exists
- (c) Retry until the file appears
- (d) Skip the stage silently

**T3.** What is the correct behaviour of a *quality gate* on failure?

- (a) Warn and continue
- (b) Fail the run, name the violated criterion and its value, and prevent
  promotion
- (c) Delete the candidate
- (d) Auto-loosen the threshold

**T4.** Which assertion is the most valuable in a training test suite?

- (a) `assert model is not None`
- (b) `assert metrics["roc_auc"] > 0.5` on a fixture with known signal and a
  documented floor
- (c) `assert True`
- (d) `assert len(X) == 1000`

## Part B — Short answer

**T5.** Explain the difference between *unit*, *data*, and *regression* tests
in an ML project, and give one concrete example of each from this course's
labs.

**T6.** What does "fail loudly" mean for a pipeline stage, and what are the
three ways a stage usually fails to do so?

**T7.** Describe how you would test a preprocessing step *without* training a
full model.

## Part C — Debugging

**T8.** This test is supposed to catch a leakage bug but always passes.
Explain why and rewrite it so it fails on the buggy code:

```python
def test_no_leakage():
    df = load_training_data()
    prep.fit(df)                      # preprocessing fitted on ALL data
    scores = evaluate(prep.transform(df))
    assert scores["auc"] < 0.99       # "not suspiciously perfect"
```

## Part D — Architecture

**T9.** Draw a pipeline DAG with at least five stages (data validation,
features, train, evaluate, register). Label each edge with what flows along it
and mark the two places a gate can refuse to continue.

## Part E — Scenario

**T10.** Your suite is green, yet a broken model reached staging last week.
Give three plausible explanations, and for each, the specific test or gate
that would have caught it.

---

**Next:** [reference solutions](../keys/question-banks-KEY.md) (bank 04), then
[bank 05](q05-apis-containers.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../../about/index.md).*
