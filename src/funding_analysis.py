
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# 1. Load datasets
companies = pd.read_csv(DATA / "companies.csv")
funding = pd.read_csv(DATA / "funding_rounds.csv")

# 2. Merge datasets
df = funding.merge(
    companies,
    on="company_id",
    how="left",
    validate="many_to_one"
)

# 3. Convert units to millions
df["amount_million"] = df["amount_original"] / 1_000_000

# 4. Group by company and currency
summary = (
    df.groupby(["company_name", "currency"])
    ["amount_million"]
    .sum()
    .reset_index()
)

print("\nRecorded funding rounds (million):")
print(summary.to_string(index=False))

# 5. Create separate charts for each currency
for currency in ["EUR", "USD"]:
    subset = summary[summary["currency"] == currency]

    subset = subset.sort_values("amount_million")

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.barh(
        subset["company_name"],
        subset["amount_million"]
    )

    ax.set_title(f"Recorded Funding Rounds ({currency})")
    ax.set_xlabel(f"Funding amount (million {currency})")

    fig.tight_layout()

    output = ROOT / "reports" / f"funding_{currency.lower()}.png"
    fig.savefig(output, dpi=200)

    plt.show()
