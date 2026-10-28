# LAB-18 — Regression on Duty: Roll Back?

## 1. Lab identity

| | |
|---|---|
| **Lab ID** | **LAB-18** |
| **Difficulty / topic** | 🚀 Advanced · Performance regression & rollback decision |
| **Prerequisite module** | [14 — Monitoring, drift, retraining](../modules/14-monitoring-drift-retraining/index.md) + [09 — Registry & rollback](../modules/09-model-artifacts-registry/index.md) |
| **Fixture** | `examples/labs/lab-18/` |
| **Estimated time** | 90 minutes · free, local, offline |

## 2. Scenario and background

`v2` shipped four days ago. The ledger holds the evidence: quality
metrics, p95 latency, error rate, and a serving window with **6 alerts**
and a mean AUC below the floor — while `v1` ran 21 calm days. Someone
says "it's only 4 days of data"; someone else says "the error rate went
13×". Your call, in writing, with the ledger as your only authority —
then execute it and let the audit trail show your reasoning.

## 3. Learning objectives

By the end you can:

1. Assemble a rollback decision from evidence (quality, latency,
   reliability, monitoring window) rather than from preference.
2. Argue both sides: sample size vs severity, drift vs degradation.
3. Execute a rollback as a recorded operation with a stated reason —
   and read the audit trail afterwards.
4. Define the "rollback threshold" for your system *before* the next
   incident, in numbers.

## 4. Prerequisites and estimated time

- Modules 09 + 14 read; LAB-15 recommended.
- No dataset (seeded ledger ships with the fixture).
- **90 min** (read evidence 20 · argue 30 · execute 10 · thresholds 20 ·
  write-up 10).

## 5. Student task statement

Write `rollback-decision.md`: the evidence table for `v1` and `v2`, both
positions argued fairly, your verdict (roll back / keep / partial
mitigation) with the numeric thresholds that justified it, then execute
via `runs_ledger.py decide` with a substantive `--reason`, and paste the
ledger + history afterwards. Finish with a pre-written "rollback
thresholds" card for the *next* incident.

## 6. Required dataset and setup instructions

```powershell
# 🪟 Windows — PowerShell — from examples/labs/lab-18
python runs_ledger.py list
python runs_ledger.py show v1
python runs_ledger.py show v2
```

## 7. Starter files

| File | Role |
|---|---|
| `runs_ledger.py` | seeded ledger + `list` / `show` / `decide` / `history` |
| `ledger.json` | generated on first run (seeded data) |
| `history.jsonl` | your decisions, appended with reasons |
| `rollback-decision.md` | **you write it** |

Evidence in the seed (verify it yourself):
`v1`: auc 0.7841 · p95 38 ms · err 0.2% · 21 days · mean_auc 0.7798 · 0 alerts · PSI 0.04.
`v2`: auc 0.7613 · p95 118 ms · err 2.6% · 4 days · mean_auc 0.7302 · 6 alerts · PSI 0.31 + 2 timeout spikes.

## 8. Numbered implementation steps

**Step 1 — Inventory the evidence** (§6 commands). Build your comparison
table: 7 rows × 2 releases. ✅ table pasted into `rollback-decision.md`.

**Step 2 — Argue "keep v2"** (3+ sentences): what 4 days of data cannot
show; recall *improved* (0.41 → 0.47); latency may be a warm-up artefact.

**Step 3 — Argue "roll back"** (3+ sentences): mean AUC below the 0.75
floor; error rate ×13; PSI 0.31 says inputs moved; 6 alerts.

**Step 4 — Verdict + thresholds.** Decide. State the numeric triggers
you used (e.g. "mean AUC < floor", "error rate > 1% sustained", "≥3
alerts/48h") — then generalise them into a **threshold card** for future
incidents. ✅ card written *with numbers*, not adjectives.

**Step 5 — Execute.**
```powershell
python runs_ledger.py decide v2 --rollback --reason "mean_auc 0.7302 below floor 0.75 after 4 days, 6 alerts, err 2.6% vs v1 0.2%; recall gain does not offset reliability loss"
python runs_ledger.py list      # ✅ serving: v1 ; v2 state: rolled_back
python runs_ledger.py history    # ✅ your entry with the reason
```
(The command above is the recorded demo run from the authoring machine;
your reason must be your own words.)

**Step 6 — The mirror case.** One paragraph: what evidence would make you
**keep** a worse-looking model (e.g. product-mandated recall target,
seasonal confound, A/B in flight)? Name the missing measurement.

**Step 7 — Roll forward plan.** Two lines: what v3 must prove before it
ships again (gate, soak window, monitoring trigger).

## 9. Commands and expected results

| Command | Expected |
|---|---|
| `python runs_ledger.py list` | v1 superseded · v2 current · `serving: v2` |
| `python runs_ledger.py show v2` | full JSON incl. window (6 alerts, mean 0.7302) |
| `python runs_ledger.py decide v2 --rollback` (no reason) | **refused**: needs `--reason` |
| `… decide v2 --rollback --reason "<your sentence>"` | `rolled back v2 -> v1` |
| `python runs_ledger.py list` (after) | `serving: v1`, v2 `rolled_back` |
| `python runs_ledger.py history` | your entry: action, from, to, reason |

## 10. Acceptance criteria (objective)

- [ ] Evidence table (7 rows × 2) pasted from `show` output.
- [ ] Both positions argued (3+ sentences each), fairly stated.
- [ ] Verdict + numeric triggers; threshold card written.
- [ ] `--reason`-less attempt refused (evidence the tool enforces
      reasoning).
- [ ] Rollback executed; `list` shows `serving: v1`; `history` shows
      your reason.
- [ ] Mirror case + roll-forward plan paragraphs.

## 11. Troubleshooting and recovery

| Symptom | Cause | Fix |
|---|---|---|
| `no previous release to roll back to` | ledger reset/re-seeded | rerun §6 (seed restores both releases) |
| `a decision needs a real reason` | `--reason` missing or <10 chars | give a sentence with numbers |
| `ledger.json` left rolled_back from a previous attempt | state persists by design | delete `ledger.json` to re-seed for a fresh attempt |
| `no such release` | typo (v2 vs rc-2) | `list` first |
| history lost after delete | history is a file like any other | note it in cleanup: submit before deleting |

## 12. Reflection questions

1. Where is the line between "small sample" and "damage"? What would
   make day 5 decisive without waiting for day 21?
2. Rollback is cheap here. What makes rollback *expensive* in real
   systems (data written by v2, schema changes) and what does that cost
   your threshold card?
3. The recall gain (0.41→0.47) favours v2. Which stakeholder owns that
   trade-off — and does your decision document name them?

## 13. Optional challenge tasks

1. Add `decide --partial`: pin v2 to 10% of traffic (describe the
   mechanism your ledger would need).
2. Write `v3-criteria.json` and connect it to LAB-15's gate so the
   roll-forward is mechanical.
3. Simulate a false alarm: a 5th day where v2's mean AUC recovers to
   0.77 — update your threshold card to show what *would* change your
   verdict.

## 14. Rubric / checklist

| Points | Criterion |
|---|---|
| 3 | evidence table complete from tool output |
| 4 | both sides argued fairly (3+ sentences each) |
| 3 | verdict with numeric triggers + threshold card |
| 2 | refusal-without-reason demonstrated |
| 3 | rollback executed; ledger + history pasted |
| 2 | mirror case + roll-forward plan |
| **17** | **total** · ≥13 = pass |

## 15. Cleanup

```powershell
cd examples\labs\lab-18
# submit BEFORE deleting: keep rollback-decision.md + history.jsonl
Remove-Item ledger.json, history.jsonl -ErrorAction SilentlyContinue   # re-seeds fresh next run
```

---

**After attempting:** a reference decision structure + threshold card
live in [`examples/labs/solutions/lab-18/`](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/labs/solutions/lab-18).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../about/index.md).*