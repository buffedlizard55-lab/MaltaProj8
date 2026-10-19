# MaltaProj8 — California healthcare with zero earned income (2026–27)

**Verified guide** to Medi-Cal and Covered California for a U.S. citizen who is a California resident, a property manager, and a full-time Kalshi trader with **$0 earned income** and income from **rental property, savings interest, and Kalshi event contracts**.

> **Live site:** https://buffedlizard55-lab.github.io/MaltaProj8/
>
> **Verified:** 2026-10-19 · **Data:** `data/core.json` → 7 generated pages · 47 official sources · 79 findings · 28 flags · 10 routes · 6 coverage options

## The answer in five lines

1. **The work rule may not apply to you.** It governs only the Medi-Cal MAGI New Adult Group (adults 19–64, household MAGI at or below 138% FPL — **$22,025/year** or **$1,836/month** for one person in 2026, no asset test). Above that you are not in the group; **Covered California has no work requirement**.
2. **If you are in the group, earned income is irrelevant.** The $580/month test is measured on **MAGI-based household income** (42 CFR 435.552(f)(2); Cal. WIC §14005.69(e)(6)), so **net rental income, taxable interest, and realized gains count**. Zero wages does not mean zero countable income.
3. **Your second route is hours, not wages.** 42 CFR 435.552(b) counts work in exchange for goods or services (**in-kind**) and unpaid work. CMS's preamble gives the example of a **property manager or building superintendent who receives free or reduced rent** and says those hours count toward 80/month.
4. **You need one qualifying month per assessment period** — not every month. At renewal, any one month since the last determination; at application, the look-back month.
5. **If you fail it, do not assume a subsidy.** A noncompliant person is deemed Medicaid-eligible and is **not** eligible for federal premium tax credits. Cure within 30 days (California: 30 days from receipt, deemed received 5 days after the notice date; a 90-day return path applies).

## What was corrected on 2026-10-19

| Correction | Old claim | Verified position | Source |
|---|---|---|---|
| $580 test basis | "income from any source / total gross income" | MAGI-based household income; net rent, not gross receipts | [42 CFR 435.552](https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-C/part-435/subpart-F/section-435.552) · [AB 2161](https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202520260AB2161) |
| Six-month averaging | available to anyone with fluctuating income | statutory **seasonal worker** only | [42 CFR 435.552(g)](https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-C/part-435/subpart-F/section-435.552) |
| 2026 marketplace 400% FPL | $63,840 | **$62,600** (2025 guideline $15,650) | [IRS PTC eligibility](https://www.irs.gov/affordable-care-act/individuals-and-families/eligibility-for-the-premium-tax-credit) · [ASPE](https://aspe.hhs.gov/topics/poverty-economic-mobility/poverty-guidelines/prior-hhs-poverty-guidelines-federal-register-references) |
| APTC repayment | capped | **no cap** for tax years after 2025 (H.R.1 §71305) | [CRS R48633](https://www.congress.gov/crs-product/R48633) |
| California statute | not covered | **AB 2161, Ch. 209** — data-conflict rule, cure from receipt, deferral authority | [AB 2161](https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202520260AB2161) |
| H.R. 10357 | would restore 100% wagering-loss deduction | introduced text is digital-asset reform; the gambling fix is described by the sponsor for the committee substitute, not the published text | [H.R.10357](https://www.congress.gov/bill/119th-congress/house-bill/10357/text) · [Titus release](https://titus.house.gov/news/documentsingle.aspx?DocumentID=5932) |

## Site map

| Page | What it is |
|---|---|
| `index.html` | Dashboard: two gates, profile, 10 routes, options, California actions, key findings, flags |
| `executive-summary.html` | The executive summary, the exact law, options, California actions, risks, action plan |
| `work-rules.html` | The rule in detail, every route, what income counts, verification and cure |
| `coverage-options.html` | Medi-Cal, Covered California, Medicare, community health centers, income bands |
| `findings.html` | All 79 findings with a source link on every row + full source register |
| `verification.html` | Source register and the verification method |
| `flagged.html` | 28 open/closed irregularities and unverified values |
| `archives.html` | Index of older pages (each carries a **Superseded** banner) |

## Repo layout

```
data/core.json        Single source of truth for the 7 generated pages
scripts/build_core.py Generator; refuses to build if a row lacks a valid source
scripts/check_core.py Validator: source ids resolve, verified rows have values,
                      unverified rows are blank, every URL is official https
scripts/check_links.py Whole-site internal link/anchor check
COORDINATION.md       Shared task board and per-session verification log
```

## Build and verify

```bash
python3 scripts/build_core.py     # regenerate the 7 pages
python3 scripts/check_core.py     # data + page validator (exit 0 = pass)
python3 scripts/check_links.py    # every internal link and anchor resolves
```

Current result: **PASS** — 47 sources, 79 findings, 28 flags, 10 routes, 6 coverage options, 15 timeline events; 453 table rows across the 7 pages, every row carrying an official source link.

## Source policy

Every table row links to an official source (congress.gov, federalregister.gov, ecfr.gov, cms.gov, medicaid.gov, dhcs.ca.gov, aspe.hhs.gov, irs.gov, coveredca.com, cftc.gov, leginfo.legislature.ca.gov, oag.ca.gov, hrservices). A value that cannot be confirmed is **left blank and flagged** — never inferred. Where two official sources conflict (for example DHCS's "gross income" handout versus the codified MAGI rule, or the DHCS member letter's "March 2027" versus the January 1, 2027 statute), both are published on `flagged.html` with links.

This is a research compilation, not legal, tax, or eligibility advice. County eligibility staff make the final determination; a CPA should review the Kalshi tax classification.
