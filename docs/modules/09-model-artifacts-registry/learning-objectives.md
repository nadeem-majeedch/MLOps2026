# Learning objectives — Module 09

Maps to syllabus outcomes
[LO 9.1–9.4](../../syllabus/detailed-syllabus.md#module-09-model-artifacts-registries-promotion-and-lifecycle-management).

| # | You can… | You prove it by… |
|---|---|---|
| **9.1** | Package a model with everything needed to use it (weights, preprocessing, metadata, signature) | A registered version folder containing the fitted pipeline (preprocessing included), `metadata.json`, and a feature list a caller can check |
| **9.2** | Register a model and record its lineage: data version, code config, parameters, metrics | `metadata.json` showing the data's sha256, metrics from the run, and the gate result — all copied at registration time |
| **9.3** | Promote a model through staging to production using an explicit, reversible transition | The `history` output: register → stage → production, plus a `rollback` entry restoring the previous version |
| **9.4** | Write a model card covering intended use, limitations, and evaluation | A one-page card for your production version (template in the lab), reviewed against the challenge's criteria |

## Supporting skills

- Explain why production promotion is **refused** for a version whose gate
  never passed, and what `--force`-style bypasses cost a team.
- State the difference between this module's **local file registry** and a
  **remote registry service** (MLflow Model Registry: server, UI, webhooks,
  aliases) — and which features each provides.
- Describe what "immutable version" means operationally: corrections create a
  new version, never an edit.

## Self-check questions

1. What four things are copied into `registry_store/vNNN/` at registration?
2. Which exact command returns production to the previous model, and what
   record makes it possible?
3. Why does the registry refuse `development → production` directly?

*(Answers in [knowledge-check.md](knowledge-check.md) — attempt first.)*

---

[← Module 09 index](index.md) · [Next: concepts →](concepts.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*