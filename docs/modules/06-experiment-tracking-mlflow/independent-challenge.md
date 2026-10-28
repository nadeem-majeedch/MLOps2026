# Independent challenge — Module 06

No step-by-step instructions. You have logged runs someone else designed; now
defend one.

## The task

**Reproduce your best run from a clean state, and explain any difference.**

1. Delete the tracking store and artifacts from the shared example
   (`mlflow.db`, `mlruns/`, `artifacts/`) — or work in a fresh copy of the project.
2. From your memo alone — not from memory — reproduce the run you called the
   champion: same config values, same data version, same seed.
3. Compare the new run's metrics with the recorded ones.
4. **If they match:** state exactly what guarantees that (list the artefacts that
   made it possible, naming the module each came from).
   **If they differ:** diagnose it — which input changed, and how do you know?
5. Write a two-paragraph "reproduction note" suitable for attaching to a
   decision record.

### Stretch (optional)

- Add a `pytest`-style script that asserts your champion's metrics within a
  stated tolerance — a preview of Module 07's performance gate.
- Log a run from a **different machine or environment** (another venv counts)
  and explain any delta in terms of Module 02's lock file.

## Acceptance criteria

- [ ] Old store genuinely deleted before the attempt (say how you verified).
- [ ] Reproduction driven by written instructions, not memory.
- [ ] Metric comparison shown with tolerance stated *in advance*.
- [ ] Any difference diagnosed to a specific input (data hash, version, seed, or code) —
      or an explicit statement of the guarantees if it matched.
- [ ] Reproduction note lists the artefact chain: data version → config → commit → run.
- [ ] Filed as `modules/06/challenge-reproduction.md`.

## How to self-mark

| Level | Signal |
|---|---|
| **Meets** | A stranger could reproduce your champion from the note alone; any delta is explained with evidence |
| **Developing** | Numbers match, but you cannot fully say *why* they match — list the missing guarantee |
| **Not yet** | Needed the old store, or relied on remembered settings |

## If you get stuck

1. The most common cause of mismatch: the config file you *think* you ran is not
   the one logged — check the run's logged artifact.
2. Second most common: data regenerated with an edited script — compare the
   file's hash against your recorded one.
3. If you cannot find your original settings at all, that is the finding:
   write down what tracking now prevents you from losing, and why Module 01's
   incident happened.

---

**Next:** [knowledge-check.md](knowledge-check.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*