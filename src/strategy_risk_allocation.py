"""Stage 6.3: hypothetical present-value risk allocation around Stage 6.2.

NOT debt modeling, contractual valuation or a probability model. All monetary
calculations use the existing authoritative lifecycle function, including the
exact fractional-time discounting of major replacements. Contractual shares
allocate *changes* in project NPV, not new physical resources.
"""
from __future__ import annotations
import copy
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from lifecycle_cash_flow import calculate_lifecycle
from strategy_value_capture import ROOT, DATA, REPORTS, PRICE_CASES, allocate, inputs, read_scenarios

STRESS_IDS = {"RS00", "RS01", "RS02", "RS03", "RS04"}
STRESS_COLS = {"stress_id", "stress_name", "capex_multiplier", "additional_cod_delay_years",
               "electricity_price_multiplier", "assumption_class", "notes"}
RISK_COLS = {"strategy_id", "capex_overrun_company_share", "cod_delay_company_share",
             "electricity_price_shortfall_company_share", "assumption_class", "notes"}


def read_risk_inputs(root=ROOT):
    root = Path(root)
    risk = pd.read_csv(root / "data/strategy_risk_allocation.csv")
    stress = pd.read_csv(root / "data/strategy_risk_stress_cases.csv")
    if set(risk.columns) != RISK_COLS or set(stress.columns) != STRESS_COLS:
        raise ValueError("Unexpected or missing Stage 6.3 CSV fields")
    if len(risk) != 4 or set(risk.strategy_id) != {"STR01", "STR02", "STR03", "STR04"}:
        raise ValueError("Risk file must contain exactly four unique strategies")
    if len(stress) != 5 or set(stress.stress_id) != STRESS_IDS:
        raise ValueError("Stress file must contain exactly five unique stress cases")
    if risk.isna().any().any() or stress.isna().any().any():
        raise ValueError("Missing values")
    if (risk.assumption_class != "analyst_scenario").any() or (stress.assumption_class != "analyst_scenario").any():
        raise ValueError("All assumptions must be explicitly exploratory")
    for col in ["capex_overrun_company_share", "cod_delay_company_share", "electricity_price_shortfall_company_share"]:
        if not np.isfinite(risk[col]).all() or not risk[col].between(0, 1).all():
            raise ValueError("Risk shares must lie within [0,1]: " + col)
    if not np.isfinite(stress[["capex_multiplier", "electricity_price_multiplier", "additional_cod_delay_years"]].to_numpy()).all():
        raise ValueError("Stress parameters must be finite")
    if (stress.capex_multiplier < 1).any() or (stress.electricity_price_multiplier <= 0).any() or (stress.electricity_price_multiplier > 1).any():
        raise ValueError("Stress factors violate defined stress boundaries")
    if (stress.additional_cod_delay_years < 0).any() or not (stress.additional_cod_delay_years % 1 == 0).all():
        raise ValueError("COD delays must be nonnegative integers")
    return risk, stress


def stressed_lifecycle(reference, engineering, base_config, price, capex_mult=1.0, delay=0, price_mult=1.0):
    case = dict(reference)
    case["capex_eur_million"] = float(case["capex_eur_million"]) * float(capex_mult)
    config = copy.deepcopy(base_config)
    # Keep initial construction spending dates unchanged; postpone commercial
    # operation and all later operating/replacement events by padding zeros.
    delay = int(delay)
    config["construction_years"] += delay
    config["construction_spend_shares"] = list(config["construction_spend_shares"]) + [0.0] * delay
    cash, _, metrics = calculate_lifecycle(case, float(price) * float(price_mult), config, engineering)
    return cash, float(metrics["npv_eur"]), metrics


def evaluate(root=ROOT):
    risk, stresses = read_risk_inputs(root)
    strategies = read_scenarios(root)
    reference, engineering, config = inputs(root)
    risk_lookup = risk.set_index("strategy_id").to_dict("index")
    results = []
    for price_id, price in PRICE_CASES.items():
        base_cash, base_npv, base_metrics = stressed_lifecycle(reference, engineering, config, price)
        for strategy in strategies.to_dict("records"):
            sid = strategy["strategy_id"]
            shares = risk_lookup[sid]
            base_ledger = allocate(base_cash, reference["real_discount_rate"], strategy)
            company_base = float(base_ledger.pv_company_cash_eur.sum())
            partner_base = float(base_ledger.pv_external_partner_cash_eur.sum())
            incremental_company_cost = float(base_ledger.pv_company_incremental_cost_eur.sum())
            assert math.isclose(company_base + partner_base, base_npv - incremental_company_cost, abs_tol=0.05)
            for stress in stresses.to_dict("records"):
                capex = float(stress["capex_multiplier"])
                delay = int(stress["additional_cod_delay_years"])
                price_multiplier = float(stress["electricity_price_multiplier"])
                # Sequential decomposition gives additive increments that exactly
                # reconcile to the FULL combined stress; ordering is a convention.
                _, npv_capex, _ = stressed_lifecycle(reference, engineering, config, price, capex_mult=capex)
                _, npv_delay, _ = stressed_lifecycle(reference, engineering, config, price, capex_mult=capex, delay=delay)
                _, npv_total, metrics = stressed_lifecycle(reference, engineering, config, price,
                                                            capex_mult=capex, delay=delay, price_mult=price_multiplier)
                d_capex = npv_capex - base_npv
                d_delay = npv_delay - npv_capex
                d_price = npv_total - npv_delay
                company_delta = (float(shares["capex_overrun_company_share"]) * d_capex
                                 + float(shares["cod_delay_company_share"]) * d_delay
                                 + float(shares["electricity_price_shortfall_company_share"]) * d_price)
                company = company_base + company_delta
                partner = partner_base + (npv_total - base_npv - company_delta)
                expected = npv_total - incremental_company_cost
                if not math.isclose(company + partner, expected, abs_tol=0.10):
                    raise AssertionError("Present value conservation failure")
                if stress["stress_id"] == "RS00" and not math.isclose(company, company_base, abs_tol=0.10):
                    raise AssertionError("Stage 6.2 baseline reconciliation failed")
                results.append({
                    "strategy_id": sid, "price_case": price_id, "stress_id": stress["stress_id"],
                    "electricity_price_eur_per_mwh": price,
                    "baseline_project_npv_eur": base_npv, "stressed_project_npv_eur": npv_total,
                    "project_npv_change_eur": npv_total - base_npv,
                    "company_baseline_npv_eur": company_base, "company_stressed_npv_eur": company,
                    "company_npv_change_eur": company_delta,
                    "external_baseline_npv_eur": partner_base, "external_stressed_npv_eur": partner,
                    "external_npv_change_eur": partner - partner_base,
                    "incremental_company_cost_pv_eur": incremental_company_cost,
                    "capex_contribution_to_project_npv_eur": d_capex,
                    "delay_contribution_to_project_npv_eur": d_delay,
                    "price_contribution_to_project_npv_eur": d_price,
                    "capex_risk_company_share": float(shares["capex_overrun_company_share"]),
                    "delay_risk_company_share": float(shares["cod_delay_company_share"]),
                    "price_risk_company_share": float(shares["electricity_price_shortfall_company_share"]),
                    "first_revenue_model_year": metrics["first_revenue_model_year"],
                    "model_status": "HYPOTHETICAL_CONTRACT_RISK_ALLOCATION_NO_DEBT"
                })
    result = pd.DataFrame(results)
    if len(result) != 60:
        raise AssertionError("Expected 4 strategies x 3 prices x 5 stresses")
    return result


def main():
    REPORTS.mkdir(exist_ok=True)
    results = evaluate()
    p = REPORTS / "stage63_risk_allocation_results.csv"
    results.to_csv(p, index=False)
    files = [DATA / "strategy_risk_allocation.csv", DATA / "strategy_risk_stress_cases.csv",
             DATA / "strategy_value_capture_scenarios.csv", DATA / "lifecycle_cash_flow_cases.json",
             DATA / "engineering_generation_cases.csv", DATA / "lcoe_scenarios_stage42.csv"]
    audit = {
        "status": "PASS_WITH_HYPOTHETICAL_RISK_ALLOCATION_LIMITATIONS",
        "result_rows": len(results), "strategies": 4, "price_cases": 3, "stress_cases": 5,
        "reconciliation": "company plus external partner NPV equals stressed lifecycle project NPV less unchanged company setup/overhead PV",
        "source_sha256": {str(f.relative_to(ROOT)): hashlib.sha256(f.read_bytes()).hexdigest() for f in files},
        "limitations": [
            "Illustrative risk-sharing percentages are not actual Proxima contracts or published financing terms.",
            "NPV-level contractual allocation, not annual cash transfer ledger, debt financing, taxes, guarantees valuation or probability model.",
            "Supplier margins and company overhead remain fixed at the Stage 6.2 reference allocation when stresses occur.",
            "A two-year COD delay retains original construction spend dates and shifts operating and replacement timelines.",
            "Stress decomposition uses ordered CAPEX then delay then price effects; attribution would differ under another ordering.",
            "Major replacement cost amount stays fixed under initial CAPEX overrun; no extra cost inflation or new capex financing.",
            "Only GEN002 and LC004 are used; risk shares are diagnostic scenario parameters, not strategy rankings.",
        ]
    }
    (REPORTS / "stage63_risk_allocation_audit.json").write_text(json.dumps(audit, indent=2) + "\n")
    reference = results[(results.price_case == "P170") & (results.stress_id == "RS04")].copy()
    reference["company_npv_change_eur_bn"] = reference.company_npv_change_eur / 1e9
    print("Stage 6.3:", audit["status"])
    print("60 scenarios saved:", p.name)
    print("Combined stress at EUR 170/MWh; company NPV change in EUR billion:")
    print(reference[["strategy_id", "company_npv_change_eur_bn", "stressed_project_npv_eur"]].to_string(index=False))


if __name__ == "__main__":
    main()
