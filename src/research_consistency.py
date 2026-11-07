"""Bounded editorial/number checks, not automated scientific fact checking."""
import csv
import json
import math
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = ('README.md', 'research/01_research_proposal.md',
             'research/05_analysis_protocol.md', 'research/25_stage4_techno_economic_synthesis.md')
START, END = '<!-- hypotheses:start -->', '<!-- hypotheses:end -->'


def hypothesis_block(register):
    return '\n\n'.join(f"**{h['id']} — {h['title']}:** {h['statement']} Status: **{h['status']}**."
                        for h in register['hypotheses'])


def audit(root=ROOT):
    root = Path(root)
    errors, values = [], []
    register = json.loads((root / 'data/research_status.json').read_text())
    hypotheses = register['hypotheses']
    if register.get('schema_version') != 1 or [h['id'] for h in hypotheses] != ['H1', 'H2', 'H3']:
        errors.append('Unsupported research status schema or hypothesis coverage.')
    for h in hypotheses:
        if h['status'] != 'open' or not all(h.get(k, '').strip() for k in ('title','statement','assessment','next_evidence')):
            errors.append(h['id'] + ': unsupported confirmation or missing evidence assessment. Reassess explicitly before advancing status.')
    stages = register['stages']
    expected = ['design_implemented','descriptive_baseline_with_limits','evidence_framework_with_gaps',
                'conditional_models_not_empirically_calibrated','planned','planned','planned']
    if [(s['stage'], s['status']) for s in stages] != list(enumerate(expected, 1)):
        errors.append('Stage status exceeds this implemented/evidence boundary or has incomplete coverage.')
    for name in DOCUMENTS:
        text = (root / name).read_text(encoding='utf-8')
        if text.count(START) != 1 or text.count(END) != 1 or text.index(START) > text.index(END):
            errors.append(name + ': hypothesis markers missing/ambiguous.')
        elif text.split(START)[1].split(END)[0].strip() != hypothesis_block(register):
            errors.append(name + ': hypothesis wording/status differs from register.')
    # Check all local editorial links. Remote source availability is outside scope.
    for path in [root / 'README.md', *sorted((root / 'research').glob('*.md'))]:
        for dest in re.findall(r'\]\(([^\s)]+)\)', path.read_text(encoding='utf-8')):
            if dest.startswith(('http:', 'https:', 'mailto:', '#')):
                continue
            target = (path.parent / dest.split('#')[0]).resolve()
            if not target.is_relative_to(root.resolve()) or not target.exists():
                errors.append(str(path.relative_to(root)) + ': unresolved/outside local target ' + dest)
    findings = json.loads((root / 'data/research_findings.json').read_text())
    ids = [f['id'] for f in findings]
    if not ids or len(ids) != len(set(ids)):
        errors.append('Empty/duplicate numerical finding identifiers.')
    for finding in findings:
        name = finding['artifact']
        path = (root / name).resolve()
        if not path.is_relative_to((root / 'reports').resolve()):
            raise ValueError('Findings may reference only project report CSVs.')
        with path.open(newline='', encoding='utf-8') as handle:
            rows = list(csv.DictReader(handle))
        selected = [r for r in rows if all(r.get(k) == str(v) for k,v in finding['where'].items())]
        if finding['classification'] != 'conditional_model_output' or not finding.get('boundary'):
            errors.append(finding['id'] + ': missing conditional classification/boundary.')
        if len(selected) != 1:
            errors.append(finding['id'] + ': finding selector is missing or nonunique.')
            continue
        value = float(selected[0][finding['field']])
        # Anchors are rounded to two decimals in the reviewed synthesis. Changes
        # require a deliberate narrative review, not silent re-pinning by a runner.
        if not math.isfinite(value) or abs(value - finding['value']) > finding['absolute_tolerance']:
            errors.append(finding['id'] + ': reviewed numerical anchor differs from generated table.')
        values.append({**finding, 'current_value': value})
    return {'status': 'FAIL' if errors else 'PASS_WITH_RESEARCH_LIMITATIONS',
            'errors': errors, 'hypotheses': hypotheses, 'stages': stages, 'findings': values,
            'scope': 'Canonical blocks, selected numerical anchors and local links only; arbitrary prose, source truth, calibration and publication suitability require human review.'}


def main():
    try:
        result = audit()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        result = {'status':'FAIL', 'errors':[str(exc)], 'findings':[], 'hypotheses':[]}
    reports = ROOT / 'reports'
    reports.mkdir(exist_ok=True)
    (reports / 'research_consistency_audit.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    lines = ['# Current Research Claims and Status', '', 'Status: '+result['status'], '',
             'Bounded consistency checks; no factual or publication approval.', '', '## Hypotheses', '']
    for h in result['hypotheses']:
        lines += [f"### {h['id']} — {h['title']} ({h['status']})", '', h['assessment'], '', 'Next evidence: '+h['next_evidence'], '']
    lines += ['## Conditional numerical anchors', '', '| Finding | Current value | Unit | Boundary |', '|---|---:|---|---|']
    for f in result['findings']:
        lines.append(f"| {f['id']} | {f['current_value']:.2f} | {f['unit']} | {f['boundary']} |")
    lines += ['', 'Selectors and source artifacts: `data/research_findings.json`.', '', '## Findings requiring correction', '']
    lines += ['- '+e for e in result['errors']] or ['None detected within the declared scope.']
    lines += ['', 'Main Stage 5 simulations, Stage 6 strategy comparison and Stage 7 final deliverables remain planned. Empirical calibration and human source/editorial review remain required.']
    (reports / 'research_consistency_summary.md').write_text('\n'.join(lines)+'\n')
    print('Research consistency: '+result['status'])
    for e in result['errors']: print('REVIEW: '+e)
    return int(bool(result['errors']))


if __name__ == '__main__':
    sys.exit(main())
