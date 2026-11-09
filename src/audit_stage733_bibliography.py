from pathlib import Path
from collections import defaultdict
from urllib.parse import urlsplit
import csv
import re

ROOT = Path(__file__).resolve().parent.parent
PAPER = ROOT / "paper"
records = []
issues = []
url_groups = defaultdict(set)

files = [
    ROOT / "data/sources.csv",
    ROOT / "data/competitive_sources.csv",
]

for path in files:
    if not path.exists():
        issues.append(f"Missing registry: {path.relative_to(ROOT)}")
        continue

    with path.open(encoding="utf-8-sig", newline="") as f:
        for line, row in enumerate(csv.DictReader(f), 2):
            sid = (row.get("source_id") or "").strip()
            title = (row.get("source_title") or "").strip()
            publisher = (row.get("publisher") or "").strip()
            date = (row.get("publication_date") or "").strip()
            url = (row.get("url") or "").strip()

            if not sid:
                issues.append(f"{path.name}:{line}: missing source_id")
                continue

            records.append((sid, title, publisher, date, url, path.name))

            for field, value in (
                ("source_title", title),
                ("publisher", publisher),
                ("publication_date", date),
                ("url", url),
            ):
                if not value:
                    issues.append(
                        f"{sid} ({path.name}:{line}): missing {field}"
                    )

            if url:
                parsed = urlsplit(url)
                if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                    issues.append(f"{sid}: malformed URL: {url}")
                url_groups[url.rstrip("/").lower()].add(sid)

manuscript = (PAPER / "manuscript.md").read_text(
    encoding="utf-8"
)
references = (PAPER / "references.md").read_text(
    encoding="utf-8"
)

citation_ids = set(re.findall(
    r"\[([A-Za-z][A-Za-z0-9_]*\d)\]",
    manuscript
))
reference_ids = set(re.findall(
    r"^##\s+([A-Za-z][A-Za-z0-9_]*\d)\b",
    references,
    flags=re.MULTILINE
))
registry_ids = {r[0] for r in records}

unresolved = sorted(citation_ids - reference_ids)
unregistered = sorted(citation_ids - registry_ids)
repeated_urls = {
    url: sorted(ids)
    for url, ids in url_groups.items()
    if len(ids) > 1
}

lines = [
    "# Stage 7.3.3 — Bibliographic Audit",
    "",
    "## Summary",
    "",
    f"- Registry rows: {len(records)}",
    f"- Unique registry IDs: {len(registry_ids)}",
    f"- Manuscript citation IDs: {len(citation_ids)}",
    f"- Bibliography heading IDs: {len(reference_ids)}",
    f"- Registry-field issues: {len(issues)}",
    f"- Repeated URL groups: {len(repeated_urls)}",
    f"- Manuscript citations absent from bibliography: {len(unresolved)}",
    f"- Manuscript citations absent from registries: {len(unregistered)}",
    "",
    "## Manuscript Citation Coverage",
    "",
]

for sid in sorted(citation_ids):
    lines.append(
        f"- {sid}: bibliography={'YES' if sid in reference_ids else 'NO'}, "
        f"registry={'YES' if sid in registry_ids else 'NO'}"
    )

lines.extend(["", "## Registry Field Issues", ""])
lines.extend(f"- {issue}" for issue in issues)
if not issues:
    lines.append("- None detected")

lines.extend(["", "## Repeated URL Groups", ""])
for url, ids in sorted(repeated_urls.items()):
    lines.append(f"- {', '.join(ids)}: {url}")
if not repeated_urls:
    lines.append("- None detected")

lines.extend([
    "",
    "## External Verification Status",
    "",
    "- BPF03: publication identity checked against DOI landing page.",
    "- EC001: publication identity checked against publisher record.",
    "- EC003: ATB 2025 methodology page identified.",
    "- Remaining entries: manual verification pending.",
    "",
    "This audit checks registry completeness and citation relationships.",
    "It does not verify the factual accuracy of all external records.",
])

output = PAPER / "stage733_bibliographic_audit.md"
output.write_text("\n".join(lines) + "\n", encoding="utf-8")

print("STAGE 7.3.3 — BIBLIOGRAPHIC AUDIT")
print("Registry rows:", len(records))
print("Unique IDs:", len(registry_ids))
print("Citation IDs:", len(citation_ids))
print("Field issues:", len(issues))
print("Repeated URL groups:", len(repeated_urls))
print("Unresolved manuscript citations:", len(unresolved))
print("Report:", output)
print("Status: MANUAL_BIBLIOGRAPHIC_REVIEW_REQUIRED")
