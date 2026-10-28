# Assessment Template

> **How to use this file:** copy it to `modules/NN-slug/assessments/quiz-NN-a.md` (or `assignment-…`, `exam-…`) per [COURSE-STANDARDS.md §5](../COURSE-STANDARDS.md#5-filename-and-path-conventions). Create the matching answer key as `modules/NN-slug/assessments/keys/<name>-KEY.md`. Delete the italic guidance lines. Do not rename, merge, or skip sections.

---

```markdown
# Quiz NN-A — Title

**Module:** NN — Module name
**Type:** Quiz | Assignment | Practical | Exam
**Level:** Beginner | Intermediate | Advanced
**⏱️ Estimated time:** X minutes
**Total marks:** NN
**Allowed resources:** Closed book | Open notes and docs/ | Tooling allowed (state which)

## Instructions for students
*How to answer, how marks are distributed, whether partial credit exists, and where
to submit. State that every question uses only material covered up to this module.*

---

## Part A — Recall and vocabulary
*Short-answer and definition questions. Every term tested must have been defined
before first use in this module.*

**A1.** *(marks)* Question text.

**A2.** *(marks)* Question text.

## Part B — Comprehension
*Application, comparison, and reasoning questions (explain why, diagnose, choose
between two approaches and justify).*

**B1.** *(marks)* Question text.

## Part C — Practical
*Hands-on: run/modify/verify a snippet, interpret provided output, or complete a
lab-derived task. Provide all input material inside the question — do not depend
on files outside the module.*

**C1.** *(marks)* Question text, including what output to show.

---

# Answer Key — Quiz NN-A (in keys/quiz-NN-a-KEY.md)

*Not shipped in the student file. One entry per question.*

**A1.** *(marks)* Model answer / marking points.

**A2.** *(marks)* Model answer / marking points.

**B1.** *(marks)* Model answer, plus explicitly which points earn which marks.

**C1.** *(marks)* Expected output and rubric; note acceptable variations across
operating systems or library versions.

## Rubric (assignments, practicals, exams)
| Criterion | Excellent | Satisfactory | Failing | Marks |
|---|---|---|---|---|
| *e.g. reproducibility* | *seed, versions, expected output verified* | *works but undocumented* | *cannot be rerun* | *x* |

## Moderation notes
*Common wrong answers, borderline cases, and the rationale for the mark split.
Author-facing; delete from the student copy.*
```

---

## Assessment design rules

1. **Coverage:** every learning objective in the module's README maps to at least one question; every question maps to an objective.
2. **Bloom mix:** quizzes are roughly 40% recall/comprehension, 60% application; assignments and practicals are mostly application and analysis.
3. **Vocabulary:** only terms defined up to that module may be tested.
4. **Fairness:** no question depends on a paid tool, a cloud account, or a specific operating system; practical questions must state what output to submit.
5. **Honesty:** answer keys live only in `assessments/keys/` and are never linked from the student-facing file.
6. **Verification:** any command in a question or key must be run once and its output checked before the assessment ships.
