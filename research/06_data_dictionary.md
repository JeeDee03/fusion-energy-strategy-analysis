# Data Dictionary and Evidence Model

Version 0.2 — 28 October 2026

Status: Synchronized with the uploaded enhanced baseline. This dictionary documents implemented tables and review states; it does not certify independent financial or technical accuracy.

## Conventions

Identifiers are strings and must be unique within their own table. References must resolve to their parent table. Dates use YYYY-MM-DD; an unknown date stays blank with an explanatory status or note. Monetary values use the currency stated in the currency field. Do not replace missing monetary values with zero. Separate not_disclosed, not_found, not_applicable, and pending_review through companion status fields when needed. Approximate values and lower bounds retain their qualifiers.

## Existing tables

### companies.csv

| Field | Meaning / rule |
|---|---|
| company_id | Unique company identifier |
| company_name | Company name |
| country | Country recorded for company; headquarters basis should be documented |
| founded_year | Reported founding year; integer |
| technology | Broad architecture; technical verification belongs to Stage 3 |
| business_model | Reported business model; Undetermined means not established in this dataset |
| company_status | Recorded operating status, requiring a reference date for current interpretation |

### funding_rounds.csv

| Field | Meaning / rule |
|---|---|
| funding_id | Unique financing-event record |
| company_id | Reference to companies.company_id |
| announcement_date | Public announcement date; not necessarily closing or payment date |
| amount_original | Amount in original currency units, not millions |
| currency | Original currency, currently EUR or USD |
| amount_usd | Optional converted amount; processed conversion is authoritative only with documented FX inputs |
| funding_type | Instrument classification; verify against disclosure |
| source_id | Existing primary source reference; does not capture all supporting sources |

### funding_snapshots.csv

| Field | Meaning / rule |
|---|---|
| snapshot_id | Unique cumulative disclosure record |
| company_id | Company reference |
| as_of_date | Date to which the cumulative amount applies; must not substitute an access date for an unknown financial reference date |
| amount_million | Reported amount in MILLIONS of original currency |
| currency | Original currency |
| comparison_basis | What the total includes, such as private investment or public and private support |
| qualifier | reported, approximate, or lower_bound; preserve in outputs |
| source_id | Existing primary source reference |
| comparability_group | Broad scope grouping; matching groups alone do not establish full comparability |
| verification_status | Recorded review state; must have supporting evidence notes |

Never sum snapshots with funding rounds. Different dates, scope, currency, and conditionality require separate treatment.

### sources.csv

| Field | Meaning / rule |
|---|---|
| source_id | Unique document/source identifier |
| source_title | Document or page title |
| publisher | Publishing organization |
| publication_date | Publication date; blank for genuinely undated material |
| url | Source location; a URL alone does not prove its claim |
| source_type | Company announcement, institutional publication, news report, etc. |
| access_date | Date the researcher actually accessed the source |

### strategic_partnerships.csv

| Field | Meaning / rule |
|---|---|
| partnership_id | Unique relationship/event record |
| company_id | Company reference |
| partner_name | Counterparty |
| announcement_date | Announcement date |
| partnership_type | Disclosed form of relationship |
| reported_value | Numeric disclosed value; interpreted ONLY with reported_unit and amount_role |
| reported_unit | Unit such as EUR_million, MW, or percent_of_project_cost |
| amount_role | Meaning of value: investment_part_of_round, power_capacity, conditional_share, etc. |
| status | Disclosed relationship state; announced does not mean executed |
| strategic_value | Researcher's qualitative description, not a demonstrated causal benefit |
| source_id | Existing source reference |

Do not aggregate values with different units or roles. Do not add an investor contribution to a round that already includes it.

### milestones.csv

| Field | Meaning / rule |
|---|---|
| milestone_id | Unique milestone record |
| company_id | Company reference |
| milestone_name | Specific event or intended achievement |
| milestone_type | Category such as hardware_demonstration, regulatory_submission or demonstrator_operations |
| target_date | Intended completion date; do not invent a day for a year-only target |
| actual_date | Actual completion date supported by evidence; blank if unachieved/unknown |
| status | planned or reported_completed; the latter is a company report, not independent validation |
| source_id | Source reference |

The implemented register contains nine selected observations. Additional fields: project_name identifies the program; statement_date dates the source statement; target_year preserves a four-digit year; target_period_text retains year/decade precision; evidence_level distinguishes company_target from company_report; notes record uncertainty. Exact dates remain blank where unknown. Revisions require new observations, not overwriting historical targets.

## Derived tables

### funding_normalized.csv

Contains the funding_rounds fields plus fx_date (date of matched reference rate) and eur_usd_rate (USD per EUR). amount_usd equals amount_original for USD events and amount_original multiplied by eur_usd_rate for EUR events. FX metadata on USD rows does not indicate that conversion was required. The current script matches the preceding rate within seven days; retain raw FX inputs and provenance when implementing reproducibility checks.

### partnership_capability_matrix.csv

company_name identifies rows. Capability columns count SELECTED recorded relationships classified by primary capability. A zero means no record assigned to that category in this sample. It does not demonstrate capability absence. The matrix is generated output; edit its inputs/classification rather than the output. Multi-label contributions are recorded separately in partnership_capability_tags.csv and must not be interpreted as unique partnership totals when summed across labels.

## Implemented claim-level evidence structure

Retain existing source_id fields for backward compatibility. The following tables contain the financing claims and links; separate partnership tables use the same schema.

### claims.csv — one row per testable statement

| Field | Meaning |
|---|---|
| claim_id | Unique statement identifier |
| entity_type | company, funding_event, funding_snapshot, partnership, project, or milestone |
| entity_id | Existing record ID; project IDs introduced when project table exists |
| claim_text | Precise statement, with units, scope, dates, and qualifiers |
| claim_type | reported_fact, company_target, researcher_interpretation, or modeling_assumption |
| verification_status | pending_review, original_source_checked, external_report_checked, or disputed_unresolved; independently_corroborated is reserved for documented independent evidence |
| review_date | Actual review date |
| notes | Limitations and unresolved conflicts |

### claim_sources.csv — one row per claim–source link

| Field | Meaning |
|---|---|
| claim_id | Reference to claims |
| source_id | Reference to sources |
| page_or_section | Page, heading, paragraph, or table locator |
| evidence_role | supports, contradicts, or contextualizes |
| source_dependency | original, independent_reporting, repeats_original, or unknown |
| verification_note | What was checked and whether amount, date, and scope match |

Use the pair (claim_id, source_id) as the unique key; combine multiple locators in one row. One source can support many claims; one claim can have many sources. A second publication repeating a press release is not independent verification. Financing and partnership claim tables are populated. Derived all_claims.csv/all_claim_sources.csv combine domains without changing source tables.

## Review-state interpretation

company_source_checked in snapshots and original_source_checked in company-backed claims describe the same source-check level. external_report_checked means the cited external article was read; it does not prove independent financial accuracy. source_dependency=unknown does not assert independence. Company announcements, targets and researcher interpretations remain separate.

## Implemented enhancement tables

### partnership_evidence.csv

One reviewed row per selected partnership; mechanisms are interpretations and not measured outcomes.

| Field | Meaning / rule |
|---|---|
| partnership_id | Reference to strategic_partnerships.partnership_id |
| company_id | Company reference |
| partner_name | Counterparty name |
| project_scope | Named project or company-level scope |
| statement_date | Date of the historical disclosure |
| commitment_form | Reported investment/MoU/PPA/contract/collaboration form; not an enforceability rating |
| documented_contribution | Source-supported role or contribution |
| legal_enforceability | Not assessed from public announcement alone |
| undisclosed_terms | Terms not established by the reviewed source |
| potential_mechanism_analyst_interpretation | Possible economic pathway; not a causal result |
| realized_benefit_evidence | Whether realized economic benefit is established in the reviewed disclosure |
| source_id | Reference to sources.source_id |
| source_locator | Document heading or paragraph containing supporting evidence |
| review_date | Actual evidence review date |
| verification_status | Review state; original_source_checked describes access/checking, not independent assurance |

### partnership_capability_tags.csv

Multi-label roles; summing labels does not give a count of unique partnerships.

| Field | Meaning / rule |
|---|---|
| partnership_id | Reference to strategic_partnerships.partnership_id |
| capability | One of capital, utility_expertise, site_access, public_support, scientific_rd, offtake, manufacturing, computing_simulation, technology_supply |

### partnership_claims.csv and partnership_claim_sources.csv

Same field definitions as claims.csv and claim_sources.csv above, using CLP-prefixed identifiers for the 11 partnership claims. Preserve the domain tables when regenerating combined outputs.

### all_claims.csv and all_claim_sources.csv

Derived row unions of the financial and partnership domain tables. Schemas match their respective source tables. Generated by integrate_stage12.py; do not edit directly. The current baseline has 25 combined claims. Milestone observations retain source references in milestones.csv and are not falsely counted as claim-table rows.

### electricity_prices_de_lu_2024.csv

Derived from retained hourly SMARD blocks; one interval per row. Price unit EUR/MWh.

| Field | Meaning / rule |
|---|---|
| interval_start_utc | Unique timezone-aware start in UTC |
| interval_start_local | Europe/Berlin start including UTC offset; repeated clock hours are distinct |
| duration_hours | Interval duration, 1.0 hour in this baseline |
| price_eur_mwh | Signed hourly day-ahead market price in EUR/MWh |
| source_id | ES001, SMARD DE/LU hourly series |

### electricity_monthly_2024.csv

Monthly aggregation using local delivery months and actual durations.

| Field | Meaning / rule |
|---|---|
| month | Europe/Berlin YYYY-MM |
| mean_eur_mwh | Arithmetic mean of equal one-hour prices, EUR/MWh |
| hours | Count of hourly intervals in the month |
| negative_price_hours | Intervals with price strictly below zero; zero is excluded |
| negative_price_share_pct | 100 × negative_price_hours / hours |

### electricity_summary_2024.json and data/raw/smard_2024/

The JSON includes year, bidding_zone, hours, mean_eur_mwh, median_eur_mwh, population_std_eur_mwh (price levels, ddof=0), p05_eur_mwh, p95_eur_mwh, min_eur_mwh, max_eur_mwh, negative_price_hours, negative_price_share_pct, hours_above_100_eur_mwh and longest_negative_run_hours. These are historical descriptors, not future distributions. The raw manifest records URLs, access date, file hashes, license and attribution. The retrieval vintage is October 2026, not an archived October 24 vintage.

### funding_audit.csv

Current selected-record review. The initial pass is preserved separately under research/references/.

| Field | Meaning / rule |
|---|---|
| record_id | Financing event or snapshot ID |
| claim_id | Reference to financing claim |
| review_status | Current review status matching the domain claim |
| amount_check | Disclosure/external-report support; no audit assurance |
| recommended_action | Current action or applied correction |
| notes | Scope limits and interpretation |

### funding_coverage.csv

Recorded sample coverage, not a completeness measurement.

| Field | Meaning / rule |
|---|---|
| company_id | Company reference |
| company_name | Company name |
| recorded_rounds | Count of selected rounds |
| first_recorded_event | Earliest selected announcement |
| last_recorded_event | Latest selected announcement |
| snapshot_date | Historical cumulative reference date |
| coverage_status | Selected events; not a complete company history |

### funding_reconciliation.csv

Arithmetic comparison only; a difference is not an identified missing transaction.

| Field | Meaning / rule |
|---|---|
| company_id | Company reference |
| currency | Original currency of compared records |
| selected_rounds_million | Sum of selected events in millions of original currency |
| recorded_snapshot_million | Reported numeric cumulative value in millions, preserving source qualifiers elsewhere |
| arithmetic_difference_million | Numeric snapshot minus selected sum; not an exact unexplained gap for lower bounds or incompatible scopes |
| interpretation | Scope, date, completeness and rounding caveats |
| ranking_permitted | no: this table does not authorize funding-strength ranking |

## Implementation review

All current CSV header fields are indexed here or in the retained base-table definitions. Publication dates, reference dates, statement dates, access dates and review dates remain distinct. Raw ECB-rate archival is a documented remaining improvement; internal conversion consistency does not establish the original downloaded rates' provenance.

## Stage 3 — Technical Evidence Architecture

### reactor_designs.csv

One record represents a specific experimental device, engineering verification facility, demonstrator, or commercial reactor concept.

- `device_id`: Unique identifier for the reactor project.
- `company_id`: Reference to the developer in companies.csv.
- `device_name`: Published device or project name.
- `technology`: Broad reactor technology.
- `device_role`: Research, engineering verification, demonstration, or commercial concept.
- `development_status`: Reported development state, subject to the source's reporting date.
- `source_id`: Primary source supporting identification and classification.

Device roles and development statuses are distinct. A conceptual commercial plant is not equivalent to an operating experimental machine.

### technical_parameters.csv

One record represents a numerical engineering parameter associated with a specific device.

- `parameter_id`: Unique technical parameter record.
- `device_id`: Reference to reactor_designs.csv.
- `parameter_name`: Unambiguous physical quantity.
- `value`: Numerical value.
- `unit`: Physical unit.
- `evidence_type`: measured, simulated, design_target, or announced_target.
- `source_id`: Source supporting the parameter.
- `notes`: Qualifications, assumptions and definition boundaries.

**Methodological rules:**

1. All numerical parameters must be linked to a specific device and source.
2. Experimentally measured results must be distinguished from modeled and targeted values.
3. Fusion power, thermal power, gross electrical power, and net electrical output must not be conflated.
4. Missing specifications must remain missing rather than being replaced with assumed zeros.
5. Technical parameters should only enter later economic models after their definitions and evidence status have been reviewed.
6. Technical conclusions must distinguish physics feasibility, engineering feasibility, and commercial viability.
7. Revisions to published technical specifications should preserve historical evidence rather than silently overwriting previous records.

The Stage 3 technical database is intended to identify engineering drivers of CAPEX, OPEX, availability, and electrical output for subsequent techno-economic modeling.

## Stage 3.5 — Economic Input Register

**File:** `data/economic_input_register.csv`

### Purpose

This dataset connects the engineering evidence collected in Stage 3 to the economic variables required for Stage 4's techno-economic models.

It identifies which model inputs have supporting technical evidence, which engineering parameters serve only as indirect indicators, and which economic quantities remain unknown.

Each row represents one required economic model input for a specific reactor design.

### Column Definitions

| Column | Description |
|---|---|
| `input_id` | Unique identifier for each economic input |
| `device_id` | Reactor design associated with the input |
| `economic_category` | Category such as CAPEX, OPEX, Output, Finance, Manufacturing, or Revenue |
| `input_name` | Name of the required economic model variable |
| `required_unit` | Unit needed for the future economic model |
| `linked_technical_parameter` | Related engineering parameter from `technical_parameters.csv`, if available |
| `evidence_value` | Recorded value of the related technical parameter |
| `evidence_unit` | Unit of the engineering evidence |
| `evidence_type` | Classification of the technical evidence |
| `source_id` | Reference to the source supporting the technical parameter |
| `evidence_status` | Whether an input is available directly, represented by an engineering proxy, or missing |
| `interpretation` | Explanation of what the engineering evidence can and cannot establish |
| `next_action` | Additional research or modeling required |

### Evidence Status Definitions

- `direct_input_candidate`: A documented quantity potentially suitable as a direct economic model input after verification.
- `engineering_proxy_only`: Related engineering evidence exists, but it cannot directly determine the required economic input.
- `missing`: No suitable supporting input has yet been identified.

The initial register generated in Stage 3.5 uses `engineering_proxy_only` and `missing`. Direct input candidates may be added later after verification.

### Methodological Rules

1. Engineering parameters must not automatically be interpreted as economic quantities.
2. All sourced numerical values must remain traceable to their original references.
3. Conceptual reactor specifications must be distinguished from experimentally demonstrated values.
4. Missing economic inputs must not be replaced with arbitrary numbers or zeros.
5. Economic assumptions introduced in Stage 4 must be explicitly labeled and justified.
6. FOAK and NOAK cost assumptions must be distinguished.
7. Electricity-generation assumptions must distinguish net electric output, availability, and capacity factor.
8. Project-level costs must be distinguished from company-level financing and investment obligations.

### Connection to Research Hypotheses

**H1 — Technology Economics:** Supplies the variables required to evaluate the effect of reactor design and operating characteristics on electricity costs.

**H2 — Commercialization Partnerships:** Identifies financial inputs required to analyze financing structures and risk allocation.

**H3 — Manufacturing Scalability:** Identifies manufacturing costs and learning assumptions needed to assess potential cost reductions.

### Research Status

The register currently identifies 11 preliminary economic model inputs for Proxima Fusion's Stellaris concept. It is an evidence-gap assessment, not a completed cost model.

The economic inputs will be quantified and evaluated during Stage 4.