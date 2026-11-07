"""Correct the skipped research number without overwriting edited documents."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD = "28_economic_assumptions_and_price_basis.md"
NEW = "27_economic_assumptions_and_price_basis.md"


def migrate_research_numbering(root=ROOT):
    root = Path(root)
    old, new = root / "research" / OLD, root / "research" / NEW
    if old.exists() and new.exists() and old.read_bytes() != new.read_bytes():
        raise ValueError("Both assumption documents exist with different contents. "
                         "Reconcile them manually; neither was changed.")
    if not old.exists() and not new.exists():
        return "not_present"
    action = "already_correct"
    if old.exists():
        if new.exists():
            old.unlink()  # Only remove a proven byte-identical duplicate.
        else:
            old.rename(new)
        action = "renamed"
    paths = [root / "README.md"] + sorted((root / "research").glob("*.md"))
    for path in paths:
        if path.is_file():
            content = path.read_text(encoding="utf-8")
            updated = content.replace(OLD, NEW)
            if updated != content:
                path.write_text(updated, encoding="utf-8")
    return action


if __name__ == "__main__":
    print("Research numbering: " + migrate_research_numbering())
