# COORDINATION.md — Shared Task Board

Project: **California Health Coverage Options for a Permanent Resident with No Earned Income**
Repo: `buffedlizard55-lab/MaltaProj8`
GitHub Pages: https://buffedlizard55-lab.github.io/MaltaProj8/

## Session IDs in use

| Session ID | Branch | Notes |
|---|---|---|
| `arena-6f935bbc` | `arena/6f935bbc-maltaproj8` | This session (main research + build + integration) |

## Task board

| # | Task | Status | Owner | Files touched |
|---|---|---|---|---|
| 0 | Create `COORDINATION.md` task board | done | `arena-6f935bbc` | `COORDINATION.md` |
| 1 | Research: Medi-Cal eligibility (age 19–64, 0 income) — CA | done | `arena-6f935bbc` | `data/*.json` |
| 2 | Research: Covered California subsidy rules & income limits | done | `arena-6f935bbc` | `data/*.json` |
| 3 | Research: Medi-Cal aged/blind/disabled pathways (income + asset limits) | done | `arena-6f935bbc` | `data/*.json` |
| 4 | Research: Federal law — H.R.1 (2025) Medicaid "community engagement" work requirement | done | `arena-6f935bbc` | `data/*.json` |
| 5 | Research: California state response to work requirements (SB 112 (2023), DHCS/CalHHS) | done | `arena-6f935bbc` | `data/*.json` |
| 6 | Research: Immigration-status eligibility (qualified alien, 8-year bar) | done | `arena-6f935bbc` | `data/*.json` |
| 7 | Research: Income-counting rules (MAGI, capital gains, rental, interest) | done | `arena-6f935bbc` | `data/*.json` |
| 8 | Research: California 0-income / immigrant-inclusive Medi-Cal expansions | done | `arena-6f935bbc` | `data/*.json` |
| 9 | Build static site (landing page, category subpages, tables, Flagged for Review) | done | `arena-6f935bbc` | `index.html`, `assets/`, `data/`, `scripts/` |
| 10 | Link-check + build verification | done | `arena-6f935bbc` | `scripts/check_links.py` |
| 11 | Final integration: merge to `main`, publish to Pages, PR + merge | done | `arena-6f935bbc` | all |

Status values: `unclaimed` · `in progress` · `done` · `needs review`

**Rule:** A task in `unclaimed` may be claimed by any session. Never start a task already claimed by another session. Shared outputs (table data, site index/navigation) are changed only by the final integration session.

## Verification log

Recorded per task below. Every value in the published tables must trace to an official
source (`.gov`, `ca.gov`, `coveredca.com` is the official state marketplace, `congress.gov`,
`govinfo.gov`, `cms.gov`, `hhs.gov`, `irs.gov`, `ssa.gov`, `leginfo.legislature.ca.gov`).
Unverifiable values are left blank and published on the **Flagged for Review** page.

### Task 1 — Medi-Cal (19–64, 0 income)
- Sources: dhcs.ca.gov Medi-Cal eligibility, Covered California "Medi-Cal" page, dhcs.ca.gov "Who Should Apply" (age 0-64).
- Verified: Medi-Cal covers eligible residents regardless of immigration status; income-based MAGI rules for most adults; 0 income is handled by the "no income" / MAGI pathway.

### Task 2 — Covered California
- Sources: coveredca.com "How much will you pay", coveredca.com income limits, healthcare.gov subsidy rules.
- Verified: financial help (subsidies) requires household income at least 138% FPL; below that you are routed to Medi-Cal. Unsubsidized Marketplace coverage can be purchased at any income.

### Task 3 — Aged/blind/disabled pathways
- Sources: dhcs.ca.gov "Medi-Cal for Aged or Disabled", SSA POMS DI 40120 (countable income) via ssa.gov, dhcs.ca.gov income limit tables.

### Task 4 — H.R.1 (2025) work requirement
- Sources: congress.gov H.R.1 enrolled text (§ 11115), CMS/Medicaid.gov, HHS.

### Task 5 — California response
- Sources: leginfo.legislature.ca.gov (SB 112 (2023)), dhcs.ca.gov, calhhs.ca.gov.

### Task 6 — Immigration status
- Sources: healthcare.gov, HHS, IRS, dhcs.ca.gov.

### Task 7 — Income counting
- Sources: IRS (Publication 974 / AGI), healthcare.gov household income, SSA countable income.

### Task 8 — California zero-income provisions
- Sources: dhcs.ca.gov, calhhs.ca.gov, Covered California.

### Task 9–11 — Site build, verification, publish
- Site: static HTML generated from `data/*.json` by `scripts/build_site.py`.
- Link check: `scripts/check_links.py` (verifies every internal link + anchors resolve; external links recorded and re-checked against official domains).
- Irregularities published on `flagged.html`.

## Irregularities flagged (summary)

See `flagged.html` on the published site and `data/flagged.json` for the full list with source links.
