
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"

df = pd.read_csv(
    REPORTS / "stage43_performance_sensitivity.csv"
)

break_even = pd.read_csv(
    REPORTS / "stage43_break_even_capacity_factor.csv"
)

power = pd.read_csv(
    REPORTS / "stage43_net_power_sensitivity.csv"
)

# Three CAPEX cases x five capacity-factor cases
assert len(df) == 15

# Check unique combinations
assert not df.duplicated(
    ["scenario_id", "performance_id"]
).any()

# At fixed CAPEX, higher CF should lower LCOE
for _, group in df.groupby("capex_eur_per_kwe"):
    ordered = group.sort_values("capacity_factor")
    assert ordered["lcoe_eur_per_mwh"].is_monotonic_decreasing

# At fixed CF, higher CAPEX should raise LCOE
for _, group in df.groupby("capacity_factor"):
    ordered = group.sort_values("capex_eur_per_kwe")
    assert ordered["lcoe_eur_per_mwh"].is_monotonic_increasing

# Verify the illustrative reference case
baseline = df[
    (df["capex_eur_per_kwe"] == 8000)
    & np.isclose(df["capacity_factor"], 0.85)
]

assert len(baseline) == 1
assert np.isclose(
    baseline.iloc[0]["lcoe_eur_per_mwh"],
    124.04728934803093,
    atol=1e-6
)

# Check the break-even result for 12,000 EUR/kWe
higher_cost = break_even[
    break_even["capex_eur_per_kwe"] == 12000
]

assert len(higher_cost) == 1
assert higher_cost.iloc[0][
    "required_capacity_factor"
] > 1

# With fixed total CAPEX, higher net output lowers LCOE
power = power.sort_values("net_power_mwe")
assert power["lcoe_eur_per_mwh"].is_monotonic_decreasing

print("All Stage 4.3 validation checks passed.")
