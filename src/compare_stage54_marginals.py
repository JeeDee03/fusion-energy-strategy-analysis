"""Stage 5.4.1: verify and compare paired uniform/triangular experiments.
Run after both independent-uniform Stage 5.2 and new triangular outputs exist.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
IDS = {'CAPEX':'capex_eur_per_kwe', 'FOM':'fixed_opex_eur_million_per_year',
       'VOM':'variable_opex_eur_per_mwh', 'RATE':'real_discount_rate',
       'PRICE':'electricity_price_eur_per_mwh'}
OUT = ['break_even_eur_2024_per_mwh','npv_eur_2024']

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main(seed, n):
    reports=ROOT/'reports'
    baseline=reports/f'stage52_draws_seed{seed}_n{n}.csv'
    modified=reports/f'stage54_triangular_draws_seed{seed}_n{n}.csv'
    mpath=reports/f'stage54_triangular_manifest_seed{seed}_n{n}.json'
    bpath=reports/f'stage52_manifest_seed{seed}_n{n}.json'
    if not all(p.exists() for p in (baseline,modified,mpath,bpath)):
        raise FileNotFoundError('Both raw datasets and manifests are needed at identical n/seed')
    bm=json.loads(bpath.read_text()); tm=json.loads(mpath.read_text())
    for path,manifest in ((baseline,bm),(modified,tm)):
        if manifest.get('sha256_outputs',{}).get(path.name)!=sha(path):
            raise ValueError(f'File hash mismatch: {path}')
        if manifest.get('seed')!=seed or manifest.get('sample_size_per_context')!=n:
            raise ValueError(f'Manifest seed/n mismatch: {path}')
    if bm.get('marginal_design')!='exploratory_uniform' or tm.get('marginal_design')!='exploratory_triangular':
        raise ValueError('Unexpected marginal design')
    if bm.get('sha256_inputs')!=tm.get('sha256_inputs'):
        raise ValueError('Input hashes differ: study is not comparable')
    for script in ('lifecycle_cash_flow.py','engineering_generation.py'):
        if bm.get('sha256_scripts',{}).get(script)!=tm.get('sha256_scripts',{}).get(script):
            raise ValueError(f'Model script hashes differ: {script}')
    a=pd.read_csv(baseline); b=pd.read_csv(modified)
    keys=['seed','context_id','draw_id']
    assert not a.duplicated(keys).any() and not b.duplicated(keys).any(), 'Duplicate draw key'
    merged=a.merge(b,on=keys,suffixes=('_uniform','_triangular'),validate='one_to_one')
    contexts=sorted(a.context_id.unique())
    assert len(contexts)==12 and set(contexts)==set(b.context_id.unique())
    assert len(merged)==len(a)==len(b)==12*n
    spec=json.loads((ROOT/'data/stage5_uncertainty_spec.json').read_text())
    definitions={p['parameter_id']:p for p in spec['parameters']}
    for ident,column in IDS.items():
        lo,mode,hi=(float(definitions[ident][k]) for k in ('lower','reference','upper'))
        u=(merged[column+'_uniform'].to_numpy()-lo)/(hi-lo)
        frac=(mode-lo)/(hi-lo)
        expected=np.where(u<frac,
              lo+np.sqrt(np.clip(u,0,1)*(hi-lo)*(mode-lo)),
              hi-np.sqrt(np.clip(1-u,0,1)*(hi-lo)*(hi-mode)))
        np.testing.assert_allclose(merged[column+'_triangular'],expected,rtol=1e-10,atol=1e-9,
                                   err_msg='Triangular sample does not match paired uniform rank: '+ident)
    # Verify structural case invariants across designs; only economic draws change.
    for field in ['engineering_case_id','construction_case_id','replacement_fraction',
                  'net_rated_mwe','finite_life_capacity_factor']:
        av=merged[field+'_uniform'].to_numpy(); bv=merged[field+'_triangular'].to_numpy()
        if av.dtype.kind in 'iuf' and bv.dtype.kind in 'iuf':
            np.testing.assert_allclose(av,bv,rtol=1e-12,atol=1e-12)
        else:
            assert np.array_equal(av,bv),f'Case mismatch {field}'
    for name in OUT:
        assert np.isfinite(merged[name+'_uniform']).all()
        assert np.isfinite(merged[name+'_triangular']).all()
    results=[]
    for context,group in merged.groupby('context_id',sort=True):
        row={'seed':seed,'context_id':context,'n':n}
        for field,stem in [(OUT[0],'break_even'),(OUT[1],'NPV')]:
            aa=group[field+'_uniform'].to_numpy()
            bb=group[field+'_triangular'].to_numpy()
            dd=bb-aa
            for q,label in [(0.05,'p05'),(0.5,'p50'),(0.95,'p95')]:
                row[f'{stem}_uniform_{label}']=np.quantile(aa,q,method='linear')
                row[f'{stem}_triangular_{label}']=np.quantile(bb,q,method='linear')
                row[f'{stem}_delta_{label}']=row[f'{stem}_triangular_{label}']-row[f'{stem}_uniform_{label}']
                row[f'{stem}_paired_delta_{label}']=np.quantile(dd,q,method='linear')
        ua=group['npv_eur_2024_uniform'].to_numpy()>0
        ub=group['npv_eur_2024_triangular'].to_numpy()>0
        row['positive_fraction_uniform']=ua.mean()
        row['positive_fraction_triangular']=ub.mean()
        row['positive_fraction_delta']=ub.mean()-ua.mean()
        row['paired_outcome_disagreement_fraction']=np.mean(ua!=ub)
        results.append(row)
    summary=pd.DataFrame(results)
    output=reports/f'stage54_marginal_comparison_seed{seed}_n{n}.csv'
    summary.to_csv(output,index=False)
    audit={
        'status':'PASS_PAIRED_COMPARISON_NOT_CONVERGENCE_CERTIFIED',
        'seed':seed,'sample_size_per_context':n,'contexts':len(contexts),'total_paired_evaluations':len(merged),
        'uniform_input_sha256':sha(baseline),'triangular_input_sha256':sha(modified),
        'comparison_sha256':sha(output),
        'methods':'identical uniform PCG64 ranks mapped by the inverse triangular CDF; each structural context reported separately',
        'interpretation':'analyst_assumption_marginal_sensitivity_not_empirical_probability',
    }
    auditpath=reports/f'stage54_marginal_comparison_audit_seed{seed}_n{n}.json'
    auditpath.write_text(json.dumps(audit,indent=2)+'\n')
    print(f'PASS — {len(merged):,} matched evaluations, {len(contexts)} contexts, seed={seed}, n={n}')
    print('Comparison:',output.name)
    print('Audit:',auditpath.name)
    print('\nCONTEXT-LEVEL MEDIAN CHANGES (triangular minus uniform)')
    print(summary[['context_id','break_even_delta_p50','NPV_delta_p50','positive_fraction_delta']].to_string(index=False))
    print('WARNING — Comparison is conditional on exploratory marginal assumptions; not a convergence or feasibility claim.')

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--seed',type=int,default=20261105)
    p.add_argument('--n',type=int,default=2048)
    args=p.parse_args()
    main(args.seed,args.n)
