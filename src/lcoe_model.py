
from pathlib import Path
import math

import pandas as pd

from economic_validation import (
    ECONOMIC_FIELDS, finite_number, positive_integer, validate_economic_case,
)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

REPORTS.mkdir(exist_ok=True)

INPUT_FILE = DATA / "lcoe_scenarios.csv"


def capital_recovery_factor(r, n):
    """Convert upfront capital into an equivalent annual cost."""
    r = finite_number(r, "real_discount_rate", minimum=0)
    n = positive_integer(n)
    if r == 0:
        return 1 / n
    # Avoid cancellation when r is near zero.
    return finite_number(r / -math.expm1(-n * math.log1p(r)),
                         "capital_recovery_factor", minimum=0)


def calculate_lcoe(row):
    """Compute simplified, real, pre-tax LCOE in EUR/MWh."""

    checked = validate_economic_case(row)
    capex = finite_number(checked["capex_eur_million"] * 1e6, "CAPEX in EUR", minimum=0)
    power_mw = checked["net_power_mwe"]
    cf = checked["capacity_factor"]
    fixed_opex = finite_number(checked["fixed_opex_eur_million_per_year"] * 1e6,
                               "fixed OPEX in EUR/year", minimum=0)
    variable_opex = checked["variable_opex_eur_per_mwh"]
    lifetime = checked["plant_lifetime_years"]
    rate = checked["real_discount_rate"]

    crf = capital_recovery_factor(rate, lifetime)

    annual_energy_mwh = finite_number(power_mw * 8760 * cf, "annual_energy_mwh",
                                       minimum=0, minimum_inclusive=False)

    annual_capital_cost = capex * crf

    annual_total_cost = (
        annual_capital_cost
        + fixed_opex
        + variable_opex * annual_energy_mwh
    )

    annual_capital_cost = finite_number(annual_capital_cost, "annual_capital_cost_eur", minimum=0)
    annual_total_cost = finite_number(annual_total_cost, "annual_total_cost_eur", minimum=0)
    lcoe = finite_number(annual_total_cost / annual_energy_mwh, "lcoe_eur_per_mwh", minimum=0)

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

    numeric_columns = list(ECONOMIC_FIELDS)

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
