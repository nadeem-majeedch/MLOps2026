# Lab 12 — Block a defective model release

## 1. Scenario and business problem

Last release, a data defect reached production because "the tests pass on my
machine" — and nobody re-ran the data contract before merging. Management's
new rule: **nothing merges unless the machine checks it.**

**Business problem:** convert your gates into a workflow that runs on every
push and pull request, then prove it blocks the things it is supposed to block
— including a model below its quality floor.

## 2. Skills practising

- Reading a workflow file as an executable specification.
- Running each CI step locally (the debugging loop that beats refreshing a
  red page).
- Causing each kind of failure on purpose: lint, test, ML gate.
- Explaining permissions and the (absence of) secrets in the file.

## 3. Prerequisites

- [concepts.md](concepts.md) read (§1–§7).
- `ruff` installed (`ruff --version`), suite green (`python -m pytest`).
- ☁️ Optional: a GitHub repository to watch it run live (free tier suffices).

## 4. Required tools and estimated time

| Item | Detail |
|---|---|
| Tools | Python 3.10+, ruff, PyYAML, the shipped `.github/workflows/ci.yml` |
| Cost | Free; GitHub's free Actions allowance covers the live portion |
| ⚠️ Resource-heavy | none locally (each step is seconds) |
| ⏱️ Estimated time | 140 minutes |

## 5. Input data and how to obtain it

```powershell
# 🪟 from examples/churn
ruff check .                      # ✅ All checks passed
python -m pytest                  # ✅ 34 passed
python ml_check.py                # ✅ ML VALIDATION PASSED
```

## 6. Where the workflow lives

```
.github/workflows/ci.yml     # at the REPO ROOT (workflows are repo-level)
examples/churn/              # every job's working-directory
├── ml_check.py              # the ML validation command
├── requirements-docker.txt  # cache key for pip
└── src/ tests/ ...
```

## 7. Setup and execution steps

**Step 1 — Read the spec.** From `ci.yml`, write: the two triggers, the three
jobs, the `runs-on` image, the permission line, and which step uploads an
artifact.
✅ **Checkpoint:** five answers, all present in the file.

**Step 2 — Run job 1 locally.** `ruff check .` from `examples/churn`.

**Step 3 — Run job 2 locally.** The generate + pytest-with-coverage command
from the workflow (worked example §3).

**Step 4 — Run job 3 locally.** `python ml_check.py` → PASSED.

**Step 5 — Break job 1 on purpose.** Add `import os` at the top of
`src/validate.py`, run `ruff check .`, capture the F401 output, then remove it.
✅ **Checkpoint:** CI's first line of defence, reproduced in one second locally.

**Step 6 — Break job 2 on purpose.** In `tests/test_data.py`, temporarily
change an assertion to something false; run `python -m pytest`, capture the
FAILING short summary, then restore.
✅ **Checkpoint:** you can name the test from its failure line alone.

**Step 7 — Break job 3 (the ML gate).** Swap in the corrupt extract:

```powershell
cp data/raw/churn.csv data/raw/churn.csv.bak     # 🐧 cp ...
cp data/corrupt/missing.csv data/raw/churn.csv
python ml_check.py; echo "exit=$LASTEXITCODE"     # ✅ FAILED, exit 1, 5/7
cp data/raw/churn.csv.bak data/raw/churn.csv
python ml_check.py                                # ✅ PASSED again
```

✅ **Checkpoint:** both captured, with the two named failing checks.

**Step 8 — The quality-floor variant of the gate.** Set
`quality.roc_auc_floor: 0.99` in `config.yaml`, train once
(`python -m src.train --config config.yaml --data data/raw/churn.csv`), run
`ml_check.py` → floor line prints `? NO`. Restore the floor and re-train.
✅ **Checkpoint:** the model itself being too weak blocks the merge, not just
bad data.

**Step 9 — Secrets reasoning (no account needed).** Write the three-place rule
and answer: *if* this workflow needed a token, where does it live (UI path),
where does it appear (`${{ secrets.X }}` in `env:`), and what must it never
touch (source, logs, files)? Then point to the line in `ci.yml` proving this
workflow needs none.
✅ **Checkpoint:** written answers + the `permissions: contents: read` line.

**Step 10 — ☁️ Optional live run.** Push to a GitHub repository (the
instructor handles pushes in this course; if it is your own fork, that push is
yours). Acceptance signals: three green checks; then open a PR with the Step 5
change and watch `lint` go red; comment on the run with the log line that
named the problem.

## 8. Expected outputs and verification

| Step | Expected | Verify |
|---|---|---|
| 1–4 | All commands green, exit 0 | console + exit codes |
| 5 | `F401` naming file and line | ruff output |
| 6 | `FAILED tests/...::test_name` | pytest short summary |
| 7 | `ML VALIDATION FAILED`, checks named, exit 1 → then PASSED | both transcripts |
| 8 | `quality floor: ... ? NO` | ml_check output |
| 9 | Written answers + quoted permission line | your note |
| 10 | green run; red run on the PR | GitHub UI (optional) |

## 9. Acceptance criteria

- [ ] All three jobs' commands reproduced locally with captured exit codes.
- [ ] Three deliberate failures captured: lint, test, ML gate — each with the
      exact error line.
- [ ] Floor-variant gate demonstrated (model too weak → blocked).
- [ ] Secrets three-place rule written, with the proof line from `ci.yml`.
- [ ] (Optional) one real red/green pair on GitHub.
- [ ] Everything filed as `modules/12/`.

## 10. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `ruff: command not found` | Not installed in this environment | `python -m pip install ruff==0.15.1` (the version CI installs) |
| Workflow does not appear on GitHub | `.github/workflows/` not at **repo** root, or file not pushed | Check path and that the branch is `main` (our trigger) |
| Workflow appears but never runs | Trigger branch mismatch | `on.push.branches: [main]` vs your default branch name |
| `ml_check` says missing metrics in CI but passes locally | CI generates data and trains; your local run reused existing files | Follow the job's step order exactly (generate → train → check) |
| YAML parse error on push | Indentation (2 spaces), or `on:` interpreted oddly by some tools | `python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"` locally |
| Cache not helping | Key includes `requirements-docker.txt` — editing pins invalidates it | Expected; that's correctness over speed |
| A step passes locally, fails on the runner | Path/cwd difference (`working-directory`) or missing install step | Compare the job's `run:` block with what you actually typed |

More: [troubleshooting.md](troubleshooting.md).

## 11. Cleanup

```powershell
# 🪟 from examples/churn
git checkout -- src/validate.py tests/test_data.py config.yaml   # if you keep a checkout
cp data/raw/churn.csv.bak data/raw/churn.csv -ErrorAction SilentlyContinue
Remove-Item data/raw/churn.csv.bak -ErrorAction SilentlyContinue
python -m pytest && ruff check . && python ml_check.py    # ✅ all green
```

## 12. Optional extension tasks

1. **Add a fourth job** (`needs: [test]`) that runs `python -m pipe.run` and
   uploads `pipe_out/report.md` as an artifact.
2. **Path filters:** make the workflow run only when `examples/**` or
   `.github/**` changes, and argue the trade-off (missed triggers vs minutes).
3. **Image build job (LO 12.3):** write — and, where you have Docker, run —
   `docker build -t churn-api:${{ github.sha }} .` as a job; state your tag
   strategy and where a registry login would go **without** committing a token.

---

**Next:** [independent-challenge.md](independent-challenge.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*