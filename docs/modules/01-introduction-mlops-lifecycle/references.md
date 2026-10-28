# References — Module 01

Official documentation and primary sources. Where a link is to a vendor's site,
it is because the tool is genuinely the standard — alternatives are named so you
are not locked into one vendor's framing.

## Concepts and primary sources

| Resource | Why read it | Type |
|---|---|---|
| [Hidden Technical Debt in Machine Learning Systems](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/43146.pdf) — Sculley et al., 2015 | The paper that named the problem; the source of "ML technical debt" as used in Module 03 | Research paper, free |
| [Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml) — Google | Practical sequencing of ML engineering work; good companion to the lifecycle diagram | Engineering guide, free |
| [Machine Learning Production Best Practices](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning) — Google Cloud architecture | A second, independent lifecycle framing to compare ours against | Vendor guide, free (☁️ product mentions) |
| [Full Stack Deep Learning — lectures](https://fullstackdeeplearning.com/) | Broader view of what surrounds a model in production | Free course |

**How to read vendor material:** the *stages* are general; the *product names*
are not. When a cloud vendor says "model monitoring", map it to our stage 8 and
move on — Module 14 teaches the concept with free tools first.

## Official tool documentation used in this module

| Tool | Documentation | Note |
|---|---|---|
| Python | [docs.python.org/3/](https://docs.python.org/3/) | Language reference + tutorial |
| pandas | [pandas.pydata.org/docs](https://pandas.pydata.org/docs/) | Used for the worked example |
| pip | [pip.pypa.io](https://pip.pypa.io/en/stable/) | Install behaviour, covered properly in Module 02 |

## Course materials to keep open

- [concepts.md](concepts.md) — the lifecycle diagram you are mapping onto
- [glossary](../../glossary/index.md) — add your own definitions as you go
- [resources](../../resources/index.md) — the curated wider reading list

## Distinguishing general principles from tool choices

| General principle (will not be obsolete) | This course's current choice (may change) |
|---|---|
| Data must be validated before use | plain pandas checks → pandera/Great Expectations (M04) |
| Datasets must be versioned for reproducibility | DVC (M04) |
| Experiments must be recorded | MLflow (M06) |
| Models must be evaluated against a baseline | scikit-learn metrics (M06) |
| Changes must be gated by automated tests | pytest + GitHub Actions (M07, M12) |
| Production quality must be monitored | Evidently + Prometheus (M14) |

When a tool changes version or vendor, the left column is what you carry with you.

---

[← Troubleshooting](troubleshooting.md) · [Module overview](index.md) · [Next: Module 02 →](../02-python-git-cli-environments/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*