
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# 1. Load original investment data
funding = pd.read_csv(
    DATA / "funding_rounds.csv",
    parse_dates=["announcement_date"]
)

# 2. Download daily exchange rates from ECB
url = (
    "https://data-api.ecb.europa.eu/service/data/"
    "EXR/D.USD.EUR.SP00.A"
    "?startPeriod=2025-01-01"
    "&endPeriod=2026-10-23"
    "&format=csvdata"
)

fx = pd.read_csv(
    url,
    usecols=["TIME_PERIOD", "OBS_VALUE"]
)

# 3. Rename columns
fx = fx.rename(
    columns={
        "TIME_PERIOD": "fx_date",
        "OBS_VALUE": "eur_usd_rate"
    }
)

fx["fx_date"] = pd.to_datetime(fx["fx_date"])
fx["eur_usd_rate"] = pd.to_numeric(
    fx["eur_usd_rate"],
    errors="raise"
)

# 4. Match each investment with its historical FX rate
funding = funding.sort_values("announcement_date")
fx = fx.sort_values("fx_date")

merged = pd.merge_asof(
    funding,
    fx,
    left_on="announcement_date",
    right_on="fx_date",
    direction="backward",
    tolerance=pd.Timedelta(days=7)
)

# 5. Calculate USD equivalents
merged["amount_usd"] = merged["amount_original"]

eur_mask = merged["currency"] == "EUR"
usd_mask = merged["currency"] == "USD"

assert (eur_mask | usd_mask).all()
assert merged.loc[eur_mask, "eur_usd_rate"].notna().all()

merged.loc[eur_mask, "amount_usd"] = (
    merged.loc[eur_mask, "amount_original"]
    * merged.loc[eur_mask, "eur_usd_rate"]
)

# 6. Validate values
assert (merged["amount_usd"] > 0).all()

# 7. Save enriched data separately
output = DATA / "funding_normalized.csv"

merged.to_csv(output, index=False)

print(
    merged[
        [
            "company_id",
            "announcement_date",
            "currency",
            "amount_original",
            "fx_date",
            "eur_usd_rate",
            "amount_usd"
        ]
    ].to_string(index=False)
)

print("\nSaved:", output)
