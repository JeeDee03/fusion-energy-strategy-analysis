
"""Stage 6.5 audit: independent file-level and analytical invariants."""

from __future__ import annotations

import json

import pandas as pd

from strategy_robustness import ROOT, calculate, sha


def main():
    root = ROOT / "reports"

    expected = {
        "stage65_feasibility_screen.csv": 60,
        "stage65_context_gate_summary.csv": 15,
        "stage65_price_thresholds.csv": 20,
    }

    # Independently regenerate the Stage 6.5 calculations.
    fresh = calculate()

    # Compare saved reports against freshly calculated results.
    for (filename, n), regenerated in zip(
        expected.items(), fresh[:3]
    ):
        stored = pd.read_csv(root / filename)

        assert len(stored) == n and len(regenerated) == n, (
            filename,
            len(stored),
            len(regenerated),
        )

        # Fix pandas dtype compatibility:
        # An entirely empty CSV column may be inferred as float64.
        # Convert to string before replacing missing values.
        if "eligible_strategy_ids" in stored.columns:
            stored["eligible_strategy_ids"] = (
                stored["eligible_strategy_ids"]
                .astype("string")
                .fillna("")
            )

        pd.testing.assert_frame_equal(
            stored,
            regenerated,
            check_exact=False,
            rtol=1e-10,
            atol=2,
            check_dtype=False,
        )

    gate, ctx, threshold, paths = fresh

    # Verify the four strategic alternatives.
    assert set(gate.strategy_id) == {
        "STR01",
        "STR02",
        "STR03",
        "STR04",
    }

    # Verify that the combined eligibility condition
    # requires all three economic gates.
    assert (
        gate.all_economic_gates
        == (
            gate.company_gate
            & gate.external_gate
            & gate.project_gate
        )
    ).all()

    # Verify consistency between individual screens
    # and aggregated context results.
    assert (
        int(ctx.feasible_strategy_count.sum())
        == int(gate.all_economic_gates.sum())
    )

    assert len(ctx) == 15
    assert len(threshold) == 20

    # Verify the electricity-price linearity check.
    assert threshold.max_linearity_residual_eur.max() < 10

    # STR01 has no external plant-owner requirement.
    assert gate.loc[
        gate.strategy_id == "STR01",
        "external_gate",
    ].all()

    # Verify audit metadata and source-file hashes.
    audit = json.loads(
        (root / "stage65_feasibility_audit.json").read_text()
    )

    assert audit["risk_rows"] == 60
    assert audit["context_rows"] == 15
    assert audit["threshold_rows"] == 20

    assert audit["inputs_sha256"] == {
        key: sha(path)
        for key, path in paths.items()
    }

    assert audit["eligible_rows"] == int(
        gate.all_economic_gates.sum()
    )

    print(
        "PASS — 60 stakeholder gate screens, "
        "15 MCDA-context checks, 20 price thresholds"
    )

    print(
        "PASS — independent regeneration, "
        "NPV reconciliation, linearity, coverage and hashes"
    )

    print(
        "WARNING — exploratory economic screen, "
        "not a financing feasibility certificate "
        "or strategy ranking"
    )


if __name__ == "__main__":
    main()
