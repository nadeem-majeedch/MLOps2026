# LAB-01 — The Reproducibility Detective

## 1. Lab identity

| | |
|---|---|
| **Lab ID** | **LAB-01** |
| **Difficulty / topic** | 🌱 Beginner · Reproducibility |
| **Prerequisite module** | [02 — Python, Git, CLI, environments](../modules/02-python-git-cli-environments/index.md) (then [05](../modules/05-reproducible-training-pipelines/index.md)) |
| **Fixture** | `examples/labs/lab-01/` |
| **Estimated time** | 75 minutes · free, local, offline |

## 2. Scenario and background

A colleague swears the model "got worse since Monday". The data file has
not changed — `python make_data.py --check` proves it byte-identical —
yet two runs of the same script report different metrics. You are the one
who has to explain why before the team's review at noon. Non-reproducible
training is the silent killer of ML trust: no experiment comparison, no
regression detection, no defensible release.

## 3. Learning objectives

By the end you can:

1. State the determinism contract: *same inputs + same code + same
   environment ⇒ byte-identical outputs*.
2. Hunt nondeterminism systematically (isolate → bisect → fix → prove)
   instead of "adding seeds until it stops".
3. Prove determinism with **hashes of outputs**, not with vibes.
4. Distinguish real nondeterminism from suspicious-looking-but-harmless
   code (the fixture contains both).

## 4. Prerequisites and estimated time

- Module 02 completed (venv, PowerShell, `python` on PATH); basic pandas.
- Datasets generated: `cd examples/labs && python make_data.py`.
- **75 min** (diagnose 40 · fix 15 · prove 20). No accounts, no GPU.

## 5. Student task statement

Fix **your copy** of `examples/labs/lab-01/train_nondeterministic.py` so
that two consecutive runs produce **byte-identical `metrics_*.json`**,
then write a short diagnosis: which of the three commented "suspicious
spots" actually mattered, which did not, and why. Evidence = the two
identical files plus your hashes.

## 6. Required dataset and setup instructions

```powershell
# 🪟 Windows — PowerShell, repository root
cd examples\labs
python make_data.py             # ✅ wrote data/customers_clean.csv (600 rows)
cd lab-01
python train_nondeterministic.py --label run1
python train_nondeterministic.py --label run2
```

🐧 Linux/macOS: `cd examples/labs && python make_data.py && cd lab-01`
then the same two commands.

## 7. Starter files

| File | Role |
|---|---|
| `train_nondeterministic.py` | the faulty script — three commented suspicious spots |
| `metrics_run1.json` / `metrics_run2.json` | your evidence (generated) |
| `../make_data.py` | deterministic data (the control in your experiment) |

## 8. Numbered implementation steps

**Step 1 — Capture the fault.** Run the script twice with different
labels; note both metric sets.
✅ **Checkpoint:** the two JSON files differ in at least `roc_auc`.
Real observed pair: `0.7994` vs `0.8126`.

**Step 2 — Eliminate the data.** `cd .. && python make_data.py --check`
→ ✅ `byte-identical across runs: YES`. Conclusion written: variation
comes from code, not inputs.

**Step 3 — Bisect the three suspects.** Change **one** suspect at a time
in your copy (seeding a split, pinning the sample, fixing the model's
randomness), re-run twice, compare hashes. Record a small table:
suspect → changed? → outputs still differ?
✅ **Checkpoint:** your table identifies the suspects that *matter* (two
of them) and the one that does nothing at all — explain the decoy in one
sentence.

**Step 4 — Fix, then prove.** Apply all fixes; run twice with labels
`a` and `b`; compare:
```powershell
fc /b metrics_a.json metrics_b.json     # 🪟 Windows: no output = identical
# 🐧 cmp metrics_a.json metrics_b.json && echo IDENTICAL
sha256sum metrics_a.json metrics_b.json # optional, both hashes shown equal
```
✅ **Checkpoint:** identical files; your diagnosis paragraph names each
suspect and its actual effect.

**Step 5 — Generalise.** Write the three-line determinism checklist you
will apply to every future training script (seed? sampling? time/ID
sources?).

## 9. Commands and expected results

| Command | Expected result |
|---|---|
| `python train_nondeterministic.py --label run1` then `--label run2` | two JSON files that **differ** (fault reproduced) |
| `python ../make_data.py --check` | `byte-identical across runs: YES` |
| your fixed script, twice | `fc /b` silent / `cmp` exit 0 — **identical** |
| `python -m py_compile train_nondeterministic.py` | exit 0 after your edits |

## 10. Acceptance criteria (objective)

- [ ] Fault reproduced once, captured as two differing files.
- [ ] Data eliminated as a cause with `--check` output pasted.
- [ ] Suspect table: every one of the three spots tested in isolation.
- [ ] Final pair of runs byte-identical (comparison command output shown).
- [ ] Diagnosis paragraph: real causes vs decoy, in your own words.

## 11. Troubleshooting and recovery

| Symptom | Cause | Fix |
|---|---|---|
| Outputs still differ after seeding the split | other sources remain (sampling, model randomness, time) | continue Step 3 — one suspect at a time |
| Outputs identical but test *fails* later | you compared only one file | hash **every** output (`metrics`, logs, artefacts) |
| `metrics_*.json` missing | ran without `--label`, overwrote the same file | use distinct labels for the two runs |
| Data check says DIFFERS | someone edited `make_data.py` | restore it; the generator is the control |

Recovery: the fixture ships broken — if you get stuck, `git checkout` is
**not yours to use** here; re-read §7 of the lab or restart your copy from
the shipped version.

## 12. Reflection questions

1. Which single fix would have hidden the bug least effectively if you
   had only applied it alone — and why?
2. Your model will run in CI on a *different machine*. Which of your fixes
   does that depend on (seeds? versions? file order?)?
3. Is byte-identical output always the goal? Give one legitimate case
   where it is not, and what you would require instead.

## 13. Optional challenge tasks

1. Add a `--seed` CLI flag and prove three different seeds produce
   *different* results while one seed reproduces exactly.
2. Introduce a fourth nondeterminism source yourself (e.g. unsorted
   `glob`) and write the test that would catch it.
3. Time-box: write the determinism contract as a pytest test another
   teammate could run.

## 14. Rubric / checklist

| Points | Criterion |
|---|---|
| 2 | Fault reproduced with evidence (two differing outputs pasted) |
| 2 | Data source eliminated via `--check` |
| 4 | All three suspects isolated and correctly classified (incl. the decoy) |
| 4 | Final outputs byte-identical, command output shown |
| 3 | Diagnosis written clearly, generalising to a future checklist |
| **15** | **total** · ≥11 = pass · ≥8 = revisit §8 |

## 15. Cleanup

```powershell
cd examples\labs\lab-01
Remove-Item metrics_*.json     # 🧹 rm -f metrics_*.json
```
Keep your diagnosis note — it is portfolio evidence.

---

**After attempting:** a reference fix lives in
[`examples/labs/solutions/lab-01/`](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/labs/solutions/lab-01)
— compare only once you have your own answer.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../about/index.md).*