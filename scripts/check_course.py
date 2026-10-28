"""Course integrity checks — the local equivalent of the validation workflow.

    python scripts/check_course.py            # run every check
    python scripts/check_course.py --list     # show what is checked

Checks (each prints PASS or a list of findings; exit 1 if anything failed):

  1. navigation   — every nav entry exists; every module index and every
                    standalone lab page appears in nav (course rule:
                    "invisible to students" pages are a defect)
  2. links        — every relative Markdown link inside docs/ resolves to a
                    file that exists; anchors resolve to a heading or an
                    explicit { #id } in the target
  3. modules      — each of the 17 module folders ships the nine required
                    files and its index.md carries an H1
  4. python       — every .py file under examples/ and scripts/ compiles
                    (syntax only; behaviour is the test suites' job)

Deliberately dependency-free (stdlib only) so it runs before anything is
installed. CI runs exactly this file: see .github/workflows/validate-course.yml.
"""

from __future__ import annotations

import argparse
import pathlib
import py_compile
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

REQUIRED_MODULE_FILES = [
    "index.md",
    "learning-objectives.md",
    "concepts.md",
    "worked-example.md",
    "lab.md",
    "independent-challenge.md",
    "knowledge-check.md",
    "troubleshooting.md",
    "references.md",
]

SKIP_DIRS = {".venv", "venv", "__pycache__", "site", "node_modules",
             ".git", ".pytest_cache", ".ruff_cache"}

LINK_RE = re.compile(r"\]\((?!https?://|mailto:|#)([^)\s]+?)(#[^)\s]*)?\)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.*?)\s*(?:\{ #([A-Za-z0-9_-]+) \})?\s*$",
                        re.MULTILINE)


def slugify(heading: str) -> str:
    """GitHub/MkDocs-style anchor slug: lowercase, strip punctuation."""
    text = re.sub(r"[`*_~]", "", heading).lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    return re.sub(r"[\s]+", "-", text.strip())


def anchors_of(path: pathlib.Path) -> set[str]:
    found: set[str] = set()
    for text, explicit in HEADING_RE.findall(
            path.read_text(encoding="utf-8")):
        if explicit:
            found.add(explicit)
        found.add(slugify(text))
    return found


def read_nav() -> tuple[list[str], str | None]:
    nav = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    entries = re.findall(r":\s*([A-Za-z0-9_./-]+\.md)", nav)
    return entries, None


def check_nav() -> list[str]:
    problems: list[str] = []
    entries, _ = read_nav()
    for entry in entries:
        if not (DOCS / entry).exists():
            problems.append(f"nav entry points at a missing file: {entry}")

    in_nav = set(entries)
    must_be_visible = [str(p.relative_to(DOCS)).replace("\\", "/")
                       for p in DOCS.glob("modules/*/index.md")]
    must_be_visible += [str(p.relative_to(DOCS)).replace("\\", "/")
                        for p in DOCS.glob("labs/lab-*.md")]
    for page in sorted(must_be_visible):
        if page not in in_nav:
            problems.append(f"page missing from nav (invisible to students): "
                            f"{page}")
    return problems


def strip_code_blocks(text: str) -> str:
    """Remove fenced code blocks — they contain example links, not links."""
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def check_links() -> list[str]:
    problems: list[str] = []
    for md in sorted(DOCS.rglob("*.md")):
        rel = md.relative_to(DOCS)
        body = strip_code_blocks(md.read_text(encoding="utf-8"))
        for target, fragment in LINK_RE.findall(body):
            resolved = (md.parent / target.split("#")[0]).resolve()
            try:
                resolved.relative_to(DOCS.resolve())
            except ValueError:
                problems.append(f"{rel}: link escapes docs/: {target}")
                continue
            if not resolved.exists():
                problems.append(f"{rel}: broken link -> {target}")
                continue
            if fragment and resolved.suffix == ".md":
                anchor = fragment.lstrip("#")
                if anchor not in anchors_of(resolved):
                    problems.append(f"{rel}: missing anchor #{anchor} "
                                    f"in {target}")
    return problems


def check_modules() -> list[str]:
    problems: list[str] = []
    module_dirs = sorted(p for p in (DOCS / "modules").iterdir() if p.is_dir())
    if len(module_dirs) != 17:
        problems.append(f"expected 17 module folders, found {len(module_dirs)}")
    for module in module_dirs:
        for name in REQUIRED_MODULE_FILES:
            if not (module / name).exists():
                problems.append(f"{module.name}: missing required file {name}")
        index = module / "index.md"
        if index.exists():
            first = index.read_text(encoding="utf-8").split("\n", 1)[0]
            if not first.startswith("# "):
                problems.append(f"{module.name}: index.md has no H1 heading")
    return problems


def check_python() -> list[str]:
    problems: list[str] = []
    for folder in ("examples", "scripts"):
        for py in sorted((ROOT / folder).rglob("*.py")):
            if set(py.parts) & SKIP_DIRS:
                continue
            try:
                py_compile.compile(str(py), doraise=True)
            except py_compile.PyCompileError as exc:
                problems.append(f"{py.relative_to(ROOT)}: {exc.msg}")
    return problems


CHECKS = [
    ("navigation", check_nav),
    ("links+anchors", check_links),
    ("module sections", check_modules),
    ("python syntax", check_python),
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="course integrity checks")
    parser.add_argument("--list", action="store_true",
                        help="print the checks and exit")
    args = parser.parse_args(argv)

    if args.list:
        for name, fn in CHECKS:
            print(f"{name:16} {fn.__doc__ or fn.__name__}")
        return 0

    failed = 0
    for name, fn in CHECKS:
        problems = fn()
        if problems:
            failed += len(problems)
            print(f"[FAIL] {name}")
            for problem in problems:
                print(f"       - {problem}")
        else:
            print(f"[PASS] {name}")
    if failed:
        print(f"\n{failed} problem(s) found — fix before pushing.")
        return 1
    print("\nall course integrity checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())