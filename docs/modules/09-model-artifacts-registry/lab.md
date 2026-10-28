# Lab 09 — Ship v1, prepare the rollback

## 1. Scenario and business problem

The model you have been building is ready for the application team. They want
one URL to point at, and you need to be able to take a bad release back within
minutes. Last quarter a competitor shipped an unreviewed model and could not
revert it for three days.

**Business problem:** release model versions with reviewable lineage, staged
promotion, and a rehearsed one-command rollback — none of which exist if the
"registry" is a folder called `models_final_v3(2).pkl`.

## 2. Skills practising

- Registering a model with complete lineage (data hash, metrics, gate).
- Enforcing promotion rules and reading a refusal as a *success* of the system.
- Executing and verifying a rollback.
- Writing a model card a reviewer could act on.

## 3. Prerequisites

- [concepts.md](concepts.md) read (§1–§7).
- `python -m pipe.run --clean` green (you need `pipe_out/evaluation.json`).
- Free, local, no accounts.

## 4. Required tools and estimated time

| Item | Detail |
|---|---|
| Tools | Python 3.10+, the `registry/` package (ships with the repo) |
| Cost | Free, local, offline |
| ⚠️ Resource-heavy | none |
| ⏱️ Estimated time | 130 minutes |

## 5. Input data and how to obtain it

```powershell
# 🪟 from examples/churn
python -m pipe.run --clean        # ✅ "pipeline complete"
python -m registry list           # ✅ "registry is empty" (or your versions)
```

## 6. Directory layout

```
examples/churn/
├── registry/
│   ├── __init__.py
│   └── __main__.py     # register | list | show | stage | rollback | get | history
├── registry_store/     # generated: index.json + vNNN/ folders
├── pipe_out/           # the model + metrics + gate you will register
└── config.yaml         # quality.roc_auc_floor (the gate the registry checks)
```

## 7. Setup and execution steps

**Step 1 — Register v1 with a real note.**
```powershell
python -m registry register --model pipe_out/model.joblib `
    --metrics pipe_out/train_metrics.json --note "baseline for API launch"
python -m registry show v001
```
✅ **Checkpoint:** `metadata.json` shows `data_sha256`, `gate.passed: true`.

**Step 2 — Promote v1 the long way.**
```powershell
python -m registry stage v001 staging
python -m registry stage v001 production
python -m registry get production
```
✅ **Checkpoint:** `get` prints the `v001` path.

**Step 3 — Try to break the rules (and watch them hold).**
```powershell
python -m registry register --model pipe_out/model.joblib `
    --metrics pipe_out/train_metrics.json --note "fast-track attempt"
python -m registry stage v002 production        # expect refusal, exit 1
python -m registry register --model pipe_out/model.joblib `
    --metrics pipe_out/train_metrics.json --evaluation nope.json --note "ungated"
python -m registry stage v003 staging
python -m registry stage v003 production        # expect refusal, exit 1
```
✅ **Checkpoint:** both refusals captured with their exact messages.

**Step 4 — Ship a proper v2, then roll back.**
```powershell
python -m registry stage v002 staging
python -m registry stage v002 production
python -m registry rollback production
python -m registry history
```
✅ **Checkpoint:** history shows the rollback event `from=v002 to=v001`, and
`get production` again returns v001.

**Step 5 — Prove the switch really matters (preview of Module 10).**
```powershell
python -m service           # second terminal: health shows model_version
```
Read `/health` (`Invoke-RestMethod http://127.0.0.1:8000/health` 🪟 /
`curl -s localhost:8000/health` 🐧), note `model_version`, roll back, restart,
and check it again.
✅ **Checkpoint:** the served version follows the registry pointer.

**Step 6 — Write the model card** for the production version, one page,
using exactly these headings:

```
1. Model & version          (id, sha, registered date)
2. Intended use             (what decisions it supports; who may use it)
3. Out-of-scope use         (what it must NOT be used for)
4. Training data            (source, size, sha256, time window)
5. Evaluation               (metrics + the threshold honesty: precision@0.5 = 0)
6. Limitations & risks      (populations not covered, known warts)
7. Rollback                 (exact command + expected effect)
```

✅ **Checkpoint:** a reviewer could answer "may I use this for X?" from §2/§3 alone.

## 8. Expected outputs and verification

| Step | Expected | Verify |
|---|---|---|
| 1 | `registered v001 ... gate=True` | `show v001` |
| 2 | stage transitions + path from `get` | console output |
| 3 | two `refused:` lines, exit 1 each | `echo $LASTEXITCODE` |
| 4 | `rollback: production v002 -> v001` in history | `history` |
| 5 | served `model_version` matches pointer | `/health` before/after |
| 6 | one-page card, §1–§7 filled | self-review against lab §9 |

## 9. Acceptance criteria

- [ ] ≥2 versions registered; metadata contains data hash, metrics, gate result.
- [ ] Both refusals captured verbatim (stage-skip and ungated promotion).
- [ ] A rollback executed **and verified** via `history` + `get production`.
- [ ] `/health` observed changing with the pointer (or, if you skipped Step 5,
      an explanation of why the pointer is what the service reads).
- [ ] Model card complete, including an honest metrics paragraph.
- [ ] Everything filed as `modules/09/`.

## 10. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `missing model file` | `pipe_out/` not built | `python -m pipe.run --clean` |
| `gate=None` on registration | `pipe_out/evaluation.json` absent | Run the pipeline (stage `evaluate` writes it) |
| `refused: no recorded previous production` | Nothing was ever promoted to production twice | Promote v002 first, then roll back |
| `get production` prints nothing / errors | No pointer set | `list` to see stage pointers; promote first |
| `no such version` | Typo'd id | `python -m registry list` |
| Health shows `artefact` not `vNNN` | Registry empty or service started before registering | Register+promote, then restart the service |

More: [troubleshooting.md](troubleshooting.md).

## 11. Cleanup

```powershell
# 🪟 from examples/churn — registry is generated state; keep it if you want
# evidence, delete it to reset the exercise:
Remove-Item -Recurse registry_store -ErrorAction SilentlyContinue
Remove-Item -Recurse pipe_out -ErrorAction SilentlyContinue
python -m pipe.run              # rebuild for the next module
python -m pytest                # ✅ green
```

## 12. Optional extension tasks

1. **Alias convention:** add a `champion`/`challenger` alias command and point
   the service at `challenger` via an environment variable.
2. **Retirement:** implement `python -m registry archive v003` with a rule
   ("archived versions are excluded from `list` but kept in `history`").
3. **Remote comparison:** with an MLflow tracking server (☁️ optional), run the
   same promotion through `mlflow models` and write a 200-word feature map
   between the two.

---

**Next:** [independent-challenge.md](independent-challenge.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*