# References — Module 04

## Official documentation

| Resource | What it is for |
|---|---|
| [pandas user guide](https://pandas.pydata.org/docs/user_guide/index.html) | Reading, checking, and transforming tabular data |
| [pandas API: missing data](https://pandas.pydata.org/docs/user_guide/missing_data.html) | `isna`, `fillna`, and why `n/a` becomes `NaN` |
| [pandera](https://unionai.github.io/pandera/) | Typed, code-first dataframe schemas — the natural next step after plain pandas checks |
| [Great Expectations](https://docs.greatexpectations.io/) | Richer expectation suites and data docs — heavier setup, worth knowing when suites grow |
| [DVC documentation](https://dvc.org/doc) | Data and pipeline versioning (the tool used in the lab) |
| [DVC: data versioning basics](https://dvc.org/doc/user-guide/data-management/data-versioning) | Exactly the concepts the lab practises |
| [Git](https://git-scm.com/doc) | The model DVC deliberately imitates |
| [CSV / RFC 4180](https://www.rfc-editor.org/rfc/rfc4180) | Why `1,234.50` in a CSV is a design problem, not a typo |

## Reading that frames the module

| Resource | Why |
|---|---|
| [Data Cascades in High-Stakes AI](https://dl.acm.org/doi/10.1145/3449288) — Sambasivan et al., 2021 | Empirical study of how undetected data problems sink ML projects — the "why validation is not bureaucracy" paper |
| [Datasheets for Datasets](https://arxiv.org/abs/1803.09010) — Gebru et al. | The origin of the dataset card this module asks you to write |
| [Data testing rules](https://martinfowler.com/articles/data-quality-testing.html) — articles on data-quality testing | Practical framing of tiers of data checks |

## Course material

- [glossary](../../glossary/index.md) — add your definitions for schema, contract, lineage
- [Module 02 lab](../02-python-git-cli-environments/lab.md) — Git habits DVC builds on
- [Module 03 concepts](../03-ml-project-technical-debt/concepts.md) — data-dependency debt, which this module repays
- [resources](../../resources/index.md) — curated wider reading

## General principle vs. tool choice

| General principle | Course choice | Alternatives |
|---|---|---|
| Declare what data must satisfy | plain pandas checks in `src/validate.py` | pandera, Great Expectations, Soda, TFDV |
| Fail loudly at the boundary | exit code 1 on any failed check | raise exceptions, CI gate (M12) |
| Data changes must be visible | content hashes + `.dvc` pointer files | `sha256sum` in a file, git-lfs, lakeFS, Quilt |
| Data must be documented | dataset card in the repo | datasheets, data cards partnership formats |
| Same bytes for the same experiment | regenerate or restore from a version | snapshots in a warehouse, object-store versioning (☁️) |

!!! note "Version-specific behaviour observed in this course"
    Verified with **DVC 3.67.1** and **pandas 3.0.x**: `n/a` strings parse as
    `NaN` by default; `dvc checkout` **refuses** to overwrite a locally modified
    file unless you pass `--force`. Newer versions may word these differently —
    the official docs above are the authority.

---

[← Troubleshooting](troubleshooting.md) · [Module overview](index.md) · [Next: Module 05 →](../05-reproducible-training-pipelines/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*