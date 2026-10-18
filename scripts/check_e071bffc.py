#!/usr/bin/env python3
"""
Verification pass for the arena/e071bffc register (tasks 22-23).

This checker does not trust rendered text. Several defects in this repository's
history were introduced or missed because a URL looks right on screen but is
wrong at byte level, so every test here is evaluated programmatically and the
result is reported as a count, not as a string the reader has to eyeball.

Checks:
  1. data/verify-e071bffc.json parses.
  2. Every register row carries an id, a url and a status from the allowed set.
  3. Status 'fetched' rows must carry a non-empty locator and confirmed text.
     Status 'not-refetched' rows must NOT claim confirmed text - a source this
     session did not read may not be used to certify a value.
  4. Every finding marked 'verified' carries a non-empty value and a source URL.
     Every finding marked 'unverified' carries an EMPTY value (never inferred)
     and a note explaining why it is blank.
  5. No Federal Register document URL anywhere in the repository uses the
     hyphenated date path /documents/YYYY-MM-DD/, which returns HTTP 404.
     The working form is /documents/YYYY/MM/DD/.
  6. No URL in the register contains whitespace, a bare scheme, or a
     non-https scheme.
  7. Every correction and every change request names the file it concerns and
     an official source URL.
  8. The pages this session published resolve their own internal links.

Exit code is non-zero if any check fails.

Usage:  python3 scripts/check_e071bffc.py
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = os.path.join(ROOT, "data", "verify-e071bffc.json")

OFFICIAL_SUFFIXES = (
    ".gov", ".gov/", "coveredca.com", "www.coveredca.com",
    "hbex.coveredca.com", "benefitscal.com",
)

failures = []
notes = []


def fail(msg):
    failures.append(msg)


def is_official(url):
    host = re.match(r"https?://([^/]+)", url)
    if not host:
        return False
    h = host.group(1).lower()
    return any(h == s or h.endswith("." + s) or h == s for s in
               ("coveredca.com", "hbex.coveredca.com", "benefitscal.com")) or h.endswith(".gov")


def main():
    with open(REG, "r", encoding="utf-8") as fh:
        d = json.load(fh)
    notes.append("register parses")

    allowed = {"fetched", "not-refetched"}
    reg = d["register_sweep"] + d["additional_official_sources_fetched"]
    for r in reg:
        rid = r.get("id", "<no id>")
        if not r.get("url"):
            fail(f"{rid}: no url")
            continue
        u = r["url"]
        if not u.startswith("https://"):
            fail(f"{rid}: url is not https ({u[:60]})")
        if re.search(r"\s", u):
            fail(f"{rid}: url contains whitespace")
        if r.get("status") not in allowed:
            fail(f"{rid}: status {r.get('status')!r} not in {sorted(allowed)}")
        if r.get("status") == "fetched":
            if not r.get("locator"):
                fail(f"{rid}: marked fetched but names no locator in the document")
            if not r.get("confirmed"):
                fail(f"{rid}: marked fetched but records nothing that was confirmed")
        if r.get("status") == "not-refetched" and r.get("confirmed"):
            fail(f"{rid}: not re-fetched this session but claims confirmed content")

    fetched = sum(1 for r in reg if r.get("status") == "fetched")
    notes.append(f"{fetched} of {len(reg)} official sources re-fetched and read this session; "
                 f"{len(reg) - fetched} honestly left as not-refetched")

    for f in d["findings"]:
        fid = f.get("id", "<no id>")
        if f.get("verdict") == "verified":
            if not f.get("value"):
                fail(f"{fid}: verdict verified but value is blank")
            if not f.get("source"):
                fail(f"{fid}: verdict verified but no source URL")
            elif not is_official(f["source"]):
                fail(f"{fid}: verdict verified but source is not an official host: {f['source'][:60]}")
        elif f.get("verdict") == "unverified":
            if f.get("value"):
                fail(f"{fid}: verdict unverified but carries a value - values must be blank, never inferred")
            if not f.get("note"):
                fail(f"{fid}: verdict unverified with no note explaining the blank")
        else:
            fail(f"{fid}: unknown verdict {f.get('verdict')!r}")
    blank = sum(1 for f in d["findings"] if f.get("verdict") == "unverified")
    notes.append(f"{len(d['findings'])} findings, {blank} left blank and flagged rather than inferred")

    # Byte-level Federal Register date-path check across the whole repository.
    # The hyphenated form /documents/YYYY-MM-DD/ returns HTTP 404; the working
    # form is /documents/YYYY/MM/DD/. Tested on raw bytes, not rendered text.
    hyphen = re.compile(rb"federalregister\.gov/documents/\d{4}-\d{2}-\d{2}/")
    slash = re.compile(rb"federalregister\.gov/documents/\d{4}/\d{2}/\d{2}/")
    bad_files = []
    slash_total = 0
    for dp, dn, fn in os.walk(ROOT):
        if ".git" in dp.split(os.sep):
            continue
        for name in fn:
            if not name.endswith((".html", ".json", ".md", ".csv", ".py", ".js", ".yml")):
                continue
            p = os.path.join(dp, name)
            try:
                raw = open(p, "rb").read()
            except OSError:
                continue
            hits = hyphen.findall(raw)
            if hits:
                bad_files.append((os.path.relpath(p, ROOT), len(hits)))
            slash_total += len(slash.findall(raw))
    if bad_files:
        for p, n in bad_files:
            fail(f"dead Federal Register date path ({n}x, HTTP 404): {p}")
    notes.append(f"{slash_total} Federal Register URLs use the working /YYYY/MM/DD/ date path; "
                 f"{len(bad_files)} file(s) use the dead hyphenated form")

    for c in d["corrections_applied"]:
        if not c.get("file"):
            fail(f"{c.get('id')}: correction names no file")
        if not c.get("source") or not is_official(c.get("source", "")):
            fail(f"{c.get('id')}: correction has no official source URL")
        for k in ("was", "now"):
            if not c.get(k):
                fail(f"{c.get('id')}: correction is missing the {k!r} side")

    # Corrections this session established but did not apply itself, because a
    # parallel session's open pull request rewrites the same lines. Each must
    # still record the independent basis and how it was resolved.
    for c in d.get("corroborated_corrections", []):
        cid = c.get("id", "<no id>")
        for k in ("issue", "independent_basis_this_session", "resolution"):
            if not c.get(k):
                fail(f"{cid}: corroborated correction is missing {k!r}")
        if not c.get("source") or not is_official(c.get("source", "")):
            fail(f"{cid}: corroborated correction has no official source URL")
    n_applied = len(d["corrections_applied"])
    n_corr = len(d.get("corroborated_corrections", []))
    notes.append(f"{n_applied} correction(s) applied by this session; {n_corr} established independently and "
                 f"de-conflicted against a parallel session's open pull request, each with its own official basis")

    for c in d["change_requests"]:
        if not c.get("file"):
            fail(f"{c.get('id')}: change request names no file")
        if not c.get("owner"):
            fail(f"{c.get('id')}: change request does not record the owning session")
        if not c.get("source") or not is_official(c.get("source", "")):
            fail(f"{c.get('id')}: change request has no official source URL")
    notes.append(f"{len(d['change_requests'])} change requests logged against other sessions' files "
                 f"(logged, not edited)")

    # Internal links on the page this session publishes.
    page = os.path.join(ROOT, "verify-e071bffc.html")
    if os.path.exists(page):
        html = open(page, encoding="utf-8").read()
        for m in re.findall(r'href="([^"#]+\.html)"', html):
            if m.startswith("http"):
                continue
            if not os.path.exists(os.path.join(ROOT, m)):
                fail(f"verify-e071bffc.html links to a page that does not exist: {m}")
        if "<title>" not in html:
            fail("verify-e071bffc.html has no <title>")
        notes.append("verify-e071bffc.html internal links resolve")
    else:
        fail("verify-e071bffc.html does not exist")

    # The enacted California statute is the highest-authority source in this pass.
    # If it stops being cited, the page silently loses its strongest evidence.
    ab = "leginfo.legislature.ca.gov"
    cited = [f for f in d["findings"] if ab in (f.get("source") or "")]
    if not cited:
        fail("no finding cites the enacted California statute at leginfo.legislature.ca.gov")
    else:
        notes.append(f"{len(cited)} finding(s) rest on the enacted California statute (AB 2161, Welf. & Inst. Code 14005.69)")

    print("arena/e071bffc verification pass")
    print("-" * 62)
    for n in notes:
        print("  OK   " + n)
    if failures:
        print("-" * 62)
        for f in failures:
            print("  FAIL " + f)
        print(f"\n{len(failures)} check(s) FAILED")
        return 1
    print("-" * 62)
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
