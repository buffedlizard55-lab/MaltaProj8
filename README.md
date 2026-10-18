# MaltaProj8 — California Health Coverage Options for a Permanent Resident with No Earned Income

A research brief published as a static site on GitHub Pages:
**<https://buffedlizard55-lab.github.io/MaltaProj8/>**

## What this is

The question was: how does a California permanent resident (or citizen) who is a property
manager and full-time Kalshi trader, has **no earned income**, and has income from rental
property, savings interest and trading, obtain health coverage — and how do they satisfy
the new federal Medicaid "work" (community engagement) requirement that takes effect on
January 1, 2027?

Every value on the site traces to an official source (DHCS, Covered California, CMS, HHS,
IRS, DOL, CFTC, Congress.gov, the Federal Register, leginfo) and links to it. Where a value
could not be confirmed from an official source, it is **left blank** and published on the
**Flagged for Review** page instead of being estimated.

## Site map

| Page | File | What it covers |
|---|---|---|
| Overview | `index.html` | Executive summary, bottom line, income-band decision table, work-rule summary |
| Options | `options.html` | Four routes to coverage, side by side, plus a decision path |
| Work Rules | `work-requirements.html` | H.R. 1 § 71119 and AB 2161: who is subject, how to comply, exemptions, hardship, non-compliance, California implementation |
| Income | `income-counting.html` | MAGI, how rent / interest / trading are counted, the $580 test, 2026 FPL tables, worked examples |
| Medi-Cal | `medicaid-eligibility.html` | Coverage groups, 2026 income limits, asset rules, groups exempt from the work rule |
| Covered CA | `covered-california.html` | Federal premium tax credit, California Premium Subsidy, premiums, open enrollment, 2027 immigrant changes |
| Status | `immigration-status.html` | Green card / citizenship and what each immigration status means for Medi-Cal and marketplace help |
| 2026–27 Changes | `california-changes.html` | Every dated California change, plus what California is doing to soften the federal changes |
| Timeline | `timeline.html` | Every key date in order |
| Apply | `apply.html` | Where to apply, how to answer the income questions, what to gather, contacts |
| Flagged | `flagged.html` | Unverified items, discrepancies between official sources, pending guidance, scope notes |
| Sources | `sources.html` | All 40 official sources with publisher, type and date |

## Repository layout

```
index.html … sources.html      generated pages (committed, so Pages serves them from main)
assets/style.css               styles
assets/site.js                 nav toggle + per-table row filter
data/sources.json              the source register (id → publisher, URL, date)
data/page-*.json               page structure: headings, intros, section order
data/entries-*.json            every published table row, each with a source id
data/flagged.json              the Flagged for Review items
scripts/build_site.py          renders data/*.json → HTML
scripts/check_links.py         verification pass (data integrity + link/anchor check)
COORDINATION.md                shared task board and verification log
```

## Rebuild and verify

```bash
python3 scripts/build_site.py     # regenerate the 12 HTML pages from data/
python3 scripts/check_links.py    # verification pass; exits non-zero on any failure
```

`check_links.py` enforces the publication rules:

- every table row cites a source id that exists in `data/sources.json`;
- verified rows have a value; unverified rows have a **blank** value and a flag;
- every source URL is `https` and on an official government or state-marketplace domain;
- every internal link resolves to a file that exists, and every internal anchor to an id
  that exists;
- every page carries the navigation and a title.

Current status: **12 pages, 259 table rows (7 flagged/unverified), 40 sources — all checks pass.**

## Notes and limits

- Research brief, not legal, tax or immigration advice.
- Amounts are 2026 figures unless the row says otherwise; the work rule and the
  2026–27 changes are forward-looking and several pieces of federal guidance are still
  pending (see `flagged.html`).
- The federal minimum wage figure used in the $580 test is the FLSA figure ($7.25), not
  the California minimum wage.

Coordination with other agent sessions is tracked in [COORDINATION.md](COORDINATION.md).
