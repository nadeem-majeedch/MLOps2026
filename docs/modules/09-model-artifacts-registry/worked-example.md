# Worked example — the registry, observed

All output is **actual** from `python -m registry …` in `examples/churn/`
(registered straight after `python -m pipe.run`).

---

## 1. Register a version

```powershell
python -m registry register --model pipe_out/model.joblib `
    --metrics pipe_out/train_metrics.json --note "baseline, run 1"
```

```text
registered v001  model=f8aa5fa30b38f8d2  roc_auc=0.7163  gate=True
```

What landed on disk:

```
registry_store/
├── index.json          # versions + stage pointers + history
└── v001/
    ├── model.joblib    # a COPY (immutable: the original may change again)
    └── metadata.json   # lineage: data sha, metrics, gate, note, timestamp
```

`gate=True` came from `pipe_out/evaluation.json` — the Module 08 gate result
travels *with* the version.

## 2. Promote it properly

```text
v001: development -> staging
v001: staging -> production
```

## 3. The first refusal: you may not skip a stage

Registering a second version and jumping straight to production:

```powershell
python -m registry stage v002 production
```

```text
refused: v002 is 'development' and may only move one step at a time (next step: staging)
exit=1
```

Proceeding correctly:

```text
v002: development -> staging
v002: staging -> production
  production was v001 (rollback: python -m registry rollback production)
```

## 4. The second refusal: ungated versions never serve

Registering **without** an evaluation file:

```powershell
python -m registry register --model pipe_out/model.joblib `
    --metrics pipe_out/train_metrics.json --evaluation pipe_out/absent.json `
    --note "never gated"
```

```text
registered v003  model=f8aa5fa30b38f8d2  roc_auc=0.7163  gate=None
v003: development -> staging
refused: v003 never passed its quality gate (no evaluation.json provided) - production requires a passed gate
exit=1
```

Note `gate=None`: *unknown is not passed*. An unknown gate is exactly the
state you must not serve from.

## 5. Rollback — the way back, rehearsed

```powershell
python -m registry rollback production
python -m registry get production
```

```text
rollback: production v002 -> v001
C:\...\examples\churn\registry_store\v001\model.joblib
```

Final `list`:

```text
version   created               stage        roc_auc  gate   note
v001      2026-10-25T20:09:44+00:00 production   0.7163   True   baseline, run 1
v002      2026-10-25T20:09:44+00:00 staging      0.7163   True   retrain, run 2
v003      2026-10-25T20:09:45+00:00 staging      0.7163   None   never gated

stage pointers: {"staging": "v003", "production": "v001", "previous_production": "v002"}
```

The demoted `v002` returned to `staging` — a failed release goes back to
testing, not to being erased.

## 6. The audit trail

```powershell
python -m registry history
```

```text
at=... action=register  version=v001  by=student
at=... action=stage     version=v001  from=development  to=staging   by=student
at=... action=stage     version=v001  from=staging      to=production by=student
at=... action=register  version=v002  by=student
at=... action=stage     version=v002  from=development  to=staging    by=student
at=... action=stage     version=v002  from=staging      to=production by=student
at=... action=register  version=v003  by=student
at=... action=stage     version=v003  from=development  to=staging     by=student
at=... action=rollback  stage=production  from=v002  to=v001  by=student
```

Nine events, each attributable — this is what an incident reviewer reads
first.

## 7. One `show` for full lineage

```powershell
python -m registry show v001
```

```json
{
  "id": "v001",
  "created_at": "2026-10-25T20:09:44+00:00",
  "stage": "production",
  "note": "baseline, run 1",
  "model_file": "model.joblib",
  "model_sha256": "f8aa5fa30b38f8d2",
  "data_sha256": "e38d7738cf5524df",
  "data_file": "data/raw/churn.csv",
  "metrics": { "roc_auc": 0.7163, "accuracy": 0.91, "...": "..." },
  "gate": { "passed": true, "source": "evaluation.json",
            "detail": "roc_auc 0.7163 vs floor 0.7" },
  "previous_version": null
}
```

`data_sha256` is the lineage hook: it names *exactly* which extract this
model learned from — the same hash class the pipeline manifest records.

---

**Next:** [lab.md](lab.md) — reproduce this, then write the model card.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*