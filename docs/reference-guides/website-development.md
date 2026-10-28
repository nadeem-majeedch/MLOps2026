# Website Development (for contributors)

How the course website is built and the rules for changing it. Students never
need this page — students read the published site or
[the Markdown on GitHub](https://github.com/nadeem-majeedch/MLOps).

---

## 1. What the site is

| | |
|---|---|
| **Generator** | [MkDocs](https://www.mkdocs.org/) — a static site generator written in Python |
| **Theme** | [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) |
| **Source** | every `.md` file under `docs/` |
| **Configuration** | [`mkdocs.yml`](https://github.com/nadeem-majeedch/MLOps/blob/main/mkdocs.yml) at the repository root |
| **Dependencies** | `requirements-docs.txt` |
| **Build output** | `site/` — generated, ignored by Git (see `.gitignore`) |

Nothing JavaScript-heavy is used: the theme's built-in search and the dark/light
palette toggle are the only client-side behaviour. There are no trackers, no
external embeds, and no third-party CDNs — the site works from a plain static
host, including offline from a local build.

## 2. How a page becomes a website

1. Write Markdown under `docs/`.
2. Add the page to `nav` in `mkdocs.yml` — **a page missing from `nav` is
   invisible to students** even though it still builds.
3. Run `mkdocs build --strict` (see [local preview](local-preview.md)).
4. Fix every warning: `--strict` turns warnings into build failures on purpose.

### Paths

- The repository is a GitHub **project site** named `MLOps`, so the published URL
  is `https://nadeem-majeedch.github.io/MLOps/`. `site_url` in `mkdocs.yml` records
  this; MkDocs handles the base path for asset and page URLs automatically.
- Always write **relative** links between Markdown files
  (`[Glossary](../glossary/index.md)`), never absolute `/...` paths. Relative links
  work on GitHub, in MkDocs, and in any other renderer.
- A link must never point outside `docs/` (for example to the root `README.md`):
  it resolves on GitHub but breaks on the site. Link to `about/index.md` instead.

## 3. Navigation sections

`nav` mirrors how a student thinks about the course:

| Section | Contains |
|---|---|
| Start Here | First-day guide, progress checklist, prerequisites, learning roadmap |
| Foundations | Modules 01–05 |
| Intermediate | Modules 06–12 |
| Advanced | Modules 13–17 |
| Labs | The 17 guided laboratories |
| Projects | Mini-projects and capstone |
| Assessments | Self-assessment scheme and rubrics |
| Reference | Glossary, troubleshooting, resources, syllabus documents, technical guides |
| About | Instructor identity, credits, standards, build roadmap |

**Every module and every lab must be reachable from `nav`.** When a module is
added or renumbered, update `nav`, the labs list, and the module's previous/next
links in the same change.

## 4. Writing rules for site pages

- **One `#` H1 per page**, no skipped heading levels (screen readers navigate by
  heading level; `##` then `###`).
- **Meaningful link text**: write `read the pre-flight checklist`, never
  `click here` or a bare URL.
- **Alt text** on every image (`![Pipeline diagram showing ...](...)`).
- Tables stay narrow (≤5 columns) and carry a header row.
- Admonitions (`!!! note`, `!!! warning`) for callouts; do not fake them with
  bold text.
- Fenced code blocks always carry a language tag for syntax highlighting.
- Keep the source readable on GitHub: if a page only renders well on the website,
  it is written wrong.

## 5. Assets and diagrams

- Store images in `docs/assets/img/` (create when first needed) and reference them
  with relative paths.
- Only use assets you may redistribute: your own drawings, CC0/CC-BY material with
  attribution, or screenshots you captured.
- Prefer a text/ASCII diagram in Markdown when it conveys the idea — it stays
  readable on GitHub and needs no asset management.

## 6. Generated pages

The 17 pages under `docs/modules/NN-*/index.md` are **generated from the syllabus**
so they cannot drift from it. They were produced by extracting each module's
section from `docs/syllabus/detailed-syllabus.md`. When the syllabus changes,
regenerate or hand-sync those pages, then re-run the link check.

## 7. Definition of done for any site change

- [ ] `python scripts/check_course.py` — links, anchors, nav, module
      sections, Python syntax (all four `[PASS]`)
- [ ] `python -m mkdocs build --strict` exits 0 with no warnings.
- [ ] Every new page is in `nav`.
- [ ] All relative links resolve (file and `#anchor`).
- [ ] Heading hierarchy is unbroken; link text is meaningful.
- [ ] The page reads correctly as plain Markdown on GitHub.
- [ ] No install/build instructions were added to the root `README.md` — they
      belong here or in [local preview](local-preview.md).

---

*Course designed and maintained by Engr. Dr. Muhammad Nadeem Majeed — see
[About](../about/index.md).*