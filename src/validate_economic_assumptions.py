"""Validate the reviewed assumption register against active scenario inputs.

No scenario values or register entries are generated or silently synchronized.
Passing checks establish traceability; the assumptions remain uncalibrated.
"""

import csv
import json
import math
from pathlib import Path

from economic_validation import finite_number
from stage34_provenance import write_json

ROOT = Path(__file__).resolve().parent.parent
PARAMETERS = {
    "CAPEX": ("capex_eur_per_kwe", "EUR_2024/kWe", "CAL002", 0),
    "POWER": ("net_power_mwe", "MWe", "CAL002", 0),
    "CF": ("capacity_factor", "fraction", "CAL002", 0),
    "FOM": ("fixed_opex_eur_million_per_year", "EUR_2024_million/year", "CAL002", 0),
    "VOM": ("variable_opex_eur_per_mwh", "EUR_2024/MWh", "CAL002", 0),
    "LIFE": ("plant_lifetime_years", "years", "CAL002", 0),
    "RATE": ("real_discount_rate", "fraction_real", "CAL002", 0),
    "SHARE": ("magnet_capex_share", "fraction", "LR010", 3),
    "LEARNING": ("magnet_learning_rate", "fraction_per_doubling", "LR010", 3),
    "PRICE": ("electricity_price_eur_per_mwh", "EUR_2024/MWh", "REV003", 4),
}
SCENARIO_FILES = (
    "lcoe_scenarios_stage42.csv", "lcoe_scenarios.csv",
    "lcoe_performance_scenarios.csv", "manufacturing_learning_scenarios.csv",
    "electricity_revenue_scenarios.csv",
)
FIELDS = {value[0]: key for key, value in PARAMETERS.items()}
FILE_FIELDS = (
    tuple(value[0] for key, value in PARAMETERS.items() if key in {"CAPEX", "POWER", "CF", "FOM", "VOM", "LIFE", "RATE"}),
    ("capex_eur_million", "net_power_mwe", "capacity_factor", "fixed_opex_eur_million_per_year",
     "variable_opex_eur_per_mwh", "plant_lifetime_years", "real_discount_rate"),
    ("capacity_factor",), ("magnet_capex_share", "magnet_learning_rate"),
    ("electricity_price_eur_per_mwh",),
)
REGISTER_COLUMNS = {
    "parameter_id", "model_field", "unit", "reference_value", "lower", "upper",
    "reference_scenario", "range_role", "evidence_class", "reference_notes",
    "rationale", "range_rationale", "dependencies", "next_evidence_needed",
    "geography", "deployment_basis", "price_year", "calibration_status",
}
GAPS = [
    "CAPEX/OPEX, lifetime and discount assumptions are not calibrated to a commercial Stellaris plant.",
    "1000 MWe is an analyst net-rated assumption; published peak electric power is not verified net output.",
    "Legacy CF grids remain independent sensitivities. New engineering cases screen conditional compatibility; reliability, improved maintenance costs and commercial feasibility remain unvalidated.",
    "FOAK is an illustrative first-unit scenario label; repeated production is not verified industrial NOAK maturity.",
    "2024 constant EUR is an adopted analyst convention, not a currency/inflation conversion of published USD estimates.",
    "Literature USD benchmarks retain their original values; their price-year and transferability remain unresolved in this project.",
    "Exploratory parameter ranges are stress-test choices, not empirical confidence intervals or probability distributions.",
    "The historical 2024 average is not a future PPA/capture-price forecast.",
]


def read_csv(path, required):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames or []
        if len(columns) != len(set(columns)) or not set(required) <= set(columns):
            raise ValueError(f"{path.name}: duplicate or missing required columns")
        rows = list(reader)
    if not rows or any(None in row or any(v is None for v in row.values()) for row in rows):
        raise ValueError(f"{path.name}: empty or malformed table")
    return rows


def unique(rows, key):
    indexed = {}
    for row in rows:
        value = row[key]
        if not value.strip() or value in indexed:
            raise ValueError(f"Empty or duplicate {key}: {value!r}")
        indexed[value] = row
    return indexed


def json_file(path):
    def reject_constant(value):
        raise ValueError(f"Non-finite JSON constant: {value}")
    return json.loads(path.read_text(encoding="utf-8"), parse_constant=reject_constant)


def audit_assumptions(root=ROOT):
    root = Path(root)
    result = {"status": "FAIL", "errors": [], "research_gaps": list(GAPS),
              "model_basis": {}, "parameters": 0, "bindings_checked": 0,
              "active_inputs": [], "calibration_status": "provisional_not_empirically_calibrated"}
    errors = result["errors"]
    try:
        basis = json_file(root / "data/economic_model_basis.json")
        if not isinstance(basis, dict):
            raise ValueError("economic_model_basis.json must be an object")
        result["model_basis"] = basis
        expected = {
            "schema_version": 1, "currency": "EUR", "price_year": 2024,
            "price_basis": "constant_real", "basis_origin": "analyst_convention_not_source_rebasing",
            "discount_basis": "real_pre_tax_unlevered", "capex_boundary": "overnight_upfront_year_zero",
            "deployment_basis": "illustrative_first_unit_FOAK", "geography": "Europe_context_not_country_calibrated",
            "net_output_basis": "analyst_net_rated_not_verified_Stellaris",
            "model_hours_per_year": 8760, "historical_year": 2024, "historical_hours": 8784,
            "calibration_status": "provisional_not_empirically_calibrated",
            "repeat_unit_basis": "learning_sensitivity_not_verified_NOAK",
        }
        for field, value in expected.items():
            if type(basis.get(field)) is not type(value) or basis[field] != value:
                errors.append(f"Model basis mismatch: {field}; this revision supports {value!r}.")
        for field in ("basis_rationale", "excluded_costs", "parameter_dependencies"):
            if not isinstance(basis.get(field), str) or not basis[field].strip():
                errors.append("Missing model basis explanation: " + field)
        register = unique(read_csv(root / "data/economic_assumptions.csv", REGISTER_COLUMNS), "parameter_id")
        if set(register) != set(PARAMETERS):
            raise ValueError("Assumption parameter IDs do not match all ten modeled input families")
        notes = unique(read_csv(root / "data/economic_reference_notes.csv", {
            "note_id", "source_id", "url", "locator", "source_role", "finding", "transfer_limit",
        }), "note_id")
        source_ids = unique(read_csv(root / "data/sources.csv", {"source_id"}), "source_id")
        for note in notes.values():
            if note["source_id"] and note["source_id"] not in source_ids:
                errors.append("Unknown source ID in " + note["note_id"])
            if not note["url"].startswith("https://") or not all(note[f].strip() for f in
                    ("locator", "source_role", "finding", "transfer_limit")):
                errors.append("Incomplete reference note: " + note["note_id"])
            if note["source_role"] not in {"context_only", "methodology_only", "historical_value"}:
                errors.append("Unsupported reference transfer claim: " + note["note_id"])
        bounds = {}
        for identifier, row in register.items():
            field, unit, ref_id, file_index = PARAMETERS[identifier]
            if row["model_field"] != field or row["unit"] != unit or row["reference_scenario"] != ref_id:
                errors.append("Field/unit/reference mismatch: " + identifier)
            if not all(row[name].strip() for name in REGISTER_COLUMNS):
                errors.append("Unexplained register field: " + identifier)
            if row["evidence_class"] != "analyst_assumption" or row["calibration_status"] != result["calibration_status"]:
                errors.append("Unsupported evidence/calibration claim: " + identifier)
            if row["range_role"] not in {"existing_scenario_envelope", "exploratory_candidate_not_executed"}:
                errors.append("Unsupported range classification: " + identifier)
            if row["geography"] != basis["geography"] or row["deployment_basis"] != basis["deployment_basis"]:
                errors.append("Geography/deployment basis mismatch: " + identifier)
            money = unit.startswith("EUR")
            if row["price_year"] != (str(basis["price_year"]) if money else "not_applicable"):
                errors.append("Price year mismatch: " + identifier)
            references = row["reference_notes"].split(";")
            if any(note not in notes for note in references):
                errors.append("Unknown reference note: " + identifier)
            lower, ref, upper = (finite_number(row[name], f"{identifier}.{name}")
                                 for name in ("lower", "reference_value", "upper"))
            if not lower <= ref <= upper:
                errors.append("Reference outside declared range: " + identifier)
            bounds[identifier] = (lower, ref, upper)
        tables = {name: unique(read_csv(root / "data" / name,
                  {"scenario_id", "assumption_class"} | set(FILE_FIELDS[index])), "scenario_id")
                  for index, name in enumerate(SCENARIO_FILES)}
        for identifier, (field, _, ref_id, file_index) in PARAMETERS.items():
            ref = tables[SCENARIO_FILES[file_index]][ref_id]
            value = finite_number(ref[field], ref_id + "." + field)
            if not math.isclose(value, bounds[identifier][1], rel_tol=1e-12, abs_tol=1e-12):
                errors.append("Register reference differs from active input: " + identifier)
        for filename, rows in tables.items():
            for row in rows.values():
                scenario = row["scenario_id"]
                expected_class = ("synthetic_test" if filename == "lcoe_scenarios.csv" else
                                  "historical_observation" if scenario == "REV001" and filename == SCENARIO_FILES[4]
                                  else "analyst_scenario")
                if row["assumption_class"] != expected_class:
                    errors.append("Unsupported scenario evidence claim: " + scenario)
                for field, identifier in FIELDS.items():
                    source_field = field
                    if identifier == "CAPEX" and filename == "lcoe_scenarios.csv":
                        source_field = "capex_eur_million"
                        value = finite_number(row[source_field], scenario + "." + source_field) * 1000 / finite_number(
                            row["net_power_mwe"], "net_power_mwe", minimum=0, minimum_inclusive=False)
                    elif field in row:
                        value = finite_number(row[field], scenario + "." + field)
                    else:
                        continue
                    if not bounds[identifier][0] <= value <= bounds[identifier][2]:
                        errors.append(f"Active input outside reviewed range: {filename}:{scenario}:{field}")
                    result["active_inputs"].append({"input_file": filename, "scenario_id": scenario,
                        "input_field": source_field, "parameter_id": identifier,
                        "value_in_register_units": value, "unit": PARAMETERS[identifier][1],
                        "classification": expected_class,
                        "source_role": "historical_value" if expected_class == "historical_observation" else "assumption_or_synthetic_test"})
        historical = json_file(root / "data/electricity_summary_2024.json")
        if historical["year"] != 2024 or historical["hours"] != 8784:
            errors.append("Historical reference year/hour count changed")
        price = float(tables[SCENARIO_FILES[4]]["REV001"]["electricity_price_eur_per_mwh"])
        if not math.isclose(price, round(float(historical["mean_eur_mwh"]), 2), abs_tol=1e-9, rel_tol=0):
            errors.append("REV001 differs from the rounded historical 2024 mean")
        result["parameters"] = len(register)
        result["bindings_checked"] = len(result["active_inputs"])
    except (OSError, ValueError, KeyError, TypeError, ZeroDivisionError) as exc:
        errors.append(str(exc))
    if not errors:
        result["status"] = "PASS_WITH_RESEARCH_GAPS"
    return result


def main():
    audit = audit_assumptions()
    write_json(ROOT / "reports/economic_assumption_audit.json", audit)
    lines = ["# Economic Assumptions and Model Basis", "", f"Status: {audit['status']}",
             f"Parameters: {audit['parameters']} | Active numerical bindings: {audit['bindings_checked']}",
             "", "Monetary model outputs use 2024 constant EUR by analyst convention.",
             "Published USD benchmarks are not converted or used as calibrated EUR inputs.",
             "", "## Errors", ""]
    lines += ["- " + item for item in audit["errors"]] or ["- None detected"]
    lines += ["", "## Retained Research Gaps", ""]
    lines += ["- " + item for item in audit["research_gaps"]]
    (ROOT / "reports").mkdir(exist_ok=True)
    (ROOT / "reports/economic_assumption_audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Economic assumptions: " + audit["status"])
    print(f"Parameters: {audit['parameters']} | Bindings: {audit['bindings_checked']} | Errors: {len(audit['errors'])}")
    for error in audit["errors"]:
        print("ERROR: " + error)
    return 1 if audit["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
