"""Validate Stage 5.4.3 H3 boundary identities and exact FOAK reconciliation.

Usage: python src/validate_stage543_learning.py --n 2048 --seed 20261105
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from run_stage5_monte_carlo import ROOT, sha256


def check(n,seed):
    folder=ROOT/'reports';suffix=f'seed{seed}_n{n}'
    dpath=folder/f'stage543_learning_draws_{suffix}.csv'
    spath=folder/f'stage543_learning_summary_{suffix}.csv'
    mpath=folder/f'stage543_learning_manifest_{suffix}.json'
    df=pd.read_csv(dpath);summ=pd.read_csv(spath);manifest=json.loads(mpath.read_text())
    if len(df)!=n*5 or len(summ)!=5:raise AssertionError('Wrong H3 coverage')
    for p,h in manifest['sha256_inputs_scripts'].items():
        if sha256(ROOT/p)!=h:raise AssertionError(f'Changed source: {p}')
    for name,h in manifest['sha256_outputs'].items():
        if sha256(folder/name)!=h:raise AssertionError(f'Changed output: {name}')
    pivot=df.pivot(index='draw_id',columns='cumulative_equivalent_units')
    if len(pivot)!=n or list(pivot['total_capex_learning_factor'].columns)!=[1,2,4,8,16]:
        raise AssertionError('Bad paired learning levels')
    if not np.allclose(pivot['total_capex_learning_factor'][1],1,rtol=0,atol=1e-12):
        raise AssertionError('N=1 must have exactly unlearned CAPEX')
    if np.any(np.diff(pivot['learned_initial_capex_eur'].to_numpy(),axis=1)>0.01):
        raise AssertionError('CAPEX rises with production doublings')
    if np.any(np.diff(pivot['break_even_eur_2024_per_mwh'].to_numpy(),axis=1)>1e-7):
        raise AssertionError('Break-even rises with learning')
    if np.any(np.diff(pivot['npv_eur_2024'].to_numpy(),axis=1)<-0.05):
        raise AssertionError('NPV falls with learning')
    if not np.allclose(df['replacement_cost_eur'],.05*df['unlearned_initial_capex_eur'],rtol=1e-12,atol=.01):
        raise AssertionError('Replacement double counting / unintended learning')
    if not np.allclose(df['learned_initial_capex_eur'],df['unlearned_initial_capex_eur']*df['total_capex_learning_factor'],rtol=1e-12,atol=.01):
        raise AssertionError('Incorrect learning identity')
    for key in ('magnet_capex_share','magnet_learning_rate'):
        defs={p['parameter_id']:p for p in json.loads((ROOT/'data/stage5_uncertainty_spec.json').read_text())['parameters']}
        ident='SHARE' if key=='magnet_capex_share' else 'LEARNING'
        if not df[key].between(defs[ident]['lower'],defs[ident]['upper']).all():
            raise AssertionError('H3 input range violated')
    # Directly reconcile the exact baseline FOAK results from the Stage 5.2 dataset.
    prior=folder/f'stage52_draws_{suffix}.csv'
    if not prior.exists():raise FileNotFoundError('Existing matching Stage 5.2 FOAK dataset required: '+str(prior))
    prior_df=pd.read_csv(prior)
    prior_df=prior_df[prior_df['context_id'].eq('GEN002_LC004_R05')].sort_values('draw_id')
    base=df[df['cumulative_equivalent_units'].eq(1)].sort_values('draw_id')
    if len(prior_df)!=n or len(base)!=n or not np.array_equal(prior_df['draw_id'],base['draw_id']):
        raise AssertionError('FOAK draw IDs mismatch')
    for field in ['break_even_eur_2024_per_mwh','npv_eur_2024']:
        if not np.allclose(prior_df[field],base[field],rtol=1e-10,atol=.01):
            raise AssertionError('FOAK model reconciliation failed: '+field)
    for _,r in summ.iterrows():
        group=df[df['cumulative_equivalent_units'].eq(r['cumulative_equivalent_units'])]
        if not np.isclose(r['break_even_p50'],group['break_even_eur_2024_per_mwh'].quantile(.5)):
            raise AssertionError('Incorrect median')
    print(f'PASS — {len(df):,} H3 evaluations, {n:,} matched draws at five learning levels')
    print('PASS — FOAK reconciliation, CAPEX/replacement boundary, monotonicity, hashes, and quantiles')
    print('WARNING — No empirically calibrated learning, NOAK economics or convergence certification')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=2048);p.add_argument('--seed',type=int,default=20261105)
    a=p.parse_args();check(a.n,a.seed)
