"""Stage 6.2 independent output and negative-test validation."""
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

from strategy_value_capture import ROOT, REPORTS, calculate_results, read_scenarios


def main():
    summary_path = REPORTS / "stage62_value_capture_results.csv"
    ledger_path = REPORTS / "stage62_stakeholder_cash_flows.csv"
    audit_path = REPORTS / "stage62_value_capture_audit.json"
    for p in (summary_path, ledger_path, audit_path):
        if not p.exists():
            raise FileNotFoundError(f"Run the model first: {p}")
    summary = pd.read_csv(summary_path)
    ledger = pd.read_csv(ledger_path)
    audit = json.loads(audit_path.read_text())
    assert audit["status"] == "PASS_WITH_EXPLORATORY_LIMITATIONS"
    assert len(summary) == 12 and summary[["strategy_id", "price_case"]].drop_duplicates().shape[0] == 12
    assert set(summary.strategy_id) == {"STR01", "STR02", "STR03", "STR04"}
    assert set(summary.price_case) == {"P120", "P170", "P200"}
    assert np.isfinite(summary.select_dtypes(include="number").to_numpy()).all()
    # Annual conservation must hold, including initial construction years.
    assert np.allclose(ledger.consolidated_cash_eur, ledger.expected_consolidated_eur, atol=0.002, rtol=1e-12)
    # Exact benchmark: costs and invoices are absent for STR01; equity share = 1.
    baseline = summary[summary.strategy_id == "STR01"]
    assert np.all(baseline.company_ownership_share == 1.0)
    assert np.all(baseline.company_supplier_margin_pv_eur.abs() < 0.01)
    # Repeat calculation to catch stale reports and compare numeric columns.
    expected, expected_ledger = calculate_results()
    numeric = list(expected.select_dtypes(include="number").columns)
    got = summary.sort_values(["strategy_id", "price_case"]).reset_index(drop=True)
    expected = expected.sort_values(["strategy_id", "price_case"]).reset_index(drop=True)
    assert np.allclose(got[numeric], expected[numeric], atol=0.05, rtol=1e-11)
    assert len(ledger) == len(expected_ledger)
    for rel, digest in audit["source_sha256"].items():
        if hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() != digest:
            raise AssertionError("Input has changed since output generation: " + rel)
    # Every price has one consolidated identity per strategy.
    for r in summary.itertuples():
        assert math.isclose(r.company_npv_eur + r.external_partner_npv_eur,
                            r.baseline_project_npv_eur - r.incremental_real_cost_pv_eur,
                            abs_tol=0.05)
    print("PASS — 4 strategies × 3 prices = 12 scenarios")
    print("PASS — annual/discounted transfers, NPV reconciliation, input hashes, and regeneration")
    print("WARNING — This is a hypothetical value-allocation model, not company valuation or strategy ranking")


if __name__ == "__main__":
    main()
