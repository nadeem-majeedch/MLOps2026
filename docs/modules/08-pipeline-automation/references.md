# References — Module 08

Official documentation for the tools and ideas in this module. External links
were valid at the time of writing.

## Tool documentation

| Resource | Use it for |
|---|---|
| [GNU Make manual](https://www.gnu.org/software/make/manual/) | The classic build-automation model: targets, dependencies, recipes — the same DAG idea, older than any of us |
| [Snakemake documentation](https://snakemake.readthedocs.io/) | DAG-driven pipelines where rules declare input/output files (bioinformatics origin, widely used) |
| [Nextflow documentation](https://www.nextflow.io/docs/latest/) | Dataflow pipelines designed for reproducibility across containers/HPC |
| [DVC documentation](https://dvc.org/doc) | Data/pipeline versioning — `dvc repro` runs a stage DAG with data-aware caching (Module 04 used `dvc add`) |
| [Python `inspect.getsource`](https://docs.python.org/3/library/inspect.html) | How the runner hashes a stage's own code |
| [hashlib](https://docs.python.org/3/library/hashlib.html) | The sha256 hashing used for signatures |

## Foundational reading (general principles)

- **Kang et al. (2022), *Towards CRISP-ML(Q)*, DAMI** — process models for
  ML systems; the "pipeline as declared, verifiable process" framing.
- **Sculley et al. (2015), *Hidden Technical Debt in Machine Learning Systems*,**
  NeurIPS — why undeclared data dependencies and glue code rot (Module 03's
  anchor text; re-read the pipeline-entanglement section here).
- **Amershi et al. (2019), *Software Engineering for Machine Learning: A Case Study*,
  Microsoft/ICSE-SEIP** — stage structure observed in industrial ML workflows.

## Distinguishing tool-specific from general

| Claim | Kind |
|---|---|
| "Order follows declared dependencies; cycles are illegal" | **General principle** (graph theory — true in Make, Snakemake, Airflow, CI) |
| "Skip when inputs/outputs are unchanged" | **General principle**, implementation varies (Make uses mtimes, this runner uses content hashes — hashes are stricter) |
| "Exit code non-zero stops the workflow" | **Convention**, near-universal but not a law |
| "`python -m pipe.run --clean`" | **Specific to this course's runner** |
| "Make compares timestamps" | **Tool semantics** — a stale timestamp can fool Make; content hashes cannot |

## Related course material

- Module 03 — the structure this pipeline automates.
- Module 07 — the tests that protect each stage.
- Module 09 — what happens to the artefacts after `report`.
- Module 13 — scheduling, retries, and alerts around the same stages.
- [Tool selection guide](../../syllabus/tool-selection-guide.md) — why not
  Airflow yet.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*