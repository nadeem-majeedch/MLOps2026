# Test Evidence Template

> **How to use this file:** copy it into `EVIDENCE/tests/README.md`. One row
> per claim, each with the exact command and its **real** output (trimmed,
> never edited). Anything you did not run gets `NOT RUN` in the status column —
> that label is acceptable; a claim without output is not. Delete italic
> guidance lines.

---

```markdown
# Test evidence — <system name>

**Collected:** <YYYY-MM-DD> · **Machine:** <OS, Python version>
**Suite command:** `python -m pytest -q` · **Result:** <N passed> (paste tail below)

## 1. Suite summary
```text
<paste the last 5 lines of the real run: count + duration>
```

## 2. Evidence table
| # | Claim being evidenced | Command | Status | Output (trimmed) |
|---|---|---|---|---|
| 1 | data contract refuses a missing column | `python -m src.validate` | ✅ ran | `FAIL required_columns … missing: [...]` exit 1 |
| 2 | suite green | `python -m pytest -q` | ✅ ran | `12 passed in 0.44s` |
| 3 | gate refuses the defective candidate | `python gate.py bad.json` | ✅ ran | `VERDICT: REFUSED` exit 1 |
| 4 | container serves from host | `curl :8000/health` | ⚠️ NOT RUN | no container runtime on this machine |
| … | … | … | … | … |

*Status vocabulary: ✅ ran · ⚠️ NOT RUN (state the blocker) · ❌ failed
(explain what you did next). Never a blank.*

## 3. Red → green cycles (when applicable)
**Defect introduced:** <what you broke and where>
```text
<the failing output, verbatim>
```
**Fix applied:** <one line + file>
```text
<the passing output, verbatim>
```

## 4. Coverage / quality numbers (if claimed)
```text
<paste pytest --cov summary or equivalent, verbatim>
```
*Only numbers that appear above may be quoted in REPORT.md.*

## 5. Gaps and limitations
- [ ] every ⚠️ above has a one-line reason and, where possible, an alternative
      check that *was* run
- [ ] flaky/nondeterministic results noted with frequency observed

## 6. Reproduction
*List the commands in order, from a fresh clone, that rebuild everything in
this document — with expected exit codes.*
```

**Self-check:** a sceptical reviewer should be able to re-run §6 and get §1.
If any row's output could not be reproduced from §6, fix §6 before submitting.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*