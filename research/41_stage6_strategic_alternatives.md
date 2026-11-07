# Stage 6.1 — Strategic Alternatives and Decision Framework

## 1. Research Objective

Stage 6 translates the engineering, techno-economic and uncertainty findings of Stages 1–5 into a structured assessment of commercialization strategies for Proxima Fusion.

The objective is to determine under which technological, financial and market conditions different commercialization models may be strategically attractive.

The analysis addresses the second part of the central research question:

> What strategic positioning should Proxima Fusion pursue to improve the commercial competitiveness of stellarator-based fusion?

This stage does not assume that any particular business model is optimal. Instead, it establishes alternatives, economic boundaries, evaluation criteria and evidence requirements for subsequent quantitative analysis.

## 2. Research Background

The preceding research stages established several relevant findings.

### 2.1 Engineering and Technological Context

Stage 3 examined stellarator engineering characteristics, including superconducting magnet systems, manufacturing complexity, maintenance requirements, effective electricity generation and technology maturity.

These factors affect potential plant construction costs, operational performance and commercialization requirements.

### 2.2 Techno-Economic Findings

Stage 4 developed models for:

- Levelized Cost of Energy (LCOE)
- Capital expenditure and operating-cost sensitivity
- Engineering-constrained electricity generation
- Construction timing and lifecycle cash flows
- Major component replacement expenditure
- Manufacturing learning and standardization
- Lifecycle break-even electricity prices and project Net Present Value (NPV)

These models establish conditional economic relationships, rather than validated commercial Stellaris costs.

### 2.3 Uncertainty and Risk Findings

Stage 5 examined uncertainty in construction costs, operating expenses, discount rates and electricity revenue.

The exploratory simulations identified construction capital intensity, electricity sale prices and discount rates as important drivers of modeled investment outcomes.

Alternative distributions and economic dependence assumptions materially changed the resulting NPV distributions.

Manufacturing learning improved modeled lifecycle economics, but did not eliminate the negative median NPV in the analyzed reference scenario.

The results remain conditional on exploratory assumptions and do not represent empirically calibrated probabilities of commercial success.

## 3. Distinguishing Project Economics from Company Economics

A central methodological distinction in Stage 6 is the difference between power-plant project economics and Proxima Fusion's company-level economics.

### 3.1 Project-Level Economics

The models developed in Stages 4–5 evaluate a hypothetical power-generating asset.

Their economic outputs include:

- Construction investment
- Operating and maintenance expenditure
- Electricity revenue
- Major component replacements
- Lifecycle NPV
- Break-even electricity sale price

These results describe the modeled project as a whole.

### 3.2 Company-Level Economics

The economic value captured by Proxima Fusion depends on its contractual and ownership position.

Potential sources of company-level value include:

- Ownership distributions from power-plant projects
- Reactor technology and equipment sales
- Engineering and development fees
- Technology licensing and royalties
- Long-term service and maintenance agreements

Proxima may also face company-level costs and risks, including:

- Research and development expenditure
- Manufacturing investment
- Equity contributions to projects
- Product qualification and delivery obligations
- Warranty and performance liabilities
- Organizational and financing costs

Consequently, positive project NPV does not necessarily imply positive NPV for Proxima Fusion.

Similarly, a project with unattractive economics for its owner may still generate contractual revenue for a technology supplier, although the sustainability of that revenue depends on customer demand, delivery obligations and the project's eventual commercial viability.

Stage 6 must therefore model the distribution of investment, risk and value between Proxima and external stakeholders.

## 4. Strategic Alternatives

Four analytical commercialization alternatives are defined.

These represent hypothetical decision options. They are not assertions that Proxima Fusion has formally selected or committed to all four models.

The canonical alternative definitions are maintained in:

`data/strategy_alternatives.csv`

### STR01 — Vertically Integrated Developer and Operator

Under STR01, Proxima retains a major ownership and operating role in commercial fusion power plants.

Potential advantages:

- Greater participation in electricity revenue and project-level value creation
- Stronger control over technology deployment
- Direct operational experience
- Closer integration between reactor development and power-plant operation

Potential disadvantages:

- Substantial company-level capital requirements
- Construction and operating risk exposure
- Greater sensitivity to electricity market conditions
- Additional organizational capabilities required for infrastructure development and operation

The main research question is whether retained ownership benefits can justify the required capital commitment and risk exposure.

### STR02 — Utility Joint Venture

Under STR02, Proxima cooperates with a utility or infrastructure partner through shared project ownership and negotiated commercial arrangements.

Potential advantages:

- Shared equity and capital requirements
- Access to power-project development and operating experience
- Potential access to customers and electricity offtake arrangements
- Allocation of selected construction and operating responsibilities

Potential disadvantages:

- Reduced direct ownership of project cash flows
- Negotiation and governance complexity
- Possible conflicts between technology-development and investor objectives
- Dependence on partner commitment and contractual terms

The main research question is whether risk sharing and complementary capabilities compensate for reduced ownership and strategic autonomy.

### STR03 — Reactor Technology Provider / OEM

Under STR03, Proxima primarily develops and supplies fusion reactor technology to external plant owners.

An Original Equipment Manufacturer (OEM) supplies equipment or integrated technical systems to customers who may retain ownership and operational responsibility.

Potential revenue mechanisms include:

- Reactor systems sales
- Engineering services
- Technology licensing
- Royalties
- Long-term technical support agreements

Potential advantages:

- Reduced direct ownership of power-plant assets
- Potential for a more scalable supplier business model
- Concentration on reactor technology and engineering capabilities
- Opportunities to serve multiple plant developers

Potential disadvantages:

- Dependence on customer project financing and deployment
- Supplier delivery and performance obligations
- Potential warranty and liability exposure
- Lower participation in long-term electricity revenue
- Possible manufacturing and working-capital requirements

The main research question is whether technology revenues can create attractive company-level value without requiring Proxima to retain substantial project ownership.

### STR04 — Hybrid Phased Commercialization

Under STR04, Proxima initially retains a stronger role in demonstrating or developing an early reference plant and subsequently expands into joint ventures, technology supply or licensing.

Potential advantages:

- Opportunity to establish a commercial technology reference
- Operational learning from early projects
- Flexibility to adjust ownership and commercialization structures over time
- Potential to separate technology-validation activities from later scaling

Potential disadvantages:

- Early-stage capital exposure
- Complex transitions in organizational responsibility
- Potential conflicts between asset ownership and technology-supplier objectives
- Uncertainty regarding the timing of commercial maturity

The main research question is whether a phased business model can balance technology validation, strategic flexibility and long-term scalability.

## 5. Strategic Evaluation Criteria

Eight preliminary criteria are defined in:

`data/strategy_decision_criteria.csv`

| ID | Criterion | Preferred direction |
|---|---|---|
| C01 | Proxima capital commitment | Lower |
| C02 | Proxima value capture | Higher |
| C03 | Construction risk retained | Lower |
| C04 | Revenue risk retained | Lower |
| C05 | Financing exposure | Lower |
| C06 | Manufacturing learning opportunity | Higher |
| C07 | Execution capability alignment | Higher |
| C08 | Strategic control | Higher |

### 5.1 Economic Criteria

C01 and C02 concern the company's financial exposure and value capture.

These should be evaluated using explicit company-level cash-flow assumptions rather than by assigning project NPV directly to Proxima.

### 5.2 Risk Criteria

C03, C04 and C05 concern the risks retained by the company.

Their evaluation must distinguish:

- Direct financial obligations
- Contractually transferred risks
- Residual guarantees and performance liabilities
- Risks shared between counterparties

The same underlying economic exposure must not be counted repeatedly under several criteria without justification.

### 5.3 Engineering and Strategic Criteria

C06–C08 examine manufacturing scale, execution capability and strategic control.

These dimensions may require evidence-supported ordinal assessments when direct monetary estimates are unavailable.

Qualitative judgments must be traceable to their assumptions or sources.

## 6. Evidence Classification

All Stage 6 claims and assumptions should be assigned an appropriate evidence classification.

The analysis distinguishes:

1. **Documented evidence:** Publicly disclosed company activities, published studies and other traceable sources.
2. **Model-derived result:** An output calculated from specified inputs and mathematical relationships.
3. **Analytical assumption:** A hypothetical ownership arrangement, contract, cost allocation or strategic scenario.
4. **Research gap:** A parameter or relationship for which available evidence is insufficient.

An analytical alternative must not be described as an announced Proxima Fusion strategy without supporting evidence.

Similarly, a conditional model ranking must not be presented as a verified corporate recommendation.

## 7. Research Boundaries

Stage 6 will preserve the methodological boundaries established in earlier stages.

In particular:

- Stages 4–5 do not provide verified Stellaris commercial cost forecasts.
- Simulated NPV frequencies are conditional on exploratory distributions.
- The strict Stage 5.3 numerical convergence requirement remains unmet.
- Project-level cash flows must not be automatically interpreted as Proxima-level cash flows.
- Equity financing and contractual risk allocation require explicit assumptions.
- Technology-supplier revenue cannot be equated with total power-plant electricity revenue.
- Commercial feasibility and organizational capability must be assessed separately.

Any illustrative strategic assessment must clearly disclose unsupported contractual and ownership assumptions.

## 8. Stage 6 Research Sequence

### Stage 6.2 — Business Model and Value Capture

Construct company-level economic representations of the four alternatives.

Identify revenue streams, costs, ownership claims and financial obligations.

### Stage 6.3 — Financing and Risk Allocation

Evaluate how alternative financing and partnership arrangements distribute construction, revenue, delivery and operating risks.

### Stage 6.4 — Multi-Criteria Decision Analysis

Develop a transparent decision model using the predefined criteria.

Document the scoring method, weighting assumptions and evidence quality.

### Stage 6.5 — Robustness and Decision Triggers

Test strategic rankings under different financial, engineering and organizational assumptions.

Identify conditions under which preferred alternatives change.

### Stage 6.6 — Integrated Strategic Synthesis

Evaluate the strength of evidence relating to H2, summarize conditional recommendations and prepare the final research report.

## 9. Stage 6.1 Acceptance Requirements

Stage 6.1 is complete when:

- Four strategic alternatives are uniquely defined.
- Eight decision criteria are documented.
- Alternative and criterion registers pass structural validation.
- Project-level and company-level economic boundaries are explicit.
- Hypothetical strategic alternatives are distinguished from documented company activities.
- No unsupported strategic rankings or numerical weights are introduced.
- The Stage 6.2 handover is documented.

## 10. Stage 6.2 Handover

The next task is to construct an analytical company-level value-capture framework.

This framework must distinguish project cash flows from technology-developer revenues, ownership distributions, equity contributions and contractual costs.

It must also preserve consistency with the existing lifecycle financial model and avoid claiming that hypothetical commercial agreements represent actual Proxima Fusion contracts.

**Stage 6.1 outcome:** Strategic decision alternatives and evaluation criteria established. Financial comparison and strategy ranking remain pending.