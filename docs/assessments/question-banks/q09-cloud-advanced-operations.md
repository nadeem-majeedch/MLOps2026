# Question bank 09 — Cloud and advanced operations

**Covers:** Modules [16 — Cloud, Kubernetes, scaling, reliability](../../modules/16-cloud-kubernetes-scaling/index.md)
and [17 — Capstone](../../modules/17-capstone/index.md).
**Format:** 10 questions — multiple choice, short answer, debugging, architecture, scenario.
**Suggested check:** 7/10, with **O5** and **O10** correct.

> *Attempt first, then read the
> [reference solutions](../keys/question-banks-KEY.md).*

---

## Part A — Multiple choice

**O1.** In Kubernetes, a `Deployment` manages:

- (a) DNS records
- (b) ReplicaSets and thus the desired state of pod replicas (with rollouts)
- (c) Persistent volumes
- (d) Container images only

**O2.** A `Service` exists to:

- (a) Build images
- (b) Give pods a stable virtual IP/DNS so traffic keeps reaching healthy
  replicas as they come and go
- (c) Store secrets
- (d) Schedule jobs

**O3.** Readiness probes matter because:

- (a) They keep containers alive forever
- (b) They take a pod out of service until it can actually answer — the model
  may still be loading
- (c) They reduce image size
- (d) They encrypt traffic

**O4.** Horizontal pod autoscaling responds to:

- (a) Lines of code
- (b) Observed load metrics (CPU, queue depth, …) against a target
- (c) Git commits
- (d) Model accuracy

## Part B — Short answer

**O5.** Define *rolling update* and *rollback* for deployments, and explain
why "surge + unavailable budget" settings are an availability decision, not a
tuning curiosity.

**O6.** Secrets in Kubernetes: how should they reach the container, and what
must never happen (three concrete "nevers")?

**O7.** What is the difference between scaling *out* and scaling *up* for an
inference service, and which one usually fails first for ML workloads — and
why (memory? GPU? batch size?)?

## Part C — Debugging

**O8.** Symptoms on a cluster; match to cause and fix:

1. Pods `CrashLoopBackOff`
2. Pods `Running` but requests time out from outside
3. Requests succeed, then 503s during a deploy
4. Pod evicted under memory pressure
5. Config change had no effect

…causes include: missing/liveness-failing probe with a fatal startup error,
no `Service`/ingress or wrong port, no readiness probe during rollout,
container exceeds limits because the model loads into RAM, editing a
ConfigMap without restarting the pods that mount it.

## Part D — Architecture

**O9.** Draw a production-grade serving architecture: ingress → API pods →
model store, with autoscaling, probes, config, secrets, and monitoring.
Annotate each element with the Kubernetes object that implements it — and mark
which parts you would deliberately *not* build on day one.

## Part E — Scenario

**O10.** A stakeholder asks you to "just move it to the cloud and add
Kubernetes". Give the decision framework: what you would confirm first
(traffic, team, SLA, budget), the smallest sensible step, the cost/security
implications to disclose, and the specific signal that justifies
orchestration. State clearly which parts of your answer are free/local and
which require a paid account.

---

**Next:** [reference solutions](../keys/question-banks-KEY.md) (bank 09) —
then take the [final review & exam-preparation guide](../final-review.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../../about/index.md).*
