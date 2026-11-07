"""Offline Stage 1–2 rebuild. Stops on execution failure; tracks open evidence separately."""
from pathlib import Path
from datetime import datetime, timezone
from importlib import metadata
import subprocess, sys, os, json, hashlib, csv, math, platform, traceback
ROOT=Path(__file__).resolve().parent.parent
REPORTS=ROOT/'reports'
REPORTS.mkdir(exist_ok=True)
SUMMARY=REPORTS/'stage12_run_summary.json'
LOG=REPORTS/'stage12_run.log'
from stage12_provenance import STEPS, REQUIRED, GENERATED, input_paths

def read(name):
 with (ROOT/'data'/name).open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def mapping(rows,key):
 result={r[key]:r for r in rows}
 if len(result)!=len(rows):raise ValueError('Duplicate '+key)
 return result
state={'schema_version':1,'started_at_utc':datetime.now(timezone.utc).isoformat(),'status':'running','python':sys.version,'platform':platform.platform(),'packages':{},'steps':[],'evidence_issues':[],'input_hashes':{},'output_hashes':{}}
def save():
 if state['status'] != 'running':state['finished_at_utc']=datetime.now(timezone.utc).isoformat()
 SUMMARY.write_text(json.dumps(state,indent=2),encoding='utf-8')

def main():
 save()
 if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE') not in (None,'','0'):
  raise RuntimeError('Disable Python optimization (-O / PYTHONOPTIMIZE): existing validators use assert checks.')
 missing=[str(ROOT/'data'/n) for n in REQUIRED if not (ROOT/'data'/n).is_file()]
 missing += [str(ROOT/'src'/s) for s in STEPS if not (ROOT/'src'/s).is_file()]
 raw=ROOT/'data/raw/smard_2024';manifest_path=raw/'manifest.json'
 if not manifest_path.is_file():missing.append(str(manifest_path))
 if missing:raise FileNotFoundError('Required files missing:\n'+'\n'.join(missing))
 for package in ['pandas','numpy','matplotlib','tabulate']:
  try:state['packages'][package]=metadata.version(package)
  except metadata.PackageNotFoundError:raise RuntimeError(f'Missing dependency: {package}. Install the project requirements in the active environment.')
 originals=[ROOT/name for name in input_paths(ROOT)]
 manifest=json.loads(manifest_path.read_text())
 for item in manifest['files']:
  path=raw/item['file']
  if not path.is_file():raise FileNotFoundError(str(path))
  if digest(path)!=item['sha256']:raise ValueError('Raw SMARD snapshot hash mismatch: '+item['file'])
 # Prevent a stale processed FX table from silently rebuilding a misleading funding chart.
 rounds=mapping(read('funding_rounds.csv'),'funding_id')
 normalized=mapping(read('funding_normalized.csv'),'funding_id')
 if set(rounds)!=set(normalized):raise ValueError('Normalized funding IDs differ from original events. Review FX normalization before rebuilding.')
 for key,r in rounds.items():
  n=normalized[key]
  for field in ['company_id','announcement_date','currency','funding_type','source_id']:
   if r[field]!=n[field]:raise ValueError(f'Stale normalized funding: {key}, {field}')
  amount=float(r['amount_original'])
  if not math.isclose(amount,float(n['amount_original']),rel_tol=1e-12):raise ValueError('Stale original amount: '+key)
  if r['currency']=='USD':expected=amount
  elif r['currency']=='EUR':
   rate=float(n['eur_usd_rate'])
   if not math.isfinite(rate) or rate<=0:raise ValueError('Invalid FX rate: '+key)
   from datetime import date
   age=(date.fromisoformat(r['announcement_date'])-date.fromisoformat(n['fx_date'])).days
   if not 0<=age<=7:raise ValueError('FX date outside preceding 7 days: '+key)
   expected=amount*rate
  else:raise ValueError('Unsupported funding currency: '+r['currency'])
  if not math.isclose(expected,float(n['amount_usd']),rel_tol=1e-10,abs_tol=.01):raise ValueError('Incorrect converted amount: '+key)
 # Hash inputs before executing any regeneration step.
 state['input_hashes']={str(p.relative_to(ROOT)):digest(p) for p in originals}
 state['fx_provenance_limit']='Existing normalized FX values checked for internal consistency; source-rate download and archived ECB input provenance are not certified by this runner.'
 environment=os.environ.copy();environment['MPLBACKEND']='Agg'
 with LOG.open('w',encoding='utf-8') as log:
  log.write('Stage 1–2 offline rebuild\nPython: '+sys.executable+'\n')
  for script in STEPS:
   print('Running '+script,flush=True)
   item={'script':script,'started_at_utc':datetime.now(timezone.utc).isoformat()};state['steps'].append(item)
   log.write('\n### '+script+'\n');log.flush()
   proc=subprocess.run([sys.executable,str(ROOT/'src'/script)],cwd=ROOT,env=environment,stdout=log,stderr=subprocess.STDOUT)
   item.update(exit_code=proc.returncode,finished_at_utc=datetime.now(timezone.utc).isoformat())
   if proc.returncode:raise RuntimeError(f'{script} failed with exit code {proc.returncode}. See reports/stage12_run.log.')
 missing_outputs=[p for p in GENERATED if not (ROOT/p).is_file()]
 if missing_outputs:raise FileNotFoundError('Expected outputs absent: '+', '.join(missing_outputs))
 # A successful rebuild must not alter its source datasets or scripts.
 changed=[name for name,h in state['input_hashes'].items() if digest(ROOT/name)!=h]
 if changed:raise RuntimeError('Source inputs changed during rebuild: '+', '.join(changed))
 state['output_hashes']={p:digest(ROOT/p) for p in GENERATED}
 alias={'company_source_checked':'original_source_checked'}
 cs=read('claims.csv')
 for s in read('funding_snapshots.csv'):
  found=[c for c in cs if c['entity_id']==s['snapshot_id']]
  if len(found)!=1:state['evidence_issues'].append(s['snapshot_id']+': expected exactly one financing claim')
  elif alias.get(found[0]['verification_status'],found[0]['verification_status'])!=alias.get(s['verification_status'],s['verification_status']):
   state['evidence_issues'].append(s['snapshot_id']+': snapshot/claim review status differs')
 pending=[r['claim_id'] for r in read('all_claims.csv') if r['verification_status'] in ['pending_review','disputed_unresolved']]
 if pending:state['evidence_issues'].append('Pending/disputed claims: '+', '.join(pending))
 state['status']='passed_with_evidence_issues' if state['evidence_issues'] else 'passed'
 save()
 print('Rebuild finished: '+state['status'])
 print('Evidence issues: '+str(len(state['evidence_issues'])))
 print('Log: reports/stage12_run.log')
 print('Environment, hashes and results: reports/stage12_run_summary.json')
 if state['evidence_issues']:
  for issue in state['evidence_issues']:print('REVIEW: '+issue)
 print('This is an execution/data-consistency result, not independent factual or publication approval.')

if __name__=='__main__':
 try:main()
 except Exception as exc:
  state['status']='failed';state['error']=str(exc);save()
  print('FAILED: '+str(exc),file=sys.stderr)
  print('Details: reports/stage12_run_summary.json; step output, if available: reports/stage12_run.log',file=sys.stderr)
  sys.exit(1)
