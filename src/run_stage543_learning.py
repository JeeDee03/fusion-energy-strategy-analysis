"""Stage 5.4.3 exploratory magnet-system learning with matched FOAK draws.

Usage: python src/run_stage543_learning.py --n 2048 --seed 20261105
This is not a verified NOAK or commercial deployment model.
"""
import argparse
import hashlib
import json
import platform
from pathlib import Path

import numpy as np
import pandas as pd

from run_stage5_monte_carlo import ROOT, INPUTS, sample_parameters, sha256
from lifecycle_cash_flow import calculate_lifecycle, normalize_config

CONTEXT = 'GEN002_LC004_R05'
SCRIPT = Path(__file__).resolve()


def run(n, seed):
    spec = json.loads((ROOT / 'data/stage5_uncertainty_spec.json').read_text())
    plan = spec['sampling_plan']
    ext = spec['learning_extension']
    if ext['status'] != 'specified_not_simulated' or ext['sampled_ids'] != ['SHARE','LEARNING']:
        raise ValueError('Unrecognized H3 specification')
    if ext['context_engineering_case'] != 'GEN002' or ext['construction_case'] != 'LC004' or float(ext['replacement_fraction']) != .05:
        raise ValueError('Unexpected H3 structural context')
    units = list(ext['cumulative_units'])
    if units != [1,2,4,8,16] or ext['replacement_rule'] != 'fraction_of_unlearned_sampled_initial_CAPEX_no_automatic_learning_on_replacements':
        raise ValueError('Unsupported learning or replacement rule')
    if seed not in plan['master_seeds'] or n not in plan['sample_sizes'] + [plan['extension_size_if_needed']]:
        raise ValueError('Use canonical seed and sample size')
    definitions = {p['parameter_id']:p for p in spec['parameters']}
    for key in ('SHARE','LEARNING'):
        if definitions[key]['distribution'] != 'exploratory_uniform' or definitions[key]['role'] != 'learning_extension':
            raise ValueError('Unsupported H3 marginal')

    # The five economic inputs are identical to the Stage 5.2 independent-uniform baseline.
    econ = sample_parameters(spec,n,seed)
    # A separate seed-derived PCG64 stream only for the two H3 parameters.
    rng = np.random.Generator(np.random.PCG64(np.random.SeedSequence([seed,543])))
    u = rng.random((n,2))
    share = definitions['SHARE']['lower'] + u[:,0]*(definitions['SHARE']['upper']-definitions['SHARE']['lower'])
    learning = definitions['LEARNING']['lower'] + u[:,1]*(definitions['LEARNING']['upper']-definitions['LEARNING']['lower'])

    base_table = pd.read_csv(ROOT/'data/lcoe_scenarios_stage42.csv')
    selected = base_table[base_table['scenario_id'].eq('CAL002')]
    if len(selected)!=1 or float(selected.iloc[0]['net_power_mwe'])!=1000:
        raise ValueError('CAL002 reference missing or unexpected')
    base = selected.iloc[0].to_dict()
    base['plant_lifetime_years'] = 35
    engineering = pd.read_csv(ROOT/'data/engineering_generation_cases.csv')
    selected = engineering[engineering['scenario_id'].eq('GEN002')]
    if len(selected)!=1: raise ValueError('Engineering case must be unique')
    eng = selected.iloc[0].to_dict()
    cases = json.loads((ROOT/'data/lifecycle_cash_flow_cases.json').read_text())['cases']
    selected = [c for c in cases if c['scenario_id']=='LC004']
    if len(selected)!=1: raise ValueError('Construction case must be unique')
    config_base = selected[0].copy()
    config_base['engineering_case_id'] = 'GEN002'
    if config_base['generation_mode']!='engineering_events':
        raise ValueError('Engineering events required')

    results = []
    for idx, draw in enumerate(econ.itertuples(index=False)):
        initial_capex_eur = float(draw.CAPEX)*1000*1000
        s=float(share[idx]); lr=float(learning[idx])
        for num_units in units:
            factor = 1-s+s*(1-lr)**np.log2(num_units)
            if not (0 < factor <= 1.00000000001):
                raise ValueError('Invalid cost reduction factor')
            learned_capex_eur = initial_capex_eur * factor
            case=base.copy()
            case.update({
                'capex_eur_million': learned_capex_eur/1e6,
                'fixed_opex_eur_million_per_year':float(draw.FOM),
                'variable_opex_eur_per_mwh':float(draw.VOM),
                'real_discount_rate':float(draw.RATE),
            })
            config=config_base.copy()
            # IMPORTANT: replacements remain linked to the UNLEARNED initial CAPEX.
            config['replacement_cost_eur_million'] = .05*initial_capex_eur/1e6
            config=normalize_config(config)
            try:
                _,_,metrics=calculate_lifecycle(case,float(draw.PRICE),config,eng)
            except Exception as exc:
                raise RuntimeError(f'Invalid H3 draw seed={seed} draw={idx} N={num_units}') from exc
            results.append({
                'seed':seed,'draw_id':idx,'context_id':CONTEXT,'cumulative_equivalent_units':num_units,
                'capex_eur_per_kwe_unlearned':float(draw.CAPEX),
                'fixed_opex_eur_million_per_year':float(draw.FOM),
                'variable_opex_eur_per_mwh':float(draw.VOM),
                'real_discount_rate':float(draw.RATE),
                'electricity_price_eur_per_mwh':float(draw.PRICE),
                'magnet_capex_share':s,'magnet_learning_rate':lr,
                'total_capex_learning_factor':factor,
                'learned_initial_capex_eur':learned_capex_eur,
                'unlearned_initial_capex_eur':initial_capex_eur,
                'replacement_cost_eur':.05*initial_capex_eur,
                'break_even_eur_2024_per_mwh':metrics['break_even_eur_2024_per_mwh'],
                'npv_eur_2024':metrics['npv_eur'],
                'npv_positive':int(metrics['npv_eur']>0),
            })
    df=pd.DataFrame(results)
    if len(df)!=n*len(units) or not np.isfinite(df.select_dtypes(include='number').to_numpy()).all():
        raise RuntimeError('Missing or nonfinite H3 results')
    output=[]
    for n_units, group in df.groupby('cumulative_equivalent_units',sort=True):
        output.append({
            'seed':seed,'sample_size':n,'context_id':CONTEXT,'cumulative_equivalent_units':n_units,
            'break_even_p05':group['break_even_eur_2024_per_mwh'].quantile(.05),
            'break_even_p50':group['break_even_eur_2024_per_mwh'].quantile(.5),
            'break_even_p95':group['break_even_eur_2024_per_mwh'].quantile(.95),
            'npv_p05_eur':group['npv_eur_2024'].quantile(.05),
            'npv_p50_eur':group['npv_eur_2024'].quantile(.5),
            'npv_p95_eur':group['npv_eur_2024'].quantile(.95),
            'positive_fraction':group['npv_positive'].mean(),
            'mean_capex_reduction_fraction':1-group['total_capex_learning_factor'].mean(),
        })
    summary=pd.DataFrame(output)
    folder=ROOT/'reports';folder.mkdir(exist_ok=True)
    suffix=f'seed{seed}_n{n}'
    draw_path=folder/f'stage543_learning_draws_{suffix}.csv'
    summary_path=folder/f'stage543_learning_summary_{suffix}.csv'
    manifest_path=folder/f'stage543_learning_manifest_{suffix}.json'
    df.to_csv(draw_path,index=False);summary.to_csv(summary_path,index=False)
    paths=INPUTS + ['src/run_stage5_monte_carlo.py','src/run_stage543_learning.py','src/lifecycle_cash_flow.py','src/engineering_generation.py']
    manifest={
        'status':'EXPLORATORY_H3_NOT_CONVERGENCE_CERTIFIED',
        'seed':seed,'n_per_level':n,'cumulative_equivalent_units':units,
        'context_id':CONTEXT,'total_evaluations':len(df),
        'generator':'NumPy PCG64; Stage 5.2 economic stream + SeedSequence([seed,543]) H3 stream',
        'sampling':'independent exploratory uniform SHARE and LEARNING; common draws across unit levels',
        'replacement_rule':'5% of UNLEARNED initial CAPEX at each replacement',
        'limitations':'No factory investment, scale-up expenditure, deployment learning evidence, or NOAK claim',
        'python_version':platform.python_version(),'numpy_version':np.__version__,'pandas_version':pd.__version__,
        'sha256_inputs_scripts':{p:sha256(ROOT/p) for p in paths},
        'sha256_outputs':{p.name:sha256(p) for p in [draw_path,summary_path]},
    }
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
    print(summary[['cumulative_equivalent_units','mean_capex_reduction_fraction','break_even_p50','npv_p50_eur','positive_fraction']].to_string(index=False))
    print('Saved:',draw_path.name,summary_path.name,manifest_path.name)
    print('Exploratory H3 sensitivity only; not empirically calibrated NOAK costs.')

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--n',type=int,default=2048)
    p.add_argument('--seed',type=int,default=20261105)
    a=p.parse_args()
    run(a.n,a.seed)
