# Stage 7.1 — Repository Reproducibility & Evidence Audit

**State:** Pending execution on the current project HEAD; this is not a publication clearance.

## Objective
Establish a traceable research-release baseline before writing a paper. Verify that the scripts, inputs, research narrative and compact outputs needed to reconstruct Stages 1–6 are version controlled; review earlier validation/audit statuses and unresolved factual evidence gaps.

## Research boundary
A passing numerical validator only certifies the programmed invariants it tests. It does not certify empirical cost assumptions, plant performance, project finance feasibility, convergence, or the correctness of external company claims.

## Required checks
1. Run `python src/audit_stage71_repository.py` to inventory critical dependencies, Git tracking and prior audit presence.
2. Review `reports/stage71_repository_audit.json`, particularly `warnings`, `required_files`, `prior_audits`, and `git.status_porcelain`. Any missing or untracked Stage 1–6 dependencies should be reconciled *before* final publication.
3. Run the existing test suite and main stage validators individually. Record exact commands, exit codes and any warnings. Do not convert warnings into passes.
4. Verify that Stage 5.3's strict two-refinement convergence requirement remains `NONCONVERGED` unless a new documented refinement actually satisfies it. Stage 5.5 multi-seed descriptive summaries do not replace convergence certification.
5. Verify Stage 6.4 is a partial four-criterion MCDA, not a comprehensive eight-criterion ranking. Stage 6.5 and 6.6 have zero jointly eligible cases in the 60 tested screens; this does not establish universal commercial impossibility.
6. Investigate missing evidence in `data/stage66_open_evidence_register.csv`; classify all major final-paper statements as documentary, modeled, assumed, or unresolved.
7. Inspect generated CSVs for units, case IDs, price basis (EUR_2024), NPV definitions and scenario scope. Avoid combining project NPV with company NPV or averaging structural contexts as if they were empirically weighted.
8. Perform a true *clean-clone* test of a new checkout and install dependencies under its own virtual environment; run supported validators and record platform/Python/dependency versions. Existing notebook/terminal success in the developer's working tree is not enough.

## Acceptance decision
Only mark Stage 7.1 `REPRODUCIBLE_RESEARCH_BASELINE_ACCEPTED` after the clean checkout rebuilds the claimed results with documented, passing commands, all critical scripts and datasets are tracked, audits are reviewed, and unresolved limitations are reflected in the publication text. Otherwise record `RELEASE_BLOCKED_OR_PARTIALLY_REPRODUCIBLE` with specific blockers and mitigations.

## Outputs
- `reports/stage71_repository_audit.json`
- `reports/stage71_file_inventory.csv`
- `research/47_stage71_reproducibility_evidence_audit.md` (this document, to be completed after actual checks)

## Next step
Stage 7.2 will author the research paper's introduction, literature review and methods using the audited research baseline, with citations and explicit separation of model assumptions from company-specific evidence.
