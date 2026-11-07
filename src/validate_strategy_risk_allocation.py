"""Stage 6.3 independent re-evaluation and risk transfer sanity checks."""
import hashlib
import json
import math
import numpy as np
import pandas as pd
from strategy_risk_allocation import ROOT, REPORTS, evaluate, read_risk_inputs
from strategy_value_capture import calculate_results


def main():
    path = REPORTS / "stage63_risk_allocation_results.csv"
    audit_path = REPORTS / "stage63_risk_allocation_audit.json"
    if not path.exists() or not audit_path.exists():
        raise FileNotFoundError("Run python src/strategy_risk_allocation.py first")
    got = pd.read_csv(path).sort_values(["strategy_id", "price_case", "stress_id"]).reset_index(drop=True)
    expected = evaluate().sort_values(["strategy_id", "price_case", "stress_id"]).reset_index(drop=True)
    assert len(got) == len(expected) == 60
    assert got[["strategy_id", "price_case", "stress_id"]].equals(expected[["strategy_id", "price_case", "stress_id"]])
    numeric = expected.select_dtypes(include="number").columns
    assert np.isfinite(got[numeric].to_numpy()).all()
    assert np.allclose(got[numeric].to_numpy(), expected[numeric].to_numpy(), atol=0.1, rtol=1e-11)
    assert np.allclose(got.company_stressed_npv_eur + got.external_stressed_npv_eur,
                       got.stressed_project_npv_eur - got.incremental_company_cost_pv_eur,
                       atol=0.1, rtol=1e-11)
    assert np.allclose(got.capex_contribution_to_project_npv_eur + got.delay_contribution_to_project_npv_eur + got.price_contribution_to_project_npv_eur,
                       got.project_npv_change_eur, atol=0.1, rtol=1e-11)
    # Reconciliation to the actual Stage 6.2 model in each price case.
    original, _ = calculate_results()
    base = got[got.stress_id == "RS00"]
    for r in base.itertuples():
        orig = original[(original.strategy_id == r.strategy_id) & (original.price_case == r.price_case)].iloc[0]
        assert math.isclose(r.company_stressed_npv_eur, orig.company_npv_eur, abs_tol=.1)
        assert math.isclose(r.external_stressed_npv_eur, orig.external_partner_npv_eur, abs_tol=.1)
    assert (got[got.stress_id == "RS00"].project_npv_change_eur.abs() < 0.1).all()
    assert (got[got.stress_id == "RS01"].project_npv_change_eur < 0).all()
    assert (got[got.stress_id == "RS03"].project_npv_change_eur < 0).all()
    risk, stress = read_risk_inputs()
    assert len(risk) == 4 and len(stress) == 5
    audit = json.loads(audit_path.read_text())
    assert audit["status"] == "PASS_WITH_HYPOTHETICAL_RISK_ALLOCATION_LIMITATIONS"
    for rel, digest in audit["source_sha256"].items():
        assert hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() == digest, rel
    print("PASS — 60 stress scenarios and exact Stage 6.2 baseline reconciliation")
    print("PASS — stakeholder NPV conservation, sequential stress attribution, hashes, regeneration")
    print("WARNING — Hypothetical contractual risk shares, no debt or empirical financing benefits")


if __name__ == "__main__":
    main()
