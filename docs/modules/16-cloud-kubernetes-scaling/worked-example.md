# Worked example — Module 16

This module's worked example is an **annotated manifest walkthrough**: you
will understand every line we apply, predict what each command must do, and
run the cost arithmetic yourself.

!!! warning "Honest execution status — read this first"
    The authoring machine for this course has **no Docker, kind, or
    kubectl** installed, so *no Kubernetes command in this module has been
    executed there*. Everything shown as **REAL** below is read from the
    actual manifest files in `examples/k8s/` (which are YAML-parsed and
    verified). Everything shown as **expected** is Kubernetes' documented
    behaviour — labelled as such, never presented as a captured run. Lab 16
    makes *your* transcript the evidence.

---

## 1. What we deploy — the real manifest, annotated

**REAL** file: [`examples/k8s/deployment.yaml`](https://github.com/nadeem-majeedch/MLOps/blob/main/examples/k8s/deployment.yaml)
(parsed with `yaml.safe_load` → `Deployment support-api` ✓).

```yaml
spec:
  replicas: 2                 # (A) two pods: one can die without an outage
  revisionHistoryLimit: 3     # (B) past revisions kept so `undo` has a target
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0       # (C) NEVER remove a ready pod before a new one passes
      maxSurge: 1             # (D) at most ONE extra pod during the update
  template:
    spec:
      containers:
        - name: api
          image: support-api:1.0        # (E) the Module 11 image, pinned tag
          imagePullPolicy: IfNotPresent  # (F) use the locally-loaded image; offline
          resources:
            requests: {cpu: 100m, memory: 256Mi}   # (G) scheduling budget = what you pay for
            limits:   {cpu: 500m, memory: 512Mi}   # (H) throttle ceiling / OOM-kill boundary
          readinessProbe:                # (I) gates TRAFFIC: ready → join the Service
            httpGet: {path: /health, port: 8000}
          livenessProbe:                 # (J) gates RESTART: fail 3× → container restarted
            httpGet: {path: /health, port: 8000}
```

Read (C)+(D) together as one guarantee: *capacity never dips below 2
during an update* — because surge adds before unavailability removes.
That guarantee collapses the moment readiness never turns true (bad image),
which is why (I) exists.

## 2. The five commands and their expected behaviour

Commands are **REAL** (they are in `examples/k8s/README.md`); the outputs
described are **expected** Kubernetes behaviour — capture your own:

| # | Command | What you should observe (expected) |
|---|---|---|
| 1 | `kubectl apply -f examples/k8s/` | `deployment.apps/support-api created` · `service/support-api created` |
| 2 | `kubectl rollout status deployment/support-api` | `deployment "support-api" successfully rolled out` — 2/2 READY |
| 3 | `kubectl get pods -o wide` | two pods, both `2/2 Running`, different node/pod IPs (ephemeral — the reason a Service exists) |
| 4 | `kubectl port-forward svc/support-api 8000:8000` then `curl :8000/health` | `{"status":"ok",...}` — the Service forwarded to one of the ready pods |
| 5 | `kubectl get endpoints support-api` | **two** pod IPs — proof the selector found both replicas |

**Prediction exercise (do it before running):** rename the image to
`support-api:9.9` and apply. What happens? Expected: the new ReplicaSet
creates a pod that fails (`ErrImageNeverPull` / back-off), the rollout
**stalls**, both old pods keep serving — and `kubectl rollout undo`
returns you to zero downtime. This is (C) doing its job; a manifest with
`maxUnavailable: 1` would instead have taken a serving pod away first.

## 3. Break, heal, rollback — the mechanics you must be able to narrate

**Break (expected):** `kubectl exec` kill the API inside one pod →
the container dies → kubelet restarts it (restart policy) → if it
repeatedly fails, the **Deployment** replaces the pod entirely. From the
outside: one `RESTARTS` counter bumps, `2/2` returns, **no client noticed**.
That is self-healing = desired state (2 replicas) being reconciled, not
magic.

**Rollout (expected):** `kubectl set image deployment/support-api api=support-api:1.1`
→ `rollout status` walks `1 of 2 updated… 2 of 2 updated… rolled out`,
watching readiness between each.

**Rollback (expected):** `kubectl rollout undo deployment/support-api` →
the previous ReplicaSet scales back up; `rollout status` confirms;
`kubectl rollout history deployment/support-api` lists revisions (limited
by (B)).

## 4. The request/limit table — one small truth table

| Situation | CPU (limit 500m) | Memory (limit 512Mi) | Outcome |
|---|---|---|---|
| steady load, 80m | within request | within request | scheduled, full speed |
| burst to 400m | above request, below limit | — | **throttled? no** — allowed to burst while node has spare, capped at 500m |
| sustained 600m | above limit | — | **throttled** (slow, alive) |
| 600 MB resident | — | above limit | **OOMKill** → restart → Deployment heals |
| no limits at all | unbounded | unbounded | starves the node — the noisy-neighbour incident |

The exam-grade detail: CPU over limit = *slow down*; memory over limit =
*die*. Different failure modes need different alerting.

## 5. Cost arithmetic (real method, placeholder price)

**Principle:** you pay for **requests × time**. The method, with prices you
look up yourself from one *published* price sheet (cite it, date it):

```
monthly ≈ replicas × 730 h × ( cpu_request × P_cpu  +  mem_GiB × P_mem )
        + storage + estimated egress
```

With our manifest's numbers (2 replicas, 100m, 256Mi ≈ 0.25 GiB):

```
= 2 × 730 × ( 0.1 × P_cpu + 0.25 × P_mem )
= 146 × P_cpu  +  365 × P_mem     "dollars per month, before storage/egress"
```

At the HPA ceiling (6 replicas) every term **triples**: 438·P_cpu +
1095·P_mem — which is why `maxReplicas: 6` is itself a cost control. Two
levers that typically halve the bill (the challenge asks you to prove
which): right-sizing requests down after measuring real usage, and
scheduled/autoscaled replicas so peak capacity exists only at peak.

No price is invented here: substitute the current published values and
show your substitution.

---

**Your turn:** produce the real transcript in [lab.md](lab.md) — that
transcript, not this page, is your evidence.

---

[← Concepts](concepts.md) · [Next: lab →](lab.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*