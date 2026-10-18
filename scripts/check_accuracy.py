#!/usr/bin/env python3
"""Fail closed on the 2026–27 corrections owned by task 21.

This is a structural/source-presence regression test, not a substitute for
reading the cited government publications or obtaining an eligibility ruling.
Historical independent verification pages are inventoried but not rewritten.
Run from any working directory: python3 scripts/check_accuracy.py
"""
from __future__ import annotations

import json
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
OWNED_PAGES = (
    "index.html",
    "accuracy-93fdc24b.html",
    "flagged.html",
    "income.html",
    "pathways.html",
    "overview.html",
    "work-requirements.html",
    "income-counting.html",
    "covered-california.html",
    "sources.html",
    "docs/index.html",
    "docs/executive-summary.html",
    "docs/medicaid.html",
    "docs/covered-california.html",
    "docs/new-laws.html",
    "docs/income-taxes.html",
    "docs/action-plan.html",
    "docs/flagged-for-review.html",
    "docs/sources.html",
)
EXTERNAL_OFFICIAL = {"coveredca.com", "www.coveredca.com", "hbex.coveredca.com", "board.coveredca.com"}


def official(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    return url.startswith("https://") and (host.endswith(".gov") or host in EXTERNAL_OFFICIAL)


class Rows(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.rows: list[tuple[str, list[str]]] = []
        self.row: dict | None = None
        self.ids: list[str] = []
        self.table_ids: set[str] = set()
        self.filter_targets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if attr.get("id"):
            self.ids.append(attr["id"] or "")
        if tag == "table" and attr.get("id"):
            self.table_ids.add(attr["id"] or "")
        if tag == "input" and attr.get("data-filter-for"):
            self.filter_targets.append(attr["data-filter-for"] or "")
        if tag == "tr":
            self.row = {"data": False, "text": "", "links": []}
        if self.row is not None:
            if tag == "td":
                self.row["data"] = True
            if tag == "a":
                self.row["links"].append(attr.get("href") or "")

    def handle_data(self, data: str) -> None:
        if self.row is not None:
            self.row["text"] += data + " "

    def handle_endtag(self, tag: str) -> None:
        if tag == "tr" and self.row is not None:
            if self.row["data"]:
                self.rows.append((" ".join(self.row["text"].split()), self.row["links"]))
            self.row = None


def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def audit_page(rel: str) -> tuple[int, list[str]]:
    parser = Rows()
    parser.feed((ROOT / rel).read_text(encoding="utf-8"))
    failures = [f"row {i}: {text[:85]}" for i, (text, urls) in enumerate(parser.rows, 1)
                if not any(official(url) for url in urls)]
    duplicate_ids = [key for key, n in Counter(parser.ids).items() if n > 1]
    if duplicate_ids:
        failures.append(f"duplicate HTML ids: {', '.join(duplicate_ids[:5])}")
    invalid_filters = [target for target in parser.filter_targets if target not in parser.table_ids]
    if invalid_filters:
        failures.append(f"table filter does not target a <table>: {', '.join(invalid_filters[:5])}")
    return len(parser.rows), failures


def main() -> None:
    errors: list[str] = []
    limits = load("data/magi-limits.json")["thresholds"]

    def limit(program: str, year: int):
        hits = [item for item in limits if item["program"].startswith(program) and item["coverage_year"] == year]
        if len(hits) != 1:
            errors.append(f"{program} {year}: expected exactly one limit row")
            return {}
        return hits[0]

    med_26 = limit("MAGI Medi-Cal", 2026)
    med_27 = limit("MAGI Medi-Cal", 2027)
    cc_26 = limit("Covered California, 2026", 2026)
    cc_27 = limit("Covered California, 2027 marketplace", 2027)
    if (med_26.get("annual_usd"), med_26.get("monthly_usd")) != (22025, 1836):
        errors.append("2026 Medi-Cal one-person DHCS chart is not $22,025/year and $1,836/month")
    if cc_26.get("annual_usd") != 62600 or cc_26.get("poverty_guideline_reference_year") != 2025:
        errors.append("2026 marketplace 400% FPL must be $62,600 using the prior-year reference")
    if cc_27.get("annual_usd") != 63840 or cc_27.get("poverty_guideline_reference_year") != 2026:
        errors.append("2027 marketplace 400% FPL must be $63,840")
    if any(med_27.get(key) is not None for key in ("annual_usd", "monthly_usd", "poverty_guideline_reference_year")):
        errors.append("2027 Medi-Cal FPL is not established: leave all 2027 amount/reference fields null")
    for item in limits:
        if not official(item.get("source", "")):
            errors.append(f"limit without official evidence: {item.get('program')}")

    source_ids = {s["id"] for s in load("data/sources.json")["sources"]}
    for file in sorted((ROOT / "data").glob("entries-*.json")):
        data = json.loads(file.read_text(encoding="utf-8"))
        for table, rows in data.get("tables", {}).items():
            for row in rows:
                if row.get("source") not in source_ids or any(x not in source_ids for x in row.get("also", [])):
                    errors.append(f"{file.name}/{table}: source id missing")
                if row.get("verified") is False and (row.get("value") or "").strip():
                    errors.append(f"{file.name}/{table}: unverified value was filled in")
    for file in ("data/income-tax.json", "data/coverage.json", "data/laws.json"):
        d = load(file)
        rows = d.get("rows") or [row for section in d["sections"] for row in section["rows"]]
        for row in rows:
            if not official(row.get("source_url", "")):
                errors.append(f"{file} {row['id']}: table's direct source is not an official site")
            if row.get("status") == "flagged" and (row.get("value") or "").strip():
                errors.append(f"{file} {row['id']}: flagged personal/unknown value was filled in")

    owned_rows = 0
    for rel in OWNED_PAGES:
        count, missing = audit_page(rel)
        owned_rows += count
        errors.extend(f"{rel}: {issue}" for issue in missing)

    # Legacy audit pages are read-only: count, do not disguise unsourced rows
    # by adding unrelated URLs. The root Flagged hub points to their register.
    legacy = []
    for file in sorted(ROOT.rglob("*.html")):
        if any(part in {".git", "node_modules", "_site"} for part in file.parts):
            continue
        rel = file.relative_to(ROOT).as_posix()
        if rel not in OWNED_PAGES:
            _count, missing = audit_page(rel)
            if missing:
                legacy.append((rel, len(missing)))
    print(f"Checked {owned_rows} table rows across {len(OWNED_PAGES)} task-21 pages (official per-row citations).")
    if legacy:
        print("Other independently maintained pages still have direct-row-link gaps (not certified here):")
        for rel, count in legacy:
            print(f"  {rel}: {count}")
    if errors:
        for error in errors:
            print("ERROR:", error)
        raise SystemExit(1)
    print("Accuracy regression checks passed; structural evidence only, not legal/URL uptime certification.")


if __name__ == "__main__":
    main()
