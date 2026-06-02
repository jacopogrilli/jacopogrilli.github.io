#!/usr/bin/env python3
"""
generate_cv.py — regenerate the data-backed LaTeX partials of the CV from the
website's canonical data in ../../_data/.

Outputs (written to ../tex/ so the backbone jgrilli_cv.tex can \input them):
  published.tex   <- publist.yml  (preprint == 0)   -> \begin{bibenum} items
  preprint.tex    <- publist.yml  (preprint == 1)   -> \begin{bibenum} items
  seminars.tex    <- talks.yml    (type ~ "seminar") -> \begin{outerlist} items
  meetings.tex    <- talks.yml    (other talks)      -> \begin{outerlist} items
  organized.tex   <- talks.yml    (what == 1 / organisational types)

The backbone keeps the \section{...} headings and the \begin/\end{bibenum|outerlist}
wrappers; these files contain only the \item lines.

Run:  python3 generate_cv.py      (from cv/script/, or anywhere — paths are resolved
                                    relative to this file)

Note: talks.yml has no "leading organizer" flag, so the $\star$ markers that used to
decorate the hand-written "Organized" section are not reproduced.
"""

import os
import re
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "..", "_data"))
OUT = os.path.normpath(os.path.join(HERE, "..", "tex"))


# ---------------------------------------------------------------- helpers
def esc(x):
    """Escape LaTeX special characters in plain text fields."""
    if x is None:
        return ""
    s = str(x)
    for a, b in (("&", r"\&"), ("%", r"\%"), ("#", r"\#"), ("_", r"\_")):
        s = s.replace(a, b)
    return s


def authors_tex(a):
    """Escape author list and underline Jacopo via the \\JG macro."""
    return esc(a).replace("J. Grilli", r"\JG")


def nonempty(x):
    return x is not None and str(x).strip() != "" and str(x).strip().lower() != "none"


MONTHS = {m: i for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july",
     "august", "september", "october", "november", "december"], start=1)}


def date_key(date_str):
    """Best-effort (year, month, day) sort key from a free-text date field."""
    s = str(date_str or "")
    years = re.findall(r"(?:19|20)\d{2}", s)
    year = int(years[-1]) if years else 0
    month = 0
    for name, num in MONTHS.items():
        if name in s.lower():
            month = num
            break
    dm = re.search(r"\b(\d{1,2})\b", s)
    day = int(dm.group(1)) if dm else 0
    return (year, month, day)


# ---------------------------------------------------------------- publications
def gen_publications():
    pubs = yaml.safe_load(open(os.path.join(DATA, "publist.yml")))
    published, preprints = [], []

    for p in pubs:
        authors = authors_tex(p.get("authors"))
        title = esc(p.get("title"))

        # "\emph{journal}. reference. year." with empties omitted
        bits = []
        if nonempty(p.get("journal")):
            bits.append(r"\emph{%s}." % esc(p.get("journal")))
        if nonempty(p.get("reference")):
            bits.append("%s." % esc(p.get("reference")))
        if nonempty(p.get("year")):
            bits.append("%s." % esc(p.get("year")))
        jref = " ".join(bits)

        # preprint link macro
        link = ""
        if nonempty(p.get("biorxiv")):
            link = r"\bioarxiv{%s}" % str(p["biorxiv"]).strip()
        elif nonempty(p.get("arxiv")):
            link = r"\arxiv{%s}" % str(p["arxiv"]).strip()

        if p.get("preprint") == 0:
            refs = []
            if nonempty(p.get("doi")):
                refs.append(r"\doi{%s} \ " % str(p["doi"]).strip())
            if nonempty(p.get("pmid")):
                refs.append(r"\pmid{%s} \ " % str(p["pmid"]).strip())
            if link:
                refs.append(link)
            tail = ("\n " + "\n".join(refs)) if refs else ""
            published.append(
                "\\item %s.\n%s\n%s\n \\\\ %s\n" % (authors, title, jref, tail))
        else:
            tail = ("\n " + link) if link else ""
            preprints.append(
                "\\item %s.\n%s\n%s\n\\ \\\\ %s\n" % (authors, title, jref, tail))

    write("published.tex", "\n".join(published))
    write("preprint.tex", "\n".join(preprints))
    return len(published), len(preprints)


# ---------------------------------------------------------------- talks
ORG_TYPES = {"workshop", "school", "working group", "satellite meeting",
             "program", "conference", "winter school on quantitative systems biology"}


def label(t):
    """Canonical, title-cased talk-type label."""
    s = str(t or "").strip()
    return s.title() if s == s.lower() else s


def route(t):
    what = t.get("what")
    typ = str(t.get("type") or "").strip().lower()
    if what == 1 or typ in ORG_TYPES:
        return "organized"
    if "seminar" in typ:
        return "seminars"
    return "meetings"


def gen_talks():
    talks = [t for t in yaml.safe_load(open(os.path.join(DATA, "talks.yml")))
             if isinstance(t, dict)]
    buckets = {"organized": [], "seminars": [], "meetings": []}

    for t in sorted(talks, key=lambda x: date_key(x.get("date")), reverse=True):
        sec = route(t)
        date = esc(t.get("date"))
        place = esc(t.get("place")) if nonempty(t.get("place")) else ""
        title = esc(t.get("title"))
        url = str(t.get("url")).strip() if nonempty(t.get("url")) else ""

        if sec == "organized":
            head = ("%s %s" % (place, label(t.get("type")))).strip()
            linked = (r"\href{%s}{%s}" % (url, title)) if url else title
            buckets[sec].append(
                "\\item %s \\\\\n\\emph{%s}, %s.\n" % (date, head, linked))
        else:
            where = ("%s. " % place) if place else ""
            buckets[sec].append(
                "\\item %s. %s\\\\\n%s: \\emph{%s}\n" %
                (date, where, label(t.get("type")), title))

    write("organized.tex", "\n".join(buckets["organized"]))
    write("seminars.tex", "\n".join(buckets["seminars"]))
    write("meetings.tex", "\n".join(buckets["meetings"]))
    return {k: len(v) for k, v in buckets.items()}


# ---------------------------------------------------------------- io
def write(name, body):
    os.makedirs(OUT, exist_ok=True)
    header = "%% AUTO-GENERATED by cv/script/generate_cv.py — do not edit by hand.\n\n"
    with open(os.path.join(OUT, name), "w") as f:
        f.write(header + body + "\n")


if __name__ == "__main__":
    npub, npre = gen_publications()
    talk_counts = gen_talks()
    print("Wrote partials to %s" % OUT)
    print("  published.tex : %d" % npub)
    print("  preprint.tex  : %d" % npre)
    for k, v in talk_counts.items():
        print("  %-13s : %d" % (k + ".tex", v))
