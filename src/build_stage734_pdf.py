from pathlib import Path
import csv
import hashlib
import json
import os
import re
import subprocess
from datetime import date

ROOT = Path(__file__).resolve().parent.parent
PAPER = ROOT / "paper"
BUILD = PAPER / "build"
BUILD.mkdir(parents=True, exist_ok=True)

MANUSCRIPT = PAPER / "manuscript.md"
SOURCE = BUILD / "publication_source.md"
OUTPUT = BUILD / "stellarator_fusion_publication.pdf"
MANIFEST = BUILD / "publication_build_manifest.json"

TARGETS = ("BPF03", "EC001", "EC003")

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(command):
    return subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )

def source_records():
    records = {}
    for filename in (
        "data/sources.csv",
        "data/competitive_sources.csv",
    ):
        with (ROOT / filename).open(
            encoding="utf-8-sig", newline=""
        ) as file:
            for row in csv.DictReader(file):
                sid = (row.get("source_id") or "").strip()
                if sid in TARGETS:
                    if sid in records:
                        raise ValueError(f"Duplicate source ID: {sid}")
                    records[sid] = row

    missing = set(TARGETS) - records.keys()
    if missing:
        raise ValueError(f"Missing sources: {sorted(missing)}")
    return records

for i in range(1, 5):
    matches = list(
        (PAPER / "figures").glob(f"figure0{i}_*.png")
    )
    if len(matches) != 1:
        raise ValueError(
            f"Figure {i}: expected one image, found {len(matches)}"
        )

original = MANUSCRIPT.read_text(encoding="utf-8")
heading = re.match(
    r"\A# The Economics of Commercial Stellarator Fusion\s*\n",
    original,
)
if not heading:
    raise ValueError("Unexpected manuscript title")

body = original[heading.end():].lstrip("\n")

subtitle = (
    "An Integrated Techno-Economic, Uncertainty, "
    "and Commercialization Strategy Analysis"
)

# Remove subtitle already present in manuscript to avoid duplication.
body = re.sub(
    r"\A\*An Integrated Techno-Economic, Uncertainty, "
    r"and Commercialization Strategy Analysis\*\s*\n",
    "",
    body,
    count=1,
).lstrip("\n")

records = source_records()

bibliography = [
    "\n### Selected References Cited in the Manuscript\n",
]

for sid in TARGETS:
    row = records[sid]
    title = (row.get("source_title") or "").strip()
    publisher = (row.get("publisher") or "").strip()
    published = (row.get("publication_date") or "").strip()
    url = (row.get("url") or "").strip()

    if not all((title, publisher, url)):
        raise ValueError(f"Incomplete reference: {sid}")

    year = published[:4] if published else "n.d."

    verified_references = {
        "BPF03": (
            "Lion, J., Anglès, J.-C., Bonauer, L., et al. "
            "(2025). Stellaris: A high-field quasi-isodynamic "
            "stellarator for a prototypical fusion power plant. "
            "*Fusion Engineering and Design*, 214, 114868."
        ),
        "EC001": (
            "Araiinejad, L. S., & Shirvan, K. (2025). "
            "Techno-economic analysis of deuterium-tritium "
            "magnetic confinement fusion power plants. "
            "*Applied Energy*, 401, 126567."
        ),
    }

    if sid in verified_references:
        entry = verified_references[sid]
    else:
        entry = f"{publisher} ({year}). *{title}*."

    bibliography.append(
        f"- **[{sid}]** {entry} <{url}>\n"
    )

bibliography.extend([
    "\nFull source inventories and unresolved bibliographic "
    "reviews are maintained in `paper/references.md` and "
    "`paper/stage733_source_review_queue.csv`.\n",
    "\nBibliographic details in this publication build are "
    "transcribed from the project source registries. "
    "This does not constitute independent verification "
    "of every source field or underlying research claim.\n",
])

author = os.getenv("RESEARCH_AUTHOR", "").strip()
author_line = (
    author if author else "Independent research project"
)

cover = f"""# The Economics of Commercial Stellarator Fusion

**{subtitle}**

{author_line}

*Independent Exploratory Research Manuscript*

November 2026

**Scientific status:** Computationally audited exploratory
research. External empirical and bibliographic verification
remain incomplete. This document is not an investment
recommendation or a certified commercial reactor assessment.

```{{=typst}}
#pagebreak()
```

"""

SOURCE.write_text(
    cover + body.rstrip() + "\n\n"
    + "\n".join(bibliography),
    encoding="utf-8",
)

command = [
    "pandoc",
    str(SOURCE),
    "--from=markdown+tex_math_single_backslash",
    "--to=pdf",
    "--pdf-engine=typst",
    "--resource-path=.:paper:paper/figures",
    "--metadata=papersize:a4",
    "--standalone",
    "-o",
    str(OUTPUT),
]

result = run(command)
if result.stderr:
    print(result.stderr)

manifest = {
    "build_date": date.today().isoformat(),
    "manuscript_sha256": sha256(MANUSCRIPT),
    "publication_source_sha256": sha256(SOURCE),
    "pdf_sha256": sha256(OUTPUT),
    "reference_ids": list(TARGETS),
    "pandoc_version": run(
        ["pandoc", "--version"]
    ).stdout.splitlines()[0],
    "typst_version": run(
        ["typst", "--version"]
    ).stdout.strip(),
    "status": "PDF_BUILT_EDITORIAL_REVIEW_PENDING",
}

MANIFEST.write_text(
    json.dumps(manifest, indent=2) + "\n",
    encoding="utf-8",
)

print("STAGE 7.3.4 — PUBLICATION BUILD")
print("PDF:", OUTPUT)
print("Manifest:", MANIFEST)
print("Status:", manifest["status"])
