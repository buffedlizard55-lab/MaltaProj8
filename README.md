# California Coverage Guide

Official-source healthcare research for a California-resident U.S. citizen with no wage income, focused on Medicaid community engagement requirements and non-wage income.

**Live site:** https://buffedlizard55-lab.github.io/MaltaProj8/

## Contents
- Executive summary; income and trading; compliance options; law and timeline
- Exclusions and exceptions; California support; coverage roadmap
- Flagged for Review (unconfirmed values blank) and official source library
- Downloadable CSV and JSON containing stable row IDs, official source references, locators, status and review date

Research date: **October 18, 2026**. General rules are distinguished from personal eligibility, which is not determined. Important unresolved issues include conflicting DHCS timing/income language, Kalshi tax classification and personal trading/property-management hour acceptance. No claim that every provision of the entire law was audited. No advice to misreport income or fabricate work.

## Build and validation
Python 3.10+; no third-party build dependencies.

```sh
python scripts/build.py
python scripts/validate.py
python -m http.server 8000 --bind 0.0.0.0
```

Edit `data/findings.json`, then regenerate the committed HTML and CSV. The site works without JavaScript; JavaScript only filters the tables. Relative links work under the GitHub project Pages path. No analytics or personal information collection.

CI checks source references, blank unresolved fields, unique IDs, and every internal link/fragment. External sources were inspected through research retrieval; automated local validation does not claim to certify external uptime or individual eligibility. The source library records review locations. Federal Register's web text is agency-hosted but not the official legal edition; the GovInfo PDF is linked for legal reliance.

`.github/workflows/pages.yml` builds and validates PRs and main and uploads a staged website artifact. GitHub Pages is already configured for legacy publication from main at `/`; committed static HTML is therefore published on merge. Switching Pages to Actions returned HTTP 403, so the existing publication mode is preserved. See `COORDINATION.md` for task ownership and release log.
