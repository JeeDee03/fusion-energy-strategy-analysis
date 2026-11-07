"""Declared Stage 1–2 boundaries; read-only freshness screening."""
from pathlib import Path
from importlib import metadata
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = ('pandas', 'numpy', 'matplotlib', 'tabulate')
SUMMARY = 'reports/stage12_run_summary.json'
STEPS=[
 'check_dataset.py','audit_funding.py','benchmark_funding.py','validate_financial_data.py',
 'validate_milestones.py','validate_partnership_evidence.py',
 'funding_comparison.py','partnership_capabilities.py','research_summary.py',
 'electricity_market_analysis.py','integrate_stage12.py'
]
REQUIRED=[
 'companies.csv','sources.csv','funding_rounds.csv','funding_snapshots.csv','funding_normalized.csv',
 'strategic_partnerships.csv','milestones.csv','claims.csv','claim_sources.csv',
 'partnership_evidence.csv','partnership_capability_tags.csv','partnership_claims.csv','partnership_claim_sources.csv'
]
GENERATED=[
 'reports/funding_comparison_usd.png','reports/partnership_capabilities.png',
 'reports/electricity_price_distribution_2024.png','reports/electricity_monthly_2024.png',
 'reports/electricity_price_duration_2024.png','reports/funding_event_timeline.png','reports/partnership_evidence_map.png',
 'research/02_market_data_summary.md','research/11_stage12_synthesis.md',
 'data/electricity_prices_de_lu_2024.csv','data/electricity_monthly_2024.csv','data/electricity_summary_2024.json',
 'data/partnership_capability_matrix.csv','data/all_claims.csv','data/all_claim_sources.csv'
]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def input_paths(root=ROOT):
    root = Path(root)
    raw = root / 'data/raw/smard_2024'
    manifest = json.loads((raw / 'manifest.json').read_text())
    paths = { 'data/'+n for n in REQUIRED }
    paths |= {str(p.relative_to(root)) for p in (root / 'src').glob('*.py')}
    paths |= {'requirements.txt', 'data/raw/smard_2024/manifest.json'}
    for item in manifest['files']:
        path = (raw / item['file']).resolve()
        if not path.is_relative_to(raw.resolve()) or not path.is_file():
            raise ValueError('Missing/outside SMARD file: '+item['file'])
        if digest(path) != item['sha256']:
            raise ValueError('Raw SMARD snapshot hash mismatch: '+item['file'])
        paths.add(str(path.relative_to(root.resolve())))
    return sorted(paths)


def freshness_issues(root=ROOT):
    root = Path(root)
    try:
        r = json.loads((root / SUMMARY).read_text())
        if r.get('schema_version') != 1 or r.get('status') != 'passed' or r.get('evidence_issues') != []:
            return ['Stage 1–2: no complete evidence-issue-free schema-1 success record; rebuild required.']
        steps = r.get('steps', [])
        if [s['script'] for s in steps] != STEPS or any(s.get('exit_code') != 0 for s in steps):
            return ['Stage 1–2: incomplete/failed step coverage.']
        issues = []
        for group, names in [('input_hashes',input_paths(root)), ('output_hashes',GENERATED)]:
            saved = r.get(group,{})
            if set(saved) != set(names): issues.append('Stage 1–2: declared '+group+' file set changed.')
            for name in names:
                p = root / name
                if not p.is_file() or saved.get(name) != digest(p):
                    issues.append('Stage 1–2: missing/changed '+name)
        if r.get('python') != sys.version or r.get('packages') != {n: metadata.version(n) for n in PACKAGES}:
            issues.append('Stage 1–2: Python/dependency versions changed.')
        return issues
    except (OSError, ValueError, KeyError, TypeError, AttributeError, metadata.PackageNotFoundError) as exc:
        return ['Stage 1–2: cannot verify record: '+str(exc)]
