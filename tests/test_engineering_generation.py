"""Generation identities, stale outputs and safe research numbering migration."""

import csv
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from engineering_generation import calculate_generation_case, build_generation_results, reconciliation_check
from migrate_research_numbering import migrate_research_numbering, OLD, NEW
from stage34_provenance import INPUTS

PROJECT = Path(__file__).resolve().parents[1]
BASE = {"maintenance_basis": "full_power_exposure", "interval_years": 4,
        "major_outage_months": 7, "other_outage_fraction": 0,
        "operating_load_fraction": 1, "gross_electric_mwe": 1250,
        "auxiliary_fraction": .2, "target_capacity_factor": .85}


class GenerationMathTests(unittest.TestCase):
    def test_full_power_upper_limit_matches_48_over_55(self):
        result = calculate_generation_case(BASE)
        self.assertAlmostEqual(result["derived_capacity_factor"], 48 / 55)
        self.assertEqual(result["net_rated_mwe"], 1000)

    def test_calendar_interval_includes_its_outage(self):
        result = calculate_generation_case({**BASE, "maintenance_basis": "calendar_cycle", "interval_years": 6})
        self.assertAlmostEqual(result["major_outage_availability"], 65 / 72)

    def test_full_power_years_are_not_fixed_calendar_years(self):
        result = calculate_generation_case({**BASE, "other_outage_fraction": .1, "operating_load_fraction": .9})
        self.assertAlmostEqual(result["operating_window_years"], 4 / .81)
        self.assertAlmostEqual(result["derived_capacity_factor"], .81 / (1 + .81 * 7 / 48))

    def test_other_losses_reduce_cf_but_delay_exposure_outage(self):
        high = calculate_generation_case(BASE)
        low = calculate_generation_case({**BASE, "other_outage_fraction": .1})
        self.assertLess(low["derived_capacity_factor"], high["derived_capacity_factor"])
        self.assertGreater(low["major_outage_availability"], high["major_outage_availability"])

    def test_auxiliaries_reduce_rating_once_not_cf_twice(self):
        first = calculate_generation_case(BASE)
        second = calculate_generation_case({**BASE, "auxiliary_fraction": .3})
        self.assertEqual(first["derived_capacity_factor"], second["derived_capacity_factor"])
        self.assertAlmostEqual(second["annual_net_energy_mwh"] / first["annual_net_energy_mwh"], .875)
        self.assertAlmostEqual(first["annual_net_energy_mwh"], 1000 * 8760 * 48 / 55)

    def test_95_percent_fails_even_ideal_five_month_case(self):
        result = calculate_generation_case({**BASE, "major_outage_months": 5, "target_capacity_factor": .95})
        self.assertAlmostEqual(result["derived_capacity_factor"], 48 / 53)
        self.assertFalse(result["target_met"])

    def test_two_month_improvement_can_conditionally_meet_95(self):
        result = calculate_generation_case({**BASE, "major_outage_months": 2,
                    "other_outage_fraction": .005, "operating_load_fraction": .995,
                    "target_capacity_factor": .95})
        self.assertTrue(result["target_met"])

    def test_target_does_not_replace_derived_generation(self):
        a = calculate_generation_case({**BASE, "target_capacity_factor": .8})
        b = calculate_generation_case({**BASE, "target_capacity_factor": .95})
        self.assertEqual(a["derived_capacity_factor"], b["derived_capacity_factor"])
        self.assertNotEqual(a["target_met"], b["target_met"])

    def test_zero_outage_can_reach_unit_cf(self):
        result = calculate_generation_case({**BASE, "major_outage_months": 0})
        self.assertEqual(result["derived_capacity_factor"], 1)

    def test_nonfinite_and_boolean_inputs_rejected(self):
        for field in BASE.keys() - {"maintenance_basis"}:
            for value in (float("nan"), float("inf"), None, True):
                with self.subTest(field=field, value=value):
                    with self.assertRaises(ValueError):
                        calculate_generation_case({**BASE, field: value})

    def test_invalid_ranges_and_basis_rejected(self):
        for changes in ({"interval_years": 0}, {"major_outage_months": -1},
                        {"other_outage_fraction": 1}, {"operating_load_fraction": 0},
                        {"operating_load_fraction": 1.1}, {"gross_electric_mwe": 0},
                        {"auxiliary_fraction": 1}, {"auxiliary_fraction": -.1},
                        {"target_capacity_factor": 1.1}, {"maintenance_basis": "unknown"},
                        {"maintenance_basis": "calendar_cycle", "interval_years": .5}):
            with self.subTest(changes=changes):
                with self.assertRaises(ValueError):
                    calculate_generation_case({**BASE, **changes})


class GenerationIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in INPUTS:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(PROJECT / name, target)
        (self.root / "reports").mkdir(exist_ok=True)

    def test_all_cases_and_deliberately_unmet_target_retained(self):
        result, audit = build_generation_results(self.root)
        self.assertEqual(len(result), 7)
        self.assertEqual(audit["targets_not_met"], 1)
        self.assertEqual(audit["targets_met"], 6)
        self.assertEqual(audit["beyond_documented_duration_cases"], 1)
        self.assertEqual(audit["status"], "PASS_WITH_LIMITATIONS")

    def test_higher_auxiliary_demand_increases_lcoe_at_fixed_capex(self):
        result, _ = build_generation_results(self.root)
        rows = result.set_index("scenario_id")
        self.assertEqual(rows.loc["GEN002", "capex_eur_million"], rows.loc["GEN007", "capex_eur_million"])
        self.assertGreater(rows.loc["GEN007", "lcoe_eur_2024_per_mwh"], rows.loc["GEN002", "lcoe_eur_2024_per_mwh"])

    def test_stale_engineering_input_is_detected(self):
        result, _ = build_generation_results(self.root)
        result.to_csv(self.root / "reports/engineering_generation_scenarios.csv", index=False)
        self.assertTrue(reconciliation_check(self.root)[0])
        path = self.root / "data/engineering_generation_cases.csv"
        with path.open(newline="") as handle:
            reader = csv.DictReader(handle)
            fields, rows = reader.fieldnames, list(reader)
        rows[1]["auxiliary_fraction"] = "0.25"
        with path.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        self.assertFalse(reconciliation_check(self.root)[0])

    def test_missing_case_output_is_detected(self):
        result, _ = build_generation_results(self.root)
        result.iloc[:-1].to_csv(self.root / "reports/engineering_generation_scenarios.csv", index=False)
        self.assertFalse(reconciliation_check(self.root)[0])


class ResearchNumberingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "research").mkdir()

    def test_rename_preserves_human_edits_and_updates_links(self):
        original = b"Research text\nHuman additions retained.\n"
        (self.root / "research" / OLD).write_bytes(original)
        (self.root / "README.md").write_text("Link: research/" + OLD)
        self.assertEqual(migrate_research_numbering(self.root), "renamed")
        self.assertEqual((self.root / "research" / NEW).read_bytes(), original)
        self.assertFalse((self.root / "research" / OLD).exists())
        self.assertIn(NEW, (self.root / "README.md").read_text())

    def test_rerun_is_idempotent(self):
        (self.root / "research" / NEW).write_text("Already correct")
        self.assertEqual(migrate_research_numbering(self.root), "already_correct")

    def test_conflicting_copies_are_not_overwritten(self):
        old = self.root / "research" / OLD
        new = self.root / "research" / NEW
        old.write_text("Human version A")
        new.write_text("Human version B")
        with self.assertRaises(ValueError):
            migrate_research_numbering(self.root)
        self.assertEqual(old.read_text(), "Human version A")
        self.assertEqual(new.read_text(), "Human version B")

    def test_identical_duplicate_is_removed_safely(self):
        for name in (OLD, NEW):
            (self.root / "research" / name).write_text("Same content")
        migrate_research_numbering(self.root)
        self.assertFalse((self.root / "research" / OLD).exists())
        self.assertEqual((self.root / "research" / NEW).read_text(), "Same content")

    def test_data_only_fixture_does_not_require_research_docs(self):
        self.assertEqual(migrate_research_numbering(self.root), "not_present")


if __name__ == "__main__":
    unittest.main(verbosity=2)
