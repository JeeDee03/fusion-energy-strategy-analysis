# Stage 6.4 — Preliminary Multi-Criteria Decision Analysis (MCDA)

## Objective

Assess whether provisional attractiveness comparisons among STR01–STR04 depend on the importance placed on company-level modeled value, ownership exposure, construction risk, and electricity-price risk. Stage 6.4 is **not** a final eight-criterion strategic ranking.

## Relationship to prior stages

- Stage 6.1 defines four analytical alternatives and criteria C01–C08.
- Stage 6.2 supplies hypothetical company-level NPV under supplier transfers and ownership arrangements.
- Stage 6.3 allocates modeled construction, delay, and revenue shocks through hypothetical risk-sharing assumptions.
- Stages 4–5 supply conditional techno-economic mechanisms and sensitivity evidence, not empirical contract forecasts.

## Criterion coverage and gaps

The first quantifiable screening includes:

- **C01 — Company capital commitment:** proxied by Proxima's assumed equity fraction, lower preferred. This is **not** measured cash-at-risk.
- **C02 — Company value capture:** Stage 6.3 company's modeled stressed NPV, higher preferred.
- **C03 — Construction risk retained:** assumed fraction of CAPEX overrun borne by Proxima, lower preferred.
- **C04 — Revenue risk retained:** assumed electricity-price shortfall fraction borne by Proxima, lower preferred.

**C05** is excluded because it overlaps C01 and other financing-related values without an independent debt-financing model. **C06–C08** remain unscored until there is adequate strategy-specific manufacturing, capability, and control evidence. Refer to `data/strategy_mcda_evidence_register.csv`.

## Scoring methodology

For each of 15 price × stress scenarios, the four strategies are compared on each criterion independently. Higher-is-better numeric measures are min-max normalized: `(x - min)/(max-min)`. Lower-is-better numeric measures are sign-inverted before normalization. A constant criterion receives neutral 0.5 for every strategy; it cannot distinguish alternatives.

A provisional composite score is the weighted sum of the four normalized scores. All weights are declared analyst preferences; see `data/strategy_mcda_weights.csv`. Four weighting policies are evaluated: BALANCED, VALUE_FOCUS, CAPITAL_FOCUS and RISK_FOCUS.

These are within-context comparisons. Scores cannot be treated as comparable across different price or stress cases, and rankings are not verified company-strategy prescriptions. Criteria C01 and C03 remain partially overlapping despite the explicit C05 exclusion.

## Robustness

`reports/stage64_weight_robustness.csv` identifies contexts where the highest-scoring strategy changes across policies, retaining ties. It diagnoses sensitivity to preferences, not the likelihood that a strategy will succeed.

A meaningful future extension requires evidence-supported qualitative scoring for C06–C08, direct funded-capital estimates, contractual obligations and explicit trade-off deliberation before a final MCDA can be considered.

## Required validation

- Full and unique coverage of 4 strategies × 3 prices × 5 shocks.
- Exact Stage 6.2 baseline reconciliation under RS00.
- Scores within [0,1], normalized weighting sums of 1.
- Independent regeneration of results from source inputs.
- Documented exclusion of C05–C08 and nonempirical scoring.

## Research limitations

A supplier showing positive company NPV may depend on selling to a project owner with unattractive economics. The model omits contract feasibility, debt structures, partner willingness, differentiated discount rates, liability pricing, and strategic control outcomes. The supplier-margin and ownership assumptions are analyst-defined.

**Research status:** Provisional four-criterion economic/risk screening. Stage 6.5 will evaluate conditional decision triggers; a complete eight-criterion MCDA is not yet justified.
