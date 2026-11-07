"""Stale-output regression tests; all mutations use temporary project fixtures."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import pandas as pd

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "src"))
from stage34_provenance import (
    INPUTS, OUTPUTS, STEPS, SUMMARY, environment, freshness_issues,
    hashes, input_paths, write_json, check_review_alignment,
)
from stage4_reconciliation import reconciliation_checks


class Stage34ReproducibilityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        paths = set(input_paths(PROJECT)) | set(OUTPUTS)
        paths |= {str(path.relative_to(PROJECT)) for path in (PROJECT / "src").glob("*.py")}
        for name in paths:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(PROJECT / name, target)
        # Synthetic successful record for isolated hash-check tests. The real
        # end-to-end runner is separately exercised against the supplied project.
        write_json(self.root / SUMMARY, {
            "schema_version": 1, "status": "passed_with_limitations",
            "steps": [{"script": script, "exit_code": 0} for script in STEPS],
            "environment": environment(),
            "input_hashes": hashes(self.root, input_paths(self.root)),
            "output_hashes": hashes(self.root, OUTPUTS),
        })

    def change_cell(self, name, column, value, row=0):
        path = self.root / name
        table = pd.read_csv(path)
        table.loc[row, column] = value
        table.to_csv(path, index=False)

    def failed_tables(self):
        return {name for name, passed, _ in reconciliation_checks(self.root) if not passed}

    def test_current_snapshot_and_all_eight_tables_pass(self):
        self.assertEqual(freshness_issues(self.root), [])
        checks = reconciliation_checks(self.root)
        self.assertEqual(len(checks), 8)
        self.assertTrue(all(passed for _, passed, _ in checks))

    def test_changed_revenue_input_detected_without_rebuild(self):
        self.change_cell("data/electricity_revenue_scenarios.csv",
                         "electricity_price_eur_per_mwh", 178.51)
        self.assertTrue(any("electricity_revenue_scenarios.csv" in issue
                            for issue in freshness_issues(self.root)))
        failed = self.failed_tables()
        self.assertIn("Current inputs: stage45_npv_summary.csv", failed)
        self.assertIn("Current inputs: stage45_annual_cash_flows.csv", failed)

    def test_nonreference_cost_change_detected(self):
        self.change_cell("data/lcoe_scenarios_stage42.csv", "capex_eur_per_kwe", 19000, row=2)
        failed = self.failed_tables()
        self.assertIn("Current inputs: stage42_lcoe_scenarios.csv", failed)
        self.assertIn("Current inputs: stage43_performance_sensitivity.csv", failed)

    def test_learning_change_detected_beyond_first_unit(self):
        self.change_cell("data/manufacturing_learning_scenarios.csv", "magnet_learning_rate", .21, row=2)
        self.assertIn("Current inputs: stage44_learning_results.csv", self.failed_tables())

    def test_missing_scenario_row_detected(self):
        path = self.root / "reports/stage43_performance_sensitivity.csv"
        pd.read_csv(path).iloc[:-1].to_csv(path, index=False)
        self.assertIn("Current inputs: stage43_performance_sensitivity.csv", self.failed_tables())

    def test_duplicate_scenario_row_detected(self):
        path = self.root / "reports/stage45_npv_summary.csv"
        table = pd.read_csv(path)
        pd.concat([table, table.iloc[:1]], ignore_index=True).to_csv(path, index=False)
        self.assertIn("Current inputs: stage45_npv_summary.csv", self.failed_tables())

    def test_edited_numeric_output_detected(self):
        self.change_cell("reports/stage44_learning_results.csv", "lcoe_eur_per_mwh", 1, row=14)
        self.assertIn("Current inputs: stage44_learning_results.csv", self.failed_tables())
        self.assertTrue(any("Changed output" in issue for issue in freshness_issues(self.root)))

    def test_missing_plot_detected(self):
        (self.root / "reports/stage45_npv_comparison.png").unlink()
        self.assertTrue(any("Missing output" in issue for issue in freshness_issues(self.root)))

    def test_changed_script_detected(self):
        script = self.root / "src/lcoe_model.py"
        script.write_text(script.read_text() + "\n# changed code\n")
        self.assertTrue(any("src/lcoe_model.py" in issue for issue in freshness_issues(self.root)))

    def test_failed_rebuild_record_not_accepted(self):
        path = self.root / SUMMARY
        record = json.loads(path.read_text())
        record["status"] = "failed"
        write_json(path, record)
        self.assertTrue(freshness_issues(self.root))

    def test_changed_review_evidence_rejected_without_overwrite(self):
        check_review_alignment(self.root)
        review = self.root / "reports/milestone_review.csv"
        before = review.read_bytes()
        self.change_cell("data/milestones.csv", "notes", "Changed source evidence")
        with self.assertRaisesRegex(ValueError, "Reviewed evidence changed"):
            check_review_alignment(self.root)
        self.assertEqual(review.read_bytes(), before)

    def test_standalone_integration_exits_nonzero_for_stale_revenue(self):
        self.change_cell("data/electricity_revenue_scenarios.csv",
                         "electricity_price_eur_per_mwh", 178.51)
        result = subprocess.run([sys.executable, "src/integrate_stage4.py"],
                                cwd=self.root, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        audit = json.loads((self.root / "reports/stage4_integration_audit.json").read_text())
        self.assertEqual(audit["status"], "FAIL")

    def test_failed_runner_invalidates_previous_success_record(self):
        (self.root / "data/technical_parameters.csv").unlink()
        result = subprocess.run([sys.executable, "src/run_stage34.py"],
                                cwd=self.root, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        record = json.loads((self.root / SUMMARY).read_text())
        self.assertEqual(record["status"], "failed")
        self.assertTrue(freshness_issues(self.root))


if __name__ == "__main__":
    unittest.main(verbosity=2)
