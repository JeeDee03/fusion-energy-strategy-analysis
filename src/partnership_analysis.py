
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

REPORTS.mkdir(exist_ok=True)

# 1. Load datasets
companies = pd.read_csv(DATA / "companies.csv")
sources = pd.read_csv(DATA / "sources.csv")
partnerships = pd.read_csv(
    DATA / "strategic_partnerships.csv",
    parse_dates=["announcement_date"]
)

# 2. Validate the records
assert partnerships["partnership_id"].is_unique
assert partnerships["company_id"].isin(
    companies["company_id"]
).all()
assert partnerships["source_id"].isin(
    sources["source_id"]
).all()

# 3. Combine records with company names
df = partnerships.merge(
    companies[["company_id", "company_name"]],
    on="company_id",
    validate="many_to_one"
)

# 4. Examine partnership types
summary = pd.crosstab(
    df["company_name"],
    df["partnership_type"]
)

print("\nPartnership type matrix:")
print(summary.to_string())

# 5. Plot the available evidence
ax = summary.plot(
    kind="barh",
    stacked=True,
    figsize=(11, 6)
)

ax.set_title(
    "Documented Strategic Partnership Events"
)
ax.set_xlabel("Number of recorded events")
ax.set_ylabel("Company")

ax.legend(
    title="Partnership Type",
    bbox_to_anchor=(1.02, 1),
    loc="upper left"
)

fig = ax.get_figure()

fig.text(
    0.5,
    0.01,
    "Exploratory dataset: selected events only; "
    "not a complete partnership census.",
    ha="center",
    fontsize=9
)

fig.tight_layout(rect=[0, 0.05, 0.77, 1])

output = REPORTS / "partnership_types.png"
fig.savefig(output, dpi=200, bbox_inches="tight")

print("\nSaved:", output)
plt.show()
