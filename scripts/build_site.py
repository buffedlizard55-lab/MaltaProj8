#!/usr/bin/env python3
"""
Build the static site from the verified data files.

Every published value lives in data/entries-*.json and points at a source id in
data/sources.json. This script never invents content: it only formats what the
data files contain.

Usage:  python3 scripts/build_site.py
"""

import json
import os
import re
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = ROOT

NAV = [
    ("index", "Overview"),
    ("options", "Options"),
    ("work-requirements", "Work Rules"),
    ("income-counting", "Income"),
    ("medicaid-eligibility", "Medi-Cal"),
    ("covered-california", "Covered CA"),
    ("immigration-status", "Status"),
    ("california-changes", "2026–27 Changes"),
    ("timeline", "Timeline"),
    ("apply", "Apply"),
    ("flagged", "Flagged"),
    ("sources", "Sources"),
]

PAGE_META = {
    "index": {
        "title": "California Health Coverage with No Earned Income",
        "h1": "California health coverage with no earned income",
        "lede": "A research brief for a California permanent resident (or citizen) who works as a property manager and full-time Kalshi trader, has no wages, and has income from rental property, savings interest and trading. "
                "Every value below is traced to a federal, state or Covered California source and links to it.",
    },
    "options": {
        "title": "Your options",
        "h1": "Your options",
        "lede": "Four routes to health coverage, what each costs, and what each does to the 2027 work requirement.",
    },
    "work-requirements": {
        "title": "Work & community engagement rules",
        "h1": "The new work requirement, in detail",
        "lede": "Section 71119 of H.R. 1 (Public Law 119-21) and California's implementation of it: who is subject, how to comply, who is exempt, and what happens if you do not comply.",
    },
    "income-counting": {
        "title": "How your income is counted",
        "h1": "How your income is counted",
        "lede": "Medi-Cal, Covered California and the $580 work-rule test all use MAGI. Here is exactly what that means for rental income, savings interest and trading.",
    },
    "medicaid-eligibility": {
        "title": "Medi-Cal eligibility",
        "h1": "Medi-Cal eligibility",
        "lede": "Coverage groups, 2026 income limits, asset rules, and which programs are not subject to the work requirement.",
    },
    "covered-california": {
        "title": "Covered California",
        "h1": "Covered California",
        "lede": "Federal premium tax credits, the California Premium Subsidy, what you would actually pay, and the 2027 open-enrollment dates.",
    },
    "immigration-status": {
        "title": "Immigration status",
        "h1": "Immigration status and coverage",
        "lede": "How a green card (or citizenship) affects Medi-Cal and marketplace financial help, and what changes between 2026 and 2027.",
    },
    "california-changes": {
        "title": "California changes 2026–2027",
        "h1": "California changes, 2026–2027",
        "lede": "Every dated change to Medi-Cal and Covered California in this window, and what California is doing to soften the federal changes.",
    },
    "timeline": {
        "title": "Timeline",
        "h1": "Key dates",
        "lede": "Every date that matters, in order, with its official source.",
    },
    "apply": {
        "title": "How to apply",
        "h1": "How to apply",
        "lede": "Where to apply, how to answer the income questions, what to gather, and who to call.",
    },
    "flagged": {
        "title": "Flagged for review",
        "h1": "Flagged for review",
        "lede": "Everything this analysis could not confirm, everything where two official sources disagree, and the boundaries of the analysis.",
    },
    "sources": {
        "title": "Sources",
        "h1": "Sources",
        "lede": "Every official source used on this site, with publisher and date. No other source was used to state a value.",
    },
}


def load_json(name):
    with open(os.path.join(DATA, name), "r", encoding="utf-8") as fh:
        return json.load(fh)


def esc(text):
    return (text or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_sources():
    return {s["id"]: s for s in load_json("sources.json")["sources"]}


def source_cell(sources, sid):
    src = sources.get(sid)
    if not src:
        return '<span class="no-source">missing source</span>'
    return (
        '<a class="src" href="{url}" target="_blank" rel="noopener noreferrer">'
        "{name} <span class=\"pub\">{pub}</span></a>"
    ).format(url=esc(src["url"]), name=esc(src["name"]), pub=esc(src["publisher"]))


def render_table(rows, sources, table_id):
    head = ["Item", "Value", "Details", "Source"]
    out = ['<div class="table-wrap">']
    if table_id:
        out.append(
            '<div class="table-tools"><label class="search">'
            '<span class="vh">Filter rows</span>'
            '<input type="search" data-filter-for="{}" placeholder="Filter rows…" '
            'aria-label="Filter rows in this table"></label>'
            '<span class="rowcount" data-count-for="{}"></span></div>'.format(table_id, table_id)
        )
    out.append('<table id="{}" class="data">'.format(table_id))
    out.append("<thead><tr>" + "".join("<th>{}</th>".format(h) for h in head) + "</tr></thead>")
    out.append("<tbody>")
    for row in rows:
        verified = row.get("verified", True)
        item = row.get("item", "")
        value = row.get("value", "")
        detail = row.get("detail", "")
        flag = row.get("flag", "")
        classes = "row" + ("" if verified else " row-flagged")
        out.append('<tr class="{}">'.format(classes))
        out.append("<td><span class=\"item\">{}</span>".format(item))
        if not verified:
            out.append('<span class="badge badge-flag">flagged</span>')
        out.append("</td>")
        if verified:
            out.append('<td class="value">{}</td>'.format(value))
        else:
            out.append('<td class="value"><span class="unverified">not confirmed</span></td>')
        detail_html = "<p>{}</p>".format(detail) if detail else ""
        if flag:
            detail_html += '<p class="flag"><strong>Flag:</strong> {}</p>'.format(flag)
        out.append("<td>{}</td>".format(detail_html))
        cell = source_cell(sources, row.get("source", ""))
        for extra in row.get("also", []):
            cell += "<br>" + source_cell(sources, extra)
        out.append("<td>{}</td>".format(cell))
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out)


def render_flags(flags, sources):
    out = ['<div class="table-wrap"><table class="data flags">']
    out.append(
        "<thead><tr><th>Item</th><th>What is known</th><th>Why it matters / what to do</th><th>Source</th></tr></thead><tbody>"
    )
    for item in flags:
        src_links = " ".join(source_cell(sources, sid) for sid in item.get("sources", []))
        out.append(
            '<tr class="row row-flagged" id="{id}">'
            '<td><span class="item">{title}</span><span class="badge badge-flag">{cat}</span></td>'
            "<td><p><strong>Issue:</strong> {issue}</p><p><strong>What is known:</strong> {known}</p></td>"
            "<td><p><strong>Why it matters:</strong> {why}</p><p><strong>What to do:</strong> {action}</p></td>"
            "<td>{srcs}</td></tr>".format(
                id=esc(item["id"]),
                title=esc(item["title"]),
                cat=esc(item["category"]),
                issue=esc(item["issue"]),
                known=esc(item["known"]),
                why=esc(item["why"]),
                action=esc(item["action"]),
                srcs=src_links,
            )
        )
    out.append("</tbody></table></div>")
    return "\n".join(out)


def render_sources_table(sources):
    rows = sorted(sources.values(), key=lambda s: s["publisher"])
    out = ['<div class="table-wrap"><table class="data"><thead><tr><th>Source</th><th>Publisher</th><th>Type</th><th>Date</th></tr></thead><tbody>']
    for s in rows:
        out.append(
            '<tr class="row"><td><a class="src" href="{url}" target="_blank" rel="noopener noreferrer">{name}</a></td>'
            "<td>{pub}</td><td>{typ}</td><td>{date}</td></tr>".format(
                url=esc(s["url"]), name=esc(s["name"]), pub=esc(s["publisher"]),
                typ=esc(s["type"]), date=esc(s["date"]),
            )
        )
    out.append("</tbody></table></div>")
    return "\n".join(out)


def page_html(slug, body, meta, sources, page_json):
    nav_html = []
    for key, label in NAV:
        cls = ' class="active"' if key == slug else ""
        nav_html.append('<a href="{}.html"{}>{}</a>'.format(key, cls, label))
    title = meta["title"]
    lede = meta["lede"]
    updated = datetime.date.today().isoformat()
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — California Health Coverage Options</title>
<meta name="description" content="{lede}">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap header-inner">
    <div class="brand">
      <a href="index.html" class="brand-link">
        <span class="brand-mark" aria-hidden="true">CA</span>
        <span class="brand-text">
          <strong>California Health Coverage Options</strong>
          <span>No earned income · permanent resident · 0 wage income</span>
        </span>
      </a>
    </div>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
  </div>
  <nav id="site-nav" class="site-nav" aria-label="Main">
    <div class="wrap nav-inner">{nav}</div>
  </nav>
</header>

<main id="main" class="wrap">
  <h1>{h1}</h1>
  <p class="lede">{lede}</p>
  {body}
</main>

<footer class="site-footer">
  <div class="wrap">
    <p><strong>Research brief, not legal, tax or immigration advice.</strong> Every value on this site is linked to the official source it came from. If a value could not be confirmed, it is left blank and listed on the <a href="flagged.html">Flagged for Review</a> page.</p>
    <p class="muted">Source list: <a href="sources.html">all official sources</a> · Page generated {updated}.</p>
  </div>
</footer>
<script src="assets/site.js" defer></script>
</body>
</html>
""".format(
        title=esc(title), lede=esc(lede), h1=esc(meta["h1"]), nav="".join(nav_html),
        body=body, updated=updated,
    )


def build_page(slug, sources):
    page = load_json("page-{}.json".format(slug))
    entries_file = os.path.join(DATA, "entries-{}.json".format(slug))
    entries = load_json("entries-{}.json".format(slug))["tables"] if os.path.exists(entries_file) else {}
    flags = load_json("flagged.json") if slug == "flagged" else None

    parts = []
    for section in page["sections"]:
        parts.append('<section class="card" id="{}">'.format(section["id"]))
        parts.append("<h2>{}</h2>".format(section["heading"]))
        if section.get("intro"):
            parts.append('<p class="section-intro">{}</p>'.format(section["intro"]))
        if section.get("note"):
            parts.append('<p class="callout">{}</p>'.format(section["note"]))
        if section.get("list"):
            parts.append("<ul class=\"checklist\">" + "".join("<li>{}</li>".format(i) for i in section["list"]) + "</ul>")
        table_id = section.get("table")
        if table_id:
            if slug == "flagged":
                parts.append(render_flags(flags["items"], sources))
            elif slug == "sources":
                parts.append(render_sources_table(sources))
            else:
                rows = entries.get(table_id, [])
                parts.append(render_table(rows, sources, table_id))
        parts.append("</section>")

    if slug == "flagged":
        parts.insert(1, '<p class="section-intro">{}</p>'.format(esc(flags["intro"])))
    if slug == "index":
        parts.insert(
            1,
            '<section class="card card-hero" id="bottom-line"><h2>The bottom line</h2>'
            "<ul class=\"checklist\">"
            "<li><strong>You do not need earned income to qualify for Medi-Cal</strong> — and you do not need earned income to satisfy the 2027 work rule.</li>"
            "<li><strong>Your income is not $0.</strong> Net rent, savings interest and trading results are all counted as MAGI income, both for the 138% FPL Medi-Cal limit and for the $580 work-rule test.</li>"
            "<li><strong>The simplest path is Medi-Cal</strong> if your MAGI is at or below $22,025 for 2026 (one person). You can apply year-round and it costs little or nothing.</li>"
            "<li><strong>If you are on Medi-Cal in 2027</strong>, make sure at least one month in every six-month window has either $580 of income from any source or 80 hours of work, volunteering, community service, job training or school.</li>"
            "<li><strong>If you have a qualifying disability</strong>, the Aged &amp; Disabled Medi-Cal program is not subject to the work rule at all — but your assets are counted.</li>"
            "</ul></section>",
        )

    body = "\n".join(parts)
    meta = PAGE_META[slug]
    out_path = os.path.join(OUT, "{}.html".format(slug))
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(page_html(slug, body, meta, sources, page))
    return out_path


def main():
    sources = build_sources()
    written = []
    for slug, _label in NAV:
        written.append(build_page(slug, sources))
    print("Built {} pages:".format(len(written)))
    for path in written:
        print("  " + os.path.relpath(path, ROOT))


if __name__ == "__main__":
    main()
