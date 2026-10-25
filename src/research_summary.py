
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RESEARCH = ROOT / "research"

RESEARCH.mkdir(exist_ok=True)

companies = pd.read_csv(DATA / "companies.csv")

rounds = pd.read_csv(
    DATA / "funding_rounds.csv",
    parse_dates=["announcement_date"]
)

snapshots = pd.read_csv(
    DATA / "funding_snapshots.csv",
    parse_dates=["as_of_date"]
)

partnerships = pd.read_csv(
    DATA / "strategic_partnerships.csv"
)

sources = pd.read_csv(DATA / "sources.csv")

# 1. Validate relationships
for dataset in [rounds, snapshots, partnerships]:
    assert dataset["company_id"].isin(
        companies["company_id"]
    ).all()

    assert dataset["source_id"].isin(
        sources["source_id"]
    ).all()

# 2. Dataset coverage by company
coverage = companies[
    ["company_id", "company_name"]
].copy()

for frame, new_column in [
    (rounds, "recorded_rounds"),
    (snapshots, "funding_snapshots"),
    (partnerships, "partnership_records")
]:
    counts = frame.groupby("company_id").size()

    coverage[new_column] = (
        coverage["company_id"]
        .map(counts)
        .fillna(0)
        .astype(int)
    )

# 3. Summarize reported cumulative funding
funding_view = snapshots.merge(
    companies[["company_id", "company_name"]],
    on="company_id",
    validate="many_to_one"
)


funding_columns = [
    "company_name",
    "as_of_date",
    "amount_million",
    "currency",
    "comparison_basis",
    "qualifier",
    "comparability_group",
    "verification_status"
]


funding_view = funding_view[
    funding_columns
].copy()

funding_view["as_of_date"] = (
    funding_view["as_of_date"]
    .dt.strftime("%Y-%m-%d")
)

# 4. Summarize partnership capabilities
capabilities_file = (
    DATA / "partnership_capability_matrix.csv"
)

capabilities = pd.read_csv(
    capabilities_file,
    index_col=0
)

# 5. Generate report
sections = [
    "# Stage 2.9 — Research Data Summary",
    "",
    "## Dataset Coverage",
    "",
    coverage.drop(columns="company_id").to_markdown(
        index=False
    ),
    "",
    "## Reported Funding Snapshots",
    "",
    funding_view.to_markdown(index=False),
    "",
    "## Selected Partnership Capabilities",
    "",
    capabilities.to_markdown(),
    "",
    "## Methodological Limitations",
    "",
    "- Funding definitions and dates differ.",
    "- Funding rounds are not complete histories.",
    "- Partnership records are selected examples.",
    "- Partnership counts do not measure quality.",
    "- Company targets are not verified outcomes.",
    "- Unknown funding is not equivalent to zero.",
]

output = RESEARCH / "02_market_data_summary.md"
output.write_text(
    "\n".join(sections),
    encoding="utf-8"
)

print("Saved research summary:", output)
print("\nDataset coverage:")
print(coverage.to_string(index=False))
