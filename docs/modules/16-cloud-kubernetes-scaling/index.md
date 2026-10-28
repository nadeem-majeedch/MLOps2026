# Module 16 — Cloud deployment concepts, Kubernetes, scaling, and reliability

!!! success "Module complete"
    Lessons, worked example, lab (with an honest no-tools path), independent
    challenge, knowledge check (with answers), troubleshooting, and references
    are all written. Lab execution requires Docker/kind/kubectl on your
    machine — see the status note below.

**Stage:** Advanced · **Estimated effort:** 12 h · **Depends on:** 11, 13 · **Next:** 17

---

## What this module is about

Everything so far ran on *your machine*. This module asks the question a
deployment engineer actually faces — **"what happens when one machine
isn't enough?"** — and answers it in the right order: concepts first,
vendor second, cluster only where a cluster earns its complexity.

```
cloud models (portable) ─► desired state ─► rolling update ─► probes & budgets ─► scale & cost
   what you rent            what should exist    never drop a request   requests vs limits   the bill
```

You will deploy a real manifest — 2 replicas, zero-downtime updates,
readiness/liveness probes, resource budgets — then **break it on purpose**
and watch it heal, then roll a bad release back with one command.

Two things this module refuses to do:

- It never presents a price it did not look up: cost arithmetic uses
  *your* published price sheet, with substitution shown.
- It never pretends the authoring machine ran Kubernetes: the manifests
  are YAML-verified, the lab requires **your** transcript as evidence, and
  machines without Docker/kind/kubectl take a documented **Path B**.

## How to study this module (in order)

| # | File | What it does | Time |
|---|---|---|---|
| 1 | [learning-objectives.md](learning-objectives.md) | What you must be able to do, and how you prove it | 10 min |
| 2 | [concepts.md](concepts.md) | Cloud models, k8s objects, rollouts, probes, resources, scaling, cost, when NOT to orchestrate | 160 min |
| 3 | [worked-example.md](worked-example.md) | Annotated real manifest + expected-behaviour tables + cost formula | 45 min |
| 4 | [lab.md](lab.md) | **Guided lab:** run it like a service (Path A / Path B) | 150 min · 60 min (B) |
| 5 | [independent-challenge.md](independent-challenge.md) | The 100-rps scaling and cost plan | 90 min |
| 6 | [knowledge-check.md](knowledge-check.md) | 10 questions with reasoning | 30 min |
| 7 | [troubleshooting.md](troubleshooting.md) | Tooling, cluster, probe, and cost confusions | as needed |
| 8 | [references.md](references.md) | Official Kubernetes docs, kind, SRE book, pricing calculators | optional |

## Before you start

- Module 11 (you can build the image) and Module 13 (you understand
  scheduled vs service workloads).
- ⚠️ **Resource-heavy lab:** ~4 GB RAM and several GB of disk for kind —
  Step 0 in [lab.md](lab.md) decides Path A vs Path B.
- **Free and local throughout.** Cloud accounts are ☁️ **optional**
  extensions only: free tier only, teardown commands written *before*
  setup, and no paid tier without your own explicit decision.

## Evidence you should produce

1. `kubectl` transcript: 2/2 pods behind one Service, health response.
2. A rolling update **and** a `rollout undo`, both captured.
3. Break/heal evidence with your narration of which layer acted.
4. Written answers: readiness vs liveness; CPU-throttle vs OOMKill.
5. A cost plan with cited published prices and two quantified levers.
6. If you took Path B: say so — labelled evidence, no invented output.

---

[← Module 15: Security, privacy, governance, fairness, and responsible deployment](../15-security-privacy-governance/index.md) · [Full syllabus](../../syllabus/detailed-syllabus.md#module-16-cloud-deployment-concepts-kubernetes-scaling-and-reliability) · [Module 17 →](../17-capstone/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../../about/index.md).*