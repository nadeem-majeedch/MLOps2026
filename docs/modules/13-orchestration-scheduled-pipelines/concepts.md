# Concepts — Module 13

*Vocabulary: orchestrator, scheduler, DAG (recalled), retry, backoff, timeout,
idempotency, catch-up, dead letter, alerting, alert fatigue, interval vs event
trigger, orchestration overhead, SLA.*

---

## 1. First, the honest question: do you need one?

Three levels of automation — pick the **smallest** that solves your problem:

| Level | Mechanism | Enough when… | Cost |
|---|---|---|---|
| **1. Script / Make** | you run it, or one OS timer calls it | one machine, one person, order already handled (Module 08) | ~0 |
| **2. Light runner** (this module) | interval loop + retries + history + alerts | unattended runs, needs an audit trail and failure visibility | ~200 lines |
| **3. Orchestrator platform** (Airflow/Prefect/Dagster) | many DAGs, UI, pools, multi-team, SLAs | dozens of workflows, dependencies across teams, compliance | heavy install, real ops |

**Orchestration is justified** when at least two hold: work must happen
*unattended on a schedule*; failures must *reach a human*; runs must be
*auditable after the fact*; multiple steps must *not* be re-run wastefully.
The trigger for this module's project was exactly that list — and a scheduled
`python -m pipe.run` in Task Scheduler satisfies none of retries, history, or
alerting by itself.

## 2. What the runner adds over Module 08

```
orchestrate/flow.py  =  the five pipe stages
                      +  decide whether work is needed (data hash / missing outputs)
                      +  schedule (--once | --every N --max-runs)
                      +  retries (--retries, --backoff)
                      +  history (orch_out/runs.jsonl, one JSON line per tick)
                      +  alerting (orch_out/ALERT.md on final failure, cleared on recovery)
```

**Tick** — one scheduled invocation. Each tick is idempotent: running a tick
twice with unchanged inputs converges to the same state (the skip logic makes
that explicit).

## 3. Retries and backoff — and their limits

- **Transient fault:** locked file, busy port, network hiccup → retrying
  usually succeeds. Policy here: `--retries 2` with `--backoff 1` seconds.
- **Deterministic fault:** broken config, contract violation, quality gate →
  it will fail identically every time. Retrying **burns time, doubles the
  alert noise, and delays the human**.

Our runner retries any task, but the docs and lab teach you to *read the
attempts list*: three identical error strings mean "stop retrying, start
thinking" (the failure demo shows exactly that shape). Real platforms express
this properly with per-task retry policies — the concept is the transferable
part.

**Timeouts** are the sibling control: a task that hangs forever is a stuck
scheduler. (Our stages are seconds-long; timeouts matter the moment a stage
calls a network service — name the knob even when you don't need it yet.)

## 4. The no-new-data skip: scheduling done right

The runner stores the last successful run's data hash. A tick with identical
data and intact outputs records `no_new_data` and exits 0. Why this matters:

- **Cost:** pointless retraining is the most common orchestrator time-sink.
- **Signal:** a history full of `success` runs that *did nothing* trains humans
  to ignore the log; explicit `no_new_data` lines keep the signal honest.
- **Trigger choice:** this is the seed of *event-driven* orchestration — "new
  file arrived" beats "every 15 minutes, hope a file is there". Interval is
  the default here because polling is simpler to teach and debug; production
  systems often add file/webhook events on top.

## 5. Alerting without alert fatigue

A failed tick writes `orch_out/ALERT.md`: run id, failed task, **every
attempt's error**, and what to do next. On a successful tick the file is
deleted — a recovered system stops shouting.

Design rules (they generalize to Module 14):
1. **Alert on state changes**, not every tick (repeat-failure emails train
   people to delete mail).
2. The alert must carry **diagnosis**, not just news (attempts, error text).
3. **Every alert needs an owner and an action** — an alert nobody can act on
   is noise with a deadline.
4. Delivery (email/Slack/webhook) is a *pluggable sink* — this module writes a
   file so it works offline; the concept transfers directly.

## 6. History as evidence

`runs.jsonl` — one line per tick: id, trigger, status (`success` /
`failed` / `no_new_data`), duration, data hash, per-task attempts. Answers
later questions: *When did we last retrain? How long do runs take? Has this
failed before?* This is the operational counterpart to Module 09's lineage:
registry explains *what a model is*, history explains *what the system did*.

## 7. Tool comparison — evidence, not fashion

| Tool | Shape | Strength | Watch out for |
|---|---|---|---|
| **cron / Task Scheduler** | OS timer → command | zero dependencies | no retries/history/alerts; misconfig is silent |
| **This runner** (course) | Python loop, readable code | transparent, offline, 200 lines | single machine, no UI, no multi-team features |
| **Prefect** | Python-defined flows, hybrid server | flows look like plain Python; good UX | needs a server/cloud for full features |
| **Dagster** | Software-defined assets, lineage-first | asset graph = data lineage view | steeper model, heavier install |
| **Airflow** | DAG-XML/Python, scheduler + web UI | the industry default; huge ecosystem | notoriously heavy; UI/infra to operate; easy to over-engineer |
| **Hosted (Cloud Composer, etc.)** | managed Airflow/etc. | no ops burden | ☁️ cost, account, lock-in |

**Rule of thumb (and the module's thesis):** one pipeline, one machine, one
person → level 1–2. Ten pipelines, cross-team SLAs, compliance audit → level 3.
Airflow on a laptop for a single student pipeline is the classic
over-engineering this course warns against — and the syllabus's design
principle *"avoid unnecessary enterprise complexity for beginners"* is
enforced right here.

## 8. What orchestration does NOT fix

Orchestration automates **what you already have**. Broken tests (Module 07),
weak gates (08), missing lineage (09), silent drift (14) arrive on schedule
and fail on schedule. Automation amplifies quality — in both directions.

---

**Next:** [worked-example.md](worked-example.md) — five ticks, all captured.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*