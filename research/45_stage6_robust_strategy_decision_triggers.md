# Stage 6.5 — Robust Strategy Assessment and Decision Triggers

## Purpose
Stage 6.4 produced a stable **provisional** four-criterion MCDA winner (STR03) in all 15 price/stress contexts and four weight policies. This is a narrow result: the criteria and cash-flow contracts were hypothetical, and customer financing viability was omitted. This stage asks whether those provisional rankings survive minimal **stakeholder economic eligibility** tests.

## Method and inputs

- Existing 60 Stage 6.3 stakeholder allocation rows (STR01–STR04, P120/P170/P200, RS00–RS04).
- Existing 240 Stage 6.4 score rows, used only to label **provisional** leaders.
- `data/strategy_feasibility_policies.csv`: a disclosed, analyst-defined zero-NPV screening rule, not a real financing covenant.
- No empirical probabilities, contract terms, or company valuation parameters are inferred.

## Economic eligibility gates

Each strategy/price/stress record must satisfy:

1. `company_stressed_npv_eur >= 0` for Proxima;
2. `external_stressed_npv_eur >= 0` for an external plant owner, except STR01, which has no external owner in this model;
3. `stressed_project_npv_eur >= 0` for the plant project itself.

The company and external stakeholder cash flows must reconcile to the project value **less real incremental company costs**. Internal supplier payments are transfers, not new consolidated value. A passing gate is *necessary under this chosen policy*, not sufficient to establish customer demand, engineering success, financeability, or execution readiness. A failed gate is a result only under the current analytical assumptions.

## Price break-even thresholds

For each strategy/stress pair, calculate the company, external stakeholder and project NPV as a function of electricity price using Stage 6.3 rows at EUR 120, 170 and 200/MWh. Verify the three points exhibit linearity to numerical tolerance. Estimate the zero-NPV price for each entity by linear inversion; the **joint threshold** is the highest applicable threshold. STR01 has no external investor threshold.

**Critical restriction:** Thresholds above EUR 200/MWh are linear extrapolations and must not be represented as realistic attainable electricity prices. The model assumes all other contractual/engineering parameters remain unchanged as prices change.

## Outputs

- `reports/stage65_feasibility_screen.csv`: all 60 eligibility results.
- `reports/stage65_context_gate_summary.csv`: 15 price/stress contexts, provisional MCDA leaders and eligible alternatives.
- `reports/stage65_price_thresholds.csv`: 20 strategy/stress joint threshold estimates.
- `reports/stage65_feasibility_audit.json`: reproducibility and limitations.

## Interpretation rules

- If no strategy passes the gates, **withhold a strategic recommendation**. Do not select the top MCDA score as an economically viable winner.
- A positive supplier NPV can coexist with a negative customer NPV, an indication that a hypothetical sales arrangement cannot be assumed achievable.
- Results reflect a single hypothetical lifecycle engineering/construction baseline and allocation assumptions; they do not establish actual Stellaris viability.
- C05 financing exposure and C06–C08 manufacturing, execution and control require separate evidence. The unscored criteria may change any ranking.
- This study does not model debt, default, warranties, partner incentives, manufacturing investment, contract repricing, strategic option value, project portfolios or public grants.

## Decision triggers for future research

| Gate | Evidence needed | Decision implication |
|---|---|---|
| Engineering maturity | Validated performance, operational availability and maintainability | Revisit output and replacement assumptions before commercial commitments |
| Construction economics | Credible EPC budgets, schedule and contingencies | Update CAPEX and delay distributions |
| Customer/partner bankability | Signed or financeable project contracts and credible partner equity/debt terms | Confirm positive **risk-adjusted** customer value; revise supplier margin as needed |
| Manufacturing readiness | Magnet production costs, qualification, factory capex and scale | Calibrate H3 and supplier working-capital commitments |
| Revenue security | Credible power purchase agreements, contracted tariffs and grid access | Replace constant electricity-price hypotheticals |
| Governance and liability | Contractual warranties, IP rights, ownership, risk transfer prices | Rebuild stakeholder cash flows and complete C05–C08 |

## Stage 6.6 handover

Combine the Stage 6.4 partial rankings with these economic gate results. Make conditional—not categorical—recommendations; explicitly flag evidence gaps and preserve Stage 5 convergence/calibration limitations. Do not claim H2 has been causally proven by synthetic contractual risk transfers.
