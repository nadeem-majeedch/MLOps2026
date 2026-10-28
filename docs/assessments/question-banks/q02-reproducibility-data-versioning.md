# Question bank 02 — Reproducibility and data versioning

**Covers:** Modules [02 — Python, Git, CLI, environments](../../modules/02-python-git-cli-environments/index.md),
[04 — Data quality, validation, versioning](../../modules/04-data-quality-validation-versioning/index.md),
[05 — Reproducible training & pipelines](../../modules/05-reproducible-training-pipelines/index.md).
**Format:** 10 questions — multiple choice, short answer, debugging, architecture, scenario.
**Suggested check:** 7/10, with **R5** and **R10** correct.

> *Attempt first, then read the
> [reference solutions](../keys/question-banks-KEY.md).*

---

## Part A — Multiple choice

**R1.** Two runs of the same training script produce different metrics. Which
set of causes is *complete*?

- (a) random seed, unsorted file reads
- (b) random seed, unsorted file reads, non-deterministic library kernels,
  hidden state from a previous run, hardware differences
- (c) random seed only
- (d) the learning rate

**R2.** What does `pip freeze > requirements.txt` guarantee?

- (a) The code will run on any machine
- (b) The exact versions used *in that environment* are recorded
- (c) The project is reproducible forever
- (d) Dependencies are secure

**R3.** A 2 GB dataset must be tracked so a colleague can reproduce your
experiment. What is the best approach?

- (a) Commit the file to Git — Git handles big files well
- (b) Commit a downloader/generator script plus a checksum; keep the bytes out
  of the repository
- (c) Email the file
- (d) Don't track data at all; the code is enough

**R4.** Which is a *data-contract* violation, as opposed to a modelling issue?

- (a) AUC dropped two points
- (b) `monthly_charges` now arrives as text
- (c) The model favours precision over recall
- (d) The threshold is 0.5

## Part B — Short answer

**R5.** Explain the difference between **data versioning** and **data
lineage**, and name one tool or mechanism the course uses for each.

**R6.** Your `train.py` reads `data/*.csv` with `glob.glob()` and no sort.
Explain precisely how this can change results, and give two independent fixes.

**R7.** A teammate says: "I committed the seed, so it's reproducible."
List four other things that must also be fixed or recorded.

## Part C — Debugging

**R8.** Find **three** distinct reproducibility defects in this snippet and say
what each one breaks:

```python
df = pd.concat([pd.read_csv(f) for f in glob.glob("data/*.csv")])
df = df.sample(frac=1)                      # shuffle
model.fit(df[X], df[y])
np.random.seed(42)                          # set once, at the end of the file
open("results.txt", "a").write(str(score))  # append
```

## Part D — Architecture

**R9.** Sketch the flow of a **validated, versioned data pipeline**: raw
extract → validation → versioned dataset → training. Mark where a schema check
runs, where a version id is written, and what a failing check must *prevent*.

## Part E — Scenario

**R10.** Last month's model scored 0.84 AUC; today's identical code scores
0.79. The data file has the same name. Walk through your diagnosis in order —
which commands you run, what each result would tell you, and the point at
which you conclude "data changed" versus "environment changed".

---

**Next:** [reference solutions](../keys/question-banks-KEY.md) (bank 02), then
[bank 03](q03-experiment-tracking-evaluation.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../../about/index.md).*
