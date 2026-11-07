"""Shared numerical contract for the current annual LCOE and project DCF.

Units are explicit in field names. No percentage, currency, or unit conversion
is guessed. Validation checks mathematical admissibility, not empirical realism.
"""

from decimal import Decimal
import math
from numbers import Real

ECONOMIC_FIELDS = (
    "capex_eur_million", "net_power_mwe", "capacity_factor",
    "fixed_opex_eur_million_per_year", "variable_opex_eur_per_mwh",
    "plant_lifetime_years", "real_discount_rate",
)


def finite_number(value, field, minimum=None, maximum=None,
                  minimum_inclusive=True, maximum_inclusive=True):
    """Return a finite float or raise a field-specific ValueError."""
    if isinstance(value, bool) or not isinstance(value, (str, Real, Decimal)):
        raise ValueError(f"{field}: expected a finite number, got {value!r}")
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{field}: expected a finite number, got {value!r}") from exc
    if not math.isfinite(number):
        raise ValueError(f"{field}: value must be finite, got {value!r}")
    if minimum is not None and (number < minimum or (number == minimum and not minimum_inclusive)):
        relation = ">=" if minimum_inclusive else ">"
        raise ValueError(f"{field}: value must be {relation} {minimum}, got {number}")
    if maximum is not None and (number > maximum or (number == maximum and not maximum_inclusive)):
        relation = "<=" if maximum_inclusive else "<"
        raise ValueError(f"{field}: value must be {relation} {maximum}, got {number}")
    return number


def positive_integer(value, field="plant_lifetime_years"):
    number = finite_number(value, field, minimum=0, minimum_inclusive=False)
    if not number.is_integer():
        raise ValueError(f"{field}: a positive whole number of years is required; got {value!r}")
    return int(number)


def validate_economic_case(row):
    """Normalize the seven required numerical fields without mutating input.

    Zero CAPEX/OPEX and zero discount rate are allowed. Power must be positive,
    0 < CF <= 1, and lifetime must be a positive integer number of years.
    Negative discount rates remain outside this model's declared boundary.
    """
    values = {}
    for field in ECONOMIC_FIELDS:
        try:
            values[field] = row[field]
        except (KeyError, IndexError, TypeError) as exc:
            raise ValueError(f"{field}: required economic input is missing") from exc
    checked = {
        "capex_eur_million": finite_number(values["capex_eur_million"], "capex_eur_million", minimum=0),
        "net_power_mwe": finite_number(values["net_power_mwe"], "net_power_mwe", minimum=0, minimum_inclusive=False),
        "capacity_factor": finite_number(values["capacity_factor"], "capacity_factor", minimum=0, maximum=1, minimum_inclusive=False),
        "fixed_opex_eur_million_per_year": finite_number(values["fixed_opex_eur_million_per_year"], "fixed_opex_eur_million_per_year", minimum=0),
        "variable_opex_eur_per_mwh": finite_number(values["variable_opex_eur_per_mwh"], "variable_opex_eur_per_mwh", minimum=0),
        "plant_lifetime_years": positive_integer(values["plant_lifetime_years"]),
        "real_discount_rate": finite_number(values["real_discount_rate"], "real_discount_rate", minimum=0),
    }
    return checked


def validate_price(price):
    # Zero and negative prices are legitimate revenue stress tests.
    return finite_number(price, "electricity_price_eur_per_mwh")
