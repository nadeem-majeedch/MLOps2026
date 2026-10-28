# Learning objectives — Module 04

## Objectives

| ID | By the end of this module you can… | Prove it by… |
|---|---|---|
| **LO 4.1** | Write automated schema and statistical checks for a tabular dataset | A validator that reports 7/7 on good data and fails on each seeded defect |
| **LO 4.2** | Detect and report common data problems: missing values, type drift, out-of-range values, duplicate keys, train/serving skew | Three corrupt extracts, each caught by at least one named check |
| **LO 4.3** | Version a dataset so an experiment can be re-run on byte-identical inputs | A `.dvc` pointer whose recorded MD5 equals your file's hash, and a restore that verifies |
| **LO 4.4** | Document a dataset's source, licence, and known limitations | A dataset card covering source, licence, size, schema, and caveats |

## What "good" looks like

- **Pass:** your validator is *trusted* — you can hand it an unknown extract and
  believe its verdict; and you can restore a specific version of the data from
  the pointer alone, proving the bytes match.
- **Not yet:** validation only checks columns exist, or the versioned file's
  recorded hash does not match reality. Both mean the gate can be bypassed.

## Vocabulary you must be able to use after this module

**data validation**, **schema**, **data quality rule**, **uniqueness constraint**,
**value range**, **missingness**, **data drift vs. schema violation**,
**data contract**, **dataset card**, **data lineage**, **immutability**,
**content hash**, **data versioning**, **pointer file**, **train/serve skew**,
**DVC**, **baseline snapshot**.

## How this module is assessed

- **Practical lab** (graded): three extracts validated + dataset versioned and
  restored — [lab.md](lab.md) §9.
- **Knowledge check:** 10 questions — [knowledge-check.md](knowledge-check.md).

!!! note "Why DVC comes last in this module"
    Data versioning is a *principle* (freeze the bytes, record the hash) that
    predates any tool. DVC is one implementation, and it assumes you already
    think in terms of Git repositories and clean status output — which is Module
    02's contribution. Learn the principle in concepts §4 before the commands in
    lab §7.

---

[← Module overview](index.md) · [Concepts →](concepts.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*