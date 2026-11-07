"""Regression checks use temporary files; project research data are never edited."""

import csv
import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "src" / "prepare_milestone_review.py"
spec = importlib.util.spec_from_file_location("review_preparation", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def write_csv(path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


class ReviewPreservationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.data = self.root / "data"
        self.data.mkdir()
        self.fields = ["milestone_id", "company_id", "source_id", "target_year", "notes"]
        self.milestones = [dict(zip(self.fields, ["M1", "C1", "S1", "2027", "Source note"]))]
        self.save_milestones()
        write_csv(self.data / "companies.csv", ["company_id", "company_name"],
                  [{"company_id": "C1", "company_name": "Test Company"}])
        write_csv(self.data / "sources.csv", ["source_id"], [{"source_id": "S1"}])
        self.output = self.root / "reports" / "milestone_review.csv"

    def save_milestones(self):
        write_csv(self.data / "milestones.csv", self.fields, self.milestones)

    def review(self):
        return module.prepare_review(self.root)

    def annotate(self):
        self.review()
        fields, rows = module.read_table(self.output, self.fields)
        fields.append("editorial_extra")
        rows[0].update({"review_notes": "Human note, retained: α\nsecond line",
                        "verification_level_review": "company_reported",
                        "editorial_extra": "Keep custom columns",
                        "target_year": "2027.0"})
        write_csv(self.output, fields, rows)
        return fields, rows

    def test_first_run_creates_blank_review(self):
        result = self.review()
        self.assertEqual((result["action"], result["added"]), ("created", 1))
        _, rows = module.read_table(self.output, module.REVIEW_FIELDS)
        self.assertEqual(rows[0]["company_name"], "Test Company")
        self.assertTrue(all(rows[0][field] == "" for field in module.REVIEW_FIELDS))

    def test_rerun_preserves_exact_bytes_and_mtime(self):
        self.annotate()
        before = self.output.read_bytes()
        mtime = self.output.stat().st_mtime_ns
        result = self.review()
        self.assertEqual(result["action"], "unchanged")
        self.assertEqual(self.output.read_bytes(), before)
        self.assertEqual(self.output.stat().st_mtime_ns, mtime)
        self.assertIsNone(result["backup"])

    def test_new_milestone_appends_and_backs_up_original(self):
        _, old_rows = self.annotate()
        before = self.output.read_bytes()
        self.milestones.append({**self.milestones[0], "milestone_id": "M2"})
        self.save_milestones()
        result = self.review()
        _, rows = module.read_table(self.output, self.fields)
        self.assertEqual(rows[0], old_rows[0])
        self.assertEqual(rows[1]["milestone_id"], "M2")
        self.assertTrue(all(rows[1][field] == "" for field in module.REVIEW_FIELDS))
        self.assertEqual(result["backup"].read_bytes(), before)
        self.assertEqual((result["preserved"], result["added"]), (1, 1))

    def test_changed_evidence_stops_without_write(self):
        self.annotate()
        before = self.output.read_bytes()
        self.milestones[0]["notes"] = "Changed underlying evidence"
        self.save_milestones()
        with self.assertRaisesRegex(ValueError, "Underlying evidence changed"):
            self.review()
        self.assertEqual(self.output.read_bytes(), before)

    def test_removed_milestone_stops_without_write(self):
        self.annotate()
        before = self.output.read_bytes()
        self.milestones.clear()
        self.save_milestones()
        with self.assertRaisesRegex(ValueError, "absent from input"):
            self.review()
        self.assertEqual(self.output.read_bytes(), before)

    def test_duplicate_input_id_rejected(self):
        self.milestones.append(dict(self.milestones[0]))
        self.save_milestones()
        with self.assertRaisesRegex(ValueError, "duplicate"):
            self.review()
        self.assertFalse(self.output.exists())

    def test_duplicate_review_id_rejected_without_write(self):
        fields, rows = self.annotate()
        write_csv(self.output, fields, rows + rows)
        before = self.output.read_bytes()
        with self.assertRaisesRegex(ValueError, "duplicate"):
            self.review()
        self.assertEqual(self.output.read_bytes(), before)

    def test_unknown_source_rejected(self):
        self.milestones[0]["source_id"] = "UNKNOWN"
        self.save_milestones()
        with self.assertRaisesRegex(ValueError, "Unknown"):
            self.review()

    def test_missing_review_input_column_rejected_without_write(self):
        self.annotate()
        write_csv(self.output, ["milestone_id"], [{"milestone_id": "M1"}])
        before = self.output.read_bytes()
        with self.assertRaisesRegex(ValueError, "missing columns"):
            self.review()
        self.assertEqual(self.output.read_bytes(), before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
