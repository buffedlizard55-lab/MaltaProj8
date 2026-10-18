# MaltaProj8 — California Healthcare & Work Requirements (2026 Guide)

**Executive summary and verified analysis** of Medicaid/Medi-Cal work requirements under **H.R.1 / P.L. 119-21 (One Big Beautiful Bill Act)** for a California resident with **zero earned income** whose income comes from **Kalshi futures trading, rental income, and savings account interest**.

> **Live site:** https://buffedlizard55-lab.github.io/MaltaProj8/ (GitHub Pages)
>
> **Status:** Active · Branch `arena/5d32bca3-maltaproj8` → `main` via PR

## Quick Answer

**You do NOT need earned income to keep Medi-Cal / Covered California.** The $580/month income test counts *any* countable income — rental net, Kalshi gains, interest all qualify. Volunteering, education, or work programs are fallbacks. See the Executive Summary on the site.

## Repo Layout

```
├── COORDINATION.md          # Shared task board / verification log
├── docs/
│   └── executive-summary.md # Full executive summary (source of truth)
├── data/
│   ├── federal-law.json     # H.R.1 §71119 + CMS IFR provisions (verified)
│   ├── california.json      # DHCS implementation, timelines, mitigation
│   ├── income-types.json    # How each income type is classified + counted
│   ├── pathways.json         # 7 ways to satisfy work requirement with 0 earned income
│   ├── magi-limits.json     # FPL / MAGI income limits 2026
│   ├── sources.json         # Source register for the Extended Analysis (S1–S40)
│   ├── flagged.json         # Open questions for the Extended Analysis (F-01–F-13)
│   ├── page-*.json          # Page definitions (sections, headings, intros)
│   └── entries-*.json       # Table rows for each page, each with a source id
├── scripts/
│   ├── build_site.py        # Renders the Extended Analysis pages from data/
│   └── check_links.py       # Verification pass over the whole site
├── assets/                  # Extended Analysis theme + table filter
├── site/
│   └── assets/style.css     # Site theme
├── index.html               # Landing page (dashboard) ← GH Pages entry
├── law.html                 # The new law — line-by-line
├── california.html          # California / Medi-Cal
├── income.html              # Income types deep dive
├── pathways.html            # 0-earned-income playbook
├── exemptions.html          # Who is exempt
├── verification.html        # Line-by-line source log
├── flagged.html             # Flagged for Review
├── _config.yml
└── .github/workflows/pages.yml
```

## Verification

Every table row links to an **official source** (congress.gov, federalregister.gov, cms.gov, dhcs.ca.gov, irs.gov, aspe.hhs.gov). If a value could not be confirmed from an official source, it is left blank and flagged on the Flagged for Review page. See `verification.html` on the site or `COORDINATION.md` for the verification log.

### Automated verification (runs against the whole site)

```bash
python3 scripts/build_site.py     # rebuilds the Extended Analysis pages from data/
python3 scripts/check_links.py    # verification pass; exits non-zero on any failure
```

`scripts/check_links.py` checks that every data file parses, that every published table row names a source id that exists, that verified rows carry a value and unverified rows are blank and flagged, that every source URL is https on an official domain, that every internal link and anchor on all 28 published pages resolves, that every page has a navigation and a title, and that every page renders the rows its data files define. Current result: **28 pages, 264 table rows (7 flagged/unverified), 40 sources, all checks pass.**

## Extended Analysis (second section of the site)

The site has three verified sections, all linked from the dashboard:

| Section | Pages | Session |
|---|---|---|
| Core guide | `index.html`, `law.html`, `california.html`, `income.html`, `pathways.html`, `exemptions.html`, `verification.html` | arena/5d32bca3 |
| Extended analysis | `overview.html`, `options.html`, `work-requirements.html`, `income-counting.html`, `medicaid-eligibility.html`, `covered-california.html`, `immigration-status.html`, `california-changes.html`, `timeline.html`, `apply.html`, `sources.html` | arena/6f935bbc |
| Research dashboard | `research/` (9 pages, 52 source-linked findings) | arena/b4c93f27 |

The Extended Analysis pages are generated from `data/page-*.json` and `data/entries-*.json` by `scripts/build_site.py`, with the source register in `data/sources.json` (40 official sources) and the open questions in `data/flagged.json` (13 items). The shared pages (`index.html`, `flagged.html`) and the site navigation are patched by the same script, so the dashboard, the flagged page and the top navigation stay in sync with the data.

## Sources (Primary)

1. H.R.1 full text (P.L. 119-21): https://www.congress.gov/bill/119th-congress/house-bill/1/text
2. CMS-2454-IFC (91 FR 33348, Jun 3 2026): https://www.federalregister.gov/documents/2026/06/03/2026-11094/medicaid-program-community-engagement-requirement-for-certain-individuals
3. CMS Fact Sheet (Jun 1 2026): https://www.cms.gov/newsroom/fact-sheets/medicaid-community-engagement-requirement-certain-individuals-interim-final-rule-comment-period-cms
4. DHCS ACWDL 25-30 (Dec 30 2025): https://www.dhcs.ca.gov/wp-content/uploads/2026/04/25-30.pdf
5. DHCS MEDIL I26-25 (Sep 1 2026): https://www.dhcs.ca.gov/wp-content/uploads/2026/09/MEDIL-I26-25.pdf
6. DHCS Implementation Plan (Jan 29 2026): https://www.dhcs.ca.gov/federal-impacts/Documents/DHCS-HR1-Implementation-Plan.pdf
7. DHCS Tracking Federal Impact: https://www.dhcs.ca.gov/tracking-federal-impact-medi-cal-eligibility/
8. HHS ASPE 2026 Poverty Guidelines: https://aspe.hhs.gov/topics/poverty-economic-mobility/poverty-guidelines

All 14 primary sources are linked directly on the Executive Summary page.

## Coordinating Sessions

Before starting, read [COORDINATION.md](COORDINATION.md). It is the shared task board. Claim a task, commit and push the claim immediately, work only in your claimed file scope.

## License

Research compilation — sources cited inline. No legal advice; consult an attorney/CPA for individual determinations.
