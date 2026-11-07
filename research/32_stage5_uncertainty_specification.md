# Stage 5 — Uncertainty Analysis Specification

Design review date: 5 November 2026. Improvement Step 9 of 9. Main Stage 5
simulation remains unimplemented; this chapter specifies and preflights it.

## 1. Research purpose and probability boundary

Investigate the robustness of conditional plant-economic findings to uncertain
inputs and modeling choices. The primary outputs will be lifecycle break-even
price and project NPV, not a company valuation or a probability that Proxima
succeeds. H1–H3 remain open; H2 still needs company-level risk/value allocation
in main Stage 6.

`data/stage5_uncertainty_spec.json` is the reviewed machine-readable design.
All proposed densities are exploratory analyst choices. An equal density across
a bounded interval is a transparent experiment, not evidence that values are
equally likely. Triangular densities with the same bounds and reference mode
will test dependence on that choice. Neither is fitted to fusion observations.
The 2024 historical electricity distribution will not be recycled as a future
PPA or lifetime merchant-revenue distribution.

## 2. Variables, support and rationale

The ten parameter families retain the economic register's original ranges and
source roles. These bounds are not confidence intervals. Literature in original
USD and historical market observations contextualize the work; they do not
calibrate the proposed real-EUR distributions.

| Parameter | Reviewed support | Pilot treatment | Basis and next evidence |
|---|---|---|---|
| Initial overnight CAPEX | 8–18 billion EUR_2024; reference 12 | Exploratory uniform, with triangular density sensitivity | Existing 8000–18000 EUR/kWe envelope mapped at fixed 1000 MWe. Obtain normalized component/FOAK costs. |
| Routine fixed OPEX | 100–300 million EUR_2024/year; reference 200 | Exploratory uniform | Existing ±50% candidate bracket. Disaggregate routine expenses and exclude separately charged replacements. |
| Routine variable OPEX | 0–10 EUR_2024/MWh; reference 5 | Exploratory uniform | Existing zero-to-double stress bracket. Zero is a mathematical endpoint, not free fuel or operation. |
| Real discount rate | 4–12%; reference 8% | Exploratory uniform | Existing hurdle-rate bracket, not measured WACC. Resolve financing/risk-allocation evidence. |
| Constant real sale price | 78.51–200 EUR_2024/MWh; reference 170 | Exploratory uniform | Mixed historical/hypothetical stress endpoints, not a forecast interval. Develop PPA/merchant capture-price cases. |
| Economic life | 25–45 years; reference 35 | Fixed at 35 in first pilot | Broader support retained for later discrete horizon sensitivity; no plant survival distribution inferred. |
| Net rated output | Legacy 800–1200 MWe envelope | Derived from each selected gross/auxiliary case | No independent power draw. Resolve rated/gross/peak and offline consumption. |
| Net CF | Legacy 70–95% algebraic envelope | Derived from maintenance/load events | The envelope is context, not an independent distribution or a truncation rule. |
| Learnable magnet share | 10–40%; reference 25% | Separate learning extension | Uncalibrated subsystem allocation; obtain cost breakdown and cost-floor evidence. |
| Component learning rate | 0–20% per doubling; reference 10% | Separate learning extension | Existing scenario envelope, not an observed fusion learning curve. |

The CAPEX mapping uses fixed **reference** power, not each context's derived
net power. Thus the higher-auxiliary case has the same sampled total overnight
CAPEX, exposing lower output at fixed investment. This is a diagnostic boundary,
not an engineering cost-scaling law or the same as holding realized EUR/kWe fixed.
All money is 2024 constant EUR by convention, real pre-tax and unlevered.

## 3. Structural contexts and feasible combinations

The first pilot has 12 separate contexts: GEN002/GEN003/GEN007 × LC004/LC006
construction timing × replacement fraction 5%/10% of sampled initial CAPEX.
No context is assigned a probability and results must not be pooled into a
weighted commercial-success distribution.

GEN002 retains seven-month major outages, 1% other downtime and 99% online load;
GEN003 uses five months with the same other losses; GEN007 raises auxiliary
fraction to 30% at fixed gross rating. FPY intervals use the declared linear
exposure/load proxy. These are mathematically admissible analyst scenarios,
not demonstrated engineering feasibility.

The LC004 five-year expenditure schedule and LC006 two-year COD delay retain
original payment shares/dates, including zero-spend delay years. Replacement
expense is derived as a fraction of each sampled initial CAPEX, not independently
sampled again. This extends the existing 600/1200-million stress anchors to other
CAPEX draws; proportional scaling is an explicit uncalibrated assumption.
Routine OPEX excludes these separate events. Debt-interest/IDC charges, taxes,
decommissioning, offline power purchases and hourly capture-price dispatch remain
excluded. Operating life starts after COD.

Net power = gross power × (1 − auxiliary fraction). Other losses/load determine
FPY operating windows. Actual annual generation is computed from interval
overlap with major outages. Do not multiply long-run CF into that generation
again. Do not independently draw both CF and the variables determining it.

GEN001 is an upper-limit diagnostic; GEN004 is a separate calendar interpretation;
GEN005 deliberately misses its 95% target; GEN006 assumes a two-month outage
beyond the documented duration target. None enters the pilot mixture. Retain
these as separately labeled deterministic/stretch analyses when useful.

Reject invalid schemas, IDs, money boundaries, nonfinite values, impossible
power/CF, inconsistent spend shares and duplicate parameter definitions. Halt
and report the offending context/input. Never silently clip, drop, resample or
reinterpret invalid inputs. This is a mathematical consistency screen, not a
claim that all interior combinations are physically realizable.

## 4. Dependence analysis

The first experiment uses independent marginal ranks as a **diagnostic**. No
evidence establishes economic independence. Mandatory comparisons retain the
same marginal supports with common-rank stresses:

| Mode | CAPEX | Fixed OPEX | Variable OPEX | Rate | Price |
|---|---|---|---|---|---|
| Independent diagnostic | Independent | Independent | Independent | Independent | Independent |
| Aligned burden | Increasing U | Increasing U | Increasing U | Increasing U | Decreasing U |
| Offsetting burden | Increasing U | Decreasing U | Decreasing U | Decreasing U | Increasing U |

These are deliberately extreme rank designs, not estimated correlations,
observed causal mechanisms or mathematical bounds on all possible tail risks.
Use common random numbers across structural contexts for matched comparisons.
Test whether conclusions survive changes in marginal density and dependence;
report design-sensitive findings as such. Do not infer correlations from the
five-company sample or funding totals.

## 5. Separate H3 learning extension

After validating the FOAK pilot, use the same initial-cost draws and vary magnet
share and component learning rate within their registered supports. Keep
N = 1, 2, 4, 8, 16 equivalent plant-scale sets as separate deployment contexts,
without probabilities. Initial CAPEX factor is

`1 − share + share × N**log2(1 − learning_rate)`.

Non-magnet CAPEX remains constant. Replacement budgets remain fractions of the
unlearned initial CAPEX; do not silently learn them again. The baseline context
is GEN002/LC004 with 5% replacements. Compare diagnostic independent share/rate
ranks with a same-rank stress. Industrial investment, redesign and cost floors
remain unresolved, so these cases are not verified NOAK economics. This extension
is specified here but not included in the 396-point preflight.

## 6. Sampling, convergence and sensitivity acceptance

Use an explicit PCG64 generator and four master seeds: 20261105–20261108. For
each seed and design/context, evaluate nested prefixes of 2048, 8192 and 32768
draws. Replicates are independent across seeds; generate input ranks once per
seed, reuse prefixes and common ranks across contexts, and archive the mapping.
The rank-transformation methods and density tests must preserve marginal supports.
This package does not implement the sampler.

Report P5/P50/P95 break-even price and NPV, plus the conditional sample fraction
with NPV > 0. Use linear quantile interpolation at index (n−1)p. Require two
consecutive size refinements to satisfy **every** seed/context/dependence mode:

- Break-even quantile change ≤ max(2 EUR/MWh, 1% × absolute previous quantile).
- NPV quantile change ≤ max(0.1 billion EUR, 2% × absolute previous quantile).
- Wilson 95% Monte Carlo interval half-width for the conditional fraction ≤ 1
  percentage point under the chosen IID design.

A Monte Carlo interval describes sampling error under the selected design. It
is not empirical confidence in commercial success, input calibration or model
completeness. If criteria fail, extend once to 131072 draws and recheck the last
two refinements; otherwise retain results explicitly marked NONCONVERGED. Check
numeric finiteness and invalid count on every run, and fail on any invalid draw.

Report within-context rank associations as descriptive sensitivity measures,
not causal coefficients. Common-rank modes have collinearity and cannot identify
separate effects. Use matched context changes to isolate structural mechanisms;
compare driver conclusions across density/dependence designs. Learning belongs
to its separate family, not an unlabeled combined FOAK/NOAK sample.

Archive design/input/script hashes, Python/package versions, seed/generator,
context, dependence mode, sample size, invalid count and output hashes. Keep
raw draws or sufficient replay information. Distribution plots must state the
exploratory conditioning, context and currency/price year.

## 7. What is executed now and what remains?

`validate_uncertainty_spec.py` validates the source-bound design and evaluates
12 contexts × (32 corners + 1 reference point) = **396 deterministic cases**.
It checks the selected range corners using the existing lifecycle model. It
neither draws random numbers nor estimates probabilities, convergence or
sensitivity rankings. Corner coverage does not prove all interior interactions
or engineering feasibility.

The reviewed source hashes prevent changed ranges/context inputs from silently
retaining an old specification. Generated outputs are `stage5_spec_audit.json`,
`.md` and `stage5_design_dry_run.csv` under `reports/`. The specification audit
joins Stage 3–4's rebuild/provenance chain, which now has 23 ordered steps.

The nine-step improvement cycle has an implemented handover, subject to a
passing rebuild and human review. Main Stage 5 simulation still needs to be
coded and validated against this contract. Main Stage 6 will compare company
strategies; Stage 7 will create final research deliverables. Empirical economic
calibration, external source review and H1–H3 confirmation remain open.
