
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

companies = pd.read_csv(DATA / "companies.csv")
funding = pd.read_csv(
    DATA / "funding_rounds.csv",
    parse_dates=["announcement_date"]
)
sources = pd.read_csv(DATA / "sources.csv")

# 1. Check for duplicate identifiers
assert funding["funding_id"].is_unique
assert companies["company_id"].is_unique
assert sources["source_id"].is_unique

# 2. Check company and source references
assert funding["company_id"].isin(
    companies["company_id"]
).all()

assert funding["source_id"].isin(
    sources["source_id"]
).all()

# 3. Validate amounts and currencies
assert funding["amount_original"].notna().all()
assert (funding["amount_original"] > 0).all()
assert funding["currency"].isin(["EUR", "USD"]).all()

# 4. Check possible duplicate funding events
possible_duplicates = funding[
    funding.duplicated(
        subset=[
            "company_id",
            "announcement_date",
            "amount_original",
            "currency"
        ],
        keep=False
    )
]

print("\nPotential duplicate records:")
print(possible_duplicates.to_string(index=False))

# 5. Measure dataset coverage
coverage = (
    funding.groupby("company_id")
    .agg(
        number_of_rounds=("funding_id", "count"),
        earliest_record=("announcement_date", "min"),
        latest_record=("announcement_date", "max")
    )
    .reset_index()
)

coverage = coverage.merge(
    companies[["company_id", "company_name"]],
    on="company_id",
    validate="one_to_one"
)

print("\nFunding dataset coverage:")
print(coverage.to_string(index=False))

print("\nBasic funding audit completed.")
