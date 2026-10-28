# Independent challenge — Module 11

> Do this **without** step-by-step help. Target **75 minutes**. Requires Docker.

---

## 1. The task

Take the shipped `Dockerfile` and make it *better* on three axes — image size,
startup safety, and persistence — while keeping the API contract intact.

## 2. Tasks

1. **Shrink the image.** Options to investigate (pick at least one): a smaller
   base (`python:3.14-slim` → investigate what `slim` vs `alpine` actually
   costs you in compatibility), dropping `PIP_NO_CACHE_DIR` in favour of
   multi-stage, or excluding anything else you can prove unnecessary.
   Report `docker images` size **before and after**, and prove the API still
   answers `/health` + 422 on the empty batch.
2. **Make startup self-diagnosing.** Change the container's `HEALTHCHECK` (or
   the app) so that "no model loaded" makes the container report **unhealthy**
   rather than merely `degraded` in JSON. Justify in three sentences why a
   platform should see unhealthy (Module 16 will rely on this).
3. **Persist results.** Run the container with a bind mount so that anything
   written to `/app/monitoring` survives `docker rm`. Prove it: create a file
   inside (via `docker exec`), remove the container, show the file on the host.
4. **Reproducibility argument.** Write 200 words: which parts of your run are
   now guaranteed by the image, which are still controlled by flags at `run`
   time, and which remain outside Docker's control entirely (concepts §8 table
   is your checklist).
5. **Honest limitation log.** If any step could not be executed in your
   environment, record: what you attempted, the exact error, and the
   verification procedure you would run where it works. (This is a graded
   deliverable — an honest gap beats a fabricated transcript.)

## 3. Deliverables

- `Dockerfile` diff with per-change justification.
- Before/after `docker images` output.
- Test transcript: `/health` 200 + empty-batch 422 **from the container**.
- `docker exec` + host-side proof for the volume task.
- `reproducibility.md` (task 4) and `limitations.md` (task 5, if applicable).

## 4. Self-check (feedback criteria)

| Grade | Looks like |
|---|---|
| **Excellent (4)** | Size reduction measured with numbers; health semantics argued, not just changed; volume proof shown on both sides; reproducibility essay distinguishes build-time/run-time/outside; limitations honest and specific |
| **Proficient (3)** | Tasks 1–3 done with evidence; essay thinner |
| **Developing (2)** | Size or volume task skipped; claims without output |
| **Not yet (1)** | No transcripts, or an image that no longer serves |

**Design rule:** the API contract (endpoints, status codes, schema) must not
change — containerisation is packaging, not a chance to redesign the service.

---

**Next:** [knowledge-check.md](knowledge-check.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*