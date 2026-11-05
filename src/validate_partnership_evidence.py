from pathlib import Path
import csv
from datetime import date
ROOT = Path(__file__).resolve().parent.parent

def read(name):
    with (ROOT / "data" / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

base = read("strategic_partnerships.csv")
evidence = read("partnership_evidence.csv")
tags = read("partnership_capability_tags.csv")
claims = read("partnership_claims.csv")
links = read("partnership_claim_sources.csv")
sources = {r["source_id"] for r in read("sources.csv")}
master = {r["partnership_id"]: r for r in base}
assert len(master) == len(base), "Duplicate master IDs"
assert len({r["partnership_id"] for r in evidence}) == len(evidence)
assert {r["partnership_id"] for r in evidence} == set(master), "Evidence coverage differs from master"
allowed = {"capital", "utility_expertise", "site_access", "public_support", "scientific_rd", "offtake", "manufacturing", "computing_simulation", "technology_supply"}
for r in evidence:
    assert r["company_id"] == master[r["partnership_id"]]["company_id"]
    assert r["source_id"] in sources
    assert date.fromisoformat(r["statement_date"]) <= date(2026, 10, 24)
    assert r["undisclosed_terms"] and r["source_locator"]
assert len({(r["partnership_id"], r["capability"]) for r in tags}) == len(tags)
assert {r["partnership_id"] for r in tags} == set(master)
assert all(r["capability"] in allowed for r in tags)
ids = {r["claim_id"] for r in claims}
assert len(ids) == len(claims)
assert {r["entity_id"] for r in claims} == set(master)
assert all(r["claim_id"] in ids and r["source_id"] in sources for r in links)
assert len({(r["claim_id"], r["source_id"]) for r in links}) == len(links)
print(f"Partnership checks passed: {len(evidence)} records, {len(tags)} capability links, {len(claims)} claims.")
print("Multiple tags per partnership are permitted; tag counts are not partnership quality scores.")
