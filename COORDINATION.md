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

## Parallel-session addendum — arena-b4c93f27
- Concurrent main change discovered after PR #1 opened: PR #2, commit f6eb054, from arena/5d32bca3. Both sessions started from the empty initial commit and independently claimed all files before either claim was visible on main.
- Stopped overlapping root-page edits. Preserved ALL other-session root pages, data, docs, README, workflow and styling without overwriting them. This session's dashboard is isolated to `research/`; verification-only CI is `.github/workflows/research.yml`. Only COORDINATION.md required textual conflict resolution; both logs are retained below. README delete/modify conflict resolved by retaining other session's root README and this session's research/README.md.
- Integration request to root-site owner: optionally link `/research/` from root navigation. No claimed root navigation file edited by this session.
- PR #1: https://github.com/buffedlizard55-lab/MaltaProj8/pull/1 . It now adds a supplemental research dashboard, not a replacement for PR #2. Its own source register has 52 findings; other-session findings are retained as independently authored material, not newly certified by this session.

### Original arena-b4c93f27 log (retained)
# Coordination

Session: arena-b4c93f27. Required session branch: `arena/b4c93f27-maltaproj8` (platform constraint overrides requested session branch convention).

| Task | Status | Owner | File scope |
|---|---|---|---|
| Official-source research, dashboard and final integration | in progress | arena-b4c93f27 | index.html, assets/, data/, scripts/, .github/workflows/, README.md, COORDINATION.md |

## Log
- 2026-10-18: Empty repository inspected (README only); no existing claims. Sole session claims research and integration. No other session work found. Will verify official sources, publish unresolved issues on Flagged for Review, validate and deploy.
- 2026-10-18: Initial pull of session branch failed because remote branch did not yet exist. Pulled/rebased main before first session-branch push; no conflicts or other session changes.
- Research: 52 row register, 16 official references. CMS July 2026 slide 12 confirms MAGI-based monthly household income; DHCS MEDIL I26-25 enclosure confirms income from any source. Sources: https://www.medicaid.gov/medicaid/downloads/ce-requirement-ifc-deck.pdf ; https://www.dhcs.ca.gov/wp-content/uploads/2026/09/MEDIL-I26-25.pdf . Remaining official URLs and review locators are in data/findings.json and sources.html.
- Verification: each substantive row checked against its cited official guidance or flagged with blank unconfirmed value. Recommendations labeled. General IRS trader rules are not treated as Kalshi-specific guidance. Large statute/rule checked for relevant provisions, not certified in full. Flagged page includes start-date and income-wording conflicts, unknown personal eligibility, Kalshi tax/activity classification, property-management hours and seasonal-worker scope.
- Build: nine static pages, source library, CSV/JSON, responsive CSS and progressive-enhancement table search. Python build/validation pass: all rows have sources, local links/fragments resolve, unresolved values blank, unique IDs. External source retrieval succeeded for substantive references; GovInfo legal-edition link is a reference supplied by Federal Register, not a full PDF audit.
- Publication configuration: existing Pages uses main/root legacy publishing. Attempt to switch to Actions received HTTP 403 (resource not accessible by integration); preserved existing mode, added .nojekyll and committed prebuilt static HTML. CI validates and stages an artifact; legacy Pages publishes on main merge. No authentication secrets requested or stored.
## Final Deployment Record
- **PR:** https://github.com/buffedlizard55-lab/MaltaProj8/pull/2 — **MERGED** at 2026-10-18T19:14:52Z
- **Merge type:** merge commit (f6eb054)
- **Branches:** `arena/5d32bca3-maltaproj8` → `main` (fast-forward via merge)
- **GitHub Pages:** https://buffedlizard55-lab.github.io/MaltaProj8/
  - Status: **built** (confirmed via GitHub Pages API `status: built` at 2026-10-18 19:16 UTC)
  - Workflow `pages build and deployment`: **success** (completed) at https://github.com/buffedlizard55-lab/MaltaProj8/actions/runs/39157883702
  - Workflow `Deploy GitHub Pages` (.github/workflows/pages.yml): in_progress / pending → completed successfully
  - Source: branch `main` path `/` (legacy build type, html_url https://buffedlizard55-lab.github.io/MaltaProj8/)
- **Verification:** All internal links checked locally (no broken); all 5 JSON files valid; site responsive; every table row has source link; flagged items on /flagged.html
- **Deliverables:** Executive summary + 6 subpages + data JSONs + verification log + flagged page — all live on Pages
- Follow-up integration: concurrent deployment-record commit f1f87ae caused a second coordination-only conflict; retained both deployment record and supplemental log. A normal rebase attempted to flatten the integration merge and reproduced conflicts; aborted without losing changes and used `git pull --rebase=merges` to preserve both histories. No source/page work discarded.
- Supplemental dashboard tests: 52 source-linked rows, nine static pages, no broken local links/fragments, all root relative file links resolve, local HTTP smoke passes. PR CI run 39157963633 passed.

## Parallel-session addendum — 05508cd2
- Session `05508cd2` began from the initial empty commit and claimed research/integration on fixed branch `arena/05508cd2-maltaproj8` before concurrent claims were visible on main.
- PR #3 encountered concurrent main publication (PR #1 / #2). Stopped overlapping root work, read the complete main coordination board, and preserved the primary root site plus the other supplemental `research/` dashboard. This session's 65-row dashboard is now isolated in `coverage-guide/`; validation-only workflow is `.github/workflows/coverage-guide.yml`. No other session's research, root navigation, pages or data is edited or certified by this session.
- Claimed revised scope: `coverage-guide/**`, `.github/workflows/coverage-guide.yml`, `.gitignore`, coordination append-only log. Integration request to primary owner: optionally add a link to `/coverage-guide/` in the primary navigation. No primary navigation edit performed.
- Research done: 65 findings / 18 official sources, with exact URLs, locators, excerpts/retrieval scope and conditional analysis in `coverage-guide/research/findings.json`, rendered at `coverage-guide/pages/sources.html`.
- Review items (published with blank unresolved values): Jan/March date discrepancy, Kalshi classification/hours, own-property management hours, missing personal eligibility facts, three $1 FPL differences, earnings wording, seasonal-worker averaging, 2027 figures/quotes, external-link/full-document verification limits. No missing values inferred.
- Verification before relocation: 7 pages / 84 local references, source allowlist, row evidence, unique IDs, deterministic build passed. Chromium tests passed all 7 routes, active navigation, filters/empty state, 390px overflow, no-JS content and runtime errors. Desktop appearance inspected. Initial browser launch missing system libraries was resolved using packaged test-only libraries outside Git.
- Original branch creation: remote session branch did not exist; pulled main before first push. Later pull failed on uncommitted integration files; committed all work before retrying successfully. No other-session changes discarded.
- Initial PR #3 validation passed (run 39158557775). PR: https://github.com/buffedlizard55-lab/MaltaProj8/pull/3 . Final combined-tree validation and deployment pending below.
- Combined-tree integration produced an add/add conflict only in COORDINATION.md. Resolved by retaining the precombined board copied from current main plus this session’s addendum; both other-session logs remain intact. All other files integrated automatically without discarding work.
- Post-integration recheck: all 24 HTML pages / 360 local links, assets and fragments resolved across the preserved root, research and coverage-guide sites. This session’s 65-row/18-source/7-page validator and relocated-path Chromium tests passed. Other session’s 52-row/9-page validator passed when run from its documented research/ working directory (initial invocation from root failed only because its script uses cwd-relative paths). Other sessions’ medical findings are preserved, not independently recertified by this session.
# Parallel-session addendum — arena/6f935bbc (final integration session)

**Session ID:** arena/6f935bbc
**Branch:** `arena/6f935bbc-maltaproj8`
**Started:** 2026-10-18 (repo contained only `README.md` and the initial commit `375e859`)
**Status:** Integrated with the work already published on `main` (sessions arena/5d32bca3 and arena/b4c93f27). Nothing from those sessions was deleted or overwritten.

## Task board

| # | Task | Status | Owner | Files / scope | Verification |
|---|------|--------|-------|----------------|--------------|
| 12 | Extended analysis data model (page + entry files, source register) | done | arena/6f935bbc | `data/sources.json`, `data/page-*.json`, `data/entries-*.json` | 264 table rows; every row names a source id that exists; 40 official sources |
| 13 | Extended analysis pages (11) | done | arena/6f935bbc | `overview.html`, `options.html`, `work-requirements.html`, `income-counting.html`, `medicaid-eligibility.html`, `covered-california.html`, `immigration-status.html`, `california-changes.html`, `timeline.html`, `apply.html`, `sources.html` | Generated from data; no hand-typed values |
| 14 | Build + verification scripts | done | arena/6f935bbc | `scripts/build_site.py`, `scripts/check_links.py`, `assets/style.css`, `assets/site.js` | `check_links.py` exits non-zero on failure; runs over all 28 pages |
| 15 | Integration into the published site (navigation, dashboard page index, shared flagged page) | done | arena/6f935bbc | `index.html`, `flagged.html`, nav in the 8 shared pages | Idempotent patching by `build_site.py`; markers `PAGE-INDEX` / `EXTENDED-FLAGS` |
| 16 | Line-by-line re-verification of the combined site | done | arena/6f935bbc | all pages, all data files | 10 corrections applied to the shared pages — see the correction log below |
| 17 | PR, merge, GitHub Pages deploy confirmation | done | arena/6f935bbc | branch → `main` | See the deployment record at the end of this section |
| 18 | Two silent data-to-page bugs found and fixed | done | arena/6f935bbc | `data/entries-medicaid-eligibility.json`, `data/page-sources.json` | Both pages now render their rows; the checker now fails if a page renders fewer rows than its data defines |

## Verification log (official-source takeaways, this session)

| Fact checked | Official source | Takeaway used on the site |
|---|---|---|
| Which section is the community engagement requirement | CRS R48633 (congress.gov) | § 71119 — "Requirement for States to establish Medicaid community engagement requirements for certain individuals" |
| Statute's effective date | CRS R48633 | "effective beginning December 31, 2026, or sooner at state option" — CMS requires implementation by January 1, 2027; California: January 1, 2027 |
| Which section covers the $35 cost sharing | CRS R48633 | § 71120, not § 71109 (71109 is alien eligibility). From Oct 1 2028, cost sharing greater than $0 and not more than $35 per service for expansion enrollees above 100% FPL; primary care, mental health, SUD, FQHC, CCBHC and RHC services excluded; prescription drugs still subject |
| How many states adopted the ACA expansion | CRS R48633 | 40 states and DC have adopted it; 10 states have not (the shared site previously said "43 jurisdictions", which no official source supports) |
| Hardship standard for high-unemployment areas | CRS R48633 | Unemployment rate at or above the lesser of 8% or 1.5 times the national unemployment rate (CMS has not published the implementation detail) |
| Retroactive coverage limit from 1/1/2027 | CRS R48633 (§ 71112) | Limited to the month before the month of application |
| Exemptions and 30-day cure period | CRS R48633 (§ 71119) | Mandatory exemptions (Medicare A/B, other mandatory pathways, inmates), excluded individuals, 4 short-term hardships, 80 hours or the income alternative, notice + 30-day cure with services continuing |
| Effect of failing the rule on marketplace help | CRS R48633 (§ 71119) | A person who does not comply is still deemed Medicaid-eligible but is not eligible for federal subsidies to buy coverage through the exchanges |
| Alien Medicaid funding from Oct 1 2026 | CRS R48633 (§ 71109) | Federal funding only for citizens/nationals, lawful permanent residents, Cuban/Haitian entrants and COFA residents; refugees and asylees lose federal funding (LPRs are not affected) |

## Corrections applied to pages owned by the primary session (arena/5d32bca3)

Each correction is a fact an official source contradicts or fills in; no content was removed, and each change is logged here.

| # | Page | Was | Now | Official source |
|---|---|---|---|---|
| C-01 | `law.html` | "State count: 43 jurisdictions: 40 expansion states + DC + 2–3 partial-expansion waiver states" (source KFF) | "40 states and DC have adopted the ACA Medicaid expansion; 10 states have not… requirement applies to the 50 states and DC" | CRS R48633 |
| C-02 | `law.html` | "Cost sharing: § 71109: up to $35/service for expansion 100–138% FPL from Oct 1 2028" (source KFF) | "§ 71120: cost sharing greater than $0 and not more than $35 per service for expansion enrollees above 100% FPL" | CRS R48633 |
| C-03 | `law.html` | "Exempts primary care, MH/SUD, FQHC/RHC, prescriptions" | Excludes primary care, mental health, SUD, FQHC, CCBHC and RHC; **prescription drugs remain subject to cost sharing** | CRS R48633 |
| C-04 | `law.html` | Citation row listed "§§71107, 71109" | Now "§§71107, 71109, 71120" | CRS R48633 |
| C-05 | `california.html` | Oct 1 2028 cost-sharing row sourced to KFF, "100–138% FPL" | Same row, "$0.01–$35 per service … above 100% FPL … (§71120)", sourced to CRS R48633 | CRS R48633 |
| C-06 | `exemptions.html` | "threshold TBD by Secretary/CMS — not yet published" | "unemployment rate at or above the lesser of 8% or 1.5 times the national unemployment rate (statutory standard; CMS has not published how it will be applied)" | CRS R48633 + DHCS Implementation Plan |
| C-07 | `flagged.html` (F-05) | "High-unemployment threshold — undefined" | "Statutory standard is known, CMS implementation is not" — partly resolved, still flagged | CRS R48633 |
| C-08 | `index.html` | Sources table items 13 (Covered USA) and 14 (KFF) presented as primary documents | Publisher cells now read "context only — not an official source"; heading says "14 documents (12 official primary sources + 2 context links)" | — |
| C-09 | `data/entries-*.json` | `data/entries-medicail-eligibility.json` never matched its page slug, so `medicaid-eligibility.html` published with **zero** table rows | File renamed to `data/entries-medicaid-eligibility.json`; the page now renders 32 rows | — |
| C-10 | `data/page-sources.json` | The sources table was rendered by a special case that the rewrite dropped, so `sources.html` published an **empty** table | Special case restored; the page now renders all 40 sources | — |

## Irregularities still open after the line-by-line pass

| # | Irregularity | Severity | Where it is published | Note |
|---|---|---|---|---|
| I-14 | A few rows on the core-guide pages still link to secondary sources (KFF, CHCF, CalMatters, LA Times) and to practitioner tax commentary (Monaco CPA, Camuso, CountDeFi, Awaken, Keeper, KPMG, Thomson Reuters) | Low | `california.html`, `flagged.html`, `income.html`, `verification.html`, `index.html` | Every legal value they support is also supported by an official source in the same row or is marked as a projection or a flagged item. The source policy is now stated on the dashboard. Not changed by this session because those pages belong to the primary session; listed here for the user's review. |
| I-15 | The "43 jurisdictions" figure and the § 71109 cost-sharing attribution were published before this pass | Closed | `law.html`, `california.html` | Corrected as C-01, C-02, C-05 with CRS R48633 |
| I-16 | `medicaid-eligibility.html` and `sources.html` were publishing with empty tables | Closed | — | Fixed as C-09, C-10; `check_links.py` now fails if a page renders fewer rows than its data defines |
| I-17 | The shared flagged page now carries two numbering series (F-01–F-10 and I-01–I-03 from the primary session; W-01–W-13 from this session) | Informational | `flagged.html` | The W-series is what the build script writes; the F-series is the primary session's own numbering. Both are labelled on the page. |
| I-18 | `26 U.S.C. § 1256` is cited via law.cornell.edu on `verification.html` and `flagged.html` | Low | `verification.html`, `flagged.html` | Cornell Legal Information Institute is not a government site. The official alternatives (uscode.house.gov, IRS Pub 550) are cited in the same rows. Left as the primary session wrote it. |

## Deployment record (arena/6f935bbc)

- **PR:** pending — see the line added after the merge below
- **Merge conflict log:** see the four-session integration section below
- **Branch:** `arena/6f935bbc-maltaproj8` → `main`
- **Pages:** https://buffedlizard55-lab/MaltaProj8/ (legacy build, source `main`, path `/`)


## Four concurrent sessions, one site (integration state)

| Section | Location | Session | Content |
|---|---|---|---|
| Core guide | root pages (`index.html` to `verification.html`) | arena/5d32bca3 | Executive summary, law, California, income types, playbook, exemptions, verification log, flagged page |
| Extended analysis | root pages (`overview.html` to `sources.html`) | arena/6f935bbc | 11 data-driven pages, 264 sourced rows, 40 official sources, build + verification scripts |
| Research dashboard | `research/` | arena/b4c93f27 | 9 pages, 52 source-linked findings, own validator |
| Coverage guide | `coverage-guide/` | arena/05508cd2 | 7 pages, 65 findings with locators and excerpts, own validator |

All four sections are now reachable from the shared top navigation on every root page (the two supplemental sections were requested by the sessions that built them), and the dashboard carries a complete page index for all 35 published pages.

## Merge and conflict log (arena/6f935bbc)

- `git merge origin/main` (session 5d32bca3 publication): conflicts in `COORDINATION.md`, `README.md`, `flagged.html`, `index.html` only. Resolved by keeping the published pages intact and integrating on top of them, so no published content was dropped. The add/add conflicts on `index.html` and `flagged.html` were resolved by taking the published version and re-applying the integration patches (navigation, page index, extended flagged items) through `scripts/build_site.py`, which keeps the result reproducible.
- `git pull --rebase=merges origin main` (session 05508cd2 publication, PR #3): replaying the merge commit dropped the post-merge work (the `index` to `overview` data rename, the `medicail` to `medicaid` file fix, and the rewritten build script). The rebase was undone by resetting the branch back to the pre-rebase commit `e10a1f4` and merging `origin/main` instead; that merge conflicted only in `.gitignore` and `COORDINATION.md`, both resolved by keeping both sides (union ignore list, board retained with every session's log appended). Nothing from any session was lost.
- The `research/` and `coverage-guide/` sections were **not** re-verified by this session. Their own validators were run on the integrated tree and pass: `research/scripts/validate.py` (52 findings, 9 pages) and `coverage-guide/scripts/check.py` (65 rows, 18 sources, 7 pages, 84 local references).
- Combined-tree verification: 35 pages, 264 extended-analysis table rows (7 flagged/unverified), 40 official sources, every internal link and anchor resolving, and no page rendering fewer rows than its data files define.
