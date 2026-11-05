# Financial Data Source Verification

Updated: 28 October 2026. Historical disclosure cutoff: 24 October 2026.

## Verification terminology

- `pending_review`: underlying evidence not yet checked.
- `company_source_checked`: a company disclosure was checked for its reported amount, scope and date.
- `original_source_checked`: claim-table terminology for checking the original disclosure; equivalent to company_source_checked for these company-source snapshots.
- `external_report_checked`: the cited external report was read; this does not establish independently audited financial accuracy or an independent financial reconstruction.
- `independently_corroborated`: reserved for documented additional independent evidence; not assigned to the current five snapshots.

## Current verification register

| Snapshot | Reference date | Amount, million | Currency | Qualifier | Scope | Review status | Source |
|---|---|---:|---|---|---|---|---|
| FS001 | 2026-07-07 | 650 | EUR | lower_bound | public_and_private | company_source_checked | [S001](https://www.proximafusion.com/press-news/proxima-fusion-raises-eu411-million-to-build-europes-commercial-fusion-champion) |
| FS002 | 2026-07-30 | 4000 | USD | approximate | reported_capital_raised | company_source_checked | [S004](https://cfs.energy/news-and-media/commonwealth-fusion-systems-raises-another-1-billion-bringing-total-capital-raised-to-4-billion/) |
| FS003 | 2026-10-06 | 400 | USD | lower_bound | reported_total_funding | external_report_checked | [S010](https://www.ksl.com/article/51632922/fusion-firm-type-one-in-200-million-siemens-energy-backed-raise) |
| FS004 | 2026-05-27 | 130 | USD | reported | private_investment | external_report_checked | [S011](https://techcrunch.com/2026/05/27/with-a-new-100m-raise-princetons-thea-energy-is-now-a-top-funded-fusion-startup/) |
| FS005 | 2024-11-20 | 335 | USD | reported | private_and_government | company_source_checked | [S005](https://tokamakenergy.com/2024/11/20/tokamak-energy-raises-125m-to-commercialise-transformative-fusion-and-magnet-technologies/) |

FS001 now relies on dated S001 rather than the undated company overview. FS003 is supported by the Reuters report hosted on KSL. FS004 remains a historical May disclosure, with a later undisclosed extension discussed in chapter 03. Source locators are recorded in claim_sources.csv.

## Review history

The initial verification register described FS003/FS004 as independently corroborated. The enhancement review corrected that wording to external_report_checked: publication in external media is not itself financial audit evidence. The first funding-audit pass and its subsequent update are preserved in [chapter 07](07_funding_audit.md).

## Continuing limitations

Cumulative snapshots and individual rounds must not be summed. Commitments, budgets, awards, PPAs and cash received remain distinct. Company totals have different dates and definitions. Unknown amounts are not zero. Full historical funding coverage and detailed financing terms remain outside this initial baseline.
