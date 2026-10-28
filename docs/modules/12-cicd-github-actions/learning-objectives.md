# Learning objectives — Module 12

Maps to syllabus outcomes
[LO 12.1–12.4](../../syllabus/detailed-syllabus.md#module-12-cicd-and-ml-validation-workflows-using-github-actions).

| # | You can… | You prove it by… |
|---|---|---|
| **12.1** | Build a CI workflow that runs linting, tests, and data/model validation on every push and pull request | `.github/workflows/ci.yml` parsed and executed: three jobs, each command run locally with a passing exit code |
| **12.2** | Add an ML validation job that blocks a bad model from merging | A failing `ml_check.py` run against corrupt data (exit 1, named checks) plus the passing run after restore |
| **12.3** | Add a build/publish job for container images with sensible caching and versioning | Your written job sketch (Module 11's build command + tag strategy) — labelled as not-yet-executed until you run it |
| **12.4** | Diagnose a failing workflow from its logs and fix it | A red run you actually caused, with the failing step, the log line, and the fix — locally or on GitHub |

## Supporting skills

- Explain each workflow section: `on`, `concurrency`, `permissions`, `jobs`,
  `steps`, `uses:` vs `run:`.
- Say why jobs run **in parallel by default**, and when `needs:` is worth the
  serialisation.
- Describe what caching (`cache: pip`) does and does not make faster.
- State the three places a secret must never appear, and where it belongs instead.

## Self-check questions

1. What exact file and events trigger this workflow?
2. Which job would fail first if `src/features.py` gained an unused import?
3. What does `permissions: contents: read` prevent?
4. Why can `ml_check.py` run in CI without retraining anything?

*(Answers in [knowledge-check.md](knowledge-check.md) — attempt first.)*

---

[← Module 12 index](index.md) · [Next: concepts →](concepts.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*