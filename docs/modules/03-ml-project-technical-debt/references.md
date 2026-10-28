# References — Module 03

## Primary sources (the debt literature)

| Resource | Why it matters here |
|---|---|
| [Hidden Technical Debt in Machine Learning Systems](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/43146.pdf) — Sculley et al., 2015 | The canonical taxonomy: data dependencies, entanglement, feedback loops, undeclared consumers. The vocabulary of this module comes from here. |
| [Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml) — Google | Sequenced advice on when to build infrastructure versus when to keep it simple |
| [Software Engineering for Machine Learning: A Case Study](https://arxiv.org/abs/1909.03136) (Amershi et al., Microsoft) | What ML practitioners actually do differently from classic software teams — empirical, not vendor |
| [Model Cards for Model Reporting](https://arxiv.org/pdf/1810.03993) — Mitchell et al. | Documentation as a first-class artefact (used again in Modules 09 and 15) |

## Official documentation for the tools in this module

| Tool | Documentation |
|---|---|
| Jupyter notebooks | [jupyter.org](https://jupyter.org/) · [nbformat spec](https://nbformat.readthedocs.io/) |
| jupytext (paired `.py`/`.ipynb`) | [jupytext.readthedocs.io](https://jupytext.readthedocs.io/) |
| nbstripout (clean notebook diffs) | [github.com/kynan/nbstripout](https://github.com/kynan/nbstripout) |
| cookiecutter templates | [cookiecutter.readthedocs.io](https://cookiecutter.readthedocs.io/) |
| scikit-learn (used by the example) | [scikit-learn.org/stable](https://scikit-learn.org/stable/) |
| PyYAML (configuration) | [yaml.org](https://yaml.org/) · [pyyaml docs](https://pyyaml.org/wiki/PyYAMLDocumentation) |

## Course material

- [glossary](../../glossary/index.md) — add your own definitions for the debt terms
- [course project map](../../syllabus/course-project-map.md) — where MP1 fits
- [resources](../../resources/index.md) — the curated wider reading list

## General principle vs. tool choice

| General principle | Course choice | Alternatives |
|---|---|---|
| One entry point that runs the whole job | `run.py` | `python -m src.train`, a Makefile target (M08) |
| Configuration outside code | `config.yaml` | environment variables, Hydra, argparse |
| Notebooks are for exploration, not production | kept in `legacy/`, logic moved to `src/` | jupytext pairing, papermill runs |
| Notebooks must diff cleanly | outputs stripped before commit | nbstripout, jupytext |
| Layout conventions come from the community | the course layout in lab §6 | cookiecutter-data-science, ZenML project template |

---

[← Troubleshooting](troubleshooting.md) · [Module overview](index.md) · [Next: Module 04 →](../04-data-quality-validation-versioning/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*