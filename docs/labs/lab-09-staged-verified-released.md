# LAB-09 — Staged, Verified, Released

## 1. Lab identity

| | |
|---|---|
| **Lab ID** | **LAB-09** |
| **Difficulty / topic** | 🔧 Intermediate · Model artefacts & release candidates |
| **Prerequisite module** | [09 — Model artifacts, registries, promotion](../modules/09-model-artifacts-registry/index.md) |
| **Fixture** | `examples/labs/lab-09/` |
| **Estimated time** | 105 minutes · free, local, offline |

## 2. Scenario and background

`stager.py` manages release candidates for the subscription-risk model:
`stage → verify → approve`. The lifecycle works. The integrity story does
not: `verify` proves the files **exist**, and `approve` trusts it. The
lab's punchline (do it yourself): corrupt one staged byte and watch the
gate still answer `VERIFY OK` — then approve a corrupted candidate. Your
task is to make bytes, not filenames, the thing that is checked.

## 3. Learning objectives

By the end you can:

1. Explain the release-candidate lifecycle: stage → verify → approve,
   with an audit record at every step.
2. Implement integrity verification (sha256 recorded at stage time,
   re-checked at verify **and** approve).
3. Demonstrate a tamper being *refused*, with the exit code and message.
4. Separate "exists", "matches spec", and "was approved by a human" —
   three different assertions.

## 4. Prerequisites and estimated time

- Module 09 read (registry + promotion vocabulary); Module 15 §3 helps.
- **105 min** (reproduce the hole 20 · implement 40 · evidence 30 ·
  write-up 15).

## 5. Student task statement

Upgrade `stager.py` (your copy) so that: (a) staging records a full
sha256 per file in the manifest; (b) `verify` recomputes and compares,
exiting 1 on any mismatch; (c) `approve` re-verifies and refuses a
tampered candidate; (d) a `test_integrity.py` proves the refusal
programmatically. Deliver before/after transcripts of the tamper drill.

## 6. Required dataset and setup instructions

```powershell
# 🪟 Windows — PowerShell — from examples/labs/lab-09
python prepare_build.py     # ✅ build/ ready: config.yaml, metrics.json, model.joblib
python stager.py stage      # ✅ staged rc-1: 3 files
python stager.py verify     # ✅ rc-1: VERIFY OK (3 file(s))
```
Now the hole, as shipped:
```powershell
python -c "import pathlib; p=pathlib.Path('staged/rc-1/model.joblib'); p.write_bytes(p.read_bytes()+b'\x00TAMPERED')"
python stager.py verify     # ✅ EXPECTED FAULT: still "VERIFY OK", exit 0
python stager.py approve rc-1   # ✅ EXPECTED FAULT: "APPROVED", exit 0
```

## 7. Starter files

| File | Role |
|---|---|
| `prepare_build.py` | trains + writes `build/` (real bytes to stage) |
| `stager.py` | lifecycle with the integrity hole (commented) |
| `test_integrity.py` | **you write it** (starter assertions in solutions) |

## 8. Numbered implementation steps

**Step 1 — Stage normally** (§6 commands) and inspect
`staged/manifest.json`: what exactly is recorded per file?
✅ Checkpoint: you can state the difference between `{"exists": true,
"size": n}` and a digest.

**Step 2 — Run the tamper drill** (§6). Capture both outputs.
✅ Checkpoint: `VERIFY OK` on corrupted bytes — the hole, in writing.

**Step 3 — Record digests.** At stage time store `sha256` (full 64 hex)
per file, plus the candidate's *own* manifest hash.

**Step 4 — Verify bytes.** `verify` recomputes each digest; mismatch →
print file, expected, actual; exit 1.

**Step 5 — Protect approval.** `approve` calls the real verifier first;
refuse with `exit 1` and do **not** change state.

**Step 6 — Prove it.** Re-run the drill: staged → corrupt → `verify`
must now fail; `approve rc-1` must refuse; then `rm -rf staged && python
prepare_build.py && python stager.py stage` to restore a clean candidate
and show approve succeeding again.

**Step 7 — Tests.** `test_integrity.py`: (a) clean stage verifies OK;
(b) tampered file → verify exit 1; (c) tampered → approve refuses and
manifest state stays `staged`. ✅ pytest green.

**Step 8 — One paragraph:** how this connects to Module 09's registry
record and Module 15's supply-chain integrity (same triple: integrity,
provenance, freshness).

## 9. Commands and expected results

| Command | As shipped (the fault) | After your fix |
|---|---|---|
| `python stager.py stage` | staged, weak manifest | staged + sha256 per file |
| corrupt + `python stager.py verify` | `VERIFY OK`, exit 0 | **mismatch listed**, exit 1 |
| corrupt + `python stager.py approve rc-1` | `APPROVED`, exit 0 | **refused**, exit 1, state unchanged |
| `python stager.py list` | `staged` | after refusal still `staged` (never `approved`) |
| `python -m pytest test_integrity.py -q` | (none yet) | all green |

## 10. Acceptance criteria (objective)

- [ ] Tamper drill "before" captured (`VERIFY OK` + `APPROVED`).
- [ ] Manifest records full sha256 per file (and candidate digest).
- [ ] `verify` exits 1 on tamper, naming file/expected/actual.
- [ ] `approve` refuses tampered candidates; state file unchanged.
- [ ] Clean candidate still approves successfully (no deadlock).
- [ ] ≥3 tests, green, including the refusal path.
- [ ] Link paragraph to registry + supply-chain concepts.

## 11. Troubleshooting and recovery

| Symptom | Cause | Fix |
|---|---|---|
| verify fails on a fresh stage | digest computed before copy finished, or on the source instead of the staged copy | hash the **staged** path after `copy2` completes |
| approve still passes after fix | approve doesn't call verify, or ignores its result | make approve *depend* on verify's exit status |
| state shows `approved` after refusal | state saved before validation | validate first, save only on success |
| tests leave a broken `staged/` | fixture pollution | each test stages into a `tmp_path` copy, or restore at teardown |

## 12. Reflection questions

1. sha256 proves the bytes didn't change — what does it *not* prove about
   *who built them*? What else would you record?
2. Where should the manifest live so an attacker cannot rewrite both the
   file and its digest?
3. A legitimate rebuild changes the digest. How does your system
   distinguish "corrupt" from "replaced by a newer build"?

## 13. Optional challenge tasks

1. Add `stager.py history` — an append-only audit log of stage/verify/
   approve attempts (including refusals).
2. Support multiple candidates (`rc-1`, `rc-2`) with independent
   manifests.
3. Sign the manifest with a key from the environment (never in the file)
   — Module 15's secrets rule applied.

## 14. Rubric / checklist

| Points | Criterion |
|---|---|
| 3 | hole demonstrated with before-evidence |
| 4 | digests recorded + verified at verify *and* approve |
| 4 | tamper refused (exit code + message + unchanged state) |
| 3 | ≥3 tests green incl. refusal |
| 2 | linkage paragraph (registry / supply chain) |
| **16** | **total** · ≥12 = pass |

## 15. Cleanup

```powershell
cd examples\labs\lab-09
Remove-Item -Recurse staged, backup, __pycache__, .pytest_cache -ErrorAction SilentlyContinue
python prepare_build.py    # optional: fresh build/ for the next attempt
```

---

**After attempting:** a reference integrity upgrade lives in
[`examples/labs/solutions/lab-09/`](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/labs/solutions/lab-09).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../about/index.md).*