# References — Module 10

## Tool documentation

| Resource | Use it for |
|---|---|
| [FastAPI documentation](https://fastapi.tiangolo.com/) | Endpoints, dependency injection, exception handlers — the primary reference |
| [FastAPI: Request Validation / Body](https://fastapi.tiangolo.com/tutorial/body/) | Schema-driven validation and 422 generation |
| [FastAPI: OpenAPI](https://fastapi.tiangolo.com/features/openapi/) | `/docs`, `/redoc`, `/openapi.json` — docs as a by-product |
| [pydantic docs](https://docs.pydantic.dev/latest/) | `Field`, `Literal`, constraints (`ge`, `le`, `min_length`) |
| [uvicorn](https://www.uvicorn.org/) | The ASGI server running the app; settings incl. `host`, `port`, workers |
| [Starlette](https://www.starlette.io/) | What FastAPI sits on: routing, responses, TestClient |
| [httpx](https://www.python-httpx.org/) | What `fastapi.testclient` uses under the hood |
| [OpenAPI specification](https://spec.openapis.org/oas/latest.html) | The schema format behind `/docs` |

## General / measured-practice reading

- **Fielding (2000), *Architectural Styles and the Design of Network-based
  Software Architectures* (PhD thesis)** — where REST was defined; useful for
  vocabulary (resources, uniform interface, statelessness).
- **Henry & Kusnetzky (Google SRE book, ch. 20)** — *Handling Overload*;
  latency vs throughput framing you will meet again in Module 16.
- **Google SRE Workbook — *Handling Overload / Latency Targets*** — why p95
  beats averages (revisited in Module 14's monitoring).

## Distinguishing tool-specific from general

| Claim | Kind |
|---|---|
| "Validate inputs at the boundary; never let bad data reach the model" | **General principle** |
| "Health endpoints must be cheap and honest" | **General principle** |
| "Load the model once per process" | **General principle** for stateful inference |
| "`422` on schema violation" | **Framework behaviour** (FastAPI/pydantic) — other stacks may use 400 |
| "`/docs` exists" | **Tool-specific** (FastAPI feature) |
| "`python -m service`, `HOST`/`PORT` env vars" | **Course-specific** |

## Related course material

- Module 09 — the production pointer this service reads.
- Module 11 — packaging this exact service into an image.
- Module 14 — logging what this API predicts.
- Module 15/16 — auth, exposure, and load (deliberately absent here).

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*