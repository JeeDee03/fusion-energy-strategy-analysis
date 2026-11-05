
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"

review = pd.read_csv(
    REPORTS / "milestone_review.csv"
)

required = [
    "company_name",
    "engineering_domain_review",
    "achievement_status_review",
    "verification_level_review"
]

assert review["milestone_id"].is_unique

# Retain reviewed records only
df = review.dropna(
    subset=required
).copy()

if df.empty:
    raise ValueError(
        "No classified milestones found. "
        "Complete the review worksheet first."
    )

allowed_domains = {
    "plasma", "magnets", "integration",
    "fuel_thermal", "electricity"
}

allowed_statuses = {
    "achieved", "in_progress",
    "planned", "unclear"
}

assert df["engineering_domain_review"].isin(
    allowed_domains
).all()

assert df["achievement_status_review"].isin(
    allowed_statuses
).all()

# Summarize available evidence
matrix = pd.crosstab(
    df["company_name"],
    df["engineering_domain_review"]
)

print("\nTechnical evidence coverage:")
print(matrix.to_string())

# Achieved versus planned milestones
status_table = pd.crosstab(
    df["company_name"],
    df["achievement_status_review"]
)

print("\nMilestone status distribution:")
print(status_table.to_string())

# Save summaries
matrix.to_csv(
    REPORTS / "technology_evidence_coverage.csv"
)

status_table.to_csv(
    REPORTS / "technology_milestone_status.csv"
)

# Visualization
fig, ax = plt.subplots(figsize=(10, 5))

matrix.plot(
    kind="barh",
    stacked=True,
    ax=ax
)

ax.set_title(
    "Documented Technical Milestone Coverage"
)
ax.set_xlabel("Classified milestone records")
ax.set_ylabel("Company")

ax.legend(
    title="Engineering domain",
    bbox_to_anchor=(1.02, 1),
    loc="upper left"
)

fig.text(
    0.5, 0.01,
    "Selected, manually classified events. "
    "Counts do not measure technology readiness.",
    ha="center",
    fontsize=9
)

fig.tight_layout(rect=[0, 0.06, 0.76, 1])

output = REPORTS / "technology_evidence_coverage.png"
fig.savefig(output, dpi=200, bbox_inches="tight")

print("\nSaved:", output)
plt.show()
