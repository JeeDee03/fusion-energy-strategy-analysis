# Stage 6.6 — Integrated Strategic Synthesis and Stage 7 Handover

**Evidence class:** Model-derived conditional assessment, not a company recommendation or verified plant forecast.
**Status:** Draft structure; update numeric statements only from `reports/stage66_synthesis_summary.md` after running the integration.

## 1. Objective

The strategic part of the research asks what business model and contracting structure could help a stellarator technology developer commercialize a power-plant design under uncertain capital, operating and revenue conditions. Stage 6 evaluates four deliberately hypothetical alternatives: integrated ownership (`STR01`), utility joint venture (`STR02`), technology supplier/OEM (`STR03`), and hybrid/phased strategy (`STR04`). No option is asserted to represent an actual Proxima Fusion contract or adopted corporate policy.

## 2. Evidence inherited from Stages 1–5

- **Industry and market context (Stages 1–2):** selected public financing, partnership and European power-market evidence. The dataset is a structured sample, not a comprehensive census.
- **Engineering (Stage 3):** engineering-conditioned electricity production, downtime, replacement and manufacturability assumptions, rather than an unconstrained capacity factor.
- **Economics (Stage 4):** lifecycle investment, replacement and power-generation model, with break-even electricity price and discounted project NPV. Project NPV is not developer-company NPV.
- **Uncertainty (Stage 5):** exploratory Monte Carlo simulation with multiple economic input distributions and dependence stress cases. Baseline sensitivity highlights CAPEX, sale price and discount-rate exposure. Results are conditional on chosen ranges; Stage 5.3 did not satisfy its strict two-consecutive-refinement rule. Manufacturing learning in one context improved modeled economics without proving commercial NOAK viability.

## 3. Stage 6 findings

### 3.1 Defined alternatives and criteria (Stage 6.1)

The four alternatives and eight evaluation criteria were registered. C05 financing exposure overlaps some other risk criteria without separately modeled debt. C06 manufacturing opportunity, C07 execution capability, and C08 strategic control lack independently supported numeric scores. They remain qualitative/evidence gaps.

### 3.2 Company versus project economics (Stage 6.2)

The developer may receive equity cash flows, technology-supply margins and/or other contract payments depending on its role. Internal transfer payments were accounted for so consolidated stakeholder NPVs reconcile to the project NPV less incremental company costs. Supplier margin can appear positive while an external owner incurs negative NPV. This is a warning about customer viability, not a demonstrated arbitrage or a company valuation.

### 3.3 Risk allocation (Stage 6.3)

Hypothetical construction overrun, COD delay, and sale-price reductions were assigned to company versus external partners according to analyst-defined percentages. Financial losses were allocated; risk transfer was not assumed to eliminate aggregate losses. No actual financing offers, guarantee prices, warranty exposures, credit terms, or equity waterfalls were modeled.

### 3.4 Provisional MCDA (Stage 6.4)

A partial four-criterion weighted, normalized screening compared company NPV, capital-share proxy, CAPEX-overrun exposure and electricity-price exposure. The analysis is preference-dependent and omits important strategic considerations. A universal leading alternative inside this particular MCDA cannot be treated as proof of commercial superiority.

### 3.5 Economic viability gates (Stage 6.5)

The subsequent test imposes nonnegative modeled NPV requirements for the company, external plant owner when applicable, and the project. Under the latest user-shared output: **0 of 60** strategy/price/stress scenarios satisfy all three economic gates and **0 of 15** contexts has an eligible strategy. The OEM developer company gate passes all 15 tests while external project-owner and plant gates fail. This directly contradicts the inference that a favorable supplier MCDA score automatically implies a workable commercialization deal.

Under no-stress reference assumptions, jointly required electricity-price thresholds are **€217.83/MWh (STR01)**, **€219.70/MWh (STR02)**, **€230.17/MWh (STR03)**, and **€222.46/MWh (STR04)**. All lie above the directly modeled €120–200/MWh price interval: **they are extrapolations**, not viable tariffs or demand evidence. The OEM developer-company price threshold of `-inf` is a sentinel for an already-positive, price-insensitive supplier NPV; it is *not* an economically meaningful negative electricity price.

Use generated `reports/stage66_synthesis_summary.md` to confirm these numbers against the actual local files.

## 4. Assessment of research hypotheses

| Hypothesis | Assessment | Missing evidence |
|---|---|---|
| H1: operating advantages may offset stellarator complexity | Modeled trade-offs are meaningful, but no empirically verified reactor-relative advantage | Validated plant availability, construction quotations and reactor-to-reactor comparison |
| H2: partnerships and business models improve commercialization | Risk-transfer and retained-value mechanisms can be calculated; favorable contractual outcomes are not independently established | Bankable project contracts, partner willingness, guarantee terms, financing costs and customer economics |
| H3: manufacturing learning reduces competitive cost | Learning assumptions reduce modeled CAPEX and break-even price, but do not demonstrate real-world commercial viability | Magnet manufacturing cost data, facility investment, supplier scale and achieved learning rates |

## 5. Conditional strategic directions

The results support **investigating**, not declaring, strategic preferences:

1. **Supplier/OEM:** Potentially limits plant ownership exposure, but must satisfy customer/project feasibility, delivery and warranty obligations and viable margins after manufacturing investments.
2. **Utility joint venture:** May allocate construction, operating and revenue exposure to capable partners. Evaluate equity and governance terms alongside the cost of transferring risk.
3. **Integrated developer/operator:** May capture greater electricity upside while demanding substantial capital and operating expertise. Financial eligibility must be demonstrated before commitment.
4. **Phased hybrid:** May offer learning and flexibility but requires explicit multi-plant timing, transition funding, and option-value modeling; the Stage 6.2 single-project proxy is insufficient.

No modeled alternative currently passes all financial eligibility gates in the analyzed stress/price grid. Therefore **withhold a categorical best-strategy recommendation**.

## 6. Decision gates for subsequent empirical research

| Decision gate | Required evidence | Model update |
|---|---|---|
| Technical performance | Third-party demonstrated net output, maintenance and outage figures | Recalibrate engineering generation and availability |
| Capital costs and COD | Itemized EPC quotations, schedule, contingencies | Update construction and time profiles |
| Manufacturing readiness | Component costs, repeat-order experience and factory investment | Include industrial investment and empirical learning |
| Revenue security | Credible electricity offtake terms and price profiles | Replace constant price simplifications |
| Counterparty viability | Partner-specific finances, contractual prices, equity and debt availability | Evaluate stakeholder financeability jointly |
| Governance and liability | Warranty, IP, technology rights, delay penalties, indemnities | Update allocations and pending decision criteria |

## 7. Unresolved limitations and publication language

- Financial scenarios are synthetic and uncalibrated to real Stellaris economics.
- Stage 5 convergence certification remains outstanding under the original strict rule.
- Stage 6 MCDA does not cover all eight criteria or genuine market access.
- Joint thresholds beyond €200/MWh extrapolate linear toy-model relationships.
- A nonnegative model NPV is a necessary **selected-screen condition**, not a sufficient bankability test.
- Stakeholder allocation tests and bookkeeping checks do not independently verify counterparty willingness.
- Do not average structural contexts as though they have measured frequencies.
- Before publication, reconcile the updated Git baseline and perform a human source/editorial audit.

## 8. Deliverables and Stage 7 handover

Generated files: `reports/stage66_strategy_evidence_matrix.csv`, `reports/stage66_context_synthesis.csv`, `reports/stage66_synthesis_summary.md` and `reports/stage66_synthesis_audit.json`.

Stage 7 should turn these into a research article with introduction, datasets/methods, engineering-economics linkage, Stage 5 uncertainty results, strategic screening, limitations, and conditional conclusions. A presentation or dashboard can be developed only after the source and claims audit. Do not repeat a model-derived association as an observed commercial fact.
