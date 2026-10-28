# Knowledge check — Module 11

## How to use this

1. Answer in writing, closed book on the second pass.
2. Mark with the [answers](#answers) only after committing.
3. Target **80% with justified reasoning**; below that re-read
   [concepts.md](concepts.md) §§1–§6.
4. Suggested self-study framework, not an official exam:
   [assessment framework](../../syllabus/assessment-framework.md).

---

## Questions

**Q1.** Define, one sentence each: image, container, layer, Dockerfile.

**Q2.** *(True/False + why)* "A container is a lightweight virtual machine."

**Q3.** Why does `COPY requirements-docker.txt .` precede `COPY src/`? State
what happens to your build time when you edit only `app.py`.

**Q4.** The service binds `0.0.0.0` in the container but `127.0.0.1` on your
laptop. Explain both choices in terms of *who* needs to reach the process.

**Q5.** Give two distinct reasons a container can be running while the host
gets `connection refused` on the mapped port.

**Q6.** What do `EXPOSE 8000` and `-p 8000:8000` each actually do? Which one
can you rely on?

**Q7.** Why is `PYTHONUNBUFFERED=1` set? Describe the symptom you would see
without it, from the operator's point of view.

**Q8.** `.dockerignore` excludes `data/` but keeps `artifacts/`. Give the
reasoning for each decision.

**Q9.** Name two things the image guarantees and two it does **not**, using
concepts §8's table (no credit for repeating without the *why*).

**Q10.** Why does Module 12 (CI) want to build this image even though it
never runs it in production?

---

## Answers

**Q1.** *Image*: a frozen layered filesystem + metadata, built from a
Dockerfile. *Container*: a running instance of an image with its own ephemeral
filesystem/network view. *Layer*: one instruction's filesystem diff, cacheable.
*Dockerfile*: the ordered, human-readable instructions that build the image. *(5/5)*

**Q2. False.** A VM virtualises hardware and boots a whole OS kernel; a
container shares the host kernel and isolates a *process* (namespaces/cgroups).
Consequences: containers start in seconds and are far lighter — but the guest
"OS userland" in the image is not a security boundary as strong as a VM's. *(5/5)*

**Q3.** Layer caching: the pip layer depends only on the requirements file, so
it is reused whenever pins don't change. Editing `app.py` rebuilds only the
later `COPY` layers — pip install is skipped (verify: second build prints
`CACHED`). *(5/5)*

**Q4.** On the laptop, only *you* call it → binding `127.0.0.1` is the
tightest, safest choice. In the container, the host (via `-p`) and other
containers must reach it *through* the container's interface — `127.0.0.1`
inside would mean "the container's own loopback", unreachable from outside.
Same code, different audience → the `HOST` env var. *(5/5)*

**Q5.** (a) No `-p` mapping (or the mapping points at the wrong container
port), so nothing forwards host traffic; (b) the app inside bound to
`127.0.0.1` instead of `0.0.0.0`, so the forwarded port has no listener behind
it. (Also valid: wrong host port, or the container exited — `docker ps`.) *(5/5)*

**Q6.** `EXPOSE` writes **documentation metadata** into the image (visible via
`docker inspect`) and opens nothing. `-p HOST:CONTAINER` creates the actual
forwarding rule. Rely only on `-p`. *(5/5)*

**Q7.** Python block-buffers stdout when it isn't a terminal; output sits in
memory until exit or buffer fill. Symptom: `docker logs -f` shows *nothing*
while the service is clearly working — and, worse, nothing at all when it
crashes, hiding the exact error you needed. *(5/5)*

**Q8.** `data/` is regenerable (and large/synthetic) — baking it wastes space
and can freeze stale data into the image; `artifacts/` is the *model the
container must serve* — if excluded, the service boots into the 503
`no model loaded` path (and health would read `degraded`). *(5/5)*

**Q9.** Guarantees: **dependency versions** (pinned requirements, resolved at
build) and **OS userland + Python version** (base image). Non-guarantees: the
**host kernel/architecture** (x86 vs ARM differ), and anything **mounted or
passed at run time** (volumes, `-e`, `-p`) — plus byte-identical image hashes
without digest pinning. *(5/5)*

**Q10.** Because a Dockerfile rots silently: base tags move, pins get yanked,
COPY paths change. Building in CI makes "the package still builds" a merge
gate — the same argument as Module 07's tests, applied to packaging. (Module 12
adds exactly this job.) *(5/5)*

**Scoring:** /50 → ×2 = %. **80+ ready.** 60–79: redo lab Steps 4–6 and re-read
concepts §4–§6. Below 60: re-read §1–§3 and re-build once more.

---

**Next:** [troubleshooting.md](troubleshooting.md) ·
[Module 12 →](../12-cicd-github-actions/index.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*