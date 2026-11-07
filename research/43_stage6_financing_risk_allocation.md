# Stage 6.3 — Financing, Partnerships and Contractual Risk Allocation

## Objective

Evaluate how four analytical commercialization arrangements distribute changes in project financial value caused by construction overruns, delayed commercial operation and electricity-price shortfalls. The analysis distinguishes **underlying project economics** from **Proxima's assumed economic exposure**. All percentages are analyst scenarios, not verified Proxima agreements.

## Connection to Stage 6.2

The authoritative engineering and lifecycle models are reused (`GEN002`, `LC004`, `CAL002`). Stage 6.2 provides the baseline company and external partner NPV, including carved-out supplier margins and incremental company setup and overhead. No project-level supplier invoice is double-counted.

Stage 6.3 measures a *change* in overall project NPV and distributes that change between Proxima and external stakeholders under declared hypothetical contractual risk shares. The model is an NPV-level allocation experiment, **not** a debt-financing model, financing waterfall or complete annual cash-flow simulation.

## Structural risk scenarios

- **RS00:** No additional shock (reference).
- **RS01:** +20% overnight construction CAPEX; replacement amounts unchanged.
- **RS02:** +2 years to commercial operation. Existing construction expenditures remain at the original dates; operating and replacement cash flows shift later.
- **RS03:** −20% constant real electricity sale price, with production held fixed.
- **RS04:** Combination of the three shocks.

The experiment evaluates the same three Stage 6.2 reference electricity prices (€120, €170, €200/MWh) and four strategy alternatives: 4 × 3 × 5 = 60 scenarios.

## Contractual risk sharing

The file `data/strategy_risk_allocation.csv` records the assumed share of each adverse NPV change retained by Proxima. The balance is attributed to the external partner. These numbers may differ from equity stakes to represent hypothetical contractual warranties, guarantees, indemnities or risk transfers. They are not actual corporate financing terms.

For the combined case, the NPV change is decomposed **in this fixed order**: CAPEX overrun, COD delay, electricity-price decrease. Each incremental difference is allocated using its corresponding risk share. The ordering is a reporting convention and influences interaction attribution. The *total* combined project NPV change is calculated from the actual combined stressed lifecycle case, not by adding isolated effects.

## Mathematical conservation

Let \(V_0\) be baseline project NPV, \(V_s\) stressed project NPV, and \(\Delta V_k\) sequential stress components. Let \(\gamma_{k,j}\) be company \(j\)'s contractual share of effect \(k\).

\[
V_{P,s}=V_{P,0}+\sum_k\gamma_{k,j}\Delta V_k
\]

\[
V_{E,s}=V_{E,0}+\sum_k(1-\gamma_{k,j})\Delta V_k
\]

The accounting identity is:

\[
V_{P,s}+V_{E,s}=V_s-PV(\text{incremental company setup and overhead})
\]

Contractual sharing does not make project overrun or delayed revenue disappear. A smaller negative impact for Proxima means greater exposure elsewhere under the same stress assumptions.

## Scientific boundaries

This model excludes debt, equity fundraising, WACC changes, tax shields, solvency, actual credit support, payment defaults, contract enforceability, construction insurance and the price of transferring risk. It keeps Stage 6.2 baseline supplier margins fixed during project shocks. Consequently, lower allocated exposure **cannot** be called a free financial improvement or evidence that a real counterparty will accept the risk.

The model uses the Stage 4/5 real EUR_2024 pre-tax unlevered lifecycle basis. It does not calculate Proxima's enterprise valuation or rank strategies.

## Acceptance and next session

1. Validate 60 results and all reference baselines against Stage 6.2.
2. Demonstrate exact company/external/project NPV reconciliation.
3. Validate independent shock signs, and correct combined NPV calculations.
4. Preserve input hashes and scenario disclosures.
5. Record conditional results without assigning probabilities or a strategic recommendation.

Stage 6.4 will examine transparent MCDA criteria and weights, subject to further checks for overlap and qualitative evidence quality. Stage 6.5 will test ranking stability and define strategic decision triggers. H2 remains unconfirmed until real financing and partnership evidence supports a stronger conclusion.
