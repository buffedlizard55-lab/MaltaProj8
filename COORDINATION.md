# COORDINATION.md — Shared Task Board

Project: **California Health Coverage Options for a Permanent Resident with No Earned Income**
Repo: `buffedlizard55-lab/MaltaProj8`
GitHub Pages: <https://buffedlizard55-lab.github.io/MaltaProj8/>

## Session IDs in use

| Session ID | Branch | Notes |
|---|---|---|
| `arena-6f935bbc` | `arena/6f935bbc-maltaproj8` | Research, build, verification, integration and publication |

## Task board

| # | Task | Status | Owner | Files touched |
|---|---|---|---|---|
| 0 | Create `COORDINATION.md` task board | done | `arena-6f935bbc` | `COORDINATION.md` |
| 1 | Research: Medi-Cal eligibility (age 19–64, 0 income) — CA | done | `arena-6f935bbc` | `data/*.json` |
| 2 | Research: Covered California subsidy rules & income limits | done | `arena-6f935bbc` | `data/*.json` |
| 3 | Research: Medi-Cal aged/blind/disabled pathways (income + asset limits) | done | `arena-6f935bbc` | `data/*.json` |
| 4 | Research: Federal law — H.R.1 / P.L. 119-21 § 71119 community engagement | done | `arena-6f935bbc` | `data/*.json` |
| 5 | Research: California implementation (ACWDL 25-30, 25-31, MEDIL I 26-25, AB 2161) | done | `arena-6f935bbc` | `data/*.json` |
| 6 | Research: Immigration status (LPR, 5-year bar, 2026 freeze, Oct 2026 reclassification) | done | `arena-6f935bbc` | `data/*.json` |
| 7 | Research: Income counting (MAGI, capital gains, rental, interest) | done | `arena-6f935bbc` | `data/*.json` |
| 8 | Research: California 2026–27 changes (asset limits, FFS, dental, premiums, renewals) | done | `arena-6f935bbc` | `data/*.json` |
| 9 | Build static site (landing page, category subpages, tables, Flagged for Review) | done | `arena-6f935bbc` | `index.html`, `assets/`, `data/`, `scripts/` |
| 10 | Link + data verification pass | done | `arena-6f935bbc` | `scripts/check_links.py` |
| 11 | Final integration: merge to `main`, publish to Pages, PR + merge | done | `arena-6f935bbc` | all |

Status values: `unclaimed` · `in progress` · `done` · `needs review`

**Rule:** A task in `unclaimed` may be claimed by any session. Never start a task already
claimed by another session. Shared outputs (table data, site index and navigation) are
changed only by the final integration session, after every other task is done.

## Verification log

Every published value was read directly from the official document cited in the row. No
value was inferred, interpolated, or carried over from a secondary source. Where an
official source could not be found, the value is blank and the row is flagged.

### Task 1 — Medi-Cal (19–64)
- DHCS "Eligibility by Federal Poverty Level" chart (updated 2026-10-15): 138% FPL annual
  limits $22,025 (1 person) … $108,247 (12), +$7,839 each additional.
- DHCS ACWDL 26-01 (2026-01-21) + Enclosures 1, 2, 3: monthly and annual 2026 FPL values,
  and the program-by-FPL chart (138% = ACA New Adults 19–64 **and** FPL Program for Aged &
  Disabled; 128% = Disabled Individuals in New Adult Group; 250% = Working Disabled Program;
  213%/322% = pregnant persons/MCAP; 266% = OTLIC children; 400+% = unsubsidized).
- Covered California "Medi-Cal" page: 138% FPL, apply any time of year, one application.
- HHS ASPE / 91 FR 1797 (2026-01-15): 2026 guideline $15,960 for one person.

### Task 2 — Covered California
- IRS "Premium tax credit (PTC) overview" (2026-07-28): income at least 100% and not more
  than 400% of the FPL; the 400% cap returned for 2026.
- Covered California 2027 FPL chart: premium contribution 0% below 138% FPL and 138–150%;
  2.8%–5.28% for 150–200%; 6.78%–8.66% for 200–250%; 8.66%–10.22% for 250–300%; 10.22%
  for 300–400%; "400+% FPL = Unsubsidized Coverage".
- Covered California news release (2026-07-21): $300 million 2027 California Premium
  Subsidy up to 200% FPL; open enrollment 2027-11-01 → 2027-01-31.
- Covered California enroller toolkits: 2026 state subsidy up to 165% FPL ($190M);
  2027 program design (preserve $0 Silver up to 150%, lower premiums 150–200%).

### Task 3 — Aged / blind / disabled pathways
- DHCS asset-limit FAQ: asset test applies to 65+, disability, nursing home, and families
  over the MAGI limit; $130,000 + $65,000/person through 2027-06-30; $21,000 / $31,000 +
  $1,550/person from 2027-07-01. MAGI-based Medi-Cal has no asset test.
- ACWDL 26-01 Enclosure 3: 138% FPL = FPL Program for Aged & Disabled.
- DHCS Medicare Savings Programs page: MSP asset limits from 2026-01-01.

### Task 4 — Federal law
- congress.gov (H.R. 1 enrolled text, P.L. 119-21) and CRS R48633 for the § 71119 text.
- CMS fact sheet (2026-06-01) and Federal Register interim final rule CMS-2454-IFC
  (2026-06-03): who is affected, the qualifying activities, the $580 income alternative,
  the exclusion list, short-term hardship options, verification and non-compliance.
- Medicaid.gov CMCS bulletin and slide deck (2025-12-08) for the statutory definitions,
  the $7.25 × 80 = $580 computation and the seasonal-worker rule.
- DOL: the federal minimum wage is $7.25 per hour (FLSA), effective 2009-07-24.

### Task 5 — California implementation
- ACWDL 25-30 (2025-12-30): exemption table, qualifying activities, look-back month,
  determination month, NNC procedure, six-month renewal look-back, members moving into and
  out of the MAGI New Adult Group, retroactive coverage, pending federal guidance list.
- ACWDL 25-31 (2025-12-30): six-month renewals.
- MEDIL I 26-25 (2026-09-11) and the enclosed member notice (2026-08-31): "an income from
  any source of at least $580 (before taxes) in any month since your last renewal"; the
  excuse list; 80 hours; part-time school; the consequence of losing Medi-Cal.
- AB 2161 (Bonta), Chapter 209, Statutes of 2026, chaptered 2026-09-15: WIC § 14005.69 as
  amended — definitions, the MAGI-based income test, exemptions, hardship, the 30-day
  notice and continued coverage, the data-conflict safeguard, the hearing requirement, the
  deferral clause and the 2029 regulation deadline.
- DHCS H.R. 1 Implementation Plan (2026) and the 2026-05 stakeholder deck.

### Task 6 — Immigration status
- DHCS "Immigration Status and Changes to Medi-Cal Eligibility": the full population table
  for January 2026 / January 2027 / July 2027.
- DHCS "Medi-Cal Changes": enrollment freeze, FFS transition, dental and premium changes,
  October 2026 federal reclassification.
- Covered California "Information for Immigrants": who keeps financial help in 2027 (LPRs,
  Cuban/Haitian entrants, COFA migrants), who loses it, and the public-charge note.

### Task 7 — Income counting
- HealthCare.gov "What to include as income": MAGI definition and the countable /
  non-countable income lists (capital gains, investment income, rental and royalty income,
  self-employment income, retirement, Social Security, tips, unemployment).
- 42 CFR 435.603 for the MAGI-based income and household rules.
- IRS Publication 527 for rental income; IRS PTC overview for the 100%/400% bounds.

### Task 8 — California 2026–27 changes
- DHCS "Medi-Cal Changes" calendar; DHCS asset-limit FAQ; DHCS stakeholder update
  (2026-01-05); ACWDL 26-07 (retroactive coverage); Covered California press release.

### Tasks 9–11 — Build, verification, publication
- Site: 12 static pages generated from `data/*.json` by `scripts/build_site.py`.
- Verification: `scripts/check_links.py` — 12 pages, **259 table rows** (7 flagged as
  unverified), 40 sources. Every row cites a source id; every verified row has a value;
  every unverified row has a blank value and a flag; every source URL is https on an
  official domain; every internal link and anchor resolves.
- Irregularities: 13 items published on `flagged.html` (see below).
- Deployment: GitHub Pages is configured for this repo (source `main`, path `/`), so the
  committed HTML at the repository root is what is served.

## Irregularities flagged (summary)

| ID | Item | Status |
|---|---|---|
| F-01 | Tax treatment of Kalshi trading gains (no IRS guidance located) | Unverified |
| F-02 | Property management: self-employment income vs. net rental income | Unverified — fact-dependent |
| F-03 | Statute / ACWDL / member notice describe the $580 test differently | Irregularity — definitional |
| F-04 | Member notice says March 2027; policy letters and statute say January 1, 2027 | Irregularity — date |
| F-05 | $1 differences between DHCS's 138% FPL chart and ACWDL 26-01 (sizes 2, 5, 7) | Irregularity — rounding |
| F-06 | Federal guidance pending on medically frail, self-attestation, verification | Pending federal guidance |
| F-07 | Definitions of "work program" and "community service" | Pending state guidance |
| F-08 | High-unemployment-county hardship exemption | Unverified — county-specific |
| F-09 | Public charge: sourced to Covered California only | Partially verified |
| F-10 | AB 2161 deferral clause can delay individual changes | Watch item |
| F-11 | California applies the work rule to state-funded adults; federal law does not require it | Irregularity — policy note |
| F-12 | The operative county letter for 2027 may be a later letter than ACWDL 25-30 | Needs review |
| F-13 | Scope note: MSP in depth, CalFresh/CalWORKs, IHSS, LTC, family glitch, county detail | Scope note |

Full text with source links for each item is published on `flagged.html` and in
`data/flagged.json`.

## Handoff log

- 2026-10-18 — Session `arena-6f935bbc` created the board and claimed tasks 0–11.
- 2026-10-18 — Research completed from official sources; site built; verification pass green.
- 2026-10-18 — Integration: PR opened from `arena/6f935bbc-maltaproj8` to `main`, merged,
  and GitHub Pages deployment confirmed.
