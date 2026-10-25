
from pathlib import Path
import pandas as pd

# Locate the project root
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# Load datasets
companies = pd.read_csv(DATA / "companies.csv")
funding = pd.read_csv(DATA / "funding_rounds.csv")
sources = pd.read_csv(DATA / "sources.csv")

# Check identifiers
assert companies["company_id"].is_unique
assert funding["funding_id"].is_unique
assert sources["source_id"].is_unique

# Connect funding records with companies
merged = funding.merge(
    companies,
    on="company_id",
    how="left",
    validate="many_to_one"
)

# Connect records with original sources
merged = merged.merge(
    sources,
    on="source_id",
    how="left",
    validate="many_to_one"
)

# Validate source and company references
assert merged["company_name"].notna().all()
assert merged["source_title"].notna().all()

# Display funding records
result = merged[
    [
        "company_name",
        "announcement_date",
        "amount_original",
        "currency",
        "source_id"
    ]
]

print(result.to_string(index=False))

print("\nDataset validation successful!")
