# Worked example — build an environment, then watch it disagree

Everything below was executed on the reference machine (Windows 11, PowerShell,
Python 3.14.7) inside `examples/churn/`. Output blocks are what the commands
actually printed.

---

## 1. Which interpreter answers?

```powershell
# 🪟 Windows / PowerShell
python --version
python -c "import sys; print(sys.executable)"
```

Actual output:

```text
Python 3.14.7
C:\Python314\python.exe
```

**Why this matters:** the second line is the only honest answer to "which Python
am I using?". If it prints a path inside a `.venv`, you are in that environment;
if it prints your system path, you are not.

## 2. Create an isolated environment

```powershell
# 🪟 Windows / PowerShell — from examples/churn
python -m venv .venv
```

```bash
# 🐧 Linux / macOS
python3 -m venv .venv
```

No output means success (the Unix way). ✅ Verify:

```powershell
Test-Path .venv\Scripts\python.exe    # 🪟 expect: True
```

## 3. Install the project's dependencies into it

```powershell
# 🪟 Windows / PowerShell
.venv\Scripts\python -m pip install pandas numpy scikit-learn PyYAML joblib pytest pytest-cov
```

```bash
# 🐧 Linux / macOS
.venv/bin/python -m pip install pandas numpy scikit-learn PyYAML joblib pytest pytest-cov
```

On the reference machine this took **7 minutes 44 seconds** first time (pip had
to download wheels); later runs are much faster because pip caches downloads.
⚠️ Budget the time — do not start this five minutes before you need it.

## 4. Verify — with versions, not vibes

```powershell
.venv\Scripts\python -c "import sys, pandas, sklearn, pytest; \
print('python', sys.version.split()[0]); print('pandas', pandas.__version__); \
print('sklearn', sklearn.__version__); print('pytest', pytest.__version__)"
```

Actual output:

```text
python 3.14.7
pandas 3.1.0
sklearn 1.9.1
pytest 9.1.1
```

✅ **Checkpoint:** all four lines print. If one raises `ModuleNotFoundError`, the
package was installed into a different interpreter — re-run §3 with the same
`.venv\Scripts\python` prefix.

## 5. Record exactly what you installed (the lock step)

```powershell
.venv\Scripts\python -m pip freeze | Select-String -Pattern '^(pandas|numpy|scikit-learn|PyYAML|joblib|pytest)=='
```

Actual output:

```text
joblib==1.6.0
numpy==2.5.4
pandas==3.1.0
pytest==9.1.1
PyYAML==6.0.3
scikit-learn==1.9.1
```

Save the full `pip freeze` output as `requirements.lock` in your project. This
list — not your memory — is what makes a rebuild reproducible.

## 6. The disagreement experiment (the point of the module)

Now compare the environment you just made with the system interpreter:

```powershell
python -c "import pandas, sys; print('system :', pandas.__version__, '|', sys.executable)"
.venv\Scripts\python -c "import pandas, sys; print('venv    :', pandas.__version__, '|', sys.executable)"
```

Actual output on the reference machine:

```text
system : 3.0.6 | C:\Python314\python.exe
venv    : 3.1.0 | C:\Users\...\examples\churn\.venv\Scripts\python.exe
```

**Same machine, same day, two pandas versions.** Any result you produce with one
is not guaranteed to reproduce with the other — pandas has changed behaviour
between minor versions before, and will again. This is not a hypothetical: it is
why step 5 exists.

## 7. Run the project's tests inside the environment

```powershell
# 🪟 Windows / PowerShell
.venv\Scripts\python -m pytest
```

Actual output:

```text
...................                                                      [100%]
19 passed in 3.73s
```

✅ **Checkpoint:** `19 passed` and exit code 0. If you see fewer tests, you are
in the wrong folder (`tests/` must be next to `pyproject.toml`).

*(Those tests belong to Module 07 — here they only prove the environment can run
the project. Do not read ahead; you will build them yourself later.)*

## 8. Exit codes: the machine-readable verdict

```powershell
.venv\Scripts\python -m pytest; echo "exit=$LASTEXITCODE"
```

`exit=0` means success; `1` means failures. Scripts, Makefiles (Module 08), and
CI (Module 12) all branch on exactly this number — which is why "it printed
something sensible" is not a verification method.

## 9. What you just did, in lifecycle terms

| Step | Lifecycle stage it supports |
|---|---|
| 1–2 Choose and isolate an interpreter | Reproducible foundation for every later stage |
| 3–4 Install and verify | Package/deploy — you can rebuild anywhere |
| 5 Lock versions | Environment reproducibility (the second leak from Module 01) |
| 6 Compare environments | Evidence that pinning is necessary, not bureaucratic |
| 7–8 Verify with tests and exit codes | The habit that Modules 07 and 12 automate |

---

**Next:** [lab.md](lab.md) — rebuild a teammate's environment from only their
repository, including two deliberate breakages you must fix.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*