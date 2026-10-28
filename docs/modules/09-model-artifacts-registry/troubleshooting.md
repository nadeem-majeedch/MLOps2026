# Troubleshooting — Module 09

Symptom → likely cause → fix. See the
[course troubleshooting hub](../../troubleshooting/index.md) for setup issues.

---

## 1. Registration

| Symptom | Likely cause | Fix |
|---|---|---|
| `missing model file: ...` | Pipeline hasn't run (or wrong folder) | `python -m pipe.run --clean` from `examples/churn` |
| `gate=None` on a version you expected gated | `--evaluation` pointed elsewhere / `pipe_out/evaluation.json` deleted | Check the path in your command; rerun `python -m pipe.run` to recreate it |
| `gate=None` even though you ran the pipeline | The evaluation file was cleaned up after registering | Re-register (versions are immutable — a corrected registration is the right move, with a note) |
| Same metrics for two versions — "is registration broken?" | You registered the same `model.joblib` twice; identical bytes, different events | Correct behaviour: two registrations record two moments in time. Retrain between them if you want distinct models |
| `PermissionError` writing `registry_store/` | File open in an editor / OneDrive-style sync lock | Close viewers; exclude `registry_store/` from sync if it keeps happening |

## 2. Promotion and refusals (refusals are usually correct)

| Message | Meaning | Action |
|---|---|---|
| `may only move one step at a time` | Lifecycle order enforced | Promote to `staging` first, then `production` |
| `never passed its quality gate` | No passing evaluation attached | Run the pipeline, re-register with the real `--evaluation` path |
| `unknown stage 'x'` | Typo | Valid stages: `development, staging, production, archived` |
| `no such version` | Wrong id (case/format: `v001`) | `python -m registry list` |
| Promotion "succeeded" but service unchanged | The **service process** resolves the model at startup | Restart the service — pointers are read at start (Module 10 explains why) |

**If you believe a refusal is wrong:** do not bypass it. First re-read the
rule (concepts §4), then — if it is genuinely a defect — write it up as an
issue (that is exactly what the independent challenge's task 3 looks for).

## 3. Rollback

| Symptom | Likely cause | Fix |
|---|---|---|
| `no recorded previous production version to roll back to` | Few than two distinct production promotions happened | Promote a second version first; rollback needs history to exist |
| `rollback implemented for 'production' only` | Called with another stage | Only production has a meaningful "way back" in this registry |
| Rolled back, but `/health` still shows the new model | Service caches its model at startup | Restart the service (Module 10) |
| History lost after deleting `registry_store/` | `index.json` was inside it | The store *is* the history — treat it as evidence, not junk (add it to backups, not to `.gitignore` evidence copies) |

## 4. Model card writing

- **"I don't know the population/limits."** Then the card's job is to say so:
  "not evaluated on X" is a valid, valuable line. Cards document *knowledge
  and its boundaries*.
- **"Metrics look bad."** Report them with context (our precision@0.5 = 0 is
  reported in every module since 06). A card that hides a number is worse than
  no card.
- **Rollback section empty** — you haven't rehearsed one. Run the lab's
  Step 4 until `history` contains your rollback event, then quote its output.

## 5. Conceptual checks

- **Is the registry a backup?** No — it versions *models and their lineage*.
  Your code/data backups are separate concerns (Module 04 handles data).
- **Does promoting retrain anything?** No. Promotion is a pointer change; the
  bytes were fixed at registration.
- **Can the registry tell you the model is good?** It can only tell you a
  *gate passed* — its opinion is as fresh as the evaluation you attached.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*