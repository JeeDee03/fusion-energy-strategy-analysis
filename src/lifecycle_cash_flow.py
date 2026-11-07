"""Real, pre-tax, unlevered construction/operation/replacement cash flows.

Construction spends occur at integer model times before COD. Operating cash
flows are paid at operating-year end. Replacements are paid at exact outage
start; yearly event buckets retain separate discounted components.
"""

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

from economic_validation import finite_number, validate_economic_case, validate_price
from engineering_generation import calculate_generation_case, build_generation_results
from project_cash_flow import calculate_project_cash_flow
from stage4_reconciliation import compare_table
from stage34_provenance import write_json
from validate_economic_assumptions import audit_assumptions, json_file

ROOT = Path(__file__).resolve().parent.parent
CONFIG_FIELDS = {
    "scenario_id", "scenario_name", "generation_mode", "engineering_case_id",
    "price_scenario_id", "construction_years", "construction_spend_shares",
    "replacement_cost_eur_million", "opex_boundary", "assumption_class", "notes",
}
EVENT_COLUMNS = ["replacement_index", "operating_time_years", "model_time_years",
                 "report_year", "outage_end_model_time_years", "outage_years_within_life",
                 "replacement_cost_eur", "discounted_replacement_cost_eur"]


def normalize_config(config):
    if not isinstance(config, dict) or set(config) != CONFIG_FIELDS:
        raise ValueError("Lifecycle case has missing or unsupported fields")
    for key in ("scenario_id", "scenario_name", "price_scenario_id", "notes"):
        if not isinstance(config[key], str) or not config[key].strip():
            raise ValueError("Missing lifecycle explanation/identifier: " + key)
    if not isinstance(config["engineering_case_id"], str):
        raise ValueError("engineering_case_id must be a string identifier or blank")
    if config["assumption_class"] != "analyst_scenario":
        raise ValueError("Lifecycle cases must remain analyst_scenario")
    years = finite_number(config["construction_years"], "construction_years", minimum=0)
    if not years.is_integer():
        raise ValueError("construction_years must be a nonnegative whole number")
    years = int(years)
    shares = config["construction_spend_shares"]
    if not isinstance(shares, list) or len(shares) != max(1, years):
        raise ValueError("construction_spend_shares length must match construction years (one upfront share for zero)")
    shares = [finite_number(s, "construction_spend_share", minimum=0, maximum=1) for s in shares]
    if not math.isclose(math.fsum(shares), 1, rel_tol=0, abs_tol=1e-12):
        raise ValueError("construction_spend_shares must sum to one")
    replacement = finite_number(config["replacement_cost_eur_million"], "replacement_cost_eur_million", minimum=0)
    if config["generation_mode"] == "legacy_constant_cf":
        if config["engineering_case_id"] or replacement != 0 or config["opex_boundary"] != "legacy_aggregate":
            raise ValueError("Legacy constant-CF cases cannot silently include engineering events/replacement costs")
    elif config["generation_mode"] == "engineering_events":
        if not config["engineering_case_id"] or config["opex_boundary"] != "routine_excludes_major_replacements":
            raise ValueError("Engineering events require an engineering case and OPEX excluding separate major replacements")
    else:
        raise ValueError("Unknown lifecycle generation_mode")
    return {**config, "construction_years": years, "construction_spend_shares": shares,
            "replacement_cost_eur_million": replacement}


def operating_schedule(engineering, lifetime):
    """Allocate operating-window output to exact overlaps with annual bins.

    q includes other downtime/load only; scheduled major outages are explicit,
    so the Step 5 long-run capacity factor is deliberately not multiplied in.
    """
    metrics = calculate_generation_case(engineering)
    q = (1 - float(engineering["other_outage_fraction"])) * float(engineering["operating_load_fraction"])
    window = metrics["operating_window_years"]
    outage = float(engineering["major_outage_months"]) / 12
    energy = [0.0] * lifetime
    events = []
    cursor = 0.0
    while cursor < lifetime - 1e-12:
        finish = min(cursor + window, float(lifetime))
        if finish <= cursor:
            raise ValueError("Maintenance cycle is too short to resolve numerically")
        for year in range(int(math.floor(cursor)), min(lifetime, int(math.ceil(finish)))):
            overlap = max(0.0, min(finish, year + 1) - max(cursor, year))
            energy[year] += metrics["net_rated_mwe"] * 8760 * q * overlap
        if finish >= lifetime - 1e-12:
            break  # Do not buy a replacement at retirement.
        events.append({"operating_time_years": finish,
                       "outage_end_operating_years": min(finish + outage, float(lifetime))})
        if len(events) > 10000:
            raise ValueError("Too many replacement events to materialize")
        cursor = finish + outage
    return energy, events, metrics


def calculate_lifecycle(case, price, config, engineering=None):
    """Pure calculation; no project files are read or written."""
    checked = validate_economic_case(case)
    price = validate_price(price)
    config = normalize_config(config)
    construction = config["construction_years"]
    life = checked["plant_lifetime_years"]
    if construction + life > 10000:
        raise ValueError("Too many annual periods to materialize")
    capex = finite_number(checked["capex_eur_million"] * 1e6, "CAPEX in EUR", minimum=0)
    fixed = finite_number(checked["fixed_opex_eur_million_per_year"] * 1e6, "fixed OPEX in EUR/year", minimum=0)
    replacement = finite_number(config["replacement_cost_eur_million"] * 1e6, "replacement cost in EUR", minimum=0)
    rate_log = math.log1p(checked["real_discount_rate"])
    if config["generation_mode"] == "engineering_events":
        if engineering is None:
            raise ValueError("engineering_events requires engineering inputs")
        energy, raw_events, generation = operating_schedule(engineering, life)
        net = generation["net_rated_mwe"]
    else:
        if engineering is not None:
            raise ValueError("Do not combine legacy CF with explicit engineering outages")
        net = checked["net_power_mwe"]
        annual = finite_number(net * 8760 * checked["capacity_factor"], "annual_net_energy_mwh", minimum=0, minimum_inclusive=False)
        energy, raw_events = [annual] * life, []
    rows = []
    for year in range(construction + life + 1):
        rows.append({"model_year": year, "operating_year": max(0, year - construction),
                     "energy_mwh": 0.0, "revenue_eur": 0.0, "routine_opex_eur": 0.0,
                     "construction_capex_eur": 0.0, "replacement_cost_eur": 0.0,
                     "discounted_energy_mwh": 0.0, "discounted_revenue_eur": 0.0,
                     "discounted_routine_opex_eur": 0.0,
                     "discounted_construction_capex_eur": 0.0,
                     "discounted_replacement_cost_eur": 0.0})
    for time, share in enumerate(config["construction_spend_shares"]):
        rows[time]["construction_capex_eur"] = capex * share
        rows[time]["discounted_construction_capex_eur"] = capex * share * math.exp(-time * rate_log)
    for operating_year, produced in enumerate(energy, 1):
        time = construction + operating_year
        row, factor = rows[time], math.exp(-time * rate_log)
        row["energy_mwh"] = produced
        row["revenue_eur"] = produced * price
        row["routine_opex_eur"] = fixed + produced * checked["variable_opex_eur_per_mwh"]
        for field in ("energy_mwh", "revenue_eur", "routine_opex_eur"):
            row["discounted_" + field] = row[field] * factor
    events = []
    for index, event in enumerate(raw_events, 1):
        start = event["operating_time_years"]
        time = construction + start
        report_year = construction + max(1, int(math.ceil(start)))
        discounted = replacement * math.exp(-time * rate_log)
        events.append({"replacement_index": index, "operating_time_years": start,
                       "model_time_years": time, "report_year": report_year,
                       "outage_end_model_time_years": construction + event["outage_end_operating_years"],
                       "outage_years_within_life": event["outage_end_operating_years"] - start,
                       "replacement_cost_eur": replacement,
                       "discounted_replacement_cost_eur": discounted})
        rows[report_year]["replacement_cost_eur"] += replacement
        rows[report_year]["discounted_replacement_cost_eur"] += discounted
    for row in rows:
        row["cash_flow_eur"] = row["revenue_eur"] - row["routine_opex_eur"] - row["construction_capex_eur"] - row["replacement_cost_eur"]
        row["discounted_cash_flow_eur"] = row["discounted_revenue_eur"] - row["discounted_routine_opex_eur"] - row["discounted_construction_capex_eur"] - row["discounted_replacement_cost_eur"]
    cash = pd.DataFrame(rows)
    cash["cumulative_discounted_eur"] = cash["discounted_cash_flow_eur"].cumsum()
    if not np.isfinite(cash.to_numpy()).all():
        raise ValueError("Lifecycle calculation produced non-finite values")
    pv_energy = finite_number(math.fsum(cash["discounted_energy_mwh"]), "discounted generation", minimum=0, minimum_inclusive=False)
    pv_capex = math.fsum(cash["discounted_construction_capex_eur"])
    pv_routine = math.fsum(cash["discounted_routine_opex_eur"])
    pv_replacements = math.fsum(cash["discounted_replacement_cost_eur"])
    pv_cost = finite_number(pv_capex + pv_routine + pv_replacements, "discounted total cost", minimum=0)
    npv = finite_number(math.fsum(cash["discounted_cash_flow_eur"]), "npv_eur")
    if not math.isclose(npv, price * pv_energy - pv_cost, rel_tol=1e-12, abs_tol=.01):
        raise ValueError("Cash-flow sum and discounted cost/generation identity disagree")
    metrics = {
        "first_revenue_model_year": construction + 1, "last_operating_model_year": construction + life,
        "replacement_count": len(events), "net_rated_mwe": net,
        "total_generation_mwh": math.fsum(energy),
        "finite_life_capacity_factor": math.fsum(energy) / (net * 8760 * life),
        "undiscounted_construction_capex_eur": math.fsum(cash["construction_capex_eur"]),
        "pv_construction_capex_eur": pv_capex, "pv_routine_opex_eur": pv_routine,
        "pv_replacement_cost_eur": pv_replacements, "pv_generation_mwh": pv_energy,
        "npv_eur": npv, "break_even_eur_2024_per_mwh": finite_number(pv_cost / pv_energy, "break-even price", minimum=0),
    }
    return cash, pd.DataFrame(events, columns=EVENT_COLUMNS), metrics


def indexed_scenarios(table, label):
    """Explicit ID checks compatible with pandas without deprecated keywords."""
    if "scenario_id" not in table or table["scenario_id"].isna().any():
        raise ValueError(f"{label}: missing scenario IDs")
    if table["scenario_id"].astype(str).str.strip().eq("").any():
        raise ValueError(f"{label}: empty scenario IDs")
    indexed = table.set_index("scenario_id")
    if not indexed.index.is_unique:
        raise ValueError(f"{label}: duplicate scenario IDs")
    return indexed


def build_lifecycle_results(root=ROOT):
    root = Path(root)
    assumptions = audit_assumptions(root)
    if assumptions["errors"]:
        raise ValueError("Economic basis/assumptions must reconcile: " + "; ".join(assumptions["errors"]))
    source = json_file(root / "data/lifecycle_cash_flow_cases.json")
    if not isinstance(source, dict) or source.get("schema_version") != 1 or source.get("price_year") != 2024 or source.get("currency") != "EUR":
        raise ValueError("Unsupported lifecycle case schema or monetary basis")
    if source.get("cost_boundary") != "staged_overnight_capex_plus_separate_replacements" or source.get("discount_basis") != "real_pre_tax_unlevered_no_extra_IDC":
        raise ValueError("Unsupported lifecycle cost/discount boundary")
    configs = source.get("cases")
    if not isinstance(configs, list) or not configs:
        raise ValueError("No lifecycle cases")
    costs = pd.read_csv(root / "data/lcoe_scenarios_stage42.csv")
    selected = costs[costs["scenario_id"] == "CAL002"]
    if len(selected) != 1:
        raise ValueError("Exactly one CAL002 reference required")
    reference = selected.iloc[0].to_dict()
    reference["capex_eur_million"] = reference["capex_eur_per_kwe"] * reference["net_power_mwe"] / 1000
    prices = indexed_scenarios(pd.read_csv(root / "data/electricity_revenue_scenarios.csv"), "Revenue cases")
    engineering, _ = build_generation_results(root)
    engineering = indexed_scenarios(engineering, "Engineering cases")
    summaries, annuals, events = [], [], []
    ids = set()
    baseline_matches = False
    for raw in configs:
        config = normalize_config(raw)
        key = config["scenario_id"]
        if key in ids:
            raise ValueError("Duplicate lifecycle scenario ID")
        ids.add(key)
        price_row = prices.loc[config["price_scenario_id"]]
        price = price_row["electricity_price_eur_per_mwh"]
        if config["generation_mode"] == "engineering_events":
            eng = engineering.loc[config["engineering_case_id"]].to_dict()
            evidence = eng["evidence_relation"]
        else:
            eng, evidence = None, "legacy_constant_CF_diagnostic"
        cash, event, metrics = calculate_lifecycle(reference, price, config, eng)
        cash.insert(0, "scenario_id", key)
        event.insert(0, "scenario_id", key)
        annuals.append(cash)
        events.append(event)
        summary = {name: value for name, value in config.items() if name != "construction_spend_shares"}
        summary["engineering_case_id"] = config["engineering_case_id"] or "not_applicable"
        summaries.append({**summary, "spend_shares_json": json.dumps(config["construction_spend_shares"], separators=(",", ":")),
                          "electricity_price_eur_2024_per_mwh": float(price),
                          "price_input_class": price_row["assumption_class"],
                          "engineering_evidence_relation": evidence, **metrics})
        if key == "LC001":
            _, legacy = calculate_project_cash_flow(reference, price)
            baseline_matches = (config["generation_mode"] == "legacy_constant_cf" and config["construction_years"] == 0
                and math.isclose(metrics["npv_eur"], legacy["npv_eur"], rel_tol=1e-10, abs_tol=1)
                and math.isclose(metrics["break_even_eur_2024_per_mwh"], legacy["lcoe_eur_per_mwh"], rel_tol=1e-10, abs_tol=1e-8))
    if not baseline_matches:
        raise ValueError("LC001 must retain the no-construction/no-replacement legacy special case")
    audit = {
        "status": "PASS_WITH_LIMITATIONS", "scenarios": len(summaries),
        "legacy_special_case_matches": baseline_matches,
        "price_year": 2024, "currency": "EUR", "discount_basis": "real_pre_tax_unlevered",
        "construction_timing": "Shares paid at t=0..C-1; COD=C; first annual operating receipts at C+1.",
        "replacement_timing": "Exact outage-start times; annual buckets retain component-specific discounting.",
        "limitations": [
            "Construction durations, spending shares and replacement costs are uncalibrated analyst scenarios, not Proxima budgets or schedules.",
            "Engineering cases interpret fixed/variable OPEX as routine expenses excluding separate major replacements; this allocation is not empirically established.",
            "Explicit operating windows replace the long-run CF loss; other downtime and load remain averaged within those windows.",
            "No extra debt-interest/IDC charge is added to the unlevered DCF. Financing, taxes, decommissioning, offline power purchases and terminal value remain excluded.",
            "LC003 zero replacement cost is a diagnostic; a delay case holds spending and other costs fixed and omits real delay overhead/overruns.",
            "No replacement is purchased at retirement; an outage starting earlier incurs full replacement cost even if its duration extends beyond retirement.",
        ],
    }
    nonempty_events = [table for table in events if not table.empty]
    event_table = (pd.concat(nonempty_events, ignore_index=True) if nonempty_events
                   else pd.DataFrame(columns=["scenario_id", *EVENT_COLUMNS]))
    return pd.DataFrame(summaries), pd.concat(annuals, ignore_index=True), event_table, audit


def reconciliation_check(root=ROOT):
    try:
        summary, annual, events, _ = build_lifecycle_results(root)
        for name, expected, keys in (
            ("lifecycle_summary.csv", summary, ["scenario_id"]),
            ("lifecycle_annual_cash_flows.csv", annual, ["scenario_id", "model_year"]),
            ("lifecycle_replacement_events.csv", events, ["scenario_id", "replacement_index"]),
        ):
            compare_table(pd.read_csv(Path(root) / "reports" / name), expected, keys)
        return True, "All lifecycle summaries, annual flows and exact replacement events match current inputs; LC001 reproduces legacy economics."
    except (OSError, ValueError, KeyError, AssertionError, TypeError) as exc:
        return False, str(exc)[:700]


def main():
    reports = ROOT / "reports"
    reports.mkdir(exist_ok=True)
    try:
        summary, annual, events, audit = build_lifecycle_results()
        summary.to_csv(reports / "lifecycle_summary.csv", index=False)
        annual.to_csv(reports / "lifecycle_annual_cash_flows.csv", index=False)
        events.to_csv(reports / "lifecycle_replacement_events.csv", index=False)
        write_json(reports / "lifecycle_audit.json", audit)
        lines = ["# Construction and Replacement Cash Flows", "", "Status: " + audit["status"], "",
                 "| Case | Construction years | Replacements | NPV billion EUR_2024 | Break-even EUR_2024/MWh |",
                 "|---|---:|---:|---:|---:|"]
        for row in summary.to_dict("records"):
            lines.append(f"| {row['scenario_id']} | {row['construction_years']} | {row['replacement_count']} | {row['npv_eur']/1e9:.3f} | {row['break_even_eur_2024_per_mwh']:.2f} |")
        lines += ["", "LC001 reproduces the original simplified model; other cases change the declared model boundary.",
                  "", audit["construction_timing"], "", audit["replacement_timing"], "", "## Limitations", ""]
        lines += ["- " + value for value in audit["limitations"]]
        (reports / "lifecycle_audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(summary["scenario_id"], summary["break_even_eur_2024_per_mwh"])
        ax.set_ylabel("Break-even constant real sale price (2024 EUR/MWh)")
        ax.set_title("Conditional construction and replacement scenarios")
        fig.tight_layout()
        fig.savefig(reports / "lifecycle_break_even.png", dpi=180, bbox_inches="tight")
        plt.close(fig)
        print("Lifecycle cash flow: " + audit["status"])
        print(f"Cases: {len(summary)} | Legacy special case matches: {audit['legacy_special_case_matches']}")
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        write_json(reports / "lifecycle_audit.json", {"status": "FAIL", "error": str(exc)})
        print("Lifecycle cash flow: FAIL — " + str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
