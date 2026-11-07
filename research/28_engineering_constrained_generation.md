# Conditional Engineering-to-Generation Scenarios

## Research purpose

Connect maintenance, other downtime, operating load and plant auxiliary demand
to net generation and LCOE. The new cases complement the original independent
CF sensitivity grid; they do not turn conceptual inputs into verified reactor
performance. The CAL002 algebraic reference remains unchanged.

The reviewed economic convention is in
[27_economic_assumptions_and_price_basis.md](27_economic_assumptions_and_price_basis.md).
Its ten parameter families and 57 bindings cover the original five economic
scenario tables. The seven new engineering cases have a separate reviewed
source file, `data/engineering_generation_cases.csv`, with explicit numerical
inputs, basis, analyst classification, source context and per-case notes.

## Time and output definitions

`gross_electric_mwe` is electrical generator output before online plant
auxiliaries, not thermal or fusion power. The assumed auxiliary fraction is
proportional to gross electrical output while online. Thus

\[
P_{net,rated}=P_{gross,rated}(1-a).
\]

Using 1250 gross MWe and 20% auxiliary demand gives an assumed 1000 net-rated
MWe. **1250 MWe and 20% are constructed analyst assumptions. They are not
published Stellaris gross output or auxiliary specifications.** The published
approximately 1000 MW peak electric value is not reclassified as either of them.
At fixed gross power, a 30% auxiliary fraction instead gives 875 net MWe.

Let `u` be other downtime as a fraction of the non-major-outage window, and `l`
be output load while online. Other downtime includes any routine/unplanned loss
represented in this simple model and excludes the separately counted major
outage. Define `q=(1-u)l`.

The exposure model assumes fusion exposure and gross electrical output scale
linearly with the same load factor. This is a deliberate first-order proxy;
actual fusion, thermal conversion, auxiliary loads and component degradation
need not be linear. No evidence of a commercial load-following capability is
inferred from this assumption.

## Two distinct maintenance bases

For a fixed calendar cycle `T` that includes its major outage `D` in years:

\[
A_{major}=1-\frac{D}{T}, \qquad CF=A_{major}q.
\]

For a component replacement threshold `F` measured in accumulated full-power
years, the non-major operating window takes `F/q` calendar years under the
linear exposure proxy. The outage follows that window:

\[
T_{cycle}=F/q+D, \qquad
A_{major}=\frac{F/q}{F/q+D}, \qquad
CF=\frac{q}{1+qD/F}.
\]

Four FPY therefore does not silently become four calendar operating years when
other losses are present. Lower operation delays the next exposure-triggered
replacement; scheduled-outage availability can increase while overall CF falls.
Months are converted using 12 equal model months per normalized year, not a
calendar maintenance schedule.

The conceptual inputs are retained from S3_006, Table 2 and Sections 2.10–2.11:
https://doi.org/10.1016/j.fusengdes.2025.114868. The paper discusses component
replacement after about four FPY, a five-month maintenance target and an early
seven-month estimate. Those are conceptual estimates, not operating records.
A six-year calendar interpretation of the broad interval remains an analyst
case. The code cross-checks technical parameter identity, units and source IDs.

## Energy and economics

\[
E_{net,annual}=P_{net,rated}\,8760\,CF.
\]

CF uses net-rated capacity as its denominator. Auxiliary demand reduces the
rating once and is not applied a second time to CF. Offline electricity
purchases, nonlinear auxiliary demand and startup loads are excluded.

The seven engineering cases reuse CAL002 fixed total overnight CAPEX of
12 billion EUR_2024 and its OPEX/lifetime/discount assumptions. Net power and CF
are replaced by the derived values. Effective EUR/kWe can therefore change;
the original 12000 EUR/kWe is not held constant when net power changes.

This isolates the value of generation performance. It does not estimate costs
of improved maintenance, reliability, larger gross generators or plant redesign.

## Conditional findings

| Case | Maintenance / loss assumption | Net MWe | Derived CF | LCOE EUR_2024/MWh |
|---|---|---:|---:|---:|
| GEN001 | Four FPY, seven months, no other losses | 1000 | 87.27% | 165.84 |
| GEN002 | Same outage; 1% other downtime, 99% online load | 1000 | 85.75% | 168.69 |
| GEN003 | Five-month outage with GEN002 other losses | 1000 | 88.93% | 162.84 |
| GEN004 | Six-year calendar cycle including seven-month outage | 1000 | 88.48% | 163.64 |
| GEN005 | Four FPY, five months, no other losses; test 95% | 1000 | 90.57% | 159.99 |
| GEN006 | Hypothetical two-month outage and lower other losses | 1000 | 95.08% | 152.63 |
| GEN007 | GEN002 with auxiliary share increased to 30% | 875 | 85.75% | 192.07 |

With four FPY and a five-month outage, the no-other-loss ceiling is
`48/53 = 90.57%`, below 95%. GEN005 intentionally tests this incompatibility.
Its unmet target is retained as a finding, not removed or counted as a software
failure. LCOE uses the derived CF, never the unmet 95% target.

GEN006 reaches the 95% target mathematically only under its explicitly more
optimistic maintenance and loss assumptions. Its two-month outage is flagged
as beyond the documented five-month maintenance target. The calculation does
not show that this regime is technically achievable or economically justified.

GEN007 shows the cost of reduced net export at fixed gross output and plant
investment. Its auxiliary penalty appears in net rating, not twice in CF.
All numerical findings remain conditional on the assumed inputs and scope.

## Verification and uncertainty handover

The new model runs in the offline pipeline, its inputs/outputs are hashed,
and integration recomputes every engineering case against current inputs.
Tests check time-basis identities, monotonic effects, auxiliary accounting,
invalid inputs, target separation, and stale/missing case outputs.

Targets satisfied do not mean commercially feasible. For later sampling, keep
scenario families and source/evidence flags together; do not combine a 95%
CF input with the unchanged five-month/four-FPY regime as if it were supported.
The original independent CF grid remains useful for algebraic sensitivities,
with its engineering compatibility unresolved outside the new cases.

## Remaining limits and Step 6

These are long-run cycle averages rather than dated annual operating schedules.
First/last partial cycles and actual outage dates affect discounted cash flow.
Step 6 must add construction timing and replacement events. If it models major
outages explicitly in annual generation, it must not apply the same outage loss
again through this long-run CF. Replacement expenditure and the costs needed
for optimistic performance remain to be estimated. Empirical plant power
balance, reliability and materials-lifetime calibration remain open.


### Implemented lifecycle handover

The Step 6 extension now places operating windows and replacement events on a
finite timeline, adds phased construction costs and evaluates dated cash flows.
See [29_construction_replacement_cash_flows.md](29_construction_replacement_cash_flows.md).
It replaces the major-outage average with explicit schedule losses; it does not
multiply both together. Source calibration, actual financing and plant feasibility
remain unresolved.
