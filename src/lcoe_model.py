
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

REPORTS.mkdir(exist_ok=True)

INPUT_FILE = DATA / "lcoe_scenarios.csv"


def capital_recovery_factor(r, n):
    """Convert upfront capital into an equivalent annual cost."""
    if n <= 0 or r < 0:
        raise ValueError("Invalid lifetime or discount rate")

    if r == 0:
        return 1 / n

    return r / (1 - (1 + r) ** (-n))


def calculate_lcoe(row):
    """Compute simplified, real, pre-tax LCOE in EUR/MWh."""

    capex = float(row["capex_eur_million"]) * 1e6
    power_mw = float(row["net_power_mwe"])
    cf = float(row["capacity_factor"])
    fixed_opex = (
        float(row["fixed_opex_eur_million_per_year"])
        * 1e6
    )
    variable_opex = float(
        row["variable_opex_eur_per_mwh"]
    )

    lifetime = int(row["plant_lifetime_years"])
    rate = float(row["real_discount_rate"])

    if capex < 0 or fixed_opex < 0 or variable_opex < 0:
        raise ValueError("Costs cannot be negative")

    if power_mw <= 0 or not (0 < cf <= 1):
        raise ValueError("Invalid power or capacity factor")

    crf = capital_recovery_factor(rate, lifetime)

    annual_energy_mwh = power_mw * 8760 * cf

    annual_capital_cost = capex * crf

    annual_total_cost = (
        annual_capital_cost
        + fixed_opex
        + variable_opex * annual_energy_mwh
    )

    lcoe = annual_total_cost / annual_energy_mwh

    return pd.Series({
        "annual_energy_mwh": annual_energy_mwh,
        "capital_recovery_factor": crf,
        "annual_capital_cost_eur": annual_capital_cost,
        "annual_total_cost_eur": annual_total_cost,
        "lcoe_eur_per_mwh": lcoe
    })


def main():
    scenarios = pd.read_csv(INPUT_FILE)

    required_columns = [
        "scenario_id", "scenario_name", "device_id",
        "capex_eur_million", "net_power_mwe",
        "capacity_factor",
        "fixed_opex_eur_million_per_year",
        "variable_opex_eur_per_mwh",
        "plant_lifetime_years", "real_discount_rate",
        "assumption_class"
    ]

    missing = set(required_columns) - set(scenarios.columns)

    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    if scenarios["scenario_id"].duplicated().any():
        raise ValueError("Duplicate scenario IDs")

    if not scenarios["assumption_class"].eq(
        "synthetic_test"
    ).all():
        raise ValueError(
            "Session 4.1 accepts synthetic_test scenarios only"
        )

    numeric_columns = required_columns[3:10]

    for col in numeric_columns:
        scenarios[col] = pd.to_numeric(
            scenarios[col], errors="raise"
        )

    if scenarios[numeric_columns].isna().any().any():
        raise ValueError("Missing numeric inputs")

    devices = pd.read_csv(DATA / "reactor_designs.csv")

    if not scenarios["device_id"].isin(
        devices["device_id"]
    ).all():
        raise ValueError("Unknown device_id")

    calculations = scenarios.apply(
        calculate_lcoe, axis=1
    )

    results = pd.concat(
        [scenarios, calculations],
        axis=1
    )

    output = REPORTS / "stage4_lcoe_test_results.csv"
    results.to_csv(output, index=False)

    print("\nSTAGE 4.1 — ILLUSTRATIVE LCOE MODEL")
    print("----------------------------------")

    print(
        results[
            [
                "scenario_name",
                "annual_energy_mwh",
                "lcoe_eur_per_mwh"
            ]
        ].to_string(index=False)
    )

    print("\nSaved:", output.relative_to(ROOT))
    print("WARNING: Synthetic inputs, not Proxima forecasts.")


if __name__ == "__main__":
    main()
