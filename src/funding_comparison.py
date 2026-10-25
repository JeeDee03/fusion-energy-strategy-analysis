
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

REPORTS.mkdir(exist_ok=True)

# 1. Load normalized funding data
funding = pd.read_csv(DATA / "funding_normalized.csv")
companies = pd.read_csv(DATA / "companies.csv")

# 2. Connect company names
df = funding.merge(
    companies[["company_id", "company_name"]],
    on="company_id",
    how="left",
    validate="many_to_one"
)

assert df["company_name"].notna().all()
assert df["amount_usd"].notna().all()

# 3. Aggregate recorded investment rounds
summary = (
    df.groupby("company_name")["amount_usd"]
    .sum()
    .div(1_000_000)
    .sort_values()
)

# 4. Plot
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.barh(summary.index, summary.values)

ax.bar_label(bars, fmt="%.1f", padding=4)

ax.set_xlim(0, summary.max() * 1.20)

ax.set_title(
    "Selected Disclosed Funding Rounds by Company"
)
ax.set_xlabel("Recorded funding (million USD)")

fig.text(
    0.5,
    0.01,
    "Historical EUR/USD reference rates; "
    "selected rounds only, not total company funding.",
    ha="center",
    fontsize=9
)

fig.tight_layout(rect=[0, 0.05, 1, 1])

output = REPORTS / "funding_comparison_usd.png"

fig.savefig(output, dpi=200)
plt.show()

print("\nRecorded funding (million USD):")
print(summary.round(2).to_string())
print("\nSaved:", output)
