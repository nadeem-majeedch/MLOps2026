# Independent challenge — Module 01

No step-by-step help here on purpose. You have the concepts and one worked lab;
this task is where you find out whether you can apply them unaided.

!!! info "Why this exists"
    Guided labs teach you the moves; independent challenges tell you whether you
    can play the game. If you feel stuck, that is the point — struggle is where
    the learning happens. Use [concepts.md](concepts.md), the
    [glossary](../../glossary/index.md), and search engines freely. Do **not**
    look for a model answer.

## The task

Find a **public postmortem or paper about a real ML system failure** and write a
**400-word analysis** mapping it onto the lifecycle diagram from concepts §2.

Good starting points (all free):

- Company engineering blogs that publish incident reviews (search
  *"ML incident postmortem"* or *"model degradation postmortem"*).
- Academic papers on ML system failures or technical debt in production.
- The classic write-up: *Hidden Technical Debt in Machine Learning Systems*
  (Sculley et al.) — see [references.md](references.md).

## What to produce

A single Markdown file containing:

1. **Source** — title, author(s), year, URL. If it is a paper, cite it properly.
2. **One-paragraph summary** — what the system was supposed to do, in your words.
3. **Failure mapping table** — at least three failures, each mapped to:

   | Failure (what went wrong) | Lifecycle stage | Technical or organisational? |
   |---|---|---|

4. **The earliest preventable point** — which stage, if done well, would have
   prevented or shortened the failure, and what specifically would have to be
   true there.
5. **What surprised you** — 3–5 sentences, honest.

## Acceptance criteria

- [ ] Source is real, public, and correctly attributed (no invented URLs — check
      that the link opens before you submit).
- [ ] ≥3 failures mapped, each to a *specific* named stage, not "MLOps".
- [ ] At least one failure classified as organisational, with a one-line reason.
- [ ] The "earliest preventable point" is concrete: name the artefact (a test, a
      threshold, a registry entry, a review) that would exist in that stage.
- [ ] 350–450 words of your own analysis (quotes excluded).
- [ ] Filed in your portfolio as `modules/01/challenge-postmortem.md`.

## How to self-mark

| Level | Signal |
|---|---|
| **Meets** | Every checkbox above satisfied; a reader could act on your recommendation |
| **Developing** | Mappings correct but vague ("they needed better monitoring") — sharpen to a named artefact |
| **Not yet** | Source unverified, or fewer than three mapped failures — redo with a different source |

## If you get stuck

1. Re-read concepts §4 (the five failure families) — most real incidents are one of them.
2. Ask yourself of each failure: *"if this stage had a definition of done, would
   this have slipped through?"*
3. Still stuck? Write down *why* you are stuck in one sentence; usually that
   sentence is the answer to the next question.

---

**Next:** [knowledge-check.md](knowledge-check.md) — then mark yourself honestly.

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see [About](../../about/index.md).*