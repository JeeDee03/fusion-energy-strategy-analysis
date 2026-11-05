
import numpy as np

from project_cash_flow import (
    load_reference_case,
    calculate_project_cash_flow,
)


def main():
    case = load_reference_case()

    # 1. At LCOE, the project NPV should equal zero
    _, reference = calculate_project_cash_flow(
        case, 170
    )

    break_even_price = reference[
        "break_even_price_eur_per_mwh"
    ]

    at_break_even, metrics = (
        calculate_project_cash_flow(
            case, break_even_price
        )
    )

    assert abs(metrics["npv_eur"]) < 1.0

    # 2. Prices below break-even should give negative NPV
    _, below = calculate_project_cash_flow(
        case, break_even_price - 10
    )
    assert below["npv_eur"] < 0

    # 3. Prices above break-even should give positive NPV
    _, above = calculate_project_cash_flow(
        case, break_even_price + 10
    )
    assert above["npv_eur"] > 0

    # 4. Verify annual net generation
    expected_energy = 1000 * 8760 * 0.85

    assert np.isclose(
        metrics["annual_energy_mwh"],
        expected_energy
    )

    # 5. Year-zero investment is recorded once
    assert len(at_break_even) == 36

    assert np.isclose(
        at_break_even.iloc[0]["cash_flow_eur"],
        -12e9
    )

    assert (
        at_break_even.iloc[1:]["investment_eur"]
        == 0
    ).all()

    # 6. Discounted cash flows sum to reported NPV
    assert np.isclose(
        at_break_even[
            "discounted_cash_flow_eur"
        ].sum(),
        metrics["npv_eur"],
        atol=1.0
    )

    print("All Stage 4.5 validation checks passed.")
    print(f"Break-even price: EUR {break_even_price:.2f}/MWh")
    print(f"NPV at break-even: EUR {metrics['npv_eur']:.2f}")


if __name__ == "__main__":
    main()
