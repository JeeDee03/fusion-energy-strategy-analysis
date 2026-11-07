
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from lcoe_model import (
    calculate_lcoe,
    capital_recovery_factor
)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

REPORTS.mkdir(exist_ok=True)

# ----------------------------------------
# 1. Load existing Stage 4.2 assumptions
# ----------------------------------------

costs = pd.read_csv(
    DATA / "lcoe_scenarios_stage42.csv"
)

performance = pd.read_csv(
    DATA / "lcoe_performance_scenarios.csv"
)

assert costs["scenario_id"].is_unique
assert performance["scenario_id"].is_unique

assert costs["assumption_class"].eq(
    "analyst_scenario"
).all()

assert performance["assumption_class"].eq(
    "analyst_scenario"
).all()

required_cost_columns = [
    "capex_eur_per_kwe",
    "net_power_mwe",
    "fixed_opex_eur_million_per_year",
    "variable_opex_eur_per_mwh",
    "plant_lifetime_years",
    "real_discount_rate"
]

for col in required_cost_columns:
    costs[col] = pd.to_numeric(costs[col], errors="raise")

performance["capacity_factor"] = pd.to_numeric(
    performance["capacity_factor"], errors="raise"
)

assert costs[required_cost_columns].notna().all().all()
assert performance["capacity_factor"].notna().all()

assert performance["capacity_factor"].between(
    0, 1, inclusive="right"
).all()

assert (costs["capex_eur_per_kwe"] >= 0).all()
assert (costs["net_power_mwe"] > 0).all()

# ----------------------------------------
# 2. Build every cost-performance combination
# ----------------------------------------

grid = costs.drop(
    columns=["capacity_factor"]
).merge(
    performance[
        ["scenario_id", "capacity_factor"]
    ].rename(
        columns={"scenario_id": "performance_id"}
    ),
    how="cross"
)

# Convert EUR/kWe to EUR million
grid["capex_eur_million"] = (
    grid["capex_eur_per_kwe"]
    * grid["net_power_mwe"]
    / 1000
)

# Reuse the Stage 4.1 LCOE model
calculated = grid.apply(calculate_lcoe, axis=1)

results = pd.concat(
    [grid.reset_index(drop=True),
     calculated.reset_index(drop=True)],
    axis=1
)

results.to_csv(
    REPORTS / "stage43_performance_sensitivity.csv",
    index=False
)

# ----------------------------------------
# 3. Produce sensitivity matrix
# ----------------------------------------

matrix = results.pivot(
    index="capex_eur_per_kwe",
    columns="capacity_factor",
    values="lcoe_eur_per_mwh"
)

print("\nLCOE SENSITIVITY (2024 EUR/MWh)")
print(matrix.round(2).to_string())

fig, ax = plt.subplots(figsize=(9, 5))

image = ax.imshow(matrix.values, aspect="auto")

ax.set_xticks(range(len(matrix.columns)))
ax.set_xticklabels(
    [f"{x:.0%}" for x in matrix.columns]
)

ax.set_yticks(range(len(matrix.index)))
ax.set_yticklabels(
    [f"2024 EUR {x:,.0f}/kWe" for x in matrix.index]
)

ax.set_xlabel("Assumed net electrical capacity factor")
ax.set_ylabel("Assumed overnight CAPEX")
ax.set_title("Fusion LCOE: CAPEX and Capacity Factor")

for i in range(len(matrix.index)):
    for j in range(len(matrix.columns)):
        ax.text(
            j, i, f"{matrix.iloc[i, j]:.0f}",
            ha="center", va="center",
            color="white" if matrix.iloc[i,j] >
            matrix.values.mean() else "black"
        )

fig.colorbar(image, ax=ax, label="LCOE (2024 EUR/MWh)")

fig.tight_layout()
fig.savefig(
    REPORTS / "stage43_lcoe_heatmap.png",
    dpi=200
)

# ----------------------------------------
# 4. Calculate the break-even capacity factor
# ----------------------------------------

# Baseline: low CAPEX at 85% capacity factor.
baseline = results[
    (results["capex_eur_per_kwe"] == 8000)
    & (np.isclose(results["capacity_factor"], 0.85))
]

if len(baseline) != 1:
    raise ValueError("Expected one reference scenario")

target_lcoe = float(
    baseline.iloc[0]["lcoe_eur_per_mwh"]
)

print(f"\nReference LCOE: EUR {target_lcoe:.2f}/MWh")

break_even = []

for _, row in costs.iterrows():
    power = float(row["net_power_mwe"])
    capex = (
        float(row["capex_eur_per_kwe"])
        * power * 1000
    )
    fom = (
        float(row["fixed_opex_eur_million_per_year"])
        * 1e6
    )
    vom = float(row["variable_opex_eur_per_mwh"])
    rate = float(row["real_discount_rate"])
    life = int(row["plant_lifetime_years"])

    crf = capital_recovery_factor(rate, life)

    required_cf = (
        (capex * crf + fom)
        / (power * 8760 * (target_lcoe - vom))
    )

    break_even.append({
        "scenario_name": row["scenario_name"],
        "capex_eur_per_kwe": row["capex_eur_per_kwe"],
        "required_capacity_factor": required_cf,
        "feasible_under_cf_le_1": required_cf <= 1
    })

break_even = pd.DataFrame(break_even)

break_even.to_csv(
    REPORTS / "stage43_break_even_capacity_factor.csv",
    index=False
)

print("\nBREAK-EVEN CAPACITY FACTORS")
print(break_even.to_string(index=False))

# ----------------------------------------
# 5. Extra sensitivity: net electrical output
# ----------------------------------------

# Fixed total plant CAPEX, CF, and OPEX.
# This is separate from the EUR/kWe scenario analysis.

reference = baseline.iloc[0].copy()
power_results = []

for power in [800, 1000, 1200]:
    case = reference.copy()
    case["net_power_mwe"] = power

    output = calculate_lcoe(case)

    power_results.append({
        "net_power_mwe": power,
        "lcoe_eur_per_mwh": output["lcoe_eur_per_mwh"]
    })

power_results = pd.DataFrame(power_results)
power_results.to_csv(
    REPORTS / "stage43_net_power_sensitivity.csv",
    index=False
)

print("\nNET POWER SENSITIVITY")
print(power_results.to_string(index=False))

print("\nAll results are hypothetical sensitivity cases.")
print("They are not Proxima cost or performance forecasts.")

plt.show()
