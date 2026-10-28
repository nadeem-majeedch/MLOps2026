# Concepts — Module 06

Tracking is not note-keeping — it is the difference between *"we tried a few
things"* and *"run `8e541425…` produced the model we shipped"*.

---

## 1. The question tracking exists to answer

Six months after a model ships, someone will ask:

> *Which code, on which data, with which settings, produced this result — and
> what did we try that worked worse?*

Without tracking, answering requires archaeology: chat history, half-renamed
notebooks, and memory. With tracking, it is a query.

**What must be recorded for a run:**

| Category | Examples | Why |
|---|---|---|
| **Parameters** (inputs you chose) | seed, split size, model family, learning rate, feature list | Without them a run cannot be repeated |
| **Metrics** (outputs you judge) | accuracy, ROC AUC, F1, training time | Without them runs cannot be compared |
| **Artifacts** (files produced) | model file, config copy, plots, metrics JSON | Without them the numbers cannot be re-inspected |
| **Source versions** (provenance) | git commit, data hash | Without them "same" cannot be verified |
| **Status & timing** | started/finished, failed | So a failing run is a record, not a mystery |

Modules 02, 04, and 05 already produce the last two (Git history, `.dvc` hash,
`config.yaml`); tracking is where they get attached to a *run*.

---

## 2. Vocabulary (MLflow's, and the general idea)

| Term | Meaning |
|---|---|
| **Experiment** | A named collection of related runs (e.g. `churn-baseline`) |
| **Run** | One execution: a set of params → metrics → artifacts |
| **Parameter** | An input you set before running |
| **Metric** | A measured output, usually numeric and comparable |
| **Artifact** | Any file produced or referenced by a run |
| **Tracking backend (store)** | Where run records live — a database or file tree |
| **Tracking server** | A service exposing the records (UI + API) |
| **Artifact store** | Where the files themselves live (folder, object store) |

!!! note "Tool-specific vs. general"
    These names are MLflow's, but the trio *parameters / metrics / artifacts*
    is the industry's shared vocabulary — Weights & Biases, Neptune, Aim, and
    Comet all use it. Learn the concepts once and every tracker reads easily.

---

## 3. Running MLflow with zero accounts

MLflow has three pieces you can mix:

| Piece | Local option (course default) | Cloud option |
|---|---|---|
| Tracking backend | **SQLite file** (`sqlite:///mlflow.db`) | Managed database (☁️) |
| Artifact store | Local folder (`mlruns/`) | Object storage (☁️) |
| Server + UI | `mlflow server` on `127.0.0.1` | Hosted UI (☁️) |

**A version-specific fact you will hit:** MLflow 3.x **rejects the legacy
plain-folder backend** (`file:./mlruns`) with an explicit error telling you to
migrate to a database backend. The course's script therefore uses
`sqlite:///mlflow.db` — still local, still free, still no account. This is a
healthy example of the general rule: *trackers change their storage defaults;
your practice (log everything, store locally) does not*.

**Privacy advantage:** running locally means hyperparameters, data-derived
metrics, and models never leave your machine — a real reason small teams start
here before adopting a hosted tracker (☁️).

---

## 4. Evaluation discipline: choosing, not collecting

Tracking creates a new failure mode: **ten runs, no decision**. The cure is a
decision procedure written *before* you look at results.

1. **State the business question first.** "Who should we contact with a
   retention offer?" implies recall at a contact budget — not raw accuracy.
2. **Pick the primary metric** for that question, and a tie-breaker.
3. **Fix the baseline and the comparison set** (split, seed, data version) so
   runs differ *only* in what you are testing.
4. **Then run**, and choose by the pre-stated rule.

### Two honesty checks this course's own data forces on you

- **Accuracy is trapped by imbalance.** In the shared example (9% churn),
  accuracy 0.91 equals the "predict nobody" baseline while F1 is 0.0. A run log
  full of accuracy numbers would rank models for the wrong reason.
- **One run is noise.** Module 05 measured AUC moving 0.7163 → 0.7418 from the
  *seed alone*. Any "improvement" smaller than that is not yet a finding:
  re-run, use cross-validation, or report a spread.

### Champion and challenger

- **Champion** — the model currently justified for use.
- **Challenger** — the candidate being compared against it.

A tracker's job is to make that comparison *auditable*: both runs, same data
version, same seed policy, different configurations, visible side by side.

---

## 5. Lineage: where tracking plugs into the lifecycle

```
data (M04: hash) ──┐
code (M02: commit) ─┼──► run (M06: params + metrics + artifacts) ──► registry (M09)
config (M05) ───────┘
```

Module 06 is the moment the chain becomes a single record. From here, "which
data produced this model" is a lookup rather than an investigation — the exact
capability that was missing in Module 01's incident.

**Minimum viable lineage for this course:** log the config as an artifact
(the script does), record the seed and split as parameters, and keep the data
file versioned (Module 04). Modules 09 and 12 strengthen this into registry
records and CI enforcement.

---

## 6. Reading results back

Two equivalent views, both worth knowing:

- **UI** (`mlflow server`) — for humans: timelines, parameter plots, artifact
  browsing.
- **Query API** (`mlflow.search_runs`) — for automation and for the lab's
  comparison table; returns a dataframe you can sort and export.

The lab uses the query so the comparison is *reproducible text* rather than a
screenshot.

---

## 7. Alternatives you will meet later

| Tool | Where it sits | Course stance |
|---|---|---|
| **MLflow** | Open source, local-first, registry included (M09) | **Used here** — same tool carries tracking → registry |
| Weights & Biases (☁️) | Hosted, polished collaboration, free tier | Good when teams need shared dashboards; account required |
| Neptune / Comet (☁️) | Hosted experiment trackers | Same trade-off |
| Aim / DVC-experiments | Open-source alternatives | Same concepts, different UIs |
| Plain CSV logging | The manual baseline | Works until the twelfth run — which is why the lab asks for ten |

---

## 8. Check yourself

1. Six months later, a model's AUC is reported as 0.78. List every artefact you
   would need to reproduce that number, naming the module that produced it.
2. Why is a spreadsheet "tracking"? At what run count does it fail, and why?
3. The lab asks for ten runs. What must be *identical* across them for the
   comparison to mean anything — and what must differ?
4. Your best run has the highest accuracy. Under what conditions is that the
   wrong choice?
5. Why does local tracking matter for privacy, and what would you check before
   moving to a hosted tracker?

*(Answers in [knowledge-check.md](knowledge-check.md).)*

---

**Next:** [worked-example.md](worked-example.md) — two real runs logged, and the query that compares them.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*