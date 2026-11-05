# Partnership Evidence and Commitment Analysis

Version 0.1 — reviewed 28 October 2026; historical statements through 24 October 2026.

## Method

This register reviews the 11 selected relationships already present in strategic_partnerships.csv. It does not constitute a complete partnership census. Existing financial values, historical dates, and original classifications are preserved. No new source IDs are needed: S012–S020 already identify the reviewed disclosures.

A commitment form describes what parties announce (investment, MoU, PPA, service contract, collaboration or award). It is not an ordinal score or legal opinion. A signed contract announcement does not disclose all conditions, guarantee delivery, or establish lender acceptance. Public-sector award selection may fund research collaborators rather than unrestricted cash for the company.

Documented contributions are separated from analyst interpretations of potential mechanisms. No record establishes a measured causal reduction in company CAPEX, WACC, construction time, or execution risk.

## Selected findings

RWE reports a EUR 25m investment within Proxima's financing round and describes utility/site capabilities. It must not be counted again as a separate round. The February MoU allocates scientific leadership to IPP and engineering, procurement and construction to Proxima; Bavaria's indicated co-financing is conditional. These are historical statements; later funding releases require their own evidence.

Google's CFS disclosure combines a 200 MW PPA, increased equity participation and future offtake options. Eni's >USD 1bn offtake value describes prospective sales, not capital received. Their pricing, termination provisions and lender acceptance are not established here.

Type One's TVA announcement describes signed fabrication/service contracts. This supports a more specific description than a generic industrial announcement, but does not quantify risk reduction. UKFE's GBP 70m award to Tokamak Energy is supplier work, not an equity investment; recognized revenue and margin cannot be inferred from the award value.

Thea's digital-twin relationships include distinct NVIDIA and PPPL contributions under one announcement. The INFUSE row aggregates three award selections. Existing rows therefore represent heterogeneous relationship records, not identical units of commercial progress.

## Data dictionary extension

partnership_evidence.csv has one row per partnership_id, referencing the existing master table. company_id and partner_name preserve identity. project_scope records the project/company level; statement_date is the historical announcement date, not proof of present status. commitment_form describes reported agreement form. documented_contribution summarizes source-supported roles. legal_enforceability records that the underlying legal terms were not assessed. undisclosed_terms records unresolved items. potential_mechanism_analyst_interpretation is explicitly an interpretation. realized_benefit_evidence records lack of demonstrated outcomes in the reviewed source, not proof that no benefit exists. source_id and source_locator provide provenance; review_date and verification_status describe this review.

partnership_capability_tags.csv contains one unique (partnership_id, capability) pair per role. Categories are capital, utility_expertise, site_access, public_support, scientific_rd, offtake, manufacturing, computing_simulation and technology_supply. Definitions follow the named contribution; public_support includes institutional research support. Multiple roles per relationship are allowed. Absence of a tag means not coded from the reviewed disclosure, not evidence of absence.

partnership_claims.csv and partnership_claim_sources.csv follow the Step 2 evidence schema with CLP-prefixed claim identifiers. They are separate domain tables to avoid overwriting the existing financing claims. Financial and partnership claims can be unioned in Stage 7 after checking uniqueness. The original primary_capability chart remains a separate single-label classification; the new tags must not silently replace its counts or legend.

## Installation and use

Copy the four data files to data/ and the validation script to src/. Add this report to research/09_partnership_evidence_analysis.md. All filenames are new; preserve strategic_partnerships.csv, sources.csv, claims.csv and claim_sources.csv. Add these field definitions to the central data dictionary when consolidating documentation.

Run python src/validate_partnership_evidence.py in the active virtual environment. Expected: 11 records, 19 capability links, 11 claims. The original source and company references and classification coverage have been checked. The validation script checks structure; it does not re-read contracts or establish legal certainty.

Do not regenerate or relabel the old partnership chart as a new quality comparison. Stage 7 will use this evidence matrix and describe its selection limits alongside the visualizations. No original funding or milestone values change in this package.

## Limits and next-stage use

H2 is now linked to documented contributions, potential economic mechanisms, and explicit missing contract terms. Future strategy models must treat missing allocations, prices and liability provisions as assumptions or unknowns. This stage does not select a superior partner ecosystem or business model. Additional companies, contracts and later revisions require the same search and coding protocol.
