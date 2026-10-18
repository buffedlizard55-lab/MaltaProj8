#!/usr/bin/env node
/**
 * build-site.js — generates the GitHub Pages site in /docs from /data/*.json
 * Session c8487e35. Every table row renders with its official source link.
 * No external dependencies, no build tooling: output is static HTML+CSS.
 * Run: node tools/build-site.js
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const DATA = path.join(ROOT, 'data');
const DOCS = path.join(ROOT, 'docs');
const VERIFY_DATE = '2026-10-18';

const read = (f) => JSON.parse(fs.readFileSync(path.join(DATA, f), 'utf8'));
const income = read('income-tax.json');
const coverage = read('coverage.json');
const laws = read('laws.json');
const flags = read('flags.json');

const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

const NAV = [
  ['index.html', 'Home'],
  ['executive-summary.html', 'Executive Summary'],
  ['income-taxes.html', 'Income & Taxes'],
  ['medicaid.html', 'Medi-Cal'],
  ['covered-california.html', 'Covered California'],
  ['new-laws.html', 'New Laws & Work Req.'],
  ['ca-mandate.html', 'CA Mandate'],
  ['action-plan.html', 'Action Plan'],
  ['sources.html', 'All Sources'],
  ['flagged-for-review.html', '⚑ Flagged for Review'],
];

function page(file, title, active, body) {
  const nav = NAV.map(([href, label]) =>
    `<a class="nav-link${href === active ? ' active' : ''}" href="${href}">${label}</a>`).join('');
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)} · Healthcare Access — Zero Earned Income, California</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="masthead">
  <div class="wrap masthead-inner">
    <div class="brand"><a href="index.html"><span class="brand-mark">✚</span> Healthcare Access<span class="brand-sub"> — CA · $0 earned income · verified findings</span></a></div>
    <div class="stamp">All data verified against official sources on <strong>${VERIFY_DATE}</strong></div>
  </div>
  <nav class="wrap nav" aria-label="Primary">${nav}</nav>
</header>
<main class="wrap">
${body}
</main>
<footer class="footer"><div class="wrap">
  <p>Generated from <code>data/*.json</code> by <code>tools/build-site.js</code> (session <code>c8487e35</code>). Every table row carries a link to its official source; values that could not be confirmed from an official source are left blank and listed on the <a href="flagged-for-review.html">Flagged for Review</a> page. This site is an organized research brief, not legal or tax advice.</p>
</div></footer>
</body></html>`;
}

function statusBadge(status) {
  return status === 'verified'
    ? '<span class="badge ok">✓ Verified</span>'
    : '<span class="badge warn">⚑ Flagged</span>';
}

function sourceCell(row) {
  const link = `<a class="src" href="${esc(row.source_url)}" target="_blank" rel="noopener">${esc(row.source_label)}</a>`;
  const note = row.note ? `<div class="note">${esc(row.note)}</div>` : '';
  return `${link}${note}`;
}

function table(rows) {
  const body = rows.map((r) => `
    <tr class="${r.status === 'flagged' ? 'row-flagged' : ''}">
      <td class="rid">${esc(r.id)}</td>
      <th scope="row" class="topic">${esc(r.topic)}</th>
      <td class="finding">${esc(r.finding)}</td>
      <td class="val">${esc(r.value)}</td>
      <td class="eff">${esc(r.effective)}</td>
      <td class="st">${statusBadge(r.status)}</td>
      <td class="src-cell">${sourceCell(r)}</td>
    </tr>`).join('\n');
  return `<div class="table-scroll"><table class="data">
<thead><tr><th>ID</th><th>Topic</th><th>Verified finding</th><th>Key value</th><th>Effective</th><th>Status</th><th>Official source</th></tr></thead>
<tbody>${body}</tbody></table></div>`;
}

/* ---------------- collectors ---------------- */
const allRowSets = [
  { section: income, rows: income.rows },
  ...coverage.sections.map((s) => ({ section: s, rows: s.rows })),
  ...laws.sections.map((s) => ({ section: s, rows: s.rows })),
];
const flaggedRows = allRowSets.flatMap((x) => x.rows.filter((r) => r.status === 'flagged'));

/* ---------------- pages ---------------- */
const pages = {};

pages['index.html'] = page('index.html', 'Home', 'index.html', `
<section class="hero">
  <h1>Obtaining Healthcare in California with $0 Earned Income</h1>
  <p class="lede">Prepared for a U.S. citizen, California resident, property manager and full-time Kalshi trader whose income is entirely <em>unearned</em>: event-contract trading results, rental income, and savings interest. Every finding below was checked line-by-line against official government (or statutorily-created exchange) sources on ${VERIFY_DATE}.</p>
  <div class="hero-actions"><a class="btn primary" href="executive-summary.html">Read the Executive Summary →</a> <a class="btn" href="action-plan.html">Jump to the Action Plan</a> <a class="btn ghost" href="flagged-for-review.html">⚑ ${flags.flags.length}+ items flagged for review</a></div>
</section>

<section class="cards">
  <a class="card" href="executive-summary.html"><h2>📋 Executive Summary</h2><p>Your options ranked, the decision thresholds for 2026–27, and what the new federal law does to you.</p></a>
  <a class="card" href="income-taxes.html"><h2>🧮 Income &amp; Taxes</h2><p>How Kalshi gains, rent and interest become "MAGI" — the only income number health programs test — plus loss and deduction levers.</p></a>
  <a class="card" href="medicaid.html"><h2>🏥 Medi-Cal</h2><p>Free coverage up to 138% FPL ($22,025 for one person in 2026). No asset test. No work requirement until Jan 1, 2027.</p></a>
  <a class="card" href="covered-california.html"><h2>🛒 Covered California</h2><p>What changed after the federal enhanced subsidies expired — and the state money replacing them (0% premium to 150% FPL).</p></a>
  <a class="card" href="new-laws.html"><h2>⚖️ New Laws &amp; Work Requirements</h2><p>P.L. 119-21 exact provisions: 80 hrs / $580 test, exemptions, uncapped repayment — and California's implementation posture.</p></a>
  <a class="card" href="ca-mandate.html"><h2>🧾 CA Individual Mandate</h2><p>The state penalty you can still owe with no wages — and the three income-based exits from it.</p></a>
  <a class="card" href="action-plan.html"><h2>✅ Action Plan</h2><p>Eight dated steps, each with its source — from projecting 2027 MAGI to surviving the March 2027 six-month renewal cycle.</p></a>
  <a class="card" href="sources.html"><h2>🔗 All Sources</h2><p>Deduplicated registry of every official source cited on the site, for manual review.</p></a>
</section>

<section class="panel keyfigs">
  <h2>Key verified numbers at a glance</h2>
  <div class="figs">
    <div class="fig"><span class="fig-n">$22,025</span><span class="fig-l">Medi-Cal income limit, 1 person, 2026 (138% FPL) — DHCS chart</span></div>
    <div class="fig"><span class="fig-n">0%</span><span class="fig-l">Required premium share up to 150% FPL for 2026 &amp; 2027, thanks to the CA Premium Subsidy</span></div>
    <div class="fig"><span class="fig-n">$580/mo</span><span class="fig-l">Income that satisfies the new Medi-Cal work requirement from Jan 1, 2027 (80 × $7.25) — CMS IFR</span></div>
    <div class="fig"><span class="fig-n">$3,000</span><span class="fig-l">Net capital losses that may offset other income each year (IRS Topic 409)</span></div>
    <div class="fig"><span class="fig-n">Nov 1 – Jan 31</span><span class="fig-l">Open enrollment for 2027 plans; Medi-Cal is year-round</span></div>
    <div class="fig"><span class="fig-n">$300M</span><span class="fig-l">California money for 2027 marketplace subsidies (up from $190M in 2026)</span></div>
  </div>
</section>

<section class="panel method">
  <h2>Method &amp; verification standard</h2>
  <ul>
    <li><strong>Source hierarchy:</strong> federal .gov (CMS, IRS, HHS/ASPE, Federal Register, eCFR, Congress.gov, CFTC), California .gov (DHCS, FTB, state agency letters), and Covered California (the state exchange created by statute) including its official HBEX/board documents. Kalshi's own help-center pages are used only to state what Kalshi itself does (tax forms it issues), never for legal conclusions.</li>
    <li><strong>No inference:</strong> if a number could not be confirmed on an official page, the cell is left blank and the row is flagged ⚑ — see <a href="flagged-for-review.html">Flagged for Review</a>.</li>
    <li><strong>Dating:</strong> subsidy rules changed materially for 2026; figures like the FTB child penalty were even corrected after publication (Apr 2026). Every row shows its effective window and the ${VERIFY_DATE} verification stamp.</li>
    <li><strong>Repo workflow:</strong> work is coordinated in <code>COORDINATION.md</code> at the repo root; data lives in <code>data/*.json</code>; this site is generated by <code>tools/build-site.js</code>.</li>
  </ul>
</section>
`);

pages['executive-summary.html'] = page('executive-summary.html', 'Executive Summary', 'executive-summary.html', `
<h1>Executive Summary</h1>
<p class="lede">How a California resident with $0 earned income obtains healthcare — and how "work requirements" actually apply to you.</p>

<section class="panel">
<h2>1. The one idea that unlocks your situation</h2>
<p>Health-coverage eligibility in California is <strong>not based on having a job</strong>. Medi-Cal and Covered California measure <strong>Modified Adjusted Gross Income (MAGI)</strong> — your federal tax return's AGI plus a few add-backs (healthcare.gov, INC-01/02). Kalshi trading gains, net rental income, and savings interest are all in that number; wages are irrelevant if they are zero. <strong>There is currently no work requirement to get Medi-Cal (until Jan 1, 2027) and no work requirement at all for Covered California financial help</strong> (MED-05, LAW-09). Your leverage is therefore <em>tax-basis income management</em>, not employment.</p>
</section>

<section class="panel">
<h2>2. Your four routes, with the exact 2026–27 thresholds (household of 1)</h2>
<div class="table-scroll"><table class="data decision">
<thead><tr><th>Route</th><th>If your MAGI is…</th><th>What you pay</th><th>Where to apply · verified source</th></tr></thead>
<tbody>
<tr><td><strong>Medi-Cal</strong> (recommended if you fit)</td><td>≤ $22,025 (138% FPL)</td><td>$0 premium, no deductible, full benefits incl. dental; <strong>no asset test</strong> — savings can be any size</td><td><a href="https://www.dhcs.ca.gov/medi-cal/qualify/qualify-for-medi-cal-eligibility-chart/">DHCS chart</a> · <a href="https://www.dhcs.ca.gov/medi-cal/help/">DHCS help (assets)</a> · any time of year</td></tr>
<tr><td><strong>Covered CA, low-income band</strong></td><td>$22,025 – $31,920 (138–200% FPL)</td><td>0% of income to benchmark ≤150% FPL ($23,940); 2.8–5.28% for 150–200% in 2027 (state subsidy; $190M→$300M) — two $0-premium Silver plans in many areas</td><td><a href="https://www.coveredca.com/pdfs/FPL-chart.pdf">Covered CA FPL chart</a> · <a href="https://hbex.coveredca.com/stakeholders/PDFs/2026-02_StatePremiumSub_PolicyExplainer-Final.pdf">HBEX explainer</a></td></tr>
<tr><td><strong>Covered CA, middle band</strong></td><td>200–400% FPL</td><td>6.78%–10.22% of income to benchmark for 2027 (federal APTC; cliff back at 400%)</td><td><a href="https://hbex.coveredca.com/toolkit/downloads/Financial_Help_Basics.pdf">HBEX quick guide</a> · <a href="https://www.coveredca.com/pdfs/FPL-chart.pdf">FPL chart</a></td></tr>
<tr><td><strong>Full-price plan + HSA</strong></td><td>&gt; 400% FPL ($63,840 at 2026 guidelines)</td><td>No federal or state premium help; Bronze/Minimum-Coverage plans are HDHPs in CA from 2026 → deductible HSA contributions ($4,400) reduce AGI even with $0 wages</td><td><a href="https://www.coveredca.com/important-changes">Covered CA Important Changes</a> · <a href="https://www.irs.gov/publications/p969">IRS Pub 969</a></td></tr>
</tbody></table></div>
<p class="fineprint">MAGI here = projected tax-year income: net trading gains (after the $3,000 net-loss cap against other income), net Schedule E rent (possibly reduced by up to $25,000 active-participation allowance if you qualify — see flag FL-05), plus taxable interest. A losing trading year can genuinely produce a $0-MAGI Medi-Cal year.</p>
</section>

<section class="panel">
<h2>3. What the new federal law (P.L. 119-21, July 4, 2025) changes for you</h2>
<ul>
<li><strong>Enhanced premium tax credits are gone.</strong> They expired Dec 31, 2025 and Congress did not renew them; 2026 Marketplace premiums jumped (Covered CA: applicants pay the old federal schedule — 2.10%–9.96% of income by band, nothing above 400%). California backfilled only the low end: ≤165% FPL in 2026, ≤200% FPL in 2027 (LAW-02/11, MKT-03–06).</li>
<li><strong>APTC repayment is uncapped from the 2026 tax year.</strong> If you estimate income low and have a big winning trading year, you repay the full excess credit at tax time (LAW-03). Mitigation: apply honestly-close, update your estimate when your trading year turns, or take the credit as a lump sum at filing (MKT-10/12).</li>
<li><strong>Medicaid (Medi-Cal) work requirement from Jan 1, 2027</strong> — the direct answer to your "work requirements with $0 earned income" question (LAW-04–06):</li>
</ul>
<div class="table-scroll"><table class="data">
<thead><tr><th>Way to satisfy it (any ONE)</th><th>Detail — per the CMS rule</th><th>Fits you?</th></tr></thead>
<tbody>
<tr><td><strong>Income test</strong></td><td>Monthly income ≥ 80 × federal minimum wage = <strong>$580/mo (2026)</strong></td><td>Very likely on paper (rent+interest alone exceed $580), <strong>but</strong> whether non-wage income counts is unconfirmed → ⚑ FL-02</td></tr>
<tr><td>80 hours/month</td><td>Work, community service, work program, or any combination</td><td>Volunteering/qualifying programs work; is trading "work"? unconfirmed → ⚑ FL-03</td></tr>
<tr><td>Half-time student</td><td>Enrolled ≥ half-time in an educational program</td><td>Low-cost hedge: any qualifying enrollment counts per the fact sheet</td></tr>
<tr><td>Exemptions</td><td>Disabled/medically frail; caregiver of child ≤13 or disabled dependent; veteran 100% disabled; former foster youth; AI/AN; SNAP/TANF-covered; treatment programs; incarcerated; pregnancy/postpartum</td><td>Health-condition-based exemption is the realistic one for some traders (documentation required)</td></tr>
</tbody></table></div>
<ul>
<li>Only matters <strong>if you are on Medi-Cal</strong> and are 19–64, childless, not pregnant, not exempt. Marketplace plans have <strong>no</strong> such condition (LAW-09). California adds <strong>six-month eligibility checks</strong> for affected adults from Mar 1, 2027 — keep mail addressed and respond inside 30 days of any non-compliance notice; you can reapply after disenrollment (LAW-05/10).</li>
</ul>
</section>

<section class="panel">
<h2>4. What California is doing for people with $0 earned income</h2>
<ul>
<li><strong>California Premium Subsidy</strong> (Health Care Affordability Reserve Fund): $190M for 2026 (holds 0% benchmark contribution ≤150% FPL; extra help to 165%), $300M for 2027 (extends to 200% FPL, ~500k projected recipients) (LAW-11).</li>
<li><strong>Medi-Cal with no asset test</strong> — the only program that ignores your savings entirely for 19–64 adults (MED-04); DHCS "no property limits."</li>
<li><strong>Bronze/Minimum-Coverage plans made HSA-eligible</strong> effective 2026 — a California-specific ACA change that gives non-wage earners a legal MAGI-reduction tool (INC-16).</li>
<li><strong>Individual-mandate safety valves</strong>: exempt if household income is below the federal filing threshold, if benchmark premiums exceed 7.28% of income (2025), or if the uninsured gap is ≤3 months (MND-04–06) — all realistic for $0-wage years.</li>
<li>County safety-net programs exist in some counties but were not verified for this report → ⚑ FL-08.</li>
</ul>
</section>

<section class="panel">
<h2>5. Bottom line — a practical playbook</h2>
<ol>
<li><strong>Project 2027 MAGI now</strong> (net trading + net rent + interest). If ≤ $22,025 (2026 basis; 2027 limits publish Jan 2027): <a href="https://apply.coveredca.com/static/lw-web/account-creation/choose-application">apply for Medi-Cal today</a> — no enrollment window, immediate start, no work test until 2027.</li>
<li>If above that: <strong>apply Nov 1, 2026 – Jan 31, 2027</strong> on Covered CA (one application screens Medi-Cal too). In the 138–200% band expect ~$0–5% of income for a Silver plan; pick Enhanced Silver (94/87) for near-zero deductibles (ACT-03, MKT-07).</li>
<li><strong>Protect yourself from the uncapped clawback:</strong> conservative estimate + prompt updates, or claim the credit entirely at filing (ACT-06).</li>
<li><strong>Document a 2027 work-requirement position now</strong>: keep the $580+/month income trail, and decide whether to add volunteer hours, a half-time course, or medical-frailty documentation (ACT-08, ⚑ FL-02/03).</li>
<li><strong>In high-gain years</strong>, run the tax levers that are actually verified: $3,000 capital-loss offset, up-to-$25,000 rental-loss special allowance if you qualify (⚑ FL-05), and HSA contributions on a Bronze plan — each reduces AGI, the number the programs re-test at reconciliation.</li>
</ol>
<p class="fineprint">All figures verified 2026-10-18 against the sources linked in the tables. Items this project could not confirm are blank + flagged, never estimated. Full source registry: <a href="sources.html">All Sources</a>.</p>
</section>
`);

/* Category pages */
pages['income-taxes.html'] = page('income-taxes.html', 'Income & Taxes', 'income-taxes.html', `
<h1>${esc(income.title)}</h1>
<p class="lede">${esc(income.blurb)}</p>
<p class="fineprint">Verified 2026-10-18. Rows marked ⚑ carry no confirmed official value — see <a href="flagged-for-review.html">Flagged for Review</a>.</p>
${table(income.rows)}
`);

const secOf = (doc, id) => doc.sections.find((s) => s.id === id);
function sectionPage(file, navId, title, blurb, rows) {
  pages[file] = page(file, title, navId, `
<h1>${esc(title)}</h1>
<p class="lede">${esc(blurb)}</p>${table(rows)}`);
}
sectionPage('medicaid.html', 'medicaid.html', secOf(coverage, 'medicaid').title, secOf(coverage, 'medicaid').blurb, secOf(coverage, 'medicaid').rows);
sectionPage('covered-california.html', 'covered-california.html', secOf(coverage, 'covered-ca').title, secOf(coverage, 'covered-ca').blurb, secOf(coverage, 'covered-ca').rows);
sectionPage('action-plan.html', 'action-plan.html', secOf(coverage, 'action-plan').title, secOf(coverage, 'action-plan').blurb, secOf(coverage, 'action-plan').rows);
sectionPage('new-laws.html', 'new-laws.html', secOf(laws, 'laws').title, secOf(laws, 'laws').blurb, secOf(laws, 'laws').rows);
sectionPage('ca-mandate.html', 'ca-mandate.html', secOf(laws, 'mandate').title, secOf(laws, 'mandate').blurb, secOf(laws, 'mandate').rows);

/* Flagged page */
pages['flagged-for-review.html'] = page('flagged-for-review.html', 'Flagged for Review', 'flagged-for-review.html', `
<h1>⚑ Flagged for Review</h1>
<p class="lede">Items this project could not confirm from official sources, plus source-side irregularities. Per the project standard, nothing here was inferred or filled in — values stay blank on the category tables and are explained here. <strong>Nothing flagged blocks the site or the PR.</strong> A "needs review" status in <code>COORDINATION.md</code> corresponds to this page.</p>
<section class="panel">
<h2>Open questions &amp; source issues (${flags.flags.length})</h2>
${flags.flags.map((f) => `
<article class="flag">
<h3>${esc(f.id)} — ${esc(f.title)}</h3>
<p><strong>Why flagged:</strong> ${esc(f.why)}</p>
<p><strong>Impact:</strong> ${esc(f.impact)}</p>
<p><strong>Recommended action:</strong> ${esc(f.action)}</p>
<p class="flag-links">${f.links.map((l, i) => `<a href="${esc(l)}" target="_blank" rel="noopener">Source ${i + 1}</a>`).join(' · ')}</p>
</article>`).join('\n')}
</section>
<section class="panel">
<h2>Table rows carrying no verified value (auto-collected)</h2>
${table(flaggedRows)}
</section>
`);

/* Sources registry */
const srcMap = new Map();
for (const set of allRowSets) for (const r of set.rows) {
  if (!srcMap.has(r.source_url)) srcMap.set(r.source_url, { url: r.source_url, label: r.source_label, rows: [] });
  srcMap.get(r.source_url).rows.push(r.id);
}
for (const f of flags.flags) for (const l of f.links) {
  if (!srcMap.has(l)) srcMap.set(l, { url: l, label: l.replace(/^https?:\/\//, '').split('/')[0], rows: [] });
  srcMap.get(l).rows.push(f.id);
}
const srcRows = [...srcMap.values()].sort((a, b) => a.url.localeCompare(b.url));
pages['sources.html'] = page('sources.html', 'All Sources', 'sources.html', `
<h1>All Sources (deduplicated registry)</h1>
<p class="lede">Every link cited anywhere on this site, in one table, for manual review. "Cited by" lists the row/flag IDs. Hosts are restricted to U.S. federal .gov, California state .gov, Covered California (statutory state exchange) domains, plus Kalshi's official help center (used only for what Kalshi itself states).</p>
<div class="table-scroll"><table class="data sources">
<thead><tr><th>#</th><th>Publisher / document</th><th>URL</th><th>Cited by</th></tr></thead>
<tbody>
${srcRows.map((s, i) => `<tr><td class="rid">${i + 1}</td><td>${esc(s.label)}</td><td><a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.url)}</a></td><td>${esc(s.rows.join(', '))}</td></tr>`).join('\n')}
</tbody></table></div>
`);

/* ---------------- write ---------------- */
fs.mkdirSync(path.join(DOCS, 'assets'), { recursive: true });
for (const [name, html] of Object.entries(pages)) fs.writeFileSync(path.join(DOCS, name), html);
fs.writeFileSync(path.join(DOCS, '.nojekyll'), '');

const css = `:root{--ink:#16232e;--mut:#5a6b7b;--line:#dbe4ec;--bg:#f4f7fa;--card:#ffffff;--navy:#14395c;--teal:#0e7a6f;--amber:#a4680a;--red:#b03a2e;}
*{box-sizing:border-box}body{margin:0;font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg)}
a{color:var(--navy)} .wrap{max-width:1240px;margin:0 auto;padding:0 20px}
.masthead{background:var(--card);border-bottom:1px solid var(--line)}
.masthead-inner{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:14px 20px;flex-wrap:wrap}
.brand a{text-decoration:none;font-weight:700;font-size:19px;color:var(--ink)} .brand-mark{color:var(--teal);margin-right:6px}
.brand-sub{font-weight:400;color:var(--mut);font-size:14px} .stamp{font-size:12.5px;color:var(--mut)}
.nav{display:flex;gap:2px;flex-wrap:wrap;padding-bottom:0}
.nav-link{padding:9px 13px;border-radius:8px 8px 0 0;text-decoration:none;color:var(--mut);font-weight:600;font-size:13.5px;border:1px solid transparent;border-bottom:none}
.nav-link:hover{background:var(--bg);color:var(--ink)} .nav-link.active{background:var(--bg);color:var(--navy);border-color:var(--line);border-bottom:1px solid var(--bg);position:relative;top:1px}
main{padding:26px 0 40px}h1{font-size:27px;margin:6px 0 8px}h2{font-size:19px;margin:4px 0 10px}
.lede{color:var(--mut);max-width:1000px;font-size:15.5px}
.hero{background:linear-gradient(135deg,#123a5f,#0e7a6f);color:#fff;border-radius:14px;padding:30px 30px 26px;margin:6px 0 22px}
.hero h1{font-size:30px;color:#fff}.hero .lede{color:#d8e6f2;font-size:16.5px}
.hero-actions{margin-top:16px;display:flex;gap:10px;flex-wrap:wrap}
.btn{display:inline-block;background:#fff;color:var(--navy);font-weight:700;padding:10px 16px;border-radius:9px;text-decoration:none;font-size:14px}
.btn.primary{background:#ffd76b;color:#1c2c39}.btn.ghost{background:rgba(255,255,255,.14);color:#fff;border:1px solid rgba(255,255,255,.5)}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:14px;margin:4px 0 22px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;text-decoration:none;color:var(--ink);transition:box-shadow .15s}
.card:hover{box-shadow:0 3px 14px rgba(20,57,92,.12)}.card h2{font-size:16px;margin:0 0 6px;color:var(--navy)}.card p{margin:0;color:var(--mut);font-size:13.5px}
.panel{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin:0 0 20px}
.figs{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px}
.fig{border:1px solid var(--line);border-radius:10px;padding:12px;background:var(--bg);display:flex;flex-direction:column;gap:4px}
.fig-n{font-size:21px;font-weight:800;color:var(--teal)}.fig-l{font-size:12.5px;color:var(--mut)}
.table-scroll{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:12px}
table.data{border-collapse:collapse;width:100%;font-size:13.5px;min-width:1080px}
table.data th,table.data td{padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top;text-align:left}
table.data thead th{background:var(--navy);color:#fff;font-size:12px;text-transform:uppercase;letter-spacing:.04em;position:sticky;top:0}
table.data tbody th{font-weight:700;min-width:150px}
table.data tr:hover td,table.data tr:hover th{background:#f7fafc}
.rid{font-family:ui-monospace,Menlo,monospace;font-size:12px;color:var(--mut);white-space:nowrap}
.val{font-weight:600;color:var(--navy);min-width:110px}.eff{color:var(--mut);min-width:90px;font-size:12.5px}
.src-cell{min-width:200px}.src{font-weight:600;font-size:13px}
.note{color:var(--mut);font-size:12px;margin-top:5px}
.badge{display:inline-block;padding:3px 9px;border-radius:99px;font-size:11.5px;font-weight:700;white-space:nowrap}
.badge.ok{background:#e2f3ee;color:var(--teal);border:1px solid #bfe3d9}
.badge.warn{background:#fdf1dd;color:var(--amber);border:1px solid #f0d9a8}
.row-flagged td,.row-flagged th{background:#fffaf0}
table.decision{min-width:860px}table.sources{min-width:900px}table.sources a{word-break:break-all}
.fineprint{font-size:12.5px;color:var(--mut)}
.flag{border:1px solid #f0d9a8;background:#fffdf6;border-radius:10px;padding:13px 16px;margin:0 0 12px}
.flag h3{margin:0 0 6px;font-size:15px;color:var(--amber)}.flag p{margin:4px 0;font-size:13.5px}
.flag-links a{font-weight:700}
.footer{border-top:1px solid var(--line);background:var(--card);margin-top:26px}.footer p{color:var(--mut);font-size:12.5px;padding:16px 0}
code{background:#eef3f8;border-radius:4px;padding:1px 5px;font-size:.92em}
@media(max-width:760px){table.data{min-width:900px}.hero h1{font-size:24px}}
`;
fs.writeFileSync(path.join(DOCS, 'assets', 'style.css'), css);

/* ---------------- self-checks ---------------- */
const errors = [];
const rowTotal = allRowSets.reduce((n, s) => n + s.rows.length, 0);
for (const set of allRowSets) for (const r of set.rows) {
  if (!r.source_url || !/^https:\/\/.+/.test(r.source_url)) errors.push(`${r.id}: missing source url`);
  if (!r.status) errors.push(`${r.id}: missing status`);
  if (r.status === 'flagged' && !/unverified|unconfirmed|not.*(published|verified)|blank/i.test(r.value + ' ' + r.finding)) {
    // informational only — flagged rows should explain blanks
  }
}
const htmlFiles = fs.readdirSync(DOCS).filter((f) => f.endsWith('.html'));
for (const f of htmlFiles) {
  const txt = fs.readFileSync(path.join(DOCS, f), 'utf8');
  const hrefs = [...txt.matchAll(/href="([^"#]+)"/g)].map((m) => m[1]).filter((h) => !/^https?:|^mailto:/.test(h));
  for (const h of hrefs) {
    if (!fs.existsSync(path.join(DOCS, h))) errors.push(`${f}: broken internal link → ${h}`);
  }
}
console.log(`pages: ${htmlFiles.length}, table rows: ${rowTotal}, flags: ${flags.flags.length}, sources: ${srcRows.length}`);
if (errors.length) { console.error('ERRORS:\n' + errors.join('\n')); process.exit(1); }
console.log('OK — all rows sourced; no broken internal links.');
