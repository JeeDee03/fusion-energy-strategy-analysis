"""Stage 6.2: experimental developer/owner cash-flow partition, EUR_2024.

The supplier production scope is ALREADY inside baseline construction CAPEX.
We carve that production expenditure out of the owner account, give it to the
supplier, and then charge the owner the supplier invoice incl. markup on the
same construction-spend dates. No production cost is duplicated.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

from engineering_generation import build_generation_results
from lifecycle_cash_flow import calculate_lifecycle
from project_cash_flow import load_reference_case

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
STRATEGY_IDS = {"STR01", "STR02", "STR03", "STR04"}
PRICE_CASES = {"P120": 120.0, "P170": 170.0, "P200": 200.0}


def read_scenarios(root=ROOT):
    df = pd.read_csv(Path(root) / "data/strategy_value_capture_scenarios.csv")
    fields = {"strategy_id", "equity_fraction", "supplier_scope_share_of_baseline_capex",
              "supplier_markup_fraction", "upfront_company_setup_eur_million",
              "annual_company_overhead_eur_million", "assumption_class", "notes"}
    if set(df.columns) != fields or set(df.strategy_id) != STRATEGY_IDS or len(df) != 4:
        raise ValueError("Expected exactly STR01–STR04 and documented scenario columns")
    if df.isna().any().any() or (df.assumption_class != "analyst_scenario").any():
        raise ValueError("Missing data or unsupported evidence status")
    for col in ("equity_fraction", "supplier_scope_share_of_baseline_capex"):
        if not np.isfinite(df[col]).all() or not df[col].between(0, 1).all():
            raise ValueError(f"{col} must be finite and in [0,1]")
    for col in ("supplier_markup_fraction", "upfront_company_setup_eur_million", "annual_company_overhead_eur_million"):
        if not np.isfinite(df[col]).all() or (df[col] < 0).any():
            raise ValueError(f"{col} must be finite and nonnegative")
    if df.notes.astype(str).str.strip().eq("").any():
        raise ValueError("Each strategy requires an assumption explanation")
    return df


def inputs(root=ROOT):
    root = Path(root)
    reference = load_reference_case()  # uses canonical repo ROOT
    generation, _ = build_generation_results(root)
    entry = generation[generation.scenario_id == "GEN002"]
    if len(entry) != 1:
        raise ValueError("GEN002 required")
    # build_generation_results includes input scenario fields
    engineering = entry.iloc[0].to_dict()
    lc = json.loads((root / "data/lifecycle_cash_flow_cases.json").read_text())
    match = [dict(x) for x in lc["cases"] if x["scenario_id"] == "LC004"]
    if len(match) != 1 or match[0]["generation_mode"] != "engineering_events":
        raise ValueError("LC004 engineering-event scenario required")
    if match[0]["engineering_case_id"] != "GEN002":
        raise ValueError("LC004 and GEN002 do not match")
    return reference, engineering, match[0]


def allocate(base_cash, rate, strategy):
    """Partition each UNDISCOUNTED annual cash flow; return annual stakeholder ledger.

    Conservation: owner cash + company cash = baseline project cash - real
    incremental company setup and overhead. The fee is an internal transfer.
    """
    s = float(strategy["supplier_scope_share_of_baseline_capex"])
    m = float(strategy["supplier_markup_fraction"])
    equity = float(strategy["equity_fraction"])
    upfront = 1e6 * float(strategy["upfront_company_setup_eur_million"])
    annual = 1e6 * float(strategy["annual_company_overhead_eur_million"])
    ledger = base_cash[["model_year", "operating_year", "construction_capex_eur", "cash_flow_eur"]].copy()
    # The supply scope is part of the existing baseline overnight CAPEX.
    ledger["supplier_production_cost_eur"] = s * ledger["construction_capex_eur"]
    ledger["supplier_invoice_eur"] = (1 + m) * ledger["supplier_production_cost_eur"]
    # Remove production costs from owner CAPEX then add supplier invoices.
    ledger["owner_project_cash_eur"] = (ledger["cash_flow_eur"]
                                         + ledger["supplier_production_cost_eur"]
                                         - ledger["supplier_invoice_eur"])
    ledger["company_equity_cash_eur"] = equity * ledger["owner_project_cash_eur"]
    ledger["external_equity_cash_eur"] = (1 - equity) * ledger["owner_project_cash_eur"]
    ledger["company_incremental_cost_eur"] = (ledger["model_year"].eq(0).astype(float) * upfront
                                             + ledger["operating_year"].gt(0).astype(float) * annual)
    ledger["company_supplier_cash_eur"] = (ledger["supplier_invoice_eur"]
                                           - ledger["supplier_production_cost_eur"])
    ledger["company_cash_eur"] = (ledger["company_equity_cash_eur"]
                                  + ledger["company_supplier_cash_eur"]
                                  - ledger["company_incremental_cost_eur"])
    ledger["external_partner_cash_eur"] = ledger["external_equity_cash_eur"]
    ledger["consolidated_cash_eur"] = ledger["company_cash_eur"] + ledger["external_partner_cash_eur"]
    ledger["expected_consolidated_eur"] = ledger["cash_flow_eur"] - ledger["company_incremental_cost_eur"]
    # Real annual allocation must reconcile BEFORE discounting.
    if not np.allclose(ledger["consolidated_cash_eur"], ledger["expected_consolidated_eur"], rtol=1e-12, atol=0.002):
        raise AssertionError("Cash transfer conservation failed")
    ledger["pv_factor"] = (1 + float(rate)) ** (-ledger["model_year"])
    # IMPORTANT: lifecycle replacement expenditure is discounted at the exact
    # outage time, which may be fractional; its annual cash-flow bucket is not.
    # Therefore we MUST reuse the authoritative lifecycle discounted CF rather
    # than rediscounting the annual cash_flow_eur with year-end factors.
    ledger["pv_cash_flow_eur"] = base_cash["discounted_cash_flow_eur"].to_numpy()
    owner_pv = (ledger["pv_cash_flow_eur"] +
                (ledger["supplier_production_cost_eur"] - ledger["supplier_invoice_eur"]) * ledger["pv_factor"])
    incremental_pv = ledger["company_incremental_cost_eur"] * ledger["pv_factor"]
    supplier_pv = ledger["company_supplier_cash_eur"] * ledger["pv_factor"]
    ledger["pv_company_cash_eur"] = equity * owner_pv + supplier_pv - incremental_pv
    ledger["pv_external_partner_cash_eur"] = (1 - equity) * owner_pv
    ledger["pv_consolidated_cash_eur"] = ledger["pv_company_cash_eur"] + ledger["pv_external_partner_cash_eur"]
    ledger["pv_company_incremental_cost_eur"] = incremental_pv
    if not np.allclose(ledger["pv_consolidated_cash_eur"], ledger["pv_cash_flow_eur"] - incremental_pv, rtol=1e-12, atol=0.002):
        raise AssertionError("Discounted allocation fails exact-event timing conservation")
    return ledger


def calculate_results(root=ROOT):
    root = Path(root)
    scenarios = read_scenarios(root)
    reference, engineering, lc = inputs(root)
    rows, ledger_frames = [], []
    for price_id, price in PRICE_CASES.items():
        base_cash, _, metrics = calculate_lifecycle(reference, price, lc, engineering)
        for strategy in scenarios.to_dict("records"):
            ledger = allocate(base_cash, reference["real_discount_rate"], strategy)
            npv_base = float(metrics["npv_eur"])
            npv_company = float(ledger["pv_company_cash_eur"].sum())
            npv_partner = float(ledger["pv_external_partner_cash_eur"].sum())
            real_cost_pv = float((ledger["company_incremental_cost_eur"] * ledger["pv_factor"]).sum())
            if not math.isclose(npv_company + npv_partner, npv_base - real_cost_pv, abs_tol=0.01):
                raise AssertionError("Discounted stakeholder value conservation failed")
            sid = strategy["strategy_id"]
            rows.append({
                "strategy_id": sid, "price_case": price_id, "electricity_price_eur_per_mwh": price,
                "baseline_project_npv_eur": npv_base,
                "company_npv_eur": npv_company, "external_partner_npv_eur": npv_partner,
                "consolidated_npv_eur": npv_company + npv_partner,
                "incremental_real_cost_pv_eur": real_cost_pv,
                "supplier_scope_share": strategy["supplier_scope_share_of_baseline_capex"],
                "supplier_markup_fraction": strategy["supplier_markup_fraction"],
                "company_ownership_share": strategy["equity_fraction"],
                "company_supplier_margin_pv_eur": float((ledger["company_supplier_cash_eur"] * ledger["pv_factor"]).sum()),
                "company_equity_cash_pv_eur": float((ledger["company_equity_cash_eur"] * ledger["pv_factor"]).sum()),
                "company_setup_overhead_pv_eur": real_cost_pv,
                "model_status": "EXPLORATORY_VALUE_ALLOCATION_ONLY",
            })
            ledger.insert(0, "strategy_id", sid)
            ledger.insert(1, "price_case", price_id)
            ledger_frames.append(ledger)
    return pd.DataFrame(rows), pd.concat(ledger_frames, ignore_index=True)


def main():
    REPORTS.mkdir(exist_ok=True)
    summary, ledger = calculate_results()
    summary.to_csv(REPORTS / "stage62_value_capture_results.csv", index=False)
    ledger.to_csv(REPORTS / "stage62_stakeholder_cash_flows.csv", index=False)
    files = [DATA / "strategy_value_capture_scenarios.csv", DATA / "lcoe_scenarios_stage42.csv",
             DATA / "lifecycle_cash_flow_cases.json", DATA / "engineering_generation_cases.csv"]
    audit = {
        "status": "PASS_WITH_EXPLORATORY_LIMITATIONS", "strategy_count": 4,
        "price_scenarios": 3, "result_rows": len(summary), "cash_flow_rows": len(ledger),
        "validation": "annual and discounted owner/supplier cash-flow conservation",
        "source_sha256": {str(f.relative_to(ROOT)): hashlib.sha256(f.read_bytes()).hexdigest() for f in files},
        "limitations": [
            "Supplier production cost is carved out from baseline CAPEX; fee markup is a transfer from plant owner to supplier.",
            "Company setup and overhead are incremental real costs; no real company financial statements or contract terms are inferred.",
            "Project hurdle rate is reused for company and investor discounting only as a diagnostic; no WACC/debt/tax modeling.",
            "Supplier and owner value should not be ranked across distinct business models without capital risk and contractual context.",
            "Company equity fraction is a simplified funding-and-cash-flow participation rule, not a modeled project-finance waterfall.",
            "Only GEN002/LC004/R05 is modeled; STR04 is not yet a true phased multi-project strategy.",
            "Revenue price scenarios are hypothetical, not commercial PPA evidence.",
        ]}
    (REPORTS / "stage62_value_capture_audit.json").write_text(json.dumps(audit, indent=2) + "\n")
    print("Stage 6.2:", audit["status"])
    print(summary[["strategy_id", "price_case", "company_npv_eur", "external_partner_npv_eur", "consolidated_npv_eur"]].to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
