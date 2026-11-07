"""Read-only check for changes since the latest complete Stage 3–4 rebuild."""

import sys
from stage34_provenance import freshness_issues


def main():
    issues = freshness_issues()
    if issues:
        print("Stage 3–4 freshness: STALE_OR_UNVERIFIED")
        for issue in issues:
            print("- " + issue)
        print("Run python src/run_stage34.py after reviewing the changes.")
        return 1
    print("Stage 3–4 freshness: CURRENT")
    print("Tracked inputs, scripts, outputs, and dependency versions match the rebuild.")
    print("This is not factual verification or publication approval.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
