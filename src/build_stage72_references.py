"""Build traceable draft references from retained research data.

Does not verify external URLs, DOIs, publication metadata,
or scientific claims. Does not modify manuscript.md.
"""

from pathlib import Path
from collections import defaultdict
import csv
import hashlib
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
PAPER = ROOT / "paper"
PAPER.mkdir(exist_ok=True)

def rows(name):
    path = DATA / name
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def clean(value):
    return " ".join(str(value or "").split())

def link(value):
    return clean(value).replace(")", "%29")

# 1. Read all available bibliography records.
records = {}
conflicts = []

for name in ("sources.csv", "competitive_sources.csv"):
    for item in rows(name):
        sid = clean(item.get("source_id"))
        if not sid:
            continue

        candidate = {
            "id": sid,
            "title": clean(item.get("source_title")),
            "publisher": clean(item.get("publisher")),
            "date": clean(item.get("publication_date")),
            "url": clean(item.get("url")),
            "type": clean(
                item.get("source_type") or item.get("source_kind")
            ),
            "locator": clean(item.get("locator")),
            "limitations": clean(item.get("limitations")),
        }

        if sid in records and records[sid] != candidate:
            conflicts.append(f"Conflicting source ID: {sid}")
        else:
            records[sid] = candidate

# 2. Add referenced economic sources not otherwise registered.
economic_notes = rows("economic_reference_notes.csv")

for item in economic_notes:
    sid = clean(item.get("source_id"))
    if not sid:
        continue

    if sid not in records:
        records[sid] = {
            "id": sid,
            "title": "",
            "publisher": "",
            "date": "",
            "url": clean(item.get("url")),
            "type": clean(item.get("source_role")),
            "locator": clean(item.get("locator")),
            "limitations": clean(item.get("transfer_limit")),
        }

# 3. Identify repeated URLs without merging source IDs.
by_url = defaultdict(list)

for sid, record in records.items():
    url = record["url"].rstrip("/").lower()
    if url:
        by_url[url].append(sid)

duplicates = {
    url: ids for url, ids in by_url.items()
    if len(ids) > 1
}

# 4. Produce a draft bibliography.
out = [
    "# Academic References — Draft",
    "",
    "Generated from the project's source registers.",
    "",
    "**Status:** Bibliographic inventory only. External "
    "links, DOI metadata, publication authorship and "
    "source claims still require independent review.",
    "",
]

incomplete = []

for sid in sorted(records):
    r = records[sid]
    missing = [
        key for key in ("title", "publisher", "date", "url")
        if not r[key]
    ]

    out.append(f"## {sid}")
    out.append(
        f"**{r['title'] or '[Title not recorded]'}**"
    )
    out.append(
        f"- Publisher: {r['publisher'] or '[Not recorded]'}"
    )
    out.append(
        f"- Publication date: {r['date'] or '[Not recorded]'}"
    )
    out.append(
        f"- Type: {r['type'] or '[Not recorded]'}"
    )
    out.append(
        f"- URL: {r['url'] or '[Not recorded]'}"
    )

    if r["locator"]:
        out.append(f"- Locator: {r['locator']}")
    if r["limitations"]:
        out.append(f"- Limitations: {r['limitations']}")

    if missing:
        incomplete.append((sid, missing))
        out.append(
            "- Bibliographic fields to review: "
            + ", ".join(missing)
        )

    out.append("")

out.extend([
    "## Bibliographic Quality Checks",
    "",
    f"- Source identifiers: {len(records)}",
    f"- Records with missing key fields: {len(incomplete)}",
    f"- Repeated URL groups: {len(duplicates)}",
    f"- Conflicting source identifiers: {len(conflicts)}",
    "",
])

for url, ids in sorted(duplicates.items()):
    out.append(
        f"- Repeated URL: {', '.join(ids)} — {url}"
    )

for error in conflicts:
    out.append(f"- CONFLICT: {error}")

(PAPER / "references.md").write_text(
    "\n".join(out) + "\n", encoding="utf-8"
)

# 5. Build claim-to-source mapping.
claims = defaultdict(list)

for item in rows("all_claim_sources.csv"):
    cid = clean(item.get("claim_id"))
    sid = clean(item.get("source_id"))
    if cid and sid:
        claims[cid].append(item)

mapping = [
    "# Stage 7.2 — Citation and Evidence Map",
    "",
    "Source relationships follow the retained project data.",
    "A source association is not independent verification.",
    "",
    "## Claim-to-Source Register",
    "",
]

unknown = set()

for cid, items in sorted(claims.items()):
    mapping.append(f"### {cid}")

    for item in items:
        sid = clean(item.get("source_id"))
        role = clean(item.get("evidence_role"))
        locator = clean(item.get("page_or_section"))
        note = clean(item.get("verification_note"))

        if sid not in records:
            unknown.add(sid)

        mapping.extend([
            f"- Source: `{sid}`",
            f"- Evidence role: {role or '[Not recorded]'}",
            f"- Locator: {locator or '[Not recorded]'}",
            f"- Review note: {note or '[Not recorded]'}",
            "",
        ])

mapping.extend([
    "## Model-Output Traceability",
    "",
    "| Result | Primary project output |",
    "|---|---|",
    "| Reference LCOE | `reports/stage4_integrated_summary.csv` |",
    "| LC004 break-even price | `reports/lifecycle_summary.csv` |",
    "| Component learning | `reports/stage44_learning_results.csv` |",
    "| Engineering capacity factors | `reports/engineering_generation_scenarios.csv` |",
    "| Monte Carlo refinement | `reports/stage52_summary_seed*_n*.csv` |",
    "| Convergence assessment | `reports/stage53_audit.json`, `reports/stage53_extension_audit.json` |",
    "| Strategy feasibility | `reports/stage65_feasibility_screen.csv` |",
    "| Strategic synthesis | `reports/stage66_context_synthesis.csv` |",
    "",
    "## Outstanding Source-ID Resolution",
    "",
])

if unknown:
    mapping.extend(
        f"- Unresolved source ID: `{sid}`"
        for sid in sorted(unknown)
    )
else:
    mapping.append(
        "- All claim source IDs resolve within the combined registers."
    )

mapping.extend([
    "",
    "## Suggested Manuscript Source Groups",
    "",
    "- Introduction: technical design literature and "
    "institutional fusion sources; review exact claims.",
    "- Industry context: company disclosures from the "
    "competitive and general registers.",
    "- Economic methodology: NREL methodology reference; "
    "not evidence supporting chosen numerical inputs.",
    "- Cost literature: ARAI study as external tokamak "
    "context, not Stellaris calibration.",
    "- Results: cite retained model-output files and "
    "scenario assumptions rather than externalizing "
    "the author's own calculations.",
    "",
])

(PAPER / "citation_map.md").write_text(
    "\n".join(mapping) + "\n", encoding="utf-8"
)

print("STAGE 7.2.7 — REFERENCE INVENTORY")
print(f"Source IDs: {len(records)}")
print(f"Incomplete records: {len(incomplete)}")
print(f"Repeated URL groups: {len(duplicates)}")
print(f"ID conflicts: {len(conflicts)}")
print(f"Unresolved claim source IDs: {len(unknown)}")
print("Created: paper/references.md")
print("Created: paper/citation_map.md")
print("External verification: NOT PERFORMED")
