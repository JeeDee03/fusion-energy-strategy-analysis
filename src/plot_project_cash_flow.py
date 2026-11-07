
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"

summary = pd.read_csv(
    REPORTS / "stage45_npv_summary.csv"
)

annual = pd.read_csv(
    REPORTS / "stage45_annual_cash_flows.csv"
)

# ----------------------------------------
# Figure 1 — NPV by revenue scenario
# ----------------------------------------

fig, ax = plt.subplots(figsize=(9, 5))

labels = summary["scenario_name"]
values = summary["npv_eur"] / 1e9

ax.bar(labels, values)
ax.axhline(0, color="black", linewidth=1)

ax.set_ylabel("Project NPV (2024 EUR billion)")
ax.set_title(
    "Illustrative Stellaris Project NPV"
)

ax.tick_params(axis="x", rotation=25)
ax.grid(axis="y", alpha=0.25)

fig.tight_layout()

fig.savefig(
    REPORTS / "stage45_npv_comparison.png",
    dpi=200
)

# ----------------------------------------
# Figure 2 — Cumulative discounted cash flow
# ----------------------------------------

fig2, ax2 = plt.subplots(figsize=(9, 5))

for name, group in annual.groupby(
    "scenario_name", sort=False
):
    ordered = group.sort_values("year")

    ax2.plot(
        ordered["year"],
        ordered["cumulative_discounted_eur"] / 1e9,
        label=name
    )

ax2.axhline(0, color="black", linewidth=1)

ax2.set_xlabel("Years since initial investment")
ax2.set_ylabel(
    "Cumulative discounted cash flow (2024 EUR billion)"
)

ax2.set_title(
    "Project Discounted Cash Flow"
)

ax2.legend()
ax2.grid(True, alpha=0.25)

fig2.tight_layout()

fig2.savefig(
    REPORTS / "stage45_cumulative_cash_flow.png",
    dpi=200
)

print("Stage 4.5 figures saved.")
plt.show()
