# Stage 5.4.1 — Marginal Distribution Sensitivity

## Research objective

Assess how changing the **assumed shape** of five independent economic input distributions affects the FOAK lifecycle break-even price and project NPV, while preserving the 12 structural contexts, input supports, engineering model and lifecycle financial model.

## Canonical inputs and experimental design

The accepted `data/stage5_uncertainty_spec.json` remains unchanged. The baseline is the Stage 5.2 independent-uniform pilot. The alternative uses **triangular distributions on exactly the same lower/upper bounds**, with the specification's `reference` values as the *modes*. These modes are not empirically estimated most-likely outcomes.

The inputs are `CAPEX`, `FOM`, `VOM`, `RATE`, and `PRICE`. `LIFE` stays fixed; net electrical output and generation are derived from the engineering case. The 12 engineering × construction × replacement contexts remain separate, with no probability weights. Magnet learning (`SHARE` and `LEARNING`) is **not** included; it belongs to the separate H3 experiment.

For each seed, independent PCG64 uniform ranks are generated identically to Stage 5.2. The triangular alternative is computed with the inverse triangular CDF of each rank. This matched-rank design isolates differences caused by marginal distribution shape and reduces sampling noise in paired comparisons. It is not a real-world dependence estimate. Within each design the five input ranks remain independent.

## Main outputs

Per seed/context: P5, P50 and P95 of break-even price and NPV; fractions of simulated cases with positive NPV; triangular-minus-uniform quantile changes; and distributions of *paired* per-draw changes. Quantile differences and quantiles of paired differences are **not** the same statistic.

No outcomes are aggregated across structural contexts. No numerical convergence certification is implied by a single matched comparison. Stage 5.3's overall strict convergence status remains `NONCONVERGED` despite its latest refinement passing all checks.

## Reproducibility and validity

- Run `src/run_stage54_triangular.py` at a seed/sample size already archived for Stage 5.2.
- Run `src/compare_stage54_marginals.py` to verify input and lifecycle-script hashes, full matched coverage, inverse-CDF pairing and unchanged engineering context metrics.
- Preserve raw CSVs and manifests locally; commit only selected compact summaries and scripts after review.
- For final robustness claims, repeat across four seeds, preferably at a sample size that provides adequate sampling precision; do not carry across Stage 5.3 convergence status automatically.

## Interpretation

Triangular distributions emphasize assumed reference values relative to uniform distributions. Any change in economic outcomes reflects the **chosen assumption about input density**, not independent evidence of a real-world commercial outcome. Comparing the two designs is a model-uncertainty stress test, not a probabilistic prediction.

## Stage 5.4.2 handover

The next experiment will change **dependence among the economic input ranks** (independent vs aligned-burden vs offsetting-burden) while maintaining explicitly chosen marginal distributions. The H3 manufacturing learning extension will remain a separate experiment to avoid CAPEX double-counting.

**Research status:** implementation and results to be recorded after local validation; no empirical success-probability claim.
