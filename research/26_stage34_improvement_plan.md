# Stage 3–4 Improvement and Stage 5 Readiness Plan

This plan follows the review of fusion-energy-strategy-analysis(8).zip.
It separates software defects, research coverage gaps, and explicitly retained
model limitations. No empirical fusion cost or performance is implied by a
successful software check. Deliverables remain in English; walkthroughs are in Turkish.

| Step | Work | Completion evidence |
|---|---|---|
| 1 | Preserve human milestone review during worksheet preparation. | Unchanged reruns preserve exact bytes; new milestones append with blank reviews; prior file is backed up on updates; changed or removed evidence stops for reconciliation. |
| 2 | Establish an ordered Stage 3–4 rebuild and input/output provenance checks. | A single offline runner records versions and hashes; all scenario IDs and inputs reconcile; changing a revenue input without rebuilding is detected; README includes Stage 3 reproduction. |
| 3 | Unify numerical validation across LCOE and DCF. | Missing, non-finite, out-of-range and inconsistent inputs fail clearly; lifetime treatment is consistent; independent reference and boundary calculations pass. |
| 4 | Build a complete economic assumption register and consistent cost basis. | Each parameter has a unit, evidence class, source or rationale, admissible range, price year, geography, FOAK/NOAK status, model mapping and limitation. Scenario values are traceable to this register. Unknown evidence remains unknown. |
| 5 | Connect engineering, power balance and generation scenarios. | Gross/net and peak/rated definitions are explicit; planned outages, other losses and derating constrain generation; a 95% case states the alternative maintenance regime it requires; joint scenarios avoid incompatible assumptions. |
| 6 | Extend project cash flow for construction and major replacements. | Construction expenditure and first revenue have explicit timing; major replacements have costs and downtime; financing and real/nominal boundaries avoid double counting; the existing simplified case remains reproducible as a special case. |
| 7 | Complete comparable company and business-model coverage. | The five companies share a common evidence matrix covering product, customer, revenue model, plant responsibility, manufacturing, maintenance, maturity and evidence gaps; no unsupported cost ranking is introduced. |
| 8 | Reconcile research claims, hypotheses and completion status. | Proposal, protocol, chapters, README and model outputs use consistent hypothesis definitions, scope and scenario labels; conditional findings are separated from empirical findings; substantive limitations remain explicit. |
| 9 | Prepare and review the Stage 5 uncertainty specification. | Variables, ranges, distribution rationale, dependencies, scenario families and feasible combinations are documented; exploratory probabilities are labelled; reproducibility, convergence and sensitivity checks are specified. |

## Step 1 implementation

`src/prepare_milestone_review.py` is replaced by an import-safe, standard-library
implementation. It retains the authoritative human review at its existing path,
`reports/milestone_review.csv`, to preserve compatibility with Stage 3 scripts.
It does not move or reclassify that file in this step.

- First run: create a blank worksheet for current milestones.
- Existing unchanged records: preserve human values, custom columns, ordering,
  and original file bytes without rewriting.
- New milestones: append blank review rows; human review remains required.
- Real worksheet updates: back up the previous bytes under `reports/backups/`
  and replace the worksheet through a temporary file.
- Changed underlying evidence or removed milestones: stop without modifying
  the worksheet. Reconcile deliberately rather than retain a stale review.
- Reject malformed schemas, duplicate or empty identifiers, and unknown company
  or source references using explicit exceptions.

Nine temporary-fixture regression tests cover these behaviors, including the
legacy numeric formatting difference between `2027` and `2027.0`.

## Retained limitations after Step 1

This change does not resolve economic calibration, stale Stage 4 outputs,
engineering feasibility, financing, or cross-company evidence coverage.
The broader provenance checks are Step 2. Human editorial review remains necessary.

## Step 2 implementation

- `run_stage34.py` executes the 17 Stage 3–4 analysis/validation scripts offline
  in dependency order, captures logs and invalidates any older success record
  before starting a new attempt. Failed attempts cannot retain a passing status.
- `stage34_provenance.py` declares input and generated-output boundaries. It
  tracks the human review as immutable input and the generated engineering-to-
  economics register as output; it also checks reviewed source alignment.
- `check_stage34_freshness.py` is read-only and rejects changed/missing inputs,
  scripts, generated artifacts or Python/dependency versions.
- `stage4_reconciliation.py` checks all rows and scenario keys of eight Stage 4
  tables against current inputs; `integrate_stage4.py` retains its original
  cross-model checks and adds these table checks.
- README includes Stage 3–4 reproduction and regression-test commands.
- Thirteen regression tests exercise stale revenue, non-reference CAPEX,
  post-first-unit learning, missing/duplicate rows, edited output, missing plots,
  changed code/review evidence, and failed rebuild handling.

The rebuild record is a local consistency record, not a signed source archive
or independent factual audit. It tracks the declared model inputs, not all
underlying external publications. Subsequent economic calibration and engineering
extensions remain necessary.

## Step 3 implementation

- `economic_validation.py` defines a common numerical contract for annual LCOE
  and project DCF, with explicit field-specific ValueError messages.
- Both model entry points enforce finite required inputs, supported ranges and
  positive whole-year lifetime without silently truncating fractional years.
- Numerical strings and integral floats are accepted; booleans, missing values,
  nonnumeric strings, NaN and infinity are rejected. Units are not guessed.
- Nonnegative CAPEX/OPEX, positive net power, 0 < CF <= 1 and nonnegative real
  discount rate remain the current model boundary. Finite zero/negative sale
  prices are valid stress tests.
- CRF uses log1p/expm1 to avoid cancellation near zero discount rate. DCF uses
  equivalent exponential discount factors to avoid positive-power overflow.
  Zero discount rate has an explicit CRF branch.
- Derived generation must remain positive; cost, revenue, cash-flow and NPV
  results must remain finite rather than exporting unusable results.
- Twenty-three tests cover invalid inputs, admissible boundaries, independent
  Decimal reference LCOE/NPV, a hand-calculated zero-rate case, near-zero rates,
  and the NPV-at-LCOE identity across alternative valid assumptions.
- The rebuild preflight requires the new shared validation module. The ordered
  pipeline remains 17 steps; existing provenance checks cover the new module.

These checks enforce mathematical admissibility within the current model. They
are not evidence of realistic commercial performance or calibrated parameter
ranges. Engineering feasibility and empirical ranges remain later steps.

## Step 4 implementation

- A reviewed ten-parameter assumption register maps to 57 active scenario
  inputs. It records units, references, reviewed ranges, rationale, dependencies,
  source roles and the next evidence needed; it is not overwritten by the
  engineering evidence-gap builder.
- A 2024 constant-EUR convention and illustrative first-unit FOAK scope are
  explicit analyst choices. Original USD literature values are not converted
  or treated as calibrated EUR inputs; repeat-unit learning is not verified NOAK.
- Existing executed ranges and unexecuted exploratory candidate ranges are
  distinguished. None is presented as a probability/confidence interval.
- A new validation step, 16 regression tests, source hashes, audit outputs and
  the integration audit check this traceability. The pipeline now has 18 steps.
- Monetary chart labels include the adopted price year. No numerical scenario
  value was changed. Full empirical economic calibration remains a research gap.

## Step 5 implementation

- Seven new analyst cases connect maintenance, other downtime, operating load,
  gross electrical power and proportional online auxiliaries to net generation
  and LCOE. Calendar and accumulated-FPY cycle definitions are explicit.
- Four-FPY exposure is converted to elapsed calendar time using a declared
  linear exposure/load proxy, not silently treated as fixed calendar years.
- CF is relative to net-rated power; auxiliaries are not deducted twice.
- A deliberately unmet 95% target is retained. A case meeting 95% under a
  hypothetical two-month outage is flagged beyond the documented duration target.
- Existing reference and independent sensitivity inputs are preserved. The
  engineering cases have a separate reviewed source CSV and audit outputs;
  their full-row recomputation is included in integration and freshness checks.
- Pipeline: 19 steps. Regression suite: 81 tests, including 20 new generation
  and safe numbering-migration tests. Commercial feasibility is not established.
- The skipped number was an editorial mistake: the assumptions chapter is
  renamed 27, while this engineering extension is chapter 28. Migration preserves
  local edits and refuses to overwrite conflicting copies.

## Step 6 implementation

- Six reviewed analyst cases introduce phased overnight CAPEX, COD, first
  receipts and replacement-event expenditure in a real pre-tax unlevered DCF.
- Engineering-event generation uses annual overlap of explicit operating
  windows, without multiplying the same major-outage loss through long-run CF.
- Replacement expense is discounted at exact outage start, including fractional
  years, and reported separately from year-end operating cash flows.
- OPEX is explicitly scoped to routine expenses excluding separately charged
  major replacements in event cases; the allocation remains an assumption.
- Construction/replacement-free LC001 reconciles to the old NPV and LCOE.
  Diagnostic cost/delay cases isolate mechanisms without claiming real budgets.
- Pipeline and integration each have 20 steps/checks. Nineteen additional tests
  bring the suite to 100. New source and all generated tables are hash-tracked.

## Step 7 implementation

- A dated primary-source snapshot covers five companies by eight criteria,
  retaining 40 cells and 14 sources. Four selected-review gaps remain explicit;
  unknowns are not interpreted as missing capability or inferior technology.
- Business profiles classify declared strategies and replace the descriptive
  Undetermined company labels. They do not assert realized electricity revenue,
  independently audited contracts or calibrated company cost comparisons.
- Source statements, evidence kinds and analyst implications remain separate.
  URLs, locators, dates, reference-device roles and limitations are retained.
- A comparison build and full-row integration reconciliation join the existing
  offline pipeline and freshness hashes. Pipeline/integration each have 21 checks.
- Deprecated pandas indexing keywords are replaced with explicit ID checks;
  no warnings are suppressed and duplicate protection remains active.
- Sixteen new tests bring the regression suite to 116 tests. A final shared
  Stage 1–2 provenance refresh is necessary because company metadata changed;
  funding and numerical scenario values remain unchanged.

## Step 8 implementation

- Proposal, protocol, README and the current Stage 4 synthesis share canonical H1–H3 definitions. `research_status.json` separates workflow implementation, conditional mechanisms, empirical calibration and future stages. All hypotheses remain open.
- The synthesis incorporates engineering generation and lifecycle DCF, with distinct legacy boundaries. Original chapters 19–24 retain their findings with explicit scope updates. Chapter 31 is the current integrated reading entry point.
- A bounded research consistency step checks canonical blocks, selected numerical anchors against CSVs and relative links. Anchors are reviewed inputs, not silently refreshed outputs. It cannot validate arbitrary prose, external source truth or publication suitability.
- Stage 1–2 now declares exact provenance sets and schema version 1. The read-only combined checker requires both complete current records, step coverage and environment matches. The combined runner rebuilds Stage 1–2 before Stage 3–4 and stops on a failure.
- Shared company metadata changes cannot be hidden by refreshing only Stage 3–4. Editorial paths are discovered after numbering migration so an old chapter filename cannot remain cached in the hash list. No financing or economic scenario values are changed; human milestone reviews are preserved.
- Pipeline: 22 Stage 3–4 steps. Twenty-one added regression tests cover stale shared inputs, missing hash/step coverage, environment/raw-snapshot changes, contradictory hypothesis status, numerical anchors, links, read-only behavior and combined-run order/failure handling. The full suite contains 137 tests.

## Step 9 implementation

- `stage5_uncertainty_spec.json` binds the ten parameter roles and reviewed supports to six source-input hashes. Five exploratory marginals are separate from 12 unweighted structural contexts; engineering net power/CF are derived, lifetime is fixed for the first pilot and learning has a separate extension.
- Existing ranges are retained with their analyst rationale and evidence gaps. Uniform and triangular densities are exploratory design alternatives; independence and common-rank dependence stresses are not empirical correlation estimates or real-world success probabilities.
- The design specifies reproducible seeds/generator, nested sample-size refinements, matched context comparisons, sensitivity interpretation, convergence thresholds and explicit nonconvergence/invalid-input behavior. No distribution is calibrated from one historical price year.
- A new preflight step checks the source-bound design and executes 396 deterministic reference/corner cases through the existing lifecycle model. It samples no random numbers, estimates no probabilities and establishes no engineering feasibility.
- Twenty-three new regression tests bring the suite to 160. Pipeline: 23 steps. Tests cover changed sources/ranges, numerical invalidity, duplicate definitions, unsupported empirical claims, derived CF, context weights, stretch cases, money boundaries, double counting, dependence maps, seeds/convergence requirements and unchanged baseline model identities.
- Chapter 32 records the complete specification. Current synthesis, status notes, README and dictionary distinguish this handover from executed Monte Carlo analysis.

## Progress

Steps 1–8 confirmed in the user's checkout: 22/22 prior steps, 137 tests and CURRENT_WITH_RESEARCH_LIMITATIONS. Step 9 is implemented and locally verified; see its integration instructions for full rebuild and test results. The nine-step improvement cycle now has an implemented technical/methodological handover, subject to the user's rebuild and human review.

Main Stage 5 simulation is still to be implemented, followed by main Stage 6 strategy comparison and Stage 7 final deliverables. Empirical economic calibration, independent factual verification and H1–H3 confirmation remain open. A successful specification preflight does not close those research gaps.
