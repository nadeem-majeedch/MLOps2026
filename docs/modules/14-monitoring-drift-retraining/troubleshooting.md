# Troubleshooting — Module 14

Symptom → likely cause → fix. See the
[course troubleshooting hub](../../troubleshooting/index.md) for Python issues.

---

## 1. Logging

| Symptom | Likely cause | Fix |
|---|---|---|
| `no model: run python -m pipe.run first` | Monitor resolves the model like the service does | Build the model (or register + promote) first |
| Records all have `actual: null` | You never passed `--labels` | Correct for live systems; to measure performance, log the window again **with** `--labels` (it appends labelled rows) |
| Log shows only one scenario | `baseline` without `--append` replaces the log by design | Use `--append` (or non-baseline scenarios, which append) when you need a mixed history |
| Timestamps all identical within a window | One `ts` per batch — honest for batch scoring | Fine for teaching; a production logger would stamp per request |

## 2. Drift report

| Symptom | Likely cause | Fix |
|---|---|---|
| `no reference: run --snapshot first` | Reference snapshot missing | Snapshot **before** you shift anything — reference = known-good state |
| `DRIFT DETECTED` on a window you know is identical | Reference is stale (taken from an older regime) or you snapshotted *after* a change | Re-baseline deliberately and record that you did (moving the baseline is a decision, not a default) |
| One feature always "strong" | Measurement/schema difference vs reference (units, encoder) | Check the Module 04 contract on both files before believing the world changed |
| `psi=-` on a categorical row | Not an error: categorical rows use the mix-shift measure | Read the measure column in the report table |
| Everything "significant" with huge data | p-values scale with N | Report PSI/KS **effect sizes** alongside p (concepts §4) |
| PSI looks odd on tiny samples | Few distinct values → collapsed bins | Treat small-window PSI as inconclusive; widen the window |

## 3. Performance report

| Symptom | Likely cause | Fix |
|---|---|---|
| `no labelled records yet: accuracy cannot be measured` | Labels haven't arrived | Working as designed — this is the *point* of the module; wait, or log with `--labels` for simulation |
| Baseline row flagged DEGRADED (0.6902 vs floor 0.70) | Window noise: 400 rows vs the 0.7163 test set | Expected at this window size — see lab Step 6; consider multi-window confirmation or the drop tripwire as primary |
| AUC ≈ 0.5 across all windows | Labels misaligned with predictions (join/order bug), or you logged `actual` from a different source | Check `customer_id` joins and that `actual` came from the same window |
| Identical metrics for shift and degrade | Reused the same scenario twice (filter issue) | Inspect `scenario` field values in `predictions.jsonl` |

## 4. Decision script

| Symptom | Likely cause | Fix |
|---|---|---|
| `missing drift_report.json` | Ran decision out of order | Chain: log → drift → performance → decision |
| Decision ignores a window you care about | Decision evaluates the **latest** window (by timestamp) | Re-log that window last, or read all rows of the performance report — the matrix keys on the most recent evidence |
| Always MONITOR despite visible degradation | Your degraded window isn't the latest, or labels missing on it | Confirm `performance` shows it as `DEGRADED` before `decision` runs |

## 5. Conceptual triage — when a real alert arrives

1. **Contract first:** is it measurement change? (Module 04 checks on both
   sides of the comparison.)
2. **Window second:** size, seasonality, sample noise — the lab Step 6
   argument is your template.
3. **Labels third:** only then ask whether accuracy actually fell.
4. **Then act** per the matrix — and record the decision either way. A
   documented MONITOR is a result; an unexamined retrain is a gamble.

## 6. Recovery smells

- **Retrained, no improvement** — you probably had case (no drift, degraded):
  inputs looked fine, so a retrain on the same distribution reproduces the
  same failure. Read the INVESTIGATE quadrant's guidance first.
- **Alerts quiet after a retrain** — check you didn't re-snapshot the
  reference to the *new* regime without noting it; quiet ≠ healthy.
- **Nobody trusts monitoring anymore** — alert fatigue (concepts §5): audit
  which alerts produced action last month; retire or re-threshold the rest.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*