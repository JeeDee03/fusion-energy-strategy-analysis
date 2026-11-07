# Stage 5.3 — Monte Carlo Convergence and Global-Sensitivity Pilot

## Objective

Assess numerical stability of Stage 5.2's independent-uniform lifecycle Monte Carlo output and identify within-context input–output rank associations. This is **not** an empirical calibration exercise or a final Stage 5 risk estimate.

## Canonical design

- Random generator: NumPy `Generator(PCG64)`.
- Four master seeds: `20261105`–`20261108`.
- Nested prefixes per seed: 2,048; 8,192; 32,768 draws.
- Twelve engineering/construction/replacement contexts evaluated separately, without assigned context probabilities.
- Five independently sampled exploratory inputs: CAPEX, FOM, VOM, RATE, PRICE.
- Outcomes: lifecycle break-even electricity price and real pre-tax unlevered project NPV.

The Stage 5.3 analysis reads saved Stage 5.2 CSV files and their manifests. It calculates nested-prefix statistics from the largest available saved sample per seed, then checks thresholds recorded in `data/stage5_uncertainty_spec.json`.

## Convergence criteria

For both transitions, 2,048→8,192 and 8,192→32,768, assess P5/P50/P95 of both outcomes, in each seed and context. A quantile passes when its absolute change is no greater than the larger of the absolute tolerance and the relative tolerance times the prior estimate:

- Break-even price: max(€2/MWh, 1% of previous quantile magnitude).
- NPV: max(€100 million, 2% of previous quantile magnitude).
- Sample fraction with positive NPV: a 95% Wilson half-width at each higher sample size no greater than 0.01 under independent draws.

Two consecutive refinements must pass. Missing seeds/sample depths result in `INCOMPLETE`; available failed checks after complete coverage result in `NONCONVERGED`. A pass is explicitly restricted to the **independent-uniform design**; additional marginal/dependence studies occur in Stage 5.4.

## Sensitivity interpretation

Rank input variables by the absolute within-context Spearman correlation with lifecycle break-even price or project NPV. Preserve signed coefficients. These are descriptive rank associations, not causal effects, partial correlations, or variance-based global sensitivity indices. For a more defensible global sensitivity ranking, later consider variance-based indices or permutation-based methods after model runtime and input dependence are addressed.

Because the same economic draws are reused across the 12 structural contexts, report matched differences relative to `GEN002_LC004_R05`. These paired scenario contrasts improve interpretability and should not be interpreted as probability-weighted reactor outcomes.

## Reproducibility / evidence boundaries

- Simulation source files and manifests must match recorded SHA-256 hashes.
- Source specifications and scripts must not change between the saved simulations and the analysis.
- Treat exploratory input distributions as conditional analytical devices, not observed probabilities for Proxima Fusion.
- Do not report an unconditional fraction of positive NPV across structural contexts.
- Avoid claims of confirmed H1/H2/H3 from these simulations.

## Outputs

- `reports/stage53_nested_quantiles.csv`
- `reports/stage53_convergence_checks.csv`
- `reports/stage53_rank_sensitivity.csv`
- `reports/stage53_matched_context_effects.csv`
- `reports/stage53_audit.json`
- `reports/stage53_audit.md`

## Research status

Stage 5.3 complete only when the canonical simulations have been evaluated, numerical results reviewed, and convergence outcomes truthfully recorded. An `INCOMPLETE` or `NONCONVERGED` result should be preserved rather than silently suppressed. Full distribution/dependence robustness and H3 learning uncertainty remain for Stage 5.4.
