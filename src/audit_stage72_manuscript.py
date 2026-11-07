"""Stage 7.2.8 — Read-only manuscript QA.

Validates file references and selected numerical claims.
Does not certify source truth or publication readiness.
"""

from pathlib import Path
import csv
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
REPORTS = ROOT / "reports"
MANUSCRIPT = PAPER / "manuscript.md"

errors = []
warnings = []
passed = []

def check(condition, message):
    (passed if condition else errors).append(message)

def csv_rows(filename):
    with (REPORTS / filename).open(
        newline="", encoding="utf-8-sig"
    ) as file:
        return list(csv.DictReader(file))

def source_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

if not MANUSCRIPT.is_file():
    raise SystemExit("ERROR: paper/manuscript.md missing")

text = MANUSCRIPT.read_text(encoding="utf-8")

# 1. Manuscript organization
sections = [
    "Abstract",
    "Introduction",
    "Research Methodology",
    "Results",
    "Discussion",
    "Research Limitations",
    "Conclusion",
    "References and Data Availability",
]

headings = re.findall(r"^##\s+(.+)$", text, re.MULTILINE)

for section in sections:
    matches = [
        name for name in headings
        if section.lower() in name.lower()
    ]
    check(len(matches) == 1, f"Section: {section}")

# 2. Figure references
expected_figures = [
    "figure01_engineering_capacity_factor.png",
    "figure02_lifecycle_break_even.png",
    "figure03_monte_carlo_refinement.png",
    "figure04_strategy_feasibility.png",
]

images = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
image_names = [Path(item).name for item in images]

for filename in expected_figures:
    check(
        image_names.count(filename) == 1,
        f"Figure referenced once: {filename}"
    )
    check(
        (PAPER / "figures" / filename).is_file(),
        f"Figure exists: {filename}"
    )

for image_path in images:
    check(
        (PAPER / image_path).is_file(),
        f"Markdown image path: {image_path}"
    )

# 3. Reference files and local Markdown links
for filename in ("references.md", "citation_map.md"):
    check(
        (PAPER / filename).is_file(),
        f"Reference document: {filename}"
    )

links = re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", text)

for target in links:
    if target.startswith(("http://", "https://", "#", "mailto:")):
        continue
    path = target.split("#", 1)[0]
    if path:
        check(
            (PAPER / path).is_file(),
            f"Local Markdown link: {target}"
        )

# 4. Selected numerical evidence
stage4 = csv_rows("stage4_integrated_summary.csv")
metrics = {
    row["metric"]: float(row["value"])
    for row in stage4
}

lifecycle = {
    row["scenario_id"]: row
    for row in csv_rows("lifecycle_summary.csv")
}

feasibility = csv_rows("stage65_feasibility_screen.csv")
learning = csv_rows("stage44_learning_results.csv")

lcoe = metrics["Reference LCOE"]
lc004 = float(
    lifecycle["LC004"]["break_even_eur_2024_per_mwh"]
)
initial_capex = metrics["Reference CAPEX"]
learned_capex = metrics["Minimum learned CAPEX"]
learning_reduction = (
    1 - learned_capex / initial_capex
) * 100

eligible = sum(
    str(row["all_economic_gates"]).strip().lower()
    == "true"
    for row in feasibility
)

# Exact values from project outputs
check(
    abs(lcoe - 170.140904) < 0.001,
    "Reference LCOE matches expected scenario anchor"
)
check(
    abs(lc004 - 213.415844) < 0.001,
    "LC004 matches expected scenario anchor"
)
check(
    abs(learning_reduction - 14.76) < 0.02,
    "Learning reduction matches expected scenario anchor"
)
check(
    len(feasibility) == 60 and eligible == 0,
    "Stage 6: zero of 60 scenarios eligible"
)

# Ensure headline numbers appear in manuscript
check("170.14" in text, "Manuscript mentions reference LCOE")
check("213.42" in text, "Manuscript mentions LC004 result")
check("14.76" in text, "Manuscript mentions learning result")

if not ("60" in text and "none" in text.lower()):
    warnings.append(
        "Confirm Stage 6 zero-of-60 finding is clearly worded."
    )

# 5. Hypothesis framing
for hypothesis in ("H1", "H2", "H3"):
    check(
        hypothesis in text,
        f"Hypothesis present: {hypothesis}"
    )

for phrase in ("convergence", "assumption", "limitations"):
    check(
        phrase in text.lower(),
        f"Research limitation vocabulary: {phrase}"
    )

# 6. References and citation identifiers
reference_ids = set()

for filename in ("references.md",):
    path = PAPER / filename
    if path.is_file():
        reference_ids.update(
            re.findall(
                r"^##\s+([A-Za-z][A-Za-z0-9_]*)\s*$",
                path.read_text(encoding="utf-8"),
                re.MULTILINE
            )
        )

# Citation syntax: [BPF03], [EC001], etc.
citations = set(
    re.findall(
        r"\[([A-Za-z]{1,5}\d{2,3})\]",
        text
    )
)

for cid in sorted(citations):
    check(
        cid in reference_ids,
        f"Citation identifier resolves: {cid}"
    )

if len(citations) < 3:
    warnings.append(
        "Fewer than three distinct source-ID citations "
        "are present in the manuscript. Perform a "
        "paragraph-level citation review."
    )

# 7. Figure provenance
manifest_path = PAPER / "figures" / "figure_manifest.json"
if manifest_path.is_file():
    manifest = json.loads(manifest_path.read_text())
    for filename, expected_hash in manifest.get(
        "source_sha256", {}
    ).items():
        source = REPORTS / filename
        check(
            source.is_file()
            and source_hash(source) == expected_hash,
            f"Figure source hash: {filename}"
        )
else:
    errors.append("Figure manifest missing")

# 8. Warnings requiring editorial review
warnings.extend([
    "Scientific claims require manual source-to-paragraph review.",
    "Bibliographic records are not all externally verified.",
    "Monte Carlo convergence must be checked against "
    "Stage 5 audit records, not visual appearance alone.",
    "Model validation does not certify economic bankability.",
])

status = (
    "TECHNICAL_CHECKS_PASSED_WITH_EDITORIAL_REVIEW"
    if not errors else "TECHNICAL_CHECKS_FAILED"
)

lines = [
    "# Stage 7.2.8 — Manuscript Audit",
    "",
    f"**Status:** {status}",
    f"**Passed checks:** {len(passed)}",
    f"**Failed checks:** {len(errors)}",
    f"**Review warnings:** {len(warnings)}",
    "",
    "## Passed Checks",
    "",
] + [f"- {item}" for item in passed]

lines += ["", "## Failed Checks", ""]
lines += (
    [f"- {item}" for item in errors]
    if errors else ["- None"]
)

lines += ["", "## Editorial Review Warnings", ""]
lines += [f"- {item}" for item in warnings]

lines += [
    "",
    "## Numerical Evidence",
    "",
    f"- Reference LCOE: {lcoe:.6f} EUR/MWh",
    f"- LC004 break-even: {lc004:.6f} EUR/MWh",
    f"- Learned CAPEX reduction: {learning_reduction:.4f}%",
    f"- Eligible strategy cases: {eligible}/{len(feasibility)}",
    f"- Citation IDs used in manuscript: {len(citations)}",
    "",
    "This audit checks a bounded set of conditions, "
    "not publication suitability.",
]

output = PAPER / "stage72_manuscript_audit.md"
output.write_text("\n".join(lines) + "\n", encoding="utf-8")

print("STAGE 7.2.8 — MANUSCRIPT AUDIT")
print("Status:", status)
print("Passed:", len(passed))
print("Failed:", len(errors))
print("Review warnings:", len(warnings))
print("Citation IDs used:", len(citations))
print("Report:", output)

for item in errors:
    print("FAIL:", item)

for item in warnings:
    print("REVIEW:", item)

raise SystemExit(1 if errors else 0)
