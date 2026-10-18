# COORDINATION — MaltaProj8 Healthcare Work Requirements

**Session ID:** arena/5d32bca3-maltaproj8 (primary / integration session)
**Created:** 2026-10-18
**Last Updated:** 2026-10-18 19:30 UTC
**Status:** Active — all tasks done, pending PR/merge + Pages deploy verification

## Project Goal
Collect, organize, analyze full list following requirements for healthcare as US citizen CA permanent resident with 0 earned income, property manager + Kalshi trader, income from Kalshi futures, rental, savings interest. Executive summary, exact details of new law (H.R.1 §71119), CA provisions. No hallucinations, verified from official sources, links for manual review. GH Pages site with dashboard, tables, flagged review page.

## Task Board

| # | Task | Status | Owner | Files/Scope | Verification | Sources |
|---|------|--------|-------|-------------|--------------|---------|
| 1 | Repo initial review + COORDINATION.md setup | done | arena/5d32bca3 | COORDINATION.md, README.md | 2026-10-18 verified empty repo (Initial commit only) | github.com/buffedlizard55-lab/MaltaProj8 commit 375e859 |
| 2 | Research federal law H.R.1 §71119 + CMS IFR + verification table | done | arena/5d32bca3 | data/federal-law.json, law.html, verification.html | Verified line-by-line against congress.gov H.R.1 text + 91 FR 33348 + CMS Fact Sheet; every row has source link | congress.gov/bill/119th-congress/house-bill/1/text; federalregister.gov/documents/2026/06/03/2026-11094; cms.gov fact sheet |
| 3 | California Medi-Cal implementation research | done | arena/5d32bca3 | data/california.json, california.html, data/magi-limits.json | Verified against DHCS ACWDL 25-30, MEDIL I26-25, Implementation Plan, Tracking page, CHCF brief | dhcs.ca.gov/wp-content/uploads/2026/04/25-30.pdf; dhcs.ca.gov/wp-content/uploads/2026/09/MEDIL-I26-25.pdf; dhcs.ca.gov/federal-impacts/Documents/DHCS-HR1-Implementation-Plan.pdf |
| 4 | Income classification deep dive (Kalshi, rental, interest) | done | arena/5d32bca3 | data/income-types.json, income.html | Verified rental/interest/self-employment against IRS Pub 525, i8615, Sch C; Kalshi: verified ABSENCE of IRS guidance via 4 practitioner sources, flagged; §1256 flagged per IRC 1256(g)(1); gambling 90% cap verified via H.R.1 §70114 | irs.gov/publications/p525; irs.gov/instructions/i8615; dhcs.ca.gov MAGI chart; congress.gov H.R.1 §70114 |
| 5 | Work requirement fulfillment pathways for 0 earned income | done | arena/5d32bca3 | data/pathways.json, pathways.html | All 7 paths verified against DHCS ACWDL 25-30 + MEDIL I26-25 + CMS IFC; $580 income test verified as counting unearned; 6-mo avg verified via H.R.1 §71119(G) | dhcs.ca.gov/wp-content/uploads/2026/04/25-30.pdf; dhcs.ca.gov/wp-content/uploads/2026/09/MEDIL-I26-25.pdf |
| 6 | Executive summary (options, recommendations) | done | arena/5d32bca3 | docs/executive-summary.md, index.html | Full summary with 14 primary sources, inline citations, coverage table, scenario matrix; cross-checked against all data files | All of the above + HHS ASPE poverty guidelines; IRS PTC rules; CoveredCA What Counts |
| 7 | GH Pages site creation - landing + dashboard + tables | done | arena/5d32bca3 | index.html, law.html, california.html, income.html, pathways.html, exemptions.html, verification.html, flagged.html, site/assets/style.css, _config.yml, .github/workflows/pages.yml | Site builds with no broken internal links; Jekyll config validated; all data file links OK; all pages share nav; responsive | Local link check passed 2026-10-18; Jekyll build via actions/jekyll-build-pages |
| 8 | Final verification line-by-line + flagged irregularities page | done | arena/5d32bca3 | verification.html, flagged.html | Every claim audited in verification.html with source check; 10 flagged items + 3 irregularities on flagged.html | See verification.html section A–E |
| 9 | Final integration, PR, merge, GH Pages deploy | in progress | arena/5d32bca3 | .github/workflows/pages.yml, git push + PR | Pending push + PR creation + merge + deploy confirmation | — |

## Scope Lock Rules
- This session owns all files (solo session, no conflicts detected)
- This session's branch is arena/5d32bca3-maltaproj8 — all work on this branch, push only here, PR from here
- Files owned exclusively by this session — no overlapping parallel sessions observed
- Small frequent commits; git pull --rebase before every push
- Never mark verified without official source link — enforced on every table row

## Flagged Irregularities — Published on Site
See flag.html on GH Pages site. 10 flagged items: F-01 Kalshi NO IRS guidance, F-02 §1256 aggressive, F-03 gambling sports contract risk, F-04 all coverage-loss estimates are projections, F-05 high-unemployment threshold TBD, F-06 ACWDL 25-30 preliminary post-dated by IFC, F-07 enrollment point-in-time variance, F-08 Kalshi 1099 gap, F-09 H.R. 10357 pending legislation, F-10 full-price premium averages. Plus 3 low-severity irregularities (I-01 date metadata, I-02 age 13 vs 14 wording, I-03 effective date phrasing). Flagged items do NOT block merge — published on /flagged.html for post-launch review.

## Integration Log
- 2026-10-18 19:10: Session started, repo empty (only README.md + 375e859 Initial commit)
- 2026-10-18 19:11: Created COORDINATION.md, claimed all tasks (solo session)
- 2026-10-18 19:12: Research complete — federal law, CA, income types, IRS classification, HHS poverty guidelines; data JSONs created (federal-law.json, california.json, income-types.json, pathways.json, magi-limits.json)
- 2026-10-18 19:13: Executive summary written (docs/executive-summary.md) with 14 primary sources
- 2026-10-18 19:14: GH Pages site built — landing (index.html) + 6 subpages (law, california, income, pathways, exemptions, verification, flagged) + style.css + _config.yml + pages.yml
- 2026-10-18 19:15: Link integrity check passed — all internal data/docs/css links OK; JSON valid; no manual input required from user
- 2026-10-18 19:15: Verification log (verification.html) + Flagged for Review (flagged.html) completed
- 2026-10-18 19:30: Final COORDINATION.md update; ready to commit, push, and open PR
