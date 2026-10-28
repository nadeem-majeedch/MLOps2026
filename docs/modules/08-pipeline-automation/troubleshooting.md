# Troubleshooting — Module 08

Symptom → likely cause → fix. See also the
[course troubleshooting hub](../../troubleshooting/index.md).

---

## 1. The runner itself

| Symptom | Likely cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'pipe'` | Not in the project folder | Run from `examples/churn` (`python -m pipe.run`) |
| `cycle in the dependency graph at 'x'` | A task lists a descendant (or itself) as a dependency | Draw the DAG; every edge must move one direction |
| `unknown task 'y'` (from `--from`) | Typo / renamed stage | `python -m pipe.run --list` gives exact names |
| `FileNotFoundError` inside a stage | A declared input doesn't exist yet (stages run out of order because a dependency was never declared) | Add the missing dependency to `TASKS` |
| `PermissionError` writing `pipe_out/` | File locked by an editor/viewer, or read-only checkout | Close the viewer; on Windows check the file isn't open in another terminal |

## 2. Skipping: too much or too little

**Everything re-runs every time.**
1. Is a stage writing *outside* its declared outputs? (Each undeclared write
   shows up as an output-signature mismatch somewhere.)
2. Is a stage nondeterministic — timestamps, random seeds, dict ordering,
   `set` iteration in the output? Fix the stage: determinism is a contract
   (concept §3).
3. Are you editing `manifest.json` or `pipe_out/` by hand?

**A stage skips when you expected a re-run.**
- The file you changed is not *declared* as that stage's input — the runner
  cannot see it. Undeclared reads are the classic cause (and the reason to
  prefer `config.yaml` over inline constants).
- You changed a different copy of the file (wrong folder / another checkout).

**A stage re-runs after an unrelated edit.** The edit touched *that stage's own
source* (each stage hashes its own function) — check which function you
actually modified.

## 3. Failures and resume

| Symptom | Likely cause | Fix |
|---|---|---|
| `FAILED ... quality gate failed: roc_auc ...` | Model below `quality.roc_auc_floor`, or floor set to a demo value | Read the numbers in the message; restore the floor or improve the model (Module 06's baseline/challenger loop) |
| `data contract violated: ...` | Raw extract changed or is corrupt | Run `python -m src.validate --data data/raw/churn.csv` alone to see all checks; regenerate if synthetic |
| Resume re-ran more stages than expected | Config or inputs genuinely changed between runs — signatures recompute each run | Expected; compare signatures in `manifest.json` to see which part differed |
| Exit code always 0 although a stage printed an error | The stage swallowed an exception (`except: pass`) | Stages must raise; that's the runner's whole failure model |
| Manifest shows `failed` but console shows later successes | Stale entries from an earlier run are kept for history | Trust the *last* run's console output + the entry's `finished_at` |

## 4. Conceptual confusions

- **"Skipping means it's correct."** Skipping means *nothing I can see changed*.
  That is why outputs are hashed too — and why `--clean` exists as the
  independent proof.
- **"Gates slow me down."** A gate costs 0.01 s here; the mistake it blocks
  costs a day. Put it in the graph so nobody can forget it (Module 12 puts it
  in CI so nobody can *bypass* it).
- **"The manifest is the source of truth."** The manifest records history; the
  signature comparison decides the *current* run. When they disagree, the
  signature wins.

## 5. Still stuck?

1. `python -m pipe.run --list` — verify the declaration first, the code second.
2. Read the failing stage's input/output list in `--list` output against what
   the code actually opens.
3. Run one stage's function in isolation (import and call it) to separate
   "graph problem" from "code problem".
4. [references.md](references.md) — the Make/Snakemake docs describe the same
   model with different syntax.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*