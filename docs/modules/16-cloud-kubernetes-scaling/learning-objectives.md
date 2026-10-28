# Learning objectives — Module 16

Maps to syllabus outcomes
[LO 16.1–16.5](../../syllabus/detailed-syllabus.md#module-16-cloud-deployment-concepts-kubernetes-scaling-and-reliability).

| # | You can… | You prove it by… |
|---|---|---|
| **16.1** | Explain core cloud models (IaaS/PaaS/serverless, regions, managed services) and map each course technique to its managed equivalent | Your mapping table: 8 course techniques (registry, scheduler, tracker, CI…) → what a managed service would do instead — with the trade-off, not just the name |
| **16.2** | Deploy the containerised API to a local Kubernetes cluster and reason about deployments, services, replicas, and rollouts | `kubectl` transcript: 2/2 pods ready, `/health` through a port-forward, a rolling update observed with `rollout status` |
| **16.3** | Design for scaling and reliability: horizontal scaling, health checks, autoscaling, graceful degradation, rollback | Break/heal evidence (crashed pod replaced) **and** `rollout undo` restoring the previous revision, each with output |
| **16.4** | Estimate the cost of a small production deployment and name the levers that control it | One-page cost plan: replicas × resource requests × hours, a published price sheet, and two levers that halve it |
| **16.5** | (Optional ☁️) Apply infrastructure-as-code principles to a real free-tier account | Manifests are the IaC artefact for the graded path; a cloud variant adds a written teardown plan |

## Supporting skills

- Say precisely what a **pod**, **deployment**, **service**, and **replica**
  each is — and which problem each one solves that the previous one cannot.
- Distinguish **requests** (scheduling budget) from **limits** (throttle /
  OOM boundary) and predict what happens when you get them wrong.
- Explain why **readiness** and **liveness** probes must not be the same
  check, and what each failure does to traffic.
- Choose between **scaling up** (bigger limits) and **scaling out** (more
  replicas) — and name which one a CPU-based HPA actually does.
- Read a rollout: surges, waits, health-checks — and know the one command
  that reverses a bad one.
- Apply teardown discipline: every optional ☁️ resource named, costed, and
  removed.

## Self-check questions

1. Your single-replica API updates to a new image and the new pod hangs on
   import. What do users experience with `maxUnavailable: 0`? What if the
   manifest had said `maxUnavailable: 1`?
2. A pod is Ready but a liveness probe now fails. What happens to traffic
   first — and then to the pod?
3. HPA scales out at 70% CPU. 70% of *what* — request or limit? Why does
   that distinction matter for cost?

*(Answers in [knowledge-check.md](knowledge-check.md) — attempt first.)*

---

[← Module 16 index](index.md) · [Next: concepts →](concepts.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*