# Economic Assumptions, Evidence and Price Basis

## Purpose and research status

This revision makes the existing Stage 4 numerical assumptions traceable. It
adopts a common accounting convention, records why each reference value is used,
and distinguishes executed sensitivity envelopes from unexecuted exploratory
ranges. It does not provide empirical calibration of a commercial Stellaris.

The register is a reviewed input, separate from the generated
`data/economic_input_register.csv`. The latter remains a Stage 3 inventory of
engineering evidence gaps and proxies; its builder must not overwrite the new
assumption register.

## Common monetary and project boundary

All hypothetical model costs, sale prices, LCOE and NPV are now interpreted in
**2024 constant EUR**, using a real, pre-tax, unlevered discount rate. This is an
explicit new analyst bookkeeping convention assigned to previously unspecified
analyst EUR values. No historical CPI, exchange-rate or source-year conversion
has been performed on them. Numerical scenario values are preserved.

Price year denotes purchasing power, not the construction date, plant COD or
cash-flow year zero. The current DCF still places overnight CAPEX at its model
year zero and operates for 35 subsequent years in the reference case. It does
not model a calendar construction schedule or claim operation in 2024.

Choosing 2024 aligns the real-price unit with the retained 2024 historical
market reference. The real/nominal distinction follows the SAM methodological
explanation, not a source of fusion-specific cost values:
https://samrepo.nlr.gov/help/mtf_lcoe.html, section “Real and Nominal Levelized
Cost of Energy”. This convention must be revisited explicitly if calibrated
cost data in other currencies/years are introduced.

The reference remains EUR 12 billion overnight CAPEX, 1000 assumed net-rated
MWe, 85% CF, EUR 200 million/year fixed OPEX, EUR 5/MWh variable OPEX, 35 operating
years and an 8% real hurdle rate. The simplified result remains approximately
170.14 EUR_2024/MWh. It is not a verified commercial electricity-cost estimate.

## Parameter register

| Parameter | Reference | Reviewed range | Range role |
|---|---:|---:|---|
| Overnight capital intensity | 12000 EUR_2024/kWe | 8000–18000 | Existing cost scenarios |
| Assumed net-rated power | 1000 MWe | 800–1200 | Existing fixed-total-CAPEX output test |
| Net electrical CF | 85% | 70–95% | Existing utilization sensitivities |
| Fixed OPEX | 200 million EUR_2024/year | 100–300 | Unexecuted exploratory candidate |
| Variable OPEX | 5 EUR_2024/MWh | 0–10 | Unexecuted exploratory candidate |
| Economic operating life | 35 years | 25–45 | Unexecuted exploratory candidate |
| Real discount rate | 8% | 4–12% | Unexecuted exploratory candidate |
| Magnet share of plant CAPEX | 25% | 10–40% | Unexecuted exploratory candidate |
| Magnet learning rate | 10% per doubling | 0–20% | Existing component-learning cases |
| Constant real sale price | 170 EUR_2024/MWh | 78.51–200 | Existing mixed historical/hypothetical tests |

The candidate brackets are explicit analyst stress choices: plus/minus 50% for
FOM, removal/doubling of the VOM placeholder, plus/minus ten years for lifetime,
plus/minus four percentage points for discount rate, and plus/minus fifteen
percentage points for magnet share. They are documented for future evaluation,
not newly executed results or evidence of realistic uncertainty bounds.

Reference price 170 is REV003, an analyst input; it is not a measured PPA or an
inferred future price. REV001 alone represents a historical observation. Its
78.51 EUR/MWh value must reconcile to the retained 2024 mean rounded to two
decimals. Freezing that value over plant operation is a stress test.

Ranges describe this reviewed analysis, not the limits of possible outcomes.
Actual costs can lie outside them; future revenues can be below the historical
average. No confidence level, probability distribution, independence assumption
or Monte Carlo sampling is implied. Joint engineering feasibility remains open.

## Evidence and transfer limits

The Araiinejad and Shirvan study provides context for the scale and uncertainty
of magnetic-fusion costs. The project retains its USD tokamak NOAK benchmark
values unchanged. These are not converted EUR bounds for a European stellarator.
Its price-year, country, scale and architecture transfer remain unresolved in
this project. Source EC001: https://doi.org/10.1016/j.apenergy.2025.126567,
published abstract and the retained benchmark table.

ATB EC003 defines CRF, LCOE and financing boundaries. It does not justify this
project's 8% discount rate or 35-year life:
https://atb.nlr.gov/electricity/2025/equations_%26_variables.
The rate is an assumed hurdle rate, not an estimated Proxima WACC.

Stellaris engineering source S3_006 motivates power and maintenance questions,
but peak electric output is not verified net-rated power, and scheduled outage
duration is not total plant CF or a replacement-cost estimate:
https://doi.org/10.1016/j.fusengdes.2025.114868, Table 2 and Section 2.11.

The numerical values of fixed/variable OPEX, lifetime, hurdle rate, magnet cost
share and learning rate remain uncalibrated analyst choices. Their reference
notes document methodology or context, not direct numerical support. The
register preserves the exact next evidence needed for each parameter.

## FOAK and repeat production

CAL001–CAL003 are now explicitly classified as illustrative first-unit FOAK
cost sensitivities for the hypothetical plant. This is an analyst scenario
label, not empirical FOAK costing or a company statement. Low/high cases are
not automatically NOAK/FOAK alternatives; they vary capital intensity within
the same declared first-unit scope.

The learning model starts from that assumed first unit and reduces only the
magnet cost portion for subsequent equivalent plant-scale magnet sets. A
modeled sixteenth unit does not establish industrial NOAK maturity. Factory
investment, construction learning and commercial deployment feasibility remain
outside the calculation. Neither the full FOAK project cost nor a mature NOAK
plant cost has been established.

## Model bindings and validation

Ten parameter families cover 57 active numerical cells in five scenario files:
21 Stage 4.2 inputs, 21 synthetic Stage 4.1 inputs, five performance CF entries,
six learning inputs and four electricity prices. Synthetic total CAPEX is
converted to capital intensity only for checking consistent register units.

`validate_economic_assumptions.py` checks coverage, unique IDs, explicit units,
reference values, range inclusion, evidence classes, source-note links and the
price-year/model basis. It checks the historical mean link and produces JSON
and Markdown audit reports. It never rewrites the reviewed register or source
scenario files. Intentional assumption changes require updating both the
relevant scenario and its reviewed rationale/range where applicable.

The validator runs before the existing rebuild steps. All new source inputs
and generated audit reports are included in freshness hashes. Stage 4
integration checks the current register and records the economic basis in its
audit. Monetary plot labels state the 2024 price unit. Offline tests validate
traceability and intentional inconsistencies, not external factual truth.

A passing result is `PASS_WITH_RESEARCH_GAPS`. It means the declared assumptions
are internally documented and connected, not scientifically calibrated.

## Remaining research work

Prioritize a plant power balance; maintenance-constrained CF; subsystem CAPEX
and OPEX; replacement-event cost/timing; construction expenditure; and an
explicit financing boundary. Historical revenue context must be developed into
future offtake/merchant scenarios. Parameter correlations and feasible scenario
families must be specified before probabilistic interpretation in Stage 5.
