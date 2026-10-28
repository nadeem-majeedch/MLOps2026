# Independent challenge — Module 08

> Do this **without** step-by-step help. Target **75 minutes**. The lab gave you
> the pattern; this is where you prove you own it.

---

## 1. The task

Add a new stage to the shared example's pipeline: **`fairness`** — a group
comparison that must run after `evaluate` and before `report`.

## 2. What the stage must do

```
... → train → evaluate → fairness → report
```

- Read `pipe_out/features.csv` and `pipe_out/model.joblib`.
- For the protected-attribute proxy the project uses (`contract_type`),
  compute the model's mean predicted probability per group and the gap
  between the highest and lowest group.
- Write `pipe_out/fairness.json` with `{"per_group": {...}, "gap": <float>}`
  and a `warned: true/false` flag when the gap exceeds **0.10** (the threshold
  is a course convention — justify or challenge it in your write-up).
- Make `report` include the fairness section (only if the file exists, so
  `report` still works during a transition).

## 3. Deliverables and proofs

1. **The diff** — your changes to `pipe/run.py` (declaration) and
   `pipe/stages.py` (implementation), each with a one-line justification.
2. **Incremental proof table.** For each experiment, the exact run log lines
   showing which stages ran vs skipped:

   | experiment | predict first | observed RUN stages |
   |---|---|---|
   | only `fairness()` source edited | | |
   | only `pipe_out/fairness.json` deleted | | |
   | only `report()` source edited | | |
   | `config.yaml` `seed` changed | | |

3. **Gate test:** set the fairness gap threshold to `0.0` (guaranteed breach)
   and show `fairness` failing with `BLOCKED` on `report`, exit code 1, and the
   manifest entry. Restore it.
4. **Clean rebuild:** `python -m pipe.run --clean` completes with the fairness
   section present in `report.md`.
5. **90-word reflection:** one thing the declaration made easy that a shell
   script would have made fragile.

## 4. Self-check (feedback criteria, no step-by-step solution)

| Grade | Looks like |
|---|---|
| **Excellent (4)** | Stage declared with complete inputs/outputs; all four incremental predictions correct *and explained*; gate failure captured with output; clean rebuild passes; reflection specific |
| **Proficient (3)** | Stage works and incremental table mostly right; one proof missing |
| **Developing (2)** | Stage works but outputs undeclared (everything re-runs), or predictions missing |
| **Not yet (1)** | No run logs, or the graph was edited in a way that breaks existing stages |

**Common failure to avoid:** adding the *function* but not the *declaration* —
if `fairness` is missing from `TASKS` in `run.py`, the runner will never call
it and your report will silently lack the section. The graph is the source of
truth, not the function file.

---

**Next:** [knowledge-check.md](knowledge-check.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*