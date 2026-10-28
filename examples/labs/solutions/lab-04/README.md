# LAB-04 — reference solution

> Attempt the lab first. This is the answer key, not the assignment.

## Reference design: `version_data.py`

The lab asks for four verbs over a hash-keyed ledger
(`dataset_ledger.json`):

```text
python version_data.py register data/customers_clean.csv --name customers
    -> sha256(file) recorded with name, size, row count, ISO timestamp
python version_data.py list
    -> one line per registered version, newest last
python version_data.py verify data/customers_clean.csv --name customers
    -> OK if the bytes hash to the recorded value, refusal naming the
       mismatch otherwise (exit 1)
python version_data.py --reproduce <run_id>
    -> re-check the data_sha256 that run recorded, before you trust its metrics
```

Ledger entry shape (keep it flat — a ledger you cannot grep is a ledger
you cannot audit):

```json
{
  "customers": {
    "sha256": "…64 hex…",
    "bytes": 123456,
    "rows": 600,
    "registered_at": "2026-10-27T00:00:00+00:00"
  }
}
```

**Do not store the data itself** — the hash is the reference; the file
is the content. (DVC, taught after this exercise, does the same idea
with a real content-addressed store.)

## The three checkpoints — what "passing" looks like

1. `python version_data.py list` → the entry appears with the hash you
   can independently reproduce:
   `python -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('data/customers_clean.csv').read_bytes()).hexdigest())"`
2. **Reproduce twice:** run the recorded experiment twice; both runs log
   the same `data_sha256` **and** the same ROC AUC. Identity of the hash
   proves same input; identity of AUC proves same computation.
3. **Tamper test:** copy the CSV, change one byte (or drop a row), point
   `--reproduce` at the copy → the check **refuses** with a message that
   names the recorded vs computed hash. The refusal is the deliverable:
   a version system that silently accepts drift is decoration.

## Reasoning checkpoints (model answers)

- **Why hash, not timestamp/filename?** Names are rewritten and mtimes
  change on copy; content addressing answers exactly one question — *are
  these the bytes the experiment saw?*
- **What does versioning NOT give you?** It gives provenance, not
  meaning: two versions can be identical in schema and different in
  population. Versioning tells you *what changed*; validation (LAB-03)
  tells you whether it matters.
- **Git vs data:** Git stores text well and bloats on binary data —
  that is why data versioning is a separate tool, not laziness.

## Common wrong answers

- Storing the CSV path as the "version" — a path is not an identity.
- Hashing a pandas DataFrame object instead of the file bytes (repr can
  vary; hash the bytes on disk).
- Accepting a tampered file with a warning — the lab scores the
  **refusal**.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../../docs/about/index.md).*