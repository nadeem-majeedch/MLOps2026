# Prerequisites — What You Need Before Starting

Read this page **before** Module 01. It lists the skills, accounts, and machine
resources the course assumes, plus a pre-flight checklist you can run to verify
your setup. Step-by-step installation guides are **not** given here — they belong
in the Module 01/02 pre-flight lessons, which are written against this page as
their specification.

**Labels:** 🪟 Windows 11 + PowerShell (primary) · 🐧 Linux/macOS equivalent ·
☁️ optional cloud account · 💲 real cost · ⚠️ resource-heavy · ✅ verification step

---

## 1. Skills you should already have

| Skill | Why the course needs it | How to shore it up |
|---|---|---|
| Basic Python (variables, functions, loops, classes) | Every example is written in Python | Re-read a beginner Python chapter; Module 02 includes a refresher |
| Reading error messages | Troubleshooting sections expect you to act on tracebacks | Practice: reproduce an error, read the last line first |
| Basic Git (clone, add, commit, status, branch) | Reproducibility depends on version control | A 1-hour Git primer; Module 02 reviews the MLOps-specific workflow |
| Command-line basics (navigate folders, run a program) | All tooling is driven from a terminal | 🪟 PowerShell basics; 🐧 any bash tutorial |
| Introductory statistics and ML (train/test split, overfitting, accuracy) | You will track, validate, and monitor models | An introductory ML course or textbook |

**Not required:** Docker, Kubernetes, CI/CD, orchestration, cloud platforms, or
production experience — all taught in sequence (Modules 11, 12, 13, 16).

## 2. Accounts you need

| Account | Required? | Used for |
|---|---|---|
| GitHub (free) | **Yes** | Hosting your work; Module 12 CI needs it (public repos get free CI minutes) |
| Nothing else | — | Everything on the graded path runs locally |

☁️ Optional extensions in Modules 06, 14, and 16 may demonstrate a cloud service.
Each is labelled ☁️ or 💲, is **never** part of the graded path, and always ships
with a free local equivalent (see
[../syllabus/tool-selection-guide.md](../syllabus/tool-selection-guide.md) §3).

## 3. Software (Windows 11, primary environment)

| Software | Version | Needed from | Notes |
|---|---|---|---|
| Windows 11 | 64-bit | now | Primary platform; all 🪟 commands tested here |
| PowerShell | 5.1 (built-in) or 7+ | now | Course commands are labelled 🪟 |
| Git for Windows | current | now | Includes Git Bash for 🐧-style commands |
| Python | 3.10 – 3.12 | now | One version, used consistently all course long |
| VS Code (or any editor) | current | now | Free; any editor is acceptable |
| Docker **or** Podman | current | Module 11 | ⚠️ Podman is the fully free/open alternative; Docker Desktop is free for students/personal use |
| WSL 2 (Ubuntu) | optional | Module 11+ | ⚠️ One way to run containers on Windows 11; Docker Desktop's WSL backend needs it |
| kind / minikube | current | Module 16 | ⚠️ Local Kubernetes; ~4 GB RAM free |

🐧 Linux/macOS: the same tools natively (bash/zsh, Python, Git, Docker or Podman,
kind). Every command that differs is shown in a `bash` block beside the PowerShell one.

## 4. Machine resources

| Resource | Minimum | Recommended |
|---|---|---|
| Free disk | 15 GB | 30 GB+ (⚠️ container images, datasets, local Kubernetes) |
| RAM | 8 GB | 16 GB (⚠️ Module 16 alone wants ~4 GB free for Kubernetes) |
| Internet | Needed for downloads, Git, CI | Broadband; course text reads offline once cloned |
| CPU | Any 64-bit | **No GPU required** — the course deliberately uses small CPU workloads |

## 5. Time and study habits

- **~150–190 hours** for the whole course; plan on **5–7 hours per week** across
  3.5–5 months (see [../learning-roadmap/index.md](../learning-roadmap/index.md)).
- Work modules in numerical order; each gate assumes the previous ones.
- Always run the ✅ verification step before marking a lesson complete.

## 6. Pre-flight checklist

Run these before Module 01. Each must print a sensible value; if it does not, fix
that item first.

```powershell
# ✅ Version checks — PowerShell
git --version
python --version
$PSVersionTable.PSVersion
```

```bash
# 🐧 Linux / macOS equivalents
git --version
python3 --version
echo "$BASH_VERSION"
```

```powershell
# ✅ Environment sanity — PowerShell
# The folder you will use for the course, and a writable disk with space
Get-Location
Get-PSDrive -Name C | Select-Object Used, Free
```

```bash
# 🐧 Linux / macOS equivalents
pwd
df -h .
```

**Pass criteria:** Git, Python 3.10+, and PowerShell/bash all report versions, and
your course folder is writable with ≥15 GB free. ✅ Containers and Kubernetes are
checked later, immediately before Modules 11 and 16 — do not install them now.

## 7. Known gaps (tracked for the course build)

1. **Pre-flight automation:** a `scripts/` verification script printing one
   PASS/FAIL summary (planned with the Module 01/02 lessons).
2. **Git and Python refresher labs:** assumed knowledge above needs short review
   material so students without that background are not stranded.
3. **Course-wide Python version statement:** to be pinned in Module 01 once the
   example stack is finalised.
4. **Glossary:** referenced terms live in `docs/GLOSSARY.md`, not yet created.

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*
