# Stage 1–2 Reproduction Guide

Version 0.1 — 28 October 2026

## Environment and execution

Use the repository's Python virtual environment. The existing analyses require pandas, NumPy, Matplotlib and tabulate. The latter is required by research_summary.py's Markdown table export. Use the project requirements file and review actual installed versions in the generated run summary; this guide does not invent a cross-platform lockfile.

From the project root:

```bash
source .venv/bin/activate
python src/run_stage12.py
```

The runner uses the active Python interpreter and stops at the first failed script. It refuses optimized Python execution because existing validation scripts rely on assert. It checks required files, raw SMARD file hashes, and consistency of processed FX values with original funding records before regeneration. No download script is invoked. Cached FX values are checked internally; the raw ECB rate provenance remains a separately documented limitation until those inputs are archived.

## Dependency order

1. check_dataset.py and audit_funding.py — company/source references and funding structure.
2. benchmark_funding.py and validate_financial_data.py — cumulative snapshot structure and review states.
3. validate_milestones.py and validate_partnership_evidence.py — enhancement tables and references.
4. funding_comparison.py — chart from retained normalized events; no live FX request.
5. partnership_capabilities.py — legacy primary-capability chart and derived matrix.
6. research_summary.py — summary after the matrix and snapshot data are ready.
7. electricity_market_analysis.py — retained raw data to processed prices, statistics and charts.
8. integrate_stage12.py — consolidated report, new figures and combined claim tables.

The original single-label partnership figure and the new multi-label map represent different coding systems. Do not merge their counts or silently relabel either as partnership quality.

## Results and provenance

reports/stage12_run.log records all child-script stdout/stderr. reports/stage12_run_summary.json records execution times, package/Python versions, platform, per-step exit codes, input/output SHA-256 hashes and unresolved evidence-status issues. These files are replaced on the next run; retain a reviewed version in Git when creating a project checkpoint.

passed means execution and listed consistency checks succeeded. passed_with_evidence_issues means the rebuild succeeded but pending/disputed claims or snapshot/claim status mismatches need review. failed means preflight or a script failed. A failed run can leave partially refreshed derived files; fix the cause and rerun the entire pipeline before treating the outputs as one consistent build. This runner is not transactional.

None of these statuses establishes a complete financing census, independent technical validation, legal enforceability of announcements or publication readiness.

## Source versus generated files

Authoritative inputs include original event/snapshot/source CSVs, milestone and partnership evidence tables, domain claim tables, the retained normalized funding table and raw SMARD snapshot. Generated outputs include charts, capability matrices, electricity summaries, consolidated claim tables and chapters 02/11. Change a fact in its owning source table, then regenerate. Handwritten chapters 03–10 and the central dictionary are not edited by the runner and still require editorial consistency review.

No external network retrieval is required by the invoked scripts. The optional FX and SMARD download scripts are deliberately excluded. Installing dependencies for a new environment is a separate setup action and may require network access.

A list of installed versions improves reproducibility but does not guarantee pixel-identical figures across operating systems and font/rendering versions. Recorded hashes identify this run's artifacts; they are not universal reference hashes for other machines.

## Known remaining work for the closing review

- Reconcile the earlier funding-audit prose with subsequent source checks and statuses.
- Consolidate the new field definitions into the central dictionary.
- Check README links and the narrative treatment of historical snapshots and target revisions.
- Record missing funding-history coverage and FX source archival as explicit limits rather than certifying completion.

These tasks belong to the Step 9 editorial and scope closure. The project remains a descriptive foundation for Stage 3, not a validated commercial forecast.
