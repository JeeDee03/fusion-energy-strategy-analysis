# Stage 5.3 — Extended Convergence Review

## 1. Objective

Evaluate whether the independent-uniform Monte Carlo simulation reaches the numerical stability requirements established in the Stage 5 uncertainty specification.

The analysis investigates 12 structural contexts using four independently seeded, nested random-number streams.

## 2. Simulation Design

The sample-size sequence is:

- 2,048 draws per structural context
- 8,192 draws per structural context
- 32,768 draws per structural context
- 131,072 draws per structural context

The extended experiments comprise 6,291,456 lifecycle evaluations across four seeds and 12 contexts.

All four extended datasets passed the Stage 5.2 validation checks.

Nested-sample comparisons confirmed that the first 32,768 observations of each extended run reproduce the corresponding previously saved results.

## 3. Convergence Results

| Refinement | Passed checks | Failed checks |
|---|---:|---:|
| 2,048 → 8,192 | 279 | 57 |
| 8,192 → 32,768 | 319 | 17 |
| 32,768 → 131,072 | 336 | 0 |

The latest refinement passed all 336 predefined numerical tolerance checks.

Earlier convergence failures were concentrated in NPV P95, reflecting instability in estimates of the upper simulated NPV tail.

The new results provide evidence of substantially improved numerical stability.

## 4. Acceptance Status

**Overall audit status: NONCONVERGED**

The accepted methodology requires two consecutive refinements to satisfy all relevant convergence checks.

The 8,192 → 32,768 refinement contained 17 failures, while the 32,768 → 131,072 refinement contained none.

Consequently, the strict two-refinement requirement remains unmet.

The latest passing refinement should not be described as proof of complete convergence or empirical model validation.

## 5. Sensitivity Findings

The earlier reference-context analysis identified the following ranking of monotonic NPV associations:

1. Capital expenditure
2. Electricity sale price
3. Real discount rate
4. Fixed operating expenditure
5. Variable operating expenditure

This ranking was consistent across the four 32,768-draw seeds.

The ranking applies to the specified exploratory uncertainty ranges and the examined reference context. Its robustness under alternative marginal distributions and dependence structures has not yet been established.

## 6. Scientific Interpretation

The extended simulations support continued exploratory use of the economic model.

However, the following limitations remain:

- The strict two-refinement convergence criterion has not passed.
- The sampled economic distributions are analyst assumptions rather than empirically calibrated probabilities.
- Structural scenarios are not assigned real-world probability weights.
- Numerical sampling precision does not establish model realism.
- Results do not quantify the actual probability of Proxima Fusion's commercial success.

## 7. Decision on Additional Simulation

A further extension to 524,288 draws per context is deferred.

The incremental computational burden is substantial, and additional numerical refinement is not presently considered more informative than examining distributional and dependency assumptions.

This is a research-prioritization decision, not a relaxation of the existing convergence criteria.

## 8. Stage 5.4 Handover

Stage 5.4 will evaluate:

- Alternative marginal distributions
- Dependence between economic input parameters
- Engineering and financial risk interactions
- Manufacturing-learning uncertainty
- Robustness of the main economic sensitivity findings

The extended Stage 5.3 datasets will remain available as a reproducible independent-uniform reference.

**Research decision:** Proceed to Stage 5.4 with documented numerical limitations and without declaring formal Stage 5.3 convergence certification.