# Stage 4 — Integration Audit

**Status:** PASS_WITH_LIMITATIONS

**Reference:** CAL002

**Reference LCOE:** 170.14 EUR/MWh

## Reconciliation Checks

- **PASS** — Stage 4.2 reference is unique: CAL002 must occur exactly once.
- **PASS** — Stage 4.2 LCOE reconciliation: Stage 4.2 must agree with shared LCOE.
- **PASS** — Stage 4.3 reference is unique: Same CAPEX and CF as CAL002.
- **PASS** — Stage 4.3 LCOE reconciliation: Performance baseline matches CAL002.
- **PASS** — Stage 4.4 starts at baseline CAPEX: At N=1, no manufacturing learning yet.
- **PASS** — Stage 4.4 starts at baseline LCOE: At N=1, all learning cases match CAL002.
- **PASS** — Stage 4.5 break-even price equals LCOE: Only valid under common model boundaries.
- **PASS** — NPV equals zero at break-even price: NPV at LCOE should be approximately zero.
- **PASS** — Stage 4.5 NPVs reproduce: Exported values match current DCF code.

## Evidence Limitations

- Economic scenarios remain analyst assumptions.
- Reference 1000 MWe is not verified Stellaris net output.
- FOAK/NOAK CAPEX not empirically calibrated.
- No construction period or interest during construction.
- No explicit replacement or decommissioning costs.
- Performance sensitivities do not model reliability.
- Magnet learning rates and CAPEX share are hypothetical.
- 2024 German electricity prices are not forecasts.
- Annual model uses a 8760-hour normalized year; 2024 historical market data contains 8784 hours.
- H1, H2, and H3 are not empirically confirmed.

## Conclusion

Passing checks establish cross-model mathematical consistency, not commercial feasibility or independent factual verification.
