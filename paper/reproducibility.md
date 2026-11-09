# Reproducibility and Computational Evidence

## 1. Scope

This document describes the computational reproduction and
verification procedures for the independent research project
*The Economics of Commercial Stellarator Fusion*.

The study uses structured input files, Python models, scenario
calculations, recorded outputs, and automated validation scripts.

Computational reproducibility and numerical consistency are
distinct from empirical validation and commercial feasibility.

## 2. Research Environment

The implementation uses Python and dependencies specified in
the repository's `requirements.txt`.

To prepare an isolated environment from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Record the Python and installed dependency versions:

```bash
python --version
python -m pip freeze
```

A clean reproduction should use a recorded Git commit and
compatible dependency versions.

## 3. Repository Organization

The primary research directories are:

| Directory | Purpose |
|---|---|
| `data/` | Structured evidence, assumptions, and scenario inputs |
| `src/` | Computational models and validation scripts |
| `tests/` | Automated unit tests |
| `reports/` | Numerical outputs, figures, and audit records |
| `research/` | Research-stage documentation and evidence reviews |
| `paper/` | Manuscript, figures, references, and editorial audits |

Not every generated report is necessarily tracked by Git.
The availability and freshness of retained outputs must be
checked before claiming complete reproduction.

## 4. Stage 1–4 Rebuild

Run from the repository root:

```bash
python src/run_stage14.py
python -m unittest discover -s tests -p 'test_*.py'
python src/check_stage14_freshness.py
```

The combined Stage 1–4 workflow includes source-based
market research, competitive evidence, engineering assumptions,
economic modeling, and reconciliation checks.

A passing execution and freshness check supports consistency
of the retained workflow. It does not independently verify
the factual accuracy of company disclosures or the validity
of the assumed reactor economics.

The Stage 1–2 closure screening retains requirements for
human source and editorial review.

## 5. Engineering and Economic Models

The engineering generation implementation is:

`src/engineering_generation.py`

The lifecycle discounted cash-flow implementation is:

`src/lifecycle_cash_flow.py`

The manufacturing learning implementation is:

`src/manufacturing_learning.py`

The reference LCOE analysis uses analyst-defined cost,
generation, operating expenditure, lifetime, and discounting
assumptions.

Important retained evidence includes:

- `reports/stage4_integrated_summary.csv`
- `reports/engineering_generation_scenarios.csv`
- `reports/lifecycle_summary.csv`
- `reports/stage44_learning_results.csv`

The reference annualized LCOE is approximately EUR 170.14/MWh,
and the LC004 lifecycle break-even price is approximately
EUR 213.42/MWh, in constant 2024 euros.

These are conditional model results rather than
company-reported project forecasts.

## 6. Stage 5 Uncertainty and Convergence

Stage 5 evaluates exploratory economic uncertainty across
predefined engineering and lifecycle contexts.

The retained convergence evidence includes:

- `reports/stage53_audit.json`
- `reports/stage53_extension_audit.json`
- `reports/stage55_integration_audit.json`

The Stage 5.3 audit reports `NONCONVERGED`, with
74 failed refinement tests.

The extension audit also reports `NONCONVERGED`,
with 17 failed refinement tests.

Stage 5.5 reports:

`COMPLETE_EXPLORATORY_CROSS_SEED_SUMMARY_NOT_CONVERGENCE_CERTIFIED`

Consequently, the numerical summaries are exploratory and
must not be described as convergence-certified estimates
or empirically calibrated probabilities of commercial success.

This section documents retained evidence. A complete Stage 5
rebuild command is not asserted here until its dependencies,
expected outputs, and clean-clone behavior are verified.

## 7. Stage 6 Commercialization Strategy Validation

Stage 6 examines four hypothetical commercialization structures:

- STR01: Integrated ownership
- STR02: Joint venture
- STR03: Technology supplier / OEM
- STR04: Hybrid ownership and supply

The applicable validation commands include:

```bash
python src/validate_strategy_mcda.py
python src/validate_strategy_value_capture.py
python src/validate_strategy_risk_allocation.py
python src/validate_strategy_robustness.py
```

The retained economic eligibility screen is:

`reports/stage65_feasibility_screen.csv`

All 60 strategy-context combinations fail at least one
applicable stakeholder or project NPV gate under the
selected assumptions.

This is a conditional screening result, not a verified
assessment of executable financing arrangements.

The MCDA component is a partial, four-criterion,
preference-dependent comparison rather than a definitive
ranking of commercialization strategies.

## 8. Manuscript Figures

The four manuscript figures are located in:

`paper/figures/`

The figure generation script is:

```bash
python src/build_stage72_figures.py
```

The figure manifest records source-file hashes:

`paper/figures/figure_manifest.json`

The figures cover:

1. Engineering-constrained capacity factors.
2. Lifecycle break-even electricity prices.
3. Monte Carlo refinement diagnostics.
4. Commercialization strategy feasibility.

Regeneration should use the recorded input reports.
Different inputs may produce different figures.

## 9. Manuscript Integrity Audit

Run:

```bash
python src/audit_stage72_manuscript.py
```

The manuscript audit checks a bounded selection of structural,
numerical, citation-reference, local-link, and figure-hash
conditions.

The retained manuscript revision passed 59 technical checks
with zero failures.

Four editorial review warnings remained, including
external reference verification and interpretive limitations.

A passing manuscript audit does not certify publication
readiness, independent source verification, or economic
bankability.

## 10. Evidence Provenance

Supporting evidence documentation is maintained in:

- `paper/references.md`
- `paper/citation_map.md`
- `paper/reference_source_inventory.md`
- `paper/stage72_results_evidence_inventory.md`
- `paper/stage72_manuscript_audit.md`

Source identifiers and file hashes establish traceability,
not automatic confirmation of external source accuracy.

The distinction between reported evidence, analyst-defined
assumptions, model outputs, and unresolved requirements
must be preserved.

## 11. Known Limitations

The study does not independently establish:

- Commercially demonstrated Stellaris power-plant performance.
- Verified construction and operating budgets.
- Empirically calibrated fusion manufacturing learning rates.
- Numerical convergence of all Monte Carlo outputs.
- Commercial success probabilities.
- Bankable financing terms or executable commercial agreements.

The lifecycle model also excludes several detailed
financing, tax, decommissioning, and hourly-market mechanisms.

These limitations apply even when the relevant Python
validation scripts complete successfully.

## 12. Reproduction Status

The previously recorded checks include:

- A clean-clone Stage 7.1 unit-test run with 160 passing tests.
- Successful Stage 6 validation scripts.
- A bounded manuscript audit with 59 passed checks.
- Figure-source hash verification.

These checks were recorded at different stages of
development and should not be represented as one fully
certified end-to-end release.

Before publication, run the complete supported workflow
from the intended release commit, capture its execution
environment and outputs, and complete human editorial review.

## 13. Research Interpretation

This repository provides an exploratory, auditable framework
for investigating commercial stellarator fusion economics.

Its results are conditional on the recorded assumptions,
source boundaries, model structures, and numerical limitations.

The project is independent research and does not constitute
a company valuation, investment recommendation, or empirical
demonstration of commercial fusion competitiveness.
