# Architecture Diagram Template

> **How to use this file:** copy it to `docs/architecture.md` in your project.
> Draw the diagram with any tool (hand-drawn photo, Mermaid, Excalidraw — the
> repository ships an *excalidraw-diagram-generator* skill), embed or link it,
> and fill the tables that make the picture *inspectable*. Delete italic
> guidance. A picture without the annotation tables below scores at most
> *Developing* on communication.

---

```markdown
# Architecture — <system name>

**Date:** <YYYY-MM-DD> · **Version:** <n> · **Author:** <name>
**Diagram:** <embedded image or link> · **Tool used:** <tool>

## 1. The picture
*Embed the diagram. It must show, as labelled boxes and arrows:*

- [ ] data source → validation → versioned dataset
- [ ] training pipeline → tracked run → artefact
- [ ] quality gate (marked as a decision point that can REFUSE)
- [ ] registry (staged / promoted) → serving
- [ ] service: API, model load point, request validation
- [ ] prediction log → drift/performance check → decision (human)
- [ ] CI boundary: what runs automatically on push

## 2. Annotated components
| Component | Technology / file | Responsibility | Owns which state |
|---|---|---|---|
| e.g. data validator | `src/validate.py` | refuses bad extracts | none (pure) |
| e.g. registry | `registry.json` + `versions/` | promotion record | versions, hashes |
| … | … | … | … |

## 3. Data flow annotations
| Arrow | What flows | Format | Failure mode if this breaks |
|---|---|---|---|
| validator → trainer | validated rows | CSV + hash | training on garbage |
| … | … | … | … |

## 4. Trust boundaries & controls
| Boundary | Crossing | Control |
|---|---|---|
| client ↔ API | requests | validation (422 + field names), auth if any |
| API ↔ model store | artefact bytes | sha256 verified against registry |
| CI ↔ secrets | credentials | platform secrets only; never in YAML |

## 5. Design decisions (the "why" that gets marked)
1. **Decision:** <e.g. load model once at import> — **alternatives
   considered:** <per-request load> — **why chosen:** <latency +
   determinism> — **what would reverse it:** <e.g. >1 model version live>.
2. *(repeat for 2–4 real decisions)*

## 6. Known gaps / day-one non-goals
*What you deliberately did not build (HA, auth, autoscaling…) and the signal
that would make you build it. Naming honest gaps scores higher than
pretending they don't exist.*
```

**Self-check:** hand this page to a classmate — can they point to where a
prediction's bytes are read, where a bad request dies, and where a rollback
takes effect? If not, the diagram is decoration.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*