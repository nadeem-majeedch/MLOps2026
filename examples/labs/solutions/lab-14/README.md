# LAB-14 — reference solution

> Attempt the lab first. This is the answer key, not the assignment.

## Two paths, one honesty rule

- **Path A — GitHub run:** a green check on a real workflow run page.
  Paste *your* run URL.
- **Path B — local rehearsal:** every CI command executed locally with
  its exit code recorded in `CI-REHEARSAL.md`, headed
  `NOT RUN on GitHub`.

The authoring machine had no GitHub account action in this exercise, so
**no run URL exists from it** — Path B is the honest deliverable there.
Never invent a workflow-run link.

## Local rehearsal transcript (what Path B records)

```text
$ python -m ruff check .
All checks passed!            (exit 0)
$ python -m pytest -q
<your count> passed           (exit 0)
$ python -c "import yaml,sys; yaml.safe_load(open('.github/workflows/ci.yml'))"
parses without error           (exit 0)
```

Run each from the same working directory the workflow's `working-directory`
would use — path mistakes are the #1 local/CI divergence.

## The workflow skeleton the rubric checks

```yaml
name: ci
on:
  push:        { branches: [main] }
  pull_request:
permissions:
  contents: read          # least privilege: CI only reads the repo
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4          # pin majors; pin SHAs for high assurance
      - uses: actions/setup-python@v5
        with: { python-version: "3.14" }
      - run: python -m pip install -r requirements.txt
      - run: python -m ruff check .
      - run: python -m pytest -q
  ml-validation:          # lightweight: data gate + metric floor, no GPU
    runs-on: ubuntu-latest
    steps: [ ... same setup ..., run: python -m src.validate, run: python check_metrics.py ]
  # third job: artifact upload of test reports (actions/upload-artifact@v4)
```

Checklist against the rubric: triggers ✓ · 3 jobs ✓ · pinned action
versions ✓ · `permissions: contents: read` ✓ · artifact upload ✓.

## The red-run drill (the part most people skip)

1. Seed a defect that any of the three checks must catch (a failing
   test, a broken lint, a metric below floor).
2. Push to a branch → the run **fails**; open the log, find the step,
   copy the exact failing line — that is your "failure-reading note"
   (it must localise job + step + command).
3. Revert → green again. Both states are evidence; paste both.

## Secrets write-up — model answers

- **Nothing in YAML.** CI secrets live in repo *Settings → Secrets and
  variables → Actions* and are injected as `${{ secrets.NAME }}` at run
  time; they never appear in the file, the log, or an artifact.
- **Injection path described:** env var at the step that needs it, and
  note that logs print *masked* values automatically for registered
  secrets.
- **None configured** — state it plainly; configuring real secrets for
  a course exercise is the wrong lesson.

## Common wrong answers

- `permissions: write-all` or omitted — the rubric wants least privilege.
- Claiming a green GitHub run you did not produce.
- Only running lint locally and assuming pytest passes in CI.
- Uploading model artifacts/logs that contain a secret "just for debug".

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../../docs/about/index.md).*