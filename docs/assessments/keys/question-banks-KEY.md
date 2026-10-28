# Reference solutions — question banks 01–09

> 🔑 **REFERENCE SOLUTIONS.** Attempt the relevant
> [question bank](../question-banks/index.md) **first**, in writing. Reading a
> key you have not competed against produces recognition, not knowledge — and
> you will misremember recognition as mastery later.
>
> **Why the explanations matter more than the letters:** the multiple-choice
> answer is a fact; the explanation is the reasoning you will need when the
> same concept appears in a new shape inside a lab or the capstone. Where a
> scenario has more than one defensible answer, the key says so and gives the
> conditions under which each holds.

Format: **Part A** — letter + why (and why the others fail); **Part B** — model
answer outline; **Part C** — the defects to find; **Part D** — what a good
diagram must contain; **Part E** — the reasoning chain a strong response shows.

---

## Bank 01 — MLOps fundamentals

**F1 → (b).** Lineage/versioning is the ability to answer "what produced this
artefact"; nothing here says the model is inaccurate (a) or slow (d).
(c) is a modelling concern, not the failure described.

**F2 → (b).** Data change changes behaviour with zero code change — this is
why monitoring exists. (a) fails because ML correctness is statistical, not
boolean; (c) is impossible in general (held-out data is a sample, not proof);
(d) inverts the lesson.

**F3 → (a).** Definition → data → experiments → evaluation → deploy → monitor →
retrain. The others put evaluation before data exists, or tracking before
anything to track.

**F4 → (b).** Uptime/latency measure the *software*. A model can degrade with
perfect infrastructure. (c) may be true somewhere but isn't the *reason*;
(a) is cynicism, not analysis; (d) is false.

**F5.** *Training* — fitting model parameters from data. *Inference* — using
the fitted model to score new inputs. *Baseline* — a deliberately simple
reference system (majority class, simple model) whose numbers every "good"
result must beat, otherwise "good" has no meaning.

**F6 (any four).** (i) Data, not just code, determines behaviour → version and
validate data. (ii) Correctness is statistical → evaluate with metrics and
uncertainty, not pass/fail. (iii) Degradation happens after deployment →
monitor. (iv) Retraining is recurring, not one-off → automate pipelines.
(v) Failures are often silent → alert on quality, not only crashes.

**F7 (any three of).** Seed & shuffle order → fix seed, sort file reads.
Environment drift → pin dependencies (lock file). Data drift → hash/record the
dataset, contract-check it. Hidden state/notebook cells → scripted pipeline,
fresh-process runs. Non-deterministic kernels → set deterministic flags or
record library versions/hardware.

**F8 — five problems, each with a location.** (1) Two notebooks as the source
of truth → replace with `src/` modules + one entry point; notebooks become
exploration only. (2) No data versioning/provenance → `data/` + generator or
DVC-style tracking, documented in README. (3) Unversioned binary `model.pkl`
→ artefact store with hash + registry (Module 09). (4) Results only in
`results.xlsx` → tracked metrics (MLflow-style) or `metrics.json` in CI.
(5) Import from outside the repo (`../shared/utils.py`) → vendor the module
inside the project, declare it in packaging. (6, bonus) README tells readers
to run a notebook → one-command reproduction script.

**F9 — a good diagram answers the question directly:** code → Git commit id
stored with the run; data → dataset version/hash stored with the run;
parameters → run parameters; all three bound to a *run record*, the run's
artefact referenced by the *registry entry* that deployment serves. Query the
registry entry → run → commit + data hash + params. Any component missing
(c.e. no run store) is the gap you must name.

**F10 — strong version of the argument:** infrastructure problems (build,
deploy, scale, monitor availability) are indeed shared with DevOps, and much
of MLOps is disciplined application of those practices. **Refutation with two
course examples:** (1) *Data and models version like nothing else* — a
byte-identical redeploy still yields different behaviour if the dataset
moved; Git+CI alone doesn't cover it (Module 04/05). (2) *Quality gates are
statistical* — CI for software checks correctness; an ML gate must refuse a
release on metric floors, drift and fairness (Labs 08/15), and a green build
says nothing about model quality (Module 14's drift-without-degradation case).

---

## Bank 02 — Reproducibility and data versioning

**R1 → (b).** Only (b) enumerates the plausible causes; (a) is incomplete,
(c)/(d) are far too narrow.

**R2 → (b).** It records versions *of that environment*, nothing more: not
platform, not transitive resolution guarantees across time, not security, not
that the code runs.

**R3 → (b).** Git is for text; large binaries bloat clones forever. A
generator/downloader + checksum gives reproducibility without the bytes. (c)
has no provenance; (d) makes the experiment unreproducible.

**R4 → (b).** A type change in a column is a contract violation — the schema
promised numbers. AUC/threshold/precision-recall are modelling choices.

**R5.** *Versioning* = identifying **which snapshot** of the data was used
(content hash/record id, e.g. DVC-style with a remote, or a committed small
CSV + hash). *Lineage* = the **chain of transformations** from source to
dataset to model (which extract, which joins, which cleaning steps, which
run). Versioning answers "what exactly"; lineage answers "where did it come
from and what happened to it". Course mechanisms: `make_data.py --check`
hashes and `manifest.json`/`registry` records as examples.

**R6.** `glob` order is filesystem-dependent → row order differs → with any
shuffled/stochastic training or split, results differ. Fixes: `sorted()`
explicitly (and/or read one file by exact name), plus set/fix the seed *and*
make the split explicit rather than order-dependent.

**R7 (four of).** Dependency versions (lock file); Python version; data
version/hash; row ordering/split logic; library defaults that changed
(framework version); hardware/kernel nondeterminism; any nondeterministic
preprocessing (e.g. `sample(frac=1)` without seed).

**R8 — three defects.** (1) Unsorted `glob` → nondeterministic row order.
(2) Unseeded shuffle → different order every run (and it happens *after*
reading, compounding (1)). (3) `np.random.seed(42)` at the end → seeds
nothing that ran before it. (4, bonus) appending to `results.txt` → results
interleave across runs and get misread as one run's.

**F9/R9 diagram checklist.** Raw extract → **schema/quality gate** (must
*block*, not warn) → versioned dataset (id + hash written) → training run
referencing that id → metrics/artefacts. The gate sits *before* any version
is minted; a failing gate must prevent downstream stages, and the version id
must be recorded with the run.

**R10 — ordered diagnosis.** (1) Confirm the claim: run evaluation on both
snapshots, same script. (2) Compare *data*: hash the CSV now vs last month
(`sha256sum`) — different hash ⇒ data changed; then diff summary statistics
to see what moved. (3) Compare *code*: `git status/log` for changes since the
last good run. (4) Compare *environment*: `pip freeze` diff / interpreter
version. (5) Compare *seed & config*: config diff. Conclusion rule: hash
mismatch with identical code+env ⇒ data; identical data+code but different
env ⇒ environment; all identical ⇒ hidden state/nondeterminism (re-run twice
to test). Each step names a command and what its output would prove.

---

## Bank 03 — Experiment tracking and evaluation

**E1 → (b).** A metric without parameters/code/data context is a number you
cannot reproduce or defend; (c) and (d) require exactly what wasn't recorded.

**E2 → (c).** Pre-declared rule + baseline + held-out data avoids both
cherry-picking and test-set mining. (a) is maximising noise; (b) and (d) are
nonsense.

**E3 → (b).** The registry's job is accountability: what, which run produced
it, how it performed, who promoted it and when. The rest are fragments.

**E4 → (b).** Distribution of *inputs* differing from training. (a) is a
retrain event; (c) irrelevant; (d) a training hyperparameter.

**E5.** Validation tunes choices; test estimates final generalisation. Tuning
against the test set for weeks makes it part of the training loop → the
reported score is optimistically biased and no longer an independent
estimate; you are measuring "how well we fit the test set".

**E6.** Accuracy rewards predicting the majority class (98% accuracy by
always saying "no"). Report precision & recall (or PR-AUC) for the positive
class, and state the trade-off: raising recall (catch more positives) brings
more false positives; where to sit depends on the cost of each error.

**E7.** An artefact stores the *actual bytes* of the model (plus
preprocessing, metadata) — metrics are descriptions, artefacts are the thing
served. Promotion without a reproducible artefact means you can score a
number you can no longer deploy.

**E8 — two errors.** (1) *Different data versions* (v3 vs v4) → not a model
comparison at all; fix: same dataset version for both runs. (2) *Different
split strategies* (random vs temporal) → different difficulty and, for time
data, temporal leakage risk; fix: one declared split policy (and for time
series, a time-based split) applied to both. (bonus: also compare on one
frozen test set at the end.)

**E9 — diagram checklist.** Training run → metrics + artefact (hash computed
here) → staged registry version (hash recorded) → gate/quality checks →
promotion changes the *pointer* the service resolves (hash re-verified at
load); rollback = re-pointing the pointer to the previous version's bytes,
not retraining.

**E10 — strong answers pick a side and defend it with the business goal.**
*Against promotion:* the goal is catching at-risk cases; worse recall fails
the stated goal regardless of AUC, and 3× latency may break the use case.
*For promotion, conditional:* only if you show recall on the actual operating
threshold, latency fits the SLO, and you canary it with a rollback trigger.
Required elements either way: state the decision metric tied to the goal
(recall/PR-AUC at threshold), show both numbers on the same held-out set,
attach conditions (canary %, latency SLO, auto-rollback threshold), and name
the flip-condition.

---

## Bank 04 — Testing and automation

**T1 → (b).** Leakage is a *feature/label relationship* bug; only a test that
inspects that relationship can catch it. Existence/row-count tests pass on
leaky data.

**T2 → (b).** The runner's job is dependency resolution: order from the DAG,
and refuse (fail) when an input is missing rather than racing (a) or
retrying (c). (d) hides the bug.

**T3 → (b).** A gate exists to *prevent* releases: fail loudly, name the
criterion and value. Warning (a) lets bad artefacts through; (c) destroys
evidence; (d) inverts the gate.

**T4 → (b).** A threshold on a fixture with known signal catches real
regressions; the others pass regardless of model quality.

**T5.** *Unit* — a pure function in isolation (e.g. `psi()` on a tiny array;
config validation rejecting `test_size: 1.5`). *Data* — assertions on the
dataset/schema (column presence, ranges, duplicates — Lab 03's checker).
*Regression* — "behaviour that used to work still works" (characterisation
test in Lab 11; gate refusing the defective candidate in Lab 15; leakage test
in Lab 07 pins preprocessing fitting on train only).

**T6.** Fail loudly = raise/exit non-zero with a message naming stage, input
and reason. The three failure modes: swallowing exceptions (`except: pass`),
returning partial results as if fine, and defaulting (missing input → empty
frame → downstream trains on nothing).

**T7.** Test the transformer directly: fit on a small hand-written frame with
known values, assert exact transformed output (scaling of a known number,
one-hot columns present, unknown category handled), assert `fit` was called
only on the training portion (leakage test). No model needed.

**T8.** It passes because fitting on all data makes the score *high*, and the
assertion only rejects *near-perfect* scores — leakage that lands at 0.95
passes happily, and the test's threshold is arbitrary. Rewrite to test the
*procedure*: fit the full preprocessing pipeline **on the training split
only**, transform the held-out split with it, and assert that (i) the
preprocessor's fitted state comes from train rows alone (e.g. compare
`mean_` to train-only mean) and (ii) an intentionally leaky variant — a
column equal to the target or fit-on-all — **fails** a test that flags
feature/label correlation or fit-on-all fitting.

**T9 — diagram checklist.** Five stages with edges labelled by artefacts
(csv/parquet → validated dataset → features → model → metrics → registry
entry), gate 1 after validation (data refuses), gate 2 after evaluate (metrics
refuse), plus the failure path: stage fails → downstream BLOCKED, manifest
records it.

**T10 — three plausible explanations with catchers.** (1) Tests didn't cover
the changed code path → add a test at the boundary (schema/contract test).
(2) The suite regenerated/retrained the artefact it was meant to check →
integrity test (hash vs recorded hash — Lab 20's lesson). (3) The gate wasn't
wired into the pipeline/CI (tested locally only, skipped on failure) →
CI step that runs the gate and blocks promotion (Labs 08/14/15).

## Bank 05 — APIs and containers

**A1 → (b).** The request violates the documented contract; 422 names the
field so the caller can fix it. (a) fabricates a result from garbage input;
(c) blames the client's bug on the server; (d) means "not found".

**A2 → (a) is the *myth*; the correct choice is (b).** Per-call loading adds
latency and opens file handles continuously; load once at import/startup (as
`service/app.py` does). Determinism comes from loading the *same* bytes once,
not from reloading.

**A3 → (b).** Docker caches layers: an unchanged instruction reuses its
layer. Installing deps before copying code means editing code doesn't
re-install packages. The other options are side effects at best.

**A4 → (a).** Exec form runs Python directly as PID 1, so `docker stop`'s
SIGTERM reaches it and it can shut down cleanly. Shell form puts a shell in
between that swallows the signal (container dies only after the grace period
with SIGKILL).

**A5.** Inside the container, `127.0.0.1` is *the container itself*. Port
publishing (`-p`) forwards host traffic into the container's network
namespace, so the app must listen on `0.0.0.0` (all interfaces) to receive
it. Symptom: app works with `curl` *inside* the container, times out from the
host.

**A6.** Batch payload: `{"records": [...]}` with `min_length=1`,
`max_length` cap (e.g. 1000), per-record bounds/types in the schema. Errors:
422 with each offending field named (never 500 for client mistakes). Response
must carry `model_version`, the `threshold` used, and per-record probability
+ flag — so the caller can audit *which* model produced a number and under
what decision rule.

**A7.** The build context is the set of files sent to the builder;
`.dockerignore` excludes paths from it. Security: secrets or stray state can
never be copied into an image if they aren't in the context; also smaller
contexts = faster, more cacheable builds.

**A8 — matches.** 1 → app bound to loopback inside the container (fix:
`ENV HOST=0.0.0.0`). 2 → no `CMD`/entrypoint, nothing keeps it running (fix:
add exec-form `CMD`). 3 → model loaded per request (fix: load at startup).
4 → dependency layer ordered after `COPY` of code (fix: install deps first).
5 → fat base image + whole repo as context + dev tools (fix: slim pinned
base, `.dockerignore`, multi-stage).

**A9 — diagram checklist.** client → ingress/port → FastAPI route → Pydantic
validation (422 branch shown) → DataFrame in declared feature order → model
loaded once at import (arrow from startup, not from the request path) →
prediction + version/threshold in response; logs written per request
(prediction, version, timestamp); 503 path when no model.

**A10 — two causes.** (1) The image doesn't contain the artefact
(`.dockerignore` excluded `artifacts/`, or `COPY` missed it) — confirm with
`docker run --rm -it <img> ls -R /app`; fix the COPY/ignore file. (2) The
service resolves a *registry* path that exists only on the host (bind-mounted
in dev, absent in the image) — check `/health`'s `model_source` and bake the
artefact or mount it. Both show as `model_version: none` + 503, which is the
service doing its job: refusing to pretend.

## Bank 06 — CI/CD and orchestration

**C1 → (b).** Secrets live in platform settings, injected at run time, masked
in logs. Anything committed (a, c, d) is compromised the moment the repo is
read — rotation, not deletion, would then be required.

**C2 → (b).** Least privilege: read-only checkout is what lint/test jobs need.
Broader scopes turn every CI compromise into a write/release compromise.

**C3 → (b).** Pinned file + cache: reproducible *and* fast. (a) is a
supply-chain lottery; (c)/(d) make runs depend on whoever configured the
machine.

**C4 → (b).** Total-cost argument: an orchestrator to be worth it needs
multiple steps, dependencies, retries/backfills or team sharing. The other
options misstate facts about orchestrators.

**C5.** *Retries* — automatic re-attempts of a failed step (with backoff);
prevents transient blips (network, 5xx) from becoming incidents. *Backfills* —
re-running a schedule for past intervals after a fix; prevents "last Tuesday
was silently wrong forever". *Idempotency* — re-running a step produces the
same result as running it once; prevents duplicates/corruption when retries or
backfills overlap (e.g. write to a date-partitioned path, not append-blind).

**C6. Include:** lint, unit/data tests, a lightweight contract check, a
deterministic metric-floor evaluation on a small fixture, and an artefact
report. **Exclude:** long hyperparameter searches, GPU training, live external
APIs, and anything nondeterministic without a seed — CI must be fast, green or
red, and identical when re-run.

**C7.** The failed run shows job → step → command; the developer reads the
first failing line of that step first (not the last error in the log),
compares with the local equivalent command, and uses uploaded artefacts
(reports, coverage, logs) that are published `if: always()` precisely so the
evidence survives the failure.

**C8 — three defects.** (1) No version pin/`==` in `requirements.txt` →
different versions on the runner. (2) `src/train.py` depends on files or cwd
not present in CI ("works on the author's machine") → declare working
directory and ship all inputs. (3) Secret inline in YAML (committed, and
printed if echoed) → move to platform secrets, reference
`${{ secrets.API_KEY }}`, and skip/mocked that test if no secret exists. A
fourth: no pinned action versions (`uses:` without a tag/SHA).

**C9 — diagram checklist.** `on: push/pull_request` → jobs `lint`, `tests`,
`ml-validation` in parallel; pip cache keyed on the requirements file; each
job uploads reports as artefacts even on failure; a release/gate job downstream
of all three decides ship; `permissions: contents: read` annotated.

**C10 — decisions.** (i) Nightly single retrain → **cron/script**: one simple
job, result visible in a file; add retries inline. (ii) 12-step cross-team DAG
with backfills → **orchestrator**: dependency graph, retries, backfills, run
history and ownership need a scheduler, not a crontab. (iii) One-off
experiment → **neither**: a notebook/script in version control. *Signal to
move up:* steps ≥ ~5 with dependencies, multiple owners, need for backfill or
SLA-driven reruns; signal to move up again: multi-team platform requirements
that a shared scheduler can't express.

## Bank 07 — Monitoring and drift

**M1 → (b).** You need inputs (to measure drift), the prediction (to audit),
model version (to attribute), time (to window), and the realised outcome later
(to measure performance). (c) is a privacy violation; (a)/(d) make both
analyses impossible.

**M2 → (b).** PSI compares two distributions binned the same way (typically
reference deciles). Labels, speed and parameters are other measurements.

**M3 → (a).** Drift needs only inputs — measurable immediately. Performance
degradation needs labels — impossible until they arrive.

**M4 → (b).** Thresholds are decisions: they must be justified, tied to a
response, and tuned on data. Defaults are unexplained; guessing maximises
alert fatigue or blindness.

**M5.** **No.** Drift measures how *inputs* are distributed; accuracy/AUC
measure whether the model still ranks/predicts correctly. Inputs can move and
the model remain fine (the course's own case: PSI 0.86 strong on features
while AUC was *slightly above* reference). The supporting measurement is
performance on **labelled** recent data against the recorded floor — drift
only *prompts* that check.

**M6.** Drift × degradation → investigate root cause; consider rollback
first if live metrics are bad, retrain only with a diagnosis. Drift × no
degradation → monitor; note flip-conditions. No drift × degradation → data
isn't the suspect: labels, bugs, leakage, upstream code. Neither → continue
with scheduled checks. Human decides in both degradation cells.

**M7.** The reference is the recorded window the comparison is made against;
record its date range because seasonal/periodic data legitimately shifts —
comparing against an unlabelled "normal" can manufacture drift. Without dates
you cannot tell seasonality from real drift, and you cannot reproduce the
comparison later.

**M8 — two explanations.** *Technical:* the reference window was built from
inverted/contaminated data (or bins miscomputed), so the comparison was
wrong; verify by recomputing PSI by hand from the stored reference and by
comparing summary stats of both windows. *Process:* the monitor was tuned
until it went quiet — thresholds raised or checks skipped without review;
verify via change history of the monitoring config (who changed what, when)
and by replaying the original data through the current thresholds.

**M9 — diagram checklist.** serving → prediction log (features + prediction +
version + time) → drift check → (branch A) labels arrive → performance check
vs floor → decision matrix → human decision: retrain | monitor | roll back →
affects deployment. Human-in-the-loop marked at (1) the decision cell and
(2) any threshold/config change.

**M10 — the reasoning chain (this is the whole module).** Evidence checked:
PSI 0.31 (inputs moved), mean AUC 0.7798 → 0.7302 (**measured degradation**),
6 alerts, p95 38 → 118 ms, errors 0.2% → 2.6%, v1 known-good (21 days, 0
alerts). **Decision: roll back to v1 first** — users are feeling latency and
errors *now*, and the live AUC confirms degradation (this is not a
chart-feeling). Retraining comes after diagnosis (what moved in
`monthly_charges`?). Flip-conditions: if you instead ride it out, you must
define latency/error SLOs, a canary with automatic rollback, and a deadline —
and say which numbers would trigger the rollback anyway. An answer that says
"drift detected → retrain" without the performance column fails the question.

## Bank 08 — Security and governance

**S1 → (b).** Removing the file doesn't un-leak the credential: history (and
caches/forks) still contain it, so **rotation** is mandatory; then decide on
history purge vs acceptance, then add scanning to prevent recurrence. (d) only
prevents *future* tracking.

**S2 → (b).** Pickle/joblib deserialize by *executing* — a crafted file runs
code at load time. That's why artefacts must come from trusted, hashed
sources (Lab 19/20's integrity checks exist for this reason).

**S3 → (b).** Narrowest scope that completes the job. Write-all (a) turns CI
into a privilege-escalation path; (c) defaults to whatever the platform
allows; (d) over-broad credentials are the classic leak.

**S4 → (b).** Measure, document, choose a policy deliberately, get it
approved. (c) is often impossible/unfair in itself; (d) is "hide the
measurement" — the disparity remains, now unmeasurable.

**S5.** *Lineage* = the chain dataset → run → artefact → version →
deployment, recorded as hashes/ids in run and registry records; answers
"where did this model come from?" *Auditability* = append-only records of
who did what when (promotions, threshold changes, overrides with reasons);
answers "who is accountable for this state?" Both are files/rows you can
read, not policies on a wall.

**S6.** Raw PII in logs = confidentiality breach surface (logs are copied,
shipped, broadly read) and is often unlawful; a pseudonymous id (hash/salted
token) still joins predictions to outcomes for drift/performance analysis
while not identifying the person. Risk ↓, monitoring usefulness mostly
preserved — provided the mapping is stored separately, access-controlled.

**S7 (any four).** Assets worth protecting (model, data, keys, API);
adversaries & their goals; entry points (unauthenticated endpoint, artefact
ingestion, dependency supply chain); controls per boundary (auth, validation,
hash verification, least privilege); what happens when one fails (incident
response, rotation, rollback).

**S8 — classification + fixes.** (1) Hard-coded key → *confidentiality*;
move to environment/secret store, rotate the exposed value, add scanning.
(2) Email in logs → *confidentiality/privacy*; log a pseudonymous id, drop
the address, assert absence in tests. (3) No auth on `/predict` →
*confidentiality + integrity* (anyone can use/abuse the model); bearer token
or network-level restriction + rate limiting. (4) `pickle.load` from an
untrusted path → *integrity/RCE*; only load hashed, registry-verified
artefacts (prefer non-executing formats where possible). (5) Group-dependent
threshold → *fairness*; single threshold, justify it, and test equalised
behaviour across groups (Module 15).

**S9 — diagram + boundaries.** client →|TLS/auth + validation| API →|least
privilege + integrity check| model store; API →|secret injection, never
baked| secret store; API →|egress control + pseudonymisation| monitoring.
Each `|` is a boundary with a named check; anything crossing it unauthenticated
is a finding.

**S10 — model verdict paragraph.** *"Verdict <date> — conditionally safe, not
unconditionally approved.* Scanner-clean (evidence: exit 0) covers only its
rules. Blocking findings: missing intended-use limits in the model card
(medium — misuse risk; fix before release), container runs as root (high —
blast radius; fix with a non-root `USER` + rebuilt image). Accepted for now:
no dataset id recorded for the shipped model (owner: <name>, fix by <date>) —
accepted only because the model is internal and the artefact hash is tracked.
Approval is conditional on the two blocking fixes being verified by re-running
the review; re-review triggers: new endpoints, new data category, model
version change."

## Bank 09 — Cloud and advanced operations

**O1 → (b).** A Deployment owns ReplicaSets and therefore pod replicas,
including rollout strategy and rollback of the pod template. DNS is a Service
/ CoreDNS concern; volumes are PersistentVolume claims; pulls are node/image
concerns.

**O2 → (b).** A Service is a stable virtual IP + DNS name in front of
ephemeral pods, so clients keep one address while pods come and go.

**O3 → (b).** Readiness gates traffic: a pod that hasn't finished loading the
model answers "not ready" and receives no requests — exactly the window where
"Running" ≠ "working". Liveness restarts a wedged container; they are
different probes for different failures.

**O4 → (b).** Autoscaling reacts to observed load metrics against a target
(CPU/queue depth/custom metrics). The rest aren't runtime signals.

**O5.** *Rolling update* = gradually replace old pods with new ones under a
strategy (surge count, max unavailable) so capacity and availability hold
during deploy. *Rollback* = reverting the Deployment to a previous pod
template/revision so traffic returns to known-good images. The surge/unavailable
settings are availability decisions: they encode how much capacity you can
spare and how many failures you tolerate mid-deploy — mis-set them and a
deploy becomes an outage, regardless of the image being "better".

**O6.** Reach the container as a mounted volume or via the platform's secret
injection at pod start. Nevers: never bake secrets into images/layers; never
put them in env files committed to Git or in CLI args (visible in process
listings); never print them in logs or error messages; never share one broad
secret where per-service scoped credentials exist.

**O7.** *Scale out* = more pod instances sharing load; *scale up* = bigger
instances (more CPU/RAM/GPU). For ML, scale-out often hits a wall first
because each replica must load the full model (memory × replicas), GPU
capacity is scarce/affordable only in chunks, and large models may not fit
"small" replicas at all — plus cold-start (model load) makes aggressive
scaling slow. Then batching/throughput tuning usually beats adding pods.

**O8 — matches.** 1 → fatal startup error or failing liveness → read the
container logs (`kubectl logs`) and fix the cause; don't raise retries. 2 →
no Service/ingress or wrong port/selector → check `kubectl get svc`, port
names and targetPort. 3 → no readiness probe, so new pods take traffic before
the model loads → add readiness on `/health`. 4 → model loads into RAM and
exceeds the memory limit → set realistic limits/requests or a smaller model.
5 → ConfigMap edited but mounted env vars are fixed at pod start → restart
the pods (or use a rollout annotation that triggers one).

**O9 — diagram checklist.** ingress/controller → Service → Deployment pods
(probes annotated) → model store (mounted or fetched, integrity-checked);
ConfigMap for non-secrets, Secret for secrets (never in the image);
horizontal PodAutoscaler attached to the Deployment; monitoring scrapes
pods. Day-one annotations: "start without autoscaling / without a service
mesh / single region" — knowing what *not* to build is part of the answer.

**O10 — the decision framework.** First confirm: real traffic (QPS,
latency budget), team operations capacity, SLA needs, and budget — plus
whether the workload even needs it (your course project runs on a laptop).
Smallest sensible step: containerise + a managed container service or a
single-node deployment, not Kubernetes. Disclose: cost model (compute,
egress, GPUs), security shared-responsibility, and that cloud steps need a
paid account (label them optional, as the course does). Signal to move to
orchestration: multiple services, dependency DAGs, elastic load, or team-scale
operations that a single box can't express. Free/local vs paid must be split
explicitly in the answer — that split is itself part of the marks.

---

*🔑 End of reference solutions. Every explanation above is modelled on what a
strong submission contains — if your reasoning differs but the evidence
chain holds, yours may be better: say so in your write-up. Attempt first,
always.*

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../../about/index.md).*
