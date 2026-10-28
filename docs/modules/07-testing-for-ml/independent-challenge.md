# Independent challenge — Module 07

> Do this **without** step-by-step help. The lab gave you the pattern; this is
> where you prove you own it. Time yourself: target **90 minutes**.

---

## 1. The scenario

A colleague's small project has *some* tests, but nobody trusts them. You are
asked to audit the suite and finish it. The project: a customer-segmentation
script that reads a CSV, scales features, fits K-means, and writes cluster
labels.

## 2. The code under audit

```python
# segment.py
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def segment(path: str, k: int = 4, seed: int = 42) -> pd.DataFrame:
    df = pd.read_csv(path)
    X = df[["age", "income", "visits"]].fillna(0)
    Xs = StandardScaler().fit_transform(X)
    model = KMeans(n_clusters=k, n_init=10, random_state=seed).fit(Xs)
    df["cluster"] = model.labels_
    return df

if __name__ == "__main__":
    segment("customers.csv").to_csv("segments.csv", index=False)
```

Its entire test suite:

```python
# test_segment.py
def test_it_runs():
    segment("customers.csv")
```

## 3. Your tasks

1. **Audit (written):** list every *distinct* property of this system that is
   currently untested, grouped by layer (unit / data / model / integration /
   regression). Aim for at least eight properties — think about missing values,
   unknown columns, `k` larger than rows, determinism, output shape, and what
   "good clusters" could mean.
2. **Write the tests.** Implement at least **seven** of your audited properties,
   spanning at least four layers. Generate your own small fixture data inside
   `tmp_path` — do not depend on a `customers.csv` you did not create.
3. **Break one deliberately.** Seed a defect (e.g. silently `fillna(-1)`), show
   the named test that catches it, and record the failure output.
4. **Judge the weakest test.** Quote your least useful test, explain why it is
   weak, and rewrite it to assert a property instead of a behaviour-free "it runs".
5. **Recommend a gate.** State which single test you would make blocking in CI
   (Module 12 preview) and justify it in one sentence.

## 4. Deliverables

- `audit.md` — the property list with layers.
- `test_segment.py` — your suite, green on the fixed code.
- `bug-catch.md` — the seeded defect, the catching test, the failure output.
- `recommendation.md` — tasks 4 and 5.

## 5. Self-check (no step-by-step solution — feedback criteria only)

| Criterion | Looks like |
|---|---|
| **Excellent (4)** | ≥7 tests over ≥4 layers; each maps to an audited property; bug caught by a named test; the rewritten test asserts a property; gate choice justified by risk |
| **Proficient (3)** | 5–6 tests, 3+ layers, bug caught, recommendation present but thin |
| **Developing (2)** | Tests exist but mostly "it runs"; weak mapping to properties |
| **Not yet (1)** | No seeded-bug evidence, or suite not runnable |

Common failure mode to avoid: testing the *library* instead of *your* code
(`assert KMeans is not None`). Test the properties your code adds.

---

**Next:** [knowledge-check.md](knowledge-check.md) ·
Compare notes with the course suite in [worked-example.md](worked-example.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*