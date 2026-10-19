#!/usr/bin/env python3
"""
Validate data/core.json and the pages generated from it by build_core.py.

Rules enforced (matching the build guard and the site's published promise):
  1. every record names a source id that exists in the register;
  2. a verified record has a non-empty value;
  3. an unverified record has an empty value (never inferred, never filled);
  4. source ids, finding ids and flag ids are unique and sequential;
  5. every source URL is https and on an official domain allowlist;
  6. warn on registered sources not used by a factual record;
  7. all eight guide pages exist, have direct official row citations,
     unique ids, working table filters and no None/NaN/TODO placeholders.

Exit code 0 = pass. Non-zero = failure, with the reasons printed.
Usage: python3 scripts/check_core.py
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "core.json")

OFFICIAL_HOSTS = (
    "congress.gov",
    "federalregister.gov",
    "cms.gov",
    "medicaid.gov",
    "hhs.gov",
    "dhcs.ca.gov",
    "chhs.ca.gov",
    "ca.gov",
    "coveredca.com",
    "irs.gov",
    "cftc.gov",
    "ecfr.gov",
    "ssa.gov",
    "bls.gov",
    "healthcare.gov",
    "house.gov",
    "hrsa.gov",
)

PAGES = {
    "index.html": "Dashboard",
    "executive-summary.html": "Executive Summary",
    "work-rules.html": "Work Rules",
    "playbook.html": "Playbook",
    "coverage-options.html": "Coverage Options",
    "findings.html": "Findings",
    "verification.html": "Verification",
    "flagged.html": "Flagged for Review",
}

SECTIONS = (
    "key_numbers",
    "profile",
    "gates",
    "options",
    "pathways",
    "findings",
    "ca_actions",
    "timeline",
    "flags",
    "action_plan",
    "routes",
    "income_types",
    "evidence",
    "calendar",
)


def host_ok(url):
    m = re.match(r"^https://([^/]+)/", url)
    if not m:
        return False
    host = m.group(1).lower()
    return any(host == h or host.endswith("." + h) for h in OFFICIAL_HOSTS)


def main():
    errors = []
    warnings = []
    with open(DATA, encoding="utf-8") as fh:
        data = json.load(fh)

    for key in ("meta", "sources") + SECTIONS:
        if key not in data:
            errors.append(f"missing top-level key: {key}")
    if errors:
        return report(errors)

    sources = {}
    seen_urls = {}
    for s in data["sources"]:
        sid = s.get("id", "")
        if sid in sources:
            errors.append(f"duplicate source id: {sid}")
        sources[sid] = s
        for field in ("title", "publisher", "url", "date", "short"):
            if not s.get(field):
                errors.append(f"{sid}: missing {field}")
        url = s.get("url", "")
        if not host_ok(url) or s.get("official") is not True:
            errors.append(f"{sid}: not an official https URL: {url}")
        if url in seen_urls:
            errors.append(f"{sid}: duplicate URL also used by {seen_urls[url]}")
        seen_urls[url] = sid

    ids = [s["id"] for s in data["sources"]]
    expected = [f"S{i:02d}" for i in range(1, len(ids) + 1)]
    if ids != expected:
        errors.append(f"source ids are not sequential S01..S{len(ids):02d}")

    used = set()
    for section in SECTIONS:
        for row in data.get(section, []):
            sid = row.get("source")
            label = row.get("id") or row.get("fact") or row.get("label") or "?"
            if not sid:
                errors.append(f"{section}/{label}: no source id")
            elif sid not in sources:
                errors.append(f"{section}/{label}: unknown source {sid}")
            else:
                used.add(sid)
            for extra in row.get("also", []):
                if extra not in sources:
                    errors.append(f"{section}/{label}: unknown additional source {extra}")
                else:
                    used.add(extra)

    # Cross-program FPL years must not silently be interchanged by the builder.
    kpis = {r["label"]: r for r in data["key_numbers"]}
    cc26 = kpis.get("Covered CA subsidy cliff (single, 2026)", {})
    cc27 = kpis.get("Covered CA 400% reference (single, 2027)", {})
    if cc26.get("value") != "$62,600 / year" or cc26.get("source") != "S41":
        errors.append("2026 marketplace 400% FPL must use the $62,600 Covered CA plan-year source")
    if cc27.get("value") != "$63,840 / year" or cc27.get("source") != "S43":
        errors.append("2027 marketplace 400% FPL must be separately labelled $63,840")
    seasonal = next((p for p in data["pathways"] if p["id"] == "P4"), {})
    if "seasonal worker" not in seasonal.get("what", "") or "lumpy Kalshi" not in seasonal.get("fit", ""):
        errors.append("seasonal averaging must not be offered solely for fluctuating trading")

    for row in data["findings"]:
        fid = row.get("id", "?")
        status = row.get("status")
        value = row.get("value")
        for field in ("id", "category", "finding", "value", "status", "source"):
            if field not in row:
                errors.append(f"findings/{fid}: missing field {field}")
        if status not in ("verified", "verified-nuance", "flagged", "unverified"):
            errors.append(f"findings/{fid}: unknown status {status!r}")
        if status in ("verified", "verified-nuance") and not value:
            errors.append(f"findings/{fid}: verified but no value")
        if status == "unverified" and value:
            errors.append(f"findings/{fid}: unverified but carries value {value!r}")

    fids = [f["id"] for f in data["findings"]]
    expected = [f"F{i:02d}" for i in range(1, len(fids) + 1)]
    if fids != expected:
        errors.append("finding ids are not sequential F01..F%02d" % len(fids))

    flids = [f["id"] for f in data["flags"]]
    expected = [f"FL-{i:02d}" for i in range(1, len(flids) + 1)]
    if flids != expected:
        errors.append("flag ids are not sequential FL-01..FL-%02d" % len(flids))
    for f in data["flags"]:
        if f.get("status") not in ("open", "closed", "unverified"):
            errors.append(f"flags/{f['id']}: unknown status {f.get('status')!r}")
        for field in ("item", "issue", "impact", "source"):
            if not f.get(field):
                errors.append(f"flags/{f['id']}: missing {field}")

    unused = sorted(set(sources) - used, key=lambda x: int(x[1:]))
    if unused:
        warnings.append("register sources not cited by a table row: " + ", ".join(unused))

    if not errors:
        for name in PAGES:
            path = os.path.join(ROOT, name)
            if not os.path.exists(path):
                errors.append(f"missing generated page: {name}")
                continue
            text = open(path, encoding="utf-8").read()
            if len(text) < 2000:
                errors.append(f"{name}: suspiciously small ({len(text)} bytes)")
            for token in (">nan<", ">NaN<", "TODO", "Lorem ipsum", "{{", "undefined"):
                if token in text:
                    errors.append(f"{name}: placeholder token {token!r}")
            if f'href="{name}" class="active"' not in text:
                errors.append(f"{name}: nav does not mark itself active")

    for name, table_id in (("findings.html", "all-findings"), ("flagged.html", "flags-open"),
                           ("verification.html", "source-register")):
        text = open(os.path.join(ROOT, name), encoding="utf-8").read()
        if f'id="{table_id}"' not in text:
            errors.append(f"{name}: missing table id {table_id}")

    # A registered source elsewhere on the page is not a citation for this row.
    # Navigational directories are lists; every factual table row needs its own
    # official primary link. Importing here also checks unique IDs/filter targets.
    from check_accuracy import audit_page
    for name in (*PAGES, "archives.html"):
        if os.path.exists(os.path.join(ROOT, name)):
            _count, missing = audit_page(name)
            errors.extend(f"{name}: {issue}" for issue in missing)

    return report(errors, data, warnings)


def report(errors, data=None, warnings=None):
    if errors:
        print(f"FAIL — {len(errors)} problem(s):")
        for e in errors:
            print("  -", e)
        return 1
    for w in warnings or []:
        print("  ! " + w)
    print(f"PASS — {len(data['sources'])} sources, {len(data['findings'])} findings, "
          f"{len(data['flags'])} flags, {len(data['pathways'])} pathways, "
          f"{len(data['options'])} coverage options, {len(data['timeline'])} timeline events.")
    print("      All source ids resolve, all verified rows carry values, all unverified rows are blank,")
    print("      every registered URL is official https, all 8 pages are present, and every factual table row has a direct official link.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
