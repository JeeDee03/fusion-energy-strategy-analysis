"""Both rebuild records must match current files; no implicit regeneration."""
import sys
from stage12_provenance import freshness_issues as stage12_issues
from stage34_provenance import ROOT, freshness_issues as stage34_issues


def freshness_issues(root=ROOT):
    return stage12_issues(root) + stage34_issues(root)


def main():
    issues = freshness_issues()
    print('Stage 1–4 freshness: '+('STALE_OR_UNVERIFIED' if issues else 'CURRENT_WITH_RESEARCH_LIMITATIONS'))
    for issue in issues: print('REVIEW: '+issue)
    print('Execution/data consistency only; human review and economic calibration remain required.')
    return int(bool(issues))


if __name__ == '__main__':
    sys.exit(main())
