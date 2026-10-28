# LAB-01 — reference solution

> Attempt the lab first. This is the answer key, not the assignment.

## The three sources of nondeterminism

| # | Where | Why it changes results |
|---|---|---|
| 1 | `load()` → `df.sample(frac=1)` | unseeded shuffle reorders rows every run |
| 2 | `main()` → `df.sample(frac=0.8)` | unseeded subsample picks a **different 80% of customers** each run — different training data, different test data |
| 3 | `GradientBoostingClassifier(random_state=None)` **and** `train_test_split(...)` with no `random_state` | unseeded split + unseeded stochastic booster |

**Verified transcript (authoring machine):**

```text
run --label a:  roc_auc 0.8126  f1 0.4571  n_test_rows 120
run --label b:  roc_auc 0.8284  f1 0.3704  n_test_rows 120
```

Same data file, same code, two answers — that is the whole incident.

## The fix (all four places)

```python
df = df.sample(frac=1, random_state=42).reset_index(drop=True)   # or delete it
sample = df.sample(frac=0.8, random_state=42)                    # or delete it
x_tr, x_te, y_tr, y_te = train_test_split(
    x_use, y_use, test_size=0.25, stratify=y_use, random_state=42)
model = GradientBoostingClassifier(n_estimators=120, subsample=0.8,
                                   random_state=42)
```

**Verification:** run twice (`--label a`, `--label b`) and compare the
two JSON files — they must be byte-identical:

```powershell
fc metrics_a.json metrics_b.json     # 🪟 "no differences encountered"
diff metrics_a.json metrics_b.json   # 🐧 no output = identical
```

## Reasoning checkpoints (model answers)

- **Which suspect matters most?** #2: it changes *which data the model
  learned from*, so it moves the metric the most. #1 and #3 only change
  ordering/optimisation noise.
- **Does the shuffle alone matter?** Not by itself — row order is
  harmless *if* every downstream selection is seeded and
  order-independent. It becomes a bug here because it feeds unseeded
  sampling and splitting. (Seeding it is still right: fewer moving parts.)
- **Is a small metric difference "fine"?** No: you cannot tell 0.8126 vs
  0.8284 from a real improvement, so *any* comparison against it —
  including a quality gate — is untrustworthy.
- **Determinism ≠ correctness:** an identical wrong answer is still
  wrong; determinism only makes results *comparable*.

## Common wrong answers

- "The data must have changed" — the CSV on disk never changes; hash it
  before/after to prove it.
- Seeding only the model — the split and subsample still vary; you get
  different test sets every run.
- Claiming you fixed it with one run — the claim needs **two runs and a
  diff**, not one.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../../docs/about/index.md).*