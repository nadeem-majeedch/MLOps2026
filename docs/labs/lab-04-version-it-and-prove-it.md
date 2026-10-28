# LAB-04 — Version It and Prove It

## 1. Lab identity

| | |
|---|---|
| **Lab ID** | **LAB-04** |
| **Difficulty / topic** | 🌱 Beginner · Data versioning & reproducibility |
| **Prerequisite module** | [04 — Data quality, validation, and versioning](../modules/04-data-quality-validation-versioning/index.md) |
| **Fixtures** | `examples/labs/make_data.py` (+ shared datasets); DVC concepts from Module 04 |
| **Estimated time** | 90 minutes · free, local, offline |

## 2. Scenario and background

Three people on the team claim their model numbers are "from the same
dataset". Nobody can prove it: the CSV was emailed around, re-saved
twice, and the good experiment's notebook lost its input path. Your job:
give every dataset a **version identity** and use it to reproduce an
earlier experiment exactly — using nothing but the repository, hashes,
and a small ledger. (Module 04 taught DVC as the industry tool; this lab
makes you feel *why* it exists before you ever install it.)

## 3. Learning objectives

By the end you can:

1. Give a dataset an immutable identity: content hash + provenance
   (generator, seed, schema) in a version ledger.
2. Reproduce a recorded experiment by re-creating **its** inputs, and
   verify with hashes, not memory.
3. Explain what DVC (or any data version tool) adds over hashes+git, and
   when that is worth it.
4. Detect silent input drift between two runs of "the same" experiment.

## 4. Prerequisites and estimated time

- Module 04 read; git basics from Module 02 (used as plain storage).
- `python examples/labs/make_data.py` run once.
- **90 min** (ledger 30 · reproduce 35 · drift test 15 · write-up 10).

## 5. Student task statement

Build `dataset_ledger.json` + a `version_data.py` tool (hash → register →
verify → `--reproduce`), register both shared datasets, then execute a
recorded experiment twice: once against the *recorded* dataset version
and once against a tampered copy — and show the reproduction check
**refusing** the tampered one.

## 6. Required dataset and setup instructions

```powershell
# 🪟 Windows — PowerShell
cd examples\labs
python make_data.py --check           # ✅ byte-identical: YES (control)
python -c "import hashlib,pathlib; \
print(hashlib.sha256(pathlib.Path('data/customers_clean.csv').read_bytes()).hexdigest()[:16])"
# ✅ 72faff5e995ab657
```
🐧: same commands with `&&` and no line-continuation backtick (drop the `\`).

## 7. Starter files

| File | Role |
|---|---|
| `make_data.py` | deterministic generator = the *provenance* record |
| shared `data/*.csv` | the datasets you version |
| `version_data.py` | **you write it** — spec in §8; reference in solutions |

Ledger entry shape (minimum fields):
`{"name", "sha256", "rows", "generator": "make_data.py", "seed": 20261026,
"schema": [...], "registered_at"}`.

## 8. Numbered implementation steps

**Step 1 — Register.** `python version_data.py register data/customers_clean.csv`
writes an entry with the full sha256 (not a prefix).
✅ Checkpoint: `python version_data.py list` shows the entry.

**Step 2 — Verify.** `python version_data.py verify data/customers_clean.csv`
→ `OK — matches ledger`. ✅ exit 0.

**Step 3 — Tamper.** Copy the file, change **one** byte, `verify` the
copy → ✅ `MISMATCH` with both hashes printed, exit 1.

**Step 4 — Reproduce an experiment.** Write `experiment.py` that trains
(in a few lines, logistic regression on the clean data) and records
`{"data_sha256": <full hash>, "seed": 2026, "roc_auc": …}` into
`run_record.json`. Run it; then delete/rename the CSV, restore it from
`make_data.py`, and re-run.
✅ Checkpoint: `data_sha256` identical across both runs; AUC identical.

**Step 5 — The refusal.** Run `experiment.py --against <tampered copy>`.
It must check the ledger and **refuse** (`exit 1`) before training.
✅ Checkpoint: refusal message names the mismatch.

**Step 6 — Tooling note.** One paragraph: what DVC (or git-lfs, or a
lakehouse table version) would do here that your ledger does not — and
whether you need it yet.

## 9. Commands and expected results

| Command | Expected |
|---|---|
| `python make_data.py --check` | `byte-identical across runs: YES` |
| `python version_data.py register …` then `list` | entry with full sha256 + seed |
| `python version_data.py verify …` (pristine) | `OK — matches ledger`, exit 0 |
| `python version_data.py verify …` (tampered) | `MISMATCH`, both hashes, exit 1 |
| `python experiment.py` twice | identical `data_sha256` and identical AUC |
| `python experiment.py --against tampered.csv` | refuses before training, exit 1 |

## 10. Acceptance criteria (objective)

- [ ] Ledger file exists with **full** sha256, rows, generator, seed, schema.
- [ ] `verify` passes pristine / fails tampered, both outputs pasted.
- [ ] Experiment records its data hash; two runs agree.
- [ ] Experiment refuses a non-ledgered input (exit code shown).
- [ ] Tooling paragraph: hashes+ledger vs DVC — honest, specific.

## 11. Troubleshooting and recovery

| Symptom | Cause | Fix |
|---|---|---|
| verify always MISMATCH after `make_data.py` | you hashed a different path or the file moved | hash the exact path you verify; regenerate only via the generator |
| reproduction AUC differs | experiment not seeded, or env changed | pin `random_state`; note package versions in the record |
| ledger empty after restart | ledger written to cwd, not script dir | write relative to the script (`pathlib.Path(__file__).parent`) |
| Windows line-endings change hashes | file edited/saved by another tool | regenerate via `make_data.py`; never hand-edit data |

## 12. Reflection questions

1. Your ledger protects against *accidental* change. What attack or
   mistake does it **not** stop, and what would?
2. Is a dataset hash a "version"? What's missing (labels? access rights?
   PII review?) before it deserves a version number?
3. Where should the ledger live — same repo as the code, or separate?
   Give the trade-off in two sentences.

## 13. Optional challenge tasks

1. Add `diff <name> --against <file>` showing which columns/rows changed.
2. Register `customers_dirty.csv` and `customers_shifted.csv`; document
   why three versions exist of "the same" table.
3. Install DVC (free, local) and reproduce your ledger with
   `dvc add` + `dvc diff` — then compare both in your tooling paragraph.

## 14. Rubric / checklist

| Points | Criterion |
|---|---|
| 4 | ledger complete (full hash, provenance fields, schema) |
| 4 | verify OK/MISMATCH demonstrated with exit codes |
| 4 | experiment reproduces and refuses tampered input |
| 3 | tooling paragraph (ledger vs DVC) specific and honest |
| **15** | **total** · ≥11 = pass |

## 15. Cleanup

```powershell
cd examples\labs
Remove-Item tampered*.csv, run_record.json -ErrorAction SilentlyContinue
```
Regenerate data any time: `python make_data.py`.

---

**After attempting:** a reference `version_data.py` lives in
[`examples/labs/solutions/lab-04/`](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/labs/solutions/lab-04).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../about/index.md).*