# References — Module 14

## Tool documentation

| Resource | Use it for |
|---|---|
| [scipy `ks_2samp`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ks_2samp.html) | The two-sample KS test used in `drift.py` |
| [scipy `chi2_contingency`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2_contingency.html) | The categorical-mix test |
| [Evidently docs](https://evidentlyai.com/docs) | An open-source drift/performance report library — the "real tool" version of what you hand-built |
| [Whylogs / whylogs docs](https://whylogs.readthedocs.io/) | Lightweight statistical logging (profiles instead of raw rows — a privacy-conscious alternative to full prediction logs) |
| [alibi-detect docs](https://adrift.readthedocs.io/) | Detection algorithms incl. online drift detectors (advanced reading) |
| [MLflow metrics logging](https://mlflow.org/docs/latest/tracking.html) | Where training metrics live (Module 06) vs serving metrics (this module) |

## Foundational papers

- **Evidently AI (2022), *Data Drift and Concept Drift* / related guides** —
  clear practical taxonomy of drift types (good bridge text).
- **Šliwa & Wójcik (2021), *Detecting data drift in production*** (or
  Gama et al., *A survey on concept drift adaptation*, ACM Computing Surveys,
  2014) — the academic treatment of drift detection and adaptation.
- **Baier & Kamps (2021), *Towards Trustworthy ML*** — decision framing for
  automated retraining.
- **Google SRE book, ch. 4 (*Alerting on Symptoms*)** — alerts must target
  symptoms users feel, with owners and actions: concepts §5's source.
- **Hand (2009), *Measuring classifier performance: a coherent alternative to
  the area under the ROC curve*** — why single AUC numbers on small windows
  need care (supports LO 14.3's noise argument).

## Distinguishing tool-specific from general

| Claim | Kind |
|---|---|
| "Drift is not proof of degradation; labels decide" | **General principle** |
| "Report effect size with p-values; thresholds need justification" | **General principle** |
| "Human approves retraining; rollback planned first" | **General principle** (course policy) |
| "PSI > 0.20 = strong" | **Convention** — common in practice, not a law; document your own |
| `drift.py`, `performance.py`, `decision.py` CLI | **Course-specific implementation** |
| "Evidently's default tabs/thresholds" | **Tool-specific** — check current docs |

## Related course material

- Module 04 — data contracts (measurement-change checks).
- Module 06/08 — reference metrics and gates reused as thresholds.
- Module 09 — the rollback in the human checklist.
- Module 13 — scheduling the whole monitoring chain.
- Module 15 — privacy of what you log; fairness of what you decide.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*