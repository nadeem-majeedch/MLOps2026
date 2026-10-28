# Concepts — Module 03

Structure is not aesthetics. In an ML project, *where* something lives determines
whether anyone can find it, test it, reproduce it, or safely change it.

---

## 1. Anatomy of an ML project

The layout used in this module (and by the shared example) — with the reason for
each entry:

```
project/
├── README.md            # what it does, how to set it up, how to run it
├── pyproject.toml       # dependencies + project metadata
├── config.yaml          # every behaviour-affecting value, out of code
├── data/
│   ├── raw/             # generated or downloaded inputs — never edited by hand
│   └── corrupt/         # deliberately broken fixtures for tests
├── src/                 # importable logic (functions and modules only)
│   ├── features.py      # feature construction
│   ├── validate.py      # data checks
│   └── train.py         # training and evaluation
├── legacy/              # old notebooks, kept for history, not imported by anything
├── experiments/         # scripts that run training with tracking (M06)
├── tests/               # automated checks (M07)
└── artifacts/           # model files, metrics — generated, never committed
```

Rules that make this layout work:

1. **`src/` contains no surprises.** Modules here are importable and side-effect
   free: importing them must not train anything, read data, or write files.
2. **One entry point.** Everything runnable lives at the top level (`run.py`) or
   is a documented command. If a stranger needs to know which of twelve scripts
   to run, the README has failed.
3. **Generated things are generated.** `data/`, `artifacts/`, and environments
   are rebuilt, not committed (Module 02 taught the `.gitignore` half).
4. **Configuration is data, not code.** Change behaviour by editing
   `config.yaml`, so a diff shows *intent* instead of *logic*.
5. **`legacy/` is a graveyard, not a shelf.** Old notebooks stay for reference
   and are never imported by the live code.

!!! note "Tool-specific vs. general"
    The folder names are a convention (this course's, influenced by
    cookiecutter-data-science). The *principles* — separation of concerns, one
    entry point, generated artefacts excluded, configuration external — are
    universal and survive any renaming.

---

## 2. Technical debt in ML systems

**Technical debt** is the future cost of a shortcut taken today. It is not
"bad code" — it is code whose next change will cost more than it should.

The ML-specific taxonomy (Sculley et al., 2015 — see
[references.md](references.md)):

| Debt type | What it looks like in an ML project | Why it is worse in ML |
|---|---|---|
| **Data dependency debt** | A file path or column name assumed in five places | Data changes independently of code, so the assumption breaks silently |
| **Entanglement** | Features that cannot be changed or tested separately | Improving one thing risks breaking three others |
| **Hidden feedback loop** | Model outputs that later become training inputs | The system quietly teaches itself its own mistakes |
| **Undeclared consumers** | Someone else's spreadsheet reads your output file | You discover the dependency when you rename it |
| **Configuration debt** | Magic numbers inside cells (`test_size=0.25`, `random_state=7`) | Nobody can say *why* 0.25, or what happens at 0.2 |
| **Glue code debt** | Manual steps between stages ("then paste this into…") | Every manual step is an outage waiting for a holiday |
| **Pipeline sprawl** | Twelve scripts that each half-run the job | Nobody knows which sequence is the real one |

**The ML-specific amplifier:** conventional debt accrues when code changes; ML
debt accrues when **data changes even if code does not**. That is why structure
must include data checks (Module 04) and not just tidy folders.

---

## 3. Notebook hygiene

Notebooks are excellent for exploration and dangerous as a home for production
logic. The four failure modes you can see in `legacy/analysis.ipynb`:

1. **Hidden state.** A cell uses a variable defined three cells earlier — rerun
   out of order and you get a different answer (or a `NameError`). The notebook
   "works" only in the exact session that produced it.
2. **Logic trapped in cells.** Nothing can be imported, tested, or reused, so
   the same 8 lines get pasted into the next notebook.
3. **Unreviewable diffs.** A `.ipynb` is JSON with embedded outputs: a two-line
   change shows as a 400-line diff, and real changes hide inside it.
4. **No entry point.** "Run cells top to bottom" is not a command anyone can
   automate — and Modules 07 and 12 need exactly that.

**Hygiene rules** (each maps to a fix in the lab):

| Rule | Mechanism |
|---|---|
| Notebooks explore; `src/` holds what matters | Move logic out as soon as it stabilises |
| Outputs never enter version control | `nbstripout` or jupytext pairing |
| Notebooks must run top-to-bottom in a fresh kernel | Test this before committing |
| One source of truth for each calculation | A function called twice beats a formula pasted twice |

---

## 4. Configuration versus code

A **magic number** is a value embedded in logic with no stated reason.
Configuration moves those values into a file, which buys you:

- **Diffable intent:** a pull request showing `test_size: 0.25 → 0.20` is a
  decision you can review; the same change buried in a cell is not.
- **Experimentation without editing code** (Module 06 logs the config with each run).
- **One place to look** when a result surprises you.

What does *not* belong in configuration: things that change what the code *is*
(function structure, business rules). If editing it could silently invalidate
every past experiment, it belongs in code and tests.

---

## 5. The README as a contract

Your README must answer four questions without a human in the loop:

1. What does this project do? (one paragraph)
2. What do I need installed? (versions)
3. How do I run it? (copy-pasteable commands)
4. What output should I see? (expected result)

The lab grades exactly these. If any answer requires you to be present, the
project is not reproducible — which was Module 02's whole point.

---

## 6. Where debt shows up in the lifecycle

```
data ──► validate ──► train ──► evaluate ──► register ──► serve ──► monitor
  │          │          │          │            │          │          │
  └── path debt     config debt  metric debt   lineage   glue code  undeclared
      entanglement  hidden state  no baseline   (no entry) (manual)   consumers
```

Every arrow between stages is where glue code and manual steps accumulate.
Modules 04–14 remove them one at a time: validation (04), configuration (05),
tracking (06), tests (07), automation (08), registry (09), APIs (10), containers
(11), CI (12), orchestration (13), monitoring (14).

---

## Check yourself

1. A colleague says: "the notebook works, so the structure can wait." Give the
   strongest version of their argument, then refute it with two debt types from §2.
2. In `legacy/analysis.ipynb`, find: a duplicated calculation, two magic numbers,
   a hidden-state risk, and a side effect. (Check yourself against
   [worked-example.md](worked-example.md).)
3. Why must `src/` modules be side-effect free? What breaks if importing
   `features.py` started training a model?
4. Which is worse and why: configuration debt or entanglement?

*(Answers in [knowledge-check.md](knowledge-check.md).)*

---

**Next:** [worked-example.md](worked-example.md) — the same analysis twice: as the notebook, and as a project. Identical numbers.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*