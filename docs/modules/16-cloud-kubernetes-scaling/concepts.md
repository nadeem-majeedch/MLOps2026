# Concepts — Module 16

This module teaches **cloud-independent concepts first** and the platform
second. Kubernetes is used because it is the industry's shared vocabulary —
not because it is the right tool for a student laptop service (it usually
is not; §9 says when it isn't). **Tool** vs **Principle** marks apply
throughout.

---

## 1. Cloud models, before any vendor name

**Cloud** = someone else's computer, rented, with an API. The rent tiers
differ in *who runs what*:

| Model | You manage | They manage | Course analogue |
|---|---|---|---|
| **IaaS** (virtual machines) | OS, runtime, scaling | hardware, network, VM | your laptop, rented |
| **PaaS** (containers/apps) | code + container | runtime, scaling, patching | GitHub Pages hosting the site |
| **Serverless** (functions) | code only | everything below, per-invocation | — (billed per call) |
| **Managed ML** (SageMaker-style) | model + data | training, serving, lineage UI | MLflow *yourself* vs tracking as a service |

**Principles that survive any vendor** (these are what the syllabus means by
"cloud-independent"):

- **Region** = a geographic area; **zone** = an isolated datacentre inside
  it. Distribute across zones so one power event isn't your outage.
- **Managed vs self-run**: pay money, lose control and portability; run it
  yourself, gain control, pay operations. There is no free option — only
  where the invoice lands.
- **Everything is an API**: if you can't recreate it from a file, you can't
  reproduce your own infrastructure (that's IaC, §8).

**Mapping this course to managed equivalents** (LO 16.1 — produce your own
version):

| What you built (free, local) | Managed equivalent | What you'd trade |
|---|---|---|
| `examples/churn/` + git | hosted git + CI minutes | convenience for lock-in |
| MLflow local tracking | managed experiment tracking | cost, data leaves your disk |
| `release.py` registry | managed model registry | workflow rigidity |
| FastAPI on localhost | managed container service | ops to budget |
| Docker image on disk | managed container registry | egress fees, availability |
| GitHub Actions | hosted CI minutes | minutes billed at scale |
| your cron/orchestrator | managed scheduler | retry UIs for cost |
| local monitoring (Module 14) | hosted monitoring | sampling, retention, price |

## 2. From container to orchestration (why Kubernetes exists)

Module 11 gave you *one* container on *one* machine. Production asks
questions that a laptop cannot answer:

- run **N copies** so one crash isn't an outage;
- replace a dead container **automatically**;
- roll out version 1.1 **without dropping requests**;
- give each process a **resource budget** so one noisy tenant can't starve
  the host;
- keep the **address stable** while the processes behind it churn.

**Orchestration** is the layer that answers all five from declarative files:
you state *what should exist*, the system works out *how to keep it true*.

**Principle:** run N copies only when N>1 buys something (fault tolerance,
throughput). A one-person internal tool with one replica and a supervisor
script can be *more* reliable than a misconfigured cluster — the orchestration
decision is earned, not automatic (§10).

## 3. Kubernetes objects: the five you need

A **cluster** = control plane + worker **nodes**. Everything else is an API
object you declare:

```
Deployment "support-api"          Service "support-api"
  owns ──► Replica ×2                  routes ──► Pods with label
             │  each is a...             app=support-api
             ▼
           Pod                       (stable DNS name + virtual IP;
             │                        pods keep churning underneath)
             ▼
        Container (your image)
```

| Object | One sentence | Why it exists |
|---|---|---|
| **Pod** | one or more containers sharing a network/filesystem, the smallest unit you schedule | containers die; pods are what actually run |
| **Deployment** | a template for pods + a *replica count* + update strategy | pods are disposable — the Deployment owns the desired state |
| **Replica** | one of the N identical pods of a Deployment | N>1 = survive a node/zone loss |
| **Service** | a stable address + load balancing over ready pods | pods have ephemeral IPs; clients need one name that outlives them |
| **Label / selector** | key=value tags; Services select pods by them | the indirection that lets pods churn behind a fixed address |

Also in the lab: **ConfigMap** (non-secret config) and **Secret**
(cluster-held sensitive values — see
[`examples/k8s/secrets.md`](https://github.com/nadeem-majeedch/MLOps/blob/main/examples/k8s/secrets.md)).

**Tool:** the actual manifests are in `examples/k8s/` —
`deployment.yaml`, `service.yaml`, `hpa.yaml`. Every line is commented;
reading them *is* half the module.

## 4. Rolling updates, and the one command that undoes them

The default strategy in our manifest:

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 0     # never take a ready pod away before a new one passes
    maxSurge: 1           # add at most one extra pod at a time
```

Sequence: create pod v1.1 → wait until **Ready** (readiness probe passes) →
send traffic → retire a v1 pod → repeat. At no point does capacity dip
below the requested replicas — *provided* readiness fails fast for bad
images. If the new pod never becomes ready, the rollout **stalls**
(`kubectl rollout status` shows it), old pods keep serving, and you decide:

```bash
kubectl rollout status deployment/support-api   # observe
kubectl rollout undo deployment/support-api     # REVERT to last good revision
```

**Principle — rollback:** a deployment mechanism without a tested undo is
half a mechanism (same rule as `release.py rollback` in Module 09 — this is
that rule at the platform layer). `revisionHistoryLimit` keeps previous
revisions available precisely so `undo` has something to restore.

## 5. Probes: readiness vs liveness

| Probe | Question | Failure means |
|---|---|---|
| **Readiness** | can this pod serve traffic *right now*? | removed from the Service — **no traffic**, pod still alive (warm-up, loading a model, dependency down) |
| **Liveness** | is this pod wedged (deadlocked, hung)? | container **restarted** by kubelet |

Our manifest: readiness on `/health` every 5 s from 3 s;
liveness on `/health` from 10 s, failing 3× before restart.

**Principle — do not point both at the same check blindly:** a slow
dependency makes readiness fail (correct: shield it) but would also make
liveness fail (wrong: restart loops make it *worse* — the classic
crash-loop-by-probe). Liveness should test "am I responsive", not "is my
whole world healthy". This distinction is worth marks in every k8s exam and
every real outage review.

## 6. Resources: requests, limits, and what actually happens

```yaml
resources:
  requests: {cpu: 100m, memory: 256Mi}   # reservation: scheduling + budget
  limits:   {cpu: 500m, memory: 512Mi}   # ceiling: throttle / OOM-kill
```

- **CPU request** — the scheduler places the pod only where 100m is free;
  the pod can burst above it while the node has spare CPU, up to the limit,
  where it is **throttled** (work slows; it is not killed).
- **Memory request** — accounting for the scheduler.
- **Memory limit** — exceeding it = **OOMKill**: the container dies and the
  Deployment replaces it. Silent data loss in flight, clean restart
  afterward.
- **No limits at all** — one runaway process can starve every pod on the
  node (noisy neighbour), which is why clusters require them.

**Cost link:** you pay for **requests × time**, not for what you use.
Over-requesting is the most common cloud bill surprise.

**HPA target point (classic exam trap):** `averageUtilization` is a
percentage of the **request**, not the limit. 70% of a 100m request = 70m —
the pod scales out long before it hits a 500m limit.

## 7. Scaling and reliability

Two directions (**Principle**):

- **Scale up** — raise limits/instance size. Simple, finite, downtime risk
  when resizing, usually cheaper until a ceiling.
- **Scale out** — add replicas. Needs statelessness (our API is: model is
  read-only, requests are independent), a router (the Service), and headroom
  in the cluster.

**HPA** (HorizontalPodAutoscaler) automates scale-out from metrics —
`examples/k8s/hpa.yaml`, min 2 / max 6 / 70% CPU, with stabilization windows
so it doesn't flap. Autoscaling is a **cost control only when idle capacity
is real**: if your load is flat, min replicas is your actual bill.

Reliability vocabulary you must be able to use:

| Term | Meaning in this lab |
|---|---|
| **Graceful degradation** | when dependency X fails, serve the degraded path (cached/default answer) instead of 500s |
| **Self-healing** | Deployment replaces a crashed/killed pod; no human |
| **Blast radius** | how much dies with one failure — replicas + zones limit it |
| **Rolling vs recreate** | rolling keeps availability; recreate is faster but has a gap |
| **Backoff / retry** | automatic retries need jitter and idempotency, or they amplify outages |

## 8. Infrastructure as code, and secrets at the cluster layer

**IaC (Principle):** infrastructure exists as reviewable files, applied by
tooling, not clicked together in a console. Kubernetes manifests *are* IaC
in the graded path; Terraform/CloudFormation/Pulumi are the ☁️ cloud
variants with the same discipline. Test: "could a teammate rebuild this
environment from the repo alone?"

**Secrets (from Module 15, restated for clusters):** manifests are
committed; values are not. `kubectl create secret` + `secretKeyRef` keeps
`deployment.yaml` commit-able while the value lives outside git — with the
honest limit spelled out in `examples/k8s/secrets.md`: base64 is not
encryption; cluster RBAC is the real boundary.

## 9. Cost management, honestly

**Cost (Principle):** cloud cost = Σ (resource requests × time × price) +
storage + **egress** (bytes leaving the region — the fee people discover
late). The levers, in the order worth pulling:

1. **Right-size requests** — measure, then cut. The biggest wins live here.
2. **Autoscaling + scheduled scaling** — pay for peak only at peak.
3. **Spot/preemptible instances** — 50–90% off, interruptible (bad for the
   single replica, fine for fault-tolerant batch training).
4. **Storage lifecycle** — old artifacts to cold storage.
5. **Region and egress discipline** — keep compute and data together.

**Cost estimate method for LO 16.4** (the challenge uses this): monthly ≈
`replicas × CPU-request-price-equivalent × 730 h` + memory term + storage +
estimated egress — from a **published** price sheet, cited by name and date.
Every number labelled *estimate*; every cloud step ☁️/💲 disclosed with a
free-tier fallback and a teardown command.

**Teardown discipline:** every optional cloud activity in this course names
its teardown *before* its setup. A student left with a bill is a course
failure, not a student failure.

## 10. When NOT to orchestrate (the anti-hierarchy step)

Advanced means knowing the limits:

| Situation | Better choice than Kubernetes |
|---|---|
| one service, one machine | Docker + restart policy / a supervisor |
| batch jobs on a schedule | cron/systemd timers (Module 13's runner already does this) |
| a static site | GitHub Pages (what this course's site uses) |
| a student learning project | compose file + README |

**Kubernetes earns its complexity when you need:** many replicas across
machines, automated self-healing and rollouts, per-team resource isolation,
or an org already running it. The graded lab exists to teach the vocabulary
and the mechanics — **running a cluster is not a requirement of this
course's production path**; the capstone's default remains local and free.

## 11. Tool vs principle, this module

| Tool (swap freely) | Principle (travels with you) |
|---|---|
| kubectl, kind, minikube | desired state, reconciliation |
| Deployment/Service/HPA kinds | stable addressing over churning instances |
| requests/limits fields | budgets before ceilings |
| readiness/liveness mechanisms | never let health checks cause the outage |
| one vendor's price sheet | cost is a design input; teardown is part of setup |

---

[← Learning objectives](learning-objectives.md) · [Next: worked example →](worked-example.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*