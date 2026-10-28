# Deployment Checklist Template

> **How to use this file:** copy it to `DEPLOYMENT.md`. Tick items **only
> after executing the check**, pasting the evidence line next to each. Items
> that cannot apply to your setup get `N/A — <reason>`, never a silent blank.
> Unexecuted cloud/cluster steps stay labelled `NOT RUN`. Delete italic
> guidance lines.

---

```markdown
# Deployment checklist — <system name>

**Target:** local | container | ☁️ cloud (<provider, account required: yes/no>)
**Version deployed:** <vNNN / artefact sha256-16> · **Date:** <YYYY-MM-DD>
**Rollback target:** <previous version id + how to re-point>

## 1. Pre-flight — artefact & quality
- [ ] quality gate passed on this exact artefact — evidence: `<cmd>` → `<verdict>`
- [ ] artefact hash matches registry record — evidence: `<verify output>`
- [ ] dataset version recorded with the model — value: `<hash/id>`
- [ ] tests green at this commit — evidence: `<pytest tail>`

## 2. Image / package
- [ ] base image pinned (no `:latest`) — value: `<FROM line>`
- [ ] dependencies pinned — evidence: `<pip freeze | head>` or requirements head
- [ ] build context reviewed (`.dockerignore` excludes secrets/generated state)
- [ ] non-root `USER` set, or N/A with reason — evidence: `<grep USER Dockerfile>`
- [ ] build transcript captured — evidence or `NOT RUN (no runtime)`

## 3. Runtime configuration
- [ ] host/port correct for the environment (`0.0.0.0` in containers) — evidence: `<health curl from the HOST>`
- [ ] secrets come from the environment/secret store — evidence: `<no literal keys in source: grep output>`
- [ ] resource requests/limits set (cluster) or N/A — values: `<>`
- [ ] probes configured (liveness/readiness) or N/A — evidence: `<>`

## 4. Go-live verification
- [ ] `/health` reports the **expected** version — output: `<>`
- [ ] one real prediction round-trip — request/response: `<>`
- [ ] validation rejects a malformed request in the deployed instance — output: `<>`
- [ ] prediction logging confirmed in the deployed instance — evidence: `<>`

## 5. Rollback readiness
- [ ] previous version still present in the registry — `registry.py list` output: `<>`
- [ ] rollback rehearsed at least once **here** — evidence: `<rollback + health showing old version>`
- [ ] rollback time noted: <~seconds/minutes>

## 6. Post-deploy monitoring
- [ ] dashboards/logs checked 10 minutes after go-live — observation: `<>`
- [ ] alert thresholds armed (with justification on file) — values: `<>`
- [ ] owner on call named: <who>

## 7. Sign-off
**Verdict:** approved | approved with conditions | blocked
**Conditions / known issues:** <>
**Reviewed by (self-study: you, dated):** <>
```

**Self-check:** section 5 is the one people fake. If you have not actually
rolled back to a previous version and watched `/health` change, do that now —
a deployment checklist with an untested rollback is a wish list.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*