# Stage 5.4.2 — Economic Dependence Stress Tests

## Objective
Test sensitivity of lifecycle break-even electricity price and NPV to the dependence structure between five economic inputs, holding their exploratory **uniform marginal distributions** and structural cases fixed.

## Baseline and alternatives
- `independent_diagnostic`: five independent PCG64 ranks (Stage 5.2 baseline).
- `aligned_burden_stress`: one shared rank: CAPEX, FOM, VOM and discount rate increase together while electricity sale price decreases.
- `offsetting_burden_stress`: one shared rank: CAPEX and electricity price increase together while FOM, VOM and discount rate decrease.

Signs and labels are read from `data/stage5_uncertainty_spec.json`. The same initial CAPEX rank is used within each matched draw in all three designs; all individual marginals retain their original uniform supports and distribution. This is a controlled rank-coupling diagnostic, **not** an empirically estimated joint distribution, a realistic financing model, or a mathematical bound on outcomes.

## Method
The stress engine calls the existing `calculate_lifecycle()` and `normalize_config()` functions from Stage 4. The 12 engineering/construction/replacement contexts remain separate. Each change to modeled initial CAPEX continues to determine replacement costs using the accepted replacement fraction. No parameter is clipped or resampled.

The paired audit checks input and script hashes, draw keys, the intended common rank and its signs, uniform support, structural invariants, reproducible generation, finite results, and sign consistency between NPV and revenue relative to break-even price.

Each context reports P5/P50/P95 of lifecycle break-even prices and NPVs, differences from the independent-uniform baseline, the conditional positive-NPV sample fraction and the proportion of matched draws whose NPV sign changes.

## Interpretation and caveats
The initial 2,048-draw comparison is a **pilot only**. No convergence certification follows from a passing paired audit. In particular, a Wilson confidence interval on the positive-NPV fraction requires independent draws across *draw IDs*, not independence among correlated input variables within a draw. Rank coupling may increase or decrease positive NPV depending on the joint model and cannot be interpreted as a guaranteed worst/best case. Structural cases are not probability-weighted.

## Next steps
Run the small paired pilot and inspect direction and magnitude of differences. If material and well validated, repeat with multiple master seeds and larger sample sizes; assess numerical precision before presenting firm conclusions. Keep this dependence experiment distinct from the triangular-marginal and magnet-learning experiments. Manufacturing learning is reserved for Stage 5.4.3.

**Status:** Implementation prepared; numerical findings pending local execution and review.
