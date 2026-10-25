# Fusion Energy Strategy — Source Review (Stage 1)

**Project:** The Economics of Commercial Fusion: A Data-Driven Market and Strategic Analysis of Proxima Fusion  
**Review date:** 24 October 2026  
**Status:** Initial source review. Findings verified against accessible official publisher summaries and institutional statements; these notes are **not** a page-by-page audit of the full FIA/F4E reports. Full report tables and precise methodology must be checked before their use in final analysis.

## Research hypotheses
- **H1 — Economic competitiveness:** Stellarator plants could be economically competitive under sufficiently favorable CAPEX, net output, availability and operating conditions.
- **H2 — Partnerships:** Utility and public-sector partnerships may reduce capital burden and commercialization risks borne by Proxima.
- **H3 — Scalability:** Standardization and manufacturing learning may reduce the cost of stellarator deployment.

---

## S01 — Fusion Industry Association (FIA)

**Title:** *The Global Fusion Industry in 2026* (sixth annual report)  
**Published:** 13 July 2026 (release)  
**Publisher/type:** Fusion Industry Association; private-company voluntary survey  
**Source:** https://www.fusionindustryassociation.org/fusion-industry-attracts-record-annual-funding-of-4-48bn-raising-total-to-14-24bn/  
**Full-report portal:** https://www.fusionindustryassociation.org/fusion-industry-reports/

### Relevant findings
1. Reported investment in private fusion has expanded substantially: $4.48bn was raised in the 12 months up to July 2026, 69% more than the preceding survey year.
2. The survey includes 56 private fusion companies. The reported industry now employs more than 16,000 people.
3. Commercial preparation is beginning before proven grid-scale deployment: six companies reported siting agreements and five reported a PPA, offtake agreement or similar commercial commitment.
4. The largest reported short-term challenges include funding (67% of respondents), power efficiency (64%) and neutron-resilient materials (64%). These are not independent measures of technical feasibility.
5. Surveyed companies employ multiple technological concepts: magnetic confinement accounts for 48% of respondents, inertial confinement 21%, and magneto-inertial approaches 14%.

### Quantitative variables worth collecting
| Variable | Value | Unit / period | Interpretation |
|---|---:|---|---|
| companies_surveyed_2026 | 56 | companies | survey participants, not necessarily complete industry census |
| funding_12m_2026_usd_bn | 4.48 | USD bn / 12 months to July 2026 | survey-reported annual funding |
| funding_growth_yoy_pct | 69 | % | change vs prior FIA survey |
| reported_cumulative_funding_usd_bn | 14.24 | USD bn / FIA survey history since 2021 | avoid treating as independently audited market total |
| reported_employment | >16000 | persons | reported industry employment |
| companies_with_siting_agreement | 6 | companies | survey observation |
| companies_with_offtake_commitment | 5 | companies | includes PPA or similar arrangement |
| funding_as_short_term_challenge_pct | 67 | % respondents | survey responses |
| power_efficiency_challenge_pct | 64 | % respondents | survey responses |
| neutron_materials_challenge_pct | 64 | % respondents | survey responses |
| respondent_average_funding_need_usd_bn | 2.7 | USD bn | stated expectations, NOT observed plant CAPEX |

### Limitations
- Voluntary survey and incomplete coverage; membership or participation may introduce selection bias.
- Company forecasts (e.g. electricity by 2030s) are intentions, not independently proven milestones.
- Annual funding changes can be affected by a few large fundraising rounds and changing samples.
- *Average amount companies say they need* is not equivalent to verified first-of-a-kind construction cost or LCOE.

### Relation to hypotheses
- **H1:** Indirect. Efficiency and materials are important constraints, but the survey cannot establish commercial cost competitiveness.
- **H2:** Supports examining PPAs, siting agreements and investment partnerships as emerging strategies.
- **H3:** Supports examining financing and materials/manufacturing bottlenecks; does not estimate learning rates.

**Research use:** Industry context, market-intelligence dashboard and hypotheses motivation; do not use as proof of plant economics.

---

## S02 — Fusion for Energy (F4E) / Fusion Observatory

**Title:** *Global Fusion Energy Trends*  
**Published:** 15 July 2026  
**Publisher/type:** Fusion for Energy, comparative institutional/sector research  
**Source:** https://fusionforenergy.europa.eu/news/f4e-publishes-the-first-global-fusion-energy-trends-report/  
**Reports portal:** https://fusionforenergy.europa.eu/reports/

### Relevant findings
1. The report benchmarks five actors — EU, US, China, Japan and UK — using public finance, private finance, devices, publications and patents, plus regulation.
2. For identified fusion funding over 2022–2025, the US leads the five studied actors at €7.38bn; China follows at €6.94bn; the EU totals €3.34bn. The figures combine different types of expenditure, including ITER in-kind contributions.
3. The EU is a strong scientific and experimental ecosystem: 22 fusion devices were identified in its portfolio, including eight active devices, but the comparison suggests weaker private investment and patent counts relative to some rivals.
4. The five actors have 83 identified fusion devices in the pipeline, 42 classified as active (operating, under construction or upgrade). The report cautions that no operating device yet demonstrates all the plasma performance and duration needed for power-plant relevance.
5. Of 2,210 identified alive fusion patent families across the five actors, China is attributed 60%, the US 20%, and EU 6%. Patent count alone should not be interpreted as innovation quality; national filing practices differ.

### Quantitative variables worth collecting
| Variable | Value | Unit / period | Interpretation |
|---|---:|---|---|
| us_identified_funding_2022_25_eur_bn | 7.38 | EUR bn | public/private and specified other contributions |
| china_identified_funding_2022_25_eur_bn | 6.94 | EUR bn | not a simple private VC measure |
| eu_identified_funding_2022_25_eur_bn | 3.34 | EUR bn | includes ITER in-kind contribution |
| eu_iter_in_kind_eur_bn | 2.12 | EUR bn | component of EU total, NOT incremental |
| uk_identified_funding_2022_25_eur_bn | 1.49 | EUR bn | source-defined funding |
| japan_identified_funding_2022_25_eur_bn | 1.21 | EUR bn | source-defined funding |
| devices_five_actors | 83 | devices | defined pipeline |
| active_devices_five_actors | 42 | devices | active definition includes construction/upgrade |
| eu_devices | 22 | devices | all reported EU devices |
| eu_active_devices | 8 | devices | active EU devices |
| alive_patent_families | 2210 | families | identified across five actors |
| china_patent_share_pct | 60 | % | of identified alive families |
| us_patent_share_pct | 20 | % | of identified alive families |
| eu_patent_share_pct | 6 | % | of identified alive families |

### Limitations
- Comparison includes five selected jurisdictions, not the complete world.
- Funding categories vary by region and include ITER contributions: **do not compare F4E totals directly against FIA private fundraising figures**.
- Patents are affected by filing jurisdictions, publication lags, and differences in quality/value.
- Research publication volume and devices are imperfect proxies for private commercialization capacity.
- The public summary does not provide all data definitions/underlying records; review the full PDF before final publication.

### Relation to hypotheses
- **H1:** Highlights Europe's relevant scientific capabilities, but no demonstration of cost competitiveness.
- **H2:** Research-to-industry gap makes public-private partnerships a meaningful strategic question; does not quantify partnership benefits.
- **H3:** Supply-chain and technical ecosystem provide enabling conditions, but learning-rate assumptions require additional engineering sources.

**Research use:** Geographic benchmarking, EU/US/China investment ecosystem, patent and device charts, explanatory background.

---

## S03 — Proxima Fusion / IPP / RWE / Free State of Bavaria

**Title:** *Memorandum of Understanding on Alpha and Stellaris* (official announcement and institutional explanation)  
**Published:** 26 February 2026  
**Publisher/type:** Proxima Fusion and Max Planck Institute for Plasma Physics (IPP); project-party statements  
**Sources:**  
- https://www.proximafusion.com/press-news/proxima-fusion-rwe-the-free-state-of-bavaria-and-max-planck-institute-for-plasma-physics-sign-agreement-to-build-the-worlds-first-commercial-fusion-power-plant-in-europe
- https://www.ipp.mpg.de/mou26en?c=14226
- https://dtcf.de/wp-content/uploads/2026/02/2026-02-26_PR_Proxima-Fusion-Alpha_EN.pdf

### Relevant findings
1. The project roadmap separates **Alpha**, the planned scientific/engineering demonstrator near IPP in Garching, from **Stellaris**, a later proposed commercial fusion plant at the former Gundremmingen fission site.
2. IPP will lead plasma physics and define Alpha's scientific mission; Proxima is responsible for engineering, procurement/tenders and construction; RWE adds utility and site experience. This is an example of coordinated cross-sector development, not proof of cost savings.
3. Alpha is specifically planned for relatively short plasma pulses and scaling heat confinement, complementing the long-pulse/steady-state studies at Wendelstein 7-X. Avoid saying Alpha itself will demonstrate continuous operation.
4. IPP cited **€2bn as the planned overall Alpha project budget**, with private investors intended to cover approximately 20% subject to funding arrangements; Bavaria outlined **up to €400m** co-financing subject to budget constraints. This is a proposed financing structure, not proof that all financing is closed.
5. Reuse of the former Gundremmingen plant site and possible local magnet manufacturing are strategic options for infrastructure and industrial capability; actual cost advantages are not quantified in these announcements.

### Quantitative variables worth collecting
| Variable | Value | Unit / period | Interpretation |
|---|---:|---|---|
| alpha_planned_budget_eur_bn | 2.0 | EUR bn | project budget announced by IPP; **not Stellaris CAPEX** |
| alpha_private_finance_target_pct | 20 | % | proposed / conditional funding share |
| bavaria_max_cofinance_eur_m | 400 | EUR million | subject to budgetary approval |
| alpha_operational_window | 2030s | decade | intended milestone, not achieved |
| alpha_location | Garching | location | planned project |
| stellaris_location | Gundremmingen | location | planned commercial site |

### Later-context update (not part of original February statement)
- On **8 July 2026**, Max Planck reported a **€411m Proxima funding round** and a valuation **above €2.4bn**. The funding round is a company financing event; it must not automatically be equated with cash committed to Alpha or the entire project's funding closure.
  Source: https://www.mpg.de/26861952/proxima-fusion-raises-411-million-euros?c=2249

### Limitations
- This is a Memorandum of Understanding and parties' announcements, not a binding, fully financed EPC contract or commissioned power plant.
- Statements about first-to-grid, schedule, energy gain and employment are project goals/expectations.
- No independently verified Stellaris LCOE, full commercial CAPEX, revenue forecast, availability or profitability appears in the cited announcements.
- Planned public financing is conditional; confirm later public decisions before labeling funds as secured.

### Relation to hypotheses
- **H1:** Explains the technical commercialization bridge from W7-X to Alpha to Stellaris; does not establish plant economic feasibility.
- **H2:** **Most direct source** for evaluating the existing public-private-utility partnership and risk-sharing model.
- **H3:** Points to magnet manufacturing and industrial ecosystem development, without measuring manufacturing learning curves or unit-cost declines.

**Research use:** Proxima case background, partnership map, institutional roles, capital structure scenarios and commercialization timeline.

---

## Cross-source synthesis — what can we conclude now?

1. **Growing capital interest, not demonstrated commercial profitability:** FIA reports strong fund raising while F4E emphasizes the scientific/industrial commercialization gap.
2. **Regional structure matters:** The EU combines a major experimental/scientific base with more limited private-investment and patent metrics than some other regions.
3. **Proxima already pursues partnerships:** The Alpha/Stellaris MoU makes H2 an evaluation of partnership *design and effectiveness*, rather than a generic suggestion to seek partners.
4. **Major evidence gap:** These sources do not provide enough validated reactor cost inputs to calculate a company-specific Proxima LCOE. A separate techno-economic literature review is essential before Stage 4.
5. **Careful definitions are mandatory:** FIA private fundraising, F4E public/private/ITER spending, and Alpha's planned project budget have different denominators and must not be summed or plotted as equivalent measures.

## Suggested first-stage datasets
- `data/raw/fia_2026_industry_indicators.csv` — survey indicators, periods, units, primary-source URLs.
- `data/raw/f4e_2026_country_benchmark.csv` — jurisdiction, funding categories, devices, patents; retain definitions.
- `data/raw/proxima_project_milestones.csv` — event date, planned/achieved, project, estimated cost, certainty, source URL.

## Follow-up verification checklist
- [ ] Access full FIA 2026 PDF and confirm survey questions, base populations and chart definitions.
- [ ] Access full F4E 2026 report and verify jurisdiction methodology, patent counting and funding categories.
- [ ] Validate latest Alpha funding approval status from Bavarian/Federal sources.
- [ ] Read Stellaris peer-reviewed engineering concept for techno-economic assumptions; do not substitute the MoU for technical data.
- [ ] Keep a separate `assumptions_register.csv` for any model parameter lacking observed evidence.
