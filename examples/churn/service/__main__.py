"""Serve the app: `python -m service` (Module 10).

HOST/PORT come from the environment so the *same code* listens on
127.0.0.1 for local work and on 0.0.0.0 inside a container (Module 11) —
never hardcode the bind address.
"""

from __future__ import annotations

import os

import uvicorn


def main() -> None:
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))
    print(f"serving on http://{host}:{port}  (docs: /docs, health: /health)")
    uvicorn.run("service.app:app", host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()