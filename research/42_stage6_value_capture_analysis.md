# Stage 6.2 — Business Models and Company-Level Value Capture

## Research question

How would hypothetical ownership and equipment-supply contracts allocate the economic value, capital obligations, and downside of one identical fusion power-plant project between Proxima and outside investors?

## Analytical basis

Reuse the Stage 4 engineering-constrained, pre-tax real EUR_2024 unlevered lifecycle model: GEN002, LC004, reference CAL002, and 5%-of-CAPEX replacement boundary. Evaluate three **hypothetical constant-real** electricity sale prices: EUR 120, 170, and 200 per MWh. Keep generation, initial overnight CAPEX, construction schedule, OPEX, replacements, and discount rate unchanged across strategies; only the allocation contracts differ.

The model is illustrative and **does not represent actual Proxima contractual terms, investor ownership, project financing, or published company earnings**.

## Strategies

- STR01: integrated owner (100% project participation)
- STR02: utility joint venture (35% project participation, 25% supplier production scope, 15% markup)
- STR03: external owner / OEM supply model (0% project participation, 40% production scope, 25% markup)
- STR04: one-project hybrid proxy (50% project participation, 30% production scope, 18% markup)

All percentages and additional setup/overhead assumptions are **exploratory analyst choices**. The hybrid is not yet a phased deployment model.

## Cash-flow mechanics and transfer conservation

Let `B_t` be the project's original annual net cash flow. Let `K_t` be construction CAPEX already included in `B_t`, `s` the supplier share of that pre-existing construction budget, `m` the supplier markup, `e` Proxima's ownership fraction, and `H_t` incremental company setup/overhead.

Define:

- Supplier production cost `C_t = s K_t` (carved out of the *existing* project construction cost).
- Invoice `F_t = (1+m) C_t` (paid at construction-spend dates).
- Residual owner cash flow `O_t = B_t + C_t - F_t`.
- Supplier net cash `S_t = F_t - C_t`.
- Company cash `P_t = e O_t + S_t - H_t`.
- External partner cash `(1-e) O_t`.

**Reconciliation identity:** `P_t + (1-e)O_t = B_t - H_t`.

The supplier markup transfers value from the plant owner to the supplier; it does **not** create extra total project value. Genuine incremental setup/overhead reduces consolidated stakeholder value.

## Important accounting and commercial boundaries

- This is a **stylized allocation of one plant's value**, not an independent company valuation.
- The supplier production cost is *reallocated from existing baseline CAPEX*: it is **not added again**.
- All supplier invoices are paid at baseline construction-spend dates; there is no receivables delay, working capital, warranty, or performance bond.
- The assumed ownership fraction also allocates all project residual net cash flows, including capital commitments. No debt, tax, equity waterfall, different risk-adjusted discount rates, or financing fees are modeled.
- Company setup and annual overhead are incremental modeled real costs.
- Fee markup and participation percentages are hypothetical; no actual contract is implied.
- An OEM may appear profitable while the owner has negative NPV. That does **not** establish demand for the OEM's system or a bankable business model.
- STR01/STR02/STR03/STR04 company NPV **must not** be directly interpreted as a final strategy ranking, since risk, capital capacity, development pipeline, project volume, IP, and financing costs differ.
- Results still inherit Stage 4–5 exploratory economic assumptions and the unresolved strict Stage 5.3 convergence limitation.

## Validation and outputs

Run `python src/strategy_value_capture.py`, followed by `python src/validate_strategy_value_capture.py`.

Generated outputs:

- `reports/stage62_value_capture_results.csv`
- `reports/stage62_stakeholder_cash_flows.csv`
- `reports/stage62_value_capture_audit.json`

Review the three price cases, identify owner-versus-supplier transfer effects, and preserve the accounting identity.

## Stage 6.3 handover

Develop *explicit* financing, partnership, risk-bearing, and contractual scenarios. Introduce exposure to construction overruns, revenue downside, guarantees, counterparty risk, and different stakeholder return requirements. Do not imply that the Stage 6.2 percentages reflect actual Proxima terms.
