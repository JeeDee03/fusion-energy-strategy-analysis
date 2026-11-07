"""Stage 5.4.2 reproducible matched dependence sensitivity audit.

Run after the Stage 5.2 uniform baseline and both stress runs exist.
For each mode: compares matched CAPEX ranks, common-rank dependence,
lifecycle results and canonical source hashes. Not convergence certification.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
KEYS = ['seed','context_id','draw_id']
PARAMS = {
    'CAPEX':'capex_eur_per_kwe',
    'FOM':'fixed_opex_eur_million_per_year',
    'VOM':'variable_opex_eur_per_mwh',
    'RATE':'real_discount_rate',
    'PRICE':'electricity_price_eur_per_mwh',
}
OUTPUTS = {
    'break_even':'break_even_eur_2024_per_mwh',
    'NPV':'npv_eur_2024',
}
MODES = ['aligned_burden_stress','offsetting_burden_stress']


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def checked(path, manifest, n, seed):
    if manifest.get('sha256_outputs',{}).get(path.name) != digest(path):
        raise ValueError(f'Output hash mismatch: {path.name}')
    if manifest.get('seed') != seed or manifest.get('sample_size_per_context') != n:
        raise ValueError(f'Seed/n disagreement in {path.name}')
    return pd.read_csv(path)


def run(seed,n):
    reports = ROOT/'reports'
    base_path=reports/f'stage52_draws_seed{seed}_n{n}.csv'
    base_manifest_path=reports/f'stage52_manifest_seed{seed}_n{n}.json'
    base_manifest=json.loads(base_manifest_path.read_text())
    baseline=checked(base_path,base_manifest,n,seed)
    if base_manifest['dependency_mode'] != 'independent_diagnostic' or base_manifest['marginal_design'] != 'exploratory_uniform':
        raise ValueError('Baseline must be independent uniform')
    spec=json.loads((ROOT/'data/stage5_uncertainty_spec.json').read_text())
    definitions={p['parameter_id']:p for p in spec['parameters']}
    choices={m['id']:m for m in spec['dependencies']['modes']}
    if baseline.duplicated(KEYS).any() or baseline.context_id.nunique()!=12 or len(baseline)!=12*n:
        raise ValueError('Baseline has missing or duplicated draw keys')
    results=[]
    inputs=[]
    for mode in MODES:
        path=reports/f'stage54_dependency_{mode}_draws_seed{seed}_n{n}.csv'
        mpath=reports/f'stage54_dependency_{mode}_manifest_seed{seed}_n{n}.json'
        manifest=json.loads(mpath.read_text())
        stress=checked(path,manifest,n,seed)
        if manifest['dependency_mode']!=mode or manifest['marginal_design']!='exploratory_uniform':
            raise ValueError(f'Unexpected stress design: {mode}')
        if manifest.get('sha256_inputs')!=base_manifest.get('sha256_inputs'):
            raise ValueError(f'Input files differ for {mode}')
        for name in ['lifecycle_cash_flow.py','engineering_generation.py']:
            if manifest.get('sha256_scripts',{}).get(name)!=base_manifest.get('sha256_scripts',{}).get(name):
                raise ValueError(f'Lifecycle/engineering code changed: {name}')
        if stress.duplicated(KEYS).any() or stress.context_id.nunique()!=12:
            raise ValueError(f'Duplicate keys / structural context count for {mode}')
        joined=baseline.merge(stress,on=KEYS,suffixes=('_baseline','_stress'),validate='one_to_one')
        if len(joined)!=12*n:
            raise ValueError(f'Unmatched draws for {mode}')
        for col in ['engineering_case_id','construction_case_id','replacement_fraction','net_rated_mwe','finite_life_capacity_factor']:
            a=joined[col+'_baseline'].to_numpy(); b=joined[col+'_stress'].to_numpy()
            if np.issubdtype(a.dtype,np.number):
                np.testing.assert_allclose(a,b,rtol=1e-12,atol=1e-12)
            elif not np.array_equal(a,b):
                raise ValueError(f'Engineering/structural discrepancy: {col}')
        # Use CAPEX rank in each baseline draw as the single common rank.
        capex=definitions['CAPEX']
        u=(joined[PARAMS['CAPEX']+'_baseline'].to_numpy()-capex['lower'])/(capex['upper']-capex['lower'])
        for name,col in PARAMS.items():
            entry=definitions[name]
            sign=choices[mode]['signs'][name]
            r=u if sign==1 else 1.0-u
            expected=entry['lower']+r*(entry['upper']-entry['lower'])
            np.testing.assert_allclose(joined[col+'_stress'].to_numpy(),expected,rtol=2e-12,atol=1e-9,err_msg=f'{mode}:{name}')
        # In all contexts, there should be exactly one vector of inputs per draw_id.
        for col in PARAMS.values():
            if stress.groupby('draw_id')[col].nunique().max()!=1:
                raise ValueError(f'Common random numbers not retained for {mode}:{col}')
        for col in OUTPUTS.values():
            if not (np.isfinite(joined[col+'_baseline']).all() and np.isfinite(joined[col+'_stress']).all()):
                raise ValueError(f'Nonfinite outputs: {mode}:{col}')
        # NPV zero-price relation: linear tariff cash flows imply sign(NPV) = sign(PRICE - break_even).
        margin=joined[PARAMS['PRICE']+'_stress'].to_numpy()-joined['break_even_eur_2024_per_mwh_stress'].to_numpy()
        npv=joined['npv_eur_2024_stress'].to_numpy()
        if np.any(np.sign(margin)!=np.sign(npv)):
            raise ValueError(f'Break-even vs NPV sign inconsistency in {mode}')
        for context,group in joined.groupby('context_id',sort=True):
            row={'seed':seed,'n':n,'mode':mode,'context_id':context}
            for stem,col in OUTPUTS.items():
                x=group[col+'_baseline'].to_numpy()
                y=group[col+'_stress'].to_numpy()
                for percentile,tag in [(0.05,'p05'),(0.50,'p50'),(0.95,'p95')]:
                    row[f'{stem}_baseline_{tag}']=np.quantile(x,percentile,method='linear')
                    row[f'{stem}_stress_{tag}']=np.quantile(y,percentile,method='linear')
                    row[f'{stem}_delta_{tag}']=row[f'{stem}_stress_{tag}']-row[f'{stem}_baseline_{tag}']
                    row[f'{stem}_paired_difference_{tag}']=np.quantile(y-x,percentile,method='linear')
            x=group['npv_eur_2024_baseline'].to_numpy()>0
            y=group['npv_eur_2024_stress'].to_numpy()>0
            row['positive_fraction_baseline']=x.mean()
            row['positive_fraction_stress']=y.mean()
            row['positive_fraction_delta']=y.mean()-x.mean()
            row['positive_outcome_flip_fraction']=(x!=y).mean()
            results.append(row)
        inputs.append({'mode':mode,'input_file':path.name,'sha256':digest(path)})
        print(f'PASS — {mode}: {len(joined):,} matched evaluations, 12 contexts')
    comparison=pd.DataFrame(results)
    output=reports/f'stage54_dependency_comparison_seed{seed}_n{n}.csv'
    comparison.to_csv(output,index=False)
    audit={
        'status':'PASS_PAIRED_DEPENDENCE_AUDIT_NOT_CONVERGENCE_CERTIFIED',
        'seed':seed,'n':n,'contexts':12,'modes':MODES,
        'baseline_file':base_path.name,'baseline_sha256':digest(base_path),
        'stress_inputs':inputs,'comparison_sha256':digest(output),
        'method':'Preserve uniform marginals; stress all inputs with CAPEX common PCG64 rank (or its complement), no estimated copula.',
        'warning':'Stress outcomes not probability bounds or empirical commercial success chances; common-rank stress is not independent iid across five inputs.'
    }
    audit_path=reports/f'stage54_dependency_audit_seed{seed}_n{n}.json'
    audit_path.write_text(json.dumps(audit,indent=2)+'\n')
    print('\nCONTEXT-LEVEL MEDIAN NPV CHANGES (stress minus independent), EUR billion')
    view=comparison[['mode','context_id','NPV_delta_p50','break_even_delta_p50','positive_fraction_delta']].copy()
    view['NPV_delta_p50']=view['NPV_delta_p50']/1e9
    print(view.to_string(index=False))
    print('\nSaved:',output.name,audit_path.name)
    print('Not a convergence certificate, empirical correlation estimate or real-world probability.')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed',type=int,default=20261105)
    parser.add_argument('--n',type=int,default=2048)
    args=parser.parse_args()
    run(args.seed,args.n)
