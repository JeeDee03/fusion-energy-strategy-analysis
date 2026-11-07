
from pathlib import Path
import json

import numpy as np
import pandas as pd

from lcoe_model import calculate_lcoe
from stage4_reconciliation import reconciliation_checks
from validate_economic_assumptions import audit_assumptions
from engineering_generation import reconciliation_check as generation_reconciliation_check
from lifecycle_cash_flow import reconciliation_check as lifecycle_reconciliation_check
from company_comparison import reconciliation_check as company_reconciliation_check
from project_cash_flow import (
    calculate_project_cash_flow,
    load_reference_case,
)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

TOL = 1e-6
checks = []
warnings = []


def record_check(name, condition, detail):
    passed = bool(condition)
    checks.append({
        "check": name,
        "status": "PASS" if passed else "FAIL",
        "detail": detail,
    })


def require_csv(filename, required_columns):
    path = REPORTS / filename

    if not path.exists():
        raise FileNotFoundError(
            f"Missing {path}. Run its Stage 4 script first."
        )

    df = pd.read_csv(path)

    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(
            f"{filename} missing: {sorted(missing)}"
        )

    return df


def main():
    checks.clear()
    warnings.clear()
    assumptions = audit_assumptions(ROOT)
    record_check("Economic assumption traceability and model basis", not assumptions["errors"],
                 assumptions["status"] + (": " + "; ".join(assumptions["errors"]) if assumptions["errors"] else
                 "; mathematical traceability only; research gaps retained."))
    engineering_passed, engineering_detail = generation_reconciliation_check(ROOT)
    record_check("Conditional engineering generation cases", engineering_passed, engineering_detail)
    lifecycle_passed, lifecycle_detail = lifecycle_reconciliation_check(ROOT)
    record_check("Construction and replacement cash-flow reconciliation", lifecycle_passed, lifecycle_detail)
    company_passed, company_detail = company_reconciliation_check(ROOT)
    record_check("Comparable company evidence and business profiles", company_passed, company_detail)
    for name, passed, detail in reconciliation_checks(ROOT):
        record_check(name, passed, detail)

    # ------------------------------------
    # 1. Load all relevant model outputs
    # ------------------------------------

    stage42 = require_csv(
        "stage42_lcoe_scenarios.csv",
        [
            "scenario_id",
            "capex_eur_per_kwe",
            "lcoe_eur_per_mwh",
        ],
    )

    stage43 = require_csv(
        "stage43_performance_sensitivity.csv",
        [
            "scenario_id",
            "capacity_factor",
            "lcoe_eur_per_mwh",
        ],
    )

    stage44 = require_csv(
        "stage44_learning_results.csv",
        [
            "scenario_id",
            "cumulative_equivalent_units",
            "total_capex_eur_million",
            "lcoe_eur_per_mwh",
        ],
    )

    stage45 = require_csv(
        "stage45_npv_summary.csv",
        [
            "scenario_id",
            "electricity_price_eur_per_mwh",
            "npv_eur",
            "break_even_price_eur_per_mwh",
        ],
    )

    case = load_reference_case()

    if case["scenario_id"] != "CAL002":
        raise ValueError("Wrong reference scenario")

    reference_lcoe = float(
        calculate_lcoe(case)["lcoe_eur_per_mwh"]
    )

    # ------------------------------------
    # 2. Stage 4.2 consistency
    # ------------------------------------

    stage42_ref = stage42[
        stage42["scenario_id"] == "CAL002"
    ]

    record_check(
        "Stage 4.2 reference is unique",
        len(stage42_ref) == 1,
        "CAL002 must occur exactly once.",
    )

    if len(stage42_ref) == 1:
        record_check(
            "Stage 4.2 LCOE reconciliation",
            np.isclose(
                stage42_ref.iloc[0]["lcoe_eur_per_mwh"],
                reference_lcoe,
                atol=TOL,
            ),
            "Stage 4.2 must agree with shared LCOE.",
        )

    # ------------------------------------
    # 3. Stage 4.3 consistency
    # ------------------------------------

    performance_ref = stage43[
        (stage43["scenario_id"] == "CAL002")
        & np.isclose(
            stage43["capacity_factor"],
            float(case["capacity_factor"]),
        )
    ]

    record_check(
        "Stage 4.3 reference is unique",
        len(performance_ref) == 1,
        "Same CAPEX and CF as CAL002.",
    )

    if len(performance_ref) == 1:
        record_check(
            "Stage 4.3 LCOE reconciliation",
            np.isclose(
                performance_ref.iloc[0]["lcoe_eur_per_mwh"],
                reference_lcoe,
                atol=TOL,
            ),
            "Performance baseline matches CAL002.",
        )

    # ------------------------------------
    # 4. Stage 4.4 consistency
    # ------------------------------------

    first_units = stage44[
        stage44["cumulative_equivalent_units"] == 1
    ]

    record_check(
        "Stage 4.4 starts at baseline CAPEX",
        not first_units.empty
        and np.allclose(
            first_units["total_capex_eur_million"],
            float(case["capex_eur_million"]),
            atol=TOL,
        ),
        "At N=1, no manufacturing learning yet.",
    )

    record_check(
        "Stage 4.4 starts at baseline LCOE",
        not first_units.empty
        and np.allclose(
            first_units["lcoe_eur_per_mwh"],
            reference_lcoe,
            atol=TOL,
        ),
        "At N=1, all learning cases match CAL002.",
    )

    # ------------------------------------
    # 5. Stage 4.5 consistency
    # ------------------------------------

    record_check(
        "Stage 4.5 break-even price equals LCOE",
        not stage45.empty
        and np.allclose(
            stage45["break_even_price_eur_per_mwh"],
            reference_lcoe,
            atol=TOL,
        ),
        "Only valid under common model boundaries.",
    )

    _, break_even = calculate_project_cash_flow(
        case, reference_lcoe
    )

    record_check(
        "NPV equals zero at break-even price",
        abs(break_even["npv_eur"]) < 1.0,
        "NPV at LCOE should be approximately zero.",
    )

    # Verify each reported NPV using current model
    recalculated_npvs = [
        calculate_project_cash_flow(
            case,
            row["electricity_price_eur_per_mwh"],
        )[1]["npv_eur"]
        for _, row in stage45.iterrows()
    ]

    record_check(
        "Stage 4.5 NPVs reproduce",
        np.allclose(
            stage45["npv_eur"],
            recalculated_npvs,
            rtol=1e-10,
            atol=1.0,
        ),
        "Exported values match current DCF code.",
    )

    # ------------------------------------
    # 6. Evidence and modeling limitations
    # ------------------------------------

    warnings.extend([
        "Economic scenarios remain analyst assumptions.",
        "Reference 1000 MWe is not verified Stellaris net output.",
        "FOAK/NOAK CAPEX not empirically calibrated.",
        "Legacy model omits construction timing. Lifecycle extension includes staged investment/late revenue in a real unlevered DCF, without an extra debt-interest/IDC charge.",
        "Lifecycle extension includes explicit major replacement events/costs under analyst assumptions. Legacy tables omit them; decommissioning remains excluded.",
        "Legacy performance sensitivities are independent algebraic tests; new engineering cases provide only conditional maintenance/load consistency, not reliability validation.",
        "Magnet learning rates and CAPEX share are hypothetical.",
        "2024 German electricity prices are not forecasts.",
        "Annual model uses a 8760-hour normalized year; "
        "2024 historical market data contains 8784 hours.",
        "H1, H2, and H3 are not empirically confirmed.",
    ])

    # ------------------------------------
    # 7. Build integrated summary
    # ------------------------------------

    rows = []

    def add(stage, metric, value, unit, classification):
        rows.append({
            "stage": stage,
            "metric": metric,
            "value": float(value),
            "unit": unit,
            "classification": classification,
        })

    add(
        "4.2", "Reference CAPEX",
        case["capex_eur_million"],
        "EUR million", "analyst_scenario"
    )

    add(
        "4.2", "Reference LCOE",
        reference_lcoe,
        "EUR/MWh", "conditional_model_output"
    )

    add(
        "4.3", "Performance combinations",
        len(stage43),
        "count", "model_coverage"
    )

    add(
        "4.3", "Minimum modeled LCOE",
        stage43["lcoe_eur_per_mwh"].min(),
        "EUR/MWh", "conditional_model_output"
    )

    add(
        "4.3", "Maximum modeled LCOE",
        stage43["lcoe_eur_per_mwh"].max(),
        "EUR/MWh", "conditional_model_output"
    )

    add(
        "4.4", "Minimum learned CAPEX",
        stage44["total_capex_eur_million"].min(),
        "EUR million", "conditional_model_output"
    )

    add(
        "4.4", "Minimum learning-case LCOE",
        stage44["lcoe_eur_per_mwh"].min(),
        "EUR/MWh", "conditional_model_output"
    )

    add(
        "4.5", "Break-even sale price",
        reference_lcoe,
        "EUR/MWh", "conditional_model_output"
    )

    add(
        "4.5", "Minimum modeled NPV",
        stage45["npv_eur"].min() / 1e9,
        "EUR billion", "conditional_model_output"
    )

    add(
        "4.5", "Maximum modeled NPV",
        stage45["npv_eur"].max() / 1e9,
        "EUR billion", "conditional_model_output"
    )

    summary = pd.DataFrame(rows)
    summary.to_csv(
        REPORTS / "stage4_integrated_summary.csv",
        index=False,
    )

    # ------------------------------------
    # 8. Write integration audit
    # ------------------------------------

    failed = [c for c in checks if c["status"] == "FAIL"]

    audit = {
        "stage": "4",
        "status": (
            "PASS_WITH_LIMITATIONS" if not failed else "FAIL"
        ),
        "economic_model_basis": assumptions["model_basis"],
        "assumption_register_status": assumptions["status"],
        "reference_scenario": "CAL002",
        "reference_lcoe_eur_per_mwh": reference_lcoe,
        "checks": checks,
        "limitations": warnings,
        "interpretation": (
            "Internal consistency only; not independent "
            "validation of engineering or commercial assumptions."
        ),
    }

    json_path = REPORTS / "stage4_integration_audit.json"

    json_path.write_text(
        json.dumps(audit, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# Stage 4 — Integration Audit",
        "",
        f"**Status:** {audit['status']}",
        "",
        f"**Reference:** CAL002",
        "",
        f"**Reference LCOE:** {reference_lcoe:.2f} EUR_2024/MWh",
        "",
        "Monetary model outputs use 2024 constant EUR by analyst convention; this is not empirical cost calibration.",
        "",
        "## Reconciliation Checks",
        "",
    ]

    for check in checks:
        lines.append(
            f"- **{check['status']}** — {check['check']}: "
            f"{check['detail']}"
        )

    lines += [
        "",
        "## Evidence Limitations",
        "",
    ]

    lines += [f"- {item}" for item in warnings]

    lines += [
        "",
        "## Conclusion",
        "",
        "Passing checks establish cross-model mathematical "
        "consistency, not commercial feasibility or "
        "independent factual verification.",
    ]

    (REPORTS / "stage4_integration_audit.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    # ------------------------------------
    # 9. Print result and fail if needed
    # ------------------------------------

    print("\nSTAGE 4 INTEGRATION REVIEW")
    print("--------------------------")
    print(f"Reference LCOE: EUR {reference_lcoe:.2f}/MWh")
    print(f"Checks passed: {len(checks) - len(failed)}")
    print(f"Checks failed: {len(failed)}")
    print(f"Status: {audit['status']}")

    print("\nGenerated:")
    print("reports/stage4_integrated_summary.csv")
    print("reports/stage4_integration_audit.json")
    print("reports/stage4_integration_audit.md")

    if failed:
        raise RuntimeError(
            "Stage 4 integration failed. Review audit."
        )


if __name__ == "__main__":
    main()
