
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

REPORTS.mkdir(exist_ok=True)

issues = []
warnings = []

def check(condition, message):
    if not condition:
        issues.append(message)

def load_csv(path):
    if not path.exists():
        issues.append(f"Missing file: {path.relative_to(ROOT)}")
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except Exception as exc:
        issues.append(f"Cannot read {path.name}: {exc}")
        return pd.DataFrame()

def has_columns(df, cols, name):
    missing = set(cols) - set(df.columns)
    check(not missing, f"{name}: missing columns {sorted(missing)}")
    return not missing

companies = load_csv(DATA / "companies.csv")
sources = load_csv(DATA / "sources.csv")
devices = load_csv(DATA / "reactor_designs.csv")
technical = load_csv(DATA / "technical_parameters.csv")
subsystems = load_csv(DATA / "engineering_subsystems.csv")
milestones = load_csv(DATA / "milestones.csv")
economic = load_csv(DATA / "economic_input_register.csv")
review = load_csv(REPORTS / "milestone_review.csv")

# Check primary identifiers
datasets = [
    (companies, "company_id", "companies"),
    (sources, "source_id", "sources"),
    (devices, "device_id", "reactor_designs"),
    (technical, "parameter_id", "technical_parameters"),
    (subsystems, "evidence_id", "engineering_subsystems"),
    (milestones, "milestone_id", "milestones"),
    (economic, "input_id", "economic_input_register"),
    (review, "milestone_id", "milestone_review"),
]

for df, key, name in datasets:
    if has_columns(df, [key], name):
        check(
            df[key].notna().all() and df[key].is_unique,
            f"{name}: invalid or duplicate {key}"
        )

# Check foreign key relationships
def check_refs(child, field, parent, parent_key, name):
    if field in child.columns and parent_key in parent.columns:
        values = child[field].dropna()
        missing = set(values) - set(parent[parent_key].dropna())
        check(not missing, f"{name}: unknown {field} {sorted(missing)}")

for df, name in [
    (devices, "reactor_designs"),
    (milestones, "milestones")
]:
    check_refs(df, "company_id", companies, "company_id", name)
    check_refs(df, "source_id", sources, "source_id", name)

for df, name in [
    (technical, "technical_parameters"),
    (subsystems, "engineering_subsystems"),
    (economic, "economic_input_register")
]:
    check_refs(df, "device_id", devices, "device_id", name)
    check_refs(df, "source_id", sources, "source_id", name)

# Numeric and evidence checks
if has_columns(
    technical,
    ["value", "unit", "evidence_type"],
    "technical_parameters"
):
    numeric = pd.to_numeric(technical["value"], errors="coerce")
    check(
        numeric.notna().all(),
        "Non-numeric or missing technical values"
    )
    check(
        technical["unit"].notna().all(),
        "Missing technical units"
    )
    allowed = {
        "measured", "simulated",
        "design_target", "announced_target"
    }
    check(
        technical["evidence_type"].isin(allowed).all(),
        "Unrecognized technical evidence type"
    )

# The review worksheet must cover the milestone register
if "milestone_id" in review and "milestone_id" in milestones:
    missing = set(milestones["milestone_id"]) - set(review["milestone_id"])
    extra = set(review["milestone_id"]) - set(milestones["milestone_id"])
    check(
        not missing and not extra,
        f"Milestone review mismatch: missing={missing}, extra={extra}"
    )

review_fields = [
    "engineering_domain_review",
    "evidence_type_review",
    "achievement_status_review",
    "verification_level_review"
]

if has_columns(review, review_fields, "milestone_review"):
    for field in review_fields:
        check(
            review[field].notna().all(),
            f"Unclassified milestone records in {field}"
        )

    allowed_review = {
        "engineering_domain_review": {
            "plasma", "magnets", "integration",
            "fuel_thermal", "electricity"
        },
        "evidence_type_review": {
            "measured", "simulated", "design_target",
            "announced_target", "administrative"
        },
        "achievement_status_review": {
            "achieved", "in_progress", "planned", "unclear"
        },
        "verification_level_review": {
            "company_reported", "peer_reviewed",
            "independently_verified", "not_checked"
        }
    }
    for field, allowed in allowed_review.items():
        check(
            review[field].isin(allowed).all(),
            f"Unexpected classification in {field}"
        )

    if "evidence_location" in review:
        count = review["evidence_location"].isna().sum()
        if count:
            warnings.append(
                f"{count} milestone records lack precise evidence locations"
            )

# Review the economic handover
if has_columns(
    economic, ["input_name", "evidence_status"],
    "economic_input_register"
):
    check(
        economic["input_name"].notna().all(),
        "Unnamed economic model inputs"
    )
    valid = {
        "direct_input_candidate",
        "engineering_proxy_only",
        "missing"
    }
    check(
        economic["evidence_status"].isin(valid).all(),
        "Invalid economic evidence status"
    )

# Generate a human-readable audit report
status = "BLOCKED" if issues else "AUTOMATED CHECKS PASSED"

lines = [
    "# Stage 3 Closure Audit",
    "",
    f"**Status:** {status}",
    "",
    "## Dataset Counts",
    "",
]

for name, df in [
    ("Reactor designs", devices),
    ("Technical parameters", technical),
    ("Engineering subsystem records", subsystems),
    ("Original milestones", milestones),
    ("Reviewed milestones", review),
    ("Economic inputs", economic)
]:
    lines.append(f"- {name}: {len(df)}")

lines += ["", "## Issues", ""]

lines += [f"- {item}" for item in issues] or ["- None detected"]

lines += ["", "## Review Warnings", ""]

lines += [f"- {item}" for item in warnings] or ["- None detected"]

lines += [
    "",
    "## Important Limitations",
    "",
    "- Automated checks do not independently verify sources.",
    "- Simulation outputs are not measured reactor performance.",
    "- Milestone counts are not technology readiness scores.",
    "- Engineering proxies are not validated economic inputs.",
    "- Human editorial review remains necessary.",
]

output = REPORTS / "stage3_closure_audit.md"
output.write_text("\n".join(lines) + "\n", encoding="utf-8")

print(f"\nStage 3 audit: {status}")
print(f"Issues: {len(issues)}")
print(f"Warnings: {len(warnings)}")
print(f"Report: {output.relative_to(ROOT)}")

for issue in issues:
    print("ISSUE:", issue)

for warning in warnings:
    print("REVIEW:", warning)

if issues:
    raise SystemExit(1)
