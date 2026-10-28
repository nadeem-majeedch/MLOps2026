# Kubernetes manifests (Module 16, optional lab)

Local-cluster manifests for the capstone/churn API image from Module 11.
**Nothing here has been applied on a cluster from this repository's
authoring machine** — Kubernetes tooling was not installed there — so treat
these as YAML-validated (parsed with `yaml.safe_load`, all four files) but
*cluster-untested* until you run Lab 16's checks yourself.

| File | Kind | Teaches |
|---|---|---|
| [deployment.yaml](deployment.yaml) | Deployment ×2 replicas | rolling update, probes, resources, labels |
| [service.yaml](service.yaml) | Service (ClusterIP) | stable address in front of disposable pods |
| [hpa.yaml](hpa.yaml) | HorizontalPodAutoscaler | CPU request-based scaling, ceilings as cost levers |
| [secrets.md](secrets.md) | how-to note | injecting `SERVICE_API_KEY` without committing it |

## Requirements (⚠️ resource-heavy)

- Docker **or** another container runtime (~4 GB RAM, several GB disk)
- `kind` (recommended, free) or `minikube`, plus `kubectl`
- the built image: `docker build -t support-api:1.0 examples/capstone-support`

## The whole lab in five commands

```bash
kind create cluster --name mlops-lab        # 🐧/🪟 WSL
kind load docker-image support-api:1.0 --name mlops-lab
kubectl apply -f examples/k8s/
kubectl rollout status deployment/support-api
kubectl port-forward svc/support-api 8000:8000   # then: curl .../health
```

Break/heal and rollback drills: see
[lab 16](../../docs/modules/16-cloud-kubernetes-scaling/lab.md).

## Cleanup (leaves no cloud resources — everything is local)

```bash
kubectl delete -f examples/k8s/
kind delete cluster --name mlops-lab
docker rmi support-api:1.0
```

There is **no cloud account, no bill, and no teardown risk**: this module's
graded path runs entirely on your machine. Cloud deployment is an explicitly
optional ☁️ extension in the module docs.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../../docs/about/index.md).*