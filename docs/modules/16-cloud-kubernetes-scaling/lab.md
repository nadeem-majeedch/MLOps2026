# Lab 16 — Run it like a service

!!! info "This lab is optional and resource-heavy — check your machine first"
    Kubernetes needs a container runtime, ~4 GB RAM and several GB of disk.
    **Step 0 decides which path you take.** The graded path stays free and
    local: kind + kubectl, no cloud account anywhere.

## 1. Scenario and business problem

Your capstone API (Module 11's image) will be handed to a team that expects
"it just keeps serving". Today it runs once, on one machine, and a crash is
an outage. The business problem: **turn a container into a service** —
replicas that survive a crash, updates that drop zero requests, and a
rollback anyone can run from the README.

## 2. Skills practising

- Applying declarative manifests and narrating what each object does.
- Reading a rollout, breaking it on purpose, and undoing it.
- Distinguishing readiness from liveness by observing both.
- Interpreting requests/limits and predicting throttle vs OOMKill.
- Optional (if metrics-server exists): wiring an HPA and reading it.
- Cost arithmetic from your own manifest numbers.

## 3. Prerequisites

- Module 11 completed (the image builds) and its Dockerfile still green.
- [concepts.md](concepts.md) §§2–6 read; manifests in `examples/k8s/` read
  line by line.
- **Step 0 preflight below** — it decides your path.

## 4. Required tools and estimated time

| Item | Detail |
|---|---|
| Tools | Docker (or compatible runtime), `kind`, `kubectl` — all free |
| Cost | **Free, local.** No cloud account, no bill, teardown is local |
| ⚠️ Resource-heavy | ~4 GB RAM free, several GB disk; the cluster takes minutes to start |
| 🕐 Estimated time | Path A: 150 min · Path B (no tools): 60 min |

**Step 0 — preflight (decides your path):**

```powershell
# 🪟 Windows — PowerShell
docker --version; kind version; kubectl version --client
```

- **All three present → Path A** (full lab).
- **Any missing → Path B** (documented substitute; the course *requires*
  only Path A when the software is available — never install things you
  cannot afford in time or disk without deciding it yourself).

## 5. Input data and how to obtain it

No dataset — the "input" is your own image and manifests:

```powershell
# 🪟 from the repository root
docker build -t support-api:1.0 examples/capstone-support
# ✅ expect: SUCCESS (Module 11 taught you to read a build log)
```

---

# Path A — full lab (tools available)

## 6. Directory layout

```
examples/k8s/
├── README.md         # five-command quickstart + teardown
├── deployment.yaml   # 2 replicas, rolling update, probes, resources
├── service.yaml      # ClusterIP front-end for the replica set
├── hpa.yaml          # OPTIONAL autoscaling (needs metrics-server)
└── secrets.md        # how values enter the cluster without entering git
```

## 7. Setup and execution steps

**Step 1 — Cluster up.**
```bash
kind create cluster --name mlops-lab
kind load docker-image support-api:1.0 --name mlops-lab
kubectl apply -f examples/k8s/
kubectl rollout status deployment/support-api
```
✅ **Checkpoint:** rollout reports successfully; `kubectl get pods` shows
**2/2 running** pods (count them — one pod is not this lab).

**Step 2 — Reach it.**
```bash
kubectl port-forward svc/support-api 8000:8000   # terminal 1
curl http://127.0.0.1:8000/health                # terminal 2
kubectl get endpoints support-api
```
✅ **Checkpoint:** health JSON answers and `endpoints` lists **two** pod IPs
— that is the Service's load balancing materialised.

**Step 3 — Observe the probes.**
```bash
kubectl describe pod -l app=support-api | grep -A2 "Liveness\|Readiness"
```
✅ **Checkpoint:** you can point at the two probe definitions and say what
each failure does (traffic vs restart — concepts §5).

**Step 4 — Rolling update.**
```bash
docker build -t support-api:1.1 examples/capstone-support
kind load docker-image support-api:1.1 --name mlops-lab
kubectl set image deployment/support-api api=support-api:1.1
kubectl rollout status deployment/support-api
```
✅ **Checkpoint:** `2 of 2 updated… rolled out`. Paste the status lines —
this is your roll-forward evidence.

**Step 5 — Break it (self-healing).**
```bash
kubectl exec deploy/support-api -- sh -c "kill 1"   # kill the API process
kubectl get pods -w                                  # watch RESTARTS climb
```
✅ **Checkpoint:** the pod returns to `2/2` **without you fixing anything**;
note the restart counter — narrate which layer acted (kubelet vs
Deployment).

**Step 6 — Rollback.**
```bash
kubectl rollout undo deployment/support-api
kubectl rollout status deployment/support-api
kubectl rollout history deployment/support-api
```
✅ **Checkpoint:** status confirms the previous revision is serving; the
history shows revisions (bounded by `revisionHistoryLimit: 3`).

**Step 7 — Optional HPA (only if metrics-server is running).**
```bash
kubectl apply -f examples/k8s/hpa.yaml
kubectl get hpa
```
✅ **Checkpoint:** either `Unknown`/no metrics → *record that honestly and
skip* (common on a fresh kind), or `<unknown>` resolves to a percentage.
Do **not** fabricate load numbers; the mechanism read is enough.

**Step 8 — Cost arithmetic (LO 16.4 input).** Using your own manifest
numbers and the worked formula in [worked-example.md §5](worked-example.md#5-cost-arithmetic-real-method-placeholder-price),
produce the monthly figure with a *published* price sheet (cite it). Note
which line items your lab does **not** incur (it is all local) — that gap
is the point of the exercise.

## 8. Expected outputs and verification methods

| Check | Expected (tool-documented behaviour) | Your evidence |
|---|---|---|
| pods | 2 × `2/2 Running` | `kubectl get pods` output |
| service | 2 endpoints | `kubectl get endpoints` |
| health | 200 + JSON | `curl` output |
| update | `successfully rolled out` | rollout status lines |
| break | RESTARTS > 0, then `2/2` | `get pods -w` capture |
| undo | previous revision serving | rollout history + status |

## 9. Acceptance criteria (✅ Lab 16 complete)

1. 2/2 pods through a Service, with a real `curl` health response.
2. One rolling update observed end to end **and** one `rollout undo`
   executed, both with transcripts.
3. Break/heal evidence: a killed process restored automatically, with your
   one-paragraph narration of which layer acted.
4. Written answers: readiness vs liveness failure outcomes; CPU-limit vs
   memory-limit outcomes.
5. Cost estimate: formula, substituted published prices, two cost levers.

## 10. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `ErrImageNeverPull` / `ImagePullBackOff` | image never loaded into kind | `kind load docker-image support-api:1.0 --name mlops-lab` |
| pods `Pending` | insufficient CPU/memory requests vs node capacity | `kubectl describe pod` → look at `Events`; lower requests or shrink replicas |
| rollout stuck at `0 of 2 updated` | readiness never passes | `kubectl describe pod` → Events + logs; check `HOST=0.0.0.0` and the image tag |
| port-forward returns nothing | forwarding the Deployment instead of the Service, or wrong port | forward **`svc/support-api`**, port `8000:8000` |
| HPAs show `<unknown>` | metrics-server absent | accept and skip (Step 7 says to record it honestly) |
| `kill 1` does nothing | PID 1 is not the API in that image | `kubectl exec` + `ps`, or use the documented restart path |
| cluster eats my laptop | resources too small | `kind delete cluster` and take **Path B** — no course penalty when documented |

## 11. Cleanup (local only — leaves nothing behind)

```bash
kubectl delete -f examples/k8s/
kind delete cluster --name mlops-lab
docker rmi support-api:1.0 support-api:1.1
```
✅ Nothing remains: no account, no bill, no teardown checklist beyond this.

---

# Path B — no container tooling (documented substitute)

Do this when Step 0 fails. It is a *different, smaller* exercise — say so in
your evidence; it does not claim Path A's outcomes.

1. **YAML fluency:** parse all three manifests
   (`python -c "import yaml,sys; print(yaml.safe_load(open(sys.argv[1]))['kind'])" examples/k8s/deployment.yaml`)
   and annotate each field from concepts §§3–6. ✅ Checkpoint: you can
   explain `maxUnavailable: 0`, both probes, and both resource fields
   without notes.
2. **Narrate, don't run:** write the expected sequence for Steps 4–6
   (update → break → undo) as a timeline with the API object state at each
   point — clearly headed *expected behaviour, not executed*.
3. **Cost work is unchanged:** Step 8's arithmetic uses published prices
   and your manifest numbers — fully gradeable offline.
4. **Plan the reinstall:** list exactly what you'd install, the disk/RAM
   you'd need, and why — so the deferred lab is one command away later.

## 12. Debrief and ethics note

- Everything in Path A is **local**: no account, no data leaves your
  machine, no bill. That is deliberate — the course's graded path must not
  depend on credit cards.
- Self-healing is not magic: it is a desired-state loop. Understanding it
  is the difference between *operating* a platform and *praying to* one.
- The honest gaps (HPA without metrics, Path B without tools) belong in
  your evidence. Report what did not run — that is engineering, not failure.

## 13. Stretch goals (optional, ☁️/💲 disclosed)

1. Add a **PodDisruptionBudget** and reason about voluntary evictions.
2. Run the same manifests on a **free-tier cloud** (☁️): record the account,
   region, estimated price **and the teardown command first** — no paid
   tier, ever, without your own explicit decision.
3. Package the manifests with **kustomize** overlays (dev/prod) — IaC
   layering without another tool's syntax.

---

[← Worked example](worked-example.md) · [Next: independent challenge →](independent-challenge.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*