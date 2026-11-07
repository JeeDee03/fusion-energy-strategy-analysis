#!/usr/bin/env python3
"""Read-only repository and evidence inventory for Stage 7.1 (stdlib only).

Does not execute the science models or verify scientific truth. Runs from repo root.
"""
import argparse
import ast
import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

REQUIRED = {
    'Stage 1-4 foundation': ['requirements.txt', 'src/lifecycle_cash_flow.py', 'src/engineering_generation.py', 'src/run_stage14.py'],
    'Stage 5': ['data/stage5_uncertainty_spec.json', 'src/run_stage5_monte_carlo.py', 'src/validate_uncertainty_spec.py', 'src/analyze_stage53.py', 'src/run_stage54_triangular.py', 'src/run_stage54_dependencies.py', 'src/run_stage543_learning.py', 'src/integrate_stage55.py', 'reports/stage55_integration_audit.json', 'reports/stage55_cross_seed_summary.csv', 'reports/stage55_integration_summary.md'],
    'Stage 6': ['data/strategy_alternatives.csv', 'data/strategy_decision_criteria.csv', 'src/strategy_value_capture.py', 'src/strategy_risk_allocation.py', 'src/strategy_mcda.py', 'src/strategy_robustness.py', 'src/integrate_stage66.py', 'src/validate_stage66.py', 'reports/stage66_synthesis_audit.json', 'reports/stage66_synthesis_summary.md', 'research/46_stage6_integrated_strategic_synthesis.md']
}
IMPORTANT_AUDITS = ['reports/stage55_integration_audit.json', 'reports/stage62_value_capture_audit.json', 'reports/stage63_risk_allocation_audit.json', 'reports/stage64_partial_mcda_audit.json', 'reports/stage65_feasibility_audit.json', 'reports/stage66_synthesis_audit.json']


def git(root, *args):
    p = subprocess.run(['git', *args], cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()


def audit(root):
    code, top, err = git(root, 'rev-parse', '--show-toplevel')
    if code != 0 or Path(top).resolve() != root.resolve():
        raise SystemExit('ERROR — Run from the top level of the Git repository. '+err)
    _, commit, _ = git(root, 'rev-parse', 'HEAD')
    _, branch, _ = git(root, 'branch', '--show-current')
    _, status, _ = git(root, 'status', '--porcelain=v1', '--untracked-files=normal')
    _, tracked_output, _ = git(root, 'ls-files', '-z')
    tracked = set(tracked_output.split('\0')) - {''}
    file_rows = []
    for stage, paths in REQUIRED.items():
        for rel in paths:
            p = root / rel
            file_rows.append({'stage':stage, 'path':rel, 'exists':p.is_file(), 'tracked':rel in tracked, 'sha256':sha256(p) if p.is_file() else ''})

    # Identify local imports that do not resolve to an available repository module.
    local_sources = sorted((root/'src').glob('*.py')) if (root/'src').is_dir() else []
    imports = set()
    for p in local_sources:
        try:
            tree = ast.parse(p.read_text(encoding='utf-8'), filename=str(p))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.update(alias.name.split('.')[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imports.add(node.module.split('.')[0])
        except (UnicodeError, SyntaxError) as e:
            imports.add('PARSE_ERROR:'+p.name+':'+str(e))
    local_missing = sorted(x for x in imports if x.startswith('PARSE_ERROR:') or (x in {p.stem for p in local_sources} and not (root/'src'/f'{x}.py').is_file()))
    audit_rows=[]
    for rel in IMPORTANT_AUDITS:
        p=root/rel
        row={'path':rel, 'exists':p.is_file(), 'tracked':rel in tracked, 'status':'NOT_FOUND', 'parse_error':''}
        if p.is_file():
            try:
                content=json.loads(p.read_text(encoding='utf-8'))
                row['status']=str(content.get('status','NO_TOP_LEVEL_STATUS')) if isinstance(content,dict) else 'NOT_AN_OBJECT'
                row['sha256']=sha256(p)
            except (UnicodeError,json.JSONDecodeError) as e: row['parse_error']=str(e)
        audit_rows.append(row)
    warnings=[]
    for row in file_rows:
        if not row['exists']: warnings.append('MISSING '+row['path'])
        elif not row['tracked']: warnings.append('UNTRACKED_REQUIRED '+row['path'])
    for row in audit_rows:
        if not row['exists']: warnings.append('MISSING_AUDIT '+row['path'])
        elif not row['tracked']: warnings.append('UNTRACKED_AUDIT '+row['path'])
        if row['parse_error']: warnings.append('INVALID_JSON '+row['path'])
    if status: warnings.append('WORKTREE_NOT_CLEAN: examine git status; new Stage 7.1 files will appear untracked')
    if local_missing: warnings.append('SOURCE_PARSE_OR_LOCAL_IMPORT_ISSUES: '+', '.join(local_missing))
    # Audit status strings are disclosed as-is; absence of errors here is not model or evidence validation.
    return {'schema':'stage71_repository_inventory_v1', 'generated_utc':datetime.now(timezone.utc).isoformat(), 'git':{'head':commit,'branch':branch,'worktree_clean':not bool(status),'status_porcelain':status.splitlines()},'required_files':file_rows,'prior_audits':audit_rows,'source_py_count':len(local_sources),'warnings':warnings,'limitations':['Read-only inventory and tracked-file checks; not a clean-clone execution test','Does not verify factual correctness, model convergence or scientific claims','Does not compare exported source hashes to originals automatically','Source-level tests and end-to-end regeneration must be run separately','New Stage 7.1 generated files may make git status unclean']}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output-dir',default='reports',help='Destination under repository (default reports)')
    args=ap.parse_args()
    root=Path.cwd().resolve()
    result=audit(root)
    out=(root/args.output_dir).resolve()
    if root not in out.parents and out != root:
        raise SystemExit('ERROR — output must be inside repository')
    out.mkdir(parents=True,exist_ok=True)
    (out/'stage71_repository_audit.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    with (out/'stage71_file_inventory.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['stage','path','exists','tracked','sha256']);w.writeheader();w.writerows(result['required_files'])
    missing=sum(not x['exists'] for x in result['required_files'])
    untracked=sum(x['exists'] and not x['tracked'] for x in result['required_files'])
    print('STAGE 7.1 — REPOSITORY INVENTORY (not end-to-end reproducibility certification)')
    print('Git HEAD:',result['git']['head'][:12], '| branch:',result['git']['branch'])
    print('Required file inventory:',len(result['required_files']),'| missing:',missing,'| present but untracked:',untracked)
    print('Prior audit files:',sum(x['exists'] for x in result['prior_audits']),'/',len(result['prior_audits']))
    print('Source scripts inventoried:',result['source_py_count'])
    print('Warnings:',len(result['warnings']))
    for w in result['warnings'][:25]:print(' -',w)
    print('Saved:',out/'stage71_repository_audit.json',out/'stage71_file_inventory.csv')
    if missing or untracked or any(not x['exists'] or x['parse_error'] for x in result['prior_audits']):sys.exit(2)

if __name__=='__main__':main()
