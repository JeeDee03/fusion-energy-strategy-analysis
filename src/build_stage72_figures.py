
"""Stage 7.2.4 — Publication figure generation.

Reads retained research CSVs without modifying source reports.
Creates descriptive graphics, not empirical validation.
"""

from pathlib import Path
import hashlib
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
OUT = ROOT / "paper" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

sources = {}

def read_csv(name):
    path = REPORTS / name
    if not path.is_file():
        raise FileNotFoundError(f"Required research artifact: {path}")
    sources[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return pd.read_csv(path)

def save(fig, name):
    path = OUT / name
    fig.savefig(path, dpi=240, bbox_inches="tight")
    plt.close(fig)
    print(f"Created: {path.relative_to(ROOT)}")

def numeric(df, field):
    if field not in df:
        raise ValueError(f"Missing field: {field}")
    values = pd.to_numeric(df[field], errors="raise")
    if not np.isfinite(values).all():
        raise ValueError(f"Nonfinite values: {field}")
    return values

# -------------------------------------------------
# FIGURE 1 — Engineering-constrained capacity factor
# -------------------------------------------------

engineering = read_csv("engineering_generation_scenarios.csv")
assert len(engineering) == 7

cf = numeric(engineering, "derived_capacity_factor") * 100
target = numeric(engineering, "target_capacity_factor") * 100

fig, ax = plt.subplots(figsize=(10, 5))
x = np.arange(len(engineering))

ax.bar(x, cf, label="Derived capacity factor")
ax.scatter(x, target, marker="x", s=65, label="Scenario target")

ax.set_xticks(x, engineering["scenario_id"])
ax.set_ylabel("Capacity factor (%)")
ax.set_xlabel("Engineering scenario")
ax.set_title("Engineering-constrained electricity availability")
ax.set_ylim(0, 105)
ax.legend()
ax.grid(axis="y", alpha=0.25)

fig.tight_layout()
save(fig, "figure01_engineering_capacity_factor.png")

# -------------------------------------------------
# FIGURE 2 — Lifecycle break-even electricity price
# -------------------------------------------------

lifecycle = read_csv("lifecycle_summary.csv")
assert len(lifecycle) == 6

price = numeric(lifecycle, "break_even_eur_2024_per_mwh")

fig, ax = plt.subplots(figsize=(10, 5))
x = np.arange(len(lifecycle))

bars = ax.bar(x, price)

ax.set_xticks(x, lifecycle["scenario_id"])
ax.set_xlabel("Lifecycle scenario")
ax.set_ylabel("Break-even electricity price (EUR_2024/MWh)")
ax.set_title("Lifecycle investment and replacement scenarios")
ax.grid(axis="y", alpha=0.25)

for bar, value in zip(bars, price):
    ax.annotate(
        f"{value:.1f}",
        (bar.get_x() + bar.get_width() / 2, bar.get_height()),
        xytext=(0, 4),
        textcoords="offset points",
        ha="center",
        fontsize=9,
    )

fig.tight_layout()
save(fig, "figure02_lifecycle_break_even.png")

# -------------------------------------------------
# FIGURE 3 — Monte Carlo refinement diagnostic
# -------------------------------------------------

seed_files = sorted(REPORTS.glob("stage52_summary_seed*_n*.csv"))

if not seed_files:
    raise FileNotFoundError("No Stage 5.2 summary files found")

frames = []
for path in seed_files:
    frame = read_csv(path.name)
    frames.append(frame)

monte = pd.concat(frames, ignore_index=True)

context = "GEN002_LC004_R05"
monte = monte.loc[monte["context_id"] == context].copy()

if monte.empty:
    raise ValueError(f"No Monte Carlo rows for {context}")

monte["sample_size"] = numeric(monte, "sample_size")
monte["seed"] = numeric(monte, "seed")
monte["median_price"] = numeric(
    monte, "lifecycle_break_even_p50"
)

if monte.duplicated(["seed", "sample_size"]).any():
    raise ValueError("Duplicate seed/sample-size summary records")

fig, ax = plt.subplots(figsize=(10, 5))

for seed, group in monte.groupby("seed"):
    group = group.sort_values("sample_size")
    ax.plot(
        group["sample_size"],
        group["median_price"],
        marker="o",
        label=f"Seed {int(seed)}",
    )

ax.set_xscale("log", base=2)
ax.set_xlabel("Monte Carlo samples per seed")
ax.set_ylabel("Median break-even price (EUR_2024/MWh)")
ax.set_title(f"Monte Carlo refinement diagnostic: {context}")
ax.legend()
ax.grid(alpha=0.25)

ax.text(
    0.01, -0.20,
    "Exploratory estimates; strict convergence criterion not satisfied.",
    transform=ax.transAxes,
    fontsize=9,
)

fig.tight_layout()
save(fig, "figure03_monte_carlo_refinement.png")

# -------------------------------------------------
# FIGURE 4 — Stakeholder economic feasibility matrix
# -------------------------------------------------

feasibility = read_csv("stage65_feasibility_screen.csv")
assert len(feasibility) == 60

strategies = ["STR01", "STR02", "STR03", "STR04"]

contexts = sorted(
    {
        (str(row.price_case), str(row.stress_id))
        for row in feasibility.itertuples()
    }
)

assert len(contexts) == 15

gate = feasibility["all_economic_gates"].astype(str).str.lower()

if not gate.isin(["true", "false"]).all():
    raise ValueError("Unexpected economic gate value")

feasibility = feasibility.copy()
feasibility["gate_bool"] = gate.eq("true")

matrix = np.zeros((len(strategies), len(contexts)))

for row in feasibility.itertuples():
    strategy = row.strategy_id
    key = (str(row.price_case), str(row.stress_id))

    if strategy not in strategies:
        raise ValueError(f"Unknown strategy: {strategy}")

    i = strategies.index(strategy)
    j = contexts.index(key)
    matrix[i, j] += int(row.gate_bool)

if matrix.max() > 1:
    raise ValueError("Duplicate strategy-context records")

fig, ax = plt.subplots(figsize=(12, 4.5))

im = ax.imshow(
    matrix,
    cmap="Greys",
    vmin=0,
    vmax=1,
    aspect="auto",
)

ax.set_yticks(range(len(strategies)), strategies)
ax.set_xticks(
    range(len(contexts)),
    [f"{p}\n{s}" for p, s in contexts],
    fontsize=8,
)

ax.set_ylabel("Commercialization strategy")
ax.set_xlabel("Price and stress context")
ax.set_title("Stakeholder economic feasibility screening")

for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        value = matrix[i, j]
        ax.text(
            j, i,
            "PASS" if value == 1 else "—",
            ha="center",
            va="center",
            fontsize=8,
            color="white" if value == 1 else "black",
        )

fig.colorbar(
    im, ax=ax,
    label="All economic gates satisfied",
    ticks=[0, 1],
)

fig.tight_layout()
save(fig, "figure04_strategy_feasibility.png")

# -------------------------------------------------
# VALIDATION AND MANIFEST
# -------------------------------------------------

assert int(feasibility["gate_bool"].sum()) == 0, (
    "Economic feasibility differs from retained Stage 6 finding"
)

manifest = {
    "stage": "7.2.4",
    "purpose": "Publication graphics from retained model outputs",
    "context": context,
    "source_sha256": sources,
    "figures": [
        "figure01_engineering_capacity_factor.png",
        "figure02_lifecycle_break_even.png",
        "figure03_monte_carlo_refinement.png",
        "figure04_strategy_feasibility.png",
    ],
    "limitations": [
        "Analyst-defined scenarios, not plant forecasts",
        "Strict Monte Carlo convergence not certified",
        "Feasibility restricted to 15 selected contexts",
    ],
}

(OUT / "figure_manifest.json").write_text(
    json.dumps(manifest, indent=2) + "\n",
    encoding="utf-8",
)

print("\nPASS — Four figures created from retained CSV data")
print("PASS — Source SHA256 manifest saved")
print("WARNING — Descriptive plotting is not model validation")
