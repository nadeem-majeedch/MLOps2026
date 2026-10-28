# Secrets in Kubernetes (Module 16 note)

Rule from Module 15, restated for this platform: **manifests are committed;
secret values are not.**

## The pattern

```bash
# 1. create the secret from your shell (value never enters git)
kubectl create secret generic support-api-secrets \
  --from-literal=service-api-key="$env:SERVICE_API_KEY"     # 🪟 PowerShell syntax shown below

# 🪟 PowerShell:
# kubectl create secret generic support-api-secrets `
#   --from-literal=service-api-key=$env:SERVICE_API_KEY
```

```yaml
# 2. mount it as an environment variable (see the commented block in
#    deployment.yaml)
env:
  - name: SERVICE_API_KEY
    valueFrom:
      secretKeyRef:
        name: support-api-secrets
        key: service-api-key
```

## What this gives you

- the **Deployment manifest stays commit-able** (labels, probes, strategy —
  no values);
- the value lives in etcd as a Secret object, readable only by whoever can
  `kubectl get secret` — which is exactly Module 15's least-privilege
  question again, at the cluster layer;
- rotation = recreate the secret + restart the deployment, no git history
  to scrub.

## Honest limits (say these out loud in your write-up)

- A Secret is base64, not encryption — cluster access *is* the privilege.
  Production clusters add encryption-at-rest (a platform concern, ☁️).
- Anything that can `kubectl get secret -o yaml` on your namespace has the
  value. RBAC decides that; it is not decided by YAML hygiene.

Cleanup: `kubectl delete secret support-api-secrets`.