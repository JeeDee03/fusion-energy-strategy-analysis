
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

DEVICE_ID = "PF_STELLARIS"

technical = pd.read_csv(DATA / "technical_parameters.csv")
devices = pd.read_csv(DATA / "reactor_designs.csv")
sources = pd.read_csv(DATA / "sources.csv")

assert DEVICE_ID in set(devices["device_id"])
assert technical["parameter_id"].is_unique

stellaris = technical[
    technical["device_id"] == DEVICE_ID
].copy()

# Economic inputs required for Stages 4 and 5.
# technical_parameter links to an engineering variable
# already investigated in Stage 3.
#
# A link does NOT mean the variable can be used
# directly as an economic model input.

model_inputs = [
    {
        "input_name": "construction_capex",
        "unit": "EUR",
        "economic_category": "CAPEX",
        "technical_parameter": None,
        "interpretation": "Total overnight plant construction cost",
        "next_action": "Define FOAK cost scenarios"
    },
    {
        "input_name": "magnet_system_capex",
        "unit": "EUR",
        "economic_category": "CAPEX",
        "technical_parameter": "peak_conductor_field",
        "interpretation": "Field is a design proxy, not a cost estimate",
        "next_action": "Research HTS material and fabrication costs"
    },
    {
        "input_name": "fixed_annual_opex",
        "unit": "EUR/year",
        "economic_category": "OPEX",
        "technical_parameter": None,
        "interpretation": "Annual fixed operating expenditure",
        "next_action": "Establish operating cost scenarios"
    },
    {
        "input_name": "replacement_cost",
        "unit": "EUR/event",
        "economic_category": "OPEX",
        "technical_parameter": "major_maintenance_duration",
        "interpretation": "Outage time is not replacement expenditure",
        "next_action": "Estimate major maintenance event costs"
    },
    {
        "input_name": "net_rated_electric_power",
        "unit": "MWe",
        "economic_category": "Output",
        "technical_parameter": "peak_electric_power",
        "interpretation": "Peak electric power is not verified net rated output",
        "next_action": "Resolve gross/net and peak/rated definitions"
    },
    {
        "input_name": "capacity_factor",
        "unit": "fraction",
        "economic_category": "Output",
        "technical_parameter": "major_maintenance_interval_min",
        "interpretation": "Major outage schedule is only one part of CF",
        "next_action": "Build availability and dispatch scenarios"
    },
    {
        "input_name": "auxiliary_power",
        "unit": "MWe",
        "economic_category": "Output",
        "technical_parameter": None,
        "interpretation": "Recirculating and other plant power consumption",
        "next_action": "Research design power balance"
    },
    {
        "input_name": "plant_lifetime",
        "unit": "years",
        "economic_category": "Finance",
        "technical_parameter": None,
        "interpretation": "Economic operating life of the plant",
        "next_action": "Define justified scenario range"
    },
    {
        "input_name": "real_discount_rate",
        "unit": "fraction",
        "economic_category": "Finance",
        "technical_parameter": None,
        "interpretation": "Real project discount rate",
        "next_action": "Define financing assumptions and scenarios"
    },
    {
        "input_name": "manufacturing_learning_rate",
        "unit": "fraction",
        "economic_category": "Manufacturing",
        "technical_parameter": "number_of_modular_coils",
        "interpretation": "Coil count alone cannot establish a learning rate",
        "next_action": "Research manufacturing learning evidence"
    },
    {
        "input_name": "electricity_capture_price",
        "unit": "EUR/MWh",
        "economic_category": "Revenue",
        "technical_parameter": None,
        "interpretation": "Realized electricity sales price",
        "next_action": "Use Stage 2 market data for revenue scenarios"
    }
]

records = []

for index, item in enumerate(model_inputs, start=1):
    parameter_name = item["technical_parameter"]

    match = stellaris.iloc[0:0]

    if parameter_name is not None:
        match = stellaris[
            stellaris["parameter_name"] == parameter_name
        ]

    if len(match) > 1:
        raise ValueError(
            f"Duplicate parameter: {parameter_name}"
        )

    if len(match) == 1:
        row = match.iloc[0]

        assert row["source_id"] in set(sources["source_id"])

        evidence_value = row["value"]
        evidence_unit = row["unit"]
        source_id = row["source_id"]
        evidence_type = row["evidence_type"]
        evidence_status = "engineering_proxy_only"
    else:
        evidence_value = ""
        evidence_unit = ""
        source_id = ""
        evidence_type = ""
        evidence_status = "missing"

    records.append({
        "input_id": f"EI{index:03d}",
        "device_id": DEVICE_ID,
        "economic_category": item["economic_category"],
        "input_name": item["input_name"],
        "required_unit": item["unit"],
        "linked_technical_parameter": parameter_name or "",
        "evidence_value": evidence_value,
        "evidence_unit": evidence_unit,
        "evidence_type": evidence_type,
        "source_id": source_id,
        "evidence_status": evidence_status,
        "interpretation": item["interpretation"],
        "next_action": item["next_action"]
    })

register = pd.DataFrame(records)

output = DATA / "economic_input_register.csv"
register.to_csv(output, index=False)

print("\nEconomic input register created.")
print(f"Device: {DEVICE_ID}")
print(f"Inputs: {len(register)}")

print("\nEvidence status:")
print(register["evidence_status"].value_counts())

print("\nInput summary:")
print(
    register[
        ["input_name", "evidence_status", "next_action"]
    ].to_string(index=False)
)

print(f"\nSaved: {output}")
