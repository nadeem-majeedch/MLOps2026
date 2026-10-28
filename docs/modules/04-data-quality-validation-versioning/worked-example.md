# Worked example — a validator, run four times

The validator is `src/validate.py` in the shared example: seven checks in plain
pandas, one result per check, exit code `0` only if everything passes. Every
output below is the **actual** output from running it on the reference machine.

---

## 1. The checks

```python
# src/validate.py — the seven rules (abbreviated; read the file for the rest)
REQUIRED_COLUMNS = [...]                    # schema
NUMERIC_COLUMNS  = [...]                   # types
nulls  = df[REQUIRED].isna().sum()         # completeness
dupes  = df["customer_id"].duplicated()     # uniqueness
(df["tenure_months"] >= 0).all()            # range
set(df["contract_type"]) <= ALLOWED        # domain
0.02 <= df["churn"].mean() <= 0.50          # target sanity
```

Run it:

```powershell
# 🪟 Windows / PowerShell — from examples/churn
python -m src.validate --data data/raw/churn.csv
```

```bash
python3 -m src.validate --data data/raw/churn.csv
```

## 2. The good extract — all seven pass

```text
file: data/raw/churn.csv   rows=2000   checks=7

  [PASS] required_columns         missing columns: none
  [PASS] column_types             non-numeric columns: none
  [PASS] no_missing_values        columns with nulls: none
  [PASS] unique_customer_id       duplicate keys: 0
  [PASS] value_ranges             tenure_months >= 0 and monthly_charges > 0
  [PASS] allowed_contract_types   unexpected values: none
  [PASS] target_sane              target values ok=True, positive rate=0.091 (accept 0.02..0.50)

7/7 checks passed
```

Exit code: **0**. ✅ This is the state your gate must reach on healthy data —
and, just as importantly, must *not* reach on unhealthy data, which the next
three runs prove.

## 3. Defect 1 — missing values

```powershell
python -m src.validate --data data/corrupt/missing.csv
```

Actual output (differences only):

```text
  [FAIL] no_missing_values        columns with nulls: monthly_charges=120
  [FAIL] value_ranges             tenure_months >= 0 and monthly_charges > 0

5/7 checks passed
```

Exit code: **1**.

**Reading it:** 120 of 2,000 rows (6%) lost `monthly_charges`. Two checks fired —
completeness found the nulls, and the range check also failed because `NaN > 0` is
not true. Two independent checks agreeing is *good*: you are not relying on one
person's idea of "broken".

## 4. Defect 2 — duplicate keys

```text
  [FAIL] unique_customer_id       duplicate keys: 75

6/7 checks passed
```

Exit code: **1** (file has 2,075 rows instead of 2,000).

**Reading it:** 75 duplicated customers. If this reached training, those
customers would appear twice — in the training set *and* possibly straddling the
train/test split, leaking labels. A uniqueness check costs milliseconds and
prevents a class of "suspiciously good results".

## 5. Defect 3 — type damage

```text
  [FAIL] no_missing_values        columns with nulls: monthly_charges=15
  [FAIL] value_ranges             tenure_months >= 0 and monthly_charges > 0

5/7 checks passed
```

Exit code: **1**.

**Interesting detail — and an honest one:** the `column_types` check **passed**.
Why? Because `pandas.read_csv` *infers* types: the numeric-looking text values
("100.00") were parsed as numbers automatically, and the 15 `"n/a"` entries
became `NaN`. So the damage surfaced as missingness, not as a wrong dtype.

**Lesson:** validation must test *meaning*, not only *types* — and you should not
assume a parser saved you. If you need the guarantee, read with an explicit
`dtype=` and see this exact file fail differently.

## 6. Versioning — freezing the bytes

Now prove you could get that good file back. (DVC 3.67.1, run inside
`examples/churn/`; `--no-scm` is used here because this folder is not itself a
Git repository — inside a real repo you would omit it.)

```powershell
# 🪟 Windows / PowerShell
python -m dvc init --no-scm
python -m dvc add data/raw/churn.csv
Get-Content data\raw\churn.csv.dvc
```

Actual content of `churn.csv.dvc`:

```text
outs:
- md5: 18df7e78d2f419439cdc4b98a592ab99
  size: 60755
  hash: md5
  path: churn.csv
```

Check status:

```powershell
python -m dvc status
```

Actual output:

```text
Data and pipelines are up to date.
```

The recorded `18df7e78…` is the file's content hash — you can confirm with
`md5sum data/raw/churn.csv` 🐧 / `Get-FileHash` 🪟.

## 7. Break it, watch it notice, restore it

```powershell
# 🪟 modify the working file
Add-Content data\raw\churn.csv "junk,row`n1,2"
python -m dvc status
```

Actual output:

```text
data\raw\churn.csv.dvc:
	changed outs:
		modified:           data\raw\churn.csv
```

Now restore:

```powershell
python -m dvc checkout
```

**Actual output (a refusal — and a good one):**

```text
ERROR: Can't remove the following unsaved files without confirmation. Use `--force` to force.
C:\...\data\raw\churn.csv
```

DVC will not silently delete your local edit. Once you are sure the local change
is disposable:

```powershell
python -m dvc checkout --force
```

Actual output and verification:

```text
M       data\raw\churn.csv
# md5 now matches again:
18df7e78d2f419439cdc4b98a592ab99 *data/raw/churn.csv
```

✅ **Checkpoint:** the hash is back to `18df7e78…`. That is *versioning*: not
"the file looks similar", but byte-for-byte proof.

!!! note "What you just observed"
    `status` detects, `checkout` restores, `--force` is the explicit consent
    step. The same trio of ideas appears again as CI gates (Module 12) and
    rollback (Modules 09 and 16) — detect, restore, confirm deliberately.

## 8. Clean up your DVC experiment

```powershell
# 🪟 back to a pristine example folder
Remove-Item -Recurse .dvc, .dvcignore, data\raw\churn.csv.dvc, data\.gitignore -ErrorAction SilentlyContinue
python generate_data.py     # regenerate to be certain
```

(The lab walks through this as its Cleanup step.)

---

**Next:** [lab.md](lab.md) — catch all three defects yourself, then version and restore the good file.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*