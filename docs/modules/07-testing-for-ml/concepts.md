# Concepts — Module 07

Software testing answers *"did my change break anything?"* ML testing must also
answer *"is the system still good enough to be worth running?"* — a different
question, needing different tests.

---

## 1. The five layers

| Layer | Subject | Speed | Example in this course |
|---|---|---|---|
| **Unit** | One function, in isolation | ms | `split_xy` returns exactly the configured columns |
| **Data** | The input's claims | ms | no nulls; keys unique; target balance sane |
| **Model** | Quality and behaviour | seconds | ROC AUC ≥ floor; probabilities in [0,1] |
| **Integration** | The whole path | seconds | CSV → validate → train → save → reload → predict |
| **Regression** | Nothing got worse | seconds | a metric floor that failed before a change |

**How they stack** (cheap and frequent at the bottom):

```
        ┌────────────────────┐
        │ integration (few)  │      run on every change
        ├────────────────────┤
        │ model / regression │      run on every change, may be slower
        ├────────────────────┤
        │ data tests         │      run whenever data or loaders change
        ├────────────────────┤
        │ unit (many)        │      run always — they are nearly free
        └────────────────────┘
```

You do not choose a layer; you build all of them, each doing the job only it can
do. Module 12 wires the suite into CI so it runs without anyone remembering to.

---

## 2. Assertions are thresholds, not truths

A conventional assertion is exact: `assert add(2,2) == 4`.
An ML assertion is a *policy*: `assert roc_auc >= 0.70`.

That difference has three consequences:

1. **Floors are chosen, not discovered.** 0.70 comes from what the business can
   accept, plus what the data can support — write down the reasoning next to the
   number (our suite does).
2. **Floors can be flaky by construction.** With 400 test rows and ~36
   positives, metric movement of ±0.03 from seed alone is normal (measured in
   Module 05). Set a floor inside the noise band and your build becomes a coin
   flip. Mitigations: widen the floor, fix the evaluation split, or evaluate on a
   frozen hold-out.
3. **A failing floor is information.** It means either the *code* broke or the
   *world moved* (data drift). Your job is to say which — the diagnosis rules in
   [troubleshooting.md](troubleshooting.md) §3.

---

## 3. Determinism: tests you can trust

A test suite that fails randomly gets disabled within a month — and then nothing
is tested. Determinism rules for ML tests:

| Rule | Implementation in this course |
|---|---|
| Seed everything | `seed: 42` in `config.yaml`, used by split and model |
| Fix the inputs | Session-scoped fixtures read one versioned dataset |
| Generate missing data, do not download | `conftest.py` regenerates data if absent |
| Avoid time/external services in tests | Nothing in the suite opens a network socket |
| Keep tests independent | Each test writes to its own `tmp_path` — no shared mutable state |
| Bound the runtime | 19 tests in ~4 s; if a test needs minutes, it is not a unit test |

**Flaky test policy:** a test that fails intermittently is a *bug in the test*
until proven otherwise. Fix it or delete it; never ignore it.

---

## 4. Fixtures and the shared example

A **fixture** is prepared state a test runs against — pytest's `fixture`
mechanism provides them declaratively:

```python
@pytest.fixture(scope="session")     # created once for the whole run
def config(): ...

@pytest.fixture(scope="session")     # regenerates data on a fresh checkout
def data_path(): ...
```

`scope="session"` matters: loading data once keeps the suite fast enough to run
constantly. (This is also the pattern Module 08 will cache across pipeline stages.)

---

## 5. Coverage: a map of the dark, not a score

**Coverage** measures which lines executed during a test run. Real numbers from
this course's suite:

```text
Name              Stmts   Miss  Cover   Missing
src\features.py      25      0   100%
src\train.py         43     11    74%   46-54, 100-107, 111
src\validate.py      45     14    69%   42, 84-97, 101
TOTAL               113     25    78%
```

Read the gaps, not the total:

- `train.py` 46–54 = the gradient-boosting branch — **deliberately** untested;
  the lab's config-variant tests can cover it if you want.
- `train.py` 100–107 = the CLI `main()` — argument parsing, exercised by hand.
- `validate.py` 84–97 = the report printer — output formatting, not logic.

**Coverage cannot tell you whether your assertions are meaningful.** 100%
coverage with trivial assertions protects nothing. Use it to *find* untested
code, then decide deliberately: test it, or record why you will not.

---

## 6. What makes a test an ML test

Three patterns that do not exist in ordinary software testing:

1. **Performance floor** — quality below a threshold fails the build (gate).
2. **Invariance / robustness** — outputs must obey properties: probabilities
   bounded, predictions identical whether batched or one-by-one, irrelevant
   perturbations not flipping decisions.
3. **Data expectations** — the input must satisfy the contract from Module 04;
   a test that proves the validator *rejects* bad data is as important as one
   that shows it accepts good data.

Plus the meta-test: **the suite must fail when the system is broken.** That is
why the lab requires a documented failing run.

---

## 7. From suite to gate

```
developer runs pytest ──► CI runs pytest on every push (M12) ──► merge blocked on red
                                 │
                                 └── data + model gates run too
```

The suite is the enforcement mechanism for everything Modules 04–06 established:
validation rules, metric floors, reproducibility. Today you run it by hand;
Module 12 makes it involuntary.

---

## 8. Check yourself

1. Classify each as unit/data/model/integration/regression: *"customer_id is
   unique"*, *"AUC ≥ 0.70"*, *"pipeline writes metrics.json"*, *"split_xy returns
   four columns"*.
2. Why is a floor set at 0.70 less safe than it looks on a 400-row test set?
3. What does 78% coverage fail to tell you? Name two things.
4. Why does the suite regenerate data instead of requiring a download?
5. A test fails on your machine and passes in a colleague's. Order your next
   three checks.

*(Answers in [knowledge-check.md](knowledge-check.md).)*

---

**Next:** [worked-example.md](worked-example.md) — the suite run, its coverage table, and a real failing gate.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*