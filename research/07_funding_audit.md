# Step 3 — Funding Evidence Audit

Review date: 28 October 2026. Historical cutoff: 24 October 2026.

## Current review update — 28 October 2026

This section supersedes the initial-pass status statements reproduced below. The nine events and five snapshots now have a checked disclosure or external-report basis. FS003 and FS004 are **external_report_checked**, not independently audited or independently reconstructed totals. The current funding_audit.csv and claim tables reflect this update; the initial CSV is retained at references/funding_audit_initial_20261028.csv.

| Record | Current status | Basis |
|---|---|---|
| FS001 | original_source_checked | Dated S001; lower_bound source/qualifier correction applied |
| FS003 | external_report_checked | S010, Reuters via KSL; cumulative-total body paragraph |
| FS004 | external_report_checked | S011; cumulative private-investment body paragraph |

The source-access issue for S010 was resolved by using the attributed Reuters copy. Specific locators now replace the two placeholder locator notes. These changes do not establish complete funding histories, payment status, or independent financial assurance. The original instruction to leave FS003/FS004 pending is retained below only as historical process documentation and must not be reapplied.

## Initial audit record (superseded where noted)

## Findings and scope

This additive audit covers the nine recorded financing events and five historical snapshots from the supplied archive. It is not a completed census of company financing. Twelve records have disclosure-level amount support in this pass; two cumulative claims remain pending. A checked company disclosure is not an independent financial audit. Financing instrument classifications and disbursement status must not be inferred merely from a round announcement.

The nine event amounts and announcement dates were checked against their original company disclosures (source IDs S001–S009 already exist in sources.csv). The audit does not add unresearched historical rounds.

## Material correction: Proxima snapshot

S001, the dated 7 July 2026 release, reports more than EUR 650m secured funding, including EUR 95m public grants. It provides a dated basis for FS001. Recommended edits in funding_snapshots.csv: retain 650 and the reference date, set source_id to S001 and qualifier to lower_bound. Retain the mixed public/private comparison basis. Do not describe the figure as exactly EUR 650m or solely private capital. Keep S021 as a separate undated website source if needed; do not delete historical provenance.

The selected Proxima equity events add to EUR 556m (130 + 15 + 411). Their difference from 650 is EUR 94m, but this is not an exact unexplained funding gap: the cumulative statement is a lower bound, includes public grants, and the event history is incomplete. Do not subtract the EUR 95m grant disclosure from rounded totals to infer an exact equity total or invent an additional round.

## Other cumulative records

CFS: S004 supports the USD 4bn company-reported historical total. Its USD 1bn event is already part of that total. Selected events total USD 1,863m; the USD 2,137m arithmetic difference is not a single identified missing transaction.

Tokamak Energy: S005 supports the USD 335m total comprising USD 275m private and USD 60m government funding. The USD 125m round is included, not additional to the total. The historical reference date remains 20 November 2024.

Type One: the USD 200m event is supported by S002. The supplied Reuters URL for FS003 could not be retrieved in this pass. Its >USD 400m cumulative claim remains pending review; an inaccessible source does not establish that the claim is false.

Thea: the USD 20m and USD 100m events are supported by S008 and S003. The USD 130m historical cumulative claim has not been fully reverified here. Do not preserve an independent-corroboration assertion without a linked additional source and a dependency note. An arithmetic difference of USD 10m is not evidence of a particular omitted transaction. Later extensions require separate review before declaring the financing history complete.

## Applying this package

1. Copy the six CSV files from data/ into your project data/ directory. They are new audit tables; do not overwrite funding_rounds.csv, funding_snapshots.csv or sources.csv with these files.
2. Add this report at research/07_funding_audit.md.
3. Apply the FS001 source/qualifier edit above to your own snapshot table. Review the FS003/FS004 statuses against this audit; until corroboration is established, use pending_review in the original snapshot table as well. Keep previous values in Git history.
4. In research/03_market_financing_analysis.md update the Proxima table qualifier/source and replace the undated-source footnote with the dated S001 basis. In research/04_source_verification.md distinguish this fresh review from previous verification labels.
5. Regenerate the existing research summary using python src/research_summary.py after editing snapshots. The selected-round chart amounts are unaffected by the FS001 edit; no funding-round amount was changed in this audit.

The existing validator accepts pending_review and lower_bound. A pipeline passing does not close unresolved factual claims.

## Evidence model and checks

claims.csv implements the claim structure designed in Step 2. claim_sources.csv links records to existing sources with section locators and dependency notes. Pending links are contextual, not newly certified support. The audit review date is not a replacement for each source's original access date. Add a new access-history entry if source-version tracking is introduced.

This package was checked for 14 unique claim IDs, record references, source foreign keys, unique claim/source pairs, and arithmetic agreement with the archived events. These checks validate structure and calculations only.

## Completion status

Completed: structural reconciliation of selected events, nine event amount/date checks, dated Proxima correction, two additional original-source cumulative checks, and a populated claim/evidence structure.

Open: full verification of FS003 and FS004, source searches for missing historical rounds and undisclosed extensions, financing instrument details where ambiguous, and confirmation that original reports and derived tables were updated locally. Stage 3 funding enhancement remains open until those items are resolved or explicitly bounded as documented limitations. This is the first audit package, not a certification of complete funding histories.
