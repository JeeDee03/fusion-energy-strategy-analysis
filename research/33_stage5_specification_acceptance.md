# Stage 5.1 — Uncertainty Specification Acceptance

## 1. Research Objective

Establish a reproducible, internally consistent uncertainty-analysis framework for the Proxima Fusion techno-economic research project before implementing Monte Carlo simulation.

Stage 5 extends the engineering-constrained generation and lifecycle economic models developed during Stages 1–4.

**Canonical specification:** `data/stage5_uncertainty_spec.json`

**Scientific methodology:** `research/32_stage5_uncertainty_specification.md`

## 2. Model Architecture

The primary economic outputs will be:

- Lifecycle break-even electricity price (real EUR_2024/MWh)
- Project net present value (real EUR_2024)
- Conditional fraction of simulated cases with positive project NPV
- P5, P50 and P95 economic outcome quantiles

The simulation will use the engineering generation and lifecycle cash-flow models.

The simplified annualized LCOE model remains available for consistency checks.

## 3. Uncertainty Classification

### Sampled parameters

The initial Monte Carlo experiment will sample five economic parameters:

1. Overnight construction CAPEX intensity
2. Annual fixed operating expenditure
3. Variable operating expenditure
4. Real discount rate
5. Electricity sale price

The initial marginal distributions are exploratory uniform distributions defined in the canonical specification.

### Engineering-derived parameters

Net electrical output and effective electricity generation will be calculated from the selected engineering scenarios.

These parameters will not be independently sampled in the initial experiment.

### Fixed parameters

Plant operating lifetime and other model constants will remain fixed according to the accepted specification.

### Separate manufacturing-learning extension

Magnet CAPEX share and manufacturing learning rate will be addressed separately to investigate H3 without double-counting capital-cost reductions.

## 4. Structural Contexts

The initial Monte Carlo experiment will evaluate 12 structural contexts.

Engineering scenarios:

- GEN002
- GEN003
- GEN007

Construction scenarios:

- LC004
- LC006

Replacement-cost fractions:

- 5%
- 10%

Each structural context will be analyzed separately.

No probability weighting across structural contexts is assumed.

## 5. Sampling and Reproducibility

The simulation engine must follow the canonical configuration for:

- NumPy PCG64 random-number generation
- Fixed master seeds
- Nested simulation sample sizes
- Matched random draws across structural contexts
- Input validation and error reporting
- Quantile calculations and sampling precision
- Convergence and reproducibility checks

The initial simulation must preserve the distinction between numerical sampling precision and uncertainty in the underlying economic assumptions.

## 6. Deterministic Preflight

The specification validator performs deterministic evaluations covering the defined structural contexts and selected input combinations.

Expected coverage:

- 12 structural contexts
- 33 deterministic evaluations per context
- 396 deterministic evaluations in total

These evaluations are not Monte Carlo samples.

The preflight confirms model executability and internal consistency under the tested inputs. It does not establish physical feasibility or empirical validity.

## 7. Acceptance Criteria

Stage 5.1 is accepted for implementation only if:

- The Stage 1–4 ordered rebuild completes successfully.
- Regression tests pass.
- Input freshness checks confirm current research artifacts.
- The uncertainty specification validator reports no errors.
- The deterministic design matrix contains all 12 contexts.
- All 396 expected deterministic evaluations are present.
- Relevant research limitations and provenance requirements remain documented.

**Acceptance status: Pending final local verification.**

## 8. Remaining Research Limitations

The initial probability distributions are exploratory analyst assumptions rather than empirically established distributions of commercial Stellaris performance.

The uncertainty analysis cannot independently establish:

- Actual construction or operating costs
- Commercial reactor availability
- Verified manufacturing learning rates
- Achievable electricity sale prices
- Real-world probability of commercial success
- Confirmation of H1, H2 or H3

## 9. Stage 5.2 Implementation Handover

Stage 5.2 will implement a reproducible Monte Carlo simulation engine based on the accepted specification.

The engine must:

1. Preserve the accepted uncertainty parameter definitions.
2. Use the engineering generation and lifecycle cash-flow models.
3. Evaluate all 12 structural contexts separately.
4. Avoid double-counting CAPEX, maintenance or replacement costs.
5. Use reproducible random-number generation.
6. Retain sufficient metadata to reconstruct simulation results.
7. Produce scenario-level LCOE or lifecycle break-even price and NPV distributions.
8. Report convergence and numerical uncertainty.
9. Clearly identify all outputs as conditional on exploratory input assumptions.

## Research Status

Stage 5.1 specification acceptance review. Main Monte Carlo simulation has not yet been conducted.