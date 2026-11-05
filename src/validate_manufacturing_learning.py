
from pathlib import Path

import numpy as np
import pandas as pd

from manufacturing_learning import (
    experience_factor,
    learned_capex
)

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"

results = pd.read_csv(
    REPORTS / "stage44_learning_results.csv"
)

# Check expected number of combinations
assert len(results) == 15

# A zero learning rate must have no cost effect
no_learning = results[
    results["scenario_id"] == "LR000"
]

assert np.allclose(
    no_learning["total_capex_eur_million"],
    12000
)

# First unit has no accumulated cost reduction
assert np.isclose(
    experience_factor(1, 0.20), 1.0
)

# One doubling with 20% learning
assert np.isclose(
    experience_factor(2, 0.20), 0.8
)

# Four doublings with 20% learning
assert np.isclose(
    experience_factor(16, 0.20),
    0.8**4
)

# Verify component-level CAPEX calculation
cost = learned_capex(
    initial_capex=12e9,
    share=0.25,
    rate=0.20,
    units=16
)

assert np.isclose(cost, 10.2288e9)

# Calculate required learning rate
# for 10% total CAPEX reduction at N=8
magnet_share = 0.25
target_total_cost_fraction = 0.90
units = 8

required_component_fraction = (
    target_total_cost_fraction
    - (1 - magnet_share)
) / magnet_share

assert 0 < required_component_fraction <= 1

required_learning_rate = (
    1
    - required_component_fraction ** (
        1 / np.log2(units)
    )
)

assert np.isclose(
    required_learning_rate,
    1 - 0.60 ** (1 / 3)
)

print(
    "Required magnet learning rate for "
    "10% total CAPEX reduction at N=8: "
    f"{required_learning_rate:.2%}"
)

print("All Stage 4.4 validation checks passed.")
