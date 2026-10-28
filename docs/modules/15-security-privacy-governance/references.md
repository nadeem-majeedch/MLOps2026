# References — Module 15

Official and primary sources first; everything listed is free to read.
Marked ⭐ = start here. External links were chosen for permanence (standards
bodies, project docs, seminal papers) — if one moves, search its title.

## Security practice

- ⭐ **OWASP Top 10** (web risks) and **OWASP ML Security Top 10** — the
  shared vocabulary for threat categories.
  <https://owasp.org/www-project-top-10/> · <https://owasp.org/www-project-machine-learning-security-top-10/>
- ⭐ **OWASP Cheat Sheet Series** — authentication, secrets management,
  logging, deserialization.
  <https://cheatsheetseries.owasp.org/>
- **NIST SP 800-53 / SP 800-207 (Zero Trust)** — control catalogues that
  professional audits draw from; read the overviews, not the whole text.
  <https://csrc.nist.gov/publications/sp800-53>
- **SLSA framework** — supply-chain integrity, from source to build.
  <https://slsa.dev/>

## Secrets and supply chain

- ⭐ **gitleaks** — free, open-source secret scanning for git history.
  <https://github.com/gitleaks/gitleaks>
- **GitHub secret scanning / push protection** — what a hosted platform
  adds (the CI enforcement point referenced in Module 12).
  <https://docs.github.com/en/code-security/secret-scanning>
- **Python packaging guidance (PyPA)** — pinned, hash-checked installs.
  <https://packaging.python.org/en/latest/guides/recommended-packages/>

## Deserialization safety

- ⭐ **Python docs — `pickle`**: "never unpickle data received from an
  untrusted source" — read the module docstring's warning verbatim.
  <https://docs.python.org/3/library/pickle.html>
- **skops** — a safer scikit-learn persistence format with allowlists.
  <https://github.com/skops-dev/skops>
- **ONNX** — exchange format that avoids arbitrary code execution for
  supported models. <https://onnx.ai/>

## Privacy

- ⭐ **ICO Guide to the UK GDPR** (plain-language, jurisdiction-neutral
  useful principles: lawfulness, minimisation, storage limitation).
  <https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/>
- **CNIL privacy engineering records** — practical data-minimisation
  patterns. <https://www.cnil.fr/en/privacy-engineering>
- Reminder: the course gives **informational context, not legal advice**.

## Fairness and responsible ML

- ⭐ **fairlearn** documentation — metrics and assessments, with a candid
  "when model metrics are not enough" section.
  <https://fairlearn.org/>
- ⭐ **Barocas, Hardt, Narayanan — *Fairness and Machine Learning*
  (free textbook)** <https://fairmlbook.org/>
- **Mitchell et al. — "Model Cards for Model Reporting"** (2019) — the
  origin of the artefact used in the lab. <https://arxiv.org/abs/1810.03993>
- **Gebru et al. — "Datasheets for Datasets"** (2021) — the datasheet
  concept. <https://arxiv.org/abs/1803.09010>
- **Sculley et al. — "Hidden Technical Debt in Machine Learning Systems"**
  — the governance case for lineage and registries (revisited from
  Module 03). <https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems>

## Incident response

- ⭐ **NIST SP 800-61 — Computer Security Incident Handling Guide**
  (detect → contain → eradicate → recover, the backbone of concepts §7).
  <https://csrc.nist.gov/publications/sp800-61>
- **Google SRE — incident management chapter** — postmortem culture,
  blameless reviews. <https://sre.google/sre-book/managing-incidents/>

## Tool documentation (Tool-specific vs Principle)

- Python `logging` (general principle: field allowlists) →
  <https://docs.python.org/3/library/logging.html>
- FastAPI security dependencies / headers (Tool) →
  <https://fastapi.tiangolo.com/tutorial/security/>

---

**Tool vs Principle:** scanners, key headers, and hash sidecars are
*tools* — swap them freely. Least privilege, minimisation, provenance, and
rehearsed response are *principles* — they travel with you.

---

[← Troubleshooting](troubleshooting.md) · [Module index](index.md) · [Module 16 →](../16-cloud-kubernetes-scaling/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*