# LAB-05 — reference solution

> Attempt the lab first. This is the answer key, not the assignment.

## Verified "before" transcript (authoring machine)

```text
run A:  manifest sha256[0:16] = 6587eb06967bb2c4a…
run B:  manifest sha256[0:16] = e149bbb5a03a9f63…
prepared.csv  IDENTICAL
features.csv  IDENTICAL
metrics.json  DIFFERS   roc_auc 0.8610 (seed 1793064993)
                        roc_auc 0.9247 (seed 1793064996)
model.joblib  DIFFERS
manifest.json DIFFERS   (its outputs hashes + run_finished_at)
```

The identical intermediate CSVs prove the *data path* is fine — every
difference is manufactured later. That narrows the audit to three
guilty lines.

## The three defects and their fixes

| # | Line | Fix |
|---|---|---|
| 1 | `stage_features` discovers columns dynamically from the data | read the column list from config (`FEATURES` constant): a schema change must break loudly, not silently re-order features |
| 2 | `seed = int(time.time())` | a real seed: `seed = 42` (or a `--seed` flag with a fixed default) and pass it to `train_test_split(random_state=…)` |
| 3 | `"run_finished_at": time.strftime(…)` baked into the hashed artifact | move timestamps **outside** the hashed content (log them separately), or hash a canonical form that excludes volatile fields |

**Proof (the whole lab):** run twice into different `--out`
directories and compare **everything**:

```powershell
python pipeline_flawed.py --out outA
python pipeline_flawed.py --out outB
foreach ($f in 'prepared.csv','features.csv','metrics.json','model.joblib','manifest.json') {
  fc /b outA\$f outB\$f        # 🪟: "FC: no differences encountered"
}
```

```bash
# 🐧
for f in prepared.csv features.csv metrics.json model.joblib manifest.json; do
  cmp -s "outA/$f" "outB/$f" && echo "$f IDENTICAL" || echo "$f DIFFERS"
done
```

**Acceptance:** all five files byte-identical, including the manifest.

## Reasoning checkpoints (model answers)

- **Which defect matters most?** #2 — it changes the *model itself*.
  #3 only changes provenance bytes, but it is the one that silently
  poisons "same manifest = same run" comparisons, so it is not optional.
- **Why did the intermediates match?** Determinism is a property of the
  *whole path*, stage by stage: prep was pure, so it matched even while
  training was chaotic. Audit by stage, not by vibes.
- **Should timestamps be forbidden?** No — record them, just don't put
  them *inside* the thing you compare. Provenance metadata and
  reproducible content are different layers.

## Common wrong answers

- Comparing only `prepared.csv` and declaring victory — the model is
  the deliverable.
- "Fixed" defect 3 by keeping the timestamp but not hashing the manifest
  — you must state *which* bytes are the identity of a run.
- One run as proof — reproducibility claims need ≥2 runs and a diff.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../../docs/about/index.md).*