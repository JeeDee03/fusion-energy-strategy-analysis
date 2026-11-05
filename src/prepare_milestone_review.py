
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

REPORTS.mkdir(exist_ok=True)

milestones = pd.read_csv(DATA / "milestones.csv")
companies = pd.read_csv(DATA / "companies.csv")
sources = pd.read_csv(DATA / "sources.csv")
devices = pd.read_csv(DATA / "reactor_designs.csv")

# Identify existing milestone columns
print("\nExisting milestone columns:")
print(milestones.columns.tolist())

required = {
    "milestone_id",
    "company_id",
    "source_id"
}

missing = required - set(milestones.columns)

if missing:
    raise ValueError(
        f"Missing required columns: {sorted(missing)}"
    )

# Validate identifiers
assert milestones["milestone_id"].is_unique
assert milestones["company_id"].isin(
    companies["company_id"]
).all()
assert milestones["source_id"].isin(
    sources["source_id"]
).all()

# Create review worksheet
review = milestones.copy()

new_fields = [
    "device_id_review",
    "engineering_domain_review",
    "evidence_type_review",
    "achievement_status_review",
    "verification_level_review",
    "evidence_location",
    "review_notes"
]

for field in new_fields:
    if field not in review.columns:
        review[field] = ""

# Attach company names for easier review
review = review.merge(
    companies[["company_id", "company_name"]],
    on="company_id",
    how="left",
    validate="many_to_one"
)

# Save without modifying original milestone records
output = REPORTS / "milestone_review.csv"
review.to_csv(output, index=False)

print("\nMilestone records:", len(review))
print("Companies:", review["company_id"].nunique())
print("Available devices:", len(devices))
print("\nReview worksheet saved:", output)
