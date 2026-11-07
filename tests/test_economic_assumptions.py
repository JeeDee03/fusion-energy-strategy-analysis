"""Assumption traceability tests. Every edit is confined to temporary fixtures."""

import csv
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "src"))
from validate_economic_assumptions import audit_assumptions
from stage34_provenance import INPUTS


class EconomicAssumptionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in INPUTS:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(PROJECT / name, target)

    def change_csv(self, name, field, value, row=0):
        path = self.root / "data" / name
        with path.open(newline="") as handle:
            reader = csv.DictReader(handle)
            fields, rows = reader.fieldnames, list(reader)
        rows[row][field] = str(value)
        with path.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def check_fails(self, text):
        result = audit_assumptions(self.root)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any(text in item for item in result["errors"]), result["errors"])

    def test_complete_register_maps_all_57_active_inputs(self):
        result = audit_assumptions(self.root)
        self.assertEqual(result["status"], "PASS_WITH_RESEARCH_GAPS")
        self.assertEqual(result["parameters"], 10)
        self.assertEqual(result["bindings_checked"], 57)
        self.assertTrue(result["research_gaps"])

    def test_reference_value_drift_rejected(self):
        self.change_csv("economic_assumptions.csv", "reference_value", 13000)
        self.check_fails("differs from active input")

    def test_active_case_outside_reviewed_range_rejected(self):
        self.change_csv("lcoe_scenarios_stage42.csv", "capex_eur_per_kwe", 19000, row=2)
        self.check_fails("outside reviewed range")

    def test_unit_mismatch_rejected(self):
        self.change_csv("economic_assumptions.csv", "unit", "USD/kWe")
        self.check_fails("unit/reference mismatch")

    def test_price_year_mismatch_rejected(self):
        self.change_csv("economic_assumptions.csv", "price_year", 2025)
        self.check_fails("Price year mismatch")

    def test_nominal_basis_rejected(self):
        path = self.root / "data/economic_model_basis.json"
        data = json.loads(path.read_text())
        data["price_basis"] = "nominal"
        path.write_text(json.dumps(data))
        self.check_fails("Model basis mismatch: price_basis")

    def test_duplicate_parameter_rejected(self):
        self.change_csv("economic_assumptions.csv", "parameter_id", "CAPEX", row=1)
        self.check_fails("duplicate parameter_id")

    def test_missing_parameter_rejected(self):
        path = self.root / "data/economic_assumptions.csv"
        with path.open(newline="") as handle:
            reader = csv.DictReader(handle)
            fields, rows = reader.fieldnames, list(reader)
        with path.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows[:-1])
        self.check_fails("all ten modeled input families")

    def test_unknown_reference_rejected(self):
        self.change_csv("economic_assumptions.csv", "reference_notes", "UNKNOWN")
        self.check_fails("Unknown reference note")

    def test_missing_rationale_rejected(self):
        self.change_csv("economic_assumptions.csv", "rationale", "")
        self.check_fails("Unexplained register field")

    def test_false_calibration_claim_rejected(self):
        self.change_csv("economic_assumptions.csv", "evidence_class", "empirically_calibrated")
        self.check_fails("Unsupported evidence/calibration claim")

    def test_range_not_accepted_as_confidence_interval(self):
        self.change_csv("economic_assumptions.csv", "range_role", "95_percent_confidence_interval")
        self.check_fails("Unsupported range classification")

    def test_historical_price_must_match_retained_market_mean(self):
        self.change_csv("electricity_revenue_scenarios.csv", "electricity_price_eur_per_mwh", 90)
        self.check_fails("rounded historical 2024 mean")

    def test_missing_numeric_binding_column_rejected(self):
        path = self.root / "data/lcoe_performance_scenarios.csv"
        with path.open(newline="") as handle:
            reader = csv.DictReader(handle)
            fields, rows = reader.fieldnames, list(reader)
        fields.remove("capacity_factor")
        with path.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
        self.check_fails("missing required columns")

    def test_literature_cannot_be_marked_as_direct_calibration(self):
        self.change_csv("economic_reference_notes.csv", "source_role", "direct_Stellaris_calibration")
        self.check_fails("Unsupported reference transfer claim")

    def test_validation_never_rewrites_reviewed_assumptions(self):
        files = [self.root / "data" / name for name in (
            "economic_assumptions.csv", "economic_reference_notes.csv", "economic_model_basis.json")]
        before = {path: path.read_bytes() for path in files}
        self.assertEqual(audit_assumptions(self.root)["status"], "PASS_WITH_RESEARCH_GAPS")
        self.assertTrue(all(path.read_bytes() == value for path, value in before.items()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
