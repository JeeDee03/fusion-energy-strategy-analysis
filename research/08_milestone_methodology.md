# Development Milestone Register — Initial Baseline

Prepared 28 October 2026. Evidence cutoff 24 October 2026.

## Purpose

Nine selected observations cover five companies. The register links financing research to later technical benchmarking. It is neither a complete project history nor a technology-readiness ranking. Statements are historical observations at statement_date, not claims that a schedule is current at the cutoff. Later statements must be added as new observations rather than overwriting earlier schedules.

## Definitions

Original columns are retained: milestone_id (unique observation ID), company_id, milestone_name, milestone_type, target_date, actual_date, status, source_id. Added columns are project_name, statement_date (date of the source statement), target_year (four-digit year only), target_period_text (original degree of precision), evidence_level, and notes.

planned means an intention stated by the company. reported_completed means the company says the event occurred; it does not mean independently verified. The evidence levels company_target and company_report preserve that distinction separately from status.

A reported completion can have a blank actual_date when the exact event day is unknown. Its statement_date establishes only that the company reported completion by that date. M007 deliberately records the announcement event itself, so actual_date can match the announcement day without inferring journal publication dates. Publication, approval, initial plasma, fusion gain, and electricity export must not be conflated.

Year-only targets stay in target_year with target_date blank. A decade-level target stays in target_period_text; no exact year is invented. Future plotting must distinguish year targets, broad periods, and dated announcements. Do not plot an inferred January 1 as an actual project date.

## Source locators

S006: final roadmap paragraphs in the June 11 2025 financing release (SMC and Alpha targets).
MS001: opening paragraphs for submission; Project Infinity paragraph for startup schedule.
MS002: opening paragraphs for vessel arrival; vacuum-vessel paragraph for operations target.
MS003: opening publication announcement; roadmap paragraph for Helios decade target.
MS004: opening paragraph reporting campaign completion.

All newly checked evidence is from project parties. Published papers and regulator records must be separately inspected before upgrading evidence status in Stage 3. Broad marketing claims about superiority or commercial viability are not adopted as findings.

## Revision history and known gaps

For a revised target, retain the existing observation and add a new milestone_id with the same company/project/event description, the later statement_date and its source. Add a supersedes_milestone_id field when a real revision is identified. None is fabricated in this baseline. No delay statistic should be calculated from this sparse sample.

Historical SMC/Alpha schedules from 2025 require later-source comparisons before being called latest. This baseline does not yet claim complete coverage of all intermediate announcements. It records no independently verified technical outcomes and supports no company ranking.

## Installation

1. The originally reviewed milestones.csv had headers only. If your file is still empty, replace it with data/milestones.csv from this package. If it already has records, merge by milestone_id instead of replacing it.
2. Append the four DATA rows from data/milestone_sources_to_append.csv to your existing data/sources.csv. Do not copy its header again and do not replace sources.csv. Reuse an existing source ID instead if you have already registered the same URL, updating milestone references accordingly. S006 is already present and must be retained.
3. Copy src/validate_milestones.py and research/08_milestone_methodology.md to the matching project directories.
4. Run python src/validate_milestones.py with the project virtual environment active.
5. Add the new field definitions and statuses to research/06_data_dictionary.md using the definitions above.

Financial claim tables remain unchanged. This initial milestone register carries source references directly; claim-level expansion can be added consistently when technical evidence is evaluated. No funding chart needs regeneration because no funding amount changed.
