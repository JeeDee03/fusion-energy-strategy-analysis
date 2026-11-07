# Stages 1–4 — Research Status, Claims and Interpretation

Review date: 5 November 2026. Updated through improvement Step 9 of 9; this numbering is separate from the main research stages.

## What is being investigated?

The project asks under which engineering, economic and market conditions stellarator fusion could compete in Europe, and what this would imply for Proxima's commercialization strategy. It combines selected disclosed financing and partnership evidence, a historical electricity baseline, technical/source comparison and conditional plant models. It does not estimate a probability of Proxima's commercial success.

## What has been implemented?

| Main stage | Current state | Remaining boundary |
|---|---|---|
| 1 | Research question, protocol and H1–H3 defined | Hypotheses remain open. |
| 2 | Descriptive funding/partnership baseline and 2024 DE/LU analysis | Selected incomplete histories, differing funding definitions, original ECB snapshot archival gap; historical prices are not forecasts. |
| 3 | Engineering evidence and five-company/eight-criterion comparison | Selected-source gaps, unlike maturity evidence, no cost/readiness ranking. |
| 4 | Annual LCOE, sensitivities, learning, legacy DCF, engineering generation and construction/replacement DCF | Analyst assumptions; empirical cost/performance calibration and human review remain open. |
| 5 | Planned | Specification in chapter 32; simulations not implemented. |
| 6 | Planned | Company-level strategy allocations/retained value not modeled. |
| 7 | Planned | Final paper, dashboard and strategy presentation not yet completed. |

The financing baseline retains its 28 October cutoff. The separate company source snapshot is reviewed through 5 November; it does not silently update financing history. Primary company statements, conceptual design results and achieved experiments remain distinct evidence kinds.

## What has been found and why?

The [current Stage 4 synthesis](25_stage4_techno_economic_synthesis.md) explains the quantitative mechanisms. Model findings arise from explicit cost, generation and timing assumptions: spreading fixed costs, discounting delayed receipts and applying learning to a subsystem share. They establish conditional relationships, rather than empirical plant cost or engineering superiority. Partnership descriptions do not establish causal financing benefits.

The canonical definitions and assessment are in `data/research_status.json`. Proposal, protocol, README and synthesis share checked hypothesis blocks. `reports/research_consistency_summary.md` lists the current numerical anchors, scopes and required next evidence. The audit checks those anchors against generated tables and verifies selected relative links; it does not independently review arbitrary natural-language claims or sources.

## Reproduction and shared provenance

Run `python src/run_stage14.py`, the regression suite, then `python src/check_stage14_freshness.py`. This rebuilds Stage 1–2 before Stage 3–4, runs closure screening and verifies both complete records against current inputs, outputs, scripts and dependency versions. Changed shared company metadata invalidates an older Stage 1–2 record. Existing Stage 3–4-only commands remain available but do not certify Stage 1–2 freshness.

A fresh record and a passing test suite establish execution/data consistency. Editorial review, factual verification, calibration and publication approval remain separate. Human milestone reviews are retained byte-for-byte. The legacy no-construction/constant-CF model and the construction/replacement extension keep distinct boundaries.

## Next evidence and handover

1. Review source locators and qualifiers, undisclosed contract terms and comparative engineering evidence.
2. Calibrate CAPEX, OPEX, replacement allocation, construction schedules, net power/auxiliaries, availability and learning inputs where evidence permits; retain unknowns explicitly.
3. Apply the completed [uncertainty specification](32_stage5_uncertainty_specification.md): exploratory ranges/densities, unweighted structural contexts, derived generation, dependence sensitivity and convergence criteria are explicit. Its deterministic preflight is not probabilistic analysis.
4. Only then implement main Stage 5 simulations. Main Stage 6 compares strategies under explicit company-level allocations; main Stage 7 produces final research deliverables.
