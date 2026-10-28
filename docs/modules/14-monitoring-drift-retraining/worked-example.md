# Worked example — two windows, two decisions

All output is **actual** from `python -m monitoring.*` in `examples/churn/`.
The "world changing" is synthetic and scripted (`log_predictions.py`
scenarios) — clearly labelled in every record. The *statistics and decisions*
are real computations on those synthetic windows.

---

## 1. Instrument, then take a reference

```powershell
python -m monitoring.log_predictions --scenario baseline --labels
python -m monitoring.drift --snapshot
```

```text
logged 400 predictions  scenario=baseline  labels=yes  -> monitoring/predictions.jsonl
reference snapshot written -> monitoring/reference.csv (2000 rows)
```

## 2. Window 2 — the world shifts (labels not yet arrived)

```powershell
python -m monitoring.log_predictions --scenario shift
python -m monitoring.drift
```

```text
logged 400 predictions  scenario=shift  labels=not yet  -> monitoring/predictions.jsonl
overall: DRIFT DETECTED
  tenure_months     stable    psi=0.0155
  monthly_charges   moderate  psi=0.1309
  support_tickets   strong    psi=0.5877
  contract_type     strong    psi=-
-> monitoring/drift_report.md
```

Four features, four verdicts against the **stated** rule (PSI > 0.20 strong).
Note `psi=-` for `contract_type`: it is categorical — that row uses the
category-mix measure instead (the table shows which measure applies).

`drift_report.md` ends with the caveat the tool itself prints:

> Drift shows inputs changed - it does NOT show the model is wrong.
> Check monitoring/performance.py before acting.

## 3. Labels arrive → performance report (case A: drift **without** degradation)

```powershell
python -m monitoring.log_predictions --scenario shift --labels
python -m monitoring.performance
```

```text
baseline   roc_auc=0.6902 drop=0.0261 -> DEGRADED
shift      roc_auc=0.7578 drop=-0.0415 -> within tolerance
-> monitoring/performance_report.md
```

Two teaching moments in one table:

1. **The shifted window scored *better* than reference** (0.7578 vs 0.7163)
   despite `DRIFT DETECTED`. Inputs moved; ranking survived — drift was not
   degradation. (Why possible? The shift changed `P(X)`, not `P(Y|X)` —
   concepts §3.)
2. **The 400-row baseline window reads 0.6902 — below the 0.70 floor** —
   while the full 400-row test set measured 0.7163. Same model, different
   sample: that is **window noise** (LO 14.3), and it is exactly why alerts
   need effect-size thresholds and multi-window confirmation rather than a
   single fragile number.

## 4. Decision A — the hard part: *don't* retrain

```powershell
python -m monitoring.decision
```

```text
drift='DRIFT DETECTED'  latest_window='shift'  degraded=False
decision: MONITOR
-> monitoring/decision.md
```

`decision.md` (real content, excerpt):

```markdown
## Decision: **MONITOR**

Distribution moved but measured performance has NOT dropped. Drift alone is
not evidence of a bad model - retrain only after labels show degradation
(or drift persists and degrades later).

## Human review checklist
- [ ] I read the drift report and know WHICH features moved.
- [ ] I read the performance report and know WHETHER labels agree.
...
```

## 5. Window 3 — the rules change (labels arrive)

```powershell
python -m monitoring.log_predictions --scenario degrade --labels
python -m monitoring.performance
python -m monitoring.decision
```

```text
baseline   roc_auc=0.6902 drop=0.0261 -> DEGRADED
shift      roc_auc=0.7578 drop=-0.0415 -> within tolerance
degrade    roc_auc=0.5384 drop=0.1779 -> DEGRADED
drift='DRIFT DETECTED'  latest_window='degrade'  degraded=True
decision: RETRAIN CANDIDATE
```

AUC collapsed from 0.7163 (reference) to **0.5384** — barely above coin-flip —
and the drop (0.1779) blows past both tripwires. Now drift and labels *agree*:

```markdown
## Decision: **RETRAIN CANDIDATE**

Drift AND measured degradation agree. Prepare a retrained candidate, run the
full pipeline and gates (Module 08), register it (Module 09), and promote only
after review.

## Human review checklist
- [ ] I read the drift report and know WHICH features moved.
- [ ] I read the performance report and know WHETHER labels agree.
- [ ] If retraining: run `python -m pipe.run --clean` and confirm the quality gate passes.
- [ ] Register the candidate: `python -m registry register ...`.
- [ ] Know the way back BEFORE promoting: `python -m registry rollback production`.
```

## 6. The asymmetry, side by side

| | Window 2 (`shift`) | Window 3 (`degrade`) |
|---|---|---|
| Drift | DRIFT DETECTED (PSI 0.59) | DRIFT DETECTED |
| Labels say | AUC **0.7578** (better) | AUC **0.5384** (collapsed) |
| Decision | **MONITOR** | **RETRAIN CANDIDATE** |
| Human action | keep watching, no retrain | full loop + rollback known first |

Same drift verdict, opposite actions — because only the second report is
allowed to speak about accuracy, and it needed `actual` to do it.

---

**Next:** [lab.md](lab.md) — reproduce both cases and defend the decisions.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*