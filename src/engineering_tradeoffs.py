
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

REPORTS.mkdir(exist_ok=True)

devices = pd.read_csv(DATA / "reactor_designs.csv")
parameters = pd.read_csv(DATA / "technical_parameters.csv")
companies = pd.read_csv(DATA / "companies.csv")

# Join parameters to devices and companies
df = parameters.merge(
    devices[["device_id", "company_id", "device_name"]],
    on="device_id",
    validate="many_to_one"
).merge(
    companies[["company_id", "company_name"]],
    on="company_id",
    validate="many_to_one"
)

# Inspect the documented engineering parameters
print("\nEngineering evidence:")
print(
    df[
        [
            "company_name",
            "device_name",
            "parameter_name",
            "value",
            "unit",
            "evidence_type"
        ]
    ].to_string(index=False)
)

# Magnetic pressure scale
mu0 = 4 * np.pi * 1e-7  # H/m, conventional approximation

def magnetic_pressure_mpa(B):
    return B**2 / (2 * mu0) / 1e6

stellaris = df[df["device_id"] == "PF_STELLARIS"]

def get_parameter(name):
    matches = stellaris[
        stellaris["parameter_name"] == name
    ]

    assert len(matches) == 1, (
        f"Expected one value for {name}"
    )

    return float(matches.iloc[0]["value"])

B_average = get_parameter("average_magnetic_field")
B_peak = get_parameter("peak_conductor_field")

p_average = magnetic_pressure_mpa(B_average)
p_peak = magnetic_pressure_mpa(B_peak)

print("\nStellaris magnetic pressure scales:")
print(f"Average-field scale: {p_average:.2f} MPa")
print(f"Peak-conductor-field scale: {p_peak:.2f} MPa")
print(f"Ratio: {p_peak / p_average:.2f}")

print(
    "\nThese are magnetic pressure scales, "
    "not calculated structural stresses."
)

# Export the joined evidence table
output = REPORTS / "stage3_engineering_evidence.csv"
df.to_csv(output, index=False)

print("\nSaved:", output)
