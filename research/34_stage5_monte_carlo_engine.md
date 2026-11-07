# Stage 5.2 — Lifecycle Monte Carlo Simulation Engine

## 1. Objective

Implement a reproducible Monte Carlo simulation to investigate how uncertain economic inputs affect the lifecycle break-even electricity price and project NPV of a hypothetical Stellaris-based fusion power plant.

The analysis follows the uncertainty specification established in Stage 5.1.

## 2. Methodology

The initial experiment samples five uncertain economic parameters:

- Overnight CAPEX intensity
- Routine fixed OPEX
- Routine variable OPEX
- Real discount rate
- Electricity sale price

All parameters use exploratory uniform marginal distributions as defined in `data/stage5_uncertainty_spec.json`.

The initial simulation assumes independent economic draws for diagnostic purposes. This independence is not an empirical claim.

## 3. Structural Contexts

The simulation evaluates 12 separate structural scenarios:

- Three engineering generation cases
- Two construction timing cases
- Two replacement-cost assumptions

The same sampled economic inputs are reused across all contexts.

Structural contexts are not assigned probability weights.

## 4. Economic Model

The simulation calls the existing `calculate_lifecycle()` function.

The lifecycle model includes staged construction expenditure, engineering-constrained electricity generation, routine operating costs, major component replacements and discounted project cash flows.

The primary model outputs are:

1. Lifecycle break-even electricity price (EUR_2024/MWh)
2. Project NPV (EUR_2024)

The output also records derived net electrical power and finite-life capacity factor.

## 5. Reproducibility

Random numbers are generated with NumPy's PCG64 algorithm.

The simulation records:

- Random seed
- Sample size
- Input parameters
- Structural context
- Dependency and marginal-distribution design
- Python and library versions
- Input and script hashes
- Output hashes

The initial analysis uses the accepted master seed `20261105`.

## 6. Validation

The pilot validation checks:

- Expected simulation counts
- Correct structural coverage
- Valid parameter bounds
- Common random numbers across contexts
- Finite economic outputs
- Break-even electricity-price and NPV consistency
- Quantile reproducibility
- Source and output hashes

Passing checks establish implementation consistency under the tested assumptions.

## 7. Research Limitations

All sampled marginal distributions are exploratory analyst assumptions.

The initial simulation does not establish empirically calibrated probabilities of commercial success.

Engineering configurations remain hypothetical, and uncertain economic inputs are not derived from an independently validated commercial Stellaris cost model.

The initial independent-input experiment does not represent observed correlations between construction cost, performance, financing and electricity prices.

## 8. Stage 5.3 Handover

The next stage will assess:

- Numerical convergence across sample sizes
- Reproducibility across independent master seeds
- Sampling precision of output quantiles
- Within-context input–output sensitivity
- Stability of reported risk drivers

Results that fail the accepted numerical convergence criteria must remain explicitly labeled nonconverged.

## Research Status

Stage 5.2 initial independent-uniform Monte Carlo implementation.

Full convergence certification, alternative marginal distributions, dependence sensitivity and manufacturing-learning uncertainty remain subsequent research tasks.