#!/usr/bin/env python3
"""
Build the extended-analysis pages of the MaltaProj8 site from the verified data files.

Every published value lives in data/entries-*.json and points at a source id in
data/sources.json. This script never invents content: it only formats what the
data files contain.

It renders the "Extended Analysis" section of the site (overview, options, work
rules, income counting, Medi-Cal, Covered California, immigration status,
California changes, timeline, apply, sources) and integrates it into the pages
owned by the primary session (index.html, flagged.html and the shared top
navigation) without removing any of their content.

Usage:  python3 scripts/build_site.py
"""

import json
import os
import re
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = ROOT

# Pages rendered by this script (slug, label).
EXT_NAV = [
    ("overview", "Overview"),
    ("options", "Options"),
    ("work-requirements", "Work Rules"),
    ("income-counting", "Income Counting"),
    ("medicaid-eligibility", "Medi-Cal"),
    ("covered-california", "Covered CA"),
    ("immigration-status", "Immigration Status"),
    ("california-changes", "2026–27 Changes"),
    ("timeline", "Timeline"),
    ("apply", "Apply"),
    ("sources", "Sources"),
]

# Site-wide navigation (href, label). The first eight entries are the pages
# published by the primary session; the last two are the shared pages.
PRIMARY_NAV = [
    ("index.html", "Dashboard"),
    ("law.html", "The Law"),
    ("california.html", "California"),
    ("income.html", "Income Types"),
    ("pathways.html", "0-Earned Playbook"),
    ("exemptions.html", "Exemptions"),
    ("verification.html", "Verification"),
    ("overview.html", "Extended Analysis"),
    ("research/index.html", "Research Dashboard"),
    ("coverage-guide/index.html", "Coverage Guide"),
    ("docs/index.html", "Docs Dashboard"),
    ("flagged.html", "Flagged for Review"),
    ("accuracy-93fdc24b.html", "Accuracy Update"),
    ("audit-6fc18b58.html", "Independent Audit"),
]

# Pages published by the primary session that receive the shared navigation link.
SHARED_PAGES = [
    "index.html",
    "law.html",
    "california.html",
    "income.html",
    "pathways.html",
    "exemptions.html",
    "verification.html",
    "flagged.html",
]

# Complete page index published on the dashboard.
PAGE_INDEX = [
    (
        "Start here",
        [
            ("index.html", "Dashboard", "Executive summary, the short answer, and the seven compliance paths."),
            ("overview.html", "Extended overview", "The full table set: your situation at a glance, income bands, and the decision path."),
            ("docs/executive-summary.md", "Executive summary (Markdown)", "Corrected long-form guidance with year-specific sources and unresolved personal values."),
            ("accuracy-93fdc24b.html", "Accuracy update (18 October 2026)", "Enacted MAGI income test, seasonal averaging, plan-year thresholds and live flags."),
            ("audit-6fc18b58.html", "Independent source audit", "Earlier independently published row-link inventory and open questions."),
        ],
    ),
    (
        "The new rule",
        [
            ("law.html", "The law, line by line", "H.R. 1 § 71119 and the CMS interim final rule, quoted and cited."),
            ("work-requirements.html", "Work & community engagement rules", "Who is subject, how to comply, the $580 test, exemptions, hardship, and what happens if you miss it."),
            ("income-counting.html", "How income is counted", "Rent, interest, and unresolved Kalshi tax character under MAGI-based methods."),
        ],
    ),
    (
        "Your coverage options",
        [
            ("options.html", "Options compared", "Medi-Cal, Covered California, employer coverage, and paying full price, side by side."),
            ("medicaid-eligibility.html", "Medi-Cal eligibility", "Coverage groups, 2026 income limits, asset rules, and which programs have no work rule."),
            ("covered-california.html", "Covered California", "Federal premium tax credits, the California Premium Subsidy, and 2027 enrollment dates."),
            ("immigration-status.html", "Immigration status", "How a green card or citizenship changes Medi-Cal and marketplace financial help."),
        ],
    ),
    (
        "California specifics",
        [
            ("california.html", "California's response", "What California is doing about the federal changes."),
            ("california-changes.html", "Changes in 2026–2027", "Every dated change to Medi-Cal and Covered California in this window."),
            ("pathways.html", "0-earned-income playbook", "Concrete ways to satisfy the rule with no wages."),
            ("exemptions.html", "Exemptions", "Who does not have to comply at all."),
        ],
    ),
    (
        "Doing it",
        [
            ("apply.html", "How to apply", "Where to apply, how to answer the income questions, what to gather, who to call."),
            ("timeline.html", "Key dates", "Every date that matters, in order, with its source."),
            ("income.html", "Income types deep dive", "Rent, interest, trading, and self-employment, classified and counted."),
        ],
    ),
    (
        "Evidence",
        [
            ("verification.html", "Earlier verification log", "Historical checks; compare conclusions with the current accuracy update."),
            ("sources.html", "Source register", "Official sources cited in this section, with publisher and date."),
            ("flagged.html", "Flagged for Review", "Everything that could not be confirmed, and where two official sources disagree."),
            ("verify-95219c64.html", "Independent check #1 (95219c64)", "First independent line-by-line re-verification: 13 claims re-checked, 5 nuances."),
            ("verify-9285d712.html", "Independent check #2 (9285d712)", "Second independent re-verification: 13 claims, 2 corrections (cost-sharing §71120, 40-state count), 6 nuances."),
            ("research/index.html", "Research dashboard", "A second, independently sourced dashboard: 52 source-linked findings."),
            ("coverage-guide/index.html", "Coverage guide", "A third, independently sourced dashboard: 65 findings with locators and excerpts."),
            ("docs/index.html", "Docs dashboard", "A fourth dashboard: 10 pages, 76 sourced rows on income taxes, coverage and the new laws."),
        ],
    ),
]

PAGE_META = {
    "overview": {
        "title": "Extended overview",
        "h1": "California health coverage with no earned income",
        "lede": "A research brief for a California permanent resident (or citizen) who works as a property manager and full-time Kalshi trader, has no wages, and has income from rental property, savings interest and trading. "
                "General rules are sourced; personal eligibility and Kalshi tax character are not established. Read the accuracy update before older pages.",
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
    "sources": {
        "title": "Sources",
        "h1": "Sources",
        "lede": "Every official source used in this section, with publisher and date. No other source was used to state a value.",
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
    # Section ids are used by anchor links. Reusing them on <table> caused
    # getElementById() to select a section, not a table, breaking row filters.
    dom_id = "table-{}".format(table_id) if table_id else "table-entries"
    if table_id:
        out.append(
            '<div class="table-tools"><label class="search">'
            '<span class="vh">Filter rows</span>'
            '<input type="search" data-filter-for="{}" placeholder="Filter rows…" '
            'aria-label="Filter rows in this table"></label>'
            '<span class="rowcount" data-count-for="{}"></span></div>'.format(dom_id, dom_id)
        )
    out.append('<table id="{}" class="data">'.format(dom_id))
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


def render_flags(flags, sources, id_prefix="F"):
    """Render flagged items. id_prefix keeps this section's ids from colliding
    with the ids already used on the shared Flagged for Review page."""
    out = ['<div class="table-wrap"><table class="data flags">']
    out.append(
        "<thead><tr><th>Item</th><th>What is known</th><th>Why it matters / what to do</th><th>Source</th></tr></thead><tbody>"
    )
    for item in flags:
        src_links = " ".join(source_cell(sources, sid) for sid in item.get("sources", []))
        item_id = "{}-{}".format(id_prefix, item["id"].split("-")[-1])
        out.append(
            '<tr class="row row-flagged" id="{id}">'
            '<td><span class="item">{title}</span><span class="badge badge-flag">{cat}</span></td>'
            "<td><p><strong>Issue:</strong> {issue}</p><p><strong>What is known:</strong> {known}</p></td>"
            "<td><p><strong>Why it matters:</strong> {why}</p><p><strong>What to do:</strong> {action}</p></td>"
            "<td>{srcs}</td></tr>".format(
                id=esc(item_id),
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
    for href, label in PRIMARY_NAV:
        cls = ' class="active"' if href == "overview.html" else ""
        nav_html.append('<a href="{}"{}>{}</a>'.format(href, cls, label))
    sub_html = []
    for key, label in EXT_NAV:
        cls = ' class="active"' if key == slug else ""
        sub_html.append('<a href="{}.html"{}>{}</a>'.format(key, cls, label))
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
<div class="topbar">
  <div class="topbar-inner">
    <div class="brand">
      <div class="brand-badge">CA</div>
      <div>
        <h1><a class="brand-link" href="index.html">California Healthcare &amp; Work Requirements</a></h1>
        <p>Extended analysis · no wages-only gate · personal outcome unknown</p>
      </div>
    </div>
    <nav class="nav" aria-label="Main">{nav}</nav>
  </div>
</div>
<div class="subbar">
  <div class="topbar-inner">
    <span class="subbar-label">Extended analysis</span>
    <nav class="nav nav-sub" aria-label="Extended analysis pages">{subnav}</nav>
  </div>
</div>

<div class="wrap" id="main">
  <h1>{h1}</h1>
  <p class="lede">{lede}</p>
  <div class="callout"><strong>Current source-audit notice:</strong> Some independently authored conclusions on this site predate the later California law or mix 2026 and 2027 poverty guidelines. Read the <a href="accuracy-93fdc24b.html">dated accuracy update</a>, <a href="flagged.html">unresolved-items hub</a> and preserved <a href="audit-6fc18b58.html">independent audit</a>. A source link is not a finding that this individual qualifies.</div>
  {body}
</div>

<div class="footer">
  <div class="wrap footer-inner">
    <p><strong>Research brief, not legal, tax or immigration advice.</strong> Tables link to official material, but a citation does not establish an individual benefit decision. Unresolved and legacy issues appear at <a href="flagged.html">Flagged for Review</a> and the <a href="accuracy-93fdc24b.html">current accuracy update</a>.</p>
    <p class="muted">Source list: <a href="sources.html">all official sources</a> · <a href="index.html">dashboard</a> · <a href="verification.html">verification log</a> · Page generated {updated}.</p>
  </div>
</div>
<script src="assets/site.js" defer></script>
</body>
</html>
""".format(
        title=esc(title), lede=esc(lede), h1=esc(meta["h1"]),
        nav="".join(nav_html), subnav="".join(sub_html),
        body=body, updated=updated,
    )


def build_page(slug, sources):
    page = load_json("page-{}.json".format(slug))
    entries_file = os.path.join(DATA, "entries-{}.json".format(slug))
    entries = load_json("entries-{}.json".format(slug))["tables"] if os.path.exists(entries_file) else {}

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
            if slug == "sources":
                parts.append(render_sources_table(sources))
            else:
                rows = entries.get(table_id, [])
                parts.append(render_table(rows, sources, table_id))
        parts.append("</section>")

    if slug == "overview":
        parts.insert(
            1,
            '<section class="card card-hero" id="bottom-line"><h2>Bottom line — conditional, source linked</h2>'
            '<ul class="checklist">'
            '<li><strong>No wages-only gate:</strong> MAGI Medi-Cal and Covered California look to household income and other eligibility criteria, not a W-2. <a href="https://www.dhcs.ca.gov/medi-cal/help/">DHCS help</a>.</li>'
            '<li><strong>Work-rule income route:</strong> for covered adults from January 2027, California §14005.69(e)(6) uses at least $580 of monthly MAGI-based household income; a qualifying amount for this person has not been shown. <a href="https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202520260AB2161">Enacted statute</a>.</li>'
            '<li><strong>Seasonal-worker-only averaging:</strong> §14005.69(e)(7) does not extend a six-month average to every investor whose results fluctuate. <a href="https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202520260AB2161">Enacted statute</a>.</li>'
            '<li><strong>Separate plan years:</strong> 2026 Medi-Cal one-person reference $22,025/year ($1,836/month); 2026 marketplace 400% FPL $62,600; 2027 marketplace 400% FPL $63,840. <a href="https://www.dhcs.ca.gov/services/medi-cal-resources/medi-cal-eligibility-division/all-county-welfare-directors-medi-cal-eligibility-division-information-letters/2026-fpl-calculation-chart-monthly-values-enclosure-1/">DHCS 2026</a> · <a href="https://hbex.coveredca.com/data-research/dashboards/OE_Dashboard.pdf">Covered CA 2026</a> · <a href="https://www.coveredca.com/pdfs/FPL-chart.pdf">Covered CA 2027</a>.</li>'
            '<li><strong>Personal result unknown:</strong> no household, actual taxable rental/interest or Kalshi classification has been supplied. See <a href="flagged.html">Flagged for Review</a>; apply through <a href="https://www.dhcs.ca.gov/medi-cal/apply/">DHCS</a> for an agency decision.</li>'
            '</ul></section>',
        )

    body = "\n".join(parts)
    meta = PAGE_META[slug]
    out_path = os.path.join(OUT, "{}.html".format(slug))
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(page_html(slug, body, meta, sources, page))
    return out_path


# ---------------------------------------------------------------------------
# Integration into the pages owned by the primary session
# ---------------------------------------------------------------------------

def read(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def write(path, text):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def patch_between(text, start_marker, end_marker, block):
    """Replace the text between two markers, or insert the block if the markers
    are not present yet. Keeps the build idempotent."""
    if start_marker in text and end_marker in text:
        pattern = re.escape(start_marker) + r".*?" + re.escape(end_marker)
        return re.sub(pattern, start_marker + "\n" + block + "\n" + end_marker, text, flags=re.S)
    if start_marker in text:
        return text.replace(start_marker, start_marker + "\n" + block + "\n" + end_marker, 1)
    return text


# Links added to the shared top navigation so that every section of the site
# is reachable from every page. The two supplemental dashboards were requested
# by the sessions that built them.
NAV_START = "<!-- integration-links -->"
NAV_END = "<!-- /integration-links -->"

INTEGRATION_LINKS = [
    ("overview.html", "Extended Analysis"),
    ("research/index.html", "Research Dashboard"),
    ("coverage-guide/index.html", "Coverage Guide"),
    ("docs/index.html", "Docs Dashboard"),
]


def is_core_generated(html):
    """The primary core owns these pages; do not append stale legacy blocks."""
    return 'generated from <a href="data/core.json">' in html


def patch_shared_nav():
    """Add the section links to the shared top navigation.

    Only the navigation block is touched, and the inserted links are wrapped in
    markers so the patch can be re-run without duplicating them.
    """
    changed = []
    block = "".join('<a href="{}">{}</a>'.format(href, label) for href, label in INTEGRATION_LINKS)
    for name in SHARED_PAGES:
        path = os.path.join(OUT, name)
        if not os.path.exists(path):
            continue
        html = read(path)
        if is_core_generated(html):
            continue
        start = html.find('<nav class="nav"')
        end = html.find("</nav>", start)
        if start == -1 or end == -1:
            continue
        nav = html[start:end]
        for href, _label in INTEGRATION_LINKS:
            nav = re.sub(r'<a href="{}">[^<]*</a>\s*'.format(re.escape(href)), "", nav)
        nav = nav.replace(NAV_START, "").replace(NAV_END, "")
        nav = nav.rstrip() + "\n      " + NAV_START + block + NAV_END + "\n    "
        html = html[:start] + nav + html[end:]
        write(path, html)
        changed.append(name)
    return changed


def build_page_index_block():
    out = ['  <div class="card" id="page-index" style="margin-top:14px">',
           "    <h3>Complete page index — every page on this site</h3>",
           '    <p class="hint">Sections were independently authored. Read the current accuracy update for corrected income methods and FPL years before relying on older summaries.</p>',
           '    <div class="alert info"><strong>Read before using a figure.</strong> This is a collection of independently contributed research pages, not a personal eligibility determination. The <a href="accuracy-93fdc24b.html">18 October accuracy update</a> corrects the gross-vs-MAGI shortcut, seasonal averaging and 2026/2027 FPL years. The <a href="flagged.html">Flagged hub</a> and <a href="audit-6fc18b58.html">independent audit</a> retain unresolved items and whole-site link exceptions. Older “verified” labels do not prove every inherited claim.</div>']
    for group, items in PAGE_INDEX:
        out.append('    <h4 class="index-group">{}</h4>'.format(esc(group)))
        out.append('    <ul class="index-list">')
        for href, label, desc in items:
            out.append('      <li><a href="{}">{}</a> <span class="muted">— {}</span></li>'.format(
                esc(href), esc(label), esc(desc)))
        out.append("    </ul>")
    out.append("  </div>")
    return "\n".join(out)


def patch_index(sources):
    """Publish the complete page index on the dashboard."""
    path = os.path.join(OUT, "index.html")
    if not os.path.exists(path):
        return False
    html = read(path)
    if is_core_generated(html):
        return False
    block = build_page_index_block()
    start = "<!-- PAGE-INDEX:START -->"
    end = "<!-- PAGE-INDEX:END -->"
    if start in html:
        html = patch_between(html, start, end, block)
    else:
        anchor = '<div class="footer">'
        if anchor not in html:
            return False
        html = html.replace(anchor, start + "\n" + block + "\n" + end + "\n\n" + anchor, 1)
    write(path, html)
    return True


def patch_flagged(sources):
    """Add the extended-analysis flagged items to the shared Flagged for Review
    page, keeping the items already published by the primary session."""
    path = os.path.join(OUT, "flagged.html")
    if not os.path.exists(path):
        return False
    html = read(path)
    if is_core_generated(html):
        return False
    flags = load_json("flagged.json")
    block = []
    block.append('<h3 class="section-title">🚩 Extended analysis — flagged items (W-01 to W-13)</h3>')
    block.append('<div class="alert warn">Independently authored extended-analysis flags. Some older wording is broader than the enacted MAGI-based methodology. If claims differ, the <a href="accuracy-93fdc24b.html">dated accuracy update</a> and newer official text govern the current guide.</div>')
    block.append('<p class="hint">{}</p>'.format(esc(flags["intro"])))
    block.append(render_flags(flags["items"], sources, id_prefix="W"))
    start = "<!-- EXTENDED-FLAGS:START -->"
    end = "<!-- EXTENDED-FLAGS:END -->"
    if start in html:
        html = patch_between(html, start, end, "\n".join(block))
    else:
        anchor = '<div class="footer">'
        if anchor not in html:
            return False
        html = html.replace(anchor, start + "\n" + "\n".join(block) + "\n" + end + "\n\n" + anchor, 1)
    write(path, html)
    return True


def main():
    sources = build_sources()
    written = []
    for slug, _label in EXT_NAV:
        written.append(build_page(slug, sources))

    nav_changed = patch_shared_nav()
    index_patched = patch_index(sources)
    flagged_patched = patch_flagged(sources)

    print("Built {} extended-analysis pages:".format(len(written)))
    for path in written:
        print("  " + os.path.relpath(path, ROOT))
    print("Shared pages updated: nav {} | dashboard index {} | flagged page {}".format(
        ", ".join(nav_changed) or "none",
        "yes" if index_patched else "no",
        "yes" if flagged_patched else "no",
    ))


if __name__ == "__main__":
    main()
