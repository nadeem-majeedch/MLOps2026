# Concepts — Module 08

*Vocabulary introduced here: stage, dependency graph / DAG, topological order,
idempotency, incremental execution, artefact, manifest, quality gate, sink,
upstream/downstream. Each is defined the first time it appears, and collected
in the [glossary](../../glossary/index.md).*

---

## 1. From a shell history to a declared pipeline

A first ML project is usually a list of commands someone remembers:

```
python generate_data.py
python -m src.validate ...
python -m src.train ...
python -m src.evaluate ...      # forgotten until something breaks
```

Three failure modes follow: **order errors** (you ran train before validate),
**omission errors** (you forgot evaluate), and **wasted work** (you retrained
when nothing changed). A **pipeline** fixes all three by *declaring* the work
instead of *imperatively* typing it.

> **Stage** — a named unit of work with declared inputs and outputs.
> **Dependency graph (DAG, directed acyclic graph)** — stages as nodes,
> "must run after" as directed edges, with no cycles (an acyclic graph has no
> path that loops back on itself — otherwise "after" has no meaning).

Our six stages:

```
generate ─► validate ─► features ─► train ─► evaluate ─► report
 (data)      (gate)     (table)     (model)   (gate)      (human)
```

**Topological order** = any ordering where every stage appears *after* all of
its dependencies. For a linear chain there is only one; for a branching graph
several exist — the runner computes one each time (depth-first visit, cycle
detection included).

Why the runner and not a shell script? A script encodes order by *position*;
a graph encodes it by *declaration*. Delete a stage from a script and you must
re-check every line after it; delete one from a graph and the order repairs
itself.

## 2. The contract each stage follows

Every function in `pipe/stages.py` obeys four rules — the same rules the
[module 03](../03-ml-project-technical-debt/index.md) refactor established:

1. **Reads only declared inputs.** If a stage secretly opens another folder,
   the runner cannot know when to re-run it → silently stale results.
2. **Writes only declared outputs** (in `pipe_out/`, plus `generate`'s raw file).
3. **Is deterministic.** Same inputs → byte-identical outputs. Without this,
   "unchanged" cannot be detected by hashing.
4. **Fails loudly.** A stage raises instead of returning partial results —
   a half-written artefact consumed downstream is worse than a stopped run.

**Artefact** — a file produced by a stage and consumed by a later one.
**Upstream/downstream** — relative direction in the graph: `train` is
downstream of `features`, and `features` is upstream of `train`.

## 3. Incremental execution: how the runner decides

The runner keeps a **manifest** (`pipe_out/manifest.json`): for each stage, its
status, duration, and a *signature*. The signature is computed fresh on every
run from three things:

| Signature part | Answers |
|---|---|
| sha256 of each declared **input** file | did the data or config change? |
| sha256 of the stage's **own source** (`inspect.getsource`) | did the code change? |
| sha256 of each declared **output** file | did someone edit or delete the results? |

A stage is skipped only when `stored signature == current signature` **and**
every output exists. Consequences worth internalising:

- Editing only `report()`'s source re-runs **only** `report` (each stage hashes
  its *own* function, not the whole file).
- Hand-editing `pipe_out/features.csv` makes `features` re-run (outputs are
  hashed, not just checked for existence) — and because regeneration is
  deterministic, `train` then finds identical input bytes and still skips.
- Deleting an output forces just that stage to rebuild it.

> **Idempotent** — running something twice has the same effect as running it
> once. Every stage must be idempotent, or incremental execution corrupts
> results the first time two runs overlap.

## 4. Failure handling: stop, record, resume

When a stage raises:

1. The runner records `{"status": "failed", "error": ...}` in the manifest.
2. Every remaining stage prints `BLOCKED (upstream '<name>' failed)` — **downstream
   work never runs on a broken upstream** (your Module 04 data gate would be
   pointless if train could start anyway).
3. The process exits **1** — a number CI (Module 12) and schedulers (Module 13)
   can act on.
4. Re-running the same command resumes: finished stages skip, the failed stage
   retries, blocked stages run.

Two kinds of failure, two different responses:

| Kind | Example | Response |
|---|---|
| **Gate refusal** (expected) | `evaluate`: `roc_auc 0.7163 < floor 0.99` | stop; fix the model or the floor |
| **Crash** (unexpected) | `KeyError: 'contract'` from a renamed config key | stop; fix the code/config, then resume |

## 5. Quality gates inside the flow

A **quality gate** is a stage whose *job* is to refuse. This module adds two:

- `validate` refuses bad data (Module 04's checks, now inside the graph);
- `evaluate` refuses weak models (`quality.roc_auc_floor` in `config.yaml`).

Gates belong *in* the pipeline, not in a wiki: the workflow then cannot produce
an artefact that skipped its own gate. (Module 12 puts the same gates in CI so
a human cannot bypass them either.)

## 6. Artefact flow and the report

`report` is a **sink** — a stage nothing else depends on, whose output is for
humans. It records metric values *and* the first 16 hex characters of each
artefact's sha256. Those hashes are the evidence you will reuse in Module 09
(lineage), Module 12 (CI checks), and the capstone (reproducibility proof).

## 7. One-command rebuild

`python -m pipe.run --clean` deletes `pipe_out/` and rebuilds from raw data.
The point is not convenience — it is **proving the pipeline is complete**. A
pipeline that only works with leftover files from yesterday's run is a pipeline
with a hidden stage. The clean rebuild is the honest test of "everything needed
is declared".

## 8. When *not* to build a graph

Three stages in a shell script is fine. Reach for a declared graph when you
answer yes to any of: (a) order matters and more than one person changes it,
(b) re-running is expensive enough that skipping matters, (c) failures need an
audit trail, (d) gates must be impossible to bypass. Scheduling those same
stages (runs at 02:00, retries, alerts) is **orchestration** — Module 13's
topic; [tool selection](../../syllabus/tool-selection-guide.md) compares the
options across the course.

---

**Next:** [worked-example.md](worked-example.md) — the actual runs, including
a real failure and its resume.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*