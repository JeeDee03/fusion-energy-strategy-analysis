
import pandas as pd

from lcoe_model import (
    capital_recovery_factor,
    calculate_lcoe
)


def test_row(**overrides):
    inputs = {
        "capex_eur_million": 8000,
        "net_power_mwe": 1000,
        "capacity_factor": 0.85,
        "fixed_opex_eur_million_per_year": 200,
        "variable_opex_eur_per_mwh": 5,
        "plant_lifetime_years": 35,
        "real_discount_rate": 0.08,
    }

    inputs.update(overrides)

    return calculate_lcoe(pd.Series(inputs))


baseline = test_row()

higher_capex = test_row(
    capex_eur_million=10000
)

lower_cf = test_row(
    capacity_factor=0.75
)

assert higher_capex["lcoe_eur_per_mwh"] > (
    baseline["lcoe_eur_per_mwh"]
)

assert lower_cf["lcoe_eur_per_mwh"] > (
    baseline["lcoe_eur_per_mwh"]
)

assert abs(
    capital_recovery_factor(0.0, 20) - 0.05
) < 1e-12

assert baseline["annual_energy_mwh"] == (
    1000 * 8760 * 0.85
)

print("All Stage 4.1 LCOE tests passed.")
