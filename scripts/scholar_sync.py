#!/usr/bin/env python3
"""
scholar_sync.py — keep _data/publist.yml in sync with Jacopo's publication record.

Data source: by DEFAULT this queries **OpenAlex** (https://openalex.org), a free
open scholarly index, keyed by Jacopo's ORCID (read from team_members.yml). Unlike
Google Scholar — which has no API and CAPTCHA/429-blocks scraping (both the
`scholarly` library and direct page requests get blocked) — OpenAlex has a proper
JSON API that does not block and returns venue, year, authors, DOI and preprint
IDs cleanly. The Google Scholar code paths are kept as opt-in fallbacks
(--scholar-direct, --scholarly) but are unreliable.

Behaviour (per agreed policy):
  * Match each Scholar publication to an existing publist.yml entry by fuzzy
    title comparison (normalised, ratio >= THRESHOLD).
  * MATCHED & the local entry is a preprint (preprint: 1) but Scholar now shows a
    real journal venue  ->  PROMOTE: fill journal / reference / year / authors /
    doi from Scholar and set preprint: 0. The existing arxiv/biorxiv code,
    highlight and description are preserved.
  * MATCHED & already published / no new info  ->  left untouched.
  * UNMATCHED (new paper)  ->  APPEND a new entry. preprint is inferred from the
    venue (real journal -> 0, otherwise 1). For a preprint the arxiv/biorxiv code
    is extracted from the Scholar eprint/pub URL when available.
  * A non-empty manual field is never overwritten.

YAML structure, ordering and comments are preserved via ruamel.yaml.

Usage:
    python3 scripts/scholar_sync.py --dry-run   # report only, no writes
    python3 scripts/scholar_sync.py             # apply changes

Usage:
    python3 scripts/scholar_sync.py --dry-run        # OpenAlex, report only
    python3 scripts/scholar_sync.py                  # OpenAlex, apply
    python3 scripts/scholar_sync.py --scholar-direct # Google Scholar HTML (blocks)
    python3 scripts/scholar_sync.py --scholarly      # scholarly lib (needs proxy)

Dependencies: ruamel.yaml (always); scholarly only for --scholarly.
"""

import argparse
import html
import json
import os
import re
import sys
import time
import urllib.request
from datetime import date, timedelta
from difflib import SequenceMatcher

from ruamel.yaml import YAML

HERE = os.path.dirname(os.path.abspath(__file__))
PUBLIST = os.path.normpath(os.path.join(HERE, "..", "_data", "publist.yml"))
TEAM = os.path.normpath(os.path.join(HERE, "..", "_data", "team_members.yml"))
MAILTO = "grilli.jacopo@gmail.com"   # OpenAlex "polite pool" contact

THRESHOLD = 0.90  # fuzzy title-match cutoff
PREPRINT_HINTS = ("arxiv", "biorxiv", "medrxiv", "preprint", "ssrn", "researchsquare")

# canonical key order for newly appended entries (mirrors publist.yml)
KEY_ORDER = ["title", "authors", "journal", "journalshort", "reference", "year",
             "doi", "arxiv", "biorxiv", "news", "description", "image",
             "mendeley", "researchgate", "pmid", "preprint", "highlight"]


# ---------------------------------------------------------------- helpers
def norm(t):
    return re.sub(r"[^a-z0-9]+", " ", str(t or "").lower()).strip()


def is_journal(venue):
    """True if the venue looks like a real journal (not a preprint server)."""
    v = str(venue or "").lower()
    return bool(v.strip()) and not any(h in v for h in PREPRINT_HINTS)


def empty(v):
    return v is None or str(v).strip() == ""


def get_author_ids():
    """Read Jacopo's ORCID and Scholar id from team_members.yml."""
    yaml = YAML()
    for m in yaml.load(open(TEAM)):
        if str(m.get("name", "")).startswith("Jacopo"):
            return {
                "orcid": str(m.get("orcidusername", "")).strip().strip('"'),
                "scholar": str(m.get("scholarusername", "")).strip().strip('"'),
            }
    raise SystemExit("Could not find Jacopo in team_members.yml")


def initials(name):
    """'Jacopo Grilli' -> 'J. Grilli' to match publist.yml author style."""
    parts = str(name or "").split()
    if len(parts) < 2:
        return name
    *firsts, last = parts
    return " ".join("%s." % p[0] for p in firsts if p) + " " + last


def extract_preprint_code(*urls):
    """Return ('biorxiv'|'arxiv', code) from a Scholar eprint/pub URL, or (None, None)."""
    for u in urls:
        u = str(u or "")
        m = re.search(r"(?:biorxiv|medrxiv)\.org/.*?(10\.\d{4,}/[^\s?&]+)", u, re.I)
        if m:
            # drop trailing version / file suffix, e.g. ".../2023.03.02.530804v1.full"
            return "biorxiv", re.sub(r"v\d+.*$", "", m.group(1))
        m = re.search(r"arxiv\.org/abs/([0-9]+\.[0-9]+)", u, re.I)
        if m:
            return "arxiv", m.group(1)
    return None, None


UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def _get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


# OpenAlex returns non-article "works" we never want in the publication list
OA_SKIP_TYPES = {"peer-review", "paratext", "erratum", "grant", "dataset",
                 "reference-entry", "supplementary-materials", "editorial", "letter"}
OA_JUNK_TITLE = re.compile(
    r"^\s*(author response|author correction|publisher correction|correction:|"
    r"erratum|reviewer\s*#|reviewer\s*&|decision letter|moesm|data and code for|"
    r"supplementary|reply to|response to|editorial|table s\d|figure s\d)", re.I)


def clean_title(t):
    """Strip HTML/MathML markup and collapse whitespace in an OpenAlex title."""
    t = re.sub(r"<mml:[^>]*>|</mml:[^>]*>", "", str(t or ""))
    t = re.sub(r"<[^>]+>", "", t)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def oa_is_junk(work, title):
    return work.get("type") in OA_SKIP_TYPES or bool(OA_JUNK_TITLE.match(title))


def fetch_openalex(orcid, years=0):
    """Pull Jacopo's works from OpenAlex (no key, no blocking), keyed by ORCID.

    years > 0 restricts to works published in the last `years` years (server-side),
    which sharply cuts the namesake/ORCID-leak and old-paper noise.
    """
    if not orcid:
        raise SystemExit("No ORCID in team_members.yml; cannot query OpenAlex.")
    flt = "author.orcid:%s" % orcid
    if years > 0:
        since = (date.today() - timedelta(days=365 * years)).isoformat()
        flt += ",from_publication_date:%s" % since
        print("Restricting to works since %s" % since, file=sys.stderr)
    pubs, cursor = [], "*"
    while cursor:
        url = ("https://api.openalex.org/works?filter=%s"
               "&per-page=200&cursor=%s&mailto=%s" % (flt, cursor, MAILTO))
        print("GET %s" % url, file=sys.stderr)
        data = _get_json(url)
        for w in data.get("results", []):
            title = clean_title(w.get("title") or w.get("display_name") or "")
            if not title or oa_is_junk(w, title):
                continue
            doi = (w.get("doi") or "").replace("https://doi.org/", "")
            authors = ", ".join(
                initials((a.get("author") or {}).get("display_name", ""))
                for a in w.get("authorships", []))
            # A work is published if ANY of its locations is a real journal — older
            # papers often list their arXiv/bioRxiv copy as primary_location, which
            # would otherwise mis-flag them as preprints.
            venue = ""
            for loc in [w.get("primary_location")] + (w.get("locations") or []):
                name = (((loc or {}).get("source") or {}).get("display_name")) or ""
                if name and is_journal(name):
                    venue = name
                    break
            is_pre = venue == ""
            kind, code = None, None
            if is_pre:
                if "10.1101/" in doi:
                    kind, code = "biorxiv", doi
                else:
                    for loc in w.get("locations", []):
                        k, c = extract_preprint_code((loc.get("landing_page_url") or ""))
                        if k:
                            kind, code = k, c
                            break
                    if not kind and "arxiv" in venue.lower():
                        kind, code = "arxiv", doi.split("arxiv.")[-1] if "arxiv." in doi.lower() else ""
            pubs.append({
                "title": title,
                "authors": authors,
                "journal": "" if is_pre else venue,
                "reference": _ref_from_biblio(w.get("biblio") or {}),
                "year": w.get("publication_year") or "",
                "doi": "" if is_pre else doi,
                "is_preprint": is_pre,
                "preprint_kind": kind,
                "preprint_code": code,
                "eprint_url": "", "pub_url": "",
            })
        cursor = (data.get("meta") or {}).get("next_cursor")
        time.sleep(0.3)
    return pubs


def _ref_from_biblio(b):
    vol, iss, fp, lp = b.get("volume"), b.get("issue"), b.get("first_page"), b.get("last_page")
    out = vol or ""
    if iss:
        out += "(%s)" % iss
    if fp:
        pages = fp + (("-" + lp) if lp and lp != fp else "")
        out += (":" if out else "") + pages
    return out


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def split_venue(line):
    """Split a Scholar venue line 'Journal 9 (3), 100-110, 2025' -> (journal, reference)."""
    line = re.sub(r",?\s*((?:19|20)\d{2})\s*$", "", line).strip()  # drop trailing year
    m = re.match(r"^(.*?)\s+(\d.*)$", line)             # journal | numeric tail
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return line, ""


def fetch_direct(scholar_id):
    """One (or few) plain HTTP requests to the public profile listing page."""
    pubs = []
    for cstart in range(0, 300, 100):
        url = ("https://scholar.google.com/citations?hl=en&user=%s"
               "&cstart=%d&pagesize=100" % (scholar_id, cstart))
        print("GET %s" % url, file=sys.stderr)
        req = urllib.request.Request(url, headers={"User-Agent": UA,
                                                   "Accept-Language": "en-US,en"})
        with urllib.request.urlopen(req, timeout=30) as r:
            page = r.read().decode("utf-8", "replace")
        if "gs_captcha" in page or "not a robot" in page.lower() or "/sorry/" in page:
            raise SystemExit("Blocked by Google Scholar (CAPTCHA). Try again later "
                             "or from a different IP, or use --scholarly with a proxy.")
        rows = re.findall(r'<tr class="gsc_a_tr">(.*?)</tr>', page, re.S)
        if not rows:
            break
        for row in rows:
            tm = re.search(r'class="gsc_a_at"[^>]*>(.*?)</a>', row, re.S)
            grays = re.findall(r'class="gs_gray">(.*?)</div>', row, re.S)
            ym = re.search(r'class="gsc_a_y[^"]*">.*?(\d{4})', row, re.S)
            if not tm:
                continue
            authors = strip_tags(grays[0]) if grays else ""
            journal, reference = split_venue(strip_tags(grays[1])) if len(grays) > 1 else ("", "")
            pubs.append({
                "title": strip_tags(tm.group(1)),
                "authors": authors,
                "journal": journal,
                "reference": reference,
                "year": ym.group(1) if ym else "",
                "doi": "", "eprint_url": "", "pub_url": "",
            })
        if len(rows) < 100:
            break
        time.sleep(1)
    return pubs


def fetch_scholarly(scholar_id):
    from scholarly import scholarly
    author = scholarly.fill(scholarly.search_author_id(scholar_id),
                            sections=["publications"])
    pubs = []
    for p in author["publications"]:
        scholarly.fill(p)
        b = p.get("bib", {})
        ref = b.get("volume", "")
        if b.get("number"):
            ref += "(%s)" % b["number"]
        if b.get("pages"):
            ref += (":" if ref else "") + b["pages"]
        pubs.append({
            "title": b.get("title", ""),
            "authors": b.get("author", "").replace(" and ", ", "),
            "journal": b.get("journal") or b.get("venue") or b.get("publisher") or "",
            "reference": ref,
            "year": b.get("pub_year", ""),
            "doi": b.get("doi", ""),
            "eprint_url": p.get("eprint_url", ""),
            "pub_url": p.get("pub_url", ""),
        })
    return pubs


def fetch(ids, method, years=0):
    if method == "openalex":
        print("Fetching from OpenAlex (ORCID %s) ..." % ids["orcid"], file=sys.stderr)
        return fetch_openalex(ids["orcid"], years=years)
    print("Fetching Google Scholar profile %s ..." % ids["scholar"], file=sys.stderr)
    pubs = fetch_scholarly(ids["scholar"]) if method == "scholarly" else fetch_direct(ids["scholar"])
    if years > 0:  # Scholar paths have no server-side date filter; trim by year
        cutoff = date.today().year - years
        pubs = [p for p in pubs if str(p.get("year", "")).isdigit() and int(p["year"]) >= cutoff]
    return pubs


def reference_from(s):
    """Reference string: use the pre-parsed one, else build from bib volume/pages."""
    if s.get("reference"):
        return s["reference"]
    vol, num, pg = s.get("volume", ""), s.get("number", ""), s.get("pages", "")
    out = vol
    if num:
        out += "(%s)" % num
    if pg:
        out += (":" if out else "") + pg
    return out


# ---------------------------------------------------------------- core
def sync(dry_run, method="openalex", years=0):
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096
    with open(PUBLIST) as f:
        local = yaml.load(f)

    local_norm = [norm(e.get("title")) for e in local]
    ids = get_author_ids()
    scholar_pubs = fetch(ids, method, years=years)
    # process published versions before preprints so a paper present on the source
    # as both does not produce a duplicate entry
    scholar_pubs.sort(key=lambda s: bool(s.get("is_preprint")))

    promoted, appended, low_conf = [], [], []

    for s in scholar_pubs:
        st = norm(s["title"])
        if not st:
            continue
        # best fuzzy match against local titles
        best_i, best_r = -1, 0.0
        for i, lt in enumerate(local_norm):
            r = SequenceMatcher(None, st, lt).ratio()
            if r > best_r:
                best_i, best_r = i, r

        if best_r >= THRESHOLD:
            entry = local[best_i]
            # promote preprint -> published when Scholar shows a journal
            if entry.get("preprint") == 1 and is_journal(s["journal"]):
                if not empty(s["journal"]):
                    entry["journal"] = s["journal"]
                if not empty(s["year"]):
                    entry["year"] = int(s["year"]) if str(s["year"]).isdigit() else s["year"]
                ref = reference_from(s)
                if not empty(ref):
                    entry["reference"] = ref
                if not empty(s["authors"]):
                    entry["authors"] = s["authors"]
                if not empty(s["doi"]):
                    entry["doi"] = s["doi"]
                entry["preprint"] = 0
                promoted.append({"title": entry.get("title"), "journal": s.get("journal"),
                                 "year": s.get("year"), "doi": s.get("doi")})
            else:
                if 0.90 <= best_r < 0.96:
                    low_conf.append((s["title"], local[best_i].get("title"), round(best_r, 2)))
            continue

        # unmatched -> append new entry
        if "is_preprint" in s:                 # OpenAlex already classified it
            is_pre = 1 if s["is_preprint"] else 0
            kind, code = s.get("preprint_kind"), s.get("preprint_code")
        else:                                  # Scholar paths: infer from venue + URLs
            is_pre = 0 if is_journal(s["journal"]) else 1
            kind, code = extract_preprint_code(s.get("eprint_url"), s.get("pub_url"))
        new = {k: None for k in KEY_ORDER}
        new["title"] = s["title"]
        new["authors"] = s["authors"]
        new["journal"] = s["journal"] or None
        new["reference"] = reference_from(s) or None
        new["year"] = int(s["year"]) if str(s["year"]).isdigit() else (s["year"] or None)
        new["doi"] = s["doi"] or None
        new["preprint"] = is_pre
        new["highlight"] = 0
        if is_pre and kind:
            new[kind] = code
        local.append(new)
        local_norm.append(st)
        appended.append({"title": s["title"], "preprint": is_pre,
                         "venue": s.get("journal") or "", "year": new["year"],
                         "code": "%s:%s" % (kind, code) if (is_pre and kind) else ""})

    # ----- report
    print("\n=== Scholar sync report ===")
    print("Scholar publications scanned : %d" % len(scholar_pubs))
    print("Promoted preprint -> published: %d" % len(promoted))
    for p in promoted:
        print("   + %s\n       -> journal: %s | year: %s | doi: %s"
              % (p["title"], p["journal"], p["year"], p["doi"]))
    print("Appended new entries          : %d" % len(appended))
    for a in appended:
        tag = "preprint" if a["preprint"] else "published"
        meta = "venue: %s | year: %s" % (a["venue"] or "-", a["year"])
        if a["code"]:
            meta += " | %s" % a["code"]
        print("   + [%s] %s\n       -> %s" % (tag, a["title"], meta))
    if low_conf:
        print("Low-confidence matches (review manually): %d" % len(low_conf))
        for a, b, r in low_conf:
            print("   ? %.2f  scholar:%s  ~  local:%s" % (r, a[:60], str(b)[:60]))

    if dry_run:
        print("\n[dry-run] no files written.")
        return
    if not promoted and not appended:
        print("\nNothing to write — publist.yml already in sync.")
        return
    with open(PUBLIST, "w") as f:
        yaml.dump(local, f)
    print("\nWrote %s" % PUBLIST)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true",
                    help="report changes without writing publist.yml")
    ap.add_argument("--scholar-direct", action="store_true",
                    help="fall back to scraping the Google Scholar HTML page (blocks)")
    ap.add_argument("--scholarly", action="store_true",
                    help="fall back to the scholarly library (needs a proxy)")
    ap.add_argument("--years", type=int, default=2, metavar="N",
                    help="only consider works published in the last N years "
                         "(default 2; pass 0 for all — adds namesake/old-paper noise)")
    args = ap.parse_args()
    method = "scholarly" if args.scholarly else "scholar-direct" if args.scholar_direct else "openalex"
    sync(args.dry_run, method=method, years=args.years)
