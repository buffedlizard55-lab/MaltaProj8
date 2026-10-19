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
    <div class="brand"><a href="index.html"><span class="brand-mark">✚</span> Healthcare Access<span class="brand-sub"> — CA · no wages · source-linked, conditional findings</span></a></div>
    <div class="stamp">Source audit <strong>${VERIFY_DATE}</strong> · <a href="../accuracy-93fdc24b.html">Current correction</a> · <a href="../flagged.html">Open questions</a></div>
  </div>
  <nav class="wrap nav" aria-label="Primary">${nav}</nav>
</header>
<main class="wrap">
<section class="panel" role="note"><strong>Read first:</strong> The <a href="../accuracy-93fdc24b.html">dated accuracy update</a> separates 2026 and 2027 FPL years and uses the enacted MAGI-based work-rule method. Personal coverage, Kalshi tax character and actual income remain unknown. Older independent claims are preserved for review; see <a href="../flagged.html">Flagged for Review</a> and the <a href="../audit-6fc18b58.html">independent audit</a>.</section>
${body}
</main>
<footer class="footer"><div class="wrap">
  <p>Generated from <code>data/*.json</code> by <code>tools/build-site.js</code> (session <code>c8487e35</code>). Rows link to research sources, but a citation is not a personal eligibility determination. The <a href="../accuracy-93fdc24b.html">current accuracy update</a> and <a href="flagged-for-review.html">unresolved-items page</a> take precedence over older uncorrected descriptions. Informational, not legal or tax advice.</p>
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
<thead><tr><th>ID</th><th>Topic</th><th>General finding / limitation</th><th>Verified value, if available</th><th>Effective</th><th>Status</th><th>Official source</th></tr></thead>
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
  <h1>Healthcare in California without earned wages</h1>
  <p class="lede">For a U.S. citizen who lives in California and reports rental income, savings interest and Kalshi trading, eligibility depends on actual MAGI, household and other facts. No wages-only gate exists; no personal benefit or Kalshi tax classification can be promised from the facts supplied.</p>
  <div class="hero-actions"><a class="btn primary" href="executive-summary.html">Conditional coverage guide →</a><a class="btn" href="../accuracy-93fdc24b.html">Current source audit</a><a class="btn ghost" href="flagged-for-review.html">Open questions</a></div>
</section>
<section class="cards">
  <a class="card" href="executive-summary.html"><h2>Executive summary</h2><p>Routes with year-specific thresholds and a source per row.</p></a>
  <a class="card" href="income-taxes.html"><h2>Income &amp; taxes</h2><p>Taxable rent and interest, with Kalshi classification left unresolved.</p></a>
  <a class="card" href="medicaid.html"><h2>Medi-Cal</h2><p>2026 one-person MAGI reference: $22,025/year ($1,836/month); other eligibility conditions apply.</p></a>
  <a class="card" href="covered-california.html"><h2>Covered California</h2><p>Marketplace reference years and conditional premium-tax credits.</p></a>
  <a class="card" href="new-laws.html"><h2>New law &amp; work rule</h2><p>$580 MAGI-based income alternative or qualifying activity/exception from 2027.</p></a>
  <a class="card" href="action-plan.html"><h2>Apply &amp; prepare</h2><p>Gather records, check the relevant dates and obtain a county determination.</p></a>
  <a class="card" href="sources.html"><h2>Source register</h2><p>Official publications used in this section.</p></a>
  <a class="card" href="flagged-for-review.html"><h2>Flagged for Review</h2><p>Unknown values and prior claims that need narrower wording.</p></a>
</section>
<section class="panel">
<h2>2026–27 reference numbers are not interchangeable</h2>
<div class="table-scroll"><table class="data decision"><thead><tr><th>Program and year</th><th>Published one-person reference</th><th>What it does not prove</th><th>Official source</th></tr></thead><tbody>
<tr><td>2026 Medi-Cal MAGI expansion</td><td>138% FPL: <strong>$22,025/year; $1,836/month</strong></td><td>No individual's eligibility, 2027 Medi-Cal FPL or tax characterization.</td><td><a href="https://www.dhcs.ca.gov/services/medi-cal-resources/medi-cal-eligibility-division/all-county-welfare-directors-medi-cal-eligibility-division-information-letters/2026-fpl-calculation-chart-monthly-values-enclosure-1/">DHCS 2026 chart</a></td></tr>
<tr><td>2026 marketplace</td><td>400% FPL: <strong>$62,600/year</strong></td><td>Not guaranteed PTC/CSR at or below this number; other conditions apply.</td><td><a href="https://hbex.coveredca.com/data-research/dashboards/OE_Dashboard.pdf">Covered California 2026 dashboard</a> · <a href="https://www.irs.gov/affordable-care-act/individuals-and-families/eligibility-for-the-premium-tax-credit">IRS eligibility</a></td></tr>
<tr><td>2027 marketplace</td><td>400% FPL: <strong>$63,840/year</strong>; state help announced to <strong>200% FPL ($31,920)</strong></td><td>Not 2026 marketplace and not 2027 Medi-Cal; no automatic personalized quote.</td><td><a href="https://www.coveredca.com/pdfs/FPL-chart.pdf">2027 FPL chart</a> · <a href="https://www.coveredca.com/press-releases/2026/07/21/covered-california-rates-and-plans-for-2027-california-continues-fight-for-health-insurance-affordability-and-access">state program</a></td></tr>
<tr><td>2027 Medi-Cal MAGI expansion</td><td><strong>— Flagged</strong></td><td>A 2026 DHCS chart does not supply the 2027 figure.</td><td><a href="https://www.dhcs.ca.gov/services/medi-cal-resources/medi-cal-eligibility-division/all-county-welfare-directors-medi-cal-eligibility-division-information-letters/2026-fpl-calculation-chart-monthly-values-enclosure-1/">DHCS 2026 chart (not 2027)</a></td></tr>
</tbody></table></div>
<p class="fineprint">Source-linked general rules, not a personal determination. See the <a href="../accuracy-93fdc24b.html">full year-specific correction</a>.</p>
</section>
`);

pages['executive-summary.html'] = page('executive-summary.html', 'Executive Summary', 'executive-summary.html', `
<h1>Coverage without earned wages: the conditional answer</h1>
<p class="lede">A U.S. citizen living in California can seek MAGI Medi-Cal or a Covered California plan without wages. County/marketplace decisions depend on actual household income, age, coverage, tax characterization and other criteria. This summary does not decide eligibility. <a href="executive-summary.md">Long-form source audit (Markdown)</a>.</p>
<section class="panel"><h2>Available routes for the reported profile</h2><div class="table-scroll"><table class="data decision"><thead><tr><th>Route</th><th>What is established</th><th>Still unknown</th><th>Official source</th></tr></thead><tbody>
<tr><td>MAGI Medi-Cal</td><td>2026 one-person 138% FPL: $22,025/year; $1,836/month. MAGI program has no property limit. Work rule for covered adults begins Jan 1, 2027; six-month financial eligibility checks begin Mar 1, 2027.</td><td>Age, household, countable income, actual aid code, 2027 Medi-Cal FPL: <strong>—</strong>.</td><td><a href="https://www.dhcs.ca.gov/services/medi-cal-resources/medi-cal-eligibility-division/all-county-welfare-directors-medi-cal-eligibility-division-information-letters/2026-fpl-calculation-chart-monthly-values-enclosure-1/">DHCS FPL chart</a> · <a href="https://www.dhcs.ca.gov/medi-cal/help/">program rules</a> · <a href="https://www.dhcs.ca.gov/tracking-federal-impact-medi-cal-eligibility/">timeline</a></td></tr>
<tr><td>Covered California, possibly APTC</td><td>No work-hours gate to buy a plan. For 2026, 400% FPL is $62,600 for one person; 2027's 400% figure is $63,840. IRS credit criteria beyond income must also be met.</td><td>Tax-credit eligibility, actual premium and plan: <strong>—</strong>. Work-rule disqualification from Medi-Cal is not an automatic subsidized fallback.</td><td><a href="https://hbex.coveredca.com/data-research/dashboards/OE_Dashboard.pdf">2026 marketplace</a> · <a href="https://www.coveredca.com/pdfs/FPL-chart.pdf">2027 chart</a> · <a href="https://www.irs.gov/affordable-care-act/individuals-and-families/eligibility-for-the-premium-tax-credit">IRS PTC</a> · <a href="https://www.dhcs.ca.gov/wp-content/uploads/2026/09/MEDIL-I26-25.pdf">DHCS notice</a></td></tr>
<tr><td>Eligible Enhanced Silver / 2027 state help</td><td>Silver cost-sharing reductions have plan/income/other conditions (generally to 250% FPL). For 2027 California announced state premium aid up to 200% FPL ($31,920 for one person) for eligible marketplace applicants.</td><td>Plan, subsidy amount, CSR level: <strong>—</strong>.</td><td><a href="https://www.coveredca.com/costs/financial-help/">Covered CA financial help</a> · <a href="https://www.coveredca.com/press-releases/2026/07/21/covered-california-rates-and-plans-for-2027-california-continues-fight-for-health-insurance-affordability-and-access">2027 state help</a></td></tr>
<tr><td>Unsubsidized plan / other Medi-Cal groups</td><td>A marketplace plan without APTC may be purchased subject to enrollment rules; aged/blind/disabled and Medicare routes have distinct criteria.</td><td>Full price, alternative category: <strong>—</strong>.</td><td><a href="https://www.coveredca.com/shopandcompare/">Shop and Compare</a> · <a href="https://www.dhcs.ca.gov/medi-cal/help/">DHCS groups</a></td></tr>
</tbody></table></div></section>
<section class="panel"><h2>2027 community engagement — no wages-only gate</h2><div class="table-scroll"><table class="data decision"><thead><tr><th>Test</th><th>Operative rule</th><th>Personal result</th><th>Official source</th></tr></thead><tbody>
<tr><td>$580 monthly income alternative</td><td>California §14005.69(e)(6) and CMS §435.552(f) use monthly <strong>MAGI-based household</strong> income. Taxable rent and interest can count; gross deposits and Kalshi payouts do not automatically qualify.</td><td><strong>— Actual countable amount unknown</strong>.</td><td><a href="https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202520260AB2161">California law</a> · <a href="https://www.federalregister.gov/documents/2026/06/03/2026-11094/medicaid-program-community-engagement-requirement-for-certain-individuals">CMS rule</a></td></tr>
<tr><td>Month and averaging</td><td>Preceding month at application; a month between determinations at renewal. Prior-six-month averaging applies to <strong>seasonal workers</strong>, not every person with irregular trading results.</td><td><strong>— Seasonal-worker status unknown</strong>.</td><td><a href="https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202520260AB2161">§14005.69(d)–(e)(7)</a></td></tr>
<tr><td>Other activities and exceptions</td><td>80 hours/month of qualifying activity or combinations; qualifying at-least-half-time education; statutory exceptions and temporary hardship subject to program rules.</td><td><strong>— Hours/exemption not established</strong>.</td><td><a href="https://www.congress.gov/bill/119th-congress/house-bill/1/text">P.L. 119-21 §71119</a> · <a href="https://www.federalregister.gov/documents/2026/06/03/2026-11094/medicaid-program-community-engagement-requirement-for-certain-individuals">CMS rule</a></td></tr>
<tr><td>Rental, interest and Kalshi tax accounting</td><td>IRS rental-expense/loss rules and DHCS MAGI guidance govern countable amounts. The CFTC exchange designation does not decide this person's Kalshi tax classification.</td><td><strong>— Rental result, interest, trading character and monthly amount unknown</strong>.</td><td><a href="https://www.irs.gov/publications/p527">IRS Pub. 527</a> · <a href="https://www.dhcs.ca.gov/wp-content/uploads/2026/07/MAGI-INCOME-AND-DEDUCTION-TYPES.pdf">DHCS chart</a> · <a href="https://www.cftc.gov/PressRoom/PressReleases/8302-20">CFTC release</a></td></tr>
</tbody></table></div></section>
<section class="panel"><h2>What to do without making up a number</h2><p>Keep rental ledgers/allowable-expense records, interest statements and complete event-contract trade history; seek qualified tax advice on the unestablished contract classification. Apply at <a href="https://www.dhcs.ca.gov/medi-cal/apply/">DHCS</a> or <a href="https://www.coveredca.com/">Covered California</a>, and respond promptly to county notices. Read the <a href="../flagged.html">central Flagged for Review hub</a> or <a href="../accuracy-93fdc24b.html">dated correction</a>; earlier independently contributed pages should not override the operative cited law.</p></section>
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
<p class="lede">Every link cited anywhere on this site, in one table, for manual review. "Cited by" lists the row/flag IDs. Sources are chiefly U.S. federal/state government and Covered California; a listed link is a research reference, not a claim that every personal question is resolved.</p>
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
