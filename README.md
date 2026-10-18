# California Coverage Guide

Official-source research dashboard on California healthcare eligibility and the 2027 Medicaid community-engagement rules, focusing on zero earned income, rentals, savings interest and own-account trading.

**Live site:** https://buffedlizard55-lab.github.io/MaltaProj8/

## Read first
- Executive summary: `index.html`
- Categories: `pages/` (work rules, income, exclusions, coverage, flagged items, sources)
- Evidence register: `research/findings.json`
- Coordination and deployment log: `COORDINATION.md`

Reviewed **October 18, 2026**. Not an eligibility determination or legal/tax advice. Individual financial amounts and Kalshi-specific classifications were not supplied or officially confirmed and remain unverified. Official date and rounding discrepancies are published, not silently resolved.

## Build and check
```sh
python scripts/seed_research.py  # editorial data → evidence JSON
python scripts/build.py          # evidence JSON → static HTML
python scripts/check.py          # rows, evidence, domains, local links, reproducibility
python -m http.server 8000 --bind 0.0.0.0
```

No dependencies, trackers, forms, credentials, third-party fonts or runtime APIs. Tables and source links work without JavaScript. JavaScript adds filtering; browser print saves a PDF. GitHub Pages serves the root of `main` using the repository's existing Pages configuration. CI checks the generated site on pull requests and main pushes.

## Verification scope
Each finding has an official source link and evidence note. Source register records retrieved text versus official search excerpts. This is row-scoped research, not an end-to-end audit of the entire federal law or 135-page rule. External sources were retrieved or located in official search results; build-environment egress does not permit automated HTTP checking of all external sites. Internal links and source structure are automatically tested. Missing personal determinations remain blank on Flagged for Review.
