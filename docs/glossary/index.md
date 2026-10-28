# Glossary of MLOps Terms

Plain-language definitions of every technical term the course relies on, listed
A–Z. Terms are defined **before** they are used in lessons; this page is the
canonical reference and grows as modules are written.

**How to read an entry:** **Term** — definition. *(where it is taught)*
`(see also: related term)`.

Missing a word you met in a lesson? That is a course bug — report it as an issue
so the entry gets added.

---

## A

- **API (application programming interface)** — a defined way for one program to
  ask another program for something, usually over HTTP with agreed request and
  response formats. *(M10)*
- **Artifact** — any file produced by a run: a trained model, a plot, a report.
  *(M06, M09)*
- **Autoscaling** — automatically adding or removing computing instances in
  response to load. *(M16)*

## B

- **Baseline** — a deliberately simple reference result (often a trivial model or
  last year's model) that everything else must beat. *(M05, M06)*
- **Blast radius** — how much of a system fails with one
  compromised part; the deciding test for whether a value is a secret. *(M15)*
- **Bias (ML/systematic)** — a systematic error in a model's behaviour, including
  unfairness toward a group. Distinct from statistical *bias* of an estimator. *(M15)*

## C

- **Cache** — stored intermediate results so unchanged steps need not be redone. *(M08)*
- **Canary release** — releasing to a small slice of traffic first, expanding only
  if metrics hold. *(M16)*
- **Champion / challenger** — the model currently serving (champion) versus the
  candidate being compared against it (challenger). *(M06, M14)*
- **CI/CD** — *continuous integration* (merge only if automated checks pass) and
  *continuous delivery/deployment* (automated, repeatable release). *(M12)*
- **Concept drift** — the relationship between inputs and the target changes, so
  an old model becomes wrong even though the data still "looks normal". *(M14)*
- **Container** — an isolated, repeatable running instance of an image. *(M11)*
- **Container image** — a frozen bundle of your code, runtime, and dependencies
  as a single immutable file. *(M11)*
- **Container registry** — a server that stores and serves images. *(M11)*

## D

- **DAG (directed acyclic graph)** — a set of tasks with ordered dependencies and
  no loops; the shape of every pipeline. *(M08, M13)*
- **Data contract** — an agreed specification of a dataset's schema, quality
  thresholds, and ownership. *(M04)*
- **Data drift** — the statistical distribution of inputs changes over time.
  Also called *covariate drift*. *(M14)*
- **Data lineage** — a record of where data came from and every transformation it
  passed through. *(M04, M09)*
- **Data minimisation** — collecting and keeping only the data you actually need. *(M15)*
- **Dataset card** — a short document describing a dataset: source, licence,
  intended use, and limitations. *(M04)*
- **Data validation** — automated checks that data conforms to an expected schema
  and quality rules. *(M04)*
- **Digest** — the fingerprint (hash) of an image; identical digest means
  identical bytes. *(M11)*

## E

- **Environment parity** — different machines running the same software versions,
  so results match. *(M02, M11)*
- **Experiment** — one deliberate attempt at improvement, recorded so it can be
  repeated and compared. *(M06)*
- **Experiment tracking** — automatically recording the parameters, metrics, and
  artifacts of each run. *(M06)*

## F

- **Fault injection** — breaking a system on purpose, through its own
  detection paths, to prove recovery works before an incident does it
  for you. *(M07, M17)*
- **Feature** — an input variable used by the model. *(M05)*
- **Feature engineering** — turning raw data into informative inputs. *(M05)*
- **Feature leakage** — accidentally letting information the model should not
  see at prediction time leak into training. *(M05)*
- **Feature store** — a shared service that stores features consistently for
  training and serving. Most small teams do not need one at first. *(M09)*

## G

- **Gate / quality gate** — an automated check that must pass before work
  moves to the next stage; a failing gate stops promotion, it does not warn
  about it. *(M08, M09)*
- **Git** — the distributed version-control system that records every change
  to code and documents; branches isolate work, merges integrate it. *(M02)*
- **GitHub Actions** — GitHub's built-in CI service: workflows in YAML run on
  hosted runners on events such as push or pull request. *(M12)*
- **Governance** — the documented rules for who may approve, promote, and
  retire a model, with an audit trail proving the rules were followed. *(M15)*

## H

- **Health probe** — a check that tells a platform whether a service is alive and
  ready to receive traffic. *(M16)*
- **Hidden feedback loop** — a model's own outputs change the future data it
  trains on, in ways nobody documented. *(M03)*

## I

- **IaaS / PaaS / serverless** — cloud levels: renting machines / renting a
  platform / paying per function call. *(M16)*
- **Idempotency** — doing the same operation twice gives the same end state as
  doing it once, so re-runs are safe. *(M08, M13)*
- **Image** — the built, immutable package a container runs from. *(M11)*
- **Incident response** — the rehearsed loop detect → contain → assess →
  notify → recover → review, with named decision owners. *(M15)*
- **Inference** — using a trained model to make predictions on new data. *(M01)*
- **Infrastructure as code (IaC)** — describing infrastructure in versioned text
  files instead of clicking a console. *(M16)*
- **Integration test** — a test that exercises several components together,
  ideally the whole pipeline end-to-end. *(M07)*

## K

- **Kernel (Python)** — the interpreter executing your notebook or script;
  notebooks silently keep using an old kernel until you switch it. *(M02)*
- **Kubernetes (K8s)** — an open-source platform that runs containers across a
  cluster: scheduling, scaling, restarts, and rollouts. Optional in this
  course. *(M16)*

## L

- **Least privilege** — every actor holds the smallest set of permissions
  its job needs, for the shortest time it needs them. *(M12, M15)*
- **Latency vs. throughput** — how long one request takes vs. how many requests
  you can serve per second. *(M10)*
- **Lineage** — see *data lineage*; also *model lineage* (which data, code, and
  run produced a model). *(M09)*
- **Lock file** — a file recording the exact versions of every dependency you
  installed, so others can rebuild the environment. *(M02)*

## M

- **Metric** — a number you compute to judge a run (accuracy, latency, cost). *(M06)*
- **Model artifact** — the saved weights plus everything needed to use them. *(M09)*
- **Model card** — a standard document describing a model's intended use,
  evaluation, limitations, and fairness. *(M09, M15)*
- **Model registry** — a catalog of model versions and their stages
  (Staging, Production, Archived). *(M09)*
- **Model serving** — making a model available to callers at runtime. *(M10)*

## O

- **Orchestrator** — software that schedules, retries, and monitors pipeline
  tasks. *(M13)*
- **Overfitting** — learning the training data's noise so well that new data
  performs worse. *(M05)*

## P

- **Parameter** — a knob you set before training (learning rate, depth). *(M06)*
- **p95 latency** — 95% of requests are served at or below this time; the tail
  that users notice. *(M10)*
- **Pipeline** — an ordered, repeatable set of steps from raw data to evaluation. *(M05)*
- **PII (personally identifiable information)** — data that identifies a person:
  names, emails, ID numbers. Handle with care; never log it casually. *(M15)*
- **Pod** — the smallest unit Kubernetes schedules: one or more containers
  sharing a network, treated as disposable. *(M16)*
- **Post-incident review** — a blameless written account of an incident:
  timeline, cause, and preventive actions with owners. *(M15, M17)*
- **Preprocessing** — cleaning, encoding, and scaling inputs before training. *(M05)*
- **Production readiness review (PRR)** — a checklist pass over a
  candidate system that files issues with evidence instead of demoing;
  ends in a go/no-go. *(M17)*
- **Pseudonymisation** — replacing direct identifiers with a stable
  reference (for example a session ID); reversible, so still personal
  data, but far safer in logs. *(M15)*
- **Promotion** — deliberately moving a model from Staging to Production. *(M09)*

## Q

- **Quality gate** — see *gate* *(G)*; in this course, a set of numeric model
  criteria a candidate must meet before release. *(M08, M09)*

## R

- **Readiness vs. liveness probe** — readiness gates *traffic* (pull a
  bad pod from the Service); liveness gates *restarting* a wedged
  container. They must not be the same check by default. *(M16)*
- **Request vs. limit (Kubernetes)** — the reservation the scheduler
  honours (what you pay for) versus the ceiling (CPU throttles at it;
  memory is OOM-killed past it). *(M16)*
- **Replica** — one running copy of a service; more replicas mean more capacity. *(M16)*
- **Reproducibility** — rerunning an experiment and getting the same result from
  the same inputs, code, and seed. *(M02, M05)*
- **Retraining trigger** — a rule (often drift-based) that starts a new training
  run automatically. *(M14)*
- **Risk register** — named risks with likelihood, impact, mitigation,
  owner, and the *accepted* residue; governance as a living document. *(M15)*
- **Rolling update** — replacing replicas gradually (surge, health-check,
  retire) so capacity never dips below the requested count. *(M16)*
- **Rollback** — returning to a previously working version after a problem. *(M09, M12, M16)*
- **Run** — one execution of a training job, recorded in the tracker. *(M06)*

## S

- **Schema** — the expected structure of data: columns, types, ranges. *(M04)*
- **Secret** — a credential (API key, password) that must never be committed to
  code or logs. *(M12, M15)*
- **Serving** — see *model serving*.
- **Supply chain (software/ML)** — the dependencies, base images, data
  files, and model artifacts you trust; verify integrity, provenance,
  and freshness of each. *(M15)*
- **SLA / SLO / SLI** — service level *agreement* (promise), *objective* (target),
  and *indicator* (the measured number). *(M16)*

## T

- **Technical debt** — the future cost of shortcuts taken now: entanglement,
  undeclared data dependencies, untested code, configuration drift. *(M03)*
- **Test fixture** — prepared data or state a test runs against. *(M07)*
- **Throughput** — see *latency vs. throughput*.
- **Training** — fitting a model to data so it can make predictions. *(M01)*
- **Threat model** — a one-page inventory of what you protect, from whom,
  through which doors, and the control per threat. *(M15)*
- **Train/serve skew** — training data prepared differently from serving data,
  so production performance silently drops. *(M04)*

## U

- **Unit test** — a test of one small piece of logic in isolation. *(M07)*
- **Unsafe deserialization** — loading an object from untrusted bytes (for example
  Python `pickle`) which can execute arbitrary code. *(M15)*

## V

- **Validation gate** — an automated check that blocks a change (a merge, a
  promotion) when a threshold is breached. *(M07, M12)*
- **Virtual environment** — an isolated per-project Python installation so
  projects do not fight over package versions. *(M02)*

## W

- **Workflow** — the automation that runs your pipeline: triggers, retries,
  schedules, and logs. *(M12, M13)*

---

*This glossary grows with the course. Missing terms are reported as repository
issues. Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*
