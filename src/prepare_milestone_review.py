"""Prepare milestone reviews without overwriting human editorial work."""

import csv
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import os
from pathlib import Path
import shutil
import tempfile
from uuid import uuid4

ROOT = Path(__file__).resolve().parent.parent
REVIEW_FIELDS = [
    "device_id_review", "engineering_domain_review", "evidence_type_review",
    "achievement_status_review", "verification_level_review",
    "evidence_location", "review_notes",
]


def read_table(path, required):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        if len(fields) != len(set(fields)):
            raise ValueError(f"Duplicate column names in {path}")
        missing = set(required) - set(fields)
        if missing:
            raise ValueError(f"{path.name}: missing columns {sorted(missing)}")
        rows = list(reader)
    if any(None in row or any(value is None for value in row.values()) for row in rows):
        raise ValueError(f"Malformed CSV rows in {path}")
    return fields, rows


def index_rows(rows, key, label):
    result = {}
    for row in rows:
        identifier = row[key]
        if not identifier.strip() or identifier in result:
            raise ValueError(f"Empty or duplicate {key} in {label}: {identifier!r}")
        result[identifier] = row
    return result


def same_value(left, right):
    """Allow harmless legacy numeric formatting, e.g. 2027 versus 2027.0."""
    if left == right:
        return True
    try:
        a, b = Decimal(left), Decimal(right)
        return a.is_finite() and b.is_finite() and a == b
    except InvalidOperation:
        return False


def prepare_review(root=ROOT):
    root = Path(root)
    data = root / "data"
    output = root / "reports" / "milestone_review.csv"
    milestone_fields, milestones = read_table(
        data / "milestones.csv", {"milestone_id", "company_id", "source_id"}
    )
    _, companies = read_table(data / "companies.csv", {"company_id", "company_name"})
    _, sources = read_table(data / "sources.csv", {"source_id"})
    current = index_rows(milestones, "milestone_id", "milestones.csv")
    company_index = index_rows(companies, "company_id", "companies.csv")
    source_index = index_rows(sources, "source_id", "sources.csv")
    for row in milestones:
        if row["company_id"] not in company_index or row["source_id"] not in source_index:
            raise ValueError(f"Unknown company_id or source_id for {row['milestone_id']}")

    expected_fields = list(dict.fromkeys(milestone_fields + REVIEW_FIELDS + ["company_name"]))
    exists = output.exists()
    if exists:
        old_fields, old_rows = read_table(output, milestone_fields)
        old = index_rows(old_rows, "milestone_id", output.name)
        removed = set(old) - set(current)
        if removed:
            raise ValueError(
                f"Reviewed milestones absent from input: {sorted(removed)}. "
                "Reconcile manually; review file was not changed."
            )
        for identifier, previous in old.items():
            changed = [field for field in milestone_fields
                       if not same_value(previous[field], current[identifier][field])]
            if changed:
                raise ValueError(
                    f"Underlying evidence changed for {identifier}: {changed}. "
                    "Review the change and reconcile the worksheet manually; "
                    "review file was not changed."
                )
        fields = old_fields + [field for field in expected_fields if field not in old_fields]
        new_rows = [row for row in milestones if row["milestone_id"] not in old]
        if not new_rows and fields == old_fields:
            return {"action": "unchanged", "preserved": len(old_rows), "added": 0,
                    "path": output, "backup": None}
        rows = [dict(row) for row in old_rows]
        for row in rows:
            for field in fields:
                if field not in row:
                    row[field] = (company_index[row["company_id"]]["company_name"]
                                  if field == "company_name" else "")
    else:
        fields, rows, new_rows = expected_fields, [], milestones

    for milestone in new_rows:
        row = {field: "" for field in fields}
        row.update(milestone)
        row["company_name"] = company_index[row["company_id"]]["company_name"]
        rows.append(row)

    output.parent.mkdir(parents=True, exist_ok=True)
    backup = None
    if exists:
        backup_dir = output.parent / "backups"
        backup_dir.mkdir(exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        backup = backup_dir / f"milestone_review_{stamp}_{uuid4().hex[:8]}.csv"
        shutil.copy2(output, backup)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="", dir=output.parent,
            prefix=".milestone_review_", suffix=".tmp", delete=False
        ) as handle:
            temporary = Path(handle.name)
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        os.replace(temporary, output)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    return {"action": "updated" if exists else "created",
            "preserved": len(rows) - len(new_rows), "added": len(new_rows),
            "path": output, "backup": backup}


def main():
    result = prepare_review()
    print(f"Milestone review: {result['action']}")
    print(f"Existing records preserved: {result['preserved']}")
    print(f"New records added: {result['added']}")
    print(f"Review worksheet: {result['path']}")
    if result["backup"]:
        print(f"Previous worksheet backup: {result['backup']}")
    if result["added"]:
        print("New records require human editorial review before Stage 3 closure.")


if __name__ == "__main__":
    main()
