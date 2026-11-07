"""Declared file boundaries and freshness checks for the Stage 3–4 rebuild."""

from datetime import datetime, timezone
from hashlib import sha256
from importlib import metadata
import json
import os
from pathlib import Path
import platform
import tempfile

ROOT = Path(__file__).resolve().parent.parent
SUMMARY = "reports/stage34_run_summary.json"
PACKAGES = ("pandas", "numpy", "matplotlib")
STEPS = (
    "validate_economic_assumptions.py",
    "validate_technical_data.py", "company_comparison.py", "engineering_tradeoffs.py",
    "maintenance_analysis.py", "engineering_generation.py", "build_economic_input_register.py",
    "check_stage3_closure.py", "technology_maturity_analysis.py",
    "lcoe_model.py", "validate_lcoe_model.py", "cost_calibration_analysis.py",
    "performance_sensitivity.py", "validate_performance_sensitivity.py",
    "manufacturing_learning.py", "validate_manufacturing_learning.py",
    "project_cash_flow.py", "validate_project_cash_flow.py",
    "plot_project_cash_flow.py", "lifecycle_cash_flow.py", "integrate_stage4.py", "research_consistency.py", "validate_uncertainty_spec.py",
)
INPUTS = tuple("data/" + name for name in (
    "companies.csv", "sources.csv", "reactor_designs.csv",
    "technical_parameters.csv", "engineering_subsystems.csv", "milestones.csv",
    "lcoe_scenarios.csv", "fusion_cost_benchmarks.csv",
    "lcoe_scenarios_stage42.csv", "lcoe_performance_scenarios.csv",
    "manufacturing_learning_scenarios.csv", "electricity_revenue_scenarios.csv",
)) + ("reports/milestone_review.csv", "requirements.txt",
      "data/economic_assumptions.csv", "data/economic_reference_notes.csv",
      "data/economic_model_basis.json", "data/electricity_summary_2024.json",
      "data/engineering_generation_cases.csv", "data/lifecycle_cash_flow_cases.json",
      "data/company_business_profiles.csv", "data/company_comparison_claims.csv",
      "data/competitive_sources.csv", "data/research_status.json",
      "data/research_findings.json", "data/stage5_uncertainty_spec.json", "README.md",
      "research/01_research_proposal.md", "research/05_analysis_protocol.md",
      "research/25_stage4_techno_economic_synthesis.md",
      "research/31_research_status_and_claims.md")
OUTPUTS = (
    "reports/stage5_spec_audit.json",
    "reports/stage5_spec_audit.md",
    "reports/stage5_design_dry_run.csv",
    "reports/research_consistency_audit.json",
    "reports/research_consistency_summary.md",
    "reports/company_comparison.csv",
    "reports/company_comparison_matrix.csv",
    "reports/company_comparison.md",
    "reports/company_comparison_audit.json",
    "reports/lifecycle_summary.csv",
    "reports/lifecycle_annual_cash_flows.csv",
    "reports/lifecycle_replacement_events.csv",
    "reports/lifecycle_audit.json",
    "reports/lifecycle_audit.md",
    "reports/lifecycle_break_even.png",
    "reports/engineering_generation_scenarios.csv",
    "reports/engineering_generation_audit.json",
    "reports/engineering_generation_audit.md",
    "reports/engineering_generation_capacity_factors.png",
    "reports/economic_assumption_audit.json",
    "reports/economic_assumption_audit.md",
    "data/economic_input_register.csv",
    "reports/stage3_engineering_evidence.csv",
    "reports/maintenance_availability_scenarios.csv",
    "reports/maintenance_availability_scenarios.png",
    "reports/maintenance_availability.png",
    "reports/technology_evidence_coverage.csv",
    "reports/technology_milestone_status.csv",
    "reports/technology_evidence_coverage.png",
    "reports/stage3_closure_audit.md",
    "reports/stage4_lcoe_test_results.csv",
    "reports/stage42_lcoe_scenarios.csv",
    "reports/stage42_capex_sensitivity.png",
    "reports/stage43_performance_sensitivity.csv",
    "reports/stage43_break_even_capacity_factor.csv",
    "reports/stage43_net_power_sensitivity.csv",
    "reports/stage43_lcoe_heatmap.png",
    "reports/stage44_learning_results.csv",
    "reports/stage44_capex_learning.png",
    "reports/stage44_lcoe_learning.png",
    "reports/stage45_npv_summary.csv",
    "reports/stage45_annual_cash_flows.csv",
    "reports/stage45_npv_comparison.png",
    "reports/stage45_cumulative_cash_flow.png",
    "reports/stage4_integrated_summary.csv",
    "reports/stage4_integration_audit.json",
    "reports/stage4_integration_audit.md",
)


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def input_paths(root=ROOT):
    # Conservatively track all top-level analysis scripts, including shared helpers.
    # Discover editorial files at call time, after the safe numbering migration.
    # Caching this glob at import time would retain a renamed-away legacy path.
    docs = {str(p.relative_to(root)) for p in (root / "research").glob("*.md")
            if p.name not in {"02_market_data_summary.md", "11_stage12_synthesis.md"}}
    return sorted(set(INPUTS) | docs |
                  {str(p.relative_to(root)) for p in (root / "src").glob("*.py")})


def hashes(root, paths):
    return {name: digest(root / name) for name in paths}


def environment():
    return {"python": platform.python_version(),
            "packages": {name: metadata.version(name) for name in PACKAGES}}


def check_review_alignment(root=ROOT):
    """Require reviewed evidence to match its source, without writing reviews."""
    from prepare_milestone_review import read_table, index_rows, same_value
    fields, milestones = read_table(root / "data/milestones.csv",
                                    {"milestone_id", "company_id", "source_id"})
    _, reviewed = read_table(root / "reports/milestone_review.csv", fields)
    original = index_rows(milestones, "milestone_id", "milestones.csv")
    reviews = index_rows(reviewed, "milestone_id", "milestone_review.csv")
    if set(original) != set(reviews):
        raise ValueError("Milestone review coverage differs from inputs. Prepare and review new records first.")
    for key, row in original.items():
        changed = [field for field in fields if not same_value(row[field], reviews[key][field])]
        if changed:
            raise ValueError(f"Reviewed evidence changed for {key}: {changed}. Reconcile manually first.")


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(value, handle, indent=2, allow_nan=False)
            handle.write("\n")
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def freshness_issues(root=ROOT):
    """Read-only verification; never refresh hashes to hide changed inputs."""
    root = Path(root)
    path = root / SUMMARY
    if not path.is_file():
        return ["No rebuild record. Run python src/run_stage34.py first."]
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
        if record.get("schema_version") != 1 or record.get("status") != "passed_with_limitations":
            return ["Latest rebuild is incomplete, failed, or has an unsupported record format."]
        expected_steps = [item.get("script") for item in record.get("steps", [])]
        if expected_steps != list(STEPS) or any(item.get("exit_code") != 0 for item in record["steps"]):
            return ["Rebuild step coverage is incomplete or contains failures."]
        issues = []
        for label, expected in (("input", input_paths(root)), ("output", list(OUTPUTS))):
            stored = record.get(label + "_hashes", {})
            if set(stored) != set(expected):
                issues.append(f"Tracked {label} file set changed; rebuild required.")
            for name in expected:
                candidate = root / name
                if not candidate.is_file():
                    issues.append(f"Missing {label}: {name}")
                elif stored.get(name) != digest(candidate):
                    issues.append(f"Changed {label}: {name}")
        if record.get("environment") != environment():
            issues.append("Python or dependency versions changed; rebuild in this environment.")
        return issues
    except (OSError, ValueError, TypeError, KeyError, AttributeError, metadata.PackageNotFoundError) as exc:
        return [f"Cannot verify rebuild record: {exc}"]
