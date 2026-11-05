
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from lcoe_model import calculate_lcoe

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

REPORTS.mkdir(exist_ok=True)

# ------------------------------------------
# 1. Load existing Stage 4.2 reference case
# ------------------------------------------

cost_scenarios = pd.read_csv(
    DATA / "lcoe_scenarios_stage42.csv"
)

reference = cost_scenarios[
    cost_scenarios["scenario_id"] == "CAL002"
]

if len(reference) != 1:
    raise ValueError(
        "Expected exactly one CAL002 reference scenario"
    )

base = reference.iloc[0]

initial_capex_per_kwe = float(
    base["capex_eur_per_kwe"]
)

net_power_mwe = float(base["net_power_mwe"])

initial_capex_eur = (
    initial_capex_per_kwe
    * net_power_mwe
    * 1000
)

# ------------------------------------------
# 2. Load learning assumptions
# ------------------------------------------

learning = pd.read_csv(
    DATA / "manufacturing_learning_scenarios.csv"
)

assert learning["scenario_id"].is_unique

assert learning["assumption_class"].eq(
    "analyst_scenario"
).all()

for column in [
    "magnet_capex_share",
    "magnet_learning_rate"
]:
    learning[column] = pd.to_numeric(
        learning[column], errors="raise"
    )

assert learning[
    ["magnet_capex_share", "magnet_learning_rate"]
].notna().all().all()

assert learning["magnet_capex_share"].between(
    0, 1
).all()

assert learning["magnet_learning_rate"].between(
    0, 1, inclusive="left"
).all()

# ------------------------------------------
# 3. Learning-curve functions
# ------------------------------------------

def experience_factor(cumulative_units, learning_rate):
    """
    Remaining cost fraction after cumulative
    production learning.

    At N = 1, the factor is 1.
    At N = 2, the factor is (1 - LR).
    """
    if cumulative_units < 1:
        raise ValueError(
            "Cumulative units must be at least 1"
        )

    if not 0 <= learning_rate < 1:
        raise ValueError("Invalid learning rate")

    return (1 - learning_rate) ** (
        np.log2(cumulative_units)
    )


def learned_capex(initial_capex, share, rate, units):
    """
    Only the magnet portion experiences
    learning. Other construction costs remain
    unchanged.

    No separate plant-wide learning factor
    is applied.
    """
    magnet_fraction = share * experience_factor(
        units, rate
    )

    remaining_fraction = 1 - share

    return initial_capex * (
        remaining_fraction + magnet_fraction
    )


# ------------------------------------------
# 4. Evaluate cumulative production levels
# ------------------------------------------

production_levels = [1, 2, 4, 8, 16]

records = []

for _, scenario in learning.iterrows():

    share = float(
        scenario["magnet_capex_share"]
    )

    rate = float(
        scenario["magnet_learning_rate"]
    )

    for units in production_levels:

        capex = learned_capex(
            initial_capex_eur,
            share,
            rate,
            units
        )

        model_input = base.copy()

        model_input["capex_eur_million"] = (
            capex / 1e6
        )

        # The same tested Stage 4.1 LCOE function
        output = calculate_lcoe(model_input)

        records.append({
            "scenario_id": scenario["scenario_id"],
            "scenario_name": scenario["scenario_name"],
            "cumulative_equivalent_units": units,
            "magnet_capex_share": share,
            "magnet_learning_rate": rate,
            "magnet_cost_factor": experience_factor(
                units, rate
            ),
            "total_capex_eur_million": capex / 1e6,
            "capex_eur_per_kwe": (
                capex / (net_power_mwe * 1000)
            ),
            "lcoe_eur_per_mwh": (
                output["lcoe_eur_per_mwh"]
            )
        })

results = pd.DataFrame(records)

# ------------------------------------------
# 5. Validate learning behavior
# ------------------------------------------

assert len(results) == (
    len(learning) * len(production_levels)
)

for _, group in results.groupby("scenario_id"):
    ordered = group.sort_values(
        "cumulative_equivalent_units"
    )

    assert ordered[
        "total_capex_eur_million"
    ].is_monotonic_decreasing

    assert ordered[
        "lcoe_eur_per_mwh"
    ].is_monotonic_decreasing

# ------------------------------------------
# 6. Export results
# ------------------------------------------

output_csv = (
    REPORTS / "stage44_learning_results.csv"
)

results.to_csv(output_csv, index=False)

print("\nSTAGE 4.4 — MANUFACTURING LEARNING")
print(
    results[
        [
            "scenario_name",
            "cumulative_equivalent_units",
            "capex_eur_per_kwe",
            "lcoe_eur_per_mwh"
        ]
    ].round(2).to_string(index=False)
)

# ------------------------------------------
# 7. Plot total plant CAPEX
# ------------------------------------------

fig, ax = plt.subplots(figsize=(9, 5))

for name, group in results.groupby(
    "scenario_name", sort=False
):
    ax.plot(
        group["cumulative_equivalent_units"],
        group["total_capex_eur_million"] / 1000,
        marker="o",
        label=name
    )

ax.set_xlabel(
    "Cumulative equivalent plant-scale magnet sets"
)

ax.set_ylabel("Plant CAPEX (EUR billion)")
ax.set_title(
    "Component-Level Learning and Plant CAPEX"
)

ax.set_xscale("log", base=2)
ax.set_xticks(production_levels)
ax.set_xticklabels(production_levels)

ax.legend()
ax.grid(True, alpha=0.3)

fig.tight_layout()

fig.savefig(
    REPORTS / "stage44_capex_learning.png",
    dpi=200
)

# ------------------------------------------
# 8. Plot LCOE
# ------------------------------------------

fig2, ax2 = plt.subplots(figsize=(9, 5))

for name, group in results.groupby(
    "scenario_name", sort=False
):
    ax2.plot(
        group["cumulative_equivalent_units"],
        group["lcoe_eur_per_mwh"],
        marker="o",
        label=name
    )

ax2.set_xlabel(
    "Cumulative equivalent plant-scale magnet sets"
)

ax2.set_ylabel("Modeled LCOE (EUR/MWh)")
ax2.set_title(
    "Magnet Learning and Fusion Electricity Cost"
)

ax2.set_xscale("log", base=2)
ax2.set_xticks(production_levels)
ax2.set_xticklabels(production_levels)

ax2.legend()
ax2.grid(True, alpha=0.3)

fig2.tight_layout()

fig2.savefig(
    REPORTS / "stage44_lcoe_learning.png",
    dpi=200
)

print("\nSaved:")
print(output_csv.relative_to(ROOT))
print("reports/stage44_capex_learning.png")
print("reports/stage44_lcoe_learning.png")

print(
    "\nWARNING: Learning rates and magnet cost "
    "shares are hypothetical analyst assumptions."
)

plt.show()
