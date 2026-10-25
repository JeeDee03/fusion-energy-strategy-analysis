
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

companies = pd.read_csv(DATA / "companies.csv")
sources = pd.read_csv(DATA / "sources.csv")
snapshots = pd.read_csv(
    DATA / "funding_snapshots.csv",
    parse_dates=["as_of_date"]
)

# Validate snapshot records
assert snapshots["snapshot_id"].is_unique
assert snapshots["company_id"].isin(
    companies["company_id"]
).all()
assert snapshots["source_id"].isin(
    sources["source_id"]
).all()
assert (snapshots["amount_million"] > 0).all()

# Connect snapshots to company and source data
df = snapshots.merge(
    companies[["company_id", "company_name", "technology"]],
    on="company_id",
    validate="many_to_one"
).merge(
    sources[["source_id", "source_title"]],
    on="source_id",
    validate="many_to_one"
)

columns = [
    "company_name",
    "as_of_date",
    "amount_million",
    "currency",
    "comparison_basis",
    "qualifier"
]

print("\nReported cumulative funding snapshots:")
print(df[columns].to_string(index=False))

print("\nData quality checks passed.")

# Detect differences in reporting definitions
if df["comparison_basis"].nunique() > 1:
    print(
        "\nWARNING: Funding definitions differ."
        "\nDo not directly rank these values as"
        " equivalent private financing."
    )
