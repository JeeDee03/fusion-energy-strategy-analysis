# Conditional Engineering and Generation Scenarios

Status: PASS_WITH_LIMITATIONS

Cases: 7 | Targets met: 6 | Targets not met: 1

| Case | Net MWe | Derived CF | Target CF | Target met | LCOE EUR_2024/MWh | Evidence relation |
|---|---:|---:|---:|---|---:|---|
| GEN001 | 1000.0 | 87.2727% | 85.0% | True | 165.84 | conceptual_maintenance_inputs_only |
| GEN002 | 1000.0 | 85.7532% | 85.0% | True | 168.69 | conceptual_maintenance_inputs_only |
| GEN003 | 1000.0 | 88.9307% | 85.0% | True | 162.84 | conceptual_maintenance_inputs_only |
| GEN004 | 1000.0 | 88.4813% | 85.0% | True | 163.64 | analyst_calendar_interpretation |
| GEN005 | 1000.0 | 90.5660% | 95.0% | False | 159.99 | conceptual_maintenance_inputs_only |
| GEN006 | 1000.0 | 95.0803% | 95.0% | True | 152.63 | beyond_documented_duration_target |
| GEN007 | 875.0 | 85.7532% | 85.0% | True | 192.07 | conceptual_maintenance_inputs_only |

## Interpretation and limitations

Targets not met are analytical findings, not invalid data. Passing cases are conditional, not verified reactor feasibility.

- Gross power, online auxiliary fraction, other downtime and load factors are analyst assumptions, not measured Stellaris parameters.
- FPY exposure and gross electrical output are assumed to scale with the same load factor; no nonlinear fusion/thermal/electric model is supplied.
- Other downtime is conditional on the non-major-outage window; losses are not subtracted twice.
- Auxiliary power reduces net-rated output once. CF is relative to that net rating. Off-state electricity purchases are excluded.
- Outputs are long-run cycle averages, not a dated annual maintenance schedule. Step 6 must handle timing and event costs consistently.
- Total reference CAPEX and OPEX are held fixed; no engineering cost uplift or replacement event cost is added here.
- Legacy independent CF grids are retained as algebraic sensitivity cases, not asserted to satisfy these engineering scenarios.
