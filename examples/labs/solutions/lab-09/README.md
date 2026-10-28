# LAB-09 — reference solution

> Attempt the lab first. This is the answer key, not the assignment.

## The distinction the lab is built around

```json
{"exists": true, "size": 3361}      // what stage() records today
```

**Existence and size are not integrity.** `exists` answers "is there a
file at that path"; the pipeline needs "is it the *same bytes* we
staged". A file can exist, have the right size, and still be a different
build (or a corrupted one).

## Verified "as shipped" transcript (authoring machine)

```text
python prepare_build.py      → build/ ready: config.yaml, metrics.json, model.joblib
python stager.py stage        → rc-1 staged  staged_at=2026-10-26T00:48:42+00:00
python stager.py list         → rc-1  staged  staged_at=…
python stager.py verify       → rc-1: VERIFY OK   (3 file(s))
```

**The hole:** `verify` prints `VERIFY OK` after checking *existence
only*. Prove it to yourself:

```powershell
# 🪟 — corrupt a staged copy, then "verify" it again
Add-Content -NoNewline -Path staged\rc-1\metrics.json -Value "tampered"
python stager.py verify       # ✅ checkpoint: still VERIFY OK — the hole, in writing
```

```bash
printf 'tampered' >> staged/rc-1/metrics.json && python stager.py verify
```

(Record the corrupted state, then restore it before you change code —
`git checkout -- staged/` or re-run `stage`.)

## The fix you build

At **stage** time:

```python
files[path.name] = {
    "exists": True,
    "size": path.stat().st_size,
    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),   # the identity
    "staged_at": now(),
}
```

At **verify/approve** time: recompute `sha256` for each staged file and
compare; any mismatch → `VERIFY FAILED` with the filename and both
hashes, exit 1. `approve` must refuse when verify fails (it currently
calls verify and then approves regardless).

**Demonstration required by the lab:**

```text
stage → verify OK
corrupt staged/metrics.json
verify → VERIFY FAILED metrics.json  staged=… actual=…   exit=1
approve → REFUSED
restore → verify OK again
```

## Reasoning checkpoints (model answers)

- **Why record the hash at stage time, not compute it at verify time
  from the build directory?** The staged copy is the artefact of record;
  the build directory keeps changing. Identity must attach to the copy
  you are vouching for.
- **What does `size` still buy you?** A cheap first check (catches
  truncation instantly) — but it cannot catch a same-size edit, which
  is exactly why sha256 is the real check.
- **Where does this connect?** The capstone's `release.json` records
  `model_sha256` at registration — this lab builds that reflex from
  scratch; LAB-20 shows the failure it prevents.

## Common wrong answers

- Hashing the manifest but not the files it lists (self-referential
  hole).
- Verifying against the *build* folder instead of the staged copy.
- Claiming "VERIFY OK means it's safe" — before your fix, it never did;
  your write-up must say what it actually checked.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../../docs/about/index.md).*