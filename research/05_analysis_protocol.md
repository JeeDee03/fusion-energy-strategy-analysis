# Research Design and Analysis Protocol

**Project:** The Economics of Commercial Fusion: A Data-Driven Market and Strategic Analysis of Proxima Fusion

**Version:** 0.1 | **Prepared:** 28 October 2026

**Status:** Initial methodological baseline. This document specifies how evidence will be collected and evaluated; it does not certify that data collection, source verification, or hypothesis testing has been completed.

## 1. Research question and analytical sequence

How should Proxima Fusion position itself technologically, economically, and strategically to become a commercially competitive fusion energy company in Europe?

The analysis proceeds from documented market evidence to technical benchmarking, hypothetical plant economics, uncertainty analysis, and strategic comparison. Company financing, plant economics, and shareholder returns are distinct analytical levels. Capital raised is not evidence of technical success, cash remaining, or profitable electricity generation.

## 2. Scope and units of analysis

- Primary case: Proxima Fusion.
- Initial comparison sample: Type One Energy, Thea Energy, Commonwealth Fusion Systems, and Tokamak Energy.
- Company comparison: international; strategic and economic interpretation: Germany and Europe.
- Historical electricity-market baseline: Germany's applicable bidding zone and market definitions, explicitly documented with each dataset. Other countries are optional extensions.
- Future plant scenarios: 2035–2050; these are hypothetical scenarios, not forecasts of company delivery dates.
- Separate units: company, financing event, funding snapshot, partnership, development project, and technical milestone. Every observation must identify its unit.

### Case-selection rationale

The initial sample is purposive rather than statistically representative. Proxima, Type One Energy, and Thea Energy provide a stellarator-focused comparison. CFS and Tokamak Energy provide reference cases from other magnetic-confinement architectures. These broad technology classifications must be checked against technical sources in Stage 3; they do not establish equivalent maturity or project scope.

The sample supports structured case comparison, not estimates for the entire fusion industry. Additional companies may be introduced when they answer a specific research question. Record the reason and date of any expansion, and apply the same collection procedure to new cases.

## 3. Evidence cutoff and update policy

Use **24 October 2026** as the initial historical evidence cutoff, consistent with the existing market-financing chapter. This is a research-design choice, not a claim that all relevant disclosures have already been captured.

An event must have been publicly disclosed on or before the cutoff to enter this baseline. A source accessed later may corroborate it only if the historical timing can be established. An undated, changing website does not establish that a reported total was valid at the cutoff; retain its observation date and mark historical applicability as unresolved unless dated evidence is available.

Keep event dates, publication dates, financial reference dates, and access dates separate. Record each company's actual coverage interval and known gaps. Do not imply complete funding histories.

If later events materially affect the analysis, either record them in a clearly labeled subsequent-events section or advance the cutoff through a documented version change. Preserve earlier records and revised target dates rather than silently overwriting them.

## 4. Inclusion, exclusion, and measurement rules

### Financing

Include traceable disclosures of equity, debt, grants, and other financial support. Preserve instrument, recipient, currency, reporting basis, status, and relevant dates. Distinguish announced, committed, closed, and disbursed amounts when disclosed; otherwise record the status as unknown.

Separate company funding from project funding. Separate new events from cumulative snapshots. Link round extensions, investor contributions, and related announcements to a common event where appropriate. Never add snapshots to rounds or recount an investor's contribution already included in a round. A project budget, valuation, PPA value, and funding received are different quantities.

Reconcile selected rounds with cumulative disclosures only where scope, date, and financing definitions permit. An unexplained difference is not automatically an omitted round. Preserve approximate amounts, undisclosed values, and lower bounds.

### Partnerships and milestones

Include publicly documented relationships with a stated development or commercial role. Record contribution, project, status, disclosed obligations, and unresolved terms. Allow multiple capability labels for one relationship. A press announcement or MoU does not establish financing closure, delivery, or realized risk reduction.

Distinguish intended milestones from achieved results. Preserve original and revised targets. Stage 2 records the chronology and evidence; Stage 3 evaluates technical significance and comparability.

### Electricity markets

Document bidding zone, product, currency, units, interval length, timezone, daylight-saving treatment, missing intervals, and sample period. Use duration weights where interval lengths differ. Distinguish a time-weighted market price from a generation-weighted realized price. Historical prices provide context; they are not forecasts for 2035–2050 or substitutes for a future PPA price.

### Missingness

Distinguish not disclosed, not found in the documented search, not applicable, and not yet reviewed. Unknown amounts or unrecorded capabilities must not be encoded as observed zero. Use explicit status fields where CSV blanks would otherwise be ambiguous.

## 5. Evidence provenance and verification

Each material claim must link to its source, relevant page or section, publication/reference date, access date, and a verification note. Allow multiple sources for one claim and multiple claims for one source.

Use original disclosures for reported transaction terms, official institutions for public decisions and statistics, and technical publications for engineering claims. External reporting can corroborate an announcement but does not constitute audited financial verification. Distinguish claims of the parties from independently demonstrated outcomes.

Verification statuses should distinguish pending review, original source checked, externally corroborated, and disputed/unresolved. External corroboration requires an explicitly linked additional source; where that source merely repeats the original announcement, note the dependency.

For conflicting claims, first compare dates, scope, definitions, and subsequent revisions. Retain both claims and explain the selected interpretation or unresolved conflict. Do not average incompatible figures. Schema validation confirms structural consistency, not factual truth.

## 6. Hypothesis evaluation plan

### H1 — Technology economics

Evaluate the technical and financial conditions under which a hypothetical stellarator plant meets a defined electricity-cost or revenue threshold. Separate FOAK and NOAK cases.

Outputs will include LCOE, break-even sale price, NPV, and sensitivity to CAPEX, availability, net output, construction time, and financing assumptions. A plant LCOE is not a company valuation. Define currency/base year, system boundary, financing assumptions, and the service supplied before comparing technologies. Wholesale market averages do not measure the full value of firm generation.

Support is conditional if competitiveness occurs within evidence-supported input ranges. Results weaken the hypothesis if competitiveness requires poorly supported costs, availability, or financing assumptions. A claim of an advantage over another architecture additionally requires comparable technical-economic evidence; favorable stellarator scenarios alone cannot establish superiority.

### H2 — Commercialization strategy

Compare integrated development with partnership or joint-venture scenarios under consistent technical assumptions. Evaluate Proxima's own funding exposure, retained cash flows, liabilities, control, and execution responsibilities separately from total project cost.

A partnership supports the hypothesis only if the modeled allocation improves a defined outcome under explicit terms and acceptable tradeoffs. Lower company funding requirements can coexist with lower retained value. Undisclosed contract terms remain unknown or are modeled as labeled scenarios. The small observational sample cannot establish causal effects on commercialization success.

### H3 — Manufacturing scalability

Evaluate component-specific standardization and learning scenarios, including magnets where justified by evidence. Separate repeatable manufacturing costs from site-specific costs and identify any cost floor or redesign requirement.

Report the learning rates and deployment assumptions required for a material economic improvement. Define the improvement threshold before interpreting results. Literature-based or assumed learning rates are scenario inputs, not measured fusion learning curves. Do not estimate an industry learning curve from company funding totals or the five-company sample.

## 7. Stage boundaries

Stage 2 establishes market context, auditable datasets, event histories, partnership evidence, and known gaps. It does not complete technical readiness rankings, company-specific plant-cost estimates, causal partnership analysis, or strategy selection.

Stage 3 evaluates technical and business-model evidence; Stage 4 builds plant-economic models; Stage 5 evaluates uncertainty; Stage 6 compares strategies. Hypotheses may remain unresolved where evidence is insufficient.

## 8. Completion criteria for the Stage 1–2 enhancement cycle

- [ ] Research protocol, sample selection, cutoff, and hypothesis evaluation plan documented.
- [ ] Data dictionary and claim-to-source relationships implemented.
- [ ] Funding events and snapshots checked for scope, timing, and double counting; unresolved issues recorded.
- [ ] Basic project/milestone chronology recorded with planned/achieved distinctions.
- [ ] Partnership contribution and commitment matrix documented without unsupported quality scores.
- [ ] German electricity-market baseline analyzed with documented time and unit conventions.
- [ ] Figures, tables, and chapter claims consistent with the underlying datasets.
- [ ] Analysis can be reproduced from documented inputs; downloaded FX data and other required external inputs are retained where permitted.
- [ ] Remaining technical and model-input gaps assigned to later stages.

These are acceptance criteria, not a statement that the work is complete. Subsequent evidence updates should change versioned observations and results without requiring the analytical design to be rebuilt.

## 9. Revision record

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-10-28 | Initial protocol drafted from the project brief and previously reviewed Stage 1–2 outputs; no new factual source audit performed. |
