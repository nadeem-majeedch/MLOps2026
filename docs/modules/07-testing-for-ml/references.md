# References — Module 07

Official documentation for the tools used in this module, plus foundational
reading. URLs verified at the time of writing; external links open in a new tab.

## Core tool documentation

| Resource | Use it for |
|---|---|
| [pytest documentation](https://docs.pytest.org/) | Test discovery, fixtures, markers, CLI flags — the reference for every error message you will meet |
| [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html) | Sharing setup cleanly (`conftest.py`, scopes) |
| [pytest coverage integration](https://docs.pytest.org/en/stable/how-to/cov.html) | `--cov`, reports, and what coverage does *not* tell you |
| [Coverage.py](https://coverage.readthedocs.io/) | The underlying measurement tool and its semantics |
| [scikit-learn testing utilities](https://scikit-learn.org/stable/modules/model_evaluation.html) | Metric definitions used by the performance floor (ROC-AUC, precision/recall) |
| [Hypothesis](https://hypothesis.readthedocs.io/) *(optional)* | Property-based testing — generating inputs instead of listing them |

## Foundational papers (general principles, not tool-specific)

- **Sculley et al. (2015), *Hidden Technical Debt in Machine Learning Systems*, NeurIPS.**
  The glue-code and pipeline-entanglement arguments that motivate testing ML
  pipelines (Module 03's core text).
- **DeVito et al. (2017), *Nips 2017 Software Engineering Challenges of ML***
  (Microsoft Research) — real production constraints around testing and
  reproducibility.
- **Breck et al. (2017), *The ML Test Score* (Google),** MLSys — the
  layer-to-production-test mapping our five layers derive from; also the origin
  of the idea that tests gate *deployment*, not just merge.

## Distinguishing tool-specific from general

| Claim | Kind |
|---|---|
| "Tests should be isolated and deterministic" | **General principle** — applies in any language/framework |
| "A suite that has never failed cannot be trusted" | **General principle** |
| "Coverage counts executed lines" | **Tool semantics** (coverage.py) — other tools count branches differently |
| "`pytest` finds `test_*.py` by default" | **Tool-specific** — config can change it |
| "`python -m pytest` guarantees interpreter consistency" | **Python-specific** behaviour, worth knowing on Windows |

When a pytest upgrade changes your workflow, the pytest changelog is the
authority — treat course text as a snapshot.

## Related course material

- Module 05 — the pipeline these tests protect.
- Module 06 — run metadata as test evidence.
- Module 12 — making this suite a required CI gate.
- [../glossary/index.md](../../glossary/index.md) — terms: test pyramid, oracle,
  flaky test, mutation testing, coverage.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*