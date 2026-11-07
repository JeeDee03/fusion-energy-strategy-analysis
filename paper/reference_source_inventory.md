# Stage 7.2.6 — Bibliographic Source Inventory

Automatically discovered source-related CSV fields.
This inventory does not independently verify external sources.

## data/all_claim_sources.csv
Rows: 25
Source-related columns: source_id, source_dependency

- source_id: S001
- source_dependency: original

- source_id: S002
- source_dependency: original

- source_id: S003
- source_dependency: original

- source_id: S004
- source_dependency: original

- source_id: S005
- source_dependency: original

## data/claim_sources.csv
Rows: 14
Source-related columns: source_id, source_dependency

- source_id: S001
- source_dependency: original

- source_id: S002
- source_dependency: original

- source_id: S003
- source_dependency: original

- source_id: S004
- source_dependency: original

- source_id: S005
- source_dependency: original

## data/company_business_profiles.csv
Rows: 5
Source-related columns: source_ids

- source_ids: BPF01;BPF02

- source_ids: BTO02;BTO03

- source_ids: BTE01;BTE02

- source_ids: BCF01;BCF02

- source_ids: BTK01;BTK02

## data/company_comparison_claims.csv
Rows: 40
Source-related columns: reference_device_id, source_ids

- reference_device_id: PF_STELLARIS
- source_ids: BPF01;BPF03

- reference_device_id: PF_STELLARIS
- source_ids: BPF01;BPF02

- reference_device_id: PF_STELLARIS
- source_ids: BPF02

- reference_device_id: PF_STELLARIS
- source_ids: BPF01;BPF02

- reference_device_id: PF_STELLARIS
- source_ids: BPF02

## data/competitive_sources.csv
Rows: 14
Source-related columns: source_id, source_title, publisher, url, publication_date, source_kind, legacy_source_id

- source_id: BPF01
- source_title: Proxima technology and programme overview
- publisher: Proxima Fusion
- url: https://www.proximafusion.com/about
- source_kind: company_website
- legacy_source_id: S3_001

- source_id: BPF02
- source_title: Proxima partnership and project MoU
- publisher: Proxima Fusion
- url: https://www.proximafusion.com/press-news/proxima-fusion-rwe-the-free-state-of-bavaria-and-max-planck-institute-for-plasma-physics-sign-agreement-to-build-the-worlds-first-commercial-fusion-power-plant-in-europe
- publication_date: 2026-02-26
- source_kind: company_announcement

- source_id: BPF03
- source_title: Stellaris engineering design paper
- publisher: Fusion Engineering and Design
- url: https://doi.org/10.1016/j.fusengdes.2025.114868
- publication_date: 2025-05-01
- source_kind: peer_reviewed_design
- legacy_source_id: S3_006

- source_id: BTO01
- source_title: Type One technology overview
- publisher: Type One Energy
- url: https://typeoneenergy.com/our-technology/
- source_kind: company_website
- legacy_source_id: S3_002

- source_id: BTO02
- source_title: Type One commercialization strategy
- publisher: Type One Energy
- url: https://typeoneenergy.com/our-strategy/
- source_kind: company_website

## data/economic_assumptions.csv
Rows: 10
Source-related columns: reference_value, reference_scenario, reference_notes

- reference_value: 12000
- reference_scenario: CAL002
- reference_notes: NOTE_COST;NOTE_REAL

- reference_value: 1000
- reference_scenario: CAL002
- reference_notes: NOTE_ENGINEERING

- reference_value: 0.85
- reference_scenario: CAL002
- reference_notes: NOTE_ENGINEERING;NOTE_METHOD

- reference_value: 200
- reference_scenario: CAL002
- reference_notes: NOTE_METHOD;NOTE_REAL

- reference_value: 5
- reference_scenario: CAL002
- reference_notes: NOTE_METHOD;NOTE_REAL

## data/economic_input_register.csv
Rows: 11
Source-related columns: source_id


- source_id: S3_006


- source_id: S3_006

- source_id: S3_006

## data/economic_reference_notes.csv
Rows: 5
Source-related columns: source_id, url, source_role

- source_id: EC001
- url: https://doi.org/10.1016/j.apenergy.2025.126567
- source_role: context_only

- source_id: EC003
- url: https://atb.nlr.gov/electricity/2025/equations_%26_variables
- source_role: methodology_only

- source_id: S3_006
- url: https://doi.org/10.1016/j.fusengdes.2025.114868
- source_role: context_only

- source_id: ES001
- url: https://www.smard.de/en
- source_role: historical_value

- url: https://samrepo.nlr.gov/help/mtf_lcoe.html
- source_role: methodology_only

## data/electricity_prices_de_lu_2024.csv
Rows: 8784
Source-related columns: source_id

- source_id: ES001

- source_id: ES001

- source_id: ES001

- source_id: ES001

- source_id: ES001

## data/engineering_generation_cases.csv
Rows: 7
Source-related columns: source_id

- source_id: S3_006

- source_id: S3_006

- source_id: S3_006

- source_id: S3_006

- source_id: S3_006

## data/engineering_subsystems.csv
Rows: 5
Source-related columns: source_id

- source_id: S3_006

- source_id: S3_006

- source_id: S3_006

- source_id: S3_006

- source_id: S3_006

## data/funding_normalized.csv
Rows: 9
Source-related columns: source_id

- source_id: S008

- source_id: S005

- source_id: S006

- source_id: S009

- source_id: S007

## data/funding_rounds.csv
Rows: 9
Source-related columns: source_id

- source_id: S001

- source_id: S002

- source_id: S003

- source_id: S004

- source_id: S005

## data/funding_snapshots.csv
Rows: 5
Source-related columns: source_id

- source_id: S001

- source_id: S004

- source_id: S010

- source_id: S011

- source_id: S005

## data/fusion_cost_benchmarks.csv
Rows: 4
Source-related columns: reference_design, source_id

- reference_design: ARAI tokamak plant
- source_id: EC001

- reference_design: ARAI tokamak plant
- source_id: EC001

- reference_design: ARAI tokamak plant
- source_id: EC001

- reference_design: ARAI tokamak plant
- source_id: EC001

## data/milestones.csv
Rows: 9
Source-related columns: source_id

- source_id: S006

- source_id: S006

- source_id: MS001

- source_id: MS001

- source_id: MS002

## data/partnership_claim_sources.csv
Rows: 11
Source-related columns: source_id, source_dependency

- source_id: S012
- source_dependency: original

- source_id: S013
- source_dependency: original

- source_id: S013
- source_dependency: original

- source_id: S014
- source_dependency: original

- source_id: S015
- source_dependency: original

## data/partnership_evidence.csv
Rows: 11
Source-related columns: source_id, source_locator

- source_id: S012
- source_locator: Opening investment paragraphs and CEO/site discussion

- source_id: S013
- source_locator: MoU financing paragraph

- source_id: S013
- source_locator: MoU paragraph describing partner roles

- source_id: S014
- source_locator: Opening PPA and investment paragraphs

- source_id: S015
- source_locator: Opening agreement announcement

## data/reactor_designs.csv
Rows: 8
Source-related columns: source_id

- source_id: S3_001

- source_id: S3_001

- source_id: S3_002

- source_id: S3_002

- source_id: S3_003

## data/sources.csv
Rows: 40
Source-related columns: source_id, source_title, publisher, publication_date, url, source_type

- source_id: S001
- source_title: Proxima Fusion Raises EUR 411M
- publisher: Proxima Fusion
- publication_date: 2026-07-07
- url: https://www.proximafusion.com/press-news/proxima-fusion-raises-eu411-million-to-build-europes-commercial-fusion-champion
- source_type: Company Announcement

- source_id: S002
- source_title: Type One Energy Completes USD 200M Series B
- publisher: Type One Energy
- publication_date: 2026-10-06
- url: https://typeoneenergy.com/insights-announcements/type-one-energy-completes-200m-series-b-financing/
- source_type: Company Announcement

- source_id: S003
- source_title: Thea Energy Raises USD 100M Series B
- publisher: Thea Energy
- publication_date: 2026-05-27
- url: https://thea.energy/press-release/thea-energy-raises-100-million-series-b-funding-to-build-scalable-fusion-power-plants/
- source_type: Company Announcement

- source_id: S004
- source_title: CFS Raises Another USD 1 Billion
- publisher: Commonwealth Fusion Systems
- publication_date: 2026-07-30
- url: https://cfs.energy/news-and-media/commonwealth-fusion-systems-raises-another-1-billion-bringing-total-capital-raised-to-4-billion/
- source_type: Company Announcement

- source_id: S005
- source_title: Tokamak Energy Raises USD 125M
- publisher: Tokamak Energy
- publication_date: 2024-11-20
- url: https://tokamakenergy.com/2024/11/20/tokamak-energy-raises-125m-to-commercialise-transformative-fusion-and-magnet-technologies/
- source_type: Company Announcement

## data/strategic_partnerships.csv
Rows: 11
Source-related columns: source_id

- source_id: S012

- source_id: S013

- source_id: S013

- source_id: S014

- source_id: S015

## data/technical_parameters.csv
Rows: 17
Source-related columns: source_id

- source_id: S3_002

- source_id: S3_006

- source_id: S3_006

- source_id: S3_006

- source_id: S3_006

