#!/usr/bin/env python3
"""
Verification pass for the published site.

Checks, in order:
  1. Every data file parses as JSON.
  2. Every table row names a source id that exists in data/sources.json.
  3. Verified rows have a value; unverified rows have no value and carry a flag.
  4. Every source URL is https and on an official government / state-marketplace domain.
  5. Every internal link in the generated HTML resolves to a file that exists.
  6. Every internal anchor link resolves to an id that exists in the target page.
  7. Every generated page carries the navigation and a title.

Exit code is non-zero if any check fails.

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
}

failures = []
warnings = []


def fail(msg):
    failures.append(msg)


def warn(msg):
    warnings.append(msg)


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
        if tag == "nav" and a.get("id") == "site-nav":
            self.has_nav = True
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title and data.strip():
            self.has_title = True


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

    # ---- 4. source URLs on official domains -----------------------------
    for sid, src in sources.items():
        parsed_url = urlparse(src["url"])
        if parsed_url.scheme != "https":
            fail("source {}: URL is not https".format(sid))
        host = (parsed_url.netloc or "").lower()
        if host not in ALLOWED_DOMAINS:
            fail("source {}: '{}' is not an allowed official domain".format(sid, host))
        if not src.get("date") or not src.get("publisher"):
            fail("source {}: missing publisher or date".format(sid))

    # ---- 5/6/7. generated HTML ------------------------------------------
    pages = {}
    for fname in sorted(os.listdir(ROOT)):
        if not fname.endswith(".html"):
            continue
        parser = LinkCollector()
        with open(os.path.join(ROOT, fname), "r", encoding="utf-8") as fh:
            parser.feed(fh.read())
        pages[fname] = parser
        if not parser.has_nav:
            fail("{}: missing site navigation".format(fname))
        if not parser.has_title:
            fail("{}: missing <title>".format(fname))

    for fname, parser in pages.items():
        for href in parser.links:
            if href.startswith(("http://", "https://", "mailto:", "tel:")):
                continue
            if href.startswith("#"):
                if href[1:] and href[1:] not in parser.ids:
                    fail("{}: anchor {} has no matching id".format(fname, href))
                continue
            target, _, anchor = href.partition("#")
            target_path = os.path.join(ROOT, target)
            if not os.path.isfile(target_path):
                fail("{}: link to '{}' points at a missing file".format(fname, href))
                continue
            if anchor and target in pages:
                if anchor not in pages[target].ids:
                    fail("{}: link '{}' points at a missing anchor".format(fname, href))

    # every source in sources.json must actually be cited somewhere
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

    print("Pages checked      : {}".format(len(pages)))
    print("Table rows checked : {} ({} flagged/unverified)".format(row_total, unverified_total))
    print("Sources checked    : {}".format(len(sources)))
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
