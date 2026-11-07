# Construction, Replacement Events and Discounted Cash Flow

## Research question and scope

How do staged investment, delayed commissioning and major replacement events
change the economics of the hypothetical plant? The extension is conditional,
real, pre-tax and unlevered, with all monetary values in 2024 constant EUR.
Construction schedules and replacement costs are analyst stress assumptions,
not published Proxima budgets, financing terms or delivery forecasts.

The original annualized LCOE and Stage 4.5 DCF remain as a controlled simplified
reference. Their monetary conventions remain in
[27_economic_assumptions_and_price_basis.md](27_economic_assumptions_and_price_basis.md).
The new boundary is declared separately in `lifecycle_cash_flow_cases.json`.

## Investment and operating clock

Let C be whole construction years and N the economic operating life. The model
uses relative project time, not actual calendar dates. Price year 2024 denotes
purchasing power, not the construction year or commercial operation date.

Construction share s_j is paid at t=j, for j=0,...,C-1. Shares are nonnegative
and sum to one. COD is t=C; the first full operating-year receipt is at C+1.
For zero construction time, the single share is paid at t=0 and receipts begin
at t=1, reproducing the previous convention.

The reference phased schedule is a five-year analyst case with shares
10%, 20%, 30%, 25%, 15%. A pure two-year-delay diagnostic retains these same
spending dates, adds two zero-spend years, and moves the entire 35-year operating
window two years later. It does not add delay overhead, cost overruns or debt
interest. This isolates timing and is not a full construction-risk forecast.

## Explicit generation and replacement events

Engineering cases use the operating windows derived in Step 5. For FPY-based
replacement, the elapsed operating window is F/q, where F is the replacement
exposure and q contains other downtime and online load. Each major outage is
then placed explicitly on the operating timeline.

Annual energy is the overlap of these operating windows with each year,
multiplied by net-rated capacity, 8760 and q. **The Step 5 long-run CF is not
multiplied in again.** This avoids counting the major outage twice. Other
downtime remains an average within operating windows rather than individual
random failure dates. The existing linear exposure/load and auxiliary-power
assumptions remain conditional.

The first operating window is initially available; the last cycle may be
partial. Consequently, a finite 35-year generation average can differ from the
infinite-cycle CF in Step 5. This is an explicit horizon effect, not a mismatch.
If retirement falls exactly at the next replacement threshold, no replacement
is purchased. If an outage starts before retirement, its full assumed event
cost is paid even when its duration extends beyond retirement; there is no
residual-value credit.

Replacement expenditure is paid at exact outage start, including fractional
years. An event at operating time 4.0812 years after a five-year construction
period is discounted from project time 9.0812, not rounded to year ten. Annual
reporting buckets retain the already-discounted replacement component.

In engineering-event cases, the unchanged 200 million EUR/year fixed and
5 EUR/MWh variable OPEX are explicitly reinterpreted as routine costs excluding
separately charged major replacements. Fixed OPEX continues during major
outages; variable OPEX follows actual generation. This allocation is an analyst
boundary assumption, not an empirical disaggregation of the original placeholder.

## Discounting, NPV and break-even price

Construction investment and replacements use their declared payment times.
Operating revenue and routine OPEX use operating-year-end payments. For
constant real price p, discounted generation E_PV and discounted costs K_PV:

\[
NPV=pE_{PV}-K_{PV}, \qquad p_{BE}=K_{PV}/E_{PV}.
\]

K_PV includes staged overnight CAPEX, routine OPEX and replacement expenditure.
The zero-NPV identity at p_BE is tested independently of the configured price.
The discounted-cost/energy metric has a broader boundary than the original
CRF-based model; equality is required only in the matched special case.

No additional loan-interest or capitalized-IDC charge is added to this unlevered
DCF. The real hurdle rate discounts dated project cash flows; actual debt,
equity, tax and construction-finance structures remain outside the model.
Adding financing charges later requires reconciling their boundary with the
discount rate rather than applying an arbitrary extra multiplier.

A yearly row can contain operating cash paid at year end and replacement cash
paid earlier within the year. Its discounted cash flow is therefore the sum of
its discounted components, not necessarily raw annual cash flow divided by
(1+r)^year. The event table provides the exact timing needed to audit this.

## Six illustrative cases

All cases use the existing REV004 hypothetical constant real sale price of
200 EUR_2024/MWh. It is an analyst revenue case, not a market forecast.

| Case | Model change | NPV billion EUR_2024 | Break-even EUR_2024/MWh |
|---|---|---:|---:|
| LC001 | Original upfront/no-replacement special case | 2.591 | 170.14 |
| LC002 | Five-year construction; original constant 85% CF | -0.283 | 204.79 |
| LC003 | Five-year construction; GEN002 explicit outages; zero event-cost diagnostic | 0.091 | 198.51 |
| LC004 | LC003 with 600 million EUR/event | -0.818 | 213.42 |
| LC005 | LC003 with 1200 million EUR/event | -1.727 | 228.32 |
| LC006 | LC004 with COD two years later at unchanged spending dates | -2.158 | 241.29 |

The replacement values are 5% and 10% of the 12-billion-EUR reference CAPEX,
chosen to expose sensitivity. They are not calibrated replacement cost shares.
LC003's zero expense is a diagnostic, not a claim that replacements are free.

LC002 versus LC003 is not an isolated replacement-cost comparison: it also
changes generation from a constant 85% reference to the explicit GEN002 finite
operating schedule. Comparisons LC003/LC004/LC005 isolate replacement expense
on the same schedule; LC004/LC006 isolate delayed COD under the stated limits.
No commercial viability or hypothesis confirmation follows from these cases.

## Data and verification

`data/lifecycle_cash_flow_cases.json` is a reviewed source input. It records
case IDs, generation mode, engineering/revenue references, construction shares,
replacement expense, OPEX boundary, evidence class and explanations.

Generated outputs are lifecycle_summary.csv, lifecycle_annual_cash_flows.csv,
lifecycle_replacement_events.csv, lifecycle_audit.json/.md and a break-even
figure. The audit reconciles LC001 against the original DCF. Integration
recomputes all three numerical tables from current inputs; freshness hashes
also cover the new source and generated outputs.

Nineteen new tests check an independent high-precision staged-investment NPV,
legacy equivalence, payment timing, generation overlap, no duplicate outage
loss, no replacement at retirement, partial final outages, exact fractional
payment discounting, zero NPV at break-even, input errors and stale event costs.
Together with the previous 81 tests, the project has 100 regression tests.

## Retained research limits

Schedules, event expenses and OPEX allocation require evidence. No commercial
plant power balance, nonlinear degradation, random failure process, ramp-up,
offline electricity purchases, tax/debt structure, decommissioning or salvage
value is included. Construction expenses beyond the phased overnight budget
are omitted. The model describes conditional mechanisms, not expected investor
returns. Step 7 returns to the company/business-model comparison; uncertainty
sampling still requires defensible ranges and feasible joint scenarios.
