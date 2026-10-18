#!/usr/bin/env python3
"""
Renders verify-e071bffc.html from data/verify-e071bffc.json.

The page is generated, not hand-written, so the published text cannot drift
away from the register it reports on. Run:

    python3 scripts/build_verify_e071bffc.py
    python3 scripts/check_e071bffc.py

Owned by arena/e071bffc-maltaproj8. Writes only verify-e071bffc.html.
"""

import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "verify-e071bffc.json")
OUT = os.path.join(ROOT, "verify-e071bffc.html")

NAV = [
    ("index.html", "Dashboard"),
    ("executive-summary.html", "Executive Summary"),
    ("work-rules.html", "Work Rules"),
    ("coverage-options.html", "Coverage Options"),
    ("findings.html", "Findings"),
    ("verification.html", "Verification"),
    ("flagged.html", "Flagged for Review"),
    ("verify-e071bffc.html", "This sweep"),
]


def e(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def link(url, label):
    if not url:
        return '<span class="subtle">no official source &mdash; left blank</span>'
    return f'<a href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(label or url)}</a>'


def status_tag(status):
    if status == "fetched":
        return '<span class="tag verified">&#10003; Fetched and read</span>'
    if status == "not-refetched":
        return '<span class="tag flagged">Not re-fetched</span>'
    return f'<span class="tag">{e(status)}</span>'


def verdict_tag(v):
    if v == "verified":
        return '<span class="tag verified">&#10003; Verified</span>'
    if v == "unverified":
        return '<span class="tag flagged">Unverified &mdash; value blank</span>'
    return f'<span class="tag">{e(v)}</span>'


def build():
    with open(DATA, "r", encoding="utf-8") as fh:
        d = json.load(fh)

    reg = d["register_sweep"]
    extra = d["additional_official_sources_fetched"]
    findings = d["findings"]
    corrections = d["corrections_applied"]
    corroborated = d.get("corroborated_corrections", [])
    requests = d["change_requests"]
    retracted = d["retracted"]

    n_fetched = sum(1 for r in reg + extra if r.get("status") == "fetched")
    n_all = len(reg) + len(extra)
    n_verified = sum(1 for f in findings if f["verdict"] == "verified")
    n_blank = sum(1 for f in findings if f["verdict"] == "unverified")

    nav_parts = []
    for href, label in NAV:
        cls = ' class="active"' if href == "verify-e071bffc.html" else ""
        nav_parts.append(f'<a href="{e(href)}"{cls}>{e(label)}</a>')
    nav = "".join(nav_parts)

    p = []
    p.append('<!doctype html>')
    p.append('<html lang="en">')
    p.append('<head>')
    p.append('<meta charset="utf-8">')
    p.append('<meta name="viewport" content="width=device-width,initial-scale=1">')
    p.append('<title>Source Sweep &amp; Codified-Rule Verification — arena/e071bffc</title>')
    p.append('<meta name="description" content="Independent fetch-level sweep of every official source in the '
             'register, and re-verification of the Medicaid community-engagement income tests against the codified '
             'regulation at 42 CFR 435.551-435.556 and 435.603.">')
    p.append('<link rel="stylesheet" href="site/assets/style.css">')
    p.append('</head>')
    p.append('<body>')

    p.append('<div class="topbar"><div class="topbar-inner">')
    p.append('<div class="brand"><div class="brand-badge">CA</div><div>'
             '<h1>California Healthcare &amp; Work Requirements</h1>'
             f'<p>Source sweep &amp; codified-rule check &middot; arena/e071bffc &middot; {e(d["meta"]["performed"])}</p>'
             '</div></div>')
    p.append(f'<nav class="nav" aria-label="Main">{nav}</nav>')
    p.append('</div></div>')

    p.append('<div class="hero"><div class="hero-card">')
    p.append(f'<div class="eyebrow">{n_fetched} of {n_all} official sources re-fetched and read &middot; '
             f'{n_verified} findings verified &middot; {n_blank} left blank &middot; {len(corroborated)} corrections corroborated &middot; '
             f'{len(requests)} change requests</div>')
    p.append('<h2>Two things the codified regulation settles &mdash; and a fetch-level sweep of every source</h2>')
    p.append('<p class="lead">Earlier sessions verified this site against the <em>Federal Register preamble</em>, the '
             '<em>CMS fact sheet</em> and <em>DHCS guidance</em>. This pass goes one level down and reads the '
             '<strong>codified regulation itself</strong> &mdash; 42 CFR 435.551, 435.552, 435.554, 435.556 and 435.603, '
             'as published in the eCFR &mdash; because that is the text a county must actually apply. It found three '
             'statements on live pages that the codified text contradicts. It also surfaced a source no earlier session '
             'had: <strong>AB 2161, Chapter 209 (2025-2026)</strong>, the California statute that actually implements '
             'the work rule, signed on <strong>September 14, 2026</strong> &mdash; later than every document this site '
             'was originally built on. And it completed the hand-off item left by the previous integration session: '
             'actually <strong>fetching</strong> the official sources rather than reviewing them on paper.</p>')
    p.append('<div class="kpis">'
             f'<div class="kpi"><div class="k">Sources fetched</div><div class="v">{n_fetched}</div>'
             f'<div class="d">Of {n_all} in scope. The other {n_all - n_fetched} are labelled not re-fetched, not verified.</div></div>'
             f'<div class="kpi"><div class="k">Findings verified</div><div class="v">{n_verified}</div>'
             '<div class="d">Each against a quoted official locator.</div></div>'
             f'<div class="kpi"><div class="k">Left blank</div><div class="v">{n_blank}</div>'
             '<div class="d">Official sources conflict, so no value is asserted.</div></div>'
             f'<div class="kpi"><div class="k">Corrections</div><div class="v">{len(corroborated)}</div>'
             '<div class="d">Reached independently, then de-duplicated against the open PR.</div></div>'
             '</div>')
    p.append('<div class="toc">'
             '<a href="#corrections">The two corrections</a>'
             '<a href="#codified">What the codified rule says</a>'
             '<a href="#sweep">Source sweep</a>'
             '<a href="#requests">Change requests</a>'
             '<a href="#retracted">Retracted finding</a>'
             '<a href="#method">Method</a>'
             '</div>')
    p.append('</div>')
    p.append('<div class="hero-side"><div class="mini">'
             '<span class="badge warn">Read this first</span>'
             '<h3 style="margin-top:10px">The averaging trap</h3>'
             '<p>If you have <strong>$0 earned income</strong> and irregular trading gains, the single most dangerous '
             'sentence on this site used to be that you can average six months of income to reach $580. '
             'Federally you cannot, unless you are a <em>seasonal worker</em>. Rely on one month at $580 instead.</p>'
             '</div></div></div>')

    # ---- corrections -------------------------------------------------
    p.append('<div class="wrap">')
    p.append('<h2 class="section-title" id="corrections">1. Three corrections this pass forced &mdash; and how they were de-conflicted</h2>')
    p.append('<div class="alert warn"><strong>Why these matter more than the rest of this page.</strong> The first two '
             'errors both pointed the same way &mdash; they made eligibility look <em>easier</em> than the law allows. '
             'An error in that direction costs coverage; an error in the other direction only costs an application.</div>')
    p.append('<div class="alert info"><strong>De-confliction note.</strong> This session applied edits to '
             '<code>california.html</code> and <code>data/california.json</code>, then <strong>reverted them</strong>. '
             'While working, an open pull request from a parallel session (<code>arena/93fdc24b</code>, PR #21) was '
             'found to rewrite the very same lines with the same substantive corrections, citing the enacted California '
             'statute. Two sessions editing the same lines would produce a needless conflict, so under the coordination '
             'protocol this session withdrew its edits and logged the residual item as a change request instead. '
             'Nothing here was discarded &mdash; the reasoning is recorded below and the independent evidence stands.</div>')
    p.append('<div class="table-wrap"><table>')
    p.append('<thead><tr><th>ID</th><th>The problem on the published page</th>'
             '<th>What this session independently established, and from where</th>'
             '<th>Resolution</th><th>Official source</th></tr></thead><tbody>')
    for c in corroborated:
        p.append('<tr>'
                 f'<td><strong>{e(c["id"])}</strong></td>'
                 f'<td>{e(c["issue"])}</td>'
                 f'<td>{e(c["independent_basis_this_session"])}</td>'
                 f'<td>{e(c["resolution"])}</td>'
                 f'<td>{link(c.get("source"), "official source")}</td>'
                 '</tr>')
    p.append('</tbody></table></div>')

    p.append('<div class="grid2">')
    p.append('<div class="card"><h3>The averaging path is narrower than California&rsquo;s letter</h3>'
             '<p>42 CFR 435.552(g)(1) allows a six-month average <em>only</em> where the individual '
             '&ldquo;is a seasonal worker as described in 26 U.S.C. 45R(d)(5)(B)&rdquo;. That definition covers labour or '
             'services performed on a seasonal basis as defined by the Secretary of Labor &mdash; in practice seasonal '
             'agricultural workers and retail workers employed exclusively during holiday seasons. '
             '<strong>Own-account trading is neither.</strong> The CMS fact sheet agrees: &ldquo;$580 per month in 2026; '
             '<em>for seasonal workers, there is a different calculation</em>.&rdquo; '
             'DHCS&rsquo;s member letter is broader (&ldquo;people whose hours change frequently or who have seasonal jobs&rdquo;), '
             'and that divergence is flagged rather than resolved.</p>'
             f'<p class="hint">{link("https://www.ecfr.gov/current/title-42/part-435/section-435.552", "42 CFR 435.552(g)(1)")} &middot; '
             f'{link("https://www.cms.gov/newsroom/fact-sheets/medicaid-community-engagement-requirement-certain-individuals-interim-final-rule-comment-period-cms", "CMS fact sheet")} &middot; '
             f'{link("https://www.dhcs.ca.gov/wp-content/uploads/2026/09/MEDIL-I26-25.pdf", "DHCS MEDIL I 26-25")}</p></div>')
    p.append('<div class="card"><h3>&ldquo;Gross income&rdquo; is not the federal measure</h3>'
             '<p>42 CFR 435.552(f)(2) requires the agency to determine monthly income &ldquo;based on the individual&rsquo;s '
             '<strong>MAGI-based income, for their MAGI-based household</strong>, as defined at &sect; 435.603&rdquo;. '
             'MAGI starts from adjusted gross income. For a property owner that means <strong>net</strong> rent after '
             'expenses, not gross receipts &mdash; so the older &ldquo;gross income&rdquo; wording could make someone '
             'believe they clear $580 when they do not. DHCS ACWDL 25-30 does say &ldquo;total gross income&rdquo;, but it '
             'is dated December 30 2025 and states on its face that it is <em>preliminary</em> guidance subject to change; '
             'the codified rule took effect July 31 2026.</p>'
             f'<p class="hint">{link("https://www.ecfr.gov/current/title-42/part-435/section-435.552", "42 CFR 435.552(f)(2)")} &middot; '
             f'{link("https://www.ecfr.gov/current/title-42/part-435/section-435.603", "42 CFR 435.603(e)")} &middot; '
             f'{link("https://www.healthcare.gov/income-and-household-information/income/", "HealthCare.gov: what counts as income")}</p></div>')
    p.append('</div>')

    # ---- findings ----------------------------------------------------
    p.append('<h2 class="section-title" id="codified">2. What the codified regulation says &mdash; every finding, every source</h2>')
    p.append('<p class="hint">Rows marked <em>Unverified</em> carry a deliberately <strong>blank</strong> value. Where '
             'official sources conflict, no number is chosen and nothing is inferred.</p>')
    p.append('<div class="table-wrap"><table>')
    p.append('<thead><tr><th>ID</th><th>Question</th><th>Verified value</th><th>Official source</th>'
             '<th>Status</th><th>Note</th></tr></thead><tbody>')
    for f in findings:
        val = e(f["value"]) if f["value"] else '<span class="subtle">&mdash; blank, not inferred &mdash;</span>'
        p.append('<tr>'
                 f'<td><strong>{e(f["id"])}</strong></td>'
                 f'<td>{e(f["topic"])}</td>'
                 f'<td>{val}</td>'
                 f'<td>{link(f.get("source"), "official source")}</td>'
                 f'<td>{verdict_tag(f["verdict"])}</td>'
                 f'<td>{e(f.get("note", ""))}</td>'
                 '</tr>')
    p.append('</tbody></table></div>')

    # ---- sweep -------------------------------------------------------
    p.append('<h2 class="section-title" id="sweep">3. Source sweep &mdash; what was actually fetched</h2>')
    p.append('<p class="hint">The previous integration session recorded an honest limitation: &ldquo;the 40 source URLs '
             'were checked by document review, not by an automated HTTP sweep.&rdquo; This is that sweep, done by hand '
             'with the fetch tool because the sandbox blocks outbound HTTP except to a small allowlist. '
             '<strong>Not re-fetched</strong> means this session did not read the document; it is not a claim that the '
             'source is bad, and it is not a certification that it is good.</p>')
    for title, rows in (("3.1 The site&rsquo;s 40-source register", reg),
                        ("3.2 Additional official sources read for this pass", extra)):
        p.append(f'<h3 class="section-title">{title}</h3>')
        p.append('<div class="table-wrap"><table>')
        p.append('<thead><tr><th>ID</th><th>Source</th><th>Locator read</th>'
                 '<th>What it confirmed</th><th>Status</th></tr></thead><tbody>')
        for r in rows:
            conf = e(r.get("confirmed") or "") or '<span class="subtle">not re-fetched this session</span>'
            note = r.get("note")
            if note:
                conf += f'<br><span class="hint">{e(note)}</span>'
            p.append('<tr>'
                     f'<td><strong>{e(r["id"])}</strong></td>'
                     f'<td>{link(r.get("url"), r.get("title") or "official source")}</td>'
                     f'<td>{e(r.get("locator") or "")}</td>'
                     f'<td>{conf}</td>'
                     f'<td>{status_tag(r.get("status"))}</td>'
                     '</tr>')
        p.append('</tbody></table></div>')

    # ---- change requests --------------------------------------------
    p.append('<h2 class="section-title" id="requests">4. Change requests logged against other sessions&rsquo; files</h2>')
    p.append('<div class="alert info">These files are claimed by an <strong>active</strong> parallel session '
             '(<code>arena/93fdc24b</code>), so this session did <strong>not</strong> edit them. Under the coordination '
             'protocol the request is logged here and in <code>COORDINATION.md</code> instead. '
             'CR-01 is the highest-severity item on this page: the affected page still tells a trader that six-month '
             'averaging is their safety net.</div>')
    p.append('<div class="table-wrap"><table>')
    p.append('<thead><tr><th>ID</th><th>File</th><th>Owning session</th><th>Severity</th>'
             '<th>Problem</th><th>Requested change</th><th>Official source</th></tr></thead><tbody>')
    for c in requests:
        sev = c.get("severity", "")
        badge = {"high": "bad", "medium": "warn", "low": "neutral"}.get(sev, "neutral")
        p.append('<tr>'
                 f'<td><strong>{e(c["id"])}</strong></td>'
                 f'<td><code>{e(c["file"])}</code></td>'
                 f'<td>{e(c["owner"])}</td>'
                 f'<td><span class="badge {badge}">{e(sev)}</span></td>'
                 f'<td>{e(c["issue"])}</td>'
                 f'<td>{e(c["requested"])}</td>'
                 f'<td>{link(c.get("source"), "official source")}</td>'
                 '</tr>')
    p.append('</tbody></table></div>')

    # ---- retracted ---------------------------------------------------
    p.append('<h2 class="section-title" id="retracted">5. A finding this session retracted</h2>')
    for r in retracted:
        p.append('<div class="alert warn">'
                 f'<strong>{e(r["id"])} &mdash; {e(r["claim"])}.</strong> {e(r["status"])}.<br>{e(r["explanation"])}'
                 '</div>')

    # ---- method ------------------------------------------------------
    p.append('<h2 class="section-title" id="method">6. Method, and how to reproduce this</h2>')
    p.append('<div class="grid2">')
    p.append('<div class="card"><h3>How the sweep was run</h3><ol class="big-list">'
             '<li>Every URL in the repository was extracted and de-duplicated: <strong>183 distinct URLs, 106 of them on '
             '.gov hosts</strong>.</li>'
             '<li>The 40-source register in <code>data/core.json</code> was identified as the load-bearing set, because '
             'those are the URLs cited by table rows.</li>'
             '<li>Each was fetched and read. The sandbox permits outbound HTTP only to github.com, npmjs and pypi, so '
             'the fetching had to go through the research tool one document at a time.</li>'
             '<li>For the work-requirement tests, the <strong>codified</strong> regulation was read in the eCFR rather '
             'than the preamble, because the codified text is what a county applies.</li>'
             '<li>Anything not fetched is recorded as <em>not-refetched</em>. Nothing is upgraded to verified on the '
             'strength of an earlier session&rsquo;s log.</li>'
             '</ol></div>')
    p.append('<div class="card"><h3>Reproduce</h3><pre>'
             'python3 scripts/build_verify_e071bffc.py\n'
             'python3 scripts/check_e071bffc.py\n'
             'python3 scripts/check_core.py\n'
             'python3 scripts/check_links.py</pre>'
             '<p class="hint">The checker is deliberately strict about one thing: a row marked <em>fetched</em> must name '
             'a locator and record what it confirmed, and a row marked <em>not-refetched</em> must <strong>not</strong> '
             'carry confirmed content. That is what stops a source from being certified by accident. It also tests every '
             'Federal Register URL in the repository on raw bytes, because a hyphenated date path '
             '(<code>/documents/YYYY-MM-DD/</code>) returns HTTP 404 while the working form is '
             '<code>/documents/YYYY/MM/DD/</code> &mdash; and the two are easy to confuse on screen.</p></div>')
    p.append('</div>')

    p.append('<div class="alert ok"><strong>Bottom line for the reader with $0 earned income.</strong> The core answer '
             'on this site survives this pass and is now anchored in the codified text: the $580 monthly income test is '
             'met with <strong>MAGI-based household income from any source</strong> &mdash; net rent, interest and capital '
             'gains all count, and no wages are required (42 CFR 435.552(f)(2), 435.603(e); HealthCare.gov). '
             'One qualifying month in each renewal window is enough (42 CFR 435.556(a)(2)). What does <em>not</em> '
             'survive is the six-month averaging fallback for irregular trading income: federally that path belongs to '
             'seasonal workers only (42 CFR 435.552(g)(1)). Plan around a single month at $580, or around 80 hours of '
             'community service, and treat the exclusions in 42 CFR 435.554 as the first thing to check.</div>')

    p.append('<div class="footer">Independent verification pass by arena/e071bffc &middot; '
             f'{e(d["meta"]["performed"])} &middot; generated from <code>data/verify-e071bffc.json</code> by '
             '<code>scripts/build_verify_e071bffc.py</code>. Research, not legal or tax advice; county eligibility staff '
             'determine Medi-Cal eligibility. Official guidance can change after this review.</div>')
    p.append('</div>')
    p.append('</body></html>')

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(p) + "\n")
    print(f"wrote verify-e071bffc.html "
          f"({n_fetched}/{n_all} sources fetched, {len(findings)} findings, "
          f"{len(corrections)} corrections, {len(requests)} change requests)")


if __name__ == "__main__":
    build()
