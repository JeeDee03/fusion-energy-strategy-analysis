
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# Load existing and new datasets
companies = pd.read_csv(DATA / "companies.csv")
sources = pd.read_csv(DATA / "sources.csv")
devices = pd.read_csv(DATA / "reactor_designs.csv")
parameters = pd.read_csv(DATA / "technical_parameters.csv")

# 1. Check unique identifiers
assert companies["company_id"].is_unique
assert sources["source_id"].is_unique
assert devices["device_id"].is_unique
assert parameters["parameter_id"].is_unique

# 2. Check company references
assert devices["company_id"].isin(
    companies["company_id"]
).all(), "Unknown company in reactor dataset"

# 3. Check source references
assert devices["source_id"].isin(
    sources["source_id"]
).all(), "Unknown reactor source"

assert parameters["source_id"].isin(
    sources["source_id"]
).all(), "Unknown parameter source"

# 4. Check device references
assert parameters["device_id"].isin(
    devices["device_id"]
).all(), "Unknown reactor in technical parameters"

# 5. Validate evidence types
allowed_evidence = {
    "measured",
    "simulated",
    "design_target",
    "announced_target"
}

assert parameters["evidence_type"].isin(
    allowed_evidence
).all(), "Invalid evidence classification"

# 6. Validate numeric values and units
assert parameters["value"].notna().all()
assert pd.to_numeric(
    parameters["value"], errors="coerce"
).notna().all()

assert parameters["unit"].notna().all()

# 7. Join parameters with device and company names
result = parameters.merge(
    devices[
        ["device_id", "company_id", "device_name"]
    ],
    on="device_id",
    validate="many_to_one"
).merge(
    companies[["company_id", "company_name"]],
    on="company_id",
    validate="many_to_one"
)

print("\nTechnical Parameters:")
print(
    result[
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

print("\nTechnical dataset validation successful!")
print(f"Devices recorded: {len(devices)}")
print(f"Parameters recorded: {len(parameters)}")
