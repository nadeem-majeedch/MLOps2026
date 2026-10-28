# Module practice exercises

Hands-on practice for every module — smaller than a
[mini-project](mini-projects.md), larger than a knowledge check. Each module
lists **three exercises**: one *read/do*, one *break/fix*, one *explain*.
Do them in order across the course; every exercise names the evidence you
should be able to show afterwards.

> ⚠️ **Suggested self-study framework — illustrative, not an official
> university assignment sheet.** Point values mentioned are illustrative;
> instructors must map them to their own regulations.

**Ground rules**

- Evidence-before-claim: an exercise is done when you can show the output,
  diff, or written answer — never before.
- Every exercise links back to its module; if the exercise feels alien,
  re-read the module's [learning objectives](../syllabus/learning-outcomes.md)
  rather than guessing.
- Free and local unless labelled ☁️.

---

## Foundations

### Module 01 — Introduction & ML lifecycle
1. **Read/do:** Take any ML feature you use daily and map it onto the nine
   lifecycle stages; write two sentences per stage about who owns it.
   *Evidence: one-page lifecycle map.*
2. **Break/fix:** Find a real "model rotted silently" story (news, postmortem)
   and identify which stage's missing artefact would have caught it earliest.
   *Evidence: the artefact named + why that stage.*
3. **Explain:** In ≤150 words, explain to a non-technical colleague why a
   green uptime dashboard can coexist with a worse model.
   [Bank 01](question-banks/q01-fundamentals.md) F4 checks this.

### Module 02 — Python, Git, CLI, environments
1. **Read/do:** Create a fresh virtual environment from a pinned
   requirements file and run one script successfully.
   *Evidence: `python --version`, install log, script output.*
2. **Break/fix:** Delete your environment, recreate it *only* from the pins,
   and note anything that fails. *Evidence: the failure list (ideally empty)
   and what you changed in the pins afterwards.*
3. **Explain:** Why does `pip freeze` on your machine differ from CI's? Give
   two concrete causes. [Bank 02](question-banks/q02-reproducibility-data-versioning.md) R2.

### Module 03 — ML project structure & technical debt
1. **Read/do:** Restructure the beginner starter
   ([`examples/starter-projects/beginner/`](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/starter-projects/beginner))
   into the course's standard layout without changing behaviour.
   *Evidence: before/after tree + tests still green.*
2. **Break/fix:** Introduce one dependency from outside the repo (an import
   that only exists on your machine) and watch a fresh clone fail; fix it.
   *Evidence: the failure, then the fix.*
3. **Explain:** Name three symptoms of technical debt you have personally hit
   this month, each with the folder it lives in.
   Practice: [LAB-02](../labs/lab-02-untangle-the-notebook.md).

## Data and training

### Module 04 — Data quality, validation, versioning
1. **Read/do:** Run `python make_data.py --check` in `examples/labs/` and
   confirm byte-identical regeneration. *Evidence: the check's output.*
2. **Break/fix:** Introduce one defect per type (null, out-of-range,
   duplicate, schema drift) into a copy of the clean CSV and make your
   validator refuse each one by name.
   *Evidence: four refusal messages.* Practice: [LAB-03](../labs/lab-03-gate-the-dirty-extract.md), [LAB-04](../labs/lab-04-version-it-and-prove-it.md).
3. **Explain:** Versioning vs lineage in five sentences each.
   [Bank 02](question-banks/q02-reproducibility-data-versioning.md) R5.

### Module 05 — Reproducible training & pipelines
1. **Read/do:** Run the same training command twice and diff the metrics
   files; they must match. *Evidence: `diff` (or hash) showing no change.*
2. **Break/fix:** Remove the seed and watch reproducibility die; restore it
   and list the *other* three leaks you would also need to close.
   *Evidence: failing then passing comparison.*
3. **Explain:** Why is "same seed, same result" necessary but not sufficient?
   Practice: [LAB-05](../labs/lab-05-deterministic-by-construction.md).

## Intermediate

### Module 06 — Experiment tracking with MLflow
1. **Read/do:** Record ≥10 runs with parameters and metrics; identify the
   champion and say *why* in one sentence tied to a baseline.
   *Evidence: run table + the sentence.*
2. **Break/fix:** Delete a run's parameters (track a run with a metric only)
   and try to justify it six "months" later. *Evidence: what you cannot answer.*
3. **Explain:** Validation vs test set, and what test-set tuning costs you.
   [Bank 03](question-banks/q03-experiment-tracking-evaluation.md) E5.
   Practice: [LAB-06](../labs/lab-06-ten-runs-one-decision.md).

### Module 07 — Testing for ML systems
1. **Read/do:** Write one test each for a pure function, a schema, and a
   metric floor; run the suite. *Evidence: `pytest -q` output.*
2. **Break/fix:** Introduce a leakage bug (fit preprocessing on all data) and
   write the test that catches it. *Evidence: red → green cycle.*
3. **Explain:** Why can't a green suite prove the shipped artefact is intact?
   Practice: [LAB-07](../labs/lab-07-catch-the-leakage.md).

### Module 08 — Pipeline automation & dependencies
1. **Read/do:** Run the intermediate starter's pipeline and read its
   `manifest.json` aloud — say what each field is for.
   *Evidence: the manifest.*
2. **Break/fix:** Delete an intermediate output and re-run: which stages
   re-execute, and why? Then break a stage deliberately and show downstream
   stages BLOCKED. *Evidence: both transcripts.*
3. **Explain:** What "fail loudly" means and the three ways code fails to.
   Practice: [LAB-08](../labs/lab-08-the-gate-that-must-refuse.md).

### Module 09 — Model artifacts & registries
1. **Read/do:** Stage → promote → verify a model with the advanced starter's
   `registry.py`, and roll back once. *Evidence: the `list`/`history` output.*
2. **Break/fix:** Tamper with the staged file and show `verify` failing.
   *Evidence: MISMATCH output.*
3. **Explain:** What a promotion record must contain to be defensible.
   [Bank 03](question-banks/q03-experiment-tracking-evaluation.md) E3.
   Practice: [LAB-09](../labs/lab-09-staged-verified-released.md).

## Intermediate — delivery

### Module 10 — Model serving with FastAPI
1. **Read/do:** Build `/health`, `/model-info`, `/predict` on the beginner
   starter's model; open `/docs` and try a real request.
   *Evidence: a Swagger screenshot or curl transcript.*
2. **Break/fix:** Send five malformed requests; every one must be 422 with the
   field named. *Evidence: the five responses.*
3. **Explain:** Why load the model once at import? Practice:
   [LAB-10](../labs/lab-10-serve-it.md), [LAB-11](../labs/lab-11-malformed-requests-autopsy.md).

### Module 11 — Docker images and containers
1. **Read/do:** Containerise your lab-10 service (or the advanced starter's);
   hit `/health` **from the host**. ☁️ needs a container runtime — otherwise
   Path B written review. *Evidence: `docker run` + curl transcript.*
2. **Break/fix:** Reorder the Dockerfile so deps install after code and
   measure the rebuild cost. *Evidence: both build logs with timings.*
3. **Explain:** Why `0.0.0.0`, exec-form CMD, and `.dockerignore`.
   Practice: [LAB-12](../labs/lab-12-ship-the-image.md).

### Module 12 — CI/CD with GitHub Actions
1. **Read/do:** Rehearse every CI command locally, then write the workflow
   (starter: [`examples/labs/lab-14/`](https://github.com/nadeem-majeedch/MLOps/tree/main/examples/labs/lab-14)).
   *Evidence: local transcript + workflow file.*
2. **Break/fix:** Seed a defect, show the run red, revert, show it green.
   *Evidence: both run states (or `NOT RUN on GitHub` if you have no repo).*
3. **Explain:** Where secrets live and three places they must never appear.
   Practice: [LAB-14](../labs/lab-14-the-machine-checks-your-work.md).

### Module 13 — Orchestration & scheduled pipelines
1. **Read/do:** Schedule the tick runner (Task Scheduler / cron), let it fire
   twice on its own, then unschedule it. *Evidence: `runs.jsonl` rows with
   timestamps you did not trigger + the unschedule command.*
2. **Break/fix:** Make a tick fail with no recovery tick and show the standing
   alert. *Evidence: `ALERT.md` persisting.*
3. **Explain:** Cron vs orchestrator for three scenarios.
   [Bank 06](question-banks/q06-cicd-orchestration.md) C10.
   Practice: [LAB-16](../labs/lab-16-a-pipeline-that-runs-itself.md).

## Advanced

### Module 14 — Monitoring, drift, retraining
1. **Read/do:** Run `monitor.py drift`, `performance`, and `decision` on the
   capstone outputs; fill the 2×2 cell from the numbers. *Evidence: the three
   outputs + your cell.*
2. **Break/fix:** Score a shifted window through the advanced starter and show
   `monitor.py --check` exiting 1 — then argue whether a retrain is justified.
   *Evidence: the exit code + your argument.*
3. **Explain:** Why drift is not proof of degraded accuracy.
   Practice: [LAB-17](../labs/lab-17-read-the-drift-not-the-chart.md), [LAB-18](../labs/lab-18-rollback-or-ride-it-out.md).

### Module 15 — Security, privacy, governance, fairness
1. **Read/do:** Run `scan_secrets.py` on both fixtures and record both exit
   codes. *Evidence: exit 1 (flawed) and exit 0 (capstone).*
2. **Break/fix:** Fix three of the five seeded defects in a copy of the flawed
   service and re-scan. *Evidence: before/after output.*
3. **Explain:** Write a dated, conditional deployment verdict for your own
   project. Practice: [LAB-19](../labs/lab-19-deployment-security-review.md).

### Module 16 — Cloud, Kubernetes, scaling, reliability
1. **Read/do:** ☁️ optional — write the manifest (Deployment + Service +
   probes + resources) for your service *without* applying it; label any
   cluster step `NOT RUN` if you have no cluster. *Evidence: YAML + label.*
2. **Break/fix:** Match five cluster symptoms to causes (bank O8) and say what
   `kubectl logs` would show for each. *Evidence: the five pairs.*
3. **Explain:** Rolling update vs rollback, and why surge/unavailable settings
   are an availability decision. [Bank 09](question-banks/q09-cloud-advanced-operations.md) O5.

### Module 17 — Capstone
The capstone *is* the practice: work the
[capstone checklist](../projects/capstone-checklist.md) milestones C1–C7, and
use the [integrated capstone assessment](capstone-assessment.md) to structure
your evidence. Practice: [LAB-20](../labs/lab-20-incident-day.md) — the full
lifecycle incident exercise.

---

**Scoring yourself:** the [rubrics & checklists](rubrics-checklists.md) page
gives an illustrative rubric per exercise type; the
[question banks](question-banks/index.md) test the theory behind them.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*