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
