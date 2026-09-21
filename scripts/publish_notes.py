#!/usr/bin/env python3
"""Publish a course folder of Obsidian notes as static HTML pages on this site.

    python3 scripts/publish_notes.py ecoevo2026             # build notes/ecoevo2026/
    python3 scripts/publish_notes.py ecoevo2026 --dry-run   # report only, write nothing
    python3 scripts/publish_notes.py ecoevo2026 --push      # build, then git commit + push

Source: <vault>/WebsiteNotes/<course>/*.md. The vault is only read, never written.
Only notes whose `publish` property is true are published: tick the checkbox in
Obsidian's Properties, or put `publish: true` in the front matter. A page that this
script made earlier for a note that is no longer published is deleted.
In the index, lines that link to an unpublished note of the course are hidden, so
the index can list every lecture and only the ready ones appear online.

Output: notes/<course>/<name>.html, one page per published note, file names
lower-cased as in the Obsidian "Webpage HTML Export" used for bg2025/qsb2024/sc2025.
Needs pandoc (brew install pandoc). Math is typeset in the browser by MathJax 4.

Obsidian syntax handled
  [[Note]], [[Note|alias]], [[Note#Heading|alias]], [[#Heading]]
      -> links to published pages of this course, or of a course already under
         notes/; anything else becomes plain text (reported).
  ![[file.pdf]], ![[image.png]], ![[image.png|300]]
      -> file copied to notes/<course>/material/, then linked (pdf) or shown.
  > [!type] Title, > [!type]- Title (callouts) -> box, or collapsible <details>.
  single newlines -> line breaks (Obsidian default, "strict line breaks" off).

Private content, removed from the public pages
  %% comments %%;
  callouts whose title starts with "Written by Claude";
  sections whose title is in PRIVATE_SECTIONS (down to the next heading of the same
  or higher level);
  lines containing "*to be made*".
"""
import argparse
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
VAULT = Path.home() / "Documents" / "WORKNOTES_remote"
NOTES_DIR = "WebsiteNotes"  # vault folder
SITE_DIR = "notes"          # site folder: https://jacopogrilli.github.io/notes/<course>/
TEMPLATE = SITE / "scripts" / "notes_template.html"
GENERATOR_TAG = '<meta name="generator" content="publish_notes.py">'  # must match the template
PRIVATE_SECTIONS = {"Material", "Differences from the old notes", "Where the material lives"}
PLACEHOLDER = "*to be made*"
PANDOC_FROM = ("markdown+tex_math_dollars+pipe_tables+hard_line_breaks+autolink_bare_uris"
               "-yaml_metadata_block-implicit_figures")
MATHJAX = "https://cdn.jsdelivr.net/npm/mathjax@4/tex-chtml.js"  # v4 breaks long formulas
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}

FRONTMATTER_RE = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*(?:\n|\Z)", re.S)
CALLOUT_RE = re.compile(r"^>\s*\[!(?P<type>[\w-]+)\](?P<fold>[+-]?)\s*(?P<title>.*)$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
WIKILINK_RE = re.compile(r"(!?)\[\[([^\]|#\\]*)(#[^\]|\\]*)?(?:\\?\|([^\]]*))?\]\]")
PROTECT_RE = re.compile(r"(\$\$.*?\$\$|\$[^$\n]+?\$|`[^`\n]+`)", re.S)


def split_frontmatter(text):
    """(properties, body). Only flat `key: value` lines are read."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    props = {}
    for line in m[1].splitlines():
        key, sep, value = line.partition(":")
        if sep and not line[:1].isspace() and not line.startswith("-"):
            props[key.strip()] = value.strip().strip("'\"")
    return props, text[m.end():]


def is_published(note):
    props, _ = split_frontmatter(note.read_text(encoding="utf-8"))
    return props.get("publish", "").lower() in {"true", "yes", "1"}


def web_name(stem):
    """File name as written by the Obsidian exporter: lower case, spaces -> hyphens."""
    return re.sub(r"\s+", "-", stem.strip()).lower()


def heading_id(text):
    """pandoc's auto_identifiers, for plain-text headings."""
    s = re.sub(r"\$[^$]*\$", "", text)
    s = re.sub(r"[*_`\[\]]", "", s).strip().lower()
    s = "".join(c for c in s if c.isalnum() or c in "_-. ")
    s = re.sub(r"\s+", "-", s)
    return re.sub(r"^[^a-z]+", "", s) or "section"


def plain(text):
    """Strip markdown and emoji, for <title> and the header."""
    s = re.sub(r"[*_`#]", "", text)
    s = "".join(c for c in s if unicodedata.category(c) != "So")
    return re.sub(r"\s+", " ", s).strip()


class Page:
    def __init__(self, course, src_dir, out_dir, note, published):
        self.course, self.src, self.out, self.note = course, src_dir, out_dir, note
        self.published = published  # stems of the notes published in this course
        self.log, self.copies = [], []

    # ---- private content -------------------------------------------------
    def strip_private(self, text):
        text, n = re.subn(r"%%.*?%%", "", text, flags=re.S)
        if n:
            self.log.append(f"removed {n} %%comment%%")
        out, skip_level, in_code = [], None, False
        for line in text.split("\n"):
            if line.lstrip().startswith("```"):
                in_code = not in_code
            m = None if in_code else HEADING_RE.match(line)
            if m:
                level, title = len(m[1]), m[2]
                if skip_level is not None and level <= skip_level:
                    skip_level = None
                if skip_level is None and title in PRIVATE_SECTIONS:
                    skip_level = level
                    self.log.append(f"removed section: {title}")
                    continue
            if skip_level is not None:
                continue
            if PLACEHOLDER in line:
                self.log.append(f"removed placeholder line: {line.strip()[:60]}")
                continue
            out.append(line)
        return out

    def hide_unpublished(self, lines):
        """In the index only: drop lines that link to a note of this course that is not published."""
        if self.note.stem != "index":
            return lines
        out = []
        for line in lines:
            hidden = None
            for m in WIKILINK_RE.finditer(line):
                if m[1]:
                    continue
                target = m[2].strip()
                parts = (target[:-3] if target.endswith(".md") else target).split("/")
                same_course = len(parts) == 1 or (len(parts) >= 3 and parts[:2] == [NOTES_DIR, self.course])
                if same_course and (self.src / f"{parts[-1]}.md").exists() and parts[-1] not in self.published:
                    hidden = parts[-1]
            if hidden:
                self.log.append(f"hid index line (links unpublished {hidden}): {line.strip()[:50]}")
            else:
                out.append(line)
        return out

    # ---- callouts --------------------------------------------------------
    def callouts(self, lines):
        out, i = [], 0
        while i < len(lines):
            m = CALLOUT_RE.match(lines[i])
            if not m:
                out.append(lines[i])
                i += 1
                continue
            j, body = i + 1, []
            while j < len(lines) and lines[j].startswith(">"):
                body.append(re.sub(r"^>\s?", "", lines[j]))
                j += 1
            kind, fold = m["type"].lower(), m["fold"]
            title = m["title"].strip() or kind.capitalize()
            if title.startswith("Written by Claude"):
                self.log.append("removed callout: Written by Claude")
                if j < len(lines) and not lines[j].strip():
                    j += 1
            elif fold:
                opened = " open" if fold == "+" else ""
                out += ["", f'<details class="callout callout-{kind}"{opened}>',
                        f"<summary>{title}</summary>", "", *body, "", "</details>", ""]
            else:
                out += ["", f"::: {{.callout .callout-{kind}}}", f"[{title}]{{.callout-title}}",
                        "", *body, ":::", ""]
            i = j
        return out

    # ---- links and embeds --------------------------------------------------
    def find_file(self, name):
        for cand in (self.src / name, self.src / "material" / name):
            if cand.is_file():
                return cand
        hits = sorted(VAULT.rglob(name))
        return hits[0] if hits else None

    def embed(self, target, alias):
        src = self.find_file(target.strip())
        if src is None:
            self.log.append(f"embed not found: {target}")
            return alias or target
        dest = f"material/{web_name(src.stem)}{src.suffix.lower()}"
        self.copies.append((src, self.out / dest))
        if src.suffix.lower() in IMAGE_EXT:
            size = f"{{width={alias}}}" if alias and alias.isdigit() else ""
            return f"![{'' if size else (alias or '')}]({dest}){size}"
        return f"[{alias or src.name}]({dest})"

    def link(self, target, anchor, alias, page_ids):
        target = target.strip()
        anchor = anchor[1:] if anchor else ""
        if not target:
            hid = heading_id(anchor)
            if hid in page_ids:
                return f"[{alias or anchor}](#{hid})"
            self.log.append(f"unresolved heading link: #{anchor}")
            return alias or anchor
        parts = (target[:-3] if target.endswith(".md") else target).split("/")
        name = parts[-1]
        course = parts[1] if len(parts) >= 3 and parts[0] == NOTES_DIR else None
        if course is None and len(parts) == 1 and (self.src / f"{name}.md").exists():
            course = self.course
        href = None
        if course == self.course:
            if name in self.published:
                href = f"{web_name(name)}.html"
        elif course and (SITE / SITE_DIR / course / f"{web_name(name)}.html").exists():
            href = f"../{course}/{web_name(name)}.html"
        text = alias or (name if course in (None, self.course) else f"{course} {name}")
        if href is None:
            why = "not published" if course == self.course else "not on the site"
            self.log.append(f"link kept as text ({why}): [[{target}]]")
            return text
        return f"[{text}]({href}{'#' + heading_id(anchor) if anchor else ''})"

    def wikilinks(self, lines):
        text = "\n".join(lines)
        page_ids = {heading_id(m[2]) for m in map(HEADING_RE.match, lines) if m}

        def sub(m):
            embed, target, anchor, alias = m.groups()
            alias = alias.strip() if alias else None
            if embed:
                return self.embed(target, alias)
            return self.link(target, anchor, alias, page_ids)

        pieces = PROTECT_RE.split(text)  # odd indices are math / code: leave untouched
        return "".join(p if k % 2 else WIKILINK_RE.sub(sub, p) for k, p in enumerate(pieces))

    def markdown(self):
        _, text = split_frontmatter(self.note.read_text(encoding="utf-8"))
        return self.wikilinks(self.callouts(self.hide_unpublished(self.strip_private(text))))


def check_html(html_file):
    """Relative links resolve, in-page anchors exist, no Obsidian syntax left over."""
    problems, s = [], html_file.read_text(encoding="utf-8")
    ids = set(re.findall(r'\bid="([^"]+)"', s))
    for href in re.findall(r'href="([^"]+)"', s):
        if href.startswith(("http://", "https://", "mailto:", "/")):
            continue
        if href.startswith("#"):
            if href[1:] not in ids:
                problems.append(f"missing anchor {href}")
        elif not (html_file.parent / href.split("#")[0]).exists():
            problems.append(f"broken link {href}")
    body = s.split("<main>", 1)[-1]
    for token in ("[[", "[!", "%%"):
        if token in body:
            problems.append(f"leftover {token!r}")
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("course", help="folder name under WebsiteNotes/, e.g. ecoevo2026")
    ap.add_argument("--vault", type=Path, default=VAULT)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--push", action="store_true", help="git commit + push after building")
    args = ap.parse_args()

    src = args.vault / NOTES_DIR / args.course
    out = SITE / SITE_DIR / args.course
    notes = sorted(src.glob("*.md"))
    if not notes:
        sys.exit(f"no notes in {src}")
    if shutil.which("pandoc") is None:
        sys.exit("pandoc not found (brew install pandoc)")
    published = [n for n in notes if is_published(n)]
    for note in notes:
        if note not in published:
            print(f"{note.name}: not published (publish is not true)")
    if not published:
        sys.exit("no note has publish: true")
    stems = {n.stem for n in published}

    index = src / "index.md"
    course_title = args.course
    if index.exists():
        _, body = split_frontmatter(index.read_text(encoding="utf-8"))
        h1 = next((l[2:] for l in body.splitlines() if l.startswith("# ")), None)
        course_title = plain(h1) if h1 else course_title

    built = []
    for note in published:
        page = Page(args.course, src, out, note, stems)
        md = page.markdown()
        h1 = next((l[2:] for l in md.splitlines() if l.startswith("# ")), note.stem)
        target = out / f"{web_name(note.stem)}.html"
        title = course_title if note.stem == "index" else f"{plain(h1)} · {course_title}"
        print(f"{note.name} -> {target.relative_to(SITE)}")
        for entry in page.log:
            print(f"    {entry}")
        if args.dry_run:
            continue
        out.mkdir(parents=True, exist_ok=True)
        for s, d in page.copies:
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(s, d)
            print(f"    copied {s.name} -> {d.relative_to(SITE)}")
        subprocess.run(["pandoc", "-f", PANDOC_FROM, "-t", "html5", f"--mathjax={MATHJAX}",
                        "--standalone", "--template", str(TEMPLATE),
                        "-M", f"pagetitle={title}", "-M", f"course-title={course_title}",
                        "-o", str(target)], input=md, text=True, check=True)
        built.append(target)

    # pages of notes that are no longer published: delete the ones this script made
    expected = {f"{web_name(n.stem)}.html" for n in published}
    for f in sorted(out.glob("*.html")) if out.exists() else []:
        if f.name in expected:
            continue
        if GENERATOR_TAG not in f.read_text(encoding="utf-8"):
            print(f"left in place, not made by this script: {f.relative_to(SITE)}")
        elif args.dry_run:
            print(f"would delete {f.relative_to(SITE)} (note not published)")
        else:
            f.unlink()
            print(f"deleted {f.relative_to(SITE)} (note not published)")

    ok = True
    for target in built:  # after the whole build, so links between new pages resolve
        for p in check_html(target):
            ok = False
            print(f"PROBLEM in {target.name}: {p}")
    if not ok:
        sys.exit("problems found: fix before publishing")
    if args.push and not args.dry_run:
        rel = str(out.relative_to(SITE))
        subprocess.run(["git", "-C", str(SITE), "add", "-A", rel], check=True)
        if subprocess.run(["git", "-C", str(SITE), "diff", "--cached", "--quiet"]).returncode == 0:
            print("nothing to commit")
            return
        subprocess.run(["git", "-C", str(SITE), "commit", "-m", f"Publish {args.course} notes"], check=True)
        subprocess.run(["git", "-C", str(SITE), "push"], check=True)


if __name__ == "__main__":
    main()
