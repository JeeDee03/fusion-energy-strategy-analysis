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

## Stage 4.2 — Fusion Cost Benchmarks and Economic Scenarios

### fusion_cost_benchmarks.csv

Contains published techno-economic estimates for reference fusion power plant designs. Each record includes the metric, value, original currency and unit, reference plant capacity, development basis and source ID.

Benchmark values must not be treated as Proxima Fusion cost estimates.

### lcoe_scenarios_stage42.csv

Contains analyst-defined sensitivity cases for the Stellaris research model.

Capital intensity is expressed in EUR/kWe and converted into total EUR million using the scenario's assumed net rated electrical capacity.

The `analyst_scenario` classification identifies hypothetical modeling assumptions, rather than source-derived plant specifications.

### Methodological Requirements

- Do not equate overnight capital cost with fully financed project cost.
- Do not compare USD and EUR values without explicit currency normalization.
- Preserve the reference price year and reactor technology when transferring cost benchmarks.
- Distinguish FOAK and NOAK development assumptions.
- Keep published evidence separate from scenario assumptions.
- Report calculated LCOE as conditional model results rather than commercial forecasts.

## Stage 4.3 — Engineering Performance Sensitivity

### lcoe_performance_scenarios.csv

Defines hypothetical net electrical capacity-factor scenarios for the Stage 4 LCOE model.

Each row specifies a unique scenario ID, descriptive name, capacity factor and assumption classification.

The values are analyst-defined sensitivities, not company-reported performance expectations.

### Stage 4.3 Generated Outputs

- `reports/stage43_performance_sensitivity.csv`: All combinations of Stage 4.2 capital costs and Stage 4.3 performance scenarios.
- `reports/stage43_break_even_capacity_factor.csv`: Capacity factors required to reach the specified reference LCOE.
- `reports/stage43_net_power_sensitivity.csv`: Separate net electrical output sensitivity with constant total CAPEX and OPEX.
- `reports/stage43_lcoe_heatmap.png`: Visualization of CAPEX and capacity-factor sensitivity.

### Methodological Rules

1. Plant availability must not automatically be treated as net electrical capacity factor.
2. Capacity factor is bounded between zero and one for the specified rated net electrical output.
3. Net electrical output must be distinguished from gross electrical output and fusion thermal power.
4. Changes to capacity factor may involve additional engineering expenditure in real projects.
5. A break-even capacity factor above one indicates that the specified target cannot be achieved through capacity-factor improvements alone under the stated assumptions.
6. Synthetic cost and performance scenarios must not be interpreted as Proxima Fusion forecasts.

## Stage 4.4 — Manufacturing Learning Analysis

### manufacturing_learning_scenarios.csv

Contains hypothetical magnet-system manufacturing learning scenarios.

| Column | Description |
|---|---|
| `scenario_id` | Unique learning scenario identifier |
| `scenario_name` | Descriptive scenario label |
| `magnet_capex_share` | Assumed magnet-system share of initial total plant CAPEX |
| `magnet_learning_rate` | Assumed magnet-system cost reduction per cumulative production doubling |
| `assumption_class` | Identifies scenarios as analyst assumptions |

### Generated Outputs

- `reports/stage44_learning_results.csv`: Modeled plant CAPEX and LCOE under alternative manufacturing learning assumptions.
- `reports/stage44_capex_learning.png`: Total plant CAPEX sensitivity to cumulative magnet-system production.
- `reports/stage44_lcoe_learning.png`: Electricity cost sensitivity to manufacturing learning.

### Methodological Rules

1. Learning rates represent cost reductions per cumulative production doubling, not per year or per individual unit.
2. Component-level cost reductions must not be double-counted through an additional plant-wide learning factor.
3. Magnet-system manufacturing costs must be distinguished from total plant CAPEX.
4. Production-volume scenarios must not be presented as company deployment forecasts.
5. Hypothetical learning rates must not be labeled as observed Proxima Fusion production experience.
6. FOAK and NOAK scenarios must distinguish technical learning from development and financing costs.
7. Learning curves must retain their defined cumulative-production reference and comparable product boundaries.

## Stage 4.5 — Electricity Revenue and Project Cash Flow

### electricity_revenue_scenarios.csv

Contains historical-price stress tests and hypothetical electricity sale-price scenarios.

Important fields:

- `scenario_id`: Unique revenue scenario identifier.
- `electricity_price_eur_per_mwh`: Assumed constant real electricity sale price.
- `pricing_basis`: Distinguishes historical-average stress tests from hypothetical fixed-price cases.
- `assumption_class`: Distinguishes historical observations from analyst scenarios.

### Generated Outputs

- `reports/stage45_npv_summary.csv`: Scenario electricity revenues, annual operating cash flows, break-even prices and NPV.
- `reports/stage45_annual_cash_flows.csv`: Year-by-year project cash-flow schedules, including year-zero investment.
- `reports/stage45_npv_comparison.png`: NPV comparison across sale-price cases.
- `reports/stage45_cumulative_cash_flow.png`: Cumulative discounted cash-flow trajectories.

### Methodological Rules

1. Historical electricity-market prices must not be presented as future market forecasts.
2. Discount rates must be consistent with real or nominal cash-flow assumptions.
3. Financing costs must not be double-counted.
4. A project-level NPV calculation must be distinguished from equity-investor NPV.
5. Break-even electricity prices are conditional on the modeled cost and operating assumptions.
6. A positive scenario NPV is not evidence that a real fusion project is commercially viable.
7. Fixed-price offtake scenarios are not equivalent to confirmed commercial power purchase agreements.

## Stage 4.6 — Integrated Economic Research Outputs

### stage4_integrated_summary.csv

Consolidates principal economic metrics across Stage 4.2–4.5.

| Column | Description |
|---|---|
| `stage` | Originating analysis stage |
| `metric` | Economic metric or coverage measure |
| `value` | Numerical value |
| `unit` | Unit of measurement |
| `classification` | Distinguishes analyst assumptions, model outputs and coverage information |

### stage4_integration_audit.json

Machine-readable record of cross-model consistency tests, reference assumptions, identified limitations and overall audit status.

### stage4_integration_audit.md

Human-readable validation summary intended for research review.

### Methodological Rules

- Model consistency checks must not be interpreted as external factual verification.
- All Stage 4 scenarios must retain their assumption classifications.
- Reference economic cases must be consistent across analyses.
- LCOE and project NPV must use compatible discount rates and cash-flow boundaries.
- Manufacturing learning must not be double-counted.
- Historical electricity prices must not be treated as future forecasts.
- The distinction between capital cost intensity, total capital investment, gross power and net electricity production must be preserved.
- Stage 5 must distinguish exploratory probability assumptions from empirically supported distributions.

## Reviewed Economic Assumptions and Price Basis — Step 4

The following are source inputs, distinct from the generated engineering
`economic_input_register.csv`. Validation never overwrites their reviewed content.

### economic_assumptions.csv

One row per modeled numerical parameter family, keyed by `parameter_id`.

| Fields | Definition |
|---|---|
| `model_field`, `unit` | Scenario input field and explicit physical/monetary unit |
| `reference_value`, `reference_scenario` | Reviewed reference and the active row it must match |
| `lower`, `upper`, `range_role` | Reviewed sensitivity envelope or unexecuted exploratory candidate, not a confidence interval |
| `evidence_class`, `calibration_status` | Analyst assumption and retained lack of empirical calibration |
| `reference_notes` | Semicolon-separated note IDs in economic_reference_notes.csv |
| `rationale`, `range_rationale` | Why the reference and bracket are used; not a substitute for evidence |
| `dependencies`, `next_evidence_needed` | Engineering/economic coupling and the outstanding research action |
| `geography`, `deployment_basis` | Declared analyst scenario scope, not country-calibrated costs |
| `price_year` | 2024 for monetary quantities; not_applicable for other quantities |

### economic_reference_notes.csv

`note_id` identifies a source note. `source_id` points to sources.csv when an
existing ID applies; the separately reviewed SAM methodology page is cited by
URL. `url` and `locator` identify the evidence. `source_role` distinguishes
context_only, methodology_only and historical_value. `finding` records what
was used and `transfer_limit` explains what it does not establish.

### economic_model_basis.json

Explicit 2024 constant-EUR analyst convention, real/pre-tax/unlevered discount
basis, overnight upfront CAPEX, illustrative first-unit FOAK scope, unverified
net-rated output, normalized 8760-hour model year and the 8784-hour historical
2024 reference. Price year is not COD or cash-flow year zero. Repeat-unit
learning is not verified NOAK. Full calibration remains open.

### economic_assumption_audit.json and .md

Generated validation outputs. Status PASS_WITH_RESEARCH_GAPS means that the
reviewed register matches active inputs and model conventions; it does not
mean empirical calibration is complete. JSON records 57 active numerical
bindings with their parameter, unit and evidence class. Errors and retained
research gaps are separate lists. These reports and all three new source inputs
are included in the Stage 3–4 provenance checks.


## Conditional Engineering Generation — Step 5

### engineering_generation_cases.csv

Reviewed analyst inputs keyed by scenario_id. `maintenance_basis` is
full_power_exposure (interval_years denotes accumulated FPY) or calendar_cycle
(interval_years includes its major outage). `major_outage_months` uses 12 equal
model months/year. `other_outage_fraction` applies only in the non-major window;
`operating_load_fraction` applies while online. `gross_electric_mwe` is electrical
power before proportional online `auxiliary_fraction`. The target_capacity_factor
is tested, not inserted as generation. `assumption_class`, `source_id` and `notes`
retain assumption/evidence limits; none is measured plant performance.

### engineering_generation_scenarios.csv

Generated full-row engineering calculations and conditional LCOE. `net_rated_mwe`
subtracts auxiliaries once. `derived_capacity_factor` is relative to that net
rating. `annual_net_energy_mwh` is the long-run annual cycle average.
`operating_window_years`, `cycle_years`, major_outage_availability and
online_availability distinguish time and loss mechanisms. `target_met` and
cf_target_gap preserve unmet performance targets. `evidence_relation` flags
shorter-than-documented duration targets and analyst calendar interpretations.
Total CAL002 investment is held fixed; effective capital intensity changes with
net rating. LCOE uses 2024 constant EUR.

### engineering_generation_audit.json, .md and capacity_factors.png

Generated summaries with conditional target counts, source limits and the
CF/target figure. An intentionally unmet target is an analytical finding.
Passing execution does not validate the optimistic engineering assumptions.
All new inputs and outputs are tracked by the Stage 3–4 rebuild/freshness checks.


## Construction and Replacement Cash Flow — Step 6

### lifecycle_cash_flow_cases.json

Reviewed source cases with an explicit 2024 constant-EUR cost/discount boundary.
construction_years is a nonnegative integer; construction_spend_shares sums to
one and has C entries (one for C=0). Shares are paid at model times 0..C-1,
COD=C, and operating receipts start at C+1. generation_mode is legacy_constant_cf
or engineering_events. engineering_case_id and price_scenario_id reference
reviewed source cases. replacement_cost_eur_million is paid per event, at exact
outage start. opex_boundary prevents silently combining aggregate costs with
separate replacements. All schedules/costs remain analyst assumptions.

### lifecycle_summary.csv

Generated per-case NPV, discounted-cost/energy break-even price, discounted
cost components, finite-life capacity factor, total generation, replacement
count, declared assumptions and source references. The finite-life CF can differ
from the Step 5 long-run cycle average because first/last cycles are partial.

### lifecycle_annual_cash_flows.csv

Generated integer reporting buckets with separately discounted construction,
routine operating and replacement components. model_year is relative project
time, not price year or an absolute calendar date. Replacement discounting uses
its exact time before aggregation, so discounted cash flow need not equal the
raw annual total divided by the integer-year discount factor.

### lifecycle_replacement_events.csv

Exact operating/project start time, replacement index, reporting year, outage
end clipped to retirement and nominal/discounted event cost. No event is bought
at retirement; earlier events incur full assumed expense even for a truncated
final outage. Other downtime/load losses are averaged within operating windows.

### lifecycle_audit.json, .md and lifecycle_break_even.png

Generated reconciliation, case findings, monetary/time boundaries, limitations
and the break-even comparison. Passing checks validate consistency, not commercial
calibration or loan-financing assumptions. All new sources/outputs are included
in Stage 3–4 hashes. Existing economic_model_basis.json now explicitly identifies
its upfront-investment boundary as legacy scope; the extension's boundary is
separate, while the 2024 constant-EUR unit is shared.


## Comparable Company and Business Evidence — Step 7

### company_business_profiles.csv

Five reviewed profiles keyed by company_id. strategy_label must match the shared
companies.csv business_model field. classification_basis is explicitly an analyst
classification of declared strategy, not observed revenue. source_ids reference
the competitive source ledger; review_date and limitations bound interpretation.
Updating this shared descriptive metadata requires a Stage 1–2 provenance refresh
before claiming its old input hashes match the new company file.

### competitive_sources.csv

Fourteen selected sources with source_id, company_id, title, publisher, URL,
publication/updated/review dates, source_kind, locator and limitations. An optional
legacy_source_id links to sources.csv without modifying its existing financial
source register. Undated websites are marked with blank publication dates, not
invented event dates. The bounded snapshot date is 2026-11-05.

### company_comparison_claims.csv

Forty records: one company/criterion pair for each of five companies and eight
criteria. claim_id is unique; reference_device_id is owned by the same company.
statement, evidence_type, source_ids and evidence_locator describe the reviewed
claim; limitation and analyst_implication explicitly separate boundaries and
interpretation. not_established_in_reviewed_sources is a review gap, not proof
that the company lacks the capability. Source statements are not independently
verified by offline validation.

### company_comparison.csv, company_comparison_matrix.csv, company_comparison.md

Generated tidy evidence table, wide comparison and linked human-readable review.
Device roles distinguish experiments, demonstrators and commercial concepts;
no maturity score or comparative LCOE is computed. Source and assumption changes
must reconcile before integration/freshness can pass.

### company_comparison_audit.json

Generated coverage and consistency status PASS_WITH_EVIDENCE_GAPS. It retains
selected-review unknown counts and interpretation limits. Counts measure dataset
coverage, not scientific readiness, source independence or commercial success.

## Current research interpretation registers — improvement Step 8

- `data/research_status.json`: canonical H1–H3 definitions, open assessments, evidence still required and implementation states for main Stages 1–7. A planned stage is not marked complete by running software.
- `data/research_findings.json`: reviewed numerical anchors; each records a report CSV, unique row selector, field, expected rounded value, absolute tolerance, unit, conditional classification and boundary. The runner checks anchors but never silently updates them to match changed results.
- `reports/research_consistency_audit.json` and `reports/research_consistency_summary.md`: generated bounded checks of hypothesis blocks, anchors and relative links. They are not source verification or automated review of arbitrary prose.
- `reports/stage12_run_summary.json` and `reports/stage34_run_summary.json`: separate execution/provenance records. `check_stage14_freshness.py` checks both declared file sets and environments without rewriting them. The Stage 1–2 record now requires schema version 1; rebuild older records.

Both rebuilds conservatively track top-level Python scripts. Stage 3–4 also tracks current editorial Markdown inputs, excluding the Stage 1–2-generated chapters 02/11 (their producer tracks those outputs). No human milestone review is overwritten.

## Stage 5 uncertainty design — improvement Step 9

- `data/stage5_uncertainty_spec.json`: reviewed source-bound specification, ten parameter roles, five pilot marginals, separate learning family, 12 unweighted contexts, dependence designs and sampling/convergence acceptance rules. No empirical probability calibration is asserted. `reviewed_input_hashes` pins the six reviewed source files; changed sources require deliberate design reconciliation.
- `reports/stage5_design_dry_run.csv`: generated 396 deterministic center/corner checks, with explicit context, parameter values, replacement cost, finite-life CF, NPV and break-even price. Rows are neither random draws nor probability-weighted observations.
- `reports/stage5_spec_audit.json` and `.md`: specification/numerical preflight results. `simulation_executed` is false. Passing does not establish feasibility, empirical calibration, convergence, or completion of main Stage 5.
