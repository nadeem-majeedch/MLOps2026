# References — Module 16

Official documentation first; everything listed is free to read. ⭐ = start
here. The authoring machine for this course has no container tooling, so
these are the sources you will actually run the lab against — they are
primary vendor docs, not recollections.

## Kubernetes (primary)

- ⭐ **Kubernetes Basics tutorial** (official, interactive) — the 30-minute
  path from pod to deployment to service.
  <https://kubernetes.io/docs/tutorials/kubernetes-basics/>
- ⭐ **Concepts → Objects in Kubernetes** — pod/deployment/service
  definitions straight from the source used in concepts §3.
  <https://kubernetes.io/docs/concepts/overview/working-with-objects/kubernetes-objects/>
- **Deployments** — rolling update strategy, `maxUnavailable`/`maxSurge`,
  rollout undo (concepts §4). <https://kubernetes.io/docs/concepts/workloads/controllers/deployment/>
- **Configure Liveness, Readiness and Startup Probes** — the distinction
  that concepts §5 is built on. <https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/>
- **Resource management for pods** — requests, limits, QoS classes.
  <https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/>
- **Horizontal Pod Autoscaling** — `averageUtilization` is relative to
  requests (the Q6 trap). <https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/>
- **Secrets** — the `secretKeyRef` mechanism (Module 15 rules restated).
  <https://kubernetes.io/docs/concepts/configuration/secret/>

## Local clusters (the lab's free path)

- ⭐ **kind** (Kubernetes IN Docker) — the lab's recommended runtime.
  <https://kind.sigs.k8s.io/docs/user/quick-start/>
- **minikube** — the alternative, with `addons enable metrics-server` for
  the optional HPA step. <https://minikube.sigs.k8s.io/docs/start/>
- **kubectl install** (all platforms).
  <https://kubernetes.io/docs/tasks/tools/>

## Cloud concepts (vendor-neutral, then one vendor's free tier)

- ⭐ **NIST definition of cloud computing** — the IaaS/PaaS/SaaS vocabulary
  without marketing. <https://www.nist.gov/publications/cloud-computing-taxonomy-and-reference-architecture>
- **Google SRE book — chapters on scalability & availability** — graceful
  degradation, quotas, capacity planning in plain language (free online).
  <https://sre.google/sre-book/table-of-contents/>
- **AWS/Azure/GCP pricing calculators** — for LO 16.4 use **one** sheet,
  cite its name and the date you read it (any of:
  <https://aws.amazon.com/pricing/calculator/>,
  <https://cloud.google.com/products/calculator>,
  <https://azure.microsoft.com/en-us/pricing/calculator/>). All ☁️ optional;
  free tiers only, teardown first.

## Infrastructure as code

- **Kubernetes manifests are the graded-path IaC** (they're in
  `examples/k8s/` — read them; that *is* the reference).
- **Terraform registry / docs** — the concept exemplar for cloud IaC (the
  syntax is the transferable part).
  <https://developer.hashicorp.com/terraform/docs>

## Containers (revision from Module 11)

- **Dockerfile reference** — `HEALTHCHECK`, layer caching, exec form.
  <https://docs.docker.com/build/dockerfile/reference/>
- ⭐ Module 11's own references page (image semantics this module builds
  on): [../11-docker-containers/references.md](../11-docker-containers/references.md)

---

**Tool vs principle:** `kubectl` and one vendor's price sheet will age;
desired-state reconciliation, budgets-before-ceiling, health checks that
don't cause outages, and cost-as-a-design-input will not.

---

[← Troubleshooting](troubleshooting.md) · [Module index](index.md) · [Module 17 →](../17-capstone/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*