# Question bank 05 — APIs and containers

**Covers:** Modules [10 — Model serving with FastAPI](../../modules/10-model-serving-fastapi/index.md)
and [11 — Docker images and containers](../../modules/11-docker-containers/index.md).
**Format:** 10 questions — multiple choice, short answer, debugging, architecture, scenario.
**Suggested check:** 7/10, with **A5** and **A10** correct.

> *Attempt first, then read the
> [reference solutions](../keys/question-banks-KEY.md).*

---

## Part A — Multiple choice

**A1.** A `/predict` request arrives with `tenure_months: -5`. The correct
response is:

- (a) 200 with probability 0
- (b) 422 naming the offending field
- (c) 500 so the operators notice
- (d) 404

**A2.** Loading the model inside the request handler on every call:

- (a) Is required for load balancing
- (b) Wastes latency and file handles; load once at startup (or cache it)
- (c) Improves determinism
- (d) Is the only thread-safe option

**A3.** In a Dockerfile, copying and installing dependencies *before* copying
application code is done to:

- (a) Impress reviewers
- (b) Maximise layer caching — code edits don't re-install packages
- (c) Shrink the model
- (d) Avoid licences

**A4.** `CMD ["python", "-m", "app"]` (exec form) versus
`CMD python -m app` (shell form) matters because:

- (a) Exec form runs fewer processes, so `docker stop`'s signal reaches Python
- (b) Shell form is faster
- (c) Exec form supports environment variables
- (d) It makes the image smaller

## Part B — Short answer

**A5.** Why must a container listen on `0.0.0.0` for published ports to work,
and what typically goes wrong when it binds to `127.0.0.1` inside the
container?

**A6.** Explain the request/response contract you would design for a batch
scoring endpoint: payload shape, limits, validation errors, and what the
response must carry so a caller can trust it (version, threshold, …).

**A7.** What is a build context, what does `.dockerignore` control, and what is
one *security* reason to keep it small?

## Part C — Debugging

**A8.** Five symptoms, five causes — match them and give the fix:

1. `curl` to the published port times out
2. Container exits immediately with code 0
3. Every request is slow by ~200 ms
4. Build re-installs all packages on every code edit
5. Image is 2.1 GB

…causes include: model loaded per request, dependency layer ordered after code,
no `CMD`, `:latest` base plus dev tools and the whole repo in the context,
app bound to loopback.

## Part D — Architecture

**A9.** Draw the full path of one prediction: client → API → validation →
preprocessing → model → response, and mark where the model file is read, where
errors are produced, and what gets logged.

## Part E — Scenario

**A10.** The service works locally but returns 503 in the container, and
`/health` reports `model_version: none`. Give the two most likely causes, the
commands to confirm each, and the fix.

---

**Next:** [reference solutions](../keys/question-banks-KEY.md) (bank 05), then
[bank 06](q06-cicd-orchestration.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../../about/index.md).*
