# Monitoring Report Template

> **How to use this file:** copy it to `MONITORING.md`. It is the standing
> document your monitoring produces — fill the plan before launch and the
> observations after. **Never write "drift detected, so we retrained" without
> labelled performance numbers** — drift alone is an invitation to
> investigate, not proof of degradation (Module 14). Delete italic guidance.

---

```markdown
# Monitoring report — <system name>

**Period covered:** <YYYY-MM-DD → YYYY-MM-DD> · **Model version:** <vNNN>
**Author:** <name> · **Status:** plan | first review | incident follow-up

## 1. What is monitored (the plan)
| Signal | Source | Metric | Threshold (with justification) | Response | Owner |
|---|---|---|---|---|---|
| input drift | prediction log vs reference | PSI per feature | ≥ 0.20 strong (convention; cite your source) | open investigation, check performance when labels land | … |
| performance | labelled outcomes | ROC-AUC / recall vs floor | drop > 0.0x vs reference | retrain ticket + rollback review | … |
| availability | service | error rate, p95 latency | > 1% / > SLO | page on-call | … |
| data contract | inbound records | validation failures | any | block + alert | … |

*Every threshold needs a one-line justification. "Because the library said
so" is not one.*

## 2. Reference window
**Reference data:** <path/hash> · **Date range:** <from → to> · **Why these
dates:** <e.g. normal trading period, excludes launch week>
*Required: without dates you cannot separate seasonality from drift.*

## 3. Prediction logging
- [ ] inputs (or lawful representation) logged — sample line: `<>`
- [ ] prediction + model version + timestamp logged — sample: `<>`
- [ ] outcome label joined later — method + latency: `<>`
- [ ] no raw personal identifiers in logs — evidence: `<grep/test output>`

## 4. Observations (period)
| Feature | PSI | Verdict | Notes |
|---|---|---|---|
| … | 0.0x | stable | |
| … | 0.5x | strong | window: <what changed> |

**Performance with labels (or "labels pending — due <date>"):**
| metric | reference | current | change | floor | verdict |
|---|---|---|---|---|---|
| ROC-AUC | 0.7662 | 0.7712 | −0.005 | 0.75 | within tolerance |

## 5. Decision (fill the 2×2)
|  | performance degraded | performance OK |
|---|---|---|
| **drift** | investigate root cause; consider rollback first | **monitor** + flip-conditions |
| **no drift** | suspect code/labels/leakage, not data | continue |

**Cell:** <> · **Decision:** retrain | monitor | roll back
**Evidence checked:** <list the exact numbers/outputs>
**Flip-conditions:** "I will change this decision if/when <specific measurable
condition> by <date>."

## 6. Actions taken
| action | who | when | result | follow-up |
|---|---|---|---|---|
| e.g. opened investigation | … | … | … | due <date> |

## 7. Honest limitations
*What this monitoring cannot see (e.g. fairness without group labels,
silent label delay, coverage gaps in logging).*
```

**Self-check:** could a colleague on call at 03:00 act on §1 without waking
you? And does §5 contain a *number* for every claim? If either is no, the
report is documentation, not monitoring.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*