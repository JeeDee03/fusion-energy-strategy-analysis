# Stage 4 — Integrated Techno-Economic Assessment

## 1. Research Objective

Stage 4 investigates the technological and economic conditions under which stellarator-based fusion electricity could become commercially competitive in Europe, with Proxima Fusion's Stellaris reactor concept as the principal case study.

The stage builds upon the market, financing, partnership and engineering research conducted in Stages 1–3.

Two hypotheses are particularly relevant:

**H1 — Technology Economics:** Operational advantages of stellarators may compensate for higher engineering complexity and investment costs.

**H3 — Manufacturing Scalability:** Manufacturing standardization, repeat production and technological learning may reduce stellarator capital costs sufficiently to improve commercial competitiveness.

The results also establish an economic foundation for the later evaluation of H2 concerning partnerships, financing and commercialization strategy.

## 2. Integrated Methodology

The research combines five analytical components:

1. A simplified annualized LCOE model.
2. A literature benchmark and provisional capital-cost sensitivity framework.
3. Capacity-factor and net electrical output sensitivity analysis.
4. Component-level manufacturing learning analysis.
5. A simplified discounted-cash-flow model evaluating electricity revenues and project NPV.

All calculations are implemented in Python and supported by explicit datasets, validation scripts and generated reports.

The individual models are linked through shared economic assumptions and a common LCOE calculation.

The Stage 4 integration audit verifies whether reference outputs remain consistent across these analyses.

## 3. Economic Reference Case

The principal hypothetical reference case, CAL002, assumes:

| Parameter | Assumption |
|---|---:|
| Overnight capital expenditure | EUR 12 billion |
| Rated net electric capacity | 1,000 MWe |
| Net electrical capacity factor | 85% |
| Annual fixed OPEX | EUR 200 million |
| Variable OPEX | EUR 5/MWh |
| Economic operating lifetime | 35 years |
| Real discount rate | 8% |

These figures are provisional analyst-defined scenarios. They are not reported actual construction or operating costs for Proxima Fusion.

The simplified model produces an LCOE of approximately EUR 170.14/MWh under these assumptions.

This figure is a conditional model output, not an estimate of Proxima Fusion's commercially achievable electricity cost.

## 4. Published Cost Evidence

Stage 4.2 records published techno-economic results for reference fusion power plant concepts.

The literature demonstrates that projected fusion costs can vary substantially with plant architecture, manufacturing assumptions, regulation and other economic conditions.

However, published tokamak-based NOAK estimates cannot be directly interpreted as Stellaris FOAK costs.

The current model has not yet resolved currency, price-year, country, plant-size and reactor-design differences sufficiently to claim a validated commercial Stellaris cost range.

These limitations must be retained in any external research summary.

## 5. Engineering Performance and H1

Stage 4.3 investigates how changes in net electrical capacity factor affect LCOE.

Under the illustrative model, greater annual generation reduces electricity cost because fixed costs are recovered across more MWh.

The analysis also calculates the capacity factor required to compensate for higher assumed construction costs.

Some modeled break-even requirements exceed 100% capacity factor, indicating that improved utilization alone cannot offset the relevant CAPEX increase within those specified scenarios.

This is a conditional finding about the model, not evidence that stellarators have higher costs than commercial tokamaks.

**H1 assessment:** The economic importance of operational performance is demonstrated mathematically. Whether actual stellarator advantages outweigh real construction and maintenance costs remains unproven.

## 6. Manufacturing Learning and H3

Stage 4.4 applies a component-level experience curve to the assumed HTS magnet-system share of plant capital expenditure.

The simplified model assumes that only the magnet-system portion benefits from manufacturing learning, while non-magnet costs remain constant.

For an illustrative 25% magnet CAPEX share and 20% learning rate, four cumulative production doublings reduce total plant CAPEX by approximately 14.76%.

The analysis demonstrates that subsystem learning can influence plant economics but that its impact depends on the size of the subsystem cost share.

The learning assumptions have not been empirically calibrated to Proxima's manufacturing program.

**H3 assessment:** Manufacturing learning could improve competitiveness under favorable conditions, but the achievable learning rate, required industrial investment and deployment scale remain unknown.

## 7. Electricity Revenue and Investment Economics

Stage 4.5 introduces a simplified project discounted-cash-flow framework.

The model calculates electricity revenue, operating cash flow, project NPV and a break-even constant real sale price.

Under the CAL002 reference assumptions, the break-even price is approximately EUR 170.14/MWh.

This agrees with the simplified LCOE because both models use the same discount rate, cost boundary, generation assumptions and upfront capital expenditure.

Historical German electricity prices are used as market context and stress-test inputs, not as forecasts of future fusion electricity prices.

Actual commercial viability would depend on future market conditions, electricity offtake arrangements, construction timing, financing, operational performance and other factors.

## 8. Integrated Findings

The analyses identify four mechanisms with important implications for fusion commercialization.

**Capital-cost exposure:** Large upfront investment makes fusion electricity economics sensitive to capital intensity and discount rates.

**Operational performance:** High net electrical generation can improve cost competitiveness, but the economic value of availability is bounded and depends on associated costs.

**Manufacturing scalability:** Component-level learning can reduce plant costs, although it does not automatically create equivalent whole-plant savings.

**Revenue realization:** A plant's investment attractiveness depends on its achievable electricity revenue, not solely on its engineering performance or LCOE.

These mechanisms should not be treated as independent in a real commercial project.

For example, improving availability might require higher CAPEX, and accelerating manufacturing learning might require additional upfront industrial investment.

The current models explore these mechanisms separately rather than fully modeling their interactions.

## 9. What Has and Has Not Been Established

The study has demonstrated:

- Mathematical consistency of the simplified LCOE and discounted-cash-flow formulations.
- Conditional sensitivity of electricity cost to CAPEX, capacity factor and assumed manufacturing learning.
- The relationship between break-even electricity prices and project NPV under matched model assumptions.
- A reproducible methodology for comparing alternative economic scenarios.

The study has not demonstrated:

- The actual construction cost of Stellaris.
- The commercial capacity factor of a future Proxima plant.
- A verified manufacturing learning rate for stellarator magnet systems.
- Cost superiority relative to competing fusion designs.
- Future electricity-market revenues or offtake prices.
- Commercial viability or positive expected investor returns.

## 10. Principal Research Limitations

The most consequential unresolved uncertainties include:

1. FOAK and NOAK plant CAPEX.
2. Net electrical output and auxiliary consumption.
3. Scheduled and unplanned maintenance.
4. Component replacement costs.
5. Actual manufacturing cost shares.
6. Learning-rate feasibility and industrial investment requirements.
7. Construction timing and financing during construction.
8. Plant lifetime, discount rate and regulatory requirements.
9. Future electricity-market conditions and realized capture prices.
10. Correlations between engineering performance, CAPEX and operating costs.

These uncertainties limit the interpretation of individual point estimates.

## 11. Stage 5 — Uncertainty Analysis Handover

The next research stage will investigate how uncertain model inputs affect economic outputs.

Initial candidates for uncertainty analysis are:

- Overnight capital intensity.
- Net electrical capacity factor.
- Fixed and variable OPEX.
- Plant economic lifetime.
- Real discount rate.
- Magnet-system CAPEX share.
- Manufacturing learning rate.
- Electricity sale price.

The distribution ranges and shapes must be explicitly justified or classified as exploratory assumptions.

Where empirical evidence is unavailable, the model should not imply that selected probability distributions represent objectively known real-world probabilities.

Stage 5 should investigate joint parameter variation and the possibility of economically important interactions and correlations.

## 12. Conclusion

Stage 4 establishes a reproducible techno-economic framework for investigating the conditions under which stellarator-based fusion might become commercially competitive.

The results identify capital costs, operational performance, manufacturing scalability and electricity revenues as major economic drivers.

The model provides conditional findings and break-even relationships, but the available evidence remains insufficient to establish Proxima Fusion's future commercial competitiveness.

H1 and H3 remain open research hypotheses. H2 will require further financial and strategic analysis.

The next stage will quantify the effects of uncertainty before the project advances to strategic decision-making.

## Supporting Research Artifacts

- `research/20_techno_economic_model_architecture.md`
- `research/21_fusion_cost_calibration.md`
- `research/22_engineering_performance_economics.md`
- `research/23_manufacturing_learning_analysis.md`
- `research/24_project_revenue_npv_analysis.md`
- `reports/stage4_integrated_summary.csv`
- `reports/stage4_integration_audit.json`
- `reports/stage4_integration_audit.md`

## Research Status

Stage 4 internally reconciled, subject to a passing integration audit.

The techno-economic model is a conditional analytical framework rather than a validated commercial project forecast.