# Stage 4.1 — Techno-Economic Model Architecture

> Scope update — 5 November 2026: this chapter describes the original analytical layer. The current synthesis is [chapter 25](25_stage4_techno_economic_synthesis.md), with engineering generation in [28](28_engineering_constrained_generation.md), construction/replacement DCF in [29](29_construction_replacement_cash_flows.md), and current research status in [31](31_research_status_and_claims.md). Legacy omissions are not omissions of every later extension; conditional results remain uncalibrated.

## 1. Research Objective

Develop a reproducible techno-economic model to investigate the conditions under which stellarator-based fusion electricity could become commercially competitive in Europe.

The initial modeling focus is Proxima Fusion's Stellaris commercial reactor concept.

**Primary hypotheses:** H1 — Technology Economics; H3 — Manufacturing Scalability.

**Secondary application:** H2 — Financing and commercialization strategies, to be investigated through subsequent investment and strategic models.

## 2. Initial Economic Metric

The first model evaluates Levelized Cost of Energy (LCOE), expressed in real EUR/MWh.

The simplified annualized formulation is:

\[
LCOE =
\frac{CAPEX \cdot CRF + FOM}
{P_{\mathrm{net}} \cdot 8760 \cdot CF}
+ VOM
\]

The capital recovery factor is:

\[
CRF = \frac{r}{1-(1+r)^{-N}}
\]

where \(r\) is the real annual discount rate and \(N\) is the plant lifetime in years.

## 3. Model Boundaries

The initial model assumes:

- Investment occurs at time zero.
- Annual net output and operating costs are constant.
- The discount rate and monetary values are expressed consistently in real terms.
- No separate major component-replacement expenditures.
- No explicit construction financing or construction schedule.
- No tax, subsidy, decommissioning or salvage accounting.
- No electricity sales or revenue assumptions.

These simplifications make the first model suitable for testing mathematical behavior, not for drawing commercial feasibility conclusions.

## 4. Assumption and Evidence Classification

The first input dataset, `data/lcoe_scenarios.csv`, contains synthetic test scenarios.

All values are hypothetical and are not represented as Proxima Fusion's commercial plant specifications.

Future scenarios must distinguish:

- Literature-reported inputs
- Company-reported design targets
- Independently verified values
- Modeled estimates
- Scenario assumptions
- Missing information

The existing `economic_input_register.csv` remains the reference for unresolved economic model inputs.

## 5. Outputs

The model produces:

- Annual net electricity generation in MWh
- Capital recovery factor
- Equivalent annual capital cost
- Equivalent annual total cost
- Simplified LCOE in EUR/MWh

## 6. Validation

Initial validation checks include:

1. Increasing CAPEX increases LCOE, all else equal.
2. Decreasing capacity factor increases LCOE when positive fixed costs exist.
3. At zero discount rate, CRF equals the reciprocal of plant lifetime.
4. Electricity production is consistent with net capacity and capacity factor.
5. Numeric inputs and device identifiers are validated.

Successful tests establish internal mathematical consistency, not commercial accuracy.

## 7. Research Implications

The model architecture provides the starting point for evaluating whether the operating benefits of a stellarator could offset higher construction or maintenance costs.

It also provides a foundation for examining FOAK-to-NOAK manufacturing learning and subsequent project investment scenarios.

## 8. Originally Planned Next Steps

Stage 4.2 will establish evidence-based cost scenarios and document assumptions.

Stage 4.3 will connect engineering performance variables to LCOE.

Stage 4.4 will model manufacturing learning.

Stage 4.5 will evaluate electricity revenue and discounted cash flows.

## References

- National Renewable Energy Laboratory / National Laboratory of the Rockies, *Simple Levelized Cost of Energy Calculator Documentation*, https://nrel.sitefinity.cloud/analysis/tech-lcoe-documentation
- National Laboratory of the Rockies, *2025 Annual Technology Baseline — Equations and Variables*, https://atb.nlr.gov/electricity/2025/equations_%26_variables

## Research Status

Stage 4.1 is the completed initial modeling layer. Subsequent Stage 4.2–4.5 analyses and the extended engineering/lifecycle models are documented separately. The original synthetic inputs do not establish empirically validated commercial competitiveness.
