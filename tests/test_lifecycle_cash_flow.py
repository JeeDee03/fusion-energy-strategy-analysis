"""Independent timing checks and lifecycle regression tests in temporary copies."""

from decimal import Decimal, localcontext
import json
import math
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from lifecycle_cash_flow import calculate_lifecycle, build_lifecycle_results, reconciliation_check
from project_cash_flow import calculate_project_cash_flow
from stage34_provenance import INPUTS

PROJECT = Path(__file__).resolve().parents[1]
CASE = {"capex_eur_million": 1, "net_power_mwe": 1, "capacity_factor": .5,
        "fixed_opex_eur_million_per_year": .01, "variable_opex_eur_per_mwh": 2,
        "plant_lifetime_years": 2, "real_discount_rate": .08}
CONFIG = {"scenario_id": "TEST", "scenario_name": "Timing test", "generation_mode": "legacy_constant_cf",
          "engineering_case_id": "", "price_scenario_id": "REV004", "construction_years": 0,
          "construction_spend_shares": [1], "replacement_cost_eur_million": 0,
          "opex_boundary": "legacy_aggregate", "assumption_class": "analyst_scenario", "notes": "Synthetic test"}
ENG = {"maintenance_basis": "full_power_exposure", "interval_years": 2,
       "major_outage_months": 12, "other_outage_fraction": 0,
       "operating_load_fraction": 1, "gross_electric_mwe": 1,
       "auxiliary_fraction": 0, "target_capacity_factor": .5}
EVENT_CONFIG = {**CONFIG, "generation_mode": "engineering_events", "engineering_case_id": "SYNTHETIC",
                "opex_boundary": "routine_excludes_major_replacements", "replacement_cost_eur_million": .1}


class LifecycleMathTests(unittest.TestCase):
    def test_legacy_special_case_matches_existing_npv_and_lcoe(self):
        _, _, metrics = calculate_lifecycle(CASE, 150, CONFIG)
        _, previous = calculate_project_cash_flow(CASE, 150)
        self.assertAlmostEqual(metrics["npv_eur"], previous["npv_eur"], delta=1e-7)
        self.assertAlmostEqual(metrics["break_even_eur_2024_per_mwh"], previous["lcoe_eur_per_mwh"])

    def test_construction_spending_precedes_revenue_and_sums_to_capex(self):
        cash, _, metrics = calculate_lifecycle(CASE, 150, {**CONFIG, "construction_years": 2,
                                                        "construction_spend_shares": [.4, .6]})
        self.assertEqual(cash["construction_capex_eur"].sum(), 1000000)
        self.assertEqual(cash.loc[0, "construction_capex_eur"], 400000)
        self.assertEqual(cash.loc[1, "construction_capex_eur"], 600000)
        self.assertEqual(cash.loc[:2, "revenue_eur"].sum(), 0)
        self.assertGreater(cash.loc[3, "revenue_eur"], 0)
        self.assertEqual(metrics["first_revenue_model_year"], 3)

    def test_independent_decimal_staged_construction_npv(self):
        config = {**CONFIG, "construction_years": 2, "construction_spend_shares": [.4, .6]}
        _, _, metrics = calculate_lifecycle(CASE, 150, config)
        with localcontext() as context:
            context.prec = 60
            growth = Decimal("1.08")
            annual_cash = Decimal(4380) * (Decimal(150) - 2) - 10000
            expected = -Decimal(400000) - Decimal(600000) / growth + annual_cash / growth**3 + annual_cash / growth**4
        self.assertAlmostEqual(metrics["npv_eur"], float(expected), delta=1e-7)

    def test_explicit_outage_removes_generation_once(self):
        cash, events, metrics = calculate_lifecycle({**CASE, "plant_lifetime_years": 5}, 150, EVENT_CONFIG, ENG)
        self.assertEqual(cash["energy_mwh"].tolist(), [0, 8760, 8760, 0, 8760, 8760])
        self.assertEqual(metrics["total_generation_mwh"], 4 * 8760)
        self.assertEqual(len(events), 1)  # No replacement purchased at retirement t=5.

    def test_reference_cf_is_not_multiplied_into_explicit_schedule(self):
        _, _, first = calculate_lifecycle({**CASE, "capacity_factor": .1}, 150, EVENT_CONFIG, ENG)
        _, _, second = calculate_lifecycle({**CASE, "capacity_factor": .9}, 150, EVENT_CONFIG, ENG)
        self.assertEqual(first["total_generation_mwh"], second["total_generation_mwh"])

    def test_fractional_outage_splits_annual_energy_correctly(self):
        engine = {**ENG, "interval_years": 1.5, "major_outage_months": 12}
        cash, events, _ = calculate_lifecycle({**CASE, "plant_lifetime_years": 3}, 150, EVENT_CONFIG, engine)
        self.assertEqual(cash["energy_mwh"].tolist(), [0, 8760, 4380, 4380])
        self.assertEqual(events.iloc[0]["model_time_years"], 1.5)

    def test_replacement_discount_uses_exact_start_not_annual_bucket(self):
        engine = {**ENG, "interval_years": 1.5}
        cash, events, metrics = calculate_lifecycle({**CASE, "plant_lifetime_years": 3}, 150, EVENT_CONFIG, engine)
        expected = 100000 / 1.08**1.5
        self.assertAlmostEqual(metrics["pv_replacement_cost_eur"], expected, delta=1e-8)
        self.assertEqual(events.iloc[0]["report_year"], 2)
        self.assertAlmostEqual(cash.loc[2, "discounted_replacement_cost_eur"], expected)
        self.assertNotAlmostEqual(expected, 100000 / 1.08**2, delta=1)

    def test_no_replacement_cost_at_retirement(self):
        _, events, metrics = calculate_lifecycle(CASE, 150, EVENT_CONFIG, ENG)
        self.assertEqual(len(events), 0)
        self.assertEqual(metrics["pv_replacement_cost_eur"], 0)

    def test_partial_final_outage_charged_at_start(self):
        engine = {**ENG, "interval_years": 1.5, "major_outage_months": 12}
        cash, events, _ = calculate_lifecycle(CASE, 150, EVENT_CONFIG, engine)
        self.assertEqual(events.iloc[0]["outage_years_within_life"], .5)
        self.assertEqual(events.iloc[0]["replacement_cost_eur"], 100000)
        self.assertEqual(cash["energy_mwh"].sum(), 1.5 * 8760)

    def test_higher_replacement_cost_reduces_npv_without_changing_energy(self):
        case = {**CASE, "plant_lifetime_years": 5}
        _, _, low = calculate_lifecycle(case, 150, EVENT_CONFIG, ENG)
        _, _, high = calculate_lifecycle(case, 150, {**EVENT_CONFIG, "replacement_cost_eur_million": .2}, ENG)
        self.assertEqual(low["total_generation_mwh"], high["total_generation_mwh"])
        self.assertLess(high["npv_eur"], low["npv_eur"])
        self.assertGreater(high["break_even_eur_2024_per_mwh"], low["break_even_eur_2024_per_mwh"])

    def test_zero_npv_at_discounted_cost_over_energy_price(self):
        for config, eng in ((CONFIG, None), ({**CONFIG, "construction_years": 2, "construction_spend_shares": [.4, .6]}, None), (EVENT_CONFIG, ENG)):
            with self.subTest(mode=config["generation_mode"]):
                case = {**CASE, "plant_lifetime_years": 5}
                _, _, metrics = calculate_lifecycle(case, 150, config, eng)
                _, _, at_break_even = calculate_lifecycle(case, metrics["break_even_eur_2024_per_mwh"], config, eng)
                self.assertLess(abs(at_break_even["npv_eur"]), 1e-6)

    def test_zero_discount_and_negative_prices_are_supported(self):
        case = {**CASE, "real_discount_rate": 0, "plant_lifetime_years": 5}
        cash, _, metrics = calculate_lifecycle(case, -10, EVENT_CONFIG, ENG)
        self.assertAlmostEqual(metrics["npv_eur"], cash["cash_flow_eur"].sum())
        self.assertLess(metrics["npv_eur"], 0)

    def test_spending_schedule_errors_rejected(self):
        for changes in ({"construction_years": -1}, {"construction_years": 2.5},
                        {"construction_spend_shares": [.4, .6]}, {"construction_spend_shares": [.9]},
                        {"construction_spend_shares": [True]}, {"replacement_cost_eur_million": float("nan")}):
            with self.subTest(changes=changes):
                with self.assertRaises(ValueError):
                    calculate_lifecycle(CASE, 150, {**CONFIG, **changes})

    def test_ambiguous_cost_or_generation_boundaries_rejected(self):
        for config, eng in (({**CONFIG, "replacement_cost_eur_million": 1}, None),
                            ({**EVENT_CONFIG, "opex_boundary": "legacy_aggregate"}, ENG),
                            (EVENT_CONFIG, None), (CONFIG, ENG),
                            ({**CONFIG, "unsupported_cf_multiplier": .9}, None)):
            with self.subTest(mode=config["generation_mode"]):
                with self.assertRaises(ValueError):
                    calculate_lifecycle(CASE, 150, config, eng)


class LifecycleIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in INPUTS:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(PROJECT / name, target)
        (self.root / "reports").mkdir(exist_ok=True)

    def test_all_six_cases_and_special_case_reconcile(self):
        summary, annual, events, audit = build_lifecycle_results(self.root)
        self.assertEqual(len(summary), 6)
        self.assertTrue(audit["legacy_special_case_matches"])
        self.assertEqual(len(events), 28)
        self.assertEqual(annual["scenario_id"].nunique(), 6)

    def test_delay_preserves_spend_timing_and_discount_shifts_operating_value(self):
        summary, _, _, _ = build_lifecycle_results(self.root)
        rows = summary.set_index("scenario_id")
        normal, delayed = rows.loc["LC004"], rows.loc["LC006"]
        self.assertEqual(normal["pv_construction_capex_eur"], delayed["pv_construction_capex_eur"])
        self.assertEqual(normal["total_generation_mwh"], delayed["total_generation_mwh"])
        self.assertLess(delayed["npv_eur"], normal["npv_eur"])
        self.assertAlmostEqual(delayed["pv_generation_mwh"] / normal["pv_generation_mwh"], 1 / 1.08**2)

    def test_stale_replacement_cost_detected(self):
        summary, annual, events, _ = build_lifecycle_results(self.root)
        for name, table in (("lifecycle_summary.csv", summary), ("lifecycle_annual_cash_flows.csv", annual), ("lifecycle_replacement_events.csv", events)):
            table.to_csv(self.root / "reports" / name, index=False)
        self.assertTrue(reconciliation_check(self.root)[0])
        path = self.root / "data/lifecycle_cash_flow_cases.json"
        source = json.loads(path.read_text())
        source["cases"][3]["replacement_cost_eur_million"] = 700
        path.write_text(json.dumps(source))
        self.assertFalse(reconciliation_check(self.root)[0])

    def test_duplicate_scenario_id_rejected(self):
        path = self.root / "data/lifecycle_cash_flow_cases.json"
        source = json.loads(path.read_text())
        source["cases"][1]["scenario_id"] = "LC001"
        path.write_text(json.dumps(source))
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            build_lifecycle_results(self.root)

    def test_source_input_is_not_rewritten(self):
        path = self.root / "data/lifecycle_cash_flow_cases.json"
        before = path.read_bytes()
        build_lifecycle_results(self.root)
        self.assertEqual(path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
