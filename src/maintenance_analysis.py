
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

REPORTS.mkdir(exist_ok=True)

# --------------------------------------------------
# 1. Load documented engineering assumptions
# --------------------------------------------------

parameters = pd.read_csv(
    DATA / "technical_parameters.csv"
)

stellaris = parameters[
    parameters["device_id"] == "PF_STELLARIS"
].copy()


def get_parameter(name, expected_unit):
    matches = stellaris[
        stellaris["parameter_name"] == name
    ]

    if len(matches) != 1:
        raise ValueError(
            f"Expected one parameter for {name}, "
            f"found {len(matches)}"
        )

    row = matches.iloc[0]

    if row["unit"] != expected_unit:
        raise ValueError(
            f"Unexpected unit for {name}: "
            f"{row['unit']}"
        )

    return float(row["value"])


interval_min = get_parameter(
    "major_maintenance_interval_min", "years"
)

interval_max = get_parameter(
    "major_maintenance_interval_max", "years"
)

duration_estimate = get_parameter(
    "major_maintenance_duration", "months"
)

duration_target = get_parameter(
    "major_maintenance_duration_target", "months"
)

full_power_years = get_parameter(
    "full_power_years_before_replacement",
    "full_power_years"
)

assert 0 < interval_min <= interval_max
assert 0 < duration_target <= duration_estimate
assert full_power_years > 0

# --------------------------------------------------
# 2. Define the two different interpretations
# --------------------------------------------------

def calendar_cycle_availability(
    interval_years,
    outage_months
):
    """
    Assumes interval_years is the total time
    between the starts of consecutive outages.
    The outage is included in that interval.
    """
    total_months = 12 * interval_years

    if np.any(outage_months >= total_months):
        raise ValueError("Outage exceeds calendar cycle")

    return 1 - outage_months / total_months


def operating_cycle_availability(
    operating_years,
    outage_months
):
    """
    Assumes continuous full-power operation
    for operating_years, followed by an outage.

    This is an illustrative simplification:
    full-power years are not necessarily
    equivalent to continuous calendar years.
    """
    operating_months = 12 * operating_years

    return operating_months / (
        operating_months + outage_months
    )


# --------------------------------------------------
# 3. Calculate scenario results
# --------------------------------------------------

scenarios = [
    {
        "scenario": "Calendar cycle - 4 years",
        "interpretation": "calendar_cycle",
        "outage_months": duration_estimate,
        "availability": calendar_cycle_availability(
            interval_min, duration_estimate
        ),
    },
    {
        "scenario": "Calendar cycle - 6 years",
        "interpretation": "calendar_cycle",
        "outage_months": duration_estimate,
        "availability": calendar_cycle_availability(
            interval_max, duration_estimate
        ),
    },
    {
        "scenario": "4 operating years - 7 months",
        "interpretation": "operating_cycle",
        "outage_months": duration_estimate,
        "availability": operating_cycle_availability(
            full_power_years, duration_estimate
        ),
    },
    {
        "scenario": "4 operating years - 5 months",
        "interpretation": "operating_cycle",
        "outage_months": duration_target,
        "availability": operating_cycle_availability(
            full_power_years, duration_target
        ),
    },
]

results = pd.DataFrame(scenarios)

results["availability_percent"] = (
    results["availability"] * 100
)

print("\nStellaris maintenance scenarios:")
print(
    results[
        ["scenario", "availability_percent"]
    ].to_string(index=False)
)

# --------------------------------------------------
# 4. Save scenario table
# --------------------------------------------------

csv_output = (
    REPORTS / "maintenance_availability_scenarios.csv"
)

results.to_csv(csv_output, index=False)

# --------------------------------------------------
# 5. Plot scenarios
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 5))

ax.barh(
    results["scenario"],
    results["availability_percent"]
)

ax.set_xlabel(
    "Major-outage availability factor (%)"
)

ax.set_title(
    "Stellaris: Maintenance Scenario Comparison"
)

ax.set_xlim(0, 100)

for i, value in enumerate(
    results["availability_percent"]
):
    ax.text(
        value + 0.5,
        i,
        f"{value:.2f}%",
        va="center"
    )

ax.invert_yaxis()

fig.tight_layout()

plot_output = (
    REPORTS / "maintenance_availability_scenarios.png"
)

fig.savefig(
    plot_output,
    dpi=200,
    bbox_inches="tight"
)

# --------------------------------------------------
# 6. Update the original report figure
# --------------------------------------------------

intervals = np.linspace(
    interval_min, interval_max, 100
)

fig2, ax2 = plt.subplots(figsize=(9, 5))

ax2.plot(
    intervals,
    calendar_cycle_availability(
        intervals, duration_estimate
    ) * 100
)

ax2.set_xlabel(
    "Calendar years between outage starts"
)

ax2.set_ylabel(
    "Major-outage availability factor (%)"
)

ax2.set_title(
    "Stellaris: Calendar-Cycle Sensitivity"
)

ax2.grid(True, alpha=0.3)

fig2.tight_layout()

fig2.savefig(
    REPORTS / "maintenance_availability.png",
    dpi=200
)

print("\nSaved:")
print(csv_output.relative_to(ROOT))
print(plot_output.relative_to(ROOT))
print("reports/maintenance_availability.png")

print(
    "\nNOTE: These are illustrative scheduled "
    "major-outage factors, not plant capacity factors."
)

plt.show()
