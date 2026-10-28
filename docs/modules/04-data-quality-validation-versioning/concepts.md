# Concepts — Module 04

Two ideas, in this order: **validation** (is this data what I think it is?) and
**versioning** (can I get *exactly* this data again?). Tools arrive only after
each idea is clear.

---

## 1. Why data needs its own checks

A compiler catches broken code before it runs. Nothing does that for data —
because a CSV file is *syntactically* valid even when it is nonsense: right
number of columns, wrong meaning.

Four silent killers, all of which you will meet in this module's lab:

| Killer | Example | How it looks from the code's side |
|---|---|---|
| **Missing values** | `monthly_charges` empty for 120 rows | Runs fine; means and models quietly shift |
| **Type drift** | `1,234.50` written by a different locale, or `n/a` | Column read as text; arithmetic breaks or coerces silently |
| **Duplicate keys** | The same `customer_id` exported twice | Row counts and metrics inflated |
| **Domain violations** | `contract_type = "lifetime_deal"` never seen in training | One-hot encoding produces all-zeros — the model gets a blank |

**Validation** is the practice of writing these expectations down as executable
checks, so a bad extract fails *before* it reaches a model.

!!! note "Tool-specific vs. general"
    The checks below are plain pandas — deliberately. The general principle is
    *"declare expectations, execute them, fail loudly."* pandera expresses the
    same thing with types; Great Expectations adds reporting and scheduling.
    Whichever tool you meet later, you will recognise it instantly.

## 2. The check families

| Family | Question it answers | Typical check |
|---|---|---|
| **Schema** | Are the columns and types what I declared? | required columns present; numeric columns numeric |
| **Completeness** | Is anything missing? | `isna()` counts below a threshold |
| **Uniqueness** | Are keys unique? | `duplicated()` on the key column |
| **Range / domain** | Are values plausible? | `tenure_months >= 0`; `contract_type ∈ {…}` |
| **Target sanity** | Is the label usable? | binary target; positive rate within bounds |
| **Distribution** | Has the data *moved*? | compare to a baseline snapshot (Module 14) |
| **Volume / freshness** | Did the extract arrive, complete? | row count and max date within expectations |

The first five are **structural** — cheap, deterministic, run everywhere. The
last two are **statistical** — they need a baseline and a tolerance, and they
belong more to monitoring (Module 14) than ingestion.

### Where validation runs

```
ingestion ──► pre-training ──► CI (on every change) ──► serving
   │               │                  │                    │
   catch          catch              catch a bad          catch drift
   bad files      bad joins          code/data combo      in production
```

Each position catches a different class of problem; only the first three are
cheap enough to run always. The lab practises the first two, and Module 12 wires
one into CI.

### Error messages are a design surface

A failed check must say *what*, *where*, and *how many*:

```text
[FAIL] no_missing_values        columns with nulls: monthly_charges=120
```

not `AssertionError`. You are writing this message for the person paged at 3 a.m.

---

## 3. Data contracts and dataset cards

Two documents that make expectations social rather than personal:

- **Data contract** — an agreed specification of a dataset: schema, quality
  thresholds, owner, and update cadence. It exists so a producer changing the
  format has to talk to the consumers *first*.
- **Dataset card** — what this dataset is: source, licence, size, collection
  method, known limitations, intended use, and sensitive content. Module 03
  touched model documentation; this is its data-side twin.

Both are Markdown files in the repository. Cheap to write, expensive to fake,
and the difference between "someone should have told us" and "someone did".

---

## 4. Data versioning — the principle

**Versioning** means: any result can be traced to the exact bytes that produced
it, and those bytes can be restored on demand.

### Why Git alone is not enough

Module 02 taught Git to version *code*. Datasets break that model:

- a 2 GB CSV in Git makes every clone painful, forever;
- data often changes without a corresponding code change;
- you want to ask "what did the data look like on 1 March?" without diffing
  gigabytes.

### The mechanism, before the tool

1. **Immutability:** once an experiment references a dataset, that dataset does
   not change under it. New data ⇒ new version, always.
2. **Content hash:** a short fingerprint computed from the bytes. Same bytes ⇒
   same hash; any edit ⇒ different hash. This is how you *prove* two machines
   used the same file.
3. **Pointer file:** a tiny text file, safe for Git, recording the hash, size,
   and path of the real data — which lives outside Git (or in a remote store).

```
Git tracks:      churn.csv.dvc      (a few lines of text: md5 18df7e78…, 60755 bytes)
Data lives in:   data/raw/churn.csv (large, in the cache or a remote)
```

That split — **code and pointers in Git, data elsewhere** — is the whole idea.

!!! warning "The honesty rule"
    If the recorded hash does not match the file, you do *not* have the version
    you think you have. Always verify: the lab makes you compare them.

---

## 5. DVC — the tool, mapped to what you already know

[DVC](https://dvc.org/doc) (Data Version Control) is free and open source, and it
borrows Git's mental model on purpose. Since you did Module 02, every DVC term
has a Git twin:

| You already know (Git) | DVC equivalent | Difference |
|---|---|---|
| `git init` | `dvc init` | Creates DVC's own metadata (`.dvc/`) |
| `git add file` | `dvc add data/raw/churn.csv` | Real file moves to DVC's cache; Git gets a tiny `.dvc` pointer |
| `git status` | `dvc status` | Reports *data* changes: `up to date` or `modified` |
| `git checkout` | `dvc checkout` | Restores the exact bytes; **refuses without `--force` if you edited the file** |
| commit message/history | Git history holds the pointer changes | Data bytes are addressed by hash, not stored in Git |
| remotes (GitHub) | DVC remotes (local dir, S3, …) | ☁️ optional; local cache is enough for this course |

**Usage pattern to remember:** Git for code, DVC for data, *both* updated
together — a commit that changes the data pointer without the code that expects
it (or vice versa) is exactly the split-brain you are trying to prevent.

**No cloud required:** the lab uses DVC's local cache only. Remote storage is an
optional extension (☁️), never the graded path.

---

## 6. Lineage — why you are doing this

**Data lineage** is the record of where data came from and what happened to it.
You get it almost as a side effect of §4: a commit references a `.dvc` pointer,
the pointer references exact bytes, and the training script (Module 05) will
record its config. Chain them and you can answer, later and under pressure:

> *Which code, on which data, produced this model?*

Module 06 logs the run; Module 09 registers the model. The chain starts here.

---

## 7. Check yourself

1. Your validator checks only "required columns exist". A CSV arrives with
   correct columns and 40% blank cells. Which check families are missing?
2. Why must a validation failure print counts, not just a boolean?
3. Two laptops hash the same file and get different values — list three possible
   causes (think line endings, encodings, edits).
4. Explain to a teammate why `churn.csv.dvc` should be committed but
   `churn.csv` should not.
5. Which stage of the lifecycle does a *contract* protect, and which does a
   *dataset card* serve?

*(Answers in [knowledge-check.md](knowledge-check.md).)*

---

**Next:** [worked-example.md](worked-example.md) — the validator run against four real files, with its actual output.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*