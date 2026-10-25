
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

snapshots = pd.read_csv(
    DATA / "funding_snapshots.csv",
    parse_dates=["as_of_date"]
)

companies = pd.read_csv(DATA / "companies.csv")
sources = pd.read_csv(DATA / "sources.csv")

# 1. Validate unique identifiers
for df, key in [
    (snapshots, "snapshot_id"),
    (companies, "company_id"),
    (sources, "source_id")
]:
    assert df[key].is_unique, f"Duplicate {key}"

# 2. Validate foreign keys
assert snapshots["company_id"].isin(
    companies["company_id"]
).all()

assert snapshots["source_id"].isin(
    sources["source_id"]
).all()

# 3. Validate numerical values
assert snapshots["amount_million"].notna().all()
assert (snapshots["amount_million"] > 0).all()

# 4. Validate financing classifications
allowed_groups = {
    "mixed_public_private",
    "reported_cumulative_capital",
    "private_capital"
}

allowed_qualifiers = {
    "reported",
    "approximate",
    "lower_bound"
}

allowed_statuses = {
    "pending_review",
    "company_source_checked",
    "independently_corroborated"
}

assert snapshots["comparability_group"].isin(
    allowed_groups
).all()

assert snapshots["qualifier"].isin(
    allowed_qualifiers
).all()

assert snapshots["verification_status"].isin(
    allowed_statuses
).all()

# 5. Validate dates
assert snapshots["as_of_date"].notna().all()

# 6. Join with company names
result = snapshots.merge(
    companies[["company_id", "company_name"]],
    on="company_id",
    validate="many_to_one"
)

# 7. Show verification progress
print("\nFunding verification status:")
print(
    result[
        [
            "company_name",
            "as_of_date",
            "amount_million",
            "currency",
            "comparability_group",
            "qualifier",
            "verification_status"
        ]
    ].to_string(index=False)
)

# 8. Check unresolved records
pending = result[
    result["verification_status"] == "pending_review"
]

if not pending.empty:
    print("\nWARNING: Unverified records remain.")
    print(pending["snapshot_id"].tolist())
else:
    print("\nAll funding snapshots reviewed.")

# 9. Confirm comparison limitations
if result["comparability_group"].nunique() > 1:
    print(
        "\nCAUTION: Funding definitions differ."
        "\nThese figures cannot be interpreted as"
        " directly equivalent financing measures."
    )

print("\nFinancial data validation complete.")
