# Stage 4.3 — Engineering Performance and LCOE Sensitivity Analysis

> Scope update — 5 November 2026: this chapter describes the original analytical layer. The current synthesis is [chapter 25](25_stage4_techno_economic_synthesis.md), with engineering generation in [28](28_engineering_constrained_generation.md), construction/replacement DCF in [29](29_construction_replacement_cash_flows.md), and current research status in [31](31_research_status_and_claims.md). Legacy omissions are not omissions of every later extension; conditional results remain uncalibrated.

## 1. Research Objective

Investigate whether higher operational performance could compensate for the potentially higher construction costs of stellarator-based fusion power plants.

**Primary hypothesis:** H1 — Technology Economics.

The analysis uses the reproducible LCOE model developed in Stage 4.1 and the provisional capital-cost scenarios established in Stage 4.2.

## 2. Methodology

The simplified annualized LCOE model is:

\[
LCOE=\frac{CAPEX \cdot CRF+FOM}{P_{\mathrm{net}}\cdot8760\cdot CF}+VOM
\]

Two dimensions are varied:

- Overnight capital intensity: EUR 8,000, EUR 12,000 and EUR 18,000/kWe.
- Net electrical capacity factor: 70%, 75%, 85%, 90% and 95%.

All other assumptions are held constant, producing 15 scenarios.

The inputs are hypothetical analyst sensitivity cases and should not be interpreted as demonstrated or predicted Stellaris performance.

## 3. Capacity-Factor Sensitivity

At an assumed capital intensity of EUR 8,000/kWe:

- A capacity factor of 75% produces LCOE of approximately EUR 139.92/MWh.
- A capacity factor of 85% produces approximately EUR 124.05/MWh.
- A capacity factor of 95% produces approximately EUR 111.52/MWh.

Higher capacity factors reduce LCOE by distributing capital recovery and fixed operating costs across greater annual electricity generation.

This finding is a mathematical consequence of the LCOE model and the selected assumptions.

## 4. Capital-Cost Compensation Analysis

Using the EUR 8,000/kWe and 85% capacity-factor case as a hypothetical reference, the target LCOE is approximately EUR 124.05/MWh.

The capacity factor required to match this target is:

- EUR 8,000/kWe: 85.0%.
- EUR 12,000/kWe: approximately 117.9%.
- EUR 18,000/kWe: approximately 167.3%.

The latter two scenarios exceed the mathematical capacity-factor limit of 100%.

Therefore, under these specific model assumptions, increasing capacity factor alone cannot fully compensate for the modeled increases in capital intensity.

This is not evidence that stellarators are inherently less competitive than tokamaks. The cost scenarios are hypothetical and are not assigned to actual competing reactor designs.

## 5. Maximum Justifiable CAPEX

The model can also calculate maximum capital expenditure compatible with a specified LCOE.

Using the same reference LCOE and other fixed assumptions:

- At 85% capacity factor: approximately EUR 8.00 billion.
- At 90% capacity factor: approximately EUR 8.61 billion.
- At 95% capacity factor: approximately EUR 9.22 billion.

The difference between the 85% and 95% cases is approximately EUR 1.22 billion.

This represents the illustrative capital-cost headroom associated with increased capacity factor, not a forecast of actual savings or investment value.

## 6. Connection to Stage 3 Engineering

The published Stellaris design discusses a target overall availability of approximately 90% and a planned major maintenance strategy.

However, plant availability and net electrical capacity factor are distinct quantities.

The Stage 3 maintenance analysis estimates only the effect of selected major planned outages. It does not include all plant downtime or operational derating.

Consequently, the capacity factors investigated here are independent analyst assumptions rather than direct predictions derived from the maintenance model.

**Engineering source:** S3_006, Lion et al. (2025), Section 2.11.

## 7. Implications for H1

The results demonstrate that operational performance can materially influence the economics of capital-intensive fusion plants.

However, the results also identify limits: sufficiently large capital-cost disadvantages cannot be overcome by capacity-factor improvements alone within the model.

H1 therefore remains conditional upon the combination of construction cost, net output, capacity factor and operational expenditure.

The hypothesis is not yet confirmed or rejected for Proxima Fusion.

## 8. Limitations

- Cost inputs are provisional analyst scenarios.
- The model assumes constant annual generation and costs.
- Overnight capital expenditure is treated as upfront spending.
- Major replacements and construction financing remain excluded.
- Capacity factors are not calibrated to a validated integrated plant reliability model.
- Net electrical output is assumed rather than demonstrated.
- Competitor-specific economics are not yet represented.
- Improving capacity factor may require additional capital or operating expenditure.

## 9. Next Research Step

Stage 4.4 will investigate FOAK-to-NOAK manufacturing learning and construction-cost reductions.

The manufacturing model should distinguish total plant CAPEX from individual subsystem costs and avoid double-counting cost improvements.

## Research Status

Stage 4.3 conditional sensitivity analysis completed. The economic effect of capacity factor and capital intensity is quantified, but Proxima's real-world commercial competitiveness remains unproven.