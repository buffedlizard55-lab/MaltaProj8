#!/usr/bin/env python3
"""
Verification pass for the whole published site (all sessions).

Checks, in order:
  1. Every data file parses as JSON.
  2. Every table row in the extended-analysis data names a source id that
     exists in data/sources.json.
  3. Verified rows have a value; unverified rows have no value and carry a flag.
  4. Every source URL in data/sources.json is https and on an official
     government / state-marketplace domain.
  5. Every internal link in every published page (root and research/) resolves
     to a file that exists.
  6. Every internal anchor link resolves to an id that exists in the target page.
  7. Every published page carries a navigation and a title.
  8. Every source id in data/sources.json is actually cited on a page.

Exit code is non-zero if any check fails. Non-official external links are
reported as warnings (they are editorial choices made by the sessions that
wrote those pages) and never block publication.

Usage:  python3 scripts/check_links.py
"""

import json
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

# Official domains only. Nothing else may be used to state a value.
ALLOWED_DOMAINS = {
    "dhcs.ca.gov", "www.dhcs.ca.gov", "ca.gov", "www.ca.gov",
    "coveredca.com", "www.coveredca.com", "hbex.coveredca.com",
    "board.coveredca.com", "apply.coveredca.com",
    "healthcare.gov", "www.healthcare.gov",
    "cms.gov", "www.cms.gov", "medicaid.gov", "www.medicaid.gov",
    "congress.gov", "www.congress.gov",
    "federalregister.gov", "www.federalregister.gov", "govinfo.gov", "www.govinfo.gov",
    "irs.gov", "www.irs.gov", "dol.gov", "www.dol.gov",
    "cftc.gov", "www.cftc.gov", "aspe.hhs.gov", "hhs.gov", "www.hhs.gov",
    "ecfr.gov", "www.ecfr.gov", "ssa.gov", "www.ssa.gov",
    "leginfo.legislature.ca.gov", "benefitscal.com", "www.benefitscal.com",
    "chhs.ca.gov", "www.chhs.ca.gov",
    "hrsa.gov", "www.hrsa.gov", "bphc.hrsa.gov",
}

# Links to these hosts are navigation, not evidence (repo, issues). They are
# allowed in published pages but can never be used as a source in the data files.
BENIGN_LINK_DOMAINS = {"github.com", "www.github.com"}

# Pages published by other sessions: their data files use full URLs rather
# than source ids, so they are checked with the generic URL walk below.
URL_KEYS = {"source", "sources", "url", "link", "citation", "source_url", "href"}

failures = []
warnings = []
info = []


def fail(msg):
    failures.append(msg)


def warn(msg):
    warnings.append(msg)


def note(msg):
    info.append(msg)


def load(name):
    with open(os.path.join(DATA, name), "r", encoding="utf-8") as fh:
        return json.load(fh)


class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.has_nav = False
        self.has_title = False
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and "href" in a:
            self.links.append(a["href"])
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "nav":
            self.has_nav = True
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title and data.strip():
            self.has_title = True


def walk_urls(node, path=""):
    """Yield (json-path, url) for every URL-looking string in a JSON tree."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key in URL_KEYS and isinstance(value, str) and value.startswith("http"):
                yield "{}.{}".format(path, key), value
            else:
                for item in walk_urls(value, "{}.{}".format(path, key)):
                    yield item
    elif isinstance(node, list):
        for idx, value in enumerate(node):
            for item in walk_urls(value, "{}[{}]".format(path, idx)):
                yield item
    elif isinstance(node, str):
        for match in re.finditer(r"https?://[^\s\"'<>]+", node):
            yield path, match.group(0)


def main():
    # ---- 1. JSON parses -------------------------------------------------
    data_files = sorted(f for f in os.listdir(DATA) if f.endswith(".json"))
    parsed = {}
    for fname in data_files:
        try:
            parsed[fname] = load(fname)
        except Exception as exc:  # noqa: BLE001
            fail("{}: invalid JSON ({})".format(fname, exc))
    if not parsed:
        fail("no data files found")
        return

    sources = {s["id"]: s for s in parsed["sources.json"]["sources"]}

    # ---- 2/3. row-level checks -----------------------------------------
    row_total = 0
    unverified_total = 0
    for fname, payload in parsed.items():
        if not fname.startswith("entries-"):
            continue
        for table, rows in payload.get("tables", {}).items():
            for row in rows:
                row_total += 1
                sid = row.get("source", "")
                if sid not in sources:
                    fail("{} / {}: row '{}' cites unknown source id '{}'".format(
                        fname, table, row.get("item", "?")[:60], sid))
                for extra in row.get("also", []):
                    if extra not in sources:
                        fail("{} / {}: row '{}' cites unknown additional source id '{}'".format(
                            fname, table, row.get("item", "?")[:60], extra))
                verified = row.get("verified", True)
                value = (row.get("value") or "").strip()
                flag = (row.get("flag") or "").strip()
                if verified:
                    if not value:
                        fail("{} / {}: verified row '{}' has an empty value".format(
                            fname, table, row.get("item", "?")[:60]))
                    if flag:
                        fail("{} / {}: verified row '{}' also carries a flag".format(
                            fname, table, row.get("item", "?")[:60]))
                else:
                    unverified_total += 1
                    if value:
                        fail("{} / {}: unverified row '{}' must have a blank value".format(
                            fname, table, row.get("item", "?")[:60]))
                    if not flag:
                        fail("{} / {}: unverified row '{}' has no flag text".format(
                            fname, table, row.get("item", "?")[:60]))

    # flagged.json rows must have an id, category and sources
    for item in parsed.get("flagged.json", {}).get("items", []):
        for field in ("id", "title", "category", "issue", "known", "why", "action"):
            if not str(item.get(field, "")).strip():
                fail("flagged.json: item {} is missing '{}'".format(item.get("id", "?"), field))
        for sid in item.get("sources", []):
            if sid not in sources:
                fail("flagged.json: item {} cites unknown source id '{}'".format(item.get("id"), sid))

    # ---- 2b. every published table is wired to its data ------------------
    for fname, payload in parsed.items():
        if not fname.startswith("page-"):
            continue
        slug = fname[len("page-"):-len(".json")]
        if slug in ("flagged", "sources"):
            continue
        entries_name = "entries-{}.json".format(slug)
        if entries_name not in parsed:
            fail("{}: no entries file '{}' — the page would render empty tables".format(
                fname, entries_name))
            continue
        tables = parsed[entries_name].get("tables", {})
        for section in payload.get("sections", []):
            tid = section.get("table")
            if not tid:
                continue
            if tid not in tables:
                fail("{}: section '{}' points at table '{}' which is not in {}".format(
                    fname, section.get("id"), tid, entries_name))
            elif not tables[tid]:
                fail("{}: table '{}' has no rows — the page would render an empty table".format(
                    fname, tid))

    for fname in parsed:
        if fname.startswith("entries-"):
            slug = fname[len("entries-"):-len(".json")]
            if "page-{}.json".format(slug) not in parsed:
                fail("{}: no matching page definition — this data would never be published".format(fname))

    # ---- 4. source URLs on official domains -----------------------------
    for sid, src in sources.items():
        parsed_url = urlparse(src["url"])
        if parsed_url.scheme != "https":
            fail("source {}: URL is not https".format(sid))
        host = (parsed_url.netloc or "").lower()
        if host not in ALLOWED_DOMAINS and not host.endswith(".gov"):
            fail("source {}: '{}' is not an allowed official domain".format(sid, host))
        if not src.get("date") or not src.get("publisher"):
            fail("source {}: missing publisher or date".format(sid))

    # ---- 5/6/7. published HTML -----------------------------------------
    page_files = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules", "__pycache__", "dist", "_site", ".cache")]
        for fname in sorted(filenames):
            if fname.endswith(".html"):
                rel = os.path.relpath(os.path.join(dirpath, fname), ROOT)
                page_files.append(rel)

    pages = {}
    for rel in page_files:
        parser = LinkCollector()
        with open(os.path.join(ROOT, rel), "r", encoding="utf-8") as fh:
            parser.feed(fh.read())
        pages[rel.replace(os.sep, "/")] = parser
        if not parser.has_nav:
            fail("{}: missing navigation".format(rel))
        if not parser.has_title:
            fail("{}: missing <title>".format(rel))

    non_official = {}
    for rel, parser in pages.items():
        base = os.path.dirname(os.path.join(ROOT, rel))
        for href in parser.links:
            if href.startswith(("mailto:", "tel:", "javascript:")):
                continue
            if href.startswith(("http://", "https://")):
                url = href
                host = (urlparse(url).netloc or "").lower()
                if host not in ALLOWED_DOMAINS and not host.endswith(".gov") and host not in BENIGN_LINK_DOMAINS:
                    non_official.setdefault(rel, set()).add(host)
                continue
            if href.startswith("#"):
                if href[1:] and href[1:] not in parser.ids:
                    fail("{}: anchor {} has no matching id".format(rel, href))
                continue
            target, _, anchor = href.partition("#")
            target_path = os.path.normpath(os.path.join(base, target))
            if not os.path.isfile(target_path):
                fail("{}: link to '{}' points at a missing file".format(rel, href))
                continue
            rel_target = os.path.relpath(target_path, ROOT).replace(os.sep, "/")
            if anchor and rel_target in pages:
                if anchor not in pages[rel_target].ids:
                    fail("{}: link '{}' points at a missing anchor".format(rel, href))

    # ---- 7b. rendered pages contain every row they promise ---------------
    for fname, payload in parsed.items():
        if not fname.startswith("page-"):
            continue
        slug = fname[len("page-"):-len(".json")]
        html_name = "{}.html".format(slug)
        html_path = os.path.join(ROOT, html_name)
        if not os.path.isfile(html_path):
            fail("{}: page '{}' was never built".format(fname, html_name))
            continue
        if slug == "flagged":
            expected = len(parsed.get("flagged.json", {}).get("items", []))
        elif slug == "sources":
            expected = len(sources)
        else:
            entries = parsed.get("entries-{}.json".format(slug), {})
            expected = 0
            for section in payload.get("sections", []):
                tid = section.get("table")
                if tid:
                    expected += len(entries.get("tables", {}).get(tid, []))
        with open(html_path, "r", encoding="utf-8") as fh:
            rendered = fh.read().count('<tr class="row')
        if rendered < expected:
            fail("{}: renders {} data rows but {} are defined in the data files".format(
                html_name, rendered, expected))

    # ---- 8. every source id is cited ------------------------------------
    cited = set()
    for fname, payload in parsed.items():
        if fname.startswith("entries-"):
            for rows in payload.get("tables", {}).values():
                for row in rows:
                    cited.add(row.get("source", ""))
                    cited.update(row.get("also", []))
    for item in parsed.get("flagged.json", {}).get("items", []):
        cited.update(item.get("sources", []))
    for sid in sources:
        if sid not in cited:
            warn("source {} is listed but not cited on any page".format(sid))

    # ---- informational: URLs in the other sessions' data files -----------
    other_files = [f for f in data_files if not f.startswith(("entries-", "page-"))
                   and f not in ("sources.json", "flagged.json")]
    other_urls = 0
    for fname in other_files:
        for path, url in walk_urls(parsed[fname]):
            other_urls += 1
            if url.startswith("http://"):
                warn("{}: URL is not https ({})".format(fname, path))
    if other_urls:
        note("{} URLs found in the other sessions' data files (checked for https)".format(other_urls))

    if non_official:
        for rel in sorted(non_official):
            warn("{}: links to {} non-official domain(s): {}".format(
                rel, len(non_official[rel]), ", ".join(sorted(non_official[rel]))))

    print("Pages checked      : {}".format(len(pages)))
    print("Table rows checked : {} ({} flagged/unverified)".format(row_total, unverified_total))
    print("Sources checked    : {}".format(len(sources)))
    for i in info:
        print("INFO  " + i)
    for w in warnings:
        print("WARN  " + w)
    if failures:
        print("\nFAILED ({} problems):".format(len(failures)))
        for f in failures:
            print("  - " + f)
        sys.exit(1)
    print("\nAll checks passed.")


if __name__ == "__main__":
    main()
