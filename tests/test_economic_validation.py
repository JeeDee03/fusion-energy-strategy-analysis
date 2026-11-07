"""Numerical contracts and independent reference checks; no project data edits."""

from decimal import Decimal, localcontext
import math
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from economic_validation import ECONOMIC_FIELDS, validate_economic_case
from lcoe_model import calculate_lcoe, capital_recovery_factor
import project_cash_flow
from project_cash_flow import calculate_project_cash_flow

BASE = {
    "capex_eur_million": 12000, "net_power_mwe": 1000,
    "capacity_factor": .85, "fixed_opex_eur_million_per_year": 200,
    "variable_opex_eur_per_mwh": 5, "plant_lifetime_years": 35,
    "real_discount_rate": .08,
}


class EconomicValidationTests(unittest.TestCase):
    def assert_both_reject(self, case, field):
        for name, function in (("LCOE", lambda: calculate_lcoe(case)),
                               ("DCF", lambda: calculate_project_cash_flow(case, 170))):
            with self.subTest(model=name):
                with self.assertRaisesRegex(ValueError, field):
                    function()

    def test_every_missing_field_is_rejected_by_both_models(self):
        for field in ECONOMIC_FIELDS:
            with self.subTest(field=field):
                case = dict(BASE)
                del case[field]
                self.assert_both_reject(case, field)

    def test_nonfinite_values_rejected_in_every_field(self):
        for field in ECONOMIC_FIELDS:
            for value in (float("nan"), float("inf"), -float("inf"),
                          "NaN", "Infinity", Decimal("NaN")):
                with self.subTest(field=field, value=value):
                    self.assert_both_reject({**BASE, field: value}, field)

    def test_missing_nonnumeric_and_boolean_values_rejected(self):
        for field in ECONOMIC_FIELDS:
            for value in (None, "", "unknown", True, False, np.bool_(True), pd.NA):
                with self.subTest(field=field, value=repr(value)):
                    self.assert_both_reject({**BASE, field: value}, field)

    def test_negative_costs_rejected(self):
        for field in ("capex_eur_million", "fixed_opex_eur_million_per_year",
                      "variable_opex_eur_per_mwh"):
            with self.subTest(field=field):
                self.assert_both_reject({**BASE, field: -1}, field)

    def test_nonpositive_power_rejected(self):
        for value in (0, -1):
            self.assert_both_reject({**BASE, "net_power_mwe": value}, "net_power_mwe")

    def test_capacity_factor_bounds_rejected(self):
        for value in (0, -.1, 1.01, 85):
            self.assert_both_reject({**BASE, "capacity_factor": value}, "capacity_factor")

    def test_fractional_and_nonpositive_lifetime_rejected(self):
        for value in (35.9, "35.9", 0, -1):
            self.assert_both_reject({**BASE, "plant_lifetime_years": value}, "plant_lifetime_years")

    def test_negative_discount_rate_rejected(self):
        self.assert_both_reject({**BASE, "real_discount_rate": -.01}, "real_discount_rate")

    def test_percent_strings_are_not_silently_converted(self):
        self.assert_both_reject({**BASE, "capacity_factor": "85%"}, "capacity_factor")
        self.assert_both_reject({**BASE, "real_discount_rate": "8%"}, "real_discount_rate")

    def test_numeric_strings_and_integral_float_lifetime_accepted(self):
        case = {key: str(value) for key, value in BASE.items()}
        case["plant_lifetime_years"] = "35.0"
        output = calculate_lcoe(case)
        self.assertAlmostEqual(output["lcoe_eur_per_mwh"], 170.14090447598142, places=10)
        cash, _ = calculate_project_cash_flow(case, "170")
        self.assertEqual(len(cash), 36)

    def test_input_mapping_is_not_mutated(self):
        case = dict(BASE)
        before = dict(case)
        validate_economic_case(case)
        calculate_lcoe(case)
        calculate_project_cash_flow(case, 200)
        self.assertEqual(case, before)

    def test_invalid_prices_rejected(self):
        for value in (None, "", "unknown", True, np.bool_(True),
                      float("nan"), float("inf"), -float("inf")):
            with self.subTest(value=repr(value)):
                with self.assertRaisesRegex(ValueError, "electricity_price_eur_per_mwh"):
                    calculate_project_cash_flow(BASE, value)

    def test_zero_and_negative_prices_are_valid_stress_tests(self):
        for price in (0, -50):
            cash, metrics = calculate_project_cash_flow(BASE, price)
            self.assertTrue(np.isfinite(cash.to_numpy()).all())
            self.assertLess(metrics["npv_eur"], 0)
            self.assertEqual(metrics["annual_revenue_eur"], 7446000 * price)

    def test_zero_costs_and_full_capacity_factor_accepted(self):
        case = {**BASE, "capex_eur_million": 0, "capacity_factor": 1,
                "fixed_opex_eur_million_per_year": 0, "variable_opex_eur_per_mwh": 0}
        self.assertEqual(calculate_lcoe(case)["lcoe_eur_per_mwh"], 0)
        _, metrics = calculate_project_cash_flow(case, 0)
        self.assertEqual(metrics["npv_eur"], 0)

    def test_independent_decimal_reference_lcoe(self):
        with localcontext() as ctx:
            ctx.prec = 60
            rate = Decimal(".08")
            crf = rate / (1 - (1 + rate) ** -35)
            expected = (Decimal(12000000000) * crf + Decimal(200000000)) / Decimal(7446000) + 5
        self.assertAlmostEqual(calculate_lcoe(BASE)["lcoe_eur_per_mwh"], float(expected), places=10)

    def test_independent_decimal_project_npv(self):
        with localcontext() as ctx:
            ctx.prec = 60
            annual_cash = Decimal(7446000) * (Decimal(200) - 5) - 200000000
            expected = -Decimal(12000000000) + sum(
                annual_cash / Decimal("1.08") ** year for year in range(1, 36))
        _, metrics = calculate_project_cash_flow(BASE, 200)
        self.assertAlmostEqual(metrics["npv_eur"], float(expected), delta=.0001)

    def test_zero_discount_rate_hand_calculation(self):
        case = {"capex_eur_million": 1, "net_power_mwe": 1,
                "capacity_factor": .5, "fixed_opex_eur_million_per_year": .01,
                "variable_opex_eur_per_mwh": 2, "plant_lifetime_years": 2,
                "real_discount_rate": 0}
        expected_lcoe = (1000000 / 2 + 10000) / 4380 + 2
        self.assertAlmostEqual(calculate_lcoe(case)["lcoe_eur_per_mwh"], expected_lcoe)
        cash, metrics = calculate_project_cash_flow(case, 150)
        self.assertEqual(metrics["npv_eur"], 276480)
        self.assertEqual(cash.iloc[0]["investment_eur"], 1000000)
        self.assertTrue((cash.iloc[1:]["investment_eur"] == 0).all())

    def test_zero_npv_at_lcoe_across_valid_cases(self):
        for changes in ({}, {"real_discount_rate": 0}, {"real_discount_rate": 1e-18},
                        {"plant_lifetime_years": 1}, {"capacity_factor": 1},
                        {"net_power_mwe": 800}, {"variable_opex_eur_per_mwh": 0}):
            with self.subTest(changes=changes):
                case = {**BASE, **changes}
                price = calculate_lcoe(case)["lcoe_eur_per_mwh"]
                _, metrics = calculate_project_cash_flow(case, price)
                self.assertLess(abs(metrics["npv_eur"]), .001)

    def test_crf_near_zero_rate_is_stable(self):
        rate = 1e-18
        with localcontext() as ctx:
            ctx.prec = 80
            r = Decimal("1e-18")
            expected = r / (1 - (1 + r) ** -35)
        result = capital_recovery_factor(rate, 35)
        self.assertTrue(math.isfinite(result))
        self.assertAlmostEqual(result, float(expected), places=15)
        self.assertEqual(capital_recovery_factor(0, 20), .05)

    def test_crf_validates_direct_arguments(self):
        for rate, lifetime in ((float("nan"), 35), (float("inf"), 35), (-.01, 35),
                               (.08, 35.9), (.08, 0), (True, 35)):
            with self.subTest(rate=rate, lifetime=lifetime):
                with self.assertRaises(ValueError):
                    capital_recovery_factor(rate, lifetime)

    def test_overflow_and_underflow_results_rejected(self):
        for changes in ({"capex_eur_million": 1e308},
                        {"net_power_mwe": 1e308},
                        {"fixed_opex_eur_million_per_year": 1e308},
                        {"net_power_mwe": 1e-300, "capacity_factor": 1e-300}):
            with self.subTest(changes=changes):
                for model in (lambda: calculate_lcoe({**BASE, **changes}),
                              lambda: calculate_project_cash_flow({**BASE, **changes}, 170)):
                    with self.assertRaises(ValueError):
                        model()

    def test_large_discount_factor_does_not_overflow(self):
        case = {**BASE, "real_discount_rate": 1e308, "capex_eur_million": 0,
                "fixed_opex_eur_million_per_year": 0, "variable_opex_eur_per_mwh": 0}
        cash, metrics = calculate_project_cash_flow(case, 50)
        self.assertTrue(np.isfinite(cash.to_numpy()).all())
        self.assertTrue(math.isfinite(metrics["npv_eur"]))

    def test_reference_loader_rejects_fractional_lifetime(self):
        row = {**BASE, "scenario_id": "CAL002", "capex_eur_per_kwe": 12000,
               "plant_lifetime_years": 35.9}
        with tempfile.TemporaryDirectory() as name:
            folder = Path(name)
            pd.DataFrame([row]).to_csv(folder / "lcoe_scenarios_stage42.csv", index=False)
            with patch.object(project_cash_flow, "DATA", folder):
                with self.assertRaisesRegex(ValueError, "plant_lifetime_years"):
                    project_cash_flow.load_reference_case()


if __name__ == "__main__":
    unittest.main(verbosity=2)
