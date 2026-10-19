# California healthcare without earned income

**Live guide:** https://buffedlizard55-lab.github.io/MaltaProj8/

Research for a U.S. citizen living in California who reports no earned income and receives rental income, Kalshi event-contract results and savings interest. Primary finding review: **October 19, 2026**. This is information, not a personal eligibility or tax determination.

## Start here

- [Executive summary](https://buffedlizard55-lab.github.io/MaltaProj8/executive-summary.html)
- [Work rules and pathways](https://buffedlizard55-lab.github.io/MaltaProj8/work-rules.html)
- [Coverage options](https://buffedlizard55-lab.github.io/MaltaProj8/coverage-options.html)
- [All findings](https://buffedlizard55-lab.github.io/MaltaProj8/findings.html)
- [Evidence and review scope](https://buffedlizard55-lab.github.io/MaltaProj8/verification.html#current-review)
- [Flagged for Review](https://buffedlizard55-lab.github.io/MaltaProj8/flagged.html)

## Main answer

Zero wages do **not** mean zero countable healthcare income. The income alternative to the Medi-Cal community-engagement requirement uses MAGI-based household income, not gross rent deposits, trading payouts or wages alone. Other routes include qualifying activities, at least half-time education and specified exclusions. The seasonal-worker averaging alternative is not a general permission to average volatile trading results. Sources: [42 CFR 435.552](https://www.ecfr.gov/current/title-42/part-435/section-435.552), [California AB 2161](https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202520260AB2161), [HealthCare.gov income methods](https://www.healthcare.gov/income-and-household-information/income/).

The user's age, household size, current coverage, actual countable income and accepted work hours are unknown. No personal eligibility decision, premium or Kalshi tax classification is invented. Losing otherwise-available Medicaid for community-engagement noncompliance is **not** an automatic route to subsidized marketplace coverage ([CMS CIB §VII](https://www.medicaid.gov/federal-policy-guidance/downloads/cib12082025.pdf)).

## Data and ownership

- `data/core.json`: primary source register, 82 findings, pathway/coverage tables, flags and dated review locations.
- `data/review-evidence.json`: short official excerpts supporting high-impact findings; records the limits of retrieval.
- `scripts/build_core.py`: sole generator of the nine primary pages (dashboard, executive summary, work rules, playbook, coverage options, findings, verification, flags, archive index).
- `scripts/build_site.py`: extended reference pages; must not overwrite primary pages.
- `tools/build-site.js`: preserved `/docs/` reference dashboard.
- `research/` and `coverage-guide/`: independently authored, preserved research sections.
- `COORDINATION.md`: append-only session claims, source review, conflict resolution and deployment record.

Historical pages remain accessible. Some have direct-row citation gaps and outdated interpretations; they are **not freshly certified as current advice**. Their gaps are inventoried on the Flagged page. Official-domain validation checks provenance structure, not whether a document supports a claim. Current evidence locations identify section-level readings and limited official search-excerpt checks. No claim is made that every sentence of every inherited page or every external URL was reverified.

## Reproduce

Requires Python 3.11+ and Node.js 22; no third-party build packages.

```sh
python3 scripts/build_all.py
python3 scripts/check_core.py
python3 scripts/check_accuracy.py
python3 scripts/check_links.py
python3 scripts/check_integration.py
python3 coverage-guide/scripts/check.py
(cd research && python3 scripts/validate.py)
python3 scripts/stage_site.py
python3 scripts/check_integration.py --site dist
```

`build_all.py` renders the Docs and extended references first, and the core last. Running it twice must be deterministic. `check_integration.py` tests review metadata, known accuracy regressions, generator ownership, all local page/asset/fragment targets and the staged artifact. It is **not an automated legal fact checker or external URL availability guarantee**.

GitHub Actions validates pull requests using this same build. Only a successful main-branch build uploads and deploys the complete site to GitHub Pages. The published artifact excludes Git internals, caches and workflow files. No application, login, analytics or user-input form is required to read the research.

## Preview

```sh
python3 scripts/stage_site.py
python3 -m http.server 8000 --bind 0.0.0.0 --directory dist
```

## Important unresolved items

See the live Flagged page for complete details and official links: conflicting DHCS January/March wording, personal trading/owner-management hours, Kalshi tax character, current litigation outcome, missing personal facts, a budget PDF's omitted unit, and an extracted 2027 marketplace chart's missing dollar column. Unknown values are not treated as zero. Source publication dates are distinct from review/access dates.

### Pages compatibility
The complete-site Actions job deploys its validated artifact. Repository Pages settings currently remain in legacy mode; the integration cannot change that setting. The deployment job waits for the same commit’s automatic legacy build to finish before deploying the complete artifact, so the historical-reference banners and staged resources are the final publication.
