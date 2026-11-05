# Stage 4.5 — Electricity Revenue, NPV and Commercial Viability

## 1. Research Objective

Evaluate the sensitivity of an illustrative Stellaris power-plant investment to electricity sale prices using a discounted-cash-flow framework.

The analysis builds on the cost assumptions established in Stage 4.2 and the engineering-economic relationships examined in Stages 4.3 and 4.4.

The objective is to distinguish electricity-generation cost from project investment value.

## 2. Financial Model

The model uses the following simplified project cash-flow equation:

\[
FCF_t=E_tP_t-FOM_t-VOM_tE_t
\]

Net Present Value is calculated as:

\[
NPV=-CAPEX+\sum_{t=1}^{N}\frac{FCF_t}{(1+r)^t}
\]

The model is expressed in real euros and uses a real discount rate.

It is a pre-tax, unlevered project model. It does not separately include interest expenses, principal repayments or tax effects.

## 3. Reference Economic Assumptions

The reference is the hypothetical Stage 4.2 mid-CAPEX scenario, CAL002:

- Total upfront CAPEX: EUR 12 billion.
- Rated net electrical capacity: 1,000 MWe.
- Net electrical capacity factor: 85%.
- Fixed annual OPEX: EUR 200 million.
- Variable OPEX: EUR 5/MWh.
- Economic operating lifetime: 35 years.
- Real discount rate: 8%.

These figures remain analyst scenario assumptions, not verified Proxima Fusion cost or performance estimates.

## 4. Electricity Revenue Scenarios

Four constant real electricity sale-price cases are investigated:

| Scenario | Sale price (EUR/MWh) | Classification |
|---|---:|---|
| 2024 German wholesale average | 78.51 | Historical-price stress test |
| Low fixed-price case | 120 | Analyst scenario |
| Intermediate fixed-price case | 170 | Analyst scenario |
| High fixed-price case | 200 | Analyst scenario |

Germany's reported 2024 average day-ahead price is used only as a historical reference. It is not presented as a forecast for future fusion power plant operation.

The remaining values are hypothetical fixed-price assumptions rather than actual power purchase agreements.

## 5. Results and Interpretation

The model calculates annual electricity generation, annual electricity revenue, operating cash flow and discounted project NPV.

Under the central hypothetical cost assumptions, the break-even constant real electricity price is approximately EUR 170.14/MWh.

A constant sale price below this level yields negative NPV, while a sale price above this level yields positive NPV.

At the break-even price, NPV is approximately zero, consistent with the simplified LCOE calculation using the same cost boundaries and discount rate.

The results demonstrate the importance of revenue realization to the investment economics of capital-intensive electricity infrastructure.

They do not establish that Proxima Fusion could obtain the assumed sale prices or achieve the modeled cost structure.

## 6. Connection to the German Electricity Market

Stage 2 collected German historical wholesale electricity-price data for 2024.

The German Federal Network Agency reports an average day-ahead electricity price of EUR 78.51/MWh for the year.

The historical price series provides information about market volatility and the presence of negative-price periods.

However, historical annual averages and hourly prices cannot be interpreted as forecasts of future fusion plant revenue.

Further analysis should consider hourly generation profiles, achieved capture prices, market evolution, potential offtake agreements and uncertainty.

Source: Bundesnetzagentur / SMARD, 2024 electricity-market review.

## 7. Strategic Implications

The distinction between LCOE and NPV is important for evaluating the commercialization of fusion electricity.

A technologically successful plant may still fail to satisfy investors' required returns if electricity revenues are insufficient.

Conversely, favorable long-term contracts may improve revenue predictability and potentially influence financing risk.

These potential advantages cannot be quantified without additional evidence about customer demand, contract terms, risk allocation and financing structures.

The findings provide a foundation for later evaluation of H2.

## 8. Model Limitations

1. All capital expenditure occurs at time zero.
2. No construction schedule or financing during construction is modeled.
3. Generation and real operating costs remain constant.
4. No component replacement, decommissioning or salvage expenditure is included.
5. No corporate income taxes, tax depreciation or subsidies are modeled.
6. No debt financing or equity cash-flow waterfall is represented.
7. Electricity sale prices are constant in real terms.
8. Grid fees, balancing costs, curtailment and contract settlement details are excluded.
9. No hourly generation or market-price capture model is included.
10. Real future commercial plant costs and electricity sale prices remain unknown.

The model is suitable for conditional economic analysis, not for valuing Proxima Fusion or predicting the profitability of an actual investment project.

## 9. Research Status and Next Steps

Stage 4.5 establishes a reproducible project cash-flow and NPV framework.

Stage 4.6 will integrate the techno-economic outputs and assess consistency across engineering, cost, performance, manufacturing learning and revenue assumptions.

Stage 5 will investigate uncertainty, including capital expenditure, capacity factor, learning effects and electricity-price risk.

Stage 6 will examine how commercialization and partnership structures may influence project economics and strategic positioning.

## References

- Bundesnetzagentur / SMARD, *Evaluation of Last Year: Electricity Market 2024*, https://www.smard.de/page/en/topic-article/5892/215704/evaluation-of-last-year
- National Laboratory of the Rockies, *2025 Annual Technology Baseline — Financial Cases and Methods*, https://atb.nlr.gov/electricity/2025/financial_cases_%26_methods
- National Laboratory of the Rockies, *2025 Annual Technology Baseline — Equations and Variables*, https://atb.nlr.gov/electricity/2025/equations_%26_variables

## Research Conclusion

Project viability depends jointly on power plant costs, net electricity production, electricity sale prices and the required rate of return.

The model demonstrates these relationships quantitatively under hypothetical conditions, but it does not establish commercial competitiveness for Proxima Fusion.