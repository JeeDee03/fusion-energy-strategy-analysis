# Stage 5.4.3 — Manufacturing Learning Under Uncertainty

## Purpose
Investigate H3 conditionally by sampling magnet CAPEX share and magnet manufacturing learning rate while keeping the five economic draws and lifecycle model aligned with the independent-uniform Stage 5.2 baseline.

## Scope
The canonical `learning_extension` defines `GEN002`, `LC004`, and a 5% replacement cost fraction. Cumulative equivalent magnet-system production levels are 1, 2, 4, 8, and 16. Each level is a *separate hypothetical repeat-unit design*, not a sequential cash-flow simulation of a manufacturing program.

## Learning equation
For initial overnight CAPEX \(C_0\), magnet share \(s\), learning rate \(L\) per production doubling, and cumulative equivalent units \(N\):

\[
C_N=C_0\left[(1-s)+s(1-L)^{\log_2N}\right].
\]

Only the initial magnet-system portion learns. Non-magnet initial costs, fixed and variable OPEX, engineering generation, construction shares, discount rates, and electricity-price draws are unchanged. Major replacement costs remain 5% of *unlearned* initial CAPEX in each case: they are not automatically reduced by learning.

The `SHARE` and `LEARNING` marginals are exploratory independent uniforms from the accepted specification. Their ranges are **not empirical confidence intervals**. They use a distinct reproducible PCG64 stream, paired across the five production levels. The economic draws reuse Stage 5.2's original seed and sample size.

## Reproducibility and validation

```bash
python src/run_stage543_learning.py --n 2048 --seed 20261105
python src/validate_stage543_learning.py --n 2048 --seed 20261105
```

Validation requires direct, draw-level reconciliation of \(N=1\) with the saved Stage 5.2 `GEN002_LC004_R05` results. It also verifies unit levels, hashes, bounded learning inputs, monotone CAPEX and break-even price, monotone NPV, and unchanged replacement costs.

## Interpretation limitations

The analysis omits magnet factory capital expenditure, qualification and engineering development, supply-chain scale-up, learning spillovers, program-level production sequences and deployment probabilities. It must **not** be described as a validated NOAK cost forecast or as proof of commercial profitability. Improving conditional lifecycle economics with larger \(N\) is a property of the imposed learning curve, not independent evidence that the learning rate can be achieved.

## Handover

Review matched reductions in CAPEX and lifecycle break-even price and matched improvements in NPV for each production level. If the 2,048-draw pilot passes, test seed and sample-size robustness before incorporating H3 into Stage 5.5 synthesis. Keep the learning extension distinct from the 12 FOAK structural contexts and the Stage 5.4.2 dependence stress tests.
