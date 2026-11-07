# Stage 4 — Integrated Techno-Economic Assessment

Updated 5 November 2026. Current synthesis superseding the original five-model summary.

## Research question and hypotheses

Under which technological, economic and market conditions could stellarator fusion compete in Europe? Proxima's concept is the motivating case, not an empirically calibrated plant forecast.

<!-- hypotheses:start -->
**H1 — Technology Economics:** Stellarator operating advantages may compensate for higher engineering complexity and capital costs. Status: **open**.

**H2 — Commercialization Strategy:** Industrial and utility partnerships may mitigate financing and commercialization risks. Status: **open**.

**H3 — Manufacturing Scalability:** Standardization and accumulated manufacturing experience may reduce reactor construction costs. Status: **open**.
<!-- hypotheses:end -->

## Method and system boundaries

Evidence is separated from company plans, conceptual engineering, analyst inputs and conditional results. The implemented layers are annualized LCOE; literature context and provisional CAPEX sensitivity; independent CF/net-power sensitivity; component-specific learning; legacy constant-price project DCF; conditional engineering generation; and construction/replacement lifecycle DCF. Five-company evidence comparison informs scope, not comparative cost estimates.

CAL002 assumes EUR 12 billion overnight CAPEX, 1000 MWe net rated output, 85% CF, EUR 200 million/year fixed OPEX, EUR 5/MWh variable OPEX, 35 operating years and an 8% real discount rate. These are analyst inputs using 2024 constant EUR by convention, not rebased commercial cost observations. Published tokamak NOAK USD benchmarks are context; differences in architecture, size, geography and price year remain unresolved.

Legacy annual LCOE and DCF put all CAPEX at year zero and use constant generation. The lifecycle extension stages overnight expenditure, delays first receipts to the end of the first operating year and charges major replacements at outage start, discounted at exact event time. Event generation comes from interval overlap rather than a second CF deduction. Routine OPEX excludes separately charged major replacements in those cases; that allocation is uncalibrated. Discounting is real, pre-tax and unlevered, with no additional debt-interest/IDC charge. Debt terms, taxes, decommissioning, offline electricity purchases and hourly capture-price dispatch remain excluded.

## Conditional findings

The legacy reference LCOE and matched DCF break-even price are **170.14 EUR_2024/MWh**. Their equality follows from matching costs, timing and generation; it is not an independently validated Proxima electricity price. Historical 2024 DE/LU prices remain context, not future revenue forecasts.

Higher net generation spreads fixed costs across more MWh; some independent sensitivities require CF above 100% to offset specified CAPEX increases. Seven new generation cases constrain that algebra with maintenance and load assumptions. Under the four-FPY/five-month no-other-loss case, CF remains below 95%. A hypothetical two-month case reaches 95% but exceeds the documented duration target. Gross power and auxiliary consumption are analyst constructs, not verified Stellaris ratings. Linear exposure/load scaling remains an unvalidated proxy.

At a 25% magnet share and 20% component learning rate, four production doublings reduce whole-plant CAPEX by **14.76%**. This is a conditional experience-curve identity, not a measured fusion learning curve. Non-magnet costs remain constant and additional industrial investment is omitted.

The six lifecycle cases retain the legacy special-case identity, then explore construction, engineering-event generation, assumed replacement budgets and COD delay. **LC004**, with a five-year construction schedule and EUR 600 million per replacement, has a break-even price of **213.42 EUR_2024/MWh**. That budget is a 5%-of-reference-CAPEX stress assumption. Compare matched cases to isolate a mechanism: LC003–LC005 vary replacement cost; LC004 versus LC006 adds two years of COD delay with unchanged investment payment dates. LC002 versus LC003 also changes generation treatment, so it is not a pure construction comparison. No case is a commercial forecast.

## Hypothesis assessment

H1: operational economics matter mathematically, but no evidence establishes that actual stellarator advantages offset real engineering and investment burdens relative to comparable alternatives.

H2: partnerships and declared delivery roles are documented. Risk allocation, retained company value and causal commercialization benefits remain unquantified; plant project NPV is not company valuation.

H3: component learning affects plant economics conditionally. Cost shares, achievable rates, deployment scale, cost floors and industrial capital requirements remain uncalibrated.

All three remain open. Passing checks establishes internal consistency only.

## Current position and next work

The original assumption register covers ten parameter families and 57 numeric inputs; engineering and lifecycle extensions have separate reviewed sources. The company comparison retains 40 cells/14 sources with four selected-review gaps, without readiness or cost ranking. Current numerical anchors are checked against generated CSVs by `src/research_consistency.py`; that bounded audit cannot judge all prose or external truth.

See [chapter 31](31_research_status_and_claims.md) for the integrated research state and remaining evidence. Improvement Step 9 now specifies uncertainty variables, explicitly exploratory ranges/densities, coherent contexts, dependencies and convergence tests in [chapter 32](32_stage5_uncertainty_specification.md). Its 396 deterministic preflight cases are not main Stage 5 simulation. Main Stage 6 will assess strategies; main Stage 7 will synthesize the final research deliverables.
