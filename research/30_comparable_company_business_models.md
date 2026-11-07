# Comparable Company Technology and Business Models

## Research objective and review boundary

Complete a common evidence framework for Proxima Fusion, Type One Energy,
Thea Energy, Commonwealth Fusion Systems and Tokamak Energy. The review is a
selected primary-source snapshot dated 5 November 2026, not a complete industry
census or legal/technical due-diligence exercise.

Five companies are reviewed against eight identical criteria: architecture,
product/development path, customer/counterpart, revenue route, ownership and
delivery, manufacturing, maintenance, and maturity evidence. Forty cells are
retained, including four explicitly unresolved cells. Coverage completeness
is not evidence completeness or a readiness ranking.

## Commercial positioning

| Company | Reviewed characterization | Material qualification |
|---|---|---|
| Proxima | Planned stellarator plant development with an industrial/public partnership structure | Delivery roles are described; final asset ownership and monetization remain unresolved here. |
| Type One | Declared technology-provider and OEM strategy serving energy-system customers | Stated OEM scope differs from independent power production; realized fees and contract risk allocation remain unestablished. |
| Thea | Planned fusion-system commercialization through Eos/Helios development | Prospective utility engagement and design review do not establish a final commercial transaction structure. |
| CFS | Planned first-ARC owner/operator and future power sales | First-plant responsibility and reported offtake do not establish present fusion-electricity revenue or the ownership model of every subsequent plant. |
| Tokamak Energy | HTS systems/engineering route alongside fusion research and technology development | Magnet contract evidence is distinct from producing commercial fusion electricity. |

These are analyst classifications of declared strategy, not audited business
segments or realized revenue. They replace the previous Undetermined labels
in the company index and are linked to the reviewed business-profile table.

## Evidence sources and limits

The detailed source ledger is `data/competitive_sources.csv`: fourteen first-party,
scientific-design and government research sources, with URLs, locators, dates,
review scope and limitations. The forty statements and separate analyst
implications are in `data/company_comparison_claims.csv`; profiles are in
`data/company_business_profiles.csv`.

Proxima's selected company/partnership statements are:
https://www.proximafusion.com/about and
https://www.proximafusion.com/press-news/proxima-fusion-rwe-the-free-state-of-bavaria-and-max-planck-institute-for-plasma-physics-sign-agreement-to-build-the-worlds-first-commercial-fusion-power-plant-in-europe.
Its conceptual maintenance evidence retains the existing Stellaris paper,
https://doi.org/10.1016/j.fusengdes.2025.114868. A website publication-year wording
is not used to overwrite the paper's existing source-register date.

Type One's own strategy statement is at
https://typeoneenergy.com/our-strategy/; technology context is at
https://typeoneenergy.com/our-technology/. The selected TVA LOI announcement
https://typeoneenergy.com/insights-announcements/tva-type-one-energy-accelerate-fusion-commercialization-tennessee/
has a September 2026 editor update; it is not treated as an unchanged 2025
specification or a guaranteed construction/operating commitment.

Thea's design and reported review disclosures are at
https://thea.energy/press-release/thea-energy-completes-fusion-power-plant-preconceptual-design/
and
https://thea.energy/press-release/u-s-department-of-energy-certifies-thea-energys-fusion-pilot-plant-preconceptual-design/.
The latter remains a company report about an external review, not independently
re-audited plant validation or a grid-generation license in this research.

CFS sources are https://cfs.energy/technology/arc/,
https://cfs.energy/company/commercial-partners/ and
https://cfs.energy/technology/hts-magnets/. An offtake disclosure supports analysis
of a proposed revenue route; contract conditions/pricing and operating delivery
are not inferred beyond the public description.

Tokamak Energy's selected HTS sources are
https://tokamakenergy.com/2024/09/03/tokamak-energy-launches-te-magnetics-to-open-new-fields-of-performance-with-transformative-hts-technology/
and
https://tokamakenergy.com/2026/04/14/tokamak-energy-named-magnet-systems-partner-for-step-fusion-programme/.
The existing experimental ST40 evidence is separately grounded in
https://www.energy.gov/science/fes/articles/small-fusion-experiment-hits-temperatures-hotter-suns-core.
A plasma experiment, an engineering contract and commercial electricity supply
are different evidence types.

## Comparable engineering questions

The architecture/manufacturing rows distinguish non-planar stellarator magnets,
planar-array/control approaches, high-field tokamak magnets and the spherical-
tokamak/HTS research-and-supply boundary. The review does not infer cost from coil
counts, simple geometry labels or project announcements.

Maintenance is comparable only when its basis, component scope, evidence status
and operating boundary are known. Proxima and Thea have conceptual maintenance
claims in the selected sources. Comparable commercial replacement cycles remain
unestablished here for Type One, CFS and Tokamak Energy. The fourth unresolved
cell is Thea's final ownership/delivery structure. These are review gaps, not
claims that the companies lack maintenance engineering or contractual plans.

The Tokamak Energy reference device ST40 is experimental; other anchors include
commercial concepts. The output explicitly carries each reference device's role.
No experiment-to-commercial-plant comparison of net power or LCOE is made.

## Implications for H1–H3

**H1:** An architecture comparison identifies where engineering assumptions must
differ; it does not establish cost superiority. The existing LCOE/lifecycle cases
remain a Proxima-focused hypothetical framework, not five calibrated plant models.

**H2:** A technology supplier and an asset owner/operator can have different
capital commitments, revenue mechanisms and delivery obligations. That is a
model-boundary distinction, not proof of lower financing risk. Quantifying any
partner benefit requires contractual risk allocation, capital contributions,
guarantees and financing terms. Partnership counts alone remain insufficient.

**H3:** Manufacturability propositions must include conductor, structural,
assembly, control, testing and industrial-investment requirements. A simpler
component shape does not establish lower whole-plant cost or an achievable
learning rate. The existing component-learning cases remain assumptions.

## Reproducibility and shared metadata

The offline comparison script validates exactly five companies by eight criteria,
unique claims, source/company/device links, dates, evidence classifications,
limits and consistency of business labels. It generates tidy/wide CSVs, a linked
Markdown review and an audit. Integration recomputes the tables; freshness also
tracks the reviewed source files. Passing checks cannot certify source truth.

The business_model field in shared companies.csv changes only the descriptive
strategy labels; country, founding year, technology and company identity are
preserved. Funding, partnership and economic scenario values are not changed.
The old Stage 1–2 provenance record was built against the earlier company file
and must be regenerated before claiming it matches this updated source. Run its
existing offline rebuild before a final cross-stage publication review. Shared
funding-dataset validation passed here; the full Stage 1–2 rebuild was not rerun
in this environment because its tabulate dependency is unavailable.

## Pandas compatibility correction

Lifecycle indexing no longer uses set_index(..., verify_integrity=True).
Explicit missing/blank-ID checks and index.is_unique preserve duplicate protection
without the deprecated argument. Three regression tests check warning-free
indexing, duplicate rejection and missing identifiers. This change does not
alter cash-flow assumptions or formulas; no warning filter or dependency downgrade
is used to conceal the issue.

## Research status

The comparison framework and selected source coverage are complete within the
stated scope, with evidence gaps retained. No business label establishes actual
fusion-electricity sales, and no comparative technical/economic winner is declared.
Step 8 reconciles hypothesis definitions, reports, source provenance and completion
claims before the uncertainty specification is finalized.
