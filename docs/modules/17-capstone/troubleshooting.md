# Troubleshooting — Module 17

Capstone problems are *integration* problems: each link works alone; the
seams fail. Symptom → cause → fix.

## The chain

| Symptom | Likely cause | Fix |
|---|---|---|
| Pipeline green, but README commands differ from reality | docs written from memory, not transcripts | re-run every command verbatim (lab Step 2 rule); fix docs, then restate claims |
| Tests pass, gate passes, but a stale `model.joblib` is what the API serves | artefacts and releases out of sync | check `release.json` `current` → `/health` `model_source`; re-register or roll back |
| `data_sha256` changed "by itself" | regenerated data with different code/seed, or CSV row order differs | regenerate with the committed `generate_data.py` + seed; if it still differs, your pipeline is not deterministic — fix that first (it's a hard-condition failure) |
| Two machines disagree on AUC | undeclared tolerance or environment drift | declare tolerance (e.g. ±0.01) **before** comparing; check pinned versions match (Module 02) |
| CI red only on GitHub, green locally | missing dependency in the CI install step, or untracked file the job needs | read the first failing job's log; add the dependency/generate step (Module 12 patterns) |
| Docker row always NOT RUN | no container runtime | label it honestly, or run Module 11's lab on a machine that has Docker — do not invent a build |
| Monitoring decision flips run to run | window too small / labels absent | size the window deliberately and state it; absence of labels caps the decision at MONITOR (Module 14) |

## The review (Lab 17)

| Symptom | Likely cause | Fix |
|---|---|---|
| Checklist verdicts are all PASS in under 5 minutes | checks written as opinions | Step 1: every row needs a command + expected result; re-run |
| Fault injection "detected" only by you watching | detection not wired to tooling | pick a fault whose path goes through validation/gate/refusal — those report themselves |
| Rollback refuses: `nothing to roll back to` | only one release ever promoted | register a second release first (lab Step 6) |
| Fault B didn't fail the gate | floor edited *below* the AUC | the injection raises the floor **above** 0.7662; verify `report.md` says FAIL |
| You edited the reference while reviewing | fixing instead of reviewing | restore by hand (no git resets in this course); repairs belong in *your* capstone |

## Scope and motivation

| Symptom | Resolution |
|---|---|
| "My capstone should be bigger" | MVP first — extensions score nothing until the hard conditions are green (concepts §3) |
| "Every scenario needs real data" | never for this course: synthetic or openly licensed only (concepts §4) |
| Evidence assembly is taking longer than building | evidence should be captured **as you go** (challenge §4) — rebuild the habit, don't marathon it |
| Stuck on where a link belongs | walk [concepts §1](concepts.md) — every part names its forging module |

General environment problems:
[course troubleshooting](../../troubleshooting/index.md). Fixture-specific
issues: each earlier module's own troubleshooting page (they are linked
from every module index).

---

[← Knowledge check](knowledge-check.md) · [Next: references →](references.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*