# LAB-05 — Deterministic by Construction

## 1. Lab identity

| | |
|---|---|
| **Lab ID** | **LAB-05** |
| **Difficulty / topic** | 🌱→🔧 Beginner·Intermediate · Pipeline design |
| **Prerequisite module** | [05 — Reproducible training and pipelines](../modules/05-reproducible-training-pipelines/index.md) · LAB-01 recommended |
| **Fixture** | `examples/labs/lab-05/` |
| **Estimated time** | 120 minutes · free, local, offline |

## 2. Scenario and background

`pipeline_flawed.py` runs four real stages (`prepare → features → train →
evaluate`) and writes five output files — but two runs disagree. The
manifest hash changes, the model bytes change, the metrics wobble. Your
team's release process hashes artefacts before shipping; with this
pipeline, every release would look "tampered". Three spots in the code
are marked suspicious with comments ending in `...` — but **not all of
them are guilty**, and part of the exercise is proving which are.

## 3. Learning objectives

By the end you can:

1. Audit a multi-stage pipeline for every nondeterminism source:
   seeds, time, ordering, environment.
2. Separate *guilty* from *cosmetic* findings with isolated experiments.
3. Make stage outputs byte-stable and hash the manifest as the release
   contract.
4. Write a determinism regression test a teammate can run.

## 4. Prerequisites and estimated time

- LAB-01 completed (you own the hunting method); Module 05 read.
- `python make_data.py` in `examples/labs/`.
- **120 min** (reproduce 20 · isolate 45 · fix 30 · prove+test 25).

## 5. Student task statement

Produce `pipeline_fixed.py` (your copy) where **two consecutive runs to
different output folders produce identical SHA-256 for every output
file**, plus a one-page audit note classifying each suspicious spot as
guilty/harmless with evidence, plus a pytest determinism test.

## 6. Required dataset and setup instructions

```powershell
# 🪟 Windows — PowerShell
cd examples\labs
python make_data.py
cd lab-05
python pipeline_flawed.py --out outA
python pipeline_flawed.py --out outB
```
Then compare (see §9 for exact commands). 🐧: identical commands.

## 7. Starter files

| File | Role |
|---|---|
| `pipeline_flawed.py` | 4 stages; 3 commented suspects (2 guilty, 1 decoy) |
| `outA/`, `outB/` | your two runs: `prepared.csv`, `features.csv`, `model.joblib`, `metrics.json`, `manifest.json` |

## 8. Numbered implementation steps

**Step 1 — Reproduce.** Run to `outA` and `outB` (§6); hash every file in
both.
✅ Checkpoint: `prepared.csv` and `features.csv` are **identical**;
`metrics.json`, `model.joblib`, `manifest.json` **differ**. Real observed
metrics: `roc_auc 0.8946 / seed 1792975430` vs `0.8990 / seed 1792975434`.

**Step 2 — Classify the suspects.** For each marked spot: state what it
*could* change, then design the one-line experiment that proves or
disproves it. ✅ Checkpoint: your audit table says which spots are guilty
(the clock-driven ones) and which is harmless *today* — with a note on
why "harmless today" is still worth pinning.

**Step 3 — Fix the guilty ones in your copy.** Real seed for the split;
no wall-clock anywhere in artefacts (put run metadata in a log, not in
hashed outputs).

**Step 4 — Prove byte-identity.**
```powershell
python pipeline_fixed.py --out fixA
python pipeline_fixed.py --out fixB
python -c "import hashlib,pathlib; \
[print(p.name, hashlib.sha256((pathlib.Path('fixA')/p.name).read_bytes()).hexdigest()==hashlib.sha256((pathlib.Path('fixB')/p.name).read_bytes()).hexdigest()) for p in pathlib.Path('fixA').iterdir()]"
```
✅ Checkpoint: every line prints `True`.

**Step 5 — Regression test.** `test_determinism.py`: runs the pipeline
into two `tmp_path` dirs (fast: accept a `--ticks`-style shrink if you
added one) and asserts equal hashes. ✅ `python -m pytest -q` green.

**Step 6 — Contract note.** One paragraph: what the manifest hash now
guarantees — and what it still cannot (environment, hidden inputs).

## 9. Commands and expected results

| Command | Expected |
|---|---|
| `python pipeline_flawed.py --out outA` / `outB` | stage lines + differing `manifest sha256` (fault) |
| hash comparison across `outA`/`outB` | csv files SAME; metrics/model/manifest DIFFER |
| fixed script, `fixA` vs `fixB` | all `True` |
| `python -m pytest -q` | green, incl. your determinism test |
| rerun fixed script into a *dirty* folder (leftover files) | still all `True` (explain any exception in the audit) |

## 10. Acceptance criteria (objective)

- [ ] Fault reproduced; per-file SAME/DIFFERS table pasted.
- [ ] All three suspicious spots classified with an experiment each.
- [ ] Two runs of your fixed pipeline: byte-identical outputs (all `True`).
- [ ] Manifest hash identical across the two runs.
- [ ] `test_determinism.py` exists and passes.
- [ ] Contract note written (guarantees vs non-guarantees).

## 11. Troubleshooting and recovery

| Symptom | Cause | Fix |
|---|---|---|
| model bytes differ though metrics match | joblib pickles non-canonical internals, or estimator not seeded | seed everything; if bytes still wobble, compare **predictions** + metrics and document why (know the difference) |
| `ValueError: could not convert string to float` | identifier column entered the features | exclude `customer_id` (the shipped version shows the fix) |
| outputs differ only in one file | inspect that file's writer for timestamps/paths | run metadata must not live in hashed artefacts |
| test hangs | pipeline too slow for a test | add a `--limit-rows` option (deterministic subsetting) |

## 12. Reflection questions

1. Why is a *decoy* suspicious spot valuable in a code review — and how
   would you phrase the "harmless today" caveat to a teammate?
2. The manifest hashes artefacts but not the *code*. What single line
   would you add, and which Module concept does it come from?
3. Determinism has a cost (e.g. threading, approximate algorithms).
   Name a case where you would *document* nondeterminism instead of
   removing it.

## 13. Optional challenge tasks

1. Make the pipeline incremental: unchanged stages skip (hash-keyed) —
   and prove identical outputs on a warm re-run.
2. Add an `--env-report` stage writing package versions to the log (not
   the artefacts).
3. Run under a different `PYTHONHASHSEED` and show outputs still match.

## 14. Rubric / checklist

| Points | Criterion |
|---|---|
| 3 | fault table (per-file SAME/DIFFERS) reproduced |
| 4 | three suspects classified with stated experiments |
| 5 | all outputs byte-identical across two runs, evidence pasted |
| 2 | determinism pytest test, green |
| 2 | contract note honest about non-guarantees |
| **16** | **total** · ≥12 = pass |

## 15. Cleanup

```powershell
cd examples\labs\lab-05
Remove-Item -Recurse outA,outB,fixA,fixB -ErrorAction SilentlyContinue
```

---

**After attempting:** a reference fix lives in
[`examples/labs/solutions/lab-05/`](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/labs/solutions/lab-05).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../about/index.md).*