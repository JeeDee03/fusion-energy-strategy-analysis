"""Evidence coverage, provenance boundaries and pandas-compatible ID guards."""

import csv
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import warnings

import pandas as pd

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "src"))
from company_comparison import build_comparison, reconciliation_check
from lifecycle_cash_flow import indexed_scenarios
from stage34_provenance import INPUTS


class ScenarioIndexCompatibilityTests(unittest.TestCase):
    def test_indexing_is_warning_free_and_preserves_rows(self):
        source = pd.DataFrame({"scenario_id": ["A", "B"], "value": [1, 2]})
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            result = indexed_scenarios(source, "Test")
        self.assertEqual(result.index.tolist(), ["A", "B"])
        self.assertEqual(result["value"].tolist(), [1, 2])
        self.assertIn("scenario_id", source.columns)

    def test_duplicate_ids_still_rejected_without_deprecated_argument(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            indexed_scenarios(pd.DataFrame({"scenario_id": ["A", "A"]}), "Test")

    def test_missing_or_blank_ids_rejected(self):
        for values in ([None], [""], ["   "]):
            with self.assertRaises(ValueError):
                indexed_scenarios(pd.DataFrame({"scenario_id": values}), "Test")


class CompanyComparisonTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in INPUTS:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(PROJECT / name, target)
        (self.root / "reports").mkdir(exist_ok=True)

    def edit(self, filename, field, value, row=0):
        path = self.root / "data" / filename
        with path.open(newline="") as handle:
            reader = csv.DictReader(handle)
            fields, rows = reader.fieldnames, list(reader)
        rows[row][field] = value
        self.save(path, fields, rows)

    def save(self, path, fields, rows):
        with path.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def test_all_five_companies_and_eight_criteria_are_retained(self):
        tidy, matrix, audit, sources = build_comparison(self.root)
        self.assertEqual((len(tidy), len(matrix), len(sources)), (40, 5, 14))
        self.assertEqual(audit["status"], "PASS_WITH_EVIDENCE_GAPS")
        self.assertEqual(audit["unresolved_cells"], 4)
        self.assertEqual(tidy.groupby("company_id").size().tolist(), [8] * 5)

    def test_business_index_and_reviewed_profile_must_agree(self):
        self.edit("companies.csv", "business_model", "Undetermined")
        with self.assertRaisesRegex(ValueError, "business-model mismatch"):
            build_comparison(self.root)

    def test_missing_cell_is_not_treated_as_complete_coverage(self):
        path = self.root / "data/company_comparison_claims.csv"
        with path.open(newline="") as handle:
            reader = csv.DictReader(handle)
            fields, rows = reader.fieldnames, list(reader)
        self.save(path, fields, rows[:-1])
        with self.assertRaisesRegex(ValueError, "all 40"):
            build_comparison(self.root)

    def test_duplicate_company_criterion_is_rejected(self):
        self.edit("company_comparison_claims.csv", "criterion", "technology", row=1)
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            build_comparison(self.root)

    def test_unknown_source_is_rejected(self):
        self.edit("company_comparison_claims.csv", "source_ids", "UNKNOWN")
        with self.assertRaisesRegex(ValueError, "source reference"):
            build_comparison(self.root)

    def test_wrong_company_source_is_rejected(self):
        self.edit("company_comparison_claims.csv", "source_ids", "BTO01")
        with self.assertRaisesRegex(ValueError, "wrong-company"):
            build_comparison(self.root)

    def test_wrong_company_device_is_rejected(self):
        self.edit("company_comparison_claims.csv", "reference_device_id", "TK_ST40")
        with self.assertRaisesRegex(ValueError, "different or unknown company"):
            build_comparison(self.root)

    def test_false_independent_verification_tag_is_rejected(self):
        self.edit("company_comparison_claims.csv", "evidence_type", "independently_verified_commercial_plant")
        with self.assertRaisesRegex(ValueError, "Unsupported evidence"):
            build_comparison(self.root)

    def test_missing_limitations_are_rejected(self):
        self.edit("company_comparison_claims.csv", "limitation", "")
        with self.assertRaisesRegex(ValueError, "blank required"):
            build_comparison(self.root)

    def test_source_after_review_cutoff_is_rejected(self):
        self.edit("competitive_sources.csv", "publication_date", "2027-01-01")
        with self.assertRaisesRegex(ValueError, "after review cutoff"):
            build_comparison(self.root)

    def test_business_labels_cannot_be_marked_as_observed_revenue(self):
        self.edit("company_business_profiles.csv", "classification_basis", "observed_commercial_revenue")
        with self.assertRaisesRegex(ValueError, "observed commercial revenue"):
            build_comparison(self.root)

    def test_stale_output_is_detected_after_claim_change(self):
        tidy, matrix, _, _ = build_comparison(self.root)
        tidy.to_csv(self.root / "reports/company_comparison.csv", index=False)
        matrix.to_csv(self.root / "reports/company_comparison_matrix.csv", index=False)
        self.assertTrue(reconciliation_check(self.root)[0])
        self.edit("company_comparison_claims.csv", "statement", "Changed reviewed statement")
        self.assertFalse(reconciliation_check(self.root)[0])

    def test_build_does_not_rewrite_reviewed_sources(self):
        paths = [self.root / "data" / name for name in (
            "companies.csv", "company_business_profiles.csv", "competitive_sources.csv", "company_comparison_claims.csv")]
        before = {path: path.read_bytes() for path in paths}
        build_comparison(self.root)
        self.assertTrue(all(path.read_bytes() == content for path, content in before.items()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
