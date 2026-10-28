# Concepts — Module 15

Security, privacy, fairness, and governance are usually taught as compliance
lectures. This module teaches them as **engineering**: each concept below is a
thing you can build, measure, or refuse. Where a statement is a *general
principle* versus *tool-specific behaviour*, it is marked **Principle** or
**Tool**.

---

## 1. Threat modelling in one page

**Threat modelling** (vocabulary) = writing down what you are protecting,
from whom, and through which doors — *before* you are attacked, or audited,
or simply wrong.

The four questions (a lightweight version of the classic "four questions"):

```
1. What are we building?      -> an ML scoring API serving a model artifact
2. What can go wrong?         -> enumerate threats (below)
3. What are we going to do?   -> one control per threat
4. Did we do a good job?      -> re-run the checks; write down residue
```

**Assets** for an ML service are wider than for ordinary software:

| Asset | What losing it looks like |
|---|---|
| Training data | privacy breach, regulatory exposure, poisoned model |
| Model artifact | theft, or *substitution* (someone serves a worse/fraudulent model) |
| Credentials (API keys, DB URLs) | everything above, at scale |
| Predictions | PII leaks (a score about a person *is* personal data) |
| Integrity of the whole chain | silently wrong answers nobody notices |

**Threats**, in the language you will hear in industry:

| Term | Plain meaning | Example from Lab 15 |
|---|---|---|
| **Secret leakage** | credentials in source, logs, or history | `API_KEY = "prod-secret-…"` |
| **Missing authentication** | anyone who reaches the port can call | defect 3: `/predict` has no check |
| **Missing authorization** | authenticated, but allowed too much | a student token able to read everyone's scores |
| **Unsafe deserialization** | loading bytes executes code | defect 4: bare `pickle.load` |
| **Injection into preprocessing** | crafted inputs manipulate the pipeline | absurd feature values that skip validation |
| **Model theft** | downloading your artifact | unauthenticated model-export endpoint |
| **Denial of service** | unbounded work per request | a 10-million-row `records` array |

**Principle:** a threat model is complete when every listed threat has a
control *and* an owner, and everything you decided *not* to fix is written
down as accepted risk. An undocumented non-fix is the same as an oversight.

## 2. Secrets vs configuration, and least privilege

**Configuration** is *what the program should do* — thresholds, feature
lists, ports. It belongs in the repository: it is reviewed, versioned, and
reproducible.

**Secrets** are *keys to other systems* — API keys, database passwords,
signing keys. They grant power outside your repo, so they belong **outside**
your repo: in environment variables, a secret manager, or (for the course)
your shell profile / `.env` file that is git-ignored.

| | Configuration | Secret |
|---|---|---|
| In git? | yes | **never** |
| Rotatable? | n/a | must be, quickly |
| If leaked? | no harm | rotate *first*, investigate second |
| Test doubles | commit fixtures | use obviously-fake placeholders |

**Blast radius** is the deciding test: if the value appearing in a public
diff would require an incident response, it is a secret.

**Least privilege (Principle):** every actor — user, service, CI job,
container — holds the smallest set of permissions that lets it do its job,
for the shortest time it needs them. Concretely:

- the CI workflow in `.github/workflows/` needs `permissions: contents: read`
  and nothing else (Module 12 already set this);
- the API process needs read access to one model file, not your whole home
  directory;
- a human's database account cannot `DROP TABLE`, because no task requires it.

**Tool:** free scanners — `gitleaks` (scans git *history*; the industry
standard, free and open source) and this course's
[`scan_secrets.py`](https://github.com/nadeem-majeedch/MLOps) (install-free,
two rules, readable). Scanning is a seatbelt, not a substitute for not
committing secrets: **rotation is the real fix**, because history and clones
retain the old value.

## 3. Supply-chain risk (ML edition)

Everything you import is trust you extended to strangers:

- **Python dependencies** — pin versions (Module 02), install from a lock or
  pinned requirements (Module 11), review what a new package does.
- **Container base images** — pin tags (`python:3.14-slim`, not `:latest`);
  rebuild regularly to pick up security patches.
- **Model artifacts** — *the ML-specific twist*. A model file is code: pickle
  and joblib formats run Python bytecode on load. Only load artifacts your
  own pipeline produced, from a path you control, after verifying an
  integrity digest (**Tool:** the fixed service checks a `sha256` sidecar
  before `pickle.load`; alternatives like ONNX or skops serialize without
  arbitrary code execution, at the cost of model-format compatibility).
- **Data files** — a CSV is benign until you `eval` it; a parquet/feather
  file can carry surprising types. Validate on entry (Module 04).

**Principle:** verify integrity (hash), verify provenance (who built it),
verify freshness (is this the version we approved?) — for code, images,
models, *and* data alike. That triple is exactly what a registry record
(Module 09) stores.

## 4. Privacy: minimisation, pseudonymisation, and log hygiene

**PII** (personally identifiable information) is any data that identifies a
person directly (name, email) or indirectly (a rare combination of
attributes). In an ML system, **predictions are PII**: "student S-0007 has a
0.86 support probability" is a fact about a person.

Three rules (**Principle**):

1. **Minimisation** — collect and keep only what the task needs. If the
   model does not consume `email`, it should not enter the service, the log,
   or the training export.
2. **Pseudonymisation** — replace direct identifiers with a stable reference
   (`S-0007`) *before* data reaches logs, lakes, or notebooks. A pseudonym
   is still personal data, but its exposure is far smaller.
3. **Log hygiene** — decide *per field*: logged / not logged / hashed.
   The default for anything about a human is **not logged**. Logs are copied
   to support tools, retained for months, and read by far more people than
   the database ever was.

Defect 2 in the lab writes `email=amina@example.edu` into a log line. The
fix is not "redact better" — it is "log the pseudonymous reference, or
nothing". Supporting techniques, with honest limits:

- **Anonymisation** (irreversible aggregation) — safe for statistics,
  incompatible with per-record prediction.
- **Pseudonymisation** (reversible, key held elsewhere) — the practical
  choice for operational logs.
- **Tokenisation / key separation** — the mapping lives in a system the log
  pipeline cannot reach.
- **Retention windows** — a log with a 30-day deletion policy leaks less by
  construction than one kept forever.

**Tool:** `logging` with a field allowlist; nothing exotic required.

## 5. Fairness: measure it, then stay humble about it

**Bias vs variance** exists in two unrelated senses — do not confuse them:
in ML statistics (underfit/overfit) and in *social* usage (systematic
unfair treatment). This module means the second.

**Group fairness** (**Principle**): compare an outcome rate across groups
defined by a sensitive attribute (here: `device_access` — a proxy for
socio-economic circumstances). The lab's metric is the **selection-rate
gap**:

```
gap = | P(flagged | group A) − P(flagged | group B) |
```

Real numbers from the capstone's 400-row baseline window (see
[worked-example.md](worked-example.md)):

| Decision rule | rate group 0 | rate group 1 | gap |
|---|---|---|---|
| group-dependent (flawed: 0.25 vs 0.60) | 0.0000 | 0.1270 | **0.1270** — over target |
| one global threshold (fixed: 0.25) | 0.1935 | 0.1270 | **0.0665** — within the 0.10 target |

Read the first row again: the flawed rule flags **nobody** from group 0.
That is not an abstract metric — it is a support service systematically
ignoring the students most likely to need it.

**The limits you must state alongside any number:**

- One metric is one lens. Other fairness definitions (equalised odds,
  calibration, individual fairness) can *conflict*; no model satisfies all
  of them simultaneously in general.
- A gap is a **prompt to investigate**, not proof of discrimination — and a
  zero gap is not proof of fairness (a model can be equally useless to
  everyone).
- Proxies matter: `device_access` correlates with income; auditing one
  column does not clear the others.
- What you *measure* depends on what you *label* — if `at_risk` itself
  encodes historical disadvantage, parity on that label can re-encode it.

**Tool:** [fairlearn](https://fairlearn.org/) (free, open source) computes
many of these metrics on plain pandas data; the course's
`fairness_audit()` in `src/train.py` computes the selection-rate gap in
twenty lines so you can see every step first.

**Ethics note:** a fairness report is a decision *aid* for humans. The
course never treats a metric as an automated release verdict — the capstone
requires a written, human `--ack` when shipping with an over-target gap
(Module 09 / `release.py`).

## 6. Governance artefacts: write it down

Governance sounds bureaucratic until an incident happens; then these four
documents are the difference between "we can explain ourselves" and "we
cannot".

| Artefact | One sentence | Kept with |
|---|---|---|
| **Model card** | What the model is for, how it was built, how well it works, where it must not be used | `docs/` next to the model, linked from the registry record |
| **Datasheet** (data documentation) | Where the data came from, how it was collected/labelled, its licences and limitations | with the dataset |
| **Risk register** | Named risks, likelihood × impact, owner, mitigation, *accepted* residue | project root, updated at each release |
| **Audit trail / lineage** | Which data, code, config, and human produced the serving model — and every promotion/rollback | registry history (`release.py history`, Module 09) |

**Lineage** is the technical backbone: with content hashes (Module 08's
manifest, Module 09's record) you can answer "what exactly is serving?" in
seconds: `release.json` → release directory → `data_sha256` → the dataset
→ `runs.jsonl` → the run → the git commit.

**Model card minimum viable sections** (write these in the capstone):

1. Model details (version, date, owner, framework)
2. Intended use & **out-of-scope use**
3. Training data & provenance (with licence)
4. Evaluation — metrics *with the split they came from*, plus subgroup table
5. Fairness analysis and its caveats
6. Ethical considerations, limitations, caveats
7. What would trigger retraining or withdrawal

**Regulation, concepts only:** data-protection law (e.g. GDPR in Europe,
similar frameworks elsewhere) generally requires a lawful basis, purpose
limitation, minimisation, storage limits, and accountability — i.e. the
artefacts above are not paperwork for their own sake. **This course gives
informational context, not legal advice**; for real deployments, policy or
legal specialists decide.

## 7. Incident response: when prevention fails

**Incident response** (**Principle**) is a rehearsed loop, not improvisation:

```
detect -> contain -> assess -> disclose/notify -> recover -> review
   ^                                                        |
   +---------------------- runbook updated -----------------+
```

For an ML system specifically:

| Phase | ML-specific action |
|---|---|
| Detect | monitoring alerts (Module 14), failed probes (Module 11), abuse reports, secret scanner in CI (Module 12) |
| Contain | revoke the leaked key; **`python release.py rollback`** (Module 09); disable the endpoint |
| Assess | which data/model/predictions were touched; hash comparison + lineage (§6) |
| Notify | users/owners per policy — a *human* decision, pre-allocated in the runbook |
| Recover | retrain/republish from a known-good record; verify gates (Module 07) |
| Review | post-incident write-up: timeline, cause, what prevents recurrence |

**Principle:** every runbook names *who decides* at each step. A runbook
nobody has rehearsed is a document, not a capability — Module 15's challenge
drills yours by fault injection.

## 8. Where each idea lands in this course

| Concept | Introduced | Reused in |
|---|---|---|
| least privilege, secret-free CI | Module 12 | capstone CI (`permissions: contents: read`) |
| integrity of artifacts | Modules 08–09 | lab step 5 (sha256 before load) |
| fairness measurement | Module 09 (gate/ack) | lab step 6, capstone `fairness.json` |
| privacy of logged fields | Module 14 (what not to log) | lab step 3 |
| incident response + rollback | Module 09 | challenge runbook, capstone fault injection |

---

**Tool vs principle recap:** *pinning, scanning, hashing, and metric
thresholds* are tools you can adopt today; *least privilege, minimisation,
provenance verification, and rehearsed response* are principles that outlive
every tool. Learn the principle, then pick the tool.

---

[← Learning objectives](learning-objectives.md) · [Next: worked example →](worked-example.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*