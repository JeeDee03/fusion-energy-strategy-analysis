"""Stage 6.6 synthesis: mechanically derive documented conclusions from Stage 5/6 reports.
No strategic rankings or empirical feasibility certification are created here.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
P = ('P120','P170','P200')
STRESS = ('RS00','RS01','RS02','RS03','RS04')
STRATEGIES = ('STR01','STR02','STR03','STR04')
FILES = {
    'stage62': 'reports/stage62_value_capture_results.csv',
    'stage63': 'reports/stage63_risk_allocation_results.csv',
    'stage64_scores': 'reports/stage64_partial_mcda_scores.csv',
    'stage64_weights': 'reports/stage64_weight_robustness.csv',
    'stage65_gates': 'reports/stage65_feasibility_screen.csv',
    'stage65_contexts': 'reports/stage65_context_gate_summary.csv',
    'stage65_thresholds': 'reports/stage65_price_thresholds.csv',
    'stage65_audit': 'reports/stage65_feasibility_audit.json',
    'stage55_summary': 'reports/stage55_integration_summary.md',
    'stage55_audit': 'reports/stage55_integration_audit.json',
}

def file_hash(p:Path)->str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def load(root=ROOT):
    root=Path(root)
    required = [k for k in FILES if not k.startswith('stage55')]
    for k in required:
        if not (root / FILES[k]).is_file():
            raise FileNotFoundError(f'Missing Stage 6 input: {FILES[k]}')
    frames={k:pd.read_csv(root / FILES[k]) for k in FILES if k not in ('stage65_audit','stage55_summary','stage55_audit') and (root / FILES[k]).exists()}
    audits={k:json.loads((root/FILES[k]).read_text()) for k in ('stage65_audit','stage55_audit') if (root/FILES[k]).exists()}
    return frames,audits

def analyze(root=ROOT):
    frames,audits=load(root)
    sc=frames['stage64_scores']; wt=frames['stage64_weights']; gate=frames['stage65_gates']; ctx=frames['stage65_contexts']; thr=frames['stage65_thresholds']
    for k,frame,cols,n in [
        ('stage62',frames['stage62'],['strategy_id','price_case'],12),
        ('stage63',frames['stage63'],['strategy_id','price_case','stress_id'],60),
        ('stage64_scores',sc,['strategy_id','price_case','stress_id','weight_set'],240),
        ('stage64_weights',wt,['price_case','stress_id'],15),
        ('stage65_gates',gate,['strategy_id','price_case','stress_id'],60),
        ('stage65_contexts',ctx,['price_case','stress_id'],15),
        ('stage65_thresholds',thr,['strategy_id','stress_id'],20),
    ]:
        if len(frame)!=n or frame.duplicated(cols).any(): raise ValueError(f'Unexpected {k} count/duplicate keys')
    for frame in (sc, gate, thr):
        if set(frame.strategy_id)!=set(STRATEGIES): raise ValueError('Strategy coverage mismatch')
    for frame in (sc,gate,ctx):
        if set(frame.price_case)!=set(P) or set(frame.stress_id)!=set(STRESS): raise ValueError('Context coverage mismatch')
    if set(sc.weight_set)!=set(['BALANCED','CAPITAL_FOCUS','RISK_FOCUS','VALUE_FOCUS']):raise ValueError('Weight policy coverage mismatch')
    if not set(['company_gate','external_gate','project_gate','all_economic_gates']).issubset(gate): raise ValueError('Missing gate status')
    if not np.array_equal(gate['all_economic_gates'].to_numpy(dtype=bool), (gate.company_gate & gate.external_gate & gate.project_gate).to_numpy(dtype=bool)):
        raise ValueError('Inconsistent economic gates')
    risk=frames['stage63']; key=['strategy_id','price_case','stress_id']
    x=gate.merge(risk[key+['company_stressed_npv_eur','external_stressed_npv_eur','stressed_project_npv_eur']],on=key,suffixes=('_gate','_risk'),validate='one_to_one')
    for n in ('company_stressed_npv_eur','external_stressed_npv_eur','stressed_project_npv_eur'):
        if not np.allclose(x[n+'_gate'],x[n+'_risk'],rtol=1e-10,atol=2.):raise ValueError(f'6.3/6.5 mismatch {n}')
    if int(ctx.feasible_strategy_count.sum())!=int(gate.all_economic_gates.sum()):raise ValueError('Context/strategy gates mismatch')
    if not np.array_equal(ctx.feasible_strategy_count.to_numpy(dtype=int),gate.groupby(['price_case','stress_id'],sort=True).all_economic_gates.sum().reindex(ctx.set_index(['price_case','stress_id']).index).to_numpy(dtype=int)):
        raise ValueError('Incorrect context counts')
    leaders=sc.loc[sc.rank_dense==1].groupby(['price_case','stress_id']).strategy_id.agg(lambda z:';'.join(sorted(set(z)))).reset_index(name='leaders')
    unique=leaders.leaders.unique().tolist()
    if 'STR03' not in unique:
        pass # Do not force STR03 to win; evidence may change in a new repository version.
    context=ctx.merge(leaders,on=['price_case','stress_id'],validate='one_to_one')
    evidence=[]
    for sid,g in gate.groupby('strategy_id',sort=True):
        evidence.append({'strategy_id':sid,'screened_cases':int(len(g)),'company_pass_count':int(g.company_gate.sum()),'external_pass_count':int(g.external_gate.sum()),'project_pass_count':int(g.project_gate.sum()),'joint_pass_count':int(g.all_economic_gates.sum()),'mcda_first_place_records':int(sc.loc[(sc.strategy_id==sid)&(sc.rank_dense==1),'weight_set'].count()),'assessment':'GATE_ELIGIBLE_ONLY_IF_ALL_PASS' if g.all_economic_gates.any() else 'NO_ECONOMICALLY_ELIGIBLE_CASE_IN_TESTED_SET'})
    ev=pd.DataFrame(evidence)
    baseline=thr[thr.stress_id=='RS00'].copy()
    if len(baseline)!=4: raise ValueError('Missing baseline thresholds')
    report={
        'status':'CONDITIONAL_STAGE6_STRATEGIC_SYNTHESIS_NO_EMPIRICAL_RECOMMENDATION',
        'scenarios_screened':int(len(gate)),
        'contexts_screened':int(len(ctx)),
        'eligible_scenarios':int(gate.all_economic_gates.sum()),
        'contexts_with_any_eligible':int((ctx.feasible_strategy_count>0).sum()),
        'all_contexts_same_mcda_leader':len(unique)==1,
        'provisional_leaders':unique,
        'baseline_joint_thresholds':{str(r.strategy_id):float(r.joint_economic_threshold_price_eur_mwh) for r in baseline.itertuples()},
        'all_baseline_thresholds_extrapolated_above_200':bool((baseline.threshold_location=='EXTRAPOLATED_ABOVE_200').all()),
        'stage55_status': audits.get('stage55_audit',{}).get('status','STAGE55_AUDIT_NOT_PROVIDED'),
        'limitations':[
            'Strategic options and fees remain hypothetical rather than disclosed contracts',
            'No direct lender terms, customer demand, default, warranties or full financing waterfalls',
            'MCDA is four-criterion partial screening; C05-C08 not fully evaluated',
            'No empirical probability of commercial success or structural scenario weights',
            'Stage 5.3 strict convergence criterion remains unmet',
            'Stage 5 manufacturing learning assumes one engineering/construction context',
            'All thresholds outside 120-200 EUR/MWh are linear extrapolations, not market forecasts',
        ]
    }
    return ev,context,report

def main():
    ev,ctx,report=analyze(ROOT)
    out=ROOT/'reports';out.mkdir(exist_ok=True)
    ev.to_csv(out/'stage66_strategy_evidence_matrix.csv',index=False)
    ctx.to_csv(out/'stage66_context_synthesis.csv',index=False)
    hashes={k:file_hash(ROOT/v) for k,v in FILES.items() if (ROOT/v).is_file()}
    audit={'status':report['status'],'source_hashes_sha256':hashes,'derived_summary':report}
    (out/'stage66_synthesis_audit.json').write_text(json.dumps(audit,indent=2,allow_nan=False)+'\n')
    rows=['# Stage 6.6 — Integrated Strategic Synthesis','',f"**Status:** `{report['status']}`",'',
          f"- Screened strategy/scenario combinations: **{report['scenarios_screened']}**",
          f"- Economically eligible: **{report['eligible_scenarios']}**",
          f"- Contexts with any eligible strategy: **{report['contexts_with_any_eligible']}/{report['contexts_screened']}**",
          f"- Provisional MCDA leader(s): **{', '.join(report['provisional_leaders'])}**",'',
          '## Baseline zero-NPV joint price thresholds','',
          '| Strategy | EUR/MWh |','|---|---:|']
    for sid,v in report['baseline_joint_thresholds'].items():rows.append(f'| {sid} | {v:.2f} |')
    rows += ['', '**Interpretation:** These are synthetic, fixed-contract thresholds, not forecasts. Thresholds above EUR 200/MWh extrapolate beyond tested prices.', '',
            '## Evidence boundaries','']
    rows += [f'- {x}' for x in report['limitations']]
    rows += ['', '## Strategic conclusion', '',
             ('**Withhold a definitive strategy recommendation**: no tested scenario passes all economic gates.' if report['eligible_scenarios']==0 else '**Compare only gate-eligible strategies**; remaining qualitative and financing criteria are still pending.'),
             'A supplier can show positive company NPV while its hypothetical customer fails the external-investor gate.',
             'Future development should prioritize engineering, manufacturing, contracting, partner financing and market evidence sufficient to rerun these models.', '',
             '## Research hypothesis assessment','',
             '- **H1:** conditional techno-economic relationships evaluated; actual stellarator operating/cost superiority unverified.',
             '- **H2:** hypothetical risk allocations modeled; partnership value and financeability not empirically established.',
             '- **H3:** manufacturing learning improves modeled CAPEX/lifecycle metrics; attainable learning and industrial investment not calibrated.', '',
             '## Stage 7 handover','',
             'Use this document as a numerical synopsis. Keep the research chapter and full source audits as primary evidence. Do not treat ranking, gate count, or extrapolated thresholds as empirical forecasts.', '']
    (out/'stage66_synthesis_summary.md').write_text('\n'.join(rows))
    print('Stage 6.6:',report['status'])
    print(f"Screens: {report['scenarios_screened']} | eligible: {report['eligible_scenarios']} | contexts eligible: {report['contexts_with_any_eligible']}/{report['contexts_screened']}")
    print('Provisional leaders:',report['provisional_leaders'])
    print(ev.to_string(index=False))
    print('Saved: stage66_strategy_evidence_matrix.csv stage66_context_synthesis.csv stage66_synthesis_audit.json stage66_synthesis_summary.md')

if __name__=='__main__':main()
