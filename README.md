# MaltaProj8 — California healthcare with $0 earned income (2026–27)

**Verified guide** for a U.S. citizen who is a California resident, a property manager, and a full-time Kalshi trader with **$0 earned income** and income from **net rental property, savings interest, and Kalshi event contracts** — including how to satisfy the new Medi-Cal work requirement.

> **Live site:** https://buffedlizard55-lab.github.io/MaltaProj8/
>
> **Verified:** 2026-10-19 · 46 official sources · 75 findings · 32 flags · 9 routes · 6 coverage options
>
> Every table row on the site links to an official source. Values that could not be confirmed are blank and flagged.

## The answer

1. **Check the gate first.** The work rule applies only to non-pregnant adults 19–64 in the Medi-Cal **MAGI New Adult Group**: household MAGI at or below **138% FPL** ($22,025/year or $1,836/month for one person in 2026), no asset test, not on Medicare. Above that limit, **Covered California has no work requirement at all**.
2. **Earned income is not the test.** The $580/month alternative is measured on **MAGI-based household income** (42 CFR 435.552(f)(2); Cal. WIC §14005.69(e)(6)). **Net** rental income, interest and recognized gains count; gross rents do not.
3. **Hours count even without wages.** 42 CFR 435.552(b) counts in-kind and unpaid work. The IFR preamble says a **property manager or building superintendent** receiving free or reduced rent counts those hours toward 80/month.
4. **One qualifying month per review period** is enough under California's current guidance — not every month. At application the county looks at the month before you apply.
5. **Failing the rule does not open a subsidy.** A non-compliant person is still deemed Medicaid-eligible and cannot receive federal premium tax credits. Cure within 30 days (coverage continues); a fair hearing is available afterwards.

## What this repo gets right that generic guides miss

| Point | Why it matters |
|---|---|
| **Net, not gross, rent** | A landlord collecting $2,000 in rent may have countable income far below that. MAGI uses Schedule E net. |
| **Kalshi losses may not reduce MAGI** | If trading is treated as gambling, winnings sit in AGI and losses are an itemized deduction — so a losing year can still produce MAGI. Character is unresolved. |
| **In-kind rent can be income too** | Free rent earned by managing someone else's building is barter income at fair market value, which also raises MAGI. |
| **A W-2 is not required** | Hours of documented owner-management work can satisfy the rule if the county accepts them. |
| **The $580 test is household income** | A spouse's income counts if you are in the same MAGI household. |
| **California's guidance conflicts with itself** | DHCS says "work and earn $580", "income from any source", and "MAGI-based"; the statute and regulation control. Flagged, not smoothed over. |

## Site map

| Page | Contents |
|---|---|
| `index.html` | Dashboard: two gates, profile, 9 routes, coverage options, California actions, key findings, flags |
| `executive-summary.html` | The one-page answer, exact law, options, California actions, risks, action plan |
| `work-rules.html` | The rule in detail: who is subject, routes, the $580 test, verification, penalties |
| `playbook.html` | **The working plan:** four routes, what counts as MAGI, evidence pack, 2026–27 calendar, failure path |
| `coverage-options.html` | Medi-Cal, Covered California, Medicare, community health centers, income bands |
| `findings.html` | All 75 findings in one table plus the full source register |
| `verification.html` | Source register, method, corrections, limits |
| `flagged.html` | 32 irregularities and unverified values, each with a source |
| `archives.html` | Index of older pages (status-labelled; not re-certified) |

## Repo layout

```
data/core.json          single source of truth for the nine generated pages
scripts/build_core.py   generator; refuses to build a row without a valid source
scripts/check_core.py   validator: ids resolve, verified rows have values,
                        unverified rows are blank, URLs are official https
scripts/check_links.py  whole-site internal link and anchor check
COORDINATION.md         shared task board and per-session verification log
```

Older data files (`data/*.json`), the `research/`, `coverage-guide/` and `docs/` sub-sites, and the legacy root pages are preserved for the audit trail. They are **not** re-certified; where one conflicts with the core pages, the core pages and the official source control.

## Build and verify

```bash
python3 scripts/build_core.py     # regenerate the core pages
python3 scripts/check_core.py     # data + page validator (exit 0 = pass)
python3 scripts/check_links.py    # internal links and anchors
```

Current result: **PASS** — 46 sources, 75 findings, 32 flags, 9 routes, 6 coverage options, 13 timeline events; 477 table rows checked, every one carrying an official link.

Do **not** run `scripts/build_site.py` after `build_core.py`; it regenerates the legacy pages and re-injects superseded content (CR-07).

## Source policy

Statute on congress.gov, the rule on federalregister.gov and ecfr.gov, agency guidance on cms.gov, medicaid.gov and dhcs.ca.gov, tax material on irs.gov, and official tables from coveredca.com and leginfo.legislature.ca.gov. News coverage is never the source of a value. When two official sources conflict, both are published on `flagged.html` with links.

This is a research compilation, not legal, tax, or eligibility advice. County eligibility staff make the final determination, and the Kalshi tax characterisation needs a CPA.
