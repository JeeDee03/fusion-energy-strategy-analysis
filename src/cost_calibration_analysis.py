
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from lcoe_model import calculate_lcoe

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

REPORTS.mkdir(exist_ok=True)

# ----------------------------------------
# 1. Load and validate literature evidence
# ----------------------------------------

benchmarks = pd.read_csv(
    DATA / "fusion_cost_benchmarks.csv"
)

sources = pd.read_csv(DATA / "sources.csv")
devices = pd.read_csv(DATA / "reactor_designs.csv")

assert benchmarks["benchmark_id"].is_unique
assert benchmarks["source_id"].isin(
    sources["source_id"]
).all()

assert pd.to_numeric(
    benchmarks["value"], errors="coerce"
).notna().all()

capex_benchmarks = benchmarks[
    benchmarks["cost_metric"].isin([
        "overnight_capex_lower",
        "overnight_capex_upper"
    ])
]

assert set(capex_benchmarks["unit"]) == {
    "USD_per_kWe"
}

print("\nPUBLISHED COST BENCHMARKS")
print(
    benchmarks[
        ["reference_design", "cost_metric",
         "value", "unit", "development_basis"]
    ].to_string(index=False)
)

# ----------------------------------------
# 2. Load provisional economic scenarios
# ----------------------------------------

scenarios = pd.read_csv(
    DATA / "lcoe_scenarios_stage42.csv"
)

assert scenarios["scenario_id"].is_unique
assert scenarios["device_id"].isin(
    devices["device_id"]
).all()

assert scenarios["assumption_class"].eq(
    "analyst_scenario"
).all()

numeric_columns = [
    "capex_eur_per_kwe",
    "net_power_mwe",
    "capacity_factor",
    "fixed_opex_eur_million_per_year",
    "variable_opex_eur_per_mwh",
    "plant_lifetime_years",
    "real_discount_rate"
]

for col in numeric_columns:
    scenarios[col] = pd.to_numeric(
        scenarios[col], errors="raise"
    )

if scenarios[numeric_columns].isna().any().any():
    raise ValueError("Missing scenario inputs")

if (scenarios["capex_eur_per_kwe"] < 0).any():
    raise ValueError("CAPEX intensity cannot be negative")

# ----------------------------------------
# 3. Convert specific CAPEX to total CAPEX
# ----------------------------------------

scenarios["capex_eur_million"] = (
    scenarios["capex_eur_per_kwe"]
    * scenarios["net_power_mwe"]
    / 1000
)

# ----------------------------------------
# 4. Use our existing Stage 4.1 model
# ----------------------------------------

calculations = scenarios.apply(
    calculate_lcoe,
    axis=1
)

results = pd.concat(
    [scenarios, calculations],
    axis=1
)

# Validate sensitivity direction
ordered = results.sort_values(
    "capex_eur_per_kwe"
)

assert ordered["lcoe_eur_per_mwh"].is_monotonic_increasing

# ----------------------------------------
# 5. Export results
# ----------------------------------------

output_csv = REPORTS / "stage42_lcoe_scenarios.csv"
results.to_csv(output_csv, index=False)

print("\nSTELLARIS ANALYST SCENARIOS")
print(
    results[
        [
            "scenario_name",
            "capex_eur_per_kwe",
            "capex_eur_million",
            "lcoe_eur_per_mwh"
        ]
    ].to_string(index=False)
)

# ----------------------------------------
# 6. Visualize CAPEX sensitivity
# ----------------------------------------

fig, ax = plt.subplots(figsize=(9, 5))

ax.plot(
    ordered["capex_eur_per_kwe"],
    ordered["lcoe_eur_per_mwh"],
    marker="o"
)

ax.set_xlabel("Assumed overnight CAPEX (2024 EUR/kWe)")
ax.set_ylabel("Modeled LCOE (2024 EUR/MWh)")

ax.set_title(
    "Provisional Stellaris CAPEX Sensitivity"
)

ax.grid(True, alpha=0.3)

fig.text(
    0.5, 0.01,
    "Analyst scenarios, not Proxima cost forecasts.",
    ha="center",
    fontsize=9
)

fig.tight_layout(rect=[0, 0.04, 1, 1])

output_png = REPORTS / "stage42_capex_sensitivity.png"

fig.savefig(
    output_png,
    dpi=200,
    bbox_inches="tight"
)

print("\nSaved:", output_csv.relative_to(ROOT))
print("Saved:", output_png.relative_to(ROOT))

print(
    "\nNOTE: USD literature benchmarks were NOT "
    "converted into EUR scenarios."
)
print(
    "Country, price year, device, and FOAK/NOAK "
    "comparability remain unresolved."
)

plt.show()
