"""Configuration for the FLAWED service — Lab 15's audit target.

Defect 1 lives here: production-style secrets are hard-coded in source,
which means they ship to anyone who can read the repository (and they are
already in every clone, backup, and cache of it).

Fix in your copy (`fixed/config.py`): read secrets from the environment
(`os.environ`), fail loudly when they are missing, and never write a real
value into this file again. See lab.md step 2.
"""

# Defect 1a: a service key that looks real, committed in plain text.
API_KEY = "prod-secret-2f8a1c77b4e9d0136ac5"

# Defect 1b: credentials inside a connection string — they leak through
# logs, error pages, and screenshots just as easily as the key above.
DATABASE_URL = "postgres://svc_admin:Tr0ub4dor-3@db.internal:5432/students"