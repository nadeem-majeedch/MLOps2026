# Independent challenge — Module 02

No step-by-step instructions. You have built an environment once with help;
now do it for something of your own.

## The task

Take **any Python script or small project you have previously written** and make
it reproducible for a stranger:

1. Move it into a new folder and `git init`.
2. Declare its dependencies in `pyproject.toml`.
3. Build a fresh `.venv`, install from that declaration, and run the script.
4. Record exact versions into `requirements.lock`.
5. Write a `README.md` containing: what it does, how to set it up, how to run it,
   and what output to expect.
6. Add a `.gitignore` that keeps environments, data, and artefacts out of history.
7. Make **at least three commits** with messages explaining *why* each change was
   made.

Then the real test: **hand it to someone else** — a classmate, a friend, or
yourself on another machine/folder — and give them only the repository. Time how
many questions they ask you.

## Acceptance criteria

- [ ] `pyproject.toml` lists every dependency actually used (grep your imports
      and check each one — no extras, none missing).
- [ ] A fresh `.venv` + install reproduces your stated expected output **exactly**
      (paste it into the README).
- [ ] `requirements.lock` committed; `.venv/`, data, and artefacts are **not**
      committed (`git status --short` proves it).
- [ ] README alone is sufficient: the rebuild required **zero** verbal
      explanation.
- [ ] ≥3 commits, each with a reason rather than "update".
- [ ] Filed in your portfolio as `modules/02/challenge-reproducible-project.md`
      (the repository itself can be linked or attached).

## How to self-mark

| Level | Signal |
|---|---|
| **Meets** | Rebuild needs only the README; output matches; history is clean and reasoned |
| **Developing** | Works, but only with a hint from you — record *which* hint; that is your TODO |
| **Not yet** | Requires you to remember anything unwritten |

## If you get stuck

1. The most common trap: you installed with plain `pip` instead of the
   `.venv` interpreter — check `sys.executable` first, always.
2. If a dependency is missing from `pyproject.toml`, the error appears at *import*
   time, not install time — that asymmetry is why step 7's grep exists.
3. If the output differs between machines, diff the two `pip freeze` files before
   anything else.

---

**Next:** [knowledge-check.md](knowledge-check.md).

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*