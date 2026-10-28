# Concepts — Module 09

*Vocabulary: artefact, bundle, signature, lineage, model registry, version,
stage, promotion, approval gate, rollback, model card, retirement, alias.*

---

## 1. An artefact is a file; a *model artefact* is a bundle

Saving weights is not enough. To serve a model you need four things that must
travel together:

| Part | Why it must travel | In our project |
|---|---|---|
| The fitted pipeline | includes **preprocessing** (scaling/one-hot) — raw weights without it cannot score raw rows | `model.joblib` (the whole sklearn `Pipeline`) |
| The signature | which columns, types, and categories the model expects | `FEATURES` in `service/model.py`, recorded in `metadata.json` |
| The metrics | what "good" meant at training time | `metrics` copied into `metadata.json` |
| The lineage | which data/config/code produced it | `data_sha256`, `model_sha256`, gate result, note |

> **Lineage** — the traceable origin of an artefact: data version, config,
> parameters, metrics, time, and who registered it. Without it, "where did
> this model come from?" has no answer six months later.

> **Model registry** — the system of record for model versions and their
> lifecycle state. It answers: *what exists, what stage each version is in,
> who approved it, and what was production yesterday?*

## 2. Local demonstration vs remote service (read this carefully)

This course ships a **local file registry** (`registry_store/` + `index.json`):

| | Local registry (this module) | MLflow Model Registry (typical production) |
|---|---|---|
| Storage | files in your repository folder | a tracking **server** with a database |
| Access | one machine, no auth | multi-user, roles/permissions, UI |
| Promotion | your CLI, refused without a passed gate | UI/API transitions, **approval hooks**, webhooks |
| Consumers | your service reads `index.json` | served models fetched by stage/alias |
| Extra features | none | aliases (`champion`/`challenger`), stage history UI, signature/quality registration |

**The concepts are identical; the transport is not.** Everything you do here
maps one-to-one onto the remote service — which is why the syllabus teaches
the concept *before* the hosted tool (see
[tool selection guide](../../syllabus/tool-selection-guide.md); the remote
registry is ☁️ optional and needs an account/server).

## 3. Versioning: immutable, numbered, never edited

`v001`, `v002`, … are **immutable**: a mistake produces `v004`, not an edit to
`v002`. Immutability is what makes rollback meaningful — the bytes you roll
*back to* are guaranteed to still exist. Two consequences students hit:

- Registering the *same* model file twice legitimately creates two versions
  (they are two events in time, with different notes and lineage).
- "Fixing metadata" means registering again with a note explaining the fix —
  the audit trail stays honest.

## 4. Stages, promotion, and approval gates

Our lifecycle: `development → staging → production`, plus `archived`.

- **Stage** — where a version currently sits in its lifecycle.
- **Promotion** — an explicit, recorded transition between stages.
- **Approval gate** — a machine-checked precondition. This registry enforces two:
    1. **one step at a time** — `development → production` is refused (you
       cannot skip testing);
    2. **passed quality gate required** — a version registered without a
       passing `evaluation.json` can never reach production.

Both refusals are *features*. The recorded refusal is also evidence: the
history shows what the system would have allowed.

## 5. Rollback: decide the way back *before* you go forward

**Rollback** — returning a stage pointer to the previously recorded version.
Our registry stores `previous_production` at every promotion, so:

```powershell
python -m registry rollback production
```

is a single, recorded, tested action. Three properties make it real:

1. The old version's **bytes were never deleted** (immutability).
2. The **pointer** moves, not the files (cheap, instant).
3. The event lands in `history` (auditable — you can see which incident caused it).

Promotion without a rehearsed rollback is not a release process; it is hope.
(Module 10's service picks the model through this pointer, so a rollback
changes what serves — that is the point.)

## 6. Lifecycle management: beyond promotion

- **Audit trail (`history`)** — append-only list of register/stage/rollback
  actions with timestamps and actor. Answers "who promoted this, when?"
- **Retirement** — moving a version to `archived` when it is no longer a
  rollback candidate (after N newer stable versions, or after the data
  contract it was trained on is gone). Archived ≠ deleted: evidence survives.
- **Deciding what to keep:** keep every version that could still be rolled
  back to; deduplicate *artefact storage*, never *history*.

## 7. Model cards (LO 9.4)

> **Model card** — a short, fixed-structure document: intended use,
> out-of-scope use, training data, evaluation metrics (with context),
> limitations/risks, and ethical considerations.

It is part of the artefact because metrics without *context* mislead: an AUC
of 0.7163 means little until you state the population, the threshold, and that
precision at 0.5 is 0.0 (our example's honest wart from Module 06/08). The lab
requires one card for your production version; Module 15 connects cards to
governance.

## 8. What the service reads (bridging to Module 10)

`service/model.py` resolves the serving model in this order: registry
`production` pointer → training artefact → none (503 with instructions).
So the registry is not documentation — it is the **switch** your API reads.
Promote, and the next process start serves a different model; roll back, and
it serves the old one.

---

**Next:** [worked-example.md](worked-example.md) — the registry's real output,
including both refusals.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*