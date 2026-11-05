from pathlib import Path
import csv
from datetime import date

ROOT = Path(__file__).resolve().parent.parent

def read(name):
    with (ROOT / "data" / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

rows = read("milestones.csv")
companies = {r["company_id"] for r in read("companies.csv")}
sources = {r["source_id"] for r in read("sources.csv")}
assert rows, "No milestone records"
assert len({r["milestone_id"] for r in rows}) == len(rows), "Duplicate milestone IDs"
for r in rows:
    assert r["company_id"] in companies, r["milestone_id"] + ": unknown company"
    assert r["source_id"] in sources, r["milestone_id"] + ": unknown source; append milestone sources first"
    assert r["status"] in {"planned", "reported_completed"}
    assert r["evidence_level"] in {"company_target", "company_report"}
    for key in ["statement_date", "target_date", "actual_date"]:
        if r[key]:
            date.fromisoformat(r[key])
    assert date.fromisoformat(r["statement_date"]) <= date(2026, 10, 24), "Statement outside historical cutoff"
    if r["target_year"]:
        assert len(r["target_year"]) == 4 and r["target_year"].isdigit()
    if r["status"] == "planned":
        assert not r["actual_date"], "Target must not have completion date"
        assert r["target_period_text"] or r["target_date"], "Missing target period"
        assert r["evidence_level"] == "company_target"
    if r["actual_date"]:
        assert date.fromisoformat(r["actual_date"]) <= date.fromisoformat(r["statement_date"])
print(f"Milestone structural checks passed: {len(rows)} records, {len({r['company_id'] for r in rows})} companies.")
print("Company-reported events and historical targets; these checks do not establish independent technical verification.")
