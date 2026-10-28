# LAB-03 — reference solution

> Attempt the lab first. This is the answer key, not the assignment.

## "Before" transcript (verified, authoring machine)

```text
rows=603 cols=['customer_id', 'tenure_months', 'monthly_charges',
               'promo_flag', 'contract_type', 'churned']
[check_missing]   ERROR missing: 3 empty values in 'monthly_charges'
[check_missing]   ERROR missing: 2 empty values in 'contract_type'
[check_ranges]    ERROR range: 1 values of 'tenure_months' outside [0, 120]
[check_ranges]    ERROR range: 1 values of 'monthly_charges' outside [0, 500]
[check_ranges]    ERROR dtype: 1 non-numeric values in 'monthly_charges'
[NOT IMPLEMENTED] check_duplicates
[NOT IMPLEMENTED] check_label_domain
[NOT IMPLEMENTED] check_schema
[NOT IMPLEMENTED] check_cardinality

5 error(s), 4 check(s) not implemented
```

## The four checks you must write — what they find in this file

| Check | Reference finding in `customers_dirty.csv` |
|---|---|
| `check_duplicates` | **3** duplicate `customer_id`s, and they are full-row duplicates (3 `df.duplicated()` rows) |
| `check_label_domain` | **1** row with `churned = 7` — labels must be exactly {0, 1} |
| `check_schema` | columns **match** `EXPECTED_COLUMNS` in this file → passes today |
| `check_cardinality` | values are exactly {monthly, one_year, two_year} → passes today |

Skeleton consistent with the fixture's message format:

```python
def check_duplicates(df):
    findings = []
    dup_ids = int(df["customer_id"].duplicated().sum())
    if dup_ids:
        findings.append(f"ERROR duplicate: {dup_ids} repeated customer_id values")
    full = int(df.duplicated().sum())
    if full:
        findings.append(f"ERROR duplicate: {full} fully repeated rows")
    return findings

def check_label_domain(df):
    bad = sorted(set(df["churned"].dropna().unique()) - {0, 1})
    return ([f"ERROR label: churned contains {bad} (allowed: 0, 1)"]
            if bad else [])

def check_schema(df):
    if list(df.columns) != EXPECTED_COLUMNS:
        return [f"ERROR schema: expected {EXPECTED_COLUMNS}, got {list(df.columns)}"]
    return []

def check_cardinality(df):
    known = {"monthly", "one_year", "two_year"}
    bad = sorted(set(df["contract_type"].dropna().unique()) - known)
    return ([f"ERROR domain: unknown contract_type {bad}"] if bad else [])
```

**Expected finished output:** `5 + 4 = 9` error lines (5 implemented
before + duplicates(2) + label(1)); schema and cardinality add **no**
lines today — run `--strict` and confirm exit 1 anyway (skipped checks
must also fail strict mode; the fixture already enforces that).

## Reasoning checkpoints (model answers)

- **Why keep checks that pass today?** A gate is a *contract*, not a
  bug list. Schema and cardinality passed today and broke last month's
  pipeline — that is precisely the argument for keeping them.
- **The `support_calls` → `promo_flag` change:** the expected schema in
  the file *already reflects the current contract*, so this run passes.
  The finding belongs in your write-up: a contract changed, the gate was
  updated to match — who approved that, and did downstream features get
  retrained? A gate can only police the contract you told it about.
- **ERROR vs WARN:** anything that corrupts training (missing, bad
  labels, schema drift) is ERROR → block. Cosmetic issues (a rare but
  legal category) are WARN → report, don't block.

## Common wrong answers

- Duplicates checked on whole rows only — misses the same id with
  *different* values (the sneakier case).
- `churned == 7` treated as missing (NaN) — it is a wrong value, not an
  absent one; say which it is.
- Silently dropping bad rows instead of reporting them — the gate's job
  is to refuse, not to launder dirty data.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../../docs/about/index.md).*