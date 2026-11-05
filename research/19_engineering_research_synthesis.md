# Stage 3 — Engineering and Technology Benchmarking: Research Synthesis

## 1. Research Objective

This chapter investigates how fusion reactor engineering affects the prospective commercial competitiveness of Proxima Fusion's stellarator technology.

The analysis focuses on the engineering drivers of construction costs, operating costs, electricity output, maintenance requirements, manufacturing scalability and technology-development risk.

**Primary hypotheses:** H1 and H3.

**Secondary connection:** H2, through the technical risks that partnerships may help mitigate.

## 2. Reactor Technology Comparison

The benchmarking analysis covers five fusion developers and distinguishes experimental devices, demonstrators, and commercial power-plant concepts.

| Company | Reference device | Confinement concept | Documented distinguishing characteristic | Evidence |
|---|---|---|---|---|
| Proxima Fusion | Stellaris | Quasi-isodynamic stellarator | Conceptual high-field design using 48 non-planar modular coils | S3_006, Table 2 |
| Type One Energy | Infinity Two | Optimized stellarator | Proposed 800 MW fusion power and 400 MWe grid output | S3_002, "Introducing Infinity Two" |
| Thea Energy | Helios | Quasi-axisymmetric stellarator | Proposed planar HTS magnet architecture with individually controlled shaping coils | S3_007, Abstract |
| Commonwealth Fusion Systems | ARC | High-field tokamak | Published physics-basis studies for a proposed 400 MW net-electric power plant | S3_008, June 4, 2026 announcement |
| Tokamak Energy | ST40 | Spherical tokamak | Experimental achievement of approximately 100 million °C plasma temperature | S3_009, "The Science" |

### 2.1 Stellarator and Tokamak Trade-offs

Stellarators use externally generated three-dimensional magnetic fields to confine plasma. Their configuration offers the prospect of steady-state operation without the large plasma current required in conventional tokamaks.

However, the complexity of their magnet systems introduces manufacturing and integration challenges. These challenges vary by design and should not be generalized to all stellarators.

Tokamaks benefit from a substantial experimental research heritage and can use comparatively simpler toroidal magnetic geometry, but face plasma-current control, disruption-management and operating-regime challenges.

The ARC and Infinity Two electricity-output figures are design projections, while the ST40 plasma-temperature result is an experimental achievement. They must not be interpreted as equivalent measures of reactor maturity or commercial performance.

### 2.2 Economic Relevance

The comparison identifies potential relationships between reactor architecture and:

- Magnet manufacturing CAPEX
- Structural and cryogenic system requirements
- Plasma control and auxiliary power demands
- Maintenance-related availability
- Construction complexity and technology-development risk

The available evidence does not establish which complete reactor architecture will deliver the lowest commercial LCOE.

**Key references:** S3_006, S3_002, S3_007, S3_008, S3_009.

## 3. Magnetic Systems and Manufacturing

### 3.1 Proxima Fusion — Non-Planar Modular Magnets

The Stellaris conceptual design uses 48 non-planar modular coils and high-temperature superconducting technology. The published design reports an average magnetic field of 9.0 T and a peak conductor field of 24.9 T (S3_006, Table 2).

The combination of strong magnetic fields, three-dimensional coil geometry, structural loading and cryogenic requirements creates demanding engineering conditions.

These are important potential contributors to magnet-system CAPEX, but the published field strengths and coil count are not sufficient to calculate commercial magnet manufacturing costs.

### 3.2 Alternative Magnet and Manufacturing Approaches

**Type One Energy:** Infinity Two is based on an optimized stellarator configuration using non-planar HTS magnets. Its peer-reviewed physics basis supports a proposed commercial operating point, but does not independently establish manufacturing cost competitiveness (S3_002).

**Thea Energy:** The published Helios design proposes 12 large planar encircling coils and 324 individually controlled superconducting shaping coils. The architecture aims to simplify the geometry of individual coils compared with traditional non-planar stellarator coils (S3_007, Abstract).

However, this design also introduces substantial requirements for shaping-coil integration, control, power supply systems and assembly.

**Commonwealth Fusion Systems:** ARC uses a high-field tokamak approach. Its published physics-basis program supports continued development of the commercial design, while complete plant construction and operating costs remain uncertain (S3_008).

**Tokamak Energy:** ST40 provides experimental spherical-tokamak physics evidence. Its plasma-temperature achievement does not directly quantify the manufacturing cost of a future HTS-based commercial reactor (S3_009).

### 3.3 Implications for H3 — Manufacturing Scalability

Manufacturing standardization and repeated production could reduce unit costs, but the magnitude of such reductions cannot yet be derived from the available evidence.

The number of coils is not a directly comparable manufacturing-cost metric. Coil geometry, dimensions, conductor requirements, structural supports, installation, testing and control systems all contribute to system costs.

Consequently, the Stage 4 economic model should investigate explicitly defined FOAK and NOAK scenarios without assuming that any particular magnet design has already established a commercial cost advantage.


## 4. Maintenance and Availability

The Stellaris conceptual design proposes periodic replacement of major in-vessel components using a sector-splitting remote-maintenance strategy.

The published study describes approximately four full-power years before major component replacement, a five-month maintenance target, and a provisional seven-month maintenance estimate (S3_006, Section 2.11).

The Stage 3 maintenance analysis evaluates two distinct interpretations:

1. **Calendar-cycle sensitivity:** A four-to-six-year interval between major outage starts, including a seven-month shutdown, yields approximately 85.4–90.3% major-outage availability.
2. **Operating-cycle sensitivity:** Four years of uninterrupted operation followed by seven months of maintenance yields approximately 87.3%. Achieving the five-month target increases this illustrative factor to approximately 90.6%.

Four full-power years do not necessarily correspond to four continuous calendar years. The second interpretation is therefore a simplified scenario rather than a direct prediction of the Stellaris operating schedule.

Both calculations exclude unplanned failures, routine maintenance and other operational losses.

**Implication for H1:** Steady-state plasma capability does not guarantee a high commercial plant capacity factor. Maintenance engineering, subsystem reliability and replacement strategies must be incorporated into techno-economic analysis.

**Stage 4 requirement:** Model scheduled major outages separately from other sources of downtime and avoid treating conceptual maintenance targets as demonstrated commercial performance.

## 5. Technology Maturity and Demonstration Risk

Technical milestones were reviewed by engineering domain, achievement status and evidence type.

The analysis distinguishes reported technical achievements from planned development activities, conceptual design results and administrative progress.

Different reactor projects are at different stages of development, and individual subsystem achievements do not demonstrate readiness of an integrated commercial power plant.

Milestone coverage is not interpreted as a numerical technology-readiness ranking.

## 6. Engineering-to-Economics Mapping

The main technical drivers identified are:

| Engineering driver | Economic consequence | Main uncertainty |
|---|---|---|
| HTS magnet architecture | Magnet and structural CAPEX | Manufacturing and material costs |
| Reactor configuration | Plasma performance and operating requirements | Net plant performance |
| Remote maintenance | Replacement expense and downtime | Actual duration and frequency |
| Thermal and breeding systems | Capital and operating expenditures | Integrated engineering feasibility |
| Manufacturing repeatability | FOAK-to-NOAK cost reduction | Learning rate |
| Technology maturity | Construction and development risk | Demonstration outcomes |

The engineering evidence identifies relevant model inputs but does not yet establish reliable commercial cost estimates.

## 7. Implications for the Research Hypotheses

### H1 — Technology Economics

Current evidence identifies potential operational advantages and important cost drivers of stellarators.

The hypothesis remains unresolved. Its evaluation requires a quantitative model combining construction costs, net electricity output, capacity factor, operating expenses and financing assumptions.

### H2 — Commercialization Partnerships

Engineering evidence identifies subsystems and development milestones where external technical expertise, shared development expenditure or risk allocation might matter.

Whether particular partnerships actually reduce Proxima's company-level risk and capital burden remains a separate strategic and financial question.

### H3 — Manufacturing Scalability

The engineering comparison supports investigating manufacturing complexity, coil architecture and repeated production as potential determinants of cost.

It does not establish a realized learning rate or demonstrate that stellarator costs will decline sufficiently to achieve competitiveness.

## 8. Stage 4 Handover

The techno-economic model should prioritize:

1. Net electrical output and auxiliary power definitions.
2. FOAK construction CAPEX.
3. Magnet-system cost scenarios.
4. Planned and unplanned maintenance.
5. Annual net electricity generation.
6. Plant lifetime and discount rate.
7. Manufacturing learning and NOAK scenarios.
8. Electricity-market revenue assumptions.
9. Transparent handling of missing and uncertain inputs.

## 9. Limitations

- Published conceptual designs are not demonstrated commercial power plants.
- Company-specific engineering data are unevenly available.
- Technical milestones represent selected evidence, not exhaustive historical coverage.
- Engineering cost proxies have not been calibrated to commercial cost data.
- Future plant performance must be treated as scenario-dependent.
- The engineering findings should not be interpreted as proof of H1, H2 or H3.

## 10. Research Status

Stage 3 engineering investigation synthesized.

The next phase is quantitative techno-economic modeling and scenario evaluation. Final hypotheses remain open pending those results.

## 11. Comparative Engineering Findings and Decision Relevance

The Stage 3 comparison identifies three important engineering mechanisms relevant to Proxima Fusion's commercial competitiveness.

### Finding 1 — Steady-State Operation Is a Potential Advantage, Not an Economic Result

Stellarator confinement offers a potential route to continuous plasma operation. However, the commercial value of this capability depends on integrated plant availability, auxiliary power demand, maintenance downtime, and net electrical output.

The results of Stage 3.3 demonstrate why scheduled maintenance must be distinguished from continuous plasma capability.

**Implication for H1:** The economic model must investigate whether possible operating advantages compensate for construction and maintenance costs.

### Finding 2 — Magnet Architecture Creates Different Manufacturing Trade-offs

Proxima's non-planar modular magnets and Thea's planar shaping-coil architecture represent different strategies for achieving stellarator magnetic confinement.

The available evidence identifies differences in coil geometry and design requirements, but does not establish comparative system manufacturing costs.

**Implication for H3:** Manufacturing learning and standardization should be modeled through transparent cost scenarios rather than inferred from coil counts alone.

### Finding 3 — Experimental Success and Commercial Readiness Are Different

The reference projects differ substantially in maturity and purpose.

ST40 provides experimental plasma-physics evidence, while Stellaris, Infinity Two, Helios, and ARC provide various levels of conceptual and engineering design evidence.

Experimental performance of one device cannot be directly interpreted as demonstrated commercial performance of another.

**Implication for H1 and H2:** The techno-economic and strategic models must account for unresolved technical risks and distinguish engineering validation from financing or commercialization announcements.

### Stage 4 Decision Variables

The principal model inputs to be investigated are:

- FOAK construction CAPEX
- Net rated electricity output
- Auxiliary power requirements
- Scheduled and unplanned downtime
- Major component replacement expenditure
- Magnet manufacturing costs
- Production learning and NOAK construction costs
- Project financing and investment structure

### Conclusion

Stage 3 establishes a structured engineering basis for analyzing Proxima Fusion's potential competitiveness. It identifies plausible technical advantages, cost drivers, manufacturing opportunities and development risks.

However, the existing evidence is insufficient to establish commercial superiority or to confirm the research hypotheses.

The next stage will evaluate the economic conditions under which these engineering characteristics could produce competitive electricity costs.