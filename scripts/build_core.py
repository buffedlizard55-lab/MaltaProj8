#!/usr/bin/env python3
"""
Build the primary, verified dashboard pages from data/core.json.

Outputs (repository root):
  index.html              — clean landing dashboard
  executive-summary.html  — executive summary, options, law, California actions
  work-rules.html         — the rule in detail, 9 practical pathways
  coverage-options.html   — every coverage option with income bands
  findings.html           — every finding in one filterable table + source register
  verification.html       — primary source register and corrections
  flagged.html            — open items, unknown values and archival link gaps
  archives.html           — index of the older detailed / supplementary sections

Every table row is generated from a record that names a source id. The build
fails if a record names a missing source, if a verified record has no value,
or if an unverified record has a value. Run scripts/check_core.py after this.

Usage: python3 scripts/build_core.py
"""

import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "core.json")

NAV = [
    ("index.html", "Dashboard"),
    ("executive-summary.html", "Executive Summary"),
    ("work-rules.html", "Work Rules"),
    ("coverage-options.html", "Coverage Options"),
    ("findings.html", "Findings"),
    ("verification.html", "Verification"),
    ("flagged.html", "Flagged for Review"),
]

STATUS = {
    "verified": ("Verified", "verified"),
    "verified-nuance": ("Verified — nuance", "verified"),
    "flagged": ("Flagged", "flagged"),
    "unverified": ("Unverified — blank", "flagged"),
    "given": ("Given by reader", "neutral"),
    "open": ("Open", "flagged"),
    "closed": ("Closed", "verified"),
}


def esc(value):
    return html.escape(str(value), quote=True)


def load():
    with open(DATA, "r", encoding="utf-8") as fh:
        return json.load(fh)


def check(data):
    sources = {s["id"]: s for s in data["sources"]}
    problems = []
    for section in ("key_numbers", "profile", "gates", "options", "pathways",
                    "findings", "ca_actions", "timeline", "flags", "action_plan"):
        for row in data[section]:
            sid = row.get("source")
            if sid and sid not in sources:
                problems.append(f"{section}/{row.get('id', row.get('fact', '?'))}: missing source {sid}")
            if not sid:
                problems.append(f"{section}/{row.get('id', row.get('fact', '?'))}: no source")
    for row in data["findings"]:
        if row["status"] == "verified" and not row.get("value"):
            problems.append(f"findings/{row['id']}: verified row has no value")
        if row["status"] == "unverified" and row.get("value"):
            problems.append(f"findings/{row['id']}: unverified row must be blank")
    return sources, problems


def badge(status):
    label, cls = STATUS.get(status, (status.title(), "neutral"))
    return f'<span class="status {cls}">{esc(label)}</span>'


def link(src):
    return (f'<a href="{esc(src["url"])}" target="_blank" rel="noopener">'
            f'{esc(src["short"])} ↗</a>')


def source_cell(sources, sid):
    src = sources[sid]
    return (f'<a href="{esc(src["url"])}" target="_blank" rel="noopener" '
            f'title="{esc(src["title"])}">{esc(src["short"])} ↗</a>')


def source_cells(sources, row):
    """Show every primary document named by a factual record."""
    return " · ".join(source_cell(sources, sid) for sid in
                      [row["source"], *row.get("also", [])])


def table(headers, rows, table_id=None, cls=""):
    tid = f' id="{table_id}"' if table_id else ""
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join('<tr class="row">' + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return (f'<div class="table-wrap"><table{tid} class="{cls}">'
            f"<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>")


def section(title, anchor, body, hint=""):
    hint_html = f'<p class="hint">{hint}</p>' if hint else ""
    return (f'<h2 class="section-title" id="{anchor}">{esc(title)}</h2>'
            f"{body}{hint_html}")


def page(title, subtitle, active, body, description=None, scripts=""):
    desc = description or subtitle
    links = []
    for href, label in NAV:
        active_attr = ' class="active"' if href == active else ""
        links.append(f'<a href="{href}"{active_attr}>{esc(label)}</a>')
    nav = "".join(links)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="stylesheet" href="site/assets/style.css">
</head>
<body>
<div class="topbar">
  <div class="topbar-inner">
    <div class="brand">
      <div class="brand-badge">CA</div>
      <div>
        <h1>California Healthcare &amp; Work Requirements</h1>
        <p>{esc(subtitle)}</p>
      </div>
    </div>
    <nav class="nav" aria-label="Main">{nav}</nav>
  </div>
</div>
{body}
<div class="footer">
  <p><strong>Source policy:</strong> every table row links to an official source
  (congress.gov, federalregister.gov, cms.gov, medicaid.gov, dhcs.ca.gov,
  aspe.hhs.gov, irs.gov, coveredca.com, cftc.gov, ca.gov). A value that could not
  be confirmed is left blank and flagged. <a href="findings.html">All findings</a> ·
  <a href="verification.html">Verification log</a> ·
  <a href="flagged.html">Flagged for Review</a> ·
  <a href="archives.html">Archive of detailed pages</a></p>
  <p>Research compilation, not legal, tax, or eligibility advice. County eligibility
  staff make the final determination. Data updated 2026-10-18. This page is
  generated from <a href="data/core.json">data/core.json</a>; do not hand-edit values.</p>
</div>
{scripts}
</body>
</html>
"""


def hero(title, eyebrow, lead, kpis, toc, side_cards, lead_html=None, sources=None):
    kpi_html = "".join(
        f'<div class="kpi"><div class="k">{esc(k["label"])}</div>'
        f'<div class="v">{esc(k["value"])}</div>'
        f'<div class="d">{esc(k["detail"])}{(" " + source_cells(sources, k)) if sources and k.get("source") else ""}</div></div>'
        for k in kpis
    )
    toc_html = "".join(f'<a href="#{esc(a)}">{esc(t)}</a>' for a, t in toc)
    side_html = "".join(
        f'<div class="mini">{c}</div>' for c in side_cards
    )
    lead_block = lead_html if lead_html is not None else f'<p class="lead">{esc(lead)}</p>'
    return f"""
<div class="hero">
  <div class="hero-card">
    <div class="eyebrow">{esc(eyebrow)}</div>
    <h2>{title}</h2>
    {lead_block}
    <div class="kpis">{kpi_html}</div>
    <div class="toc">{toc_html}</div>
  </div>
  <div class="hero-side">{side_html}</div>
</div>
"""


def category_cards():
    cards = [
        ("Executive Summary", "executive-summary.html", "The one-page answer, the exact law, your options, California's actions, and the action plan."),
        ("Work Rules", "work-rules.html", "Who is subject, 9 practical pathways for $0 earned income, the $580 test, verification, and the penalty."),
        ("Coverage Options", "coverage-options.html", "Medi-Cal, Covered California, Medicare, and community health centers, with income bands and costs."),
        ("All Findings", "findings.html", "Every finding in one filterable table, plus the full official-source register."),
        ("The Law — line by line", "law.html", "The detailed H.R.1 §71119 table: statutory text, dates, provisions, and citations."),
        ("California / Medi-Cal", "california.html", "DHCS implementation, timeline, exemptions, mitigation, and Covered California."),
        ("Income & MAGI", "income.html", "How rental, interest, and Kalshi income are counted — and what remains unresolved."),
        ("0-Earned Playbook", "pathways.html", "The original detailed playbook, retained as a reference and corrected where needed."),
        ("Verification Log", "verification.html", "The source register, corrections and review limitations."),
        ("Accuracy update", "accuracy-93fdc24b.html", "2026/2027 program-year thresholds, MAGI method and seasonal-worker statute."),
        ("Flagged for Review", "flagged.html", "Open irregularities, unverified values, and the questions the reader should raise with the county or a CPA."),
    ]
    body = "".join(
        f'<a class="card card-link" href="{href}"><h3>{esc(t)}</h3><p>{esc(d)}</p>'
        f'<span class="more">Open →</span></a>'
        for t, href, d in cards
    )
    return f'<div class="grid3">{body}</div>'


def dashboard(data, sources):
    top_findings = [f for f in data["findings"] if f["status"] in ("verified", "verified-nuance")][:12]
    finding_rows = [
        [f'<span class="tag">{esc(f["id"])}</span>', esc(f["category"]),
         f'<strong>{esc(f["finding"])}</strong><br><span class="subtle">{esc(f["detail"])}</span>',
         esc(f["value"]), source_cells(sources, f), badge(f["status"])]
        for f in top_findings
    ]
    path_rows = [
        [f'<span class="tag">{esc(p["id"])}</span>', f'<strong>{esc(p["path"])}</strong>',
         esc(p["what"]), esc(p["earned"]), esc(p["hours"]), esc(p["fit"]),
         source_cells(sources, p), badge(p["status"])]
        for p in data["pathways"]
    ]
    option_rows = [
        [f'<strong>{esc(o["option"])}</strong>', esc(o["who"]), esc(o["work_rule"]),
         esc(o["cost"]), esc(o["how"]), source_cells(sources, o), badge(o["status"])]
        for o in data["options"]
    ]
    profile_rows = [
        [esc(p["fact"]), esc(p["value"]) if p["value"] else '<em>blank</em>',
         esc(p["note"]), source_cells(sources, p), badge(p["status"])]
        for p in data["profile"]
    ]
    gate_cards = "".join(
        f'<div class="card"><div class="eyebrow">{esc(g["id"])}</div>'
        f'<h3>{esc(g["title"])}</h3><p>{esc(g["body"])}</p>'
        f'<p class="gate-yes"><strong>If yes:</strong> {esc(g["if_yes"])}</p>'
        f'<p class="gate-no"><strong>If no:</strong> {esc(g["if_no"])}</p>'
        f'<p class="hint">Source: {source_cell(sources, g["source"])}</p></div>'
        for g in data["gates"]
    )
    flag_rows = [
        [f'<span class="tag">{esc(f["id"])}</span>', f'<strong>{esc(f["item"])}</strong>',
         esc(f["issue"]), esc(f["impact"]), source_cells(sources, f), badge(f["status"])]
        for f in data["flags"] if f["status"] == "open"
    ][:8]

    lead_html = (
        '<p class="lead"><strong>Short answer:</strong> you do not need a W-2 to satisfy '
        'California\'s Medicaid work rule. There are <strong>three independent routes</strong>: '
        'document <strong>80 hours of qualifying work</strong> (CMS expressly counts property-management duties exchanged for free or reduced rent), show <strong>$580 of properly determined household MAGI-based monthly income</strong> '
        'in a qualifying month, or qualify for an <strong>exclusion or exemption</strong>. Which route fits you has not been established. If your MAGI is above '
        'the Medi-Cal limit, <strong>Covered California has no work requirement at all</strong>. '
        'Every row below links to an official source.</p>'
    )
    body = hero(
        "You can satisfy the work rule with $0 earned income — if you document the right route.",
        "Verified 2026-10-18 · H.R.1 §71119 · CMS-2454-IFC · DHCS ACWDL 25-30 / MEDIL I26-25",
        "",
        data["key_numbers"],
        [("answer", "Answer in 30 seconds"), ("gates", "Two gates"), ("paths", "9 pathways"),
         ("options", "Coverage options"), ("ca", "What California is doing"),
         ("findings", "Key findings"), ("flags", "Flagged items"), ("map", "Site map")],
        [
            '<span class="badge ok">Start here</span><h3 style="margin-top:10px">The two gates</h3>'
            '<p>First: are you in the Medi-Cal MAGI New Adult Group (income ≤ 138% FPL)? Second: can you show one qualifying month per renewal period? Most of the confusion disappears once you separate the two.</p>'
            '<p><a href="executive-summary.html">Read the executive summary →</a></p>',
            '<h3>The strongest route for a property manager</h3>'
            '<p>CMS\'s rule defines work to include in-kind work and gives the example of a property manager or building superintendent who receives free or reduced rent. Those hours count toward 80/month.</p>'
            '<p class="hint">42 CFR 435.552(b) · 91 FR 33348</p>',
            '<div class="alert warn" style="margin:0"><strong>The trap:</strong> if you fail the work rule, you are still deemed Medicaid-eligible and you are <strong>not</strong> eligible for federal premium tax credits. The fallback is not automatically Covered California with a subsidy.</div>',
        ],
        lead_html=lead_html,
        sources=sources,
    ) + f"""
<div class="wrap">
  <div class="card" id="answer" style="border-left:4px solid #2563eb">
    <h3>Your answer in 30 seconds</h3>
    <div class="grid3" style="margin-top:10px">
      <div><div class="eyebrow">Route 1 — strongest</div><h3>In-kind property-management work</h3>
      <p>If you perform property-management duties in exchange for free or reduced rent, CMS expressly counts those hours as work. Aim for 80 documented hours in a qualifying month. If you own the rental property, ask the county whether your actual management duties qualify; ownership alone is not proof. Keep a duty list, any rent-credit agreement, and a monthly log.</p>
      <p class="hint">{source_cell(sources, "S03")}</p></div>
      <div><div class="eyebrow">Route 2 — if countable</div><h3>$580 of household MAGI-based monthly income</h3>
      <p>DHCS's letter describes income from any source in a qualifying month, but later-enacted California law requires MAGI-based methods for your household budget. Countable rental and savings interest may help. Kalshi tax character, deductible expenses and your actual monthly amount are unknown; gross deposits or payouts alone do not show a pass.</p>
      <p class="hint">{source_cell(sources, "S42")} · {source_cell(sources, "S03")} · {source_cell(sources, "S10")}</p></div>
      <div><div class="eyebrow">Route 3 — fallback</div><h3>Exclusion, exemption, or 80 hours of activity</h3>
      <p>If neither route fits, the rule can be met with 80 hours of community service, a work program, at least half-time school, or a combination — or you may be excluded or exempt (age, disability, caregiving, Medicare, high-unemployment county).</p>
      <p class="hint">{source_cell(sources, "S09")}</p></div>
    </div>
    <div class="alert info" style="margin-top:12px"><strong>But first check Gate 1.</strong> Medi-Cal's MAGI New Adult Group is limited to household income at or below 138% FPL — $22,025/year or $1,836/month for one person in 2026. If your properly determined household MAGI is above that limit, this Medi-Cal work rule does not apply; Covered California has no work requirement. Your household size, rental net, interest and Kalshi tax amount were not supplied. The 2026 marketplace 400% FPL reference is $62,600 for one person; 2027 uses $63,840. See <a href="coverage-options.html">Coverage Options</a> and <a href="accuracy-93fdc24b.html">Accuracy update</a>.</div>
  </div>

  {section("The two gates — do them in order", "gates", f'<div class="grid2">{gate_cards}</div>', "Both gates must be true before the work rule applies. Gate 1 is an income test; Gate 2 is a work/income/exemption test.")}

  {section("Your profile — what is given and what is missing", "profile", table(
      ["Fact", "Value", "What it changes", "Official context (not proof of your facts)", "Status"],
      profile_rows,
      table_id="profile-table",
  ), "No personal eligibility value is inferred. The linked rule gives context, not independent proof of a reader-given fact. Blank cells are flagged; FPL examples use one person only as a reference.")}

  {section("9 practical pathways for $0 earned income", "paths", table(
      ["#", "Pathway", "What satisfies it", "Earned income?", "Hours", "Best fit", "Source", "Status"],
      path_rows,
      table_id="pathways-table",
  ), "The statute has five activity categories plus two income alternatives; the table separates the practical routes, including in-kind work, self-employment, and exemptions. Every row links to the official rule.")}

  {section("Every coverage option, side by side", "options", table(
      ["Option", "Who qualifies", "Work requirement", "Cost", "How to apply", "Source", "Status"],
      option_rows,
      table_id="options-table",
  ), "This table is about coverage, not just the work rule. If you are above 138% FPL, the relevant options are Covered California (no work requirement) and full-price coverage. If you are below, Medi-Cal is usually the lowest-cost option.")}

  {section("What California is doing for people with $0 earned income", "ca", table(
      ["#", "Action", "What it means", "Source", "Status"],
      [[f'<span class="tag">{esc(a["id"])}</span>', f'<strong>{esc(a["action"])}</strong>',
        esc(a["detail"]), source_cell(sources, a["source"]), badge(a["status"])]
       for a in data["ca_actions"]],
      table_id="ca-table",
  ), "California implements the federal rule; it does not waive it. The state help is in the income test, in-kind/self-employment work, community service, education, exclusions, outreach, ex parte verification, the 30-day cure, and the state premium subsidy for Covered California.")}

  {section("Key verified findings", "findings", table(
      ["ID", "Category", "Finding", "Verified value", "Source", "Status"],
      finding_rows,
      table_id="key-findings-table",
  ), 'This is a selection. <a href="findings.html">Open the full findings table →</a> (all ' + str(len(data["findings"])) + " findings, filterable, with the source register).")}

  {section("Flagged for review — read these before relying on the site", "flags", table(
      ["ID", "Item", "Issue", "Why it matters", "Source", "Status"],
      flag_rows,
      table_id="flags-table",
  ), 'These are the highest-impact open items. <a href="flagged.html">See the full Flagged for Review page →</a>')}

  {section("Site map — every category", "map", category_cards(), "The dashboard and six primary pages are the verified core. The older detailed pages and the three supplementary dashboards are preserved in the archive and are not re-certified by this session.")}
</div>
"""
    return page(
        "California Healthcare & Work Requirements — Verified 2026 Dashboard",
        "Verified dashboard — $0 earned income · Kalshi · rental · interest",
        "index.html",
        body,
        "Verified dashboard for a California resident with zero earned income: Medi-Cal work rules, in-kind property-management work, the $580 income test, Covered California, and every official source.",
        scripts='<script src="assets/site.js" defer></script>',
    )


def executive_summary(data, sources):
    law_rows = [
        ("Citation", "H.R.1, 119th Congress — Public Law 119-21, §71119, adding SSA §1902(xx)", "S01"),
        ("Signed", "July 4, 2025", "S01"),
        ("Federal effective date", "January 1, 2027, unless a state starts sooner or receives a good-faith waiver (latest December 31, 2028)", "S03"),
        ("Who is subject", "Non-pregnant adults 19–64 in the ACA adult group or certain section 1115 demonstrations providing minimum essential coverage, not entitled to or enrolled in Medicare", "S05"),
        ("Qualifying activities", "Work, community service, work program, at least half-time education, or a combination — at least 80 hours in the month", "S01"),
        ("Income alternative", "Monthly income at least the federal minimum wage × 80 hours = $580 in 2026", "S06"),
        ("Seasonal alternative", "Average monthly income over the preceding six months of at least $580 for a seasonal worker under IRC §45R(d)(5)(B)", "S06"),
        ("Who is excluded", "Former foster youth under 26; American Indians/Alaska Natives; parents/caretakers of a child 13 or younger or a disabled person; veterans with a total disability rating; medically frail; TANF/SNAP work-requirement compliance; SUD treatment; inmates; pregnant/postpartum", "S06"),
        ("Mandatory exceptions", "Under 19; Medicare Part A or B; another mandatory categorically needy group; recent inmate", "S07"),
        ("Hardship exceptions (state option)", "Inpatient/nursing facility/inpatient psychiatric care; medical travel; federally declared disaster county; county unemployment at or above the lesser of 8% or 1.5× the national rate", "S06"),
        ("Verification", "State must check all reliable information first; if it cannot verify, notice plus 30 calendar days to cure; coverage continues during cure", "S03"),
        ("Renewal standard", "One or more months between determinations; the months need not be consecutive", "S06"),
        ("Consequence", "Denial or disenrollment after cure. The person is still deemed Medicaid-eligible and is NOT eligible for federal premium tax credits", "S02"),
        ("Six-month renewals", "SSA §71107; policy effective January 1, 2027; California's first affected renewal dates begin March 1, 2027", "S11"),
        ("Cost sharing", "From October 1, 2028, up to $35 per service for some expansion enrollees above 100% FPL; primary care, mental health, SUD, FQHC, CCBHC and RHC excluded; prescriptions remain subject", "S02"),
        ("Territories", "Not subject", "S06"),
        ("Section 1115", "The requirement cannot be waived", "S06"),
    ]
    law_table = table(
        ["Item", "What the law says", "Source"],
        [[f"<strong>{esc(a)}</strong>", esc(b), source_cell(sources, c)] for a, b, c in law_rows],
        table_id="law-summary",
    )
    option_rows = [
        [f'<strong>{esc(o["option"])}</strong>', esc(o["who"]), esc(o["work_rule"]),
         esc(o["cost"]), esc(o["how"]), source_cells(sources, o), badge(o["status"])]
        for o in data["options"]
    ]
    action_rows = [
        [f'<span class="tag">{esc(a["id"])}</span>', f'<strong>{esc(a["action"])}</strong>',
         esc(a["detail"]), source_cell(sources, a["source"]), badge(a["status"])]
        for a in data["ca_actions"]
    ]
    plan_rows = [
        [f'<span class="tag">{esc(p["step"])}</span>', f'<strong>{esc(p["action"])}</strong>',
         esc(p["detail"]), source_cells(sources, p)]
        for p in data["action_plan"]
    ]
    open_flags = [f for f in data["flags"] if f["status"] == "open"]
    flag_rows = [
        [f'<span class="tag">{esc(f["id"])}</span>', esc(f["item"]), esc(f["issue"]),
         esc(f["impact"]), source_cells(sources, f), badge(f["status"])]
        for f in open_flags
    ]
    counts = {
        "total": len(data["findings"]),
        "verified": sum(1 for f in data["findings"] if f["status"] in ("verified", "verified-nuance")),
        "flagged": sum(1 for f in data["findings"] if f["status"] == "flagged"),
        "unverified": sum(1 for f in data["findings"] if f["status"] == "unverified"),
        "open_flags": len(open_flags),
        "sources": len(data["sources"]),
    }
    body = hero(
        "Executive summary: your options, the exact law, and what California is doing.",
        "Executive summary · verified 2026-10-18",
        "",
        data["key_numbers"][:4],
        [("bottom-line", "Bottom line"), ("profile", "Your profile"), ("gates2", "Two gates"),
         ("law", "The law"), ("options2", "Options"), ("routes", "Strongest routes"),
         ("california", "California actions"), ("risks", "Risks"), ("plan", "Action plan"),
         ("status", "Verification status"), ("sources", "Sources")],
        [
            '<span class="badge ok">Bottom line</span><h3 style="margin-top:10px">Several conditional routes</h3><p>CMS expressly counts qualifying in-kind property-management work. The income alternative requires $580 of monthly household income under MAGI-based methods. Exemptions, community service, school, and work programs are other possible paths; none is assumed for this reader.</p>',
            '<h3>What California is not doing</h3><p>California is not waiving the rule for people with zero earned income. It is implementing the federal rule and adding outreach, ex parte checks, a 30-day cure period, and a Covered California state subsidy.</p>',
            '<div class="alert warn" style="margin:0"><strong>The biggest risk is not the work itself.</strong> It is missing a renewal notice or failing to cure in 30 days. Keep your address current and open every county letter.</div>',
        ],
        lead_html='<p class="lead">This page answers four questions in order: (1) Are you in the Medi-Cal group the work rule applies to? (2) If yes, how can you satisfy it with zero earned income? (3) What are your coverage options if you are not in that group? (4) What is California actually doing to help? Every factual row links to an official source; unresolved items are flagged, not guessed.</p>',
        sources=sources,
    ) + f"""
<div class="wrap">
  {section("Bottom line", "bottom-line", f'''
  <div class="card">
    <ol class="big-list">
      <li><strong>Zero earned income is not zero MAGI.</strong> Countable net rental income and savings interest can matter. Whether and how Kalshi event-contract results enter this household’s MAGI budget is unresolved; a trading payout is not automatically income.</li>
      <li><strong>Gate 1 is the Medi-Cal income limit.</strong> For a one-person household in 2026, MAGI must be at or below $22,025/year ($1,836/month). MAGI Medi-Cal has no asset test. The reader’s household size and countable amount remain unknown.</li>
      <li><strong>Gate 2 is the community engagement rule.</strong> If you are in the affected group, you need one qualifying month per renewal period. CMS expressly counts property-management duties exchanged for free or reduced rent toward <strong>80 hours</strong>; owner-management alone needs county verification. Alternatively, enacted California law allows <strong>$580 of monthly income determined with household MAGI-based methods</strong>.</li>
      <li><strong>Covered California has no work requirement.</strong> If your MAGI is between 138% and 400% FPL, you may qualify for federal help and, at or below 165% FPL in 2026 / 200% FPL in 2027, a California state subsidy. Above 400% FPL, the federal credit is unavailable for 2026.</li>
      <li><strong>Failing the Medicaid work rule blocks marketplace subsidies.</strong> You are deemed Medicaid-eligible, so you cannot get federal premium tax credits. The fallback is cure, reapply, or pay full price.</li>
    </ol>
  </div>''')}

  {section("Your profile: what is given and what is missing", "profile", table(
      ["Fact", "Value", "What it changes", "Official context (not proof of your facts)", "Status"],
      [[esc(p["fact"]), esc(p["value"]) if p["value"] else "<em>blank</em>", esc(p["note"]), source_cells(sources, p), badge(p["status"])] for p in data["profile"]],
      table_id="profile-table-2",
  ), "The reader supplied citizenship, residence, work, trading, income sources, and zero earned income. Age, household size, exact amounts, disability/pregnancy status, county and current coverage were not supplied, so they are blank and flagged.")}

  {section("The two gates, in order", "gates2", ''.join(
      f'<div class="card" style="margin-bottom:12px"><div class="eyebrow">{esc(g["id"])}</div><h3>{esc(g["title"])}</h3><p>{esc(g["body"])}</p><p><strong>If yes:</strong> {esc(g["if_yes"])}</p><p><strong>If no:</strong> {esc(g["if_no"])}</p><p class="hint">Source: {source_cell(sources, g["source"])}</p></div>'
      for g in data["gates"]
  ))}

  {section("The exact law, line by line", "law", law_table, "This is a summary of the operative provisions. The detailed page contains the statutory subparagraphs and the CMS/California implementation citations: <a href='law.html'>The Law →</a>")}

  {section("Every coverage option", "options2", table(
      ["Option", "Who qualifies", "Work requirement", "Cost", "How to apply", "Source", "Status"],
      option_rows,
      table_id="options-table-2",
  ), "The work rule applies only to Medi-Cal's MAGI New Adult Group. Covered California, Medicare, and community health centers do not impose it.")}

  {section("Your strongest routes with zero earned income", "routes", f'''
  <div class="grid3">
    <div class="card"><div class="eyebrow">Route 1</div><h3>In-kind property-management work</h3>
    <p>CMS defines work to include work in exchange for goods or services, and gives the example of a property manager or building superintendent who receives free or reduced rent. The hours spent on those duties count toward 80 per month.</p>
    <p><strong>Keep:</strong> the lease or rent-credit agreement, a duty list, and a monthly hours log. Ask the county what else it wants.</p>
    <p class="hint">{source_cell(sources, "S03")}</p></div>
    <div class="card"><div class="eyebrow">Route 2</div><h3>$580 household MAGI-based income</h3>
    <p>DHCS's outreach letter says “income from any source” in one month since the last renewal. Enacted AB 2161 §14005.69(e)(6) requires MAGI-based financial methods for the individual’s household budget. Do not count gross rent, deposits or Kalshi payouts automatically.</p>
    <p><strong>Keep:</strong> rental and expense records, interest statements and full Kalshi transactions. Tax classification and exact income remain unknown.</p>
    <p class="hint">{source_cell(sources, "S42")} · {source_cell(sources, "S03")} · {source_cell(sources, "S10")}</p></div>
    <div class="card"><div class="eyebrow">Route 3</div><h3>Self-employment or fallback activity</h3>
    <p>DHCS lists self-employment as work. If owner-management is questioned, 80 hours of community service, a work program, half-time school, or a combination also satisfies the rule.</p>
    <p><strong>Keep:</strong> a contemporaneous log and a named contact for community service.</p>
    <p class="hint">{source_cell(sources, "S09")}</p></div>
  </div>''')}

  {section("What California is doing", "california", table(
      ["#", "Action", "What it means", "Source", "Status"],
      action_rows,
      table_id="ca-actions-2",
  ), "California implements the federal rule. It does not waive it for zero-earned-income adults. Its help is procedural and financial, not a blanket exemption.")}

  {section("What could go wrong — open flags", "risks", table(
      ["ID", "Item", "Issue", "Why it matters", "Source", "Status"],
      flag_rows,
      table_id="flags-table-2",
  ), 'The full list, including closed corrections, is on <a href="flagged.html">Flagged for Review</a>.')}

  {section("Action plan — no user input required to read this, but these are the steps at renewal", "plan", table(
      ["Step", "Action", "Detail", "Source"],
      plan_rows,
      table_id="action-plan-2",
  ), "This site cannot apply for you or access your accounts. It tells you what to keep and when to respond.")}

  {section("Verification status", "status", f'''
  <div class="kpis">
    <div class="kpi"><div class="k">Findings in this core dataset</div><div class="v">{counts["total"]}</div><div class="d">Every row names a source.</div></div>
    <div class="kpi"><div class="k">Verified or verified with nuance</div><div class="v">{counts["verified"]}</div><div class="d">Checked against an official source.</div></div>
    <div class="kpi"><div class="k">Flagged</div><div class="v">{counts["flagged"]}</div><div class="d">Official sources conflict or the point is unresolved.</div></div>
    <div class="kpi"><div class="k">Unverified — blank</div><div class="v">{counts["unverified"]}</div><div class="d">No official value located; left blank.</div></div>
    <div class="kpi"><div class="k">Open flags</div><div class="v">{counts["open_flags"]}</div><div class="d">Published on Flagged for Review.</div></div>
    <div class="kpi"><div class="k">Official sources</div><div class="v">{counts["sources"]}</div><div class="d">Full register on the Findings page.</div></div>
  </div>
  <div class="alert info" style="margin-top:12px">The later-enacted AB 2161 and CMS rule specify MAGI-based household methods and limit six-month averaging to seasonal workers; older DHCS letters use broader shorthand. Personal rental expenses, household composition, Kalshi tax character and January-vs-March DHCS timing remain visible as flags. See the <a href="accuracy-93fdc24b.html">dated accuracy update</a>.</div>''')}

  {section("Sources used on this page", "sources", table(
      ["ID", "Source", "Publisher", "Date", "Link"],
      [[esc(s["id"]), esc(s["title"]), esc(s["publisher"]), esc(s["date"]),
        f'<a href="{esc(s["url"])}" target="_blank" rel="noopener">Open ↗</a>']
       for s in data["sources"] if s["id"] in {x[2] for x in law_rows} | {o["source"] for o in data["options"]} | {a["source"] for a in data["ca_actions"]} | {p["source"] for p in data["action_plan"]} | {g["source"] for g in data["gates"]}],
      table_id="sources-2",
  ), 'The complete source register is on <a href="findings.html#sources">Findings → Source register</a>.')}
</div>
"""
    return page(
        "Executive Summary — California Healthcare & Work Requirements",
        "Executive summary · the law · your options · California actions",
        "executive-summary.html",
        body,
        "Executive summary of California Medi-Cal work requirements for a zero-earned-income resident: the exact H.R.1 §71119 rule, nine pathways, coverage options, California actions, risks, and an action plan.",
    )


def work_rules(data, sources):
    path_rows = [
        [f'<span class="tag">{esc(p["id"])}</span>', f'<strong>{esc(p["path"])}</strong><br><span class="subtle">{esc(p["statute"])}</span>',
         esc(p["what"]), esc(p["earned"]), esc(p["hours"]), esc(p["fit"]), esc(p["note"]),
         source_cells(sources, p), badge(p["status"])]
        for p in data["pathways"]
    ]
    timeline_rows = [
        [f'<strong>{esc(t["date"])}</strong>', esc(t["event"]), source_cell(sources, t["source"])]
        for t in data["timeline"]
    ]
    subject_rows = [
        ("Applies to", "Non-pregnant adults 19–64 in the Medi-Cal MAGI New Adult Group (aid code M1) or certain section 1115 demonstrations providing minimum essential coverage, who are not entitled to or enrolled in Medicare.", "S05"),
        ("Does not apply to", "Children, adults 65+, pregnant/postpartum people, people eligible through aged/blind/disabled pathways, and Medicare beneficiaries.", "S11"),
        ("Excluded (not an applicable individual)", "Former foster youth under 26; American Indians/Alaska Natives; parents/caretakers of a child 13 or younger or a disabled person; veterans with a total disability rating; medically frail; TANF/SNAP work-requirement compliance; SUD treatment participants; inmates; pregnant/postpartum people.", "S06"),
        ("Mandatory exceptions", "Under 19; Medicare Part A or B; another mandatory categorically needy group; recent inmate (within the 3-month period).", "S07"),
        ("Short-term hardship (state option; California lists them)", "Inpatient hospital, nursing facility, ICF/IID or inpatient psychiatric care; travel outside the community for serious or complex medical care; federally declared disaster county; county unemployment at or above the lesser of 8% or 1.5× the national rate.", "S09"),
        ("Personal facts not supplied", "Age, household size, county, pregnancy/disability status, and Medicare status. These determine whether you are subject, excluded, or exempt. Blank and flagged.", "S16"),
    ]
    subject_table = table(
        ["Category", "Who", "Source"],
        [[f"<strong>{esc(a)}</strong>", esc(b), source_cell(sources, c)] for a, b, c in subject_rows],
        table_id="subject-table",
    )
    income_rows = [
        ("Net rental income (Schedule E)", "Counts in MAGI", "IRS Pub 527; 42 CFR 435.603", "S27"),
        ("Gross rent receipts", "Do not equate deposits with countable income; enacted AB 2161 requires MAGI-based household financial methods.", "WIC §14005.69(e)(6); IRS Pub 527", "S42"),
        ("Taxable interest", "Counts if included in household MAGI", "42 CFR 435.603; HealthCare.gov", "S33"),
        ("Tax-exempt interest", "Added back for MAGI where applicable", "42 CFR 435.603; HealthCare.gov", "S32"),
        ("Kalshi event contracts", "Individual tax character and countable amount unknown — a gross payout is not an established MAGI value", "General IRS rules are not a Kalshi-specific classification", "S29"),
        ("Trading losses", "Deductibility and netting depend on the federal tax character of these particular contracts", "IRS Topic 409; H.R.1 §70114 (conditional wagering treatment)", "S30"),
        ("Unemployment, SDI, retirement, dividends", "The preliminary DHCS letter lists these as possible sources; apply the enacted household MAGI method", "AB 2161 §14005.69(e)(6)", "S42"),
        ("Assets (rental property, savings principal)", "No property/resource test for MAGI Medi-Cal; non-MAGI pathways can differ", "42 CFR 435.603(g)", "S33"),
        ("Taxable lump sum", "Generally counted in the month received; this does not classify every Kalshi payout", "42 CFR 435.603(e)(1)", "S33"),
        ("Gifts, loans, credit-card rewards", "", "No uniform treatment was established by the ACWDL’s omission; leave person-specific value blank", "S33"),
    ]
    income_table = table(
        ["Income type", "How it is treated", "Authority", "Source"],
        [[f"<strong>{esc(a)}</strong>", esc(b), esc(c), source_cell(sources, d)] for a, b, c, d in income_rows],
        table_id="income-table",
    )
    verify_rows = [
        ("Application look-back", "The month immediately before the month of application. States may require up to three consecutive months; California's ACWDL uses the month before application.", "S06"),
        ("Renewal look-back", "One or more months between determinations; the months do not have to be consecutive. One qualifying month is enough.", "S09"),
        ("Ex parte first", "The state must check all reliable information available to it before requesting documents from the individual.", "S04"),
        ("Notice and cure", "If the state cannot verify, it must send a notice and allow 30 calendar days to demonstrate compliance or an exemption. Services continue during the cure period.", "S03"),
        ("Documentation from 2028", "Beginning January 1, 2028, documentation must be required when reasonably available. Through 2027 states have flexibility.", "S04"),
        ("More frequent checks", "States may verify more often than at renewal, at their option.", "S03"),
        ("Reapplication", "A disenrolled person may reapply at any time and will be assessed for compliance on reapplication.", "S05"),
    ]
    verify_table = table(
        ["Stage", "Rule", "Source"],
        [[f"<strong>{esc(a)}</strong>", esc(b), source_cell(sources, c)] for a, b, c in verify_rows],
        table_id="verify-table",
    )
    body = hero(
        "The work rule in detail — and nine ways to satisfy it with zero earned income.",
        "Work rules · H.R.1 §71119 · 42 CFR 435.550–435.563 · DHCS ACWDL 25-30",
        "",
        data["key_numbers"][2:],
        [("who", "Who is subject"), ("paths2", "9 pathways"), ("income", "$580 and MAGI"),
         ("verify", "Verification and cure"), ("penalty", "Penalty"), ("dates", "California dates"),
         ("quotes", "Official quotes"), ("flags2", "Open flags")],
        [
            '<span class="badge ok">Key distinction</span><h3 style="margin-top:10px">Work hours ≠ earned income</h3><p>The Medicaid rule counts <em>work</em>, including in-kind and unpaid work. It does not require a W-2 or a paycheck. That is why a property manager with zero earned income can still satisfy an 80-hour work test.</p>',
            '<h3>One month is enough</h3><p>At renewal, California asks whether you met the rule in <em>any</em> month since the last determination. The months do not have to be consecutive. This is more forgiving than a continuous 80-hours-every-month rule.</p>',
            '<div class="alert warn" style="margin:0"><strong>Do not confuse the two tests.</strong> The 138% FPL test helps decide whether you qualify for MAGI Medi-Cal. The $580 income alternative is one way to meet the separate work rule if it applies. A high-income month can affect both, in opposite directions.</div>',
        ],
        lead_html='<p class="lead">This page separates the eligibility test from the work test, lists every practical pathway, explains what income counts, and shows exactly how California verifies and cures. Where the federal and state sources differ, the row is flagged rather than smoothed over.</p>',
        sources=sources,
    ) + f"""
<div class="wrap">
  {section("Who is subject — and who is not", "who", subject_table, "The rule is narrow. It applies to the MAGI New Adult Group, not to all Medi-Cal. If you are 65+, disabled, pregnant, or on Medicare, a different set of rules applies.")}

  {section("Nine practical pathways", "paths2", table(
      ["#", "Pathway", "What satisfies it", "Earned income?", "Hours", "Best fit", "Note / documentation", "Source", "Status"],
      path_rows,
      table_id="pathways-table-2",
  ), "Pathways 1–3 are the best fit for a property manager / Kalshi trader with zero earned income. Pathways 4–9 are fallbacks or personal exemptions.")}

  {section("The $580 test and MAGI — what counts", "income", income_table, "Use enacted California AB 2161 §14005.69(e)(6) and the CMS rule: monthly household MAGI-based financial methods, not the preliminary ACWDL's broad gross-income phrase. The reader's allowable rental expenses and Kalshi tax result remain unverified.")}

  {section("Verification, notice, and the 30-day cure", "verify", verify_table, "The cure period is the most important protection. If you receive a notice, respond within 30 days; coverage continues while you cure.")}

  {section("What happens if you do not comply", "penalty", f'''
  <div class="alert warn"><strong>Two consequences, not one.</strong> After the cure period, the state may deny or disenroll you. Separately, a person who does not comply is still deemed Medicaid-eligible, which means they are <strong>not eligible for federal premium tax credits</strong> to buy a marketplace plan. You can reapply for Medicaid at any time.</div>
  <div class="card" style="margin-top:12px"><h3>Why this matters for a Kalshi trader</h3><p>Trading amounts are not fixed wages; tax characterization and household MAGI are unknown. A low-income month does not itself establish the $580 alternative, and MAGI Medi-Cal has no asset test. Document a qualifying month of actual activity, an allowed MAGI-based income result, or a valid exemption for each applicable renewal period; confirm your own facts with the county.</p>
  <p class="hint">Sources: {source_cell(sources, "S02")} · {source_cell(sources, "S05")}</p></div>''')}

  {section("California dates and timeline", "dates", table(
      ["Date", "Event", "Source"],
      timeline_rows,
      table_id="timeline-table",
  ), "The work rule starts January 1, 2027. Six-month renewals are effective January 1, 2027, but the first affected renewal dates begin March 1, 2027. The DHCS member letter's “March 2027” wording is flagged.")}

  {section("Official quotes to check yourself", "quotes", f'''
  <div class="card">
    <h3>In-kind work — CMS IFR, 91 FR 33348</h3>
    <blockquote>“There are jobs in various sectors, ranging from domestic service to specialized facility management, where individuals may choose to accept in-kind compensation in the form of non-monetary benefits like housing, meals, or utilities. For example, an individual who performs duties as a property manager or building superintendent may receive compensation in the form of free or reduced rent. Under our definition of work at § 435.552(b), the hours the individual spends performing these duties would count toward meeting the 80-hour requirement.”</blockquote>
    <p class="hint">{source_cell(sources, "S03")}</p>
    <h3 style="margin-top:16px">Income from any source — DHCS MEDIL I26-25</h3>
    <blockquote>“Have an income from any source of at least $580 (before taxes) in any month since your last renewal.”</blockquote>
    <p class="hint">{source_cell(sources, "S10")}</p>
    <h3 style="margin-top:16px">Earlier preliminary total-gross wording — DHCS ACWDL 25-30</h3>
    <blockquote>“An individual's total gross income for a month must meet or exceed this amount.”</blockquote>
    <p class="hint">This preliminary letter predates the enacted California income method; do not use the quotation alone to count gross rents or payouts. {source_cell(sources, "S09")}</p>
    <h3 style="margin-top:16px">Enacted California household MAGI method — AB 2161 §14005.69(e)(6)–(7)</h3>
    <blockquote>“The individual has a total monthly income, using modified adjusted gross income (MAGI)-based financial methods ... for their individual MAGI-based household budget” of at least 80 times the applicable minimum wage. The six-month alternative also requires that the individual “is a seasonal worker.”</blockquote>
    <p class="hint">{source_cell(sources, "S42")}</p>
    <h3 style="margin-top:16px">MAGI-based monthly household income — CMS IFR slides</h3>
    <blockquote>“States must use an individual's modified adjusted gross income (MAGI)-based monthly household income for Medicaid to determine compliance with the community engagement requirement (i.e., generally the same income methodology used to determine financial eligibility).”</blockquote>
    <p class="hint">{source_cell(sources, "S07")}</p>
  </div>''')}

  {section("Open flags on the work rules", "flags2", table(
      ["ID", "Item", "Issue", "Why it matters", "Source", "Status"],
      [[f'<span class="tag">{esc(f["id"])}</span>', esc(f["item"]), esc(f["issue"]), esc(f["impact"]),
        source_cells(sources, f), badge(f["status"])]
       for f in data["flags"] if f["status"] != "closed" and f["id"] in
       {"FL-02","FL-03","FL-04","FL-05","FL-07","FL-08","FL-09","FL-10","FL-11","FL-12","FL-17","FL-18","FL-19","FL-21"}],
      table_id="flags-table-3",
  ), 'The full list is on <a href="flagged.html">Flagged for Review</a>.')}
</div>
"""
    return page(
        "Work Rules — California Medi-Cal Community Engagement",
        "Work rules · 9 pathways · $580 test · verification",
        "work-rules.html",
        body,
        "Detailed verified guide to the Medi-Cal community engagement rule: who is subject, nine pathways for zero earned income, what income counts, verification, the 30-day cure, and California dates.",
    )


def coverage_options(data, sources):
    option_rows = [
        [f'<strong>{esc(o["option"])}</strong>', esc(o["who"]), esc(o["work_rule"]),
         esc(o["cost"]), esc(o["how"]), source_cells(sources, o), badge(o["status"])]
        for o in data["options"]
    ]
    # Program-year and poverty-guideline year are not interchangeable:
    # 2026 Medi-Cal uses 2026 FPL; 2026 Covered California uses 2025 FPL.
    band_data = [
        ("2026 Medi-Cal", "100% FPL (2026 reference)", "$15,960", "$1,330", "Guideline used for the current-year Medi-Cal calculation, not the marketplace 2026 100% reference.", "S17"),
        ("2026 Medi-Cal", "138% FPL (2026 reference)", "$22,025", "$1,836", "One-person adult expansion upper limit published by DHCS; household and monthly income must be checked.", "S15"),
        ("2026 Covered California", "400% FPL (2025 reference)", "$62,600", "", "Official plan-year 2026 single-person federal PTC upper income reference; other eligibility rules still apply.", "S41"),
        ("2027 Covered California", "400% FPL (2026 reference)", "$63,840", "", "Marketplace plan-year 2027 reference. This is not a 2027 Medi-Cal amount.", "S43"),
        ("2027 Medi-Cal", "138% FPL (current-year reference)", "", "", "Not established by the 2026 DHCS chart; future guideline and household facts remain unconfirmed. Flag FL-26.", "S15"),
    ]
    bands = table(
        ["Program / coverage year", "FPL basis", "Annual", "Monthly", "Meaning", "Official source"],
        [[esc(year), esc(fpl), esc(annual) if annual else '<em>blank — flagged</em>',
          esc(monthly) if monthly else '<em>blank — not published here</em>', esc(note), source_cell(sources, sid)]
         for year, fpl, annual, monthly, note, sid in band_data],
        table_id="bands-table",
    )
    aptc_data = [
        ("Under 138%", "2.10% (generally Medi-Cal instead)"),
        ("138% – under 150%", "3.14% – 4.19%"),
        ("150% – under 165%", "4.19% – 4.91%"),
        ("165% – under 200%", "4.91% – 6.60%"),
        ("200% – under 250%", "6.60% – 8.44%"),
        ("250% – under 300%", "8.44% – 9.96%"),
        ("300% – 400%", "9.96%"),
        ("Above 400%", "No federal premium tax credit for 2026"),
    ]
    aptc = table(
        ["Household income (% FPL), 2026", "Federal applicable percentage for benchmark Silver", "Official source"],
        [[esc(band), esc(share), source_cell(sources, "S18")] for band, share in aptc_data],
        table_id="aptc-table",
    )
    state_data = [
        ("2026", "At or below 165% FPL", "0% below 150% FPL; 3.19% – 3.91% from 150% to 165%", "S18"),
        ("2027", "Up to 200% FPL", "2.8% – 5.28% from above 150% to 200%", "S20"),
    ]
    state = table(
        ["Coverage year", "California state subsidy", "Applicable percentage for state subsidy", "Official source"],
        [[esc(year), esc(band), esc(share), source_cell(sources, sid)] for year, band, share, sid in state_data],
        table_id="state-table",
    )
    body = hero(
        "Every coverage option — and which ones have a work requirement.",
        "Coverage options · Medi-Cal · Covered California · Medicare · community health centers",
        "",
        data["key_numbers"],
        [("bands", "Income bands"), ("options3", "Options"), ("aptc", "Federal help"),
         ("state", "California subsidy"), ("fail", "If you fail the work rule"),
         ("above", "If you are above 138% FPL"), ("sources3", "Sources")],
        [
            '<span class="badge ok">First question</span><h3 style="margin-top:10px">Which program are you in?</h3><p>The MAGI New Adult Group generally uses up to 138% FPL. Marketplace financial help is conditional on income and other eligibility rules; 2026 and 2027 use different FPL references. The work rule applies only to affected Medicaid adults.</p>',
            '<h3>No work requirement outside Medi-Cal</h3><p>Covered California, Medicare, and community health centers do not impose the community engagement rule.</p>',
            '<div class="alert warn" style="margin:0"><strong>Do not assume you can fail Medi-Cal and get a subsidy.</strong> Failing the work rule makes you deemed Medicaid-eligible and blocks federal premium tax credits.</div>',
        ],
        lead_html='<p class="lead">This page is a decision table, not a quote engine. It shows the published income bands, the 2026 federal premium-tax-credit percentages, the California state subsidy for 2026 and 2027, and the work-rule status of each option. Where an official dollar figure does not exist, the cell is blank and flagged.</p>',
        sources=sources,
    ) + f"""
<div class="wrap">
  {section("Published income bands — one-person reference, separate program years", "bands", bands, "2026 Medi-Cal and 2026 marketplace use different FPL years. The 2027 Medi-Cal amount and this person’s household size are unknown; blank is not zero. Consult the dated official program charts.")}

  {section("Every option, side by side", "options3", table(
      ["Option", "Who qualifies", "Work requirement", "Cost", "How to apply", "Source", "Status"],
      option_rows,
      table_id="options-table-3",
  ), "Medi-Cal and Covered California are the two main paths. Medicare and community health centers matter if you are 65+/disabled or need care regardless of insurance.")}

  {section("Federal premium tax credit percentages for 2026", "aptc", aptc, "These are the federal applicable percentages before the California state subsidy. The enhanced federal credits expired December 31, 2025, and the 400% cliff returned for 2026.")}

  {section("California state premium subsidy", "state", state, "The state subsidy is available only through Covered California's subsidized application and only if the person is otherwise eligible for the federal premium tax credit.")}

  {section("If you fail the Medicaid work rule", "fail", f'''
  <div class="alert warn"><strong>You do not automatically fall into a subsidized marketplace plan.</strong> The statute deems a noncompliant person Medicaid-eligible and makes them ineligible for federal premium tax credits. The practical options are: cure within 30 days, reapply for Medicaid when you can show compliance, or buy a plan at full price. This is the single most important reason to keep at least one qualifying month per renewal period.</div>
  <p class="hint" style="margin-top:8px">Sources: {source_cell(sources, "S02")} · {source_cell(sources, "S05")}</p>''')}

  {section("If your MAGI is above 138% FPL", "above", f'''
  <div class="card">
    <p>You are not in the Medi-Cal MAGI New Adult Group, so the community engagement rule does not apply to you. The relevant question becomes marketplace financial help:</p>
    <ul>
      <li><strong>100%–400% FPL:</strong> Covered California with the federal premium tax credit; the 2026 applicable percentage ranges from 2.10% to 9.96% of household income for the benchmark Silver plan.</li>
      <li><strong>At or below 165% FPL in 2026 / 200% FPL in 2027:</strong> the California state subsidy may further reduce your share.</li>
      <li><strong>Above 400% FPL:</strong> no federal premium tax credit for 2026. You can still buy a plan at full price; the site does not estimate the premium because it varies by age, region, plan and tobacco use.</li>
    </ul>
    <p class="hint">Sources: {source_cell(sources, "S18")} · {source_cell(sources, "S19")} · {source_cell(sources, "S20")} · {source_cell(sources, "S41")} · {source_cell(sources, "S43")}</p>
  </div>''')}

  {section("Sources", "sources3", table(
      ["ID", "Source", "Publisher", "Date", "Link"],
      [[esc(s["id"]), esc(s["title"]), esc(s["publisher"]), esc(s["date"]),
        f'<a href="{esc(s["url"])}" target="_blank" rel="noopener">Open ↗</a>']
       for s in data["sources"] if s["id"] in {"S15","S16","S17","S18","S19","S20","S40","S05","S02","S41","S42","S43"}],
      table_id="sources-3",
  ), 'Full register: <a href="findings.html#sources">Findings → Source register</a>.')}
</div>
"""
    return page(
        "Coverage Options — Medi-Cal, Covered California, Medicare",
        "Coverage options · income bands · federal and state help",
        "coverage-options.html",
        body,
        "Every California coverage option for a zero-earned-income resident: Medi-Cal, Covered California with and without subsidies, Medicare, and community health centers, with published income bands and work-rule status.",
    )


def findings_page(data, sources):
    rows = [
        [f'<span class="tag">{esc(f["id"])}</span>', esc(f["category"]),
         f'<strong>{esc(f["finding"])}</strong><br><span class="subtle">{esc(f["detail"])}</span>',
         esc(f["value"]) if f["value"] else '<em>blank — no official value located</em>',
         source_cells(sources, f), badge(f["status"])]
        for f in data["findings"]
    ]
    counts = {
        "total": len(data["findings"]),
        "verified": sum(1 for f in data["findings"] if f["status"] in ("verified", "verified-nuance")),
        "flagged": sum(1 for f in data["findings"] if f["status"] == "flagged"),
        "unverified": sum(1 for f in data["findings"] if f["status"] == "unverified"),
    }
    source_rows = [
        [esc(s["id"]), esc(s["title"]), esc(s["publisher"]), esc(s["date"]),
         f'<a href="{esc(s["url"])}" target="_blank" rel="noopener">Open ↗</a>',
         "Yes" if s.get("official") else "No"]
        for s in data["sources"]
    ]
    body = hero(
        "All findings — one table, every source, no inferred values.",
        f"{counts['total']} findings · {counts['verified']} verified · {counts['flagged']} flagged · {counts['unverified']} unverified",
        "",
        [
            {"label": "Findings", "value": str(counts["total"]), "detail": "Each row names a source id."},
            {"label": "Verified", "value": str(counts["verified"]), "detail": "Checked against an official source."},
            {"label": "Flagged", "value": str(counts["flagged"]), "detail": "Official sources conflict or the point is unresolved."},
            {"label": "Unverified", "value": str(counts["unverified"]), "detail": "Value left blank."},
        ],
        [("findings-table", "Filterable findings"), ("sources", "Source register"), ("method", "Method")],
        [
            '<span class="badge ok">How to read this</span><h3 style="margin-top:10px">Four statuses</h3><p><strong>Verified</strong> — the value matches an official source. <strong>Verified — nuance</strong> — the value is official but a related point is unresolved. <strong>Flagged</strong> — official sources conflict or the law is unsettled. <strong>Unverified — blank</strong> — no official value was located; the value is blank.</p>',
            '<h3>Source rule</h3><p>Every row links to congress.gov, federalregister.gov, cms.gov, medicaid.gov, dhcs.ca.gov, aspe.hhs.gov, irs.gov, coveredca.com, cftc.gov, or another official government domain. Third-party commentary is not used to fill a value.</p>',
            '<div class="alert info" style="margin:0">The filter searches the visible table text. It works without JavaScript as a full table; the search box is an enhancement.</div>',
        ],
        lead_html='<p class="lead">This is the audit trail. Every substantive claim on the dashboard and the category pages appears here with its verified value, its official source, and a status. The table is generated from <a href="data/core.json">data/core.json</a>; the build fails if a row names a missing source or if an unverified row carries a value.</p>',
    ) + f"""
<div class="wrap">
  {section("Filterable findings", "findings-table", f'''
  <div class="table-tools">
    <label for="findings-filter"><strong>Filter</strong>
      <input id="findings-filter" type="search" placeholder="Try: Kalshi, rental, six-month, exemption…" data-filter-for="all-findings">
    </label>
    <span class="subtle" data-count-for="all-findings"></span>
  </div>
  ''' + table(
      ["ID", "Category", "Finding and detail", "Verified value", "Source", "Status"],
      rows,
      table_id="all-findings",
  ), "Rows with a blank value are unverified. Rows marked flagged have an official source but a conflict or open legal question.")}

  {section("Source register", "sources", table(
      ["ID", "Source", "Publisher", "Date", "Link", "Official"],
      source_rows,
      table_id="source-register",
  ), "All sources are on official government or state-exchange domains. The register includes the exact document title, publisher, and date so each can be checked manually.")}

  {section("Method and limitations", "method", f'''
  <div class="card">
    <h3>What was checked</h3>
    <ul>
      <li>The statute and CRS summary for the rule, effective date, activities, income test, exemptions, penalties and six-month renewals.</li>
      <li>The CMS interim final rule, its June 29, 2026 correction, the CMS fact sheet, the December 2025 CIB, and the July 2026 IFR slide deck for the federal implementation details, including in-kind work and the MAGI income methodology.</li>
      <li>DHCS ACWDL 25-30, MEDIL I26-25, the 2026 FPL letters and charts, the Medi-Cal Changes page, the Tracking page, and the H.R.1 implementation plan for California's dates, income test, exemptions and outreach.</li>
      <li>Covered California's 2026 Open Enrollment financial details ($62,600) and 2027 FPL chart ($63,840); the applicable FPL reference years differ from current-year Medi-Cal.</li>
      <li>IRS publications and 42 CFR 435.603 for MAGI, rental, interest, capital gains and the no-asset-test rule.</li>
      <li>IRS recordkeeping guidance supports keeping complete transactions. The form, if any, issued for these contracts is unknown and left blank.</li>
    </ul>
    <h3>What was not done</h3>
    <ul>
      <li>No personal eligibility determination. Age, household size, county, income amounts, disability/pregnancy status and current coverage were not supplied.</li>
      <li>No tax return, account access, or Kalshi account data was used.</li>
      <li>No legal advice on the Kalshi classification. The site flags the unresolved question and recommends a CPA.</li>
      <li>No full end-to-end audit of the 135-page IFR; the relevant sections were checked against the Federal Register text and the CMS summary deck.</li>
      <li>The older detailed pages and the three supplementary dashboards were preserved, not re-certified line by line by this session.</li>
    </ul>
    <p class="hint">Generated from <a href="data/core.json">data/core.json</a> by <code>scripts/build_core.py</code>. Run <code>python3 scripts/check_core.py</code> to re-validate.</p>
  </div>''')}
</div>
"""
    return page(
        "All Findings — Verified Source Table",
        f"{counts['total']} findings · {counts['verified']} verified · {counts['flagged']} flagged",
        "findings.html",
        body,
        "Every finding in the California healthcare work-requirements research, with verified values, official source links, status labels, and the full source register.",
        scripts='<script src="assets/site.js" defer></script>',
    )


def archives(data, sources):
    sections = [
        ("Current primary guide and accuracy update", "Current", [
            ("index.html", "Dashboard"),
            ("executive-summary.html", "Executive Summary"),
            ("work-rules.html", "Work Rules"),
            ("coverage-options.html", "Coverage Options"),
            ("findings.html", "All Findings"),
            ("verification.html", "Verification log"),
            ("flagged.html", "Flagged for Review"),
            ("archives.html", "Archive (this page)"),
            ("accuracy-93fdc24b.html", "Dated accuracy update"),
        ], "Eight pages generated from data/core.json plus a dated accuracy supplement. High-impact amounts and rules were rechecked; source presence does not certify every inherited claim or URL uptime."),
        ("Detailed reference pages", "Preserved", [
            ("law.html", "The Law — line by line"),
            ("california.html", "California / Medi-Cal"),
            ("income.html", "Income & MAGI"),
            ("pathways.html", "0-Earned Playbook"),
            ("exemptions.html", "Exemptions"),
            ("verification-detailed.html", "Verification log (detail, superseded)"),
            ("flagged-detailed.html", "Flagged for Review (detail, superseded)"),
        ], "Earlier sessions' pages. Preserved and patched for navigation; key factual corrections are logged in verification.html and flagged.html. Not re-certified row by row by this session."),
        ("Extended analysis", "Preserved", [
            ("overview.html", "Overview"),
            ("options.html", "Options"),
            ("work-requirements.html", "Work requirements"),
            ("income-counting.html", "Income counting"),
            ("medicaid-eligibility.html", "Medicaid eligibility"),
            ("covered-california.html", "Covered California"),
            ("immigration-status.html", "Immigration status"),
            ("california-changes.html", "California changes"),
            ("timeline.html", "Timeline"),
            ("apply.html", "How to apply"),
            ("sources.html", "Source register"),
        ], "Generated by scripts/build_site.py from data/page-*.json and data/entries-*.json. Preserved as a detailed reference."),
        ("Supplementary dashboards", "Preserved", [
            ("research/index.html", "Research dashboard (9 pages)"),
            ("coverage-guide/index.html", "Coverage guide (7 pages)"),
            ("docs/index.html", "Docs dashboard (10 pages)"),
            ("audit-6fc18b58.html", "Independent audit (6fc18b58)"),
            ("verify-5bf2fb99.html", "Independent check (5bf2fb99)"),
            ("verify-9285d712.html", "Independent check (9285d712)"),
            ("verify-95219c64.html", "Independent check (95219c64)"),
            ("verify-a9c46f9b.html", "Independent check (a9c46f9b)"),
        ], "Preserved supplementary material; compare disputed claims with the dated accuracy update and current primary pages."),
    ]
    blocks = ""
    for title, status, pages, note in sections:
        rows = "".join(
            f'<li><a href="{esc(href)}">{esc(label)}</a> <span class="subtle">— {esc(href)}</span></li>'
            for href, label in pages
        )
        first = ' id="archive"' if not blocks else ""
        blocks += f"""
  <h2 class="section-title"{first}>{esc(title)} <span class="badge neutral">{esc(status)}</span></h2>
  <div class="card" style="margin-bottom:12px"><p>{esc(note)}</p></div>
  <div class="card"><ul class="big-list">{rows}</ul></div>
"""
    body = hero(
        "Archive — every page, clearly labelled by status.",
        "Archive · preserved detailed pages and supplementary dashboards",
        "",
        [
            {"label": "Current entry points", "value": "9", "detail": "Eight generated core pages plus the dated accuracy update."},
            {"label": "Detailed reference pages", "value": "7", "detail": "Preserved; two are the superseded originals."},
            {"label": "Extended analysis pages", "value": "11", "detail": "Preserved generated reference."},
            {"label": "Supplementary sections", "value": "8 pages", "detail": "Research, coverage guide, docs, and five independent checks."},
        ],
        [("archive", "Page index"), ("build", "Build and verification"), ("policy", "Status policy")],
        [
            '<span class="badge ok">Nothing was deleted</span><h3 style="margin-top:10px">Earlier research preserved</h3><p>The current dashboard and dated accuracy update are the starting points. Detailed pages and supplementary dashboards remain reachable here with explicit status and link-gap cautions.</p>',
            '<h3>Why an archive?</h3><p>The earlier pages are useful detail, but they were written at different times and some contained errors. The core pages correct the highest-impact ones; the archive lets you inspect the original reasoning without treating every row as newly certified.</p>',
            '<div class="alert info" style="margin:0">If a detailed page conflicts with a core page, the core page and the official source control. The conflict should be logged on <a href="flagged.html">Flagged for Review</a>.</div>',
        ],
        lead_html='<p class="lead">This is the whole-site map. The primary pages are generated from <code>data/core.json</code>; the <a href="accuracy-93fdc24b.html">dated accuracy update</a> identifies later substantive corrections. Other pages are preserved as detailed reference or supplementary research, not automatically re-certified.</p>',
    )
    build_card = (
        '<div class="card"><h3>Rebuild the core</h3>'
        '<pre><code>python3 scripts/build_core.py\n'
        'python3 scripts/check_core.py\n'
        'python3 scripts/check_links.py</code></pre>'
        '<p>The core build fails if a row names a missing source, if a verified row '
        'has no value, or if an unverified row carries a value. The link checker '
        'verifies internal links and anchors across the published site.</p>'
        f'<p class="hint">Data: <a href="data/core.json">data/core.json</a> · '
        f'{len(data["sources"])} official sources</p></div>'
    )
    policy_card = (
        '<div class="card"><ul>'
        '<li><strong>Verified</strong> — the value matches an official source linked on the row.</li>'
        '<li><strong>Verified — nuance</strong> — the value is official, but a related definition or date is unresolved and flagged.</li>'
        '<li><strong>Flagged</strong> — official sources conflict, or the legal question is unsettled.</li>'
        '<li><strong>Unverified — blank</strong> — no official value was located; the cell is blank.</li>'
        '<li><strong>Preserved</strong> — earlier work retained for reference; not re-certified by this session.</li>'
        '</ul></div>'
    )
    body += (
        '<div class="wrap">' + blocks
        + section("Build and verification", "build", build_card)
        + section("Status policy", "policy", policy_card)
        + '</div>'
    )
    return page(
        "Archive — Every Page and Its Status",
        "Archive · primary core, detailed reference, supplementary dashboards",
        "archives.html",
        body,
        "Index of every page on the California healthcare work-requirements site, labelled as verified core, preserved detailed reference, or supplementary research.",
    )


def flagged(data, sources):
    # Report archival row-link exceptions honestly, without attaching a random
    # government URL to a historical claim that the document does not support.
    from check_accuracy import audit_page
    archival_pages = (
        "flagged-detailed.html", "verification-detailed.html",
        "verify-5bf2fb99.html", "verify-9285d712.html",
        "verify-95219c64.html", "verify-a9c46f9b.html",
    )
    archive_gaps = []
    for rel in archival_pages:
        if os.path.exists(os.path.join(ROOT, rel)):
            _rows, issues = audit_page(rel)
            if issues:
                archive_gaps.append((rel, len(issues)))
    rows = []
    for f in data["flags"]:
        rows.append([
            f'<span class="tag" id="{esc(f["id"])}">{esc(f["id"])}</span>',
            f'<strong>{esc(f["item"])}</strong>',
            esc(f["issue"]),
            esc(f["impact"]),
            source_cells(sources, f),
            badge(f["status"]),
        ])
    open_rows = [r for r, f in zip(rows, data["flags"]) if f["status"] == "open"]
    unver_rows = [r for r, f in zip(rows, data["flags"]) if f["status"] == "unverified"]
    closed_rows = [r for r, f in zip(rows, data["flags"]) if f["status"] == "closed"]
    heads = ["ID", "Item", "Issue", "Why it matters", "Source", "Status"]
    counts = {k: sum(1 for f in data["flags"] if f["status"] == k) for k in ("open", "unverified", "closed")}
    body = hero(
        "Flagged for Review — every open irregularity, in one place.",
        "Flagged for Review · nothing hidden, nothing filled in",
        "",
        [
            {"label": "Open flags", "value": str(counts["open"]), "detail": "Unresolved conflicts or missing official values."},
            {"label": "Unverified — blank", "value": str(counts["unverified"]), "detail": "No official value located; the cell stays empty."},
            {"label": "Corrections closed", "value": str(counts["closed"]), "detail": "Earlier errors fixed and recorded."},
            {"label": "Official sources cited", "value": str(len(data["sources"])), "detail": "Every flag names at least one."},
        ],
        [("open", "Open flags"), ("unverified", "Unverified — blank"), ("closed", "Corrections closed"), ("archive-gaps", "Archival link gaps"), ("policy", "What a flag means")],
        [
            '<span class="badge warn">Read first</span><h3 style="margin-top:10px">A flag is not a finding of ineligibility</h3><p>It marks a place where official sources conflict, a value could not be confirmed, or the law is unsettled. The affected cell is left blank rather than estimated.</p>',
            '<h3>How to use this page</h3><p>Take the flag ID to the county eligibility worker, a CPA, or a Covered California counselor. Do not treat a blank as a zero.</p>',
            '<div class="alert warn" style="margin:0">Nothing on this page was inferred. Where a number could not be confirmed from an official source, it is absent.</div>',
        ],
        lead_html='<p class="lead">These are the items the site will not paper over. Each row names the official source it was checked against, states the conflict, and says why it matters for a California resident with zero earned income.</p>',
    )
    body += '<div class="wrap">'
    body += section("Open flags", "open", table(heads, open_rows, table_id="flags-open"),
                   "Ordered by ID. The same flags appear in context on the Work Rules, Coverage Options and Executive Summary pages.")
    body += section("Unverified — value deliberately left blank", "unverified",
                    table(heads, unver_rows, table_id="flags-unverified"),
                    "These rows have no official value. The site does not estimate, average, or infer one.")
    body += section("Corrections closed on this site", "closed",
                    table(heads, closed_rows, table_id="flags-closed"),
                    "Earlier pages carried these errors. They were corrected at the data layer, so every generated page now shows the corrected value.")
    body += section("Other flagged registers on this site", "registers", (
        '<div class="card"><p>Earlier sessions published their own flagged-item registers inside the supplementary dashboards. '
        'They are preserved and linked here so no flagged item is reachable only by accident.</p>'
        '<ul class="big-list">'
        '<li><a href="docs/flagged-for-review.html">Docs flags</a> — taxes, subsidies and unresolved values</li>'
        '<li><a href="research/review.html">Research flags</a> — income, public-charge and enforcement questions</li>'
        '<li><a href="coverage-guide/pages/flagged.html">Coverage-guide flags</a> — timing, hours and FPL</li>'
        '<li><a href="audit-6fc18b58.html">Independent source audit</a> and <a href="archives.html#archive">other checks</a></li>'
        '</ul>'
        f'<p class="hint">This primary register has {len(data["flags"])} flags generated from <code>data/core.json</code>.</p></div>'
    ))
    gap_items = "".join(
        f'<li><a href="{esc(rel)}">{esc(rel)}</a> — {count} row(s) without a direct official-domain citation</li>'
        for rel, count in archive_gaps
    )
    body += section("Preserved archived pages — row-link gaps still open", "archive-gaps", (
        '<div class="alert warn"><strong>Not certified as current advice.</strong> '
        f'{sum(count for _, count in archive_gaps)} archived table rows across '
        f'{len(archive_gaps)} preserved pages have no direct official-domain link. '
        'Some are editorial or indirect-register references; a missing link does not by itself prove a factual error. '
        'Do not treat these historical tables as individually source-verified. '
        'The independent <a href="audit-6fc18b58.html">earlier audit</a> is a dated, separate inventory, not the current count. '
        'See the <a href="accuracy-93fdc24b.html">current accuracy update</a> before using an older figure.</div>'
        f'<div class="card"><ul class="big-list">{gap_items}</ul></div>'
    ), "The count is recalculated from the preserved files on each core rebuild by scripts/check_accuracy.py; no irrelevant official URL is attached to an unrelated editorial row.")
    body += section("What a flag means", "policy", (
        '<div class="card"><ul class="big-list">'
        '<li><strong>Open</strong> — two official sources conflict, or the legal question is not settled. Both readings are shown and the reader is told which decision-maker resolves it.</li>'
        '<li><strong>Unverified — blank</strong> — no official source states the value. The cell is empty by design; an empty cell is never a zero.</li>'
        '<li><strong>Closed</strong> — an earlier value on this site was wrong. The correction, the old value, and the official source are recorded in the row.</li>'
        '</ul><p class="hint">Flags do not block publication. They are published here, labelled, as required. '
        'Full source register: <a href="findings.html#sources">Findings → Sources</a>.</p></div>'
    ))
    body += '</div>'
    return page(
        "Flagged for Review — Open Irregularities",
        "Flagged for Review · open, unverified, and corrected items",
        "flagged.html",
        body,
        "Every open irregularity, unverified blank value, and closed correction on the California healthcare work-requirements site, each with an official source link.",
    )


def verification(data, sources):
    src_rows = []
    for s in data["sources"]:
        src_rows.append([
            f'<span class="tag">{esc(s["id"])}</span>',
            esc(s["publisher"]),
            f'<strong>{esc(s["title"])}</strong>',
            esc(s["date"]),
            f'<a href="{esc(s["url"])}" target="_blank" rel="noopener">Open ↗</a>',
        ])
    corrections = [f for f in data["flags"] if f["status"] == "closed"]
    corr_rows = [[f'<span class="tag">{esc(f["id"])}</span>', f'<strong>{esc(f["item"])}</strong>',
                  esc(f["issue"]), source_cells(sources, f)] for f in corrections]
    body = hero(
        "Verification — what was checked, against what, and when.",
        "Verification log · 2026-10-18 · line-by-line source audit",
        "",
        [
            {"label": "Official sources", "value": str(len(data["sources"])), "detail": "Primary documents, not summaries."},
            {"label": "Table rows checked", "value": str(len(data["findings"])), "detail": "Each row names a source."},
            {"label": "Closed corrections", "value": str(len(corrections)), "detail": "Earlier errors fixed at the data layer."},
            {"label": "Build guard", "value": "3 rules", "detail": "Missing source, empty verified value, valued unverified row."},
        ],
        [("method", "Method"), ("sources", "Source register"), ("corrections", "Corrections"), ("limits", "Limits")],
        [
            '<h3>Primary documents only</h3><p>Statute on congress.gov, the rule on federalregister.gov, agency guidance on cms.gov, medicaid.gov and dhcs.ca.gov, tax material on irs.gov. News coverage is never the source of a value.</p>',
            '<h3>Blank beats wrong</h3><p>If two official sources conflict, both are shown and the row is flagged. If none states the value, the cell stays empty.</p>',
            '<div class="alert info" style="margin:0">A row marked “verified” means the value matches the linked document. It does not mean the reader qualifies.</div>',
        ],
        lead_html='<p class="lead">This is the source trail behind the primary core. It lists the official documents, corrections and limits of a source-presence check; it does not claim a new end-to-end re-reading of every inherited document.</p>',
    )
    body += '<div class="wrap">'
    body += section("Method", "method", (
        '<div class="card"><ol class="big-list">'
        '<li><strong>Collect the primary document.</strong> Statute, regulation, Federal Register notice, agency letter, or official table — not a summary of it.</li>'
        '<li><strong>Extract one value per row.</strong> Each row of every table is a single claim with a single source id.</li>'
        '<li><strong>Cross-check.</strong> Where two agencies both speak, the values are compared. A difference is flagged, not averaged.</li>'
        '<li><strong>Leave blanks.</strong> No official value means no value in the cell.</li>'
        '<li><strong>Guard the build.</strong> The generator refuses to publish a row with a missing source, a verified row with no value, or an unverified row that carries one.</li>'
        '</ol><p class="hint">Reproduce: <code>python3 scripts/build_core.py &amp;&amp; python3 scripts/check_core.py &amp;&amp; python3 scripts/check_links.py</code></p></div>'
    ), "The data file is <a href=\"data/core.json\">data/core.json</a>; the generator is <a href=\"scripts/build_core.py\">scripts/build_core.py</a>.")
    body += section(f"Source register — {len(sources)} official documents", "sources",
                    table(["ID", "Publisher", "Document", "Date", "Link"], src_rows, table_id="source-register"),
                    "Dates identify the document's publication/effective date where shown, otherwise an explicitly labelled access date. Every core finding names a registered source ID.")
    body += section("Corrections applied to earlier pages", "corrections",
                    table(["ID", "Item", "What was wrong and what changed", "Source"], corr_rows, table_id="corrections-table"),
                    "These are recorded as closed. The generated pages carry the corrected value.")
    body += section("Limits of this review", "limits", (
        '<div class="card"><ul class="big-list">'
        '<li><strong>It is a document review, not a legal opinion.</strong> Only a county eligibility worker, an administrative law judge, or a court can decide a specific case.</li>'
        '<li><strong>Personal facts are missing.</strong> Age, household size, county, exact income, filing status, and current coverage were not supplied, so no personal eligibility determination is made.</li>'
        '<li><strong>Guidance can change.</strong> CMS and DHCS can issue sub-regulatory guidance at any time; the source register is dated so a reader can see the vintage.</li>'
        '<li><strong>Links can rot.</strong> <code>scripts/check_links.py</code> validates internal links and anchors; official external URLs were checked when the register was compiled.</li>'
        '</ul><p class="hint">Report a conflict by citing the flag ID and the official document. Do not edit a value without a source.</p></div>'
    ))
    body += '</div>'
    return page(
        "Verification — Source Audit and Corrections",
        f"Verification log · method, {len(sources)}-source register, corrections",
        "verification.html",
        body,
        "Verification log for the California healthcare work-requirements site: method, the full 40-document official source register, corrections applied, and the limits of the review.",
    )


def main():
    data = load()
    sources, problems = check(data)
    if problems:
        raise SystemExit("Data validation failed:\n" + "\n".join(problems))
    outputs = {
        "index.html": dashboard(data, sources),
        "executive-summary.html": executive_summary(data, sources),
        "work-rules.html": work_rules(data, sources),
        "coverage-options.html": coverage_options(data, sources),
        "findings.html": findings_page(data, sources),
        "verification.html": verification(data, sources),
        "flagged.html": flagged(data, sources),
        "archives.html": archives(data, sources),
    }
    for name, content in outputs.items():
        path = os.path.join(ROOT, name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        print(f"wrote {name} ({len(content):,} bytes)")
    print(f"{len(data['findings'])} findings, {len(data['sources'])} sources, no missing source ids.")


if __name__ == "__main__":
    main()
