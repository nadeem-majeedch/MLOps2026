# References — Module 12

## Tool documentation

| Resource | Use it for |
|---|---|
| [GitHub Actions documentation](https://docs.github.com/en/actions) | The primary reference: workflows, jobs, runners, expressions |
| [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) | `on`, `jobs.<job>.steps`, `needs:`, `permissions`, `concurrency` |
| [Contexts / expressions](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts) | `${{ github.* }}`, `${{ secrets.* }}` |
| [Managing secrets](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions) | Where secrets live, how they're masked, how they reach `env:` |
| [Security hardening for GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions) | Least privilege, pinning actions, secret hygiene |
| [actions/setup-python](https://github.com/actions/setup-python) | Interpreter provisioning + pip caching (our `cache-dependency-path`) |
| [actions/upload-artifact](https://github.com/actions/upload-artifact) | Shipping the coverage report from a run |
| [ruff](https://docs.astral.sh/ruff/) | The linter our `lint` job runs |

## General reading

- **Hilton et al. (2016), *Continuous Integration in Open Source Software*,
  PROMISE** — empirical view of CI practices.
- **Google SRE book, ch. 12 (*Safe Releases*)** — progressive rollout and the
  role of automated checks before any delivery step.
- **Sculley et al. (2015)** — why ML pipelines need the same discipline plus
  data tests (the argument for the `ml-validate` job).

## Distinguishing tool-specific from general

| Claim | Kind |
|---|---|
| "Every change must be checked before merge" | **General principle** |
| "CI should stay fast and deterministic or it gets ignored" | **General principle** |
| "Secrets never in source, logs, or disk" | **General principle** |
| "`on: push: branches: [main]`", `runs-on: ubuntu-latest` | **GitHub Actions syntax** |
| "Free Actions minutes for public repos" | **Vendor policy** — verify current terms |
| "`permissions: contents: read`" | **Platform-specific** mechanism of the general least-privilege idea |

## Related course material

- Module 07 — the suite CI runs.
- Module 08/09 — the gates `ml_validate` re-enforces.
- Module 11 — what an image-build job would package (lab extension 3).
- Module 13 — where heavy/nightly validation belongs.
- [Tool selection guide](../../syllabus/tool-selection-guide.md) — CI options
  beyond GitHub Actions.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*