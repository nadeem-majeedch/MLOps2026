# Knowledge check — Module 16

## How to use this

1. Answer **in writing**, open book first, then closed book.
2. Mark yourself with the [answers](#answers) — **only after** committing
   to yours.
3. Target: **80% with justified reasoning**. Below that, re-read
   [concepts.md](concepts.md) §§1–9 before moving on.
4. Self-assessment inside a *suggested self-study framework* — not an
   official university exam. See
   [assessment-framework](../../syllabus/assessment-framework.md).

---

## Questions

**Q1.** Sort these into IaaS, PaaS, serverless, managed-ML: a virtual
machine; a hosted container app; a function billed per invocation; a
managed training-and-endpoint service. What does each *you* still manage?

**Q2.** Explain each object in one sentence, and name the problem it solves
that the previous one cannot: Pod → Deployment → Service.

**Q3.** With `maxUnavailable: 0, maxSurge: 1` and 2 replicas, walk through a
bad-image rollout. What do users experience? What does `rollout status`
show, and what single command returns you to safety?

**Q4.** A pod is Ready, then its liveness probe fails for 3 cycles.
Sequence of events, please — and what *should* have happened if instead the
*readiness* probe was the one failing?

**Q5.** Requests `100m/256Mi`, limits `500m/512Mi`: what happens under
(a) a 400m CPU burst, (b) sustained 600m CPU, (c) 600 MB resident memory,
(d) no limits configured at all?

**Q6.** HPA `averageUtilization: 70` — 70% of *what*? Why would an engineer
who thinks it's 70% of the *limit* badly over-provision?

**Q7.** Give two concrete reasons horizontal scaling needs a Service, then
one concrete case where a single replica with a restart policy beats a
cluster.

**Q8.** The cost formula bills `requests × time`. Explain why actual
utilisation does not appear in it, and name the two levers most likely to
halve a student-team's bill.

**Q9.** Your cluster holds a secret in a manifest. State the rule, the
mechanism (`secretKeyRef`), and the honest limit of base64 encoding.

**Q10.** A colleague says "we should run everything on Kubernetes — it's
the professional choice." Give the counter-argument using concepts §10,
and the one question that decides it.

---

## Answers

**A1.** VM → IaaS (you manage OS, runtime, scaling). Hosted container app
→ PaaS (you manage code + container). Per-invocation function →
serverless (you manage code only). Managed training/endpoint → managed-ML
(you manage model + data). The pattern: each tier moves work downward
away from you — and moves the invoice toward per-unit pricing.

**A2.** **Pod** = the smallest schedulable unit (one+ containers) — solves
"containers need a shared network/filesystem context". **Deployment** =
desired replica count + template + update strategy — solves "pods are
disposable; someone must own keeping N of them alive and rolling them
safely". **Service** = stable address + selector-based load balancing —
solves "pod IPs are ephemeral; clients need a name that survives churn".
Each object exists because the previous one is *unstable* or *addressable
only by something that keeps changing*.

**A3.** Surge creates a third pod with the bad image; its readiness never
passes (crash/ImagePull failure), so it never joins the Service; the
retirement step never happens because readiness gates progression — users
keep being served by the two healthy v1 pods the whole time. `rollout
status` stalls showing progress incomplete (e.g. `1 of 2 updated`), and
`kubectl rollout undo deployment/support-api` aborts back to the last good
revision. (If readiness *could* pass while the app is broken — bad health
check — this guarantee evaporates: that is why probes matter more than
strategy settings.)

**A4.** Liveness failing 3× (`failureThreshold: 3`, period 15 s) → kubelet
restarts the container: traffic continues to other ready replicas meanwhile;
the restarted container must pass readiness again before rejoining. If
instead readiness failed: the pod is pulled **out of the Service**
immediately (no new traffic), stays running, keeps retrying — no restart.
Rule of thumb: readiness protects *users* from bad pods; liveness protects
*you* from wedged pods — and a liveness probe that tests external
dependencies causes restart storms instead of fixing them.

**A5.** (a) 400m: above request, below limit — may burst while the node has
spare CPU, capped at 500m; no throttle, no kill. (b) sustained 600m →
**CPU throttled** at 500m: the process slows but stays alive. (c) 600 MB →
over the 512Mi memory limit → **OOMKill**; the container dies and the
Deployment replaces it. (d) no limits → the pod may starve co-tenant pods
on the node (noisy neighbour); clusters that permit this are inviting a
node-wide incident. Asymmetry to remember: CPU over limit = *slow*,
memory over limit = *die*.

**A6.** 70% of the **CPU request** (100m), i.e. 70 m. Someone reading it
as 70% of the limit (500m = 350 m) would think scaling begins at 350 m —
so they'd raise requests to make 70% land where they *think* the knee is,
paying for 3–5× the reservation while the HPA actually triggers at 70 m.
Cost is billed on requests, so this misreading is paid for every hour.

**A7.** (i) pods have ephemeral IPs — without a Service there is no stable
address to configure, and every client rewrites itself on each churn;
(ii) one name must fan out across replicas, which a DNS record to a pod
cannot do. Single-replica + restart policy wins when: one machine, one
consumer, downtime tolerance measured in seconds, and no one to operate a
cluster — the orchestration complexity buys nothing there (concepts §10).

**A8.** Cloud billing charges **reserved capacity** (requests × time),
whether or not you use it — utilisation is your efficiency ratio, not the
invoice line. The two levers that usually halve a team bill: (1)
**right-size requests** after measuring real usage (over-requesting is the
classic waste), (2) **scale down off-peak** via autoscaling/scheduled
scaling (you stop paying for peak replicas at 3 a.m.). Spot instances and
storage lifecycle are the next two, with trade-offs worth naming.

**A9.** Rule (Module 15): manifests are committed, values are not.
Mechanism: `kubectl create secret …` then `valueFrom.secretKeyRef` in the
Deployment — the value lives as a cluster object, mounted at runtime.
Honest limit: base64 is encoding, not encryption — anyone who can
`kubectl get secret` (or read etcd) has the value; RBAC/encryption-at-rest
are the real boundary, and cluster access itself is the privilege.

**A10.** The counter: Kubernetes earns its complexity only when you need
many replicas across machines, automated heal/rollout, or team-level
resource isolation — and it *adds* failure modes (probes that restart-loop,
crash-loops, control-plane ops) that a single supervised container does not
have. The deciding question: **"How many machines and how much downtime
tolerance do I actually have?"** One service on one box with a restart
policy is the professional choice when the answer is "one" — professionality
is choosing the smallest system you can operate, not the largest résumé
keyword.

---

**Scoring:** 8+ with sound reasoning → proceed to Module 17. 6–7 → re-read
concepts §§3–9, retry Q4, Q5, Q8. ≤5 → take lab Path A (or B) first; the
objects should then be concrete, not words.

---

[← Independent challenge](independent-challenge.md) · [Next: troubleshooting →](troubleshooting.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*