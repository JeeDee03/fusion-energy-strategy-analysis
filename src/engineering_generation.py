"""Conditional engineering-to-generation model, separate from legacy CF tests.

The full-power-exposure case assumes exposure and electrical gross output both
scale linearly with operating load. This is an analyst proxy, not a validated
fusion power balance, materials lifetime or reliability model.
"""

import math
from pathlib import Path

import pandas as pd

from economic_validation import finite_number
from lcoe_model import calculate_lcoe
from prepare_milestone_review import read_table, index_rows
from stage4_reconciliation import compare_table
from stage34_provenance import write_json

ROOT = Path(__file__).resolve().parent.parent
FIELDS = {
    "scenario_id", "scenario_name", "maintenance_basis", "interval_years",
    "major_outage_months", "other_outage_fraction", "operating_load_fraction",
    "gross_electric_mwe", "auxiliary_fraction", "target_capacity_factor",
    "assumption_class", "source_id", "notes",
}


def calculate_generation_case(row):
    """Compute long-run cycle averages; no economic or source files are read."""
    try:
        basis = row["maintenance_basis"]
        interval = finite_number(row["interval_years"], "interval_years", minimum=0, minimum_inclusive=False)
        months = finite_number(row["major_outage_months"], "major_outage_months", minimum=0)
        other = finite_number(row["other_outage_fraction"], "other_outage_fraction", minimum=0, maximum=1, maximum_inclusive=False)
        load = finite_number(row["operating_load_fraction"], "operating_load_fraction", minimum=0, maximum=1, minimum_inclusive=False)
        gross = finite_number(row["gross_electric_mwe"], "gross_electric_mwe", minimum=0, minimum_inclusive=False)
        auxiliary = finite_number(row["auxiliary_fraction"], "auxiliary_fraction", minimum=0, maximum=1, maximum_inclusive=False)
        target = finite_number(row["target_capacity_factor"], "target_capacity_factor", minimum=0, maximum=1, minimum_inclusive=False)
    except KeyError as exc:
        raise ValueError(f"Required engineering field missing: {exc}") from exc
    outage_years = months / 12
    nonmajor_output_factor = finite_number((1 - other) * load, "nonmajor_output_factor",
                                           minimum=0, minimum_inclusive=False)
    if basis == "full_power_exposure":
        # Exposure F accumulates during an operating window F/q; the outage
        # follows. FPY is not silently interpreted as calendar operating years.
        operating_window = finite_number(interval / nonmajor_output_factor, "operating_window_years", minimum=0, minimum_inclusive=False)
        cycle = finite_number(operating_window + outage_years, "cycle_years", minimum=0, minimum_inclusive=False)
        major_availability = operating_window / cycle
    elif basis == "calendar_cycle":
        if outage_years >= interval:
            raise ValueError("major_outage_months must be shorter than the calendar cycle")
        cycle = interval
        operating_window = interval - outage_years
        major_availability = operating_window / cycle
    else:
        raise ValueError("maintenance_basis must be full_power_exposure or calendar_cycle")
    online_availability = major_availability * (1 - other)
    cf = finite_number(online_availability * load, "derived_capacity_factor", minimum=0, maximum=1, minimum_inclusive=False)
    net = finite_number(gross * (1 - auxiliary), "net_rated_mwe", minimum=0, minimum_inclusive=False)
    energy = finite_number(net * 8760 * cf, "annual_net_energy_mwh", minimum=0, minimum_inclusive=False)
    return {
        "operating_window_years": operating_window, "cycle_years": cycle,
        "major_outage_availability": major_availability,
        "online_availability": online_availability, "derived_capacity_factor": cf,
        "net_rated_mwe": net, "annual_net_energy_mwh": energy,
        "target_met": bool(cf >= target or math.isclose(cf, target, rel_tol=0, abs_tol=1e-12)),
        "cf_target_gap": cf - target,
    }


def build_generation_results(root=ROOT):
    root = Path(root)
    _, scenarios = read_table(root / "data/engineering_generation_cases.csv", FIELDS)
    indexed = index_rows(scenarios, "scenario_id", "engineering_generation_cases.csv")
    if not indexed:
        raise ValueError("No engineering generation cases")
    _, sources = read_table(root / "data/sources.csv", {"source_id"})
    source_ids = index_rows(sources, "source_id", "sources.csv")
    _, parameters = read_table(root / "data/technical_parameters.csv", {
        "device_id", "parameter_name", "value", "unit", "source_id"})

    def technical(name, unit):
        rows = [p for p in parameters if p["device_id"] == "PF_STELLARIS" and p["parameter_name"] == name]
        if len(rows) != 1 or rows[0]["unit"] != unit or rows[0]["source_id"] != "S3_006":
            raise ValueError("Engineering evidence mismatch for " + name)
        return finite_number(rows[0]["value"], name, minimum=0, minimum_inclusive=False)

    fpy = technical("full_power_years_before_replacement", "full_power_years")
    target_months = technical("major_maintenance_duration_target", "months")
    estimated_months = technical("major_maintenance_duration", "months")
    costs = pd.read_csv(root / "data/lcoe_scenarios_stage42.csv")
    selected = costs[costs["scenario_id"] == "CAL002"]
    if len(selected) != 1:
        raise ValueError("Exactly one CAL002 economic reference is required")
    reference = selected.iloc[0].to_dict()
    reference["capex_eur_million"] = finite_number(reference["capex_eur_per_kwe"], "capex_eur_per_kwe", minimum=0) * finite_number(
        reference["net_power_mwe"], "net_power_mwe", minimum=0, minimum_inclusive=False) / 1000
    rows = []
    for scenario in scenarios:
        if scenario["assumption_class"] != "analyst_scenario" or scenario["source_id"] != "S3_006" or scenario["source_id"] not in source_ids:
            raise ValueError("Engineering cases must remain analyst assumptions with explicit S3_006 context")
        if not scenario["scenario_name"].strip() or not scenario["notes"].strip():
            raise ValueError("Engineering case lacks explanation")
        metrics = calculate_generation_case(scenario)
        months = float(scenario["major_outage_months"])
        if months < target_months:
            evidence_relation = "beyond_documented_duration_target"
        elif scenario["maintenance_basis"] == "calendar_cycle":
            evidence_relation = "analyst_calendar_interpretation"
        elif math.isclose(float(scenario["interval_years"]), fpy) and any(
                math.isclose(months, value) for value in (target_months, estimated_months)):
            evidence_relation = "conceptual_maintenance_inputs_only"
        else:
            evidence_relation = "other_analyst_maintenance_assumption"
        case = {**reference, "net_power_mwe": metrics["net_rated_mwe"],
                "capacity_factor": metrics["derived_capacity_factor"]}
        lcoe = calculate_lcoe(case)
        if not math.isclose(float(lcoe["annual_energy_mwh"]), metrics["annual_net_energy_mwh"], rel_tol=1e-12):
            raise ValueError("Engineering and economic energy calculations disagree")
        numerical_fields = FIELDS - {"scenario_id", "scenario_name", "maintenance_basis", "assumption_class", "source_id", "notes"}
        clean_scenario = {**scenario, **{key: float(scenario[key]) for key in numerical_fields}}
        rows.append({**clean_scenario, **metrics, "evidence_relation": evidence_relation,
                     "capex_eur_million": reference["capex_eur_million"],
                     "effective_capex_eur_per_kwe": reference["capex_eur_million"] * 1000 / metrics["net_rated_mwe"],
                     "lcoe_eur_2024_per_mwh": float(lcoe["lcoe_eur_per_mwh"]),
                     "cost_basis": "fixed_CAL002_total_overnight_capex"})
    result = pd.DataFrame(rows)
    audit = {
        "status": "PASS_WITH_LIMITATIONS", "scenarios": len(result),
        "targets_met": int(result["target_met"].sum()),
        "targets_not_met": int((~result["target_met"]).sum()),
        "beyond_documented_duration_cases": int((result["evidence_relation"] == "beyond_documented_duration_target").sum()),
        "interpretation": "Targets not met are analytical findings, not invalid data. Passing cases are conditional, not verified reactor feasibility.",
        "limitations": [
            "Gross power, online auxiliary fraction, other downtime and load factors are analyst assumptions, not measured Stellaris parameters.",
            "FPY exposure and gross electrical output are assumed to scale with the same load factor; no nonlinear fusion/thermal/electric model is supplied.",
            "Other downtime is conditional on the non-major-outage window; losses are not subtracted twice.",
            "Auxiliary power reduces net-rated output once. CF is relative to that net rating. Off-state electricity purchases are excluded.",
            "Outputs are long-run cycle averages, not a dated annual maintenance schedule. Step 6 must handle timing and event costs consistently.",
            "Total reference CAPEX and OPEX are held fixed; no engineering cost uplift or replacement event cost is added here.",
            "Legacy independent CF grids are retained as algebraic sensitivity cases, not asserted to satisfy these engineering scenarios.",
        ],
    }
    return result, audit


def reconciliation_check(root=ROOT):
    try:
        expected, _ = build_generation_results(root)
        actual = pd.read_csv(Path(root) / "reports/engineering_generation_scenarios.csv")
        compare_table(actual, expected, ["scenario_id"])
        return True, "All conditional engineering cases and LCOEs match current inputs. Physical validation remains open."
    except (OSError, ValueError, KeyError, AssertionError) as exc:
        return False, str(exc)[:700]


def main():
    reports = ROOT / "reports"
    reports.mkdir(exist_ok=True)
    try:
        results, audit = build_generation_results()
        results.to_csv(reports / "engineering_generation_scenarios.csv", index=False)
        write_json(reports / "engineering_generation_audit.json", audit)
        lines = ["# Conditional Engineering and Generation Scenarios", "", "Status: " + audit["status"],
                 "", f"Cases: {audit['scenarios']} | Targets met: {audit['targets_met']} | Targets not met: {audit['targets_not_met']}",
                 "", "| Case | Net MWe | Derived CF | Target CF | Target met | LCOE EUR_2024/MWh | Evidence relation |",
                 "|---|---:|---:|---:|---|---:|---|"]
        for row in results.to_dict("records"):
            lines.append(f"| {row['scenario_id']} | {row['net_rated_mwe']:.1f} | {row['derived_capacity_factor']:.4%} | "
                         f"{row['target_capacity_factor']:.1%} | {row['target_met']} | {row['lcoe_eur_2024_per_mwh']:.2f} | {row['evidence_relation']} |")
        lines += ["", "## Interpretation and limitations", "", audit["interpretation"], ""]
        lines += ["- " + item for item in audit["limitations"]]
        (reports / "engineering_generation_audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(10, 5))
        x = range(len(results))
        ax.bar(x, 100 * results["derived_capacity_factor"], label="Derived conditional CF")
        ax.scatter(list(x), 100 * results["target_capacity_factor"], color="black", marker="x", label="Tested CF target", zorder=3)
        ax.set_xticks(list(x), results["scenario_id"])
        ax.set_ylabel("Net-rated capacity factor (%)")
        ax.set_title("Conditional generation scenarios; assumptions are not validated plant performance")
        ax.set_ylim(0, 100)
        ax.legend()
        fig.tight_layout()
        fig.savefig(reports / "engineering_generation_capacity_factors.png", dpi=180, bbox_inches="tight")
        plt.close(fig)
        print("Engineering generation: " + audit["status"])
        print(f"Cases: {audit['scenarios']} | Targets met: {audit['targets_met']} | Targets not met: {audit['targets_not_met']}")
        return 0
    except (OSError, ValueError, KeyError) as exc:
        write_json(reports / "engineering_generation_audit.json", {"status": "FAIL", "error": str(exc)})
        print("Engineering generation: FAIL — " + str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
