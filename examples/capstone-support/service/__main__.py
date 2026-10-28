"""Serve the capstone API: `python -m service` (HOST/PORT env overrides)."""

from __future__ import annotations

import os

import uvicorn


def main() -> None:
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))
    print(f"serving on http://{host}:{port}  (docs: /docs)")
    uvicorn.run("service.app:app", host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()