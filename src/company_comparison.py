"""Comparable technology/business-model evidence; no scores or cost ranking.

Source review is a dated human research snapshot. Offline checks validate
coverage and consistency, not the truth of company statements or contracts.
"""

from datetime import date
from pathlib import Path

import pandas as pd

from prepare_milestone_review import read_table, index_rows
from stage4_reconciliation import compare_table
from stage34_provenance import write_json

ROOT = Path(__file__).resolve().parent.parent
REVIEW_DATE = "2026-11-05"
COMPANIES = {"PF001", "TO001", "TE001", "CF001", "TK001"}
CRITERIA = {
    "technology": "Technology architecture",
    "product": "Reference product and development path",
    "customer": "Target customer or counterpart",
    "revenue": "Declared commercialization / revenue route",
    "delivery": "Ownership and delivery responsibility",
    "manufacturing": "Manufacturing approach",
    "maintenance": "Maintenance evidence",
    "maturity": "Nature of maturity evidence",
}
EVIDENCE = {"conceptual_design", "announced_strategy", "announced_project",
            "announced_contract", "reported_design_review", "reported_subsystem_result",
            "reported_experiment", "analyst_inference", "not_established_in_reviewed_sources"}
SOURCE_KINDS = {"company_website", "company_announcement", "peer_reviewed_design", "government_research_summary"}


def build_comparison(root=ROOT):
    root = Path(root)
    _, companies = read_table(root / "data/companies.csv", {"company_id", "company_name", "business_model"})
    company_index = index_rows(companies, "company_id", "companies.csv")
    if set(company_index) != COMPANIES:
        raise ValueError("Comparison scope must retain all five selected companies")
    _, devices = read_table(root / "data/reactor_designs.csv", {"device_id", "company_id", "device_role"})
    device_index = index_rows(devices, "device_id", "reactor_designs.csv")
    _, legacy_sources = read_table(root / "data/sources.csv", {"source_id"})
    legacy_ids = index_rows(legacy_sources, "source_id", "sources.csv")
    _, profiles = read_table(root / "data/company_business_profiles.csv", {
        "company_id", "strategy_label", "classification_basis", "source_ids", "review_date", "limitations"})
    profile_index = index_rows(profiles, "company_id", "company_business_profiles.csv")
    if set(profile_index) != COMPANIES:
        raise ValueError("Business profiles must cover the same five companies")
    _, sources = read_table(root / "data/competitive_sources.csv", {
        "source_id", "company_id", "source_title", "publisher", "url", "publication_date",
        "updated_date", "review_date", "source_kind", "locator", "limitations", "legacy_source_id"})
    source_index = index_rows(sources, "source_id", "competitive_sources.csv")
    cutoff = date.fromisoformat(REVIEW_DATE)
    for row in sources:
        if row["company_id"] not in COMPANIES or row["source_kind"] not in SOURCE_KINDS:
            raise ValueError("Unsupported source company/kind: " + row["source_id"])
        if row["review_date"] != REVIEW_DATE:
            raise ValueError("Source review date differs from declared snapshot")
        for field in ("publication_date", "updated_date"):
            if row[field] and date.fromisoformat(row[field]) > cutoff:
                raise ValueError("Source dated after review cutoff: " + row["source_id"])
        if not row["url"].startswith("https://") or not all(row[k].strip() for k in
                ("source_title", "publisher", "locator", "limitations")):
            raise ValueError("Incomplete primary-source record: " + row["source_id"])
        if row["legacy_source_id"] and row["legacy_source_id"] not in legacy_ids:
            raise ValueError("Unknown legacy source ID: " + row["source_id"])

    def resolve(ids, company):
        keys = ids.split(";")
        if not keys or any(key not in source_index or source_index[key]["company_id"] != company for key in keys):
            raise ValueError("Unknown or wrong-company source reference: " + ids)
        return ";".join(source_index[key]["url"] for key in keys)

    for row in profiles:
        company = row["company_id"]
        if not row["strategy_label"].strip() or row["strategy_label"] == "Undetermined":
            raise ValueError("Business profile lacks an explicit reviewed classification")
        if row["strategy_label"] != company_index[company]["business_model"]:
            raise ValueError("Company index/profile business-model mismatch: " + company)
        if row["classification_basis"] != "analyst_classification_of_declared_strategy":
            raise ValueError("Business classifications must not assert observed commercial revenue")
        if row["review_date"] != REVIEW_DATE or not row["limitations"].strip():
            raise ValueError("Business profile lacks review scope/limitations")
        resolve(row["source_ids"], company)
    required = {"claim_id", "company_id", "criterion", "reference_device_id", "statement",
                "evidence_type", "source_ids", "evidence_locator", "limitation",
                "analyst_implication", "review_date"}
    _, claims = read_table(root / "data/company_comparison_claims.csv", required)
    index_rows(claims, "claim_id", "company_comparison_claims.csv")
    pairs = set()
    result = []
    for row in claims:
        company, criterion = row["company_id"], row["criterion"]
        pair = company, criterion
        if pair in pairs or company not in COMPANIES or criterion not in CRITERIA:
            raise ValueError("Duplicate or unsupported company/criterion pair")
        pairs.add(pair)
        if any(not row[name].strip() for name in required):
            raise ValueError("Comparison claim contains blank required evidence fields")
        if row["evidence_type"] not in EVIDENCE or row["review_date"] != REVIEW_DATE:
            raise ValueError("Unsupported evidence claim or review date")
        device = device_index.get(row["reference_device_id"])
        if device is None or device["company_id"] != company:
            raise ValueError("Reference device belongs to a different or unknown company")
        urls = resolve(row["source_ids"], company)
        result.append({**row, "company_name": company_index[company]["company_name"],
                       "strategy_label": profile_index[company]["strategy_label"],
                       "reference_device_role": device["device_role"], "source_urls": urls})
    if pairs != {(company, criterion) for company in COMPANIES for criterion in CRITERIA}:
        raise ValueError("Comparison must retain all 40 company/criterion cells, including unresolved cells")
    tidy = pd.DataFrame(result).sort_values(["company_id", "criterion"]).reset_index(drop=True)
    matrix_rows = []
    for company in sorted(COMPANIES):
        values = {"company_id": company, "company_name": company_index[company]["company_name"],
                  "strategy_label": profile_index[company]["strategy_label"]}
        for criterion in CRITERIA:
            row = next(item for item in result if item["company_id"] == company and item["criterion"] == criterion)
            values[criterion] = row["statement"] + " [" + row["evidence_type"] + "]"
        matrix_rows.append(values)
    audit = {
        "status": "PASS_WITH_EVIDENCE_GAPS", "review_date": REVIEW_DATE,
        "companies": len(COMPANIES), "criteria": len(CRITERIA), "cells": len(tidy),
        "primary_sources": len(sources),
        "unresolved_cells": int(tidy["evidence_type"].eq("not_established_in_reviewed_sources").sum()),
        "interpretation": "Coverage is not technical readiness, source independence, comparative LCOE or commercial success.",
        "limitations": [
            "Reported plans, conceptual designs, contracts and experimental results are different evidence types; no ordinal maturity score is assigned.",
            "Unresolved means not established in this selected review, not absence of a capability or disclosure anywhere.",
            "Business labels classify declared strategy, not realized fusion-electricity revenue, margins or financing risk reduction.",
            "First-party websites and announcements were manually reviewed; offline validation cannot independently certify their claims or track later page changes.",
            "The same engineering/economic model is not calibrated separately for five companies, so no company LCOE or cost ranking is inferred.",
            "This is a bounded source snapshot, not a full legal, financial, licensing or technical due-diligence review.",
        ],
    }
    return tidy, pd.DataFrame(matrix_rows), audit, source_index


def reconciliation_check(root=ROOT):
    try:
        tidy, matrix, _, _ = build_comparison(root)
        compare_table(pd.read_csv(Path(root) / "reports/company_comparison.csv"), tidy, ["company_id", "criterion"])
        compare_table(pd.read_csv(Path(root) / "reports/company_comparison_matrix.csv"), matrix, ["company_id"])
        return True, "Five company profiles and all 40 evidence cells match the dated reviewed sources; gaps remain explicit."
    except (OSError, ValueError, KeyError, AssertionError) as exc:
        return False, str(exc)[:700]


def main():
    reports = ROOT / "reports"
    reports.mkdir(exist_ok=True)
    try:
        tidy, matrix, audit, sources = build_comparison()
        tidy.to_csv(reports / "company_comparison.csv", index=False)
        matrix.to_csv(reports / "company_comparison_matrix.csv", index=False)
        write_json(reports / "company_comparison_audit.json", audit)
        lines = ["# Company Technology and Business-Model Comparison", "", "Status: " + audit["status"],
                 "", "Review snapshot: " + REVIEW_DATE, "", audit["interpretation"], ""]
        for criterion, label in CRITERIA.items():
            lines += ["## " + label, "", "| Company | Reviewed statement | Evidence | Sources | Limitation |",
                      "|---|---|---|---|---|"]
            for row in tidy[tidy["criterion"] == criterion].to_dict("records"):
                links = ", ".join(f"[{key}]({sources[key]['url']})" for key in row["source_ids"].split(";"))
                lines.append(f"| {row['company_name']} | {row['statement']} | {row['evidence_type']} | {links} | {row['limitation']} |")
            lines.append("")
        lines += ["## Interpretation limits", ""] + ["- " + value for value in audit["limitations"]]
        (reports / "company_comparison.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("Company comparison: " + audit["status"])
        print(f"Companies: 5 | Criteria: 8 | Cells: 40 | Unresolved cells: {audit['unresolved_cells']}")
        return 0
    except (OSError, ValueError, KeyError) as exc:
        write_json(reports / "company_comparison_audit.json", {"status": "FAIL", "error": str(exc)})
        print("Company comparison: FAIL — " + str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
