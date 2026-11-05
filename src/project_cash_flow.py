
from pathlib import Path

import numpy as np
import pandas as pd

from lcoe_model import calculate_lcoe

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)


def load_reference_case():
    cases = pd.read_csv(
        DATA / "lcoe_scenarios_stage42.csv"
    )

    selected = cases[
        cases["scenario_id"] == "CAL002"
    ]

    if len(selected) != 1:
        raise ValueError("CAL002 must occur exactly once")

    row = selected.iloc[0].copy()

    required = [
        "capex_eur_per_kwe",
        "net_power_mwe",
        "capacity_factor",
        "fixed_opex_eur_million_per_year",
        "variable_opex_eur_per_mwh",
        "plant_lifetime_years",
        "real_discount_rate",
    ]

    for field in required:
        row[field] = float(row[field])

    row["capex_eur_million"] = (
        row["capex_eur_per_kwe"]
        * row["net_power_mwe"]
        / 1000
    )

    return row


def calculate_project_cash_flow(case, price):
    """
    Simplified real, unlevered, pre-tax project DCF.

    Year 0: full upfront CAPEX.
    Years 1..N: constant generation, sale price and OPEX.

    No financing, taxes, replacements, residual value,
    price escalation or construction schedule.
    """
    price = float(price)

    if not np.isfinite(price):
        raise ValueError("Invalid electricity price")

    capex = float(case["capex_eur_million"]) * 1e6
    power = float(case["net_power_mwe"])
    cf = float(case["capacity_factor"])
    fixed_opex = (
        float(case["fixed_opex_eur_million_per_year"])
        * 1e6
    )
    variable_opex = float(
        case["variable_opex_eur_per_mwh"]
    )
    rate = float(case["real_discount_rate"])

    raw_lifetime = float(case["plant_lifetime_years"])
    lifetime = int(raw_lifetime)

    if raw_lifetime != lifetime or lifetime <= 0:
        raise ValueError("Invalid lifetime")
    if rate < 0 or not np.isfinite(rate):
        raise ValueError("Invalid discount rate")
    if capex < 0 or fixed_opex < 0 or variable_opex < 0:
        raise ValueError("Costs must be nonnegative")
    if power <= 0 or not 0 < cf <= 1:
        raise ValueError("Invalid power or capacity factor")

    annual_energy = power * 8760 * cf

    annual_revenue = annual_energy * price
    annual_variable_opex = annual_energy * variable_opex

    annual_cash_flow = (
        annual_revenue
        - fixed_opex
        - annual_variable_opex
    )

    rows = [{
        "year": 0,
        "electricity_mwh": 0.0,
        "revenue_eur": 0.0,
        "operating_cost_eur": 0.0,
        "investment_eur": capex,
        "cash_flow_eur": -capex,
        "discounted_cash_flow_eur": -capex,
    }]

    for year in range(1, lifetime + 1):
        rows.append({
            "year": year,
            "electricity_mwh": annual_energy,
            "revenue_eur": annual_revenue,
            "operating_cost_eur": (
                fixed_opex + annual_variable_opex
            ),
            "investment_eur": 0.0,
            "cash_flow_eur": annual_cash_flow,
            "discounted_cash_flow_eur": (
                annual_cash_flow / (1 + rate) ** year
            ),
        })

    cash_flows = pd.DataFrame(rows)
    cash_flows["cumulative_discounted_eur"] = (
        cash_flows["discounted_cash_flow_eur"].cumsum()
    )

    npv = cash_flows[
        "discounted_cash_flow_eur"
    ].sum()

    lcoe = float(
        calculate_lcoe(case)["lcoe_eur_per_mwh"]
    )

    return cash_flows, {
        "annual_energy_mwh": annual_energy,
        "annual_revenue_eur": annual_revenue,
        "annual_operating_cash_flow_eur": annual_cash_flow,
        "lcoe_eur_per_mwh": lcoe,
        "break_even_price_eur_per_mwh": lcoe,
        "npv_eur": npv,
    }


def main():
    reference = load_reference_case()

    prices = pd.read_csv(
        DATA / "electricity_revenue_scenarios.csv"
    )

    if not prices["scenario_id"].is_unique:
        raise ValueError("Duplicate scenario IDs")

    allowed = {
        "historical_observation",
        "analyst_scenario",
    }

    if not prices["assumption_class"].isin(allowed).all():
        raise ValueError("Unexpected assumption class")

    prices["electricity_price_eur_per_mwh"] = (
        pd.to_numeric(
            prices["electricity_price_eur_per_mwh"],
            errors="raise"
        )
    )

    if not np.isfinite(
        prices["electricity_price_eur_per_mwh"]
    ).all():
        raise ValueError("Invalid electricity prices")

    summaries = []
    all_cash_flows = []

    for _, scenario in prices.iterrows():
        cash_flows, metrics = calculate_project_cash_flow(
            reference,
            scenario["electricity_price_eur_per_mwh"]
        )

        cash_flows.insert(
            0, "scenario_id", scenario["scenario_id"]
        )

        cash_flows.insert(
            1, "scenario_name", scenario["scenario_name"]
        )

        all_cash_flows.append(cash_flows)

        summaries.append({
            "scenario_id": scenario["scenario_id"],
            "scenario_name": scenario["scenario_name"],
            "pricing_basis": scenario["pricing_basis"],
            "assumption_class": scenario["assumption_class"],
            "electricity_price_eur_per_mwh": (
                scenario["electricity_price_eur_per_mwh"]
            ),
            **metrics,
        })

    summary = pd.DataFrame(summaries)
    annual = pd.concat(
        all_cash_flows, ignore_index=True
    )

    summary.to_csv(
        REPORTS / "stage45_npv_summary.csv",
        index=False
    )

    annual.to_csv(
        REPORTS / "stage45_annual_cash_flows.csv",
        index=False
    )

    print("\nSTAGE 4.5 — PROJECT CASH-FLOW ANALYSIS")
    print(
        summary[[
            "scenario_name",
            "electricity_price_eur_per_mwh",
            "annual_revenue_eur",
            "npv_eur",
            "break_even_price_eur_per_mwh",
        ]].to_string(index=False)
    )

    print("\nOutputs saved in reports/")
    print(
        "WARNING: Illustrative real, pre-tax, "
        "unlevered project cash flows."
    )


if __name__ == "__main__":
    main()
