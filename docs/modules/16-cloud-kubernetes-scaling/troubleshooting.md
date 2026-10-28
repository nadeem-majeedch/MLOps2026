# Troubleshooting — Module 16

Symptom → cause → fix. The lab's own table covers lab-specific failures;
this page groups everything by layer. Course-wide problems live in
[../../troubleshooting/index.md](../../troubleshooting/index.md).

## Before you have the tools

| Symptom | Cause | Fix |
|---|---|---|
| `docker: command not found` (or equivalents) | no container runtime installed | take **Path B** (lab.md Step 0) — document it; do not install GBs of tooling under time pressure without deciding to |
| kind cluster creation times out / VMs won't start | virtualisation off or RAM too low | enable virtualisation in BIOS/Windows features, or free ~4 GB RAM; otherwise Path B |
| `kubectl` connects to something unexpected | wrong context (you have more than one cluster) | `kubectl config get-contexts` · `kubectl config use-context kind-mlops-lab` |
| WSL2 vs native Docker confusion (Windows) | kind's docker context points at a different engine than the one holding your image | run kind and `docker build` inside the same environment (same terminal session) |

## Cluster and manifests

| Symptom | Likely cause | Fix |
|---|---|---|
| `ImagePullBackOff` / `ErrImageNeverPull` | image exists on the host but not in the cluster's runtime | `kind load docker-image support-api:1.0 --name mlops-lab` |
| pods stuck `Pending` | requests don't fit any node | `kubectl describe pod` → Events section tells you; lower `requests` or replicas |
| `apply` rejects the YAML | syntax or wrong path | re-parse locally: `python -c "import yaml;yaml.safe_load(open('examples/k8s/deployment.yaml'))"` — the README's commands assume you're at the **repository root** |
| Service has no endpoints | selector matches no pod labels | `kubectl get pods --show-labels` vs the Service's `selector.app` |
| port-forward gives connection refused | forwarding the wrong object/port, or pods not ready | forward `svc/support-api 8000:8000`; confirm `2/2` first |

## Probes, updates, restarts

| Symptom | Likely cause | Fix |
|---|---|---|
| rollout stuck `0 of 2 updated` | readiness never passes | `kubectl describe pod` Events + `kubectl logs` — usually app not listening on `0.0.0.0`, wrong port, or missing artefact in image |
| new pods become Ready but requests fail | health check lies (checks `/` or always-200) | probe must hit a real signal — `/health` verifies the model loaded |
| restart loop climbing `RESTARTS` | liveness probe failing on a dependency, or OOMKill | describe: `OOMKilled` → raise the memory **limit**; `Liveness probe failed` → simplify the probe (concepts §5) |
| `kubectl set image` did nothing visible | wrong container name | `kubectl set image deployment/support-api **api**=…` — the name is the *container*'s, not the pod's |
| `rollout undo` "no rollout in progress" but bad version still there | undo applies to the last *completed* rollout | check `kubectl rollout history`; apply undo again or `--to-revision=N` |

## Scaling and cost

| Symptom | Likely cause | Fix |
|---|---|---|
| HPA shows `<unknown>` for targets | metrics-server missing | lab says record it and skip (Path A Step 7); enabling it is optional |
| HPA won't scale up | current load below 70% of **requests** | requests too high → right-size them (this *is* the cost lesson) |
| pods evicted under memory pressure | limit ≈ node capacity | lower limit or requests; check `kubectl describe pod` Events |
| cost estimate looks absurd | price sheet units misread (per vCPU-hour vs per GB-hour, per 1000 GiB egress) | restate units explicitly in the formula; show your substitution |

## Conceptual knots

| Confusion | Resolution |
|---|---|
| "Replicas = instances I pay for" | replicas × **requests** × time is the bill — utilisation is not on the invoice |
| "Readiness and liveness can share a probe" | only if the liveness question is genuinely "am I responsive" — otherwise restart storms (concepts §5) |
| "Self-healing means it can't go down" | it means *pods* are replaced; the Deployment, Service, or node can still be the outage — that's what replicas *and* zones are for |
| "Path B is failing the lab" | Path B is the honest substitute for a machine without tooling; the lab explicitly grades it as such |

---

[← Knowledge check](knowledge-check.md) · [Next: references →](references.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*