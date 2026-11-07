"""Reconcile every Stage 4 scenario table against current source inputs.

Recomputation uses existing pure model functions; analysis modules with file
writing at import time are deliberately not imported here. No files are written.
"""

import math
from pathlib import Path

import numpy as np
import pandas as pd

from lcoe_model import calculate_lcoe, capital_recovery_factor
from project_cash_flow import calculate_project_cash_flow

ROOT = Path(__file__).resolve().parent.parent


def read_input(root, name):
    table = pd.read_csv(root / "data" / name)
    if table.empty or "scenario_id" not in table:
        raise ValueError(f"{name}: missing scenario rows or scenario_id")
    if table["scenario_id"].isna().any() or table["scenario_id"].duplicated().any():
        raise ValueError(f"{name}: empty or duplicate scenario IDs")
    return table


def with_capex(table):
    table = table.copy()
    table["capex_eur_million"] = table["capex_eur_per_kwe"] * table["net_power_mwe"] / 1000
    return table


def lcoe_rows(table):
    return pd.concat([table.reset_index(drop=True),
                      table.apply(calculate_lcoe, axis=1).reset_index(drop=True)], axis=1)


def expected_tables(root=ROOT):
    root = Path(root)
    synthetic = read_input(root, "lcoe_scenarios.csv")
    costs = read_input(root, "lcoe_scenarios_stage42.csv")
    performance = read_input(root, "lcoe_performance_scenarios.csv")
    learning = read_input(root, "manufacturing_learning_scenarios.csv")
    prices = read_input(root, "electricity_revenue_scenarios.csv")
    reference = with_capex(costs[costs["scenario_id"] == "CAL002"])
    if len(reference) != 1:
        raise ValueError("Expected exactly one CAL002 reference")
    base = reference.iloc[0]
    grid = costs.drop(columns="capacity_factor").merge(
        performance[["scenario_id", "capacity_factor"]].rename(
            columns={"scenario_id": "performance_id"}), how="cross")
    calculated_grid = lcoe_rows(with_capex(grid))
    # These are the explicitly declared legacy Stage 4.3 comparison assumptions.
    # They are separate from the main CAL002 reference; Step 4 will register them.
    baseline = calculated_grid[
        (calculated_grid["capex_eur_per_kwe"] == 8000)
        & np.isclose(calculated_grid["capacity_factor"], .85)
    ]
    if len(baseline) != 1:
        raise ValueError("Stage 4.3 requires its declared 8000 EUR/kWe, 85% reference")
    target = float(baseline.iloc[0]["lcoe_eur_per_mwh"])
    break_even, power_rows, learning_rows, summaries, annual_rows = [], [], [], [], []
    for _, row in costs.iterrows():
        power = float(row["net_power_mwe"])
        crf = capital_recovery_factor(float(row["real_discount_rate"]), int(row["plant_lifetime_years"]))
        required_cf = (float(row["capex_eur_per_kwe"]) * power * 1000 * crf
                       + float(row["fixed_opex_eur_million_per_year"]) * 1e6) / (
                           power * 8760 * (target - float(row["variable_opex_eur_per_mwh"])))
        break_even.append({"scenario_name": row["scenario_name"],
                           "capex_eur_per_kwe": row["capex_eur_per_kwe"],
                           "required_capacity_factor": required_cf,
                           "feasible_under_cf_le_1": required_cf <= 1})
    for power in (800, 1000, 1200):
        case = baseline.iloc[0].copy()
        case["net_power_mwe"] = power
        power_rows.append({"net_power_mwe": power,
                           "lcoe_eur_per_mwh": calculate_lcoe(case)["lcoe_eur_per_mwh"]})
    initial = float(base["capex_eur_million"])
    for _, scenario in learning.iterrows():
        share = float(scenario["magnet_capex_share"])
        rate = float(scenario["magnet_learning_rate"])
        for units in (1, 2, 4, 8, 16):
            factor = (1 - rate) ** math.log2(units)
            capex = initial * (1 - share + share * factor)
            case = base.copy()
            case["capex_eur_million"] = capex
            learning_rows.append({
                "scenario_id": scenario["scenario_id"], "scenario_name": scenario["scenario_name"],
                "cumulative_equivalent_units": units, "magnet_capex_share": share,
                "magnet_learning_rate": rate, "magnet_cost_factor": factor,
                "total_capex_eur_million": capex,
                "capex_eur_per_kwe": capex * 1000 / float(base["net_power_mwe"]),
                "lcoe_eur_per_mwh": calculate_lcoe(case)["lcoe_eur_per_mwh"],
            })
    for _, price in prices.iterrows():
        annual, metrics = calculate_project_cash_flow(base, price["electricity_price_eur_per_mwh"])
        annual.insert(0, "scenario_id", price["scenario_id"])
        annual.insert(1, "scenario_name", price["scenario_name"])
        annual_rows.append(annual)
        summaries.append({**price.to_dict(), **metrics})
    return {
        "stage4_lcoe_test_results.csv": (lcoe_rows(synthetic), ["scenario_id"]),
        "stage42_lcoe_scenarios.csv": (lcoe_rows(with_capex(costs)), ["scenario_id"]),
        "stage43_performance_sensitivity.csv": (calculated_grid, ["scenario_id", "performance_id"]),
        "stage43_break_even_capacity_factor.csv": (pd.DataFrame(break_even), ["scenario_name", "capex_eur_per_kwe"]),
        "stage43_net_power_sensitivity.csv": (pd.DataFrame(power_rows), ["net_power_mwe"]),
        "stage44_learning_results.csv": (pd.DataFrame(learning_rows), ["scenario_id", "cumulative_equivalent_units"]),
        "stage45_npv_summary.csv": (pd.DataFrame(summaries), ["scenario_id"]),
        "stage45_annual_cash_flows.csv": (pd.concat(annual_rows, ignore_index=True), ["scenario_id", "year"]),
    }


def compare_table(actual, expected, keys):
    if set(actual.columns) != set(expected.columns):
        raise ValueError("Column set differs from current inputs/model")
    if actual[keys].isna().any().any() or actual.duplicated(keys).any():
        raise ValueError("Missing or duplicate scenario keys")
    numeric = actual.select_dtypes(include="number")
    if not np.isfinite(numeric.to_numpy()).all():
        raise ValueError("Non-finite report values")
    actual = actual.sort_values(keys).reset_index(drop=True)
    expected = expected.sort_values(keys).reset_index(drop=True)
    pd.testing.assert_frame_equal(actual[expected.columns], expected, check_dtype=False,
                                  check_exact=False, rtol=1e-10, atol=1e-6)


def reconciliation_checks(root=ROOT):
    results = []
    for filename, (expected, keys) in expected_tables(root).items():
        try:
            actual = pd.read_csv(Path(root) / "reports" / filename)
            compare_table(actual, expected, keys)
            results.append(("Current inputs: " + filename, True,
                            "All scenario keys, input fields and model outputs reconcile."))
        except (OSError, ValueError, AssertionError, KeyError) as exc:
            results.append(("Current inputs: " + filename, False,
                            "Stale, missing or inconsistent table: " + str(exc)[:650]))
    return results
