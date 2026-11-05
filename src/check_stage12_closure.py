"""Read-only project audit; writes only a closure review report and JSON findings.
A passing automated audit is not editorial or scientific sign-off.
"""
from pathlib import Path
from datetime import datetime,timezone
import csv,json,hashlib,re,sys
ROOT=Path(__file__).resolve().parent.parent
REPORTS=ROOT/'reports';REPORTS.mkdir(exist_ok=True)
findings=[]
def add(level,area,message):findings.append({'level':level,'area':area,'message':message})
def text(rel):
 p=ROOT/rel
 if not p.is_file():add('BLOCKER','required_file','Missing '+rel);return ''
 return p.read_text(encoding='utf-8')
def rows(rel):
 s=text(rel)
 return list(csv.DictReader(s.splitlines())) if s else []
summary_raw=text('reports/stage12_run_summary.json')
if summary_raw:
 try:
  summary=json.loads(summary_raw)
  if summary.get('status')!='passed':add('BLOCKER','rebuild','Last rebuild status: '+str(summary.get('status')))
  for group in ['input_hashes','output_hashes']:
   if not summary.get(group):add('BLOCKER','rebuild','No '+group+' recorded')
   for name,expected in summary.get(group,{}).items():
    p=ROOT/name
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:
     add('BLOCKER','rebuild','File differs from last successful rebuild or is missing: '+name)
  for issue in summary.get('evidence_issues',[]):add('BLOCKER','evidence',issue)
 except (ValueError,TypeError) as exc:add('BLOCKER','rebuild','Invalid run summary: '+str(exc))

docs={}
for name in ['README.md','research/01_research_proposal.md','research/03_market_financing_analysis.md','research/04_source_verification.md','research/05_analysis_protocol.md','research/06_data_dictionary.md','research/07_funding_audit.md','research/08_milestone_methodology.md','research/09_partnership_evidence_analysis.md','research/10_electricity_market_baseline.md','research/11_stage12_synthesis.md','research/12_reproducibility_guide.md']:
 docs[name]=text(name)
 # Check ordinary relative Markdown targets, including images; not remote availability.
 for dest in re.findall(r'\]\(([^\s)]+)\)',docs[name]):
  if dest.startswith(('http:','https:','mailto:','#')):continue
  dest=dest.split('#')[0]
  if dest and not ((ROOT/name).parent/dest).exists():add('REVIEW','document_links',name+' -> '+dest+' does not resolve')
readme=docs.get('README.md','')
for token in ['run_stage12.py','11_stage12_synthesis.md']:
 if token not in readme:add('REVIEW','README','Add the current reproduction/report reference: '+token)
proposal=docs.get('research/01_research_proposal.md','')
if 'Research design in progress' in proposal or 'no original quantitative results' in proposal.lower():
 add('REVIEW','stale_progress','Proposal still describes the initial pre-analysis state. Replace with a dated progress note; do not claim hypotheses validated.')
audit=docs.get('research/07_funding_audit.md','')
current_update = audit.partition('## Current review update — 28 October 2026')[2].partition('## Initial audit record')[0]
update_complete = all(token in current_update for token in ['FS003', 'FS004', 'external_report_checked', 'S010', 'S011'])
if any(p in audit for p in ['could not be retrieved','two cumulative claims remain pending','has not been fully reverified here']) and not update_complete:
 add('REVIEW','historical_audit','Chapter 07 contains initial review outcomes superseded by later checks. Preserve as dated history and append an explicit update linking the current evidence; do not erase the original review record.')
finance=docs.get('research/03_market_financing_analysis.md','')
if 'not necessarily the publication date' in finance:
 add('REVIEW','Proxima_source','Chapter 03 still has the old undated-Proxima footnote; check against dated S001 evidence.')

# Central dictionary must describe the new tables; domain notes alone are not the central index.
dictionary=docs.get('research/06_data_dictionary.md','')
for token in ['milestones.csv','partnership_evidence.csv','partnership_capability_tags.csv','electricity_prices_de_lu_2024.csv','electricity_monthly_2024.csv','all_claims.csv','all_claim_sources.csv','external_report_checked']:
 if token not in dictionary:add('REVIEW','data_dictionary','Central dictionary lacks a table/status reference: '+token)
# Current audit status and source locators must agree with implemented evidence.
claim_rows=rows('data/claims.csv')
claim_map={c['claim_id']: c for c in claim_rows}
for item in rows('data/funding_audit.csv'):
 c=claim_map.get(item['claim_id'])
 if c is None or item['review_status'] != c['verification_status']:
  add('REVIEW','audit_status','Funding audit disagrees with current claim: '+item['record_id'])
for link in rows('data/claim_sources.csv'):
 if 'not verified' in link['page_or_section'].lower():
  add('REVIEW','source_locator','Placeholder locator remains: '+link['claim_id'])
sources=rows('data/sources.csv')
ids=[r['source_id'] for r in sources]
if len(ids)!=len(set(ids)):add('BLOCKER','sources','Duplicate source IDs')
for rel in ['data/claims.csv','data/partnership_claims.csv']:
 for r in rows(rel):
  if r.get('verification_status') in ['pending_review','disputed_unresolved']:
   add('REVIEW','evidence',rel+': '+r['claim_id']+' remains '+r['verification_status'])
# These are mandatory human review items, not claims that an error exists.
manual=[
 'Read the consolidated chapter against current CSVs and supporting audit notes; confirm amounts, qualifiers, dates and source locators.',
 'Check that external_report_checked means the cited report was read, not independently audited financial accuracy. Harmonize terminology in chapter 04 and the dictionary.',
 'Keep the selected/incomplete funding-history scope explicit. Do not claim all historical rounds or undisclosed extensions have been captured.',
 'Verify that year-only targets and company-reported completions are not presented as exact dates or independent technical demonstrations.',
 'Retain the single-year, DE/LU scope and October 2026 retrieval vintage of the 2024 electricity baseline; do not present historical means as future sale prices.',
 'Record that FX conversions were checked internally but the original ECB input snapshot/provenance has not yet been archived in this enhancement cycle.',
 'Confirm that H1-H3 remain research hypotheses, with technical benchmarking and economic testing assigned to later stages.',
 'Inspect rendered tables/figures and select one clear reading entry point in README; no chart should imply a financing-strength or partnership-quality ranking.'
]
block=sum(f['level']=='BLOCKER' for f in findings);review=sum(f['level']=='REVIEW' for f in findings)
status='blocked' if block else ('needs_review' if review else 'automated_checks_clear_human_review_required')
record={'created_at_utc':datetime.now(timezone.utc).isoformat(),'status':status,'blockers':block,'review_findings':review,'findings':findings,'mandatory_human_review':manual,'scope':'Automated structural/document-reference screening only; no completion certification.'}
(REPORTS/'stage12_closure_review.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
lines=['# Stage 1–2 Closure Review','',f'Status: {status}',f'Blockers: {block} | Review findings: {review}','','## Automated findings','']
lines += [f"- **{f['level']} / {f['area']}**: {f['message']}" for f in findings] or ['No automated findings. Human review remains required.']
lines += ['','## Mandatory human review','']+['- [ ] '+m for m in manual]
lines += ['','This audit does not modify original data, manuscripts or the previous rebuild log. A clean execution result is not scientific validation or publication approval.']
(REPORTS/'stage12_closure_review.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('Closure screening: '+status)
print(f'Blockers: {block} | Review findings: {review}')
print('Open reports/stage12_closure_review.md for exact items.')
print('Human editorial review still required; Stage 1–2 is not automatically declared complete.')
sys.exit(1 if block else 0)
