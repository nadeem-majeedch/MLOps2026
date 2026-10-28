# Experiment Record Template

> **How to use this file:** copy it to `EXPERIMENTS.md` (capstone component
> *tracking & selection*, and [MP2](../assessments/mini-projects.md)). One
> record per campaign; keep the tracker's own export (screenshot/CSV) linked,
> never retyped. The **selection rule must be written before the results are
> looked at** — dated, in section 2. Delete italic guidance lines.

---

```markdown
# Experiment record — <campaign name>

**Run dates:** <start → end> · **Tracker:** MLflow (local) | tracked-runs.jsonl
**Dataset:** <name> · **version/hash:** <sha256 or id> · **Code commit:** <sha>
**Compute:** local CPU · seed policy: <fixed / swept, stated>

## 1. Question
*One sentence: what decision will these runs inform? Include the baseline you
are trying to beat and why it is the right baseline.*

## 2. Selection rule (written BEFORE looking at results)
*Date it. Example: "Choose the run with the highest ROC-AUC among those with
recall ≥ 0.40 on validation; tie-break: lower p95 latency; if none qualify,
keep the baseline and report why."*

**Rule frozen at:** <YYYY-MM-DD HH:MM>

## 3. Configuration space
| Knob | Values tried | Why this range |
|---|---|---|
| e.g. learning rate | … | … |
| e.g. features included | … | … |

## 4. Runs
| run id | parameters | ROC-AUC | recall | precision | other | notes |
|---|---|---|---|---|---|---|
| 001 (baseline) | … | … | … | … | … | reference row |
| 002 | … | … | … | … | … | |
| … | | | | | | *(≥10 rows for MP2)* |

## 5. Selection (apply §2 mechanically)
**Rule applied:** <copy of §2>
**Selected run:** <id> — **why the rule says so:** <one line quoting the
numbers>.
**Rejected runners-up and why:** <at least one, with numbers>.

## 6. Final evaluation (test set — touched ONCE)
| model | ROC-AUC | recall | precision | vs baseline |
|---|---|---|---|---|
| selected | … | … | … | +0.0x / −0.0x |

**Known limitations:** <e.g. single split; class imbalance; latency not
measured at peak>. *At least one, honestly.*

## 7. Artefact
**Model file:** <path> · **sha256:** <hash> · **registry version:** <vNNN>
**Reproduce with:** `<exact command>` · **Tracker link/export:** <path or link>
```

**Self-check:** could someone reproduce your table from the recorded hash and
command alone — and would your §2 rule, applied by a stranger to §4, pick the
same winner? If not, the "selection" is a story, not a procedure.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*