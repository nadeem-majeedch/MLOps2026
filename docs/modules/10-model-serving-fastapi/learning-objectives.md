# Learning objectives — Module 10

Maps to syllabus outcomes
[LO 10.1–10.4](../../syllabus/detailed-syllabus.md#module-10-model-serving-and-rest-apis-using-fastapi).

| # | You can… | You prove it by… |
|---|---|---|
| **10.1** | Expose a registered model through a REST API with input validation and clear error responses | Live curl transcript: 200 with predictions, 422 with per-field messages, both from the same server |
| **10.2** | Distinguish batch, online (synchronous), and streaming inference and justify the choice | A 3-sentence justification for *this* API (online, batched requests) naming what would change the choice |
| **10.3** | Test the API automatically, including malformed-input checks | `tests/test_service.py` — 8 tests green inside the project suite (34 total) |
| **10.4** | Measure and report throughput/latency honestly | Your own measurement note: method, request count, p50/max, and one caveat about what it does *not* prove |

## Supporting skills

- Read a pydantic schema as a contract and predict what a malformed payload
  will return (status code, error shape) *before* sending it.
- Explain why the model loads **once at startup** and what 503-with-instructions
  gives you over a crash on boot.
- Say what `/health` is for (orchestrators, load balancers, humans) and why it
  must stay cheap.
- Name two things deliberately left out (authentication, HTTPS) and where they
  belong (Module 15 / Module 16).

## Self-check questions

1. Which endpoint should an orchestrator poll, and why that one?
2. What status code does a bad `contract_type` produce, and who generated the body?
3. Why does `/predict` take a list instead of one record?

*(Answers in [knowledge-check.md](knowledge-check.md) — attempt first.)*

---

[← Module 10 index](index.md) · [Next: concepts →](concepts.md)

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*