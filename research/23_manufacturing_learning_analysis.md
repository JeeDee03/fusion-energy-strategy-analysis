# Stage 4.4 — FOAK-to-NOAK Manufacturing Learning Analysis

> Scope update — 5 November 2026: this chapter describes the original analytical layer. The current synthesis is [chapter 25](25_stage4_techno_economic_synthesis.md), with engineering generation in [28](28_engineering_constrained_generation.md), construction/replacement DCF in [29](29_construction_replacement_cash_flows.md), and current research status in [31](31_research_status_and_claims.md). Legacy omissions are not omissions of every later extension; conditional results remain uncalibrated.

## 1. Research Objective

Investigate whether repeated manufacturing and technological learning could reduce the construction cost of stellarator-based fusion power plants sufficiently to improve their economic competitiveness.

**Primary hypothesis:** H3 — Manufacturing Scalability.

The analysis focuses on the potential influence of HTS magnet-system manufacturing learning on the total capital cost and LCOE of a hypothetical Stellaris-based power plant.

## 2. Methodology

We apply a one-factor experience curve:

\[
C(N)=C_1(1-LR)^{\log_2(N)}
\]

where \(LR\) is the assumed cost reduction per doubling of cumulative equivalent production and \(N\) is the cumulative production index relative to the initial reference.

The model separates the initial magnet-system share from the remainder of plant CAPEX:

\[
CAPEX(N)=C_0[(1-s)+s(1-LR_m)^{\log_2(N)}]
\]

Only the magnet-system portion experiences learning. Non-magnet construction costs are held constant.

This approach avoids applying magnet cost reductions twice through simultaneous magnet-level and total-plant learning factors.

## 3. Initial Assumptions

The model uses the Stage 4.2 mid-CAPEX analyst scenario:

- Initial total CAPEX: EUR 12 billion.
- Initial magnet-system CAPEX share: 25%.
- Magnet-system learning rates: 0%, 10%, and 20%.
- Cumulative equivalent magnet sets: 1, 2, 4, 8 and 16.

All parameters are hypothetical and are not reported Proxima Fusion manufacturing costs or empirically calibrated stellarator learning rates.

Operating performance, net electrical power, fixed OPEX, variable OPEX, discount rate and lifetime remain fixed at the Stage 4.2 reference assumptions.

## 4. Results

At a 20% assumed magnet learning rate, four doublings of cumulative production reduce the modeled magnet-system cost to 40.96% of its initial value.

With an initial magnet share of 25%, total plant CAPEX falls by 14.76%, from EUR 12 billion to approximately EUR 10.23 billion.

The LCOE model translates this capital-cost reduction into a lower modeled electricity-generation cost, with operating performance and other economic variables held constant.

## 5. Required Learning Rate

For an illustrative objective of reducing total plant CAPEX by 10% at eight cumulative equivalent magnet sets:

\[
0.90=0.75+0.25(1-LR_m)^3
\]

The required magnet-system learning rate is approximately 15.66% per cumulative production doubling.

This is a model-derived requirement, not a forecast of Proxima's actual manufacturing learning.

## 6. Implications for H3

The model establishes that manufacturing learning could materially improve stellarator economics under certain conditions.

However, the benefit depends strongly on:

- The initial magnet-system share of plant CAPEX.
- The achievable learning rate.
- The number of comparable units manufactured.
- The extent to which manufacturing improvements transfer across designs.
- Whether additional production infrastructure and development expenditure are required.

The results do not confirm H3 for Proxima Fusion.

## 7. Important Limitations

1. Learning rates are not calibrated to observed commercial stellarator production data.
2. The initial magnet CAPEX share is an analyst assumption.
3. The cumulative production index represents equivalent plant-scale magnet sets, not a verified Proxima manufacturing forecast.
4. The model assumes constant non-magnet plant costs.
5. Additional manufacturing infrastructure and development investments are excluded.
6. Changes in material prices, design specifications, regulation and construction conditions are excluded.
7. FOAK and NOAK are conceptual development categories here, not independently identified production milestones.
8. The model estimates unit-level cost sensitivity, not the cumulative cost or cash flow of building an entire reactor fleet.

## 8. Strategic Relevance

The results suggest that Proxima's long-term cost competitiveness could depend partly on achieving repeatable magnet manufacturing processes and standardization.

However, the economic value of manufacturing learning must ultimately be compared with investments required to establish production capability and the risks associated with scaling the technology.

Stage 5 will investigate uncertainties around learning rates and component cost shares.

Stage 6 will consider how production partnerships and industrial development strategies might influence the commercialization pathway.

## References

- International Energy Agency, *Glossary: Learning rate and learning-by-doing*. https://www.iea.org/glossary
- Haas et al. (2023), *Technological learning: Lessons learned on energy technologies*. https://doi.org/10.1002/wene.463
- Proxima Fusion, Stellaris conceptual reactor design, source S3_006.

## Research Status

Stage 4.4 conditional learning-curve analysis. H3 remains unconfirmed pending empirical calibration and further economic assessment.
