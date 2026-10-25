
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

# Load data
companies = pd.read_csv(DATA / "companies.csv")
partnerships = pd.read_csv(
    DATA / "strategic_partnerships.csv"
)

# Define primary strategic capability
capability_mapping = {
    "P001": "Industrial & Manufacturing",
    "P002": "Public Sector & Funding",
    "P003": "Scientific & R&D",
    "P004": "Commercial & Market Access",
    "P005": "Commercial & Market Access",
    "P006": "Industrial & Manufacturing",
    "P007": "Computing & Simulation",
    "P008": "Scientific & R&D",
    "P009": "Industrial & Manufacturing",
    "P010": "Industrial & Manufacturing",
    "P011": "Public Sector & Funding"
}

# Require every partnership to be classified
assert set(partnerships["partnership_id"]) == set(
    capability_mapping
), "Unclassified or unexpected partnership records"

partnerships["primary_capability"] = (
    partnerships["partnership_id"].map(
        capability_mapping
    )
)

# Connect with company names
df = partnerships.merge(
    companies[["company_id", "company_name"]],
    on="company_id",
    validate="many_to_one"
)

# Build company-capability matrix
matrix = pd.crosstab(
    df["company_name"],
    df["primary_capability"]
)

matrix = matrix.reindex(
    companies["company_name"],
    fill_value=0
)

print("\nStrategic Capability Matrix:")
print(matrix.to_string())

# Save structured analysis
matrix.to_csv(
    DATA / "partnership_capability_matrix.csv"
)

# Create visualization
fig, ax = plt.subplots(figsize=(11, 6))

matrix.plot(
    kind="barh",
    stacked=True,
    ax=ax
)

ax.set_title(
    "Documented Partnership Capabilities"
)
ax.set_xlabel("Selected partnership records")
ax.set_ylabel("Fusion company")

ax.legend(
    title="Primary capability",
    bbox_to_anchor=(1.02, 1),
    loc="upper left"
)

fig.text(
    0.5,
    0.01,
    "Selected announcements only; "
    "not a measure of partnership quality "
    "or complete ecosystem coverage.",
    ha="center",
    fontsize=9
)

fig.tight_layout(rect=[0, 0.06, 0.76, 1])

output = REPORTS / "partnership_capabilities.png"
fig.savefig(output, dpi=200, bbox_inches="tight")

print("\nSaved:", output)

plt.show()
