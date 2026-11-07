"""Stage 5.4.1 paired exploratory triangular marginal experiment.
Usage: python src/run_stage54_triangular.py --n 128 --seed 20261105
Preserves the Stage 5.2 independent-uniform baseline without changing its files.
"""
import argparse
import hashlib
import itertools
import json
import platform
from pathlib import Path

import numpy as np
import pandas as pd

from lifecycle_cash_flow import calculate_lifecycle, normalize_config

ROOT = Path(__file__).resolve().parents[1]
INPUTS = [
    'data/stage5_uncertainty_spec.json',
    'data/lifecycle_cash_flow_cases.json',
    'data/engineering_generation_cases.csv',
    'data/lcoe_scenarios_stage42.csv',
]


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def sample_parameters(spec, n, seed, marginal_design="exploratory_triangular"):
    """Paired input design: same independent PCG64 uniforms as Stage 5.2.

    Inverse triangular CDF preserves each draw's underlying uniform rank.
    The reference value is the triangle's mode, not an empirical mean.
    """
    rng = np.random.Generator(np.random.PCG64(seed))
    ids = spec['pilot']['sampled_ids']
    definitions = {p['parameter_id']: p for p in spec['parameters']}
    u = rng.random((n, len(ids)))
    draws = {}
    for j, ident in enumerate(ids):
        p = definitions[ident]
        if p['distribution'] != 'exploratory_uniform':
            raise ValueError('Unrecognized canonical pilot distribution: ' + ident)
        lower, mode, upper = (float(p[k]) for k in ('lower','reference','upper'))
        if not lower < upper or not lower <= mode <= upper:
            raise ValueError(f'Invalid triangular bounds/mode: {ident}')
        if marginal_design == 'exploratory_triangular':
            fraction = (mode - lower) / (upper - lower)
            draws[ident] = np.where(
                u[:, j] < fraction,
                lower + np.sqrt(u[:, j] * (upper - lower) * (mode - lower)),
                upper - np.sqrt((1.0 - u[:, j]) * (upper - lower) * (upper - mode)),
            )
        elif marginal_design == 'exploratory_uniform':
            draws[ident] = lower + u[:, j] * (upper - lower)
        else:
            raise ValueError('Unsupported marginal design')
        if not np.isfinite(draws[ident]).all():
            raise RuntimeError(f'Nonfinite sample for {ident}')
    return pd.DataFrame(draws).assign(draw_id=np.arange(n, dtype=int))


def run(n, seed, outdir=None):
    spec_path = ROOT / INPUTS[0]
    spec = json.loads(spec_path.read_text(encoding='utf-8'))
    if spec['schema_version'] != 1 or spec['design_status'] != 'specified_not_simulated':
        raise ValueError('Unexpected specification version/status')
    plan = spec['sampling_plan']
    if plan['generator'] != 'numpy.random.Generator_PCG64':
        raise ValueError('Unsupported generator')
    if seed not in plan['master_seeds']:
        raise ValueError('Seed not listed in canonical specification')
    permitted = plan['sample_sizes'] + [plan['extension_size_if_needed']]
    if n not in permitted and n not in (16, 32, 64, 128, 256):
        raise ValueError('n must be a canonical sample size or an explicit small pilot size')
    pilot = spec['pilot']
    if pilot['context_weights'] is not None:
        raise ValueError('Structural contexts must not be probabilistically weighted')
    if pilot['sampled_ids'] != ['CAPEX','FOM','VOM','RATE','PRICE']:
        raise ValueError('Unexpected sampled parameters')

    outdir = Path(outdir) if outdir else ROOT / 'reports'
    outdir.mkdir(parents=True, exist_ok=True)
    draws = sample_parameters(spec, n, seed, marginal_design="exploratory_triangular")

    scenarios = pd.read_csv(ROOT / 'data/lcoe_scenarios_stage42.csv')
    base_rows = scenarios.loc[scenarios['scenario_id'].eq('CAL002')]
    if len(base_rows) != 1:
        raise ValueError('One CAL002 reference case required')
    baseline = base_rows.iloc[0].to_dict()
    reference_mwe = float(baseline['net_power_mwe'])
    if reference_mwe != 1000.0:
        raise ValueError('Spec requires fixed 1000 MWe CAPEX reference')
    baseline['plant_lifetime_years'] = 35

    eng_rows = pd.read_csv(ROOT / 'data/engineering_generation_cases.csv')
    if not eng_rows['scenario_id'].is_unique:
        raise ValueError('Duplicate engineering scenario')
    engineering = eng_rows.set_index('scenario_id')
    cases = json.loads((ROOT / 'data/lifecycle_cash_flow_cases.json').read_text())['cases']
    lifecycle_cases = {c['scenario_id']: c for c in cases}
    if len(lifecycle_cases) != len(cases):
        raise ValueError('Duplicate lifecycle scenario')

    all_outputs = []
    contexts = list(itertools.product(
        pilot['engineering_case_ids'],
        pilot['construction_case_ids'],
        pilot['replacement_fractions_of_sampled_initial_CAPEX'],
    ))
    if len(contexts) != 12:
        raise ValueError('Expected 12 structural contexts')

    for engineering_id, construction_id, replacement_fraction in contexts:
        if engineering_id not in engineering.index or construction_id not in lifecycle_cases:
            raise ValueError('Structural reference missing')
        eng = engineering.loc[engineering_id].to_dict()
        config_base = lifecycle_cases[construction_id].copy()
        config_base['engineering_case_id'] = engineering_id
        if config_base['generation_mode'] != 'engineering_events':
            raise ValueError('Engineering events required')

        context_id = f'{engineering_id}_{construction_id}_R{round(replacement_fraction*100):02d}'
        rows = []
        for draw in draws.itertuples(index=False):
            capex_eur = float(draw.CAPEX) * reference_mwe * 1000
            case = baseline.copy()
            case.update({
                'capex_eur_million': capex_eur / 1e6,
                'fixed_opex_eur_million_per_year': float(draw.FOM),
                'variable_opex_eur_per_mwh': float(draw.VOM),
                'real_discount_rate': float(draw.RATE),
            })
            config = config_base.copy()
            config['replacement_cost_eur_million'] = capex_eur * replacement_fraction / 1e6
            config = normalize_config(config)
            try:
                _, _, metrics = calculate_lifecycle(case, float(draw.PRICE), config, eng)
            except Exception as exc:
                raise RuntimeError(f'Invalid draw: {context_id} seed={seed} draw={draw.draw_id} '
                                   f'CAPEX={draw.CAPEX} FOM={draw.FOM} VOM={draw.VOM} '
                                   f'RATE={draw.RATE} PRICE={draw.PRICE}') from exc
            rows.append({
                'seed': seed, 'draw_id': int(draw.draw_id), 'context_id': context_id,
                'engineering_case_id': engineering_id,
                'construction_case_id': construction_id,
                'replacement_fraction': replacement_fraction,
                'dependency_mode': 'independent_diagnostic',
                'marginal_design': 'exploratory_triangular',
                'capex_eur_per_kwe': float(draw.CAPEX),
                'fixed_opex_eur_million_per_year': float(draw.FOM),
                'variable_opex_eur_per_mwh': float(draw.VOM),
                'real_discount_rate': float(draw.RATE),
                'electricity_price_eur_per_mwh': float(draw.PRICE),
                'net_rated_mwe': metrics['net_rated_mwe'],
                'finite_life_capacity_factor': metrics['finite_life_capacity_factor'],
                'replacement_count': metrics['replacement_count'],
                'break_even_eur_2024_per_mwh': metrics['break_even_eur_2024_per_mwh'],
                'npv_eur_2024': metrics['npv_eur'],
                'npv_positive': int(metrics['npv_eur'] > 0),
            })
        all_outputs.extend(rows)
        print(f'Completed {context_id}: {n} draws', flush=True)

    results = pd.DataFrame(all_outputs)
    if len(results) != n * len(contexts) or not np.isfinite(results.select_dtypes(include='number').to_numpy()).all():
        raise RuntimeError('Missing/nonfinite simulation output')
    summaries = []
    for context, group in results.groupby('context_id', sort=True):
        summaries.append({
            'seed': seed, 'context_id': context, 'sample_size': n,
            'lifecycle_break_even_p05': group['break_even_eur_2024_per_mwh'].quantile(.05),
            'lifecycle_break_even_p50': group['break_even_eur_2024_per_mwh'].quantile(.50),
            'lifecycle_break_even_p95': group['break_even_eur_2024_per_mwh'].quantile(.95),
            'npv_p05_eur': group['npv_eur_2024'].quantile(.05),
            'npv_p50_eur': group['npv_eur_2024'].quantile(.50),
            'npv_p95_eur': group['npv_eur_2024'].quantile(.95),
            'conditional_fraction_npv_positive': group['npv_positive'].mean(),
            'interpretation': 'conditional_exploratory_not_real_world_success_probability',
        })
    summary = pd.DataFrame(summaries)
    suffix = f'seed{seed}_n{n}'
    sample_path = outdir / f'stage54_triangular_draws_{suffix}.csv'
    summary_path = outdir / f'stage54_triangular_summary_{suffix}.csv'
    manifest_path = outdir / f'stage54_triangular_manifest_{suffix}.json'
    results.to_csv(sample_path, index=False)
    summary.to_csv(summary_path, index=False)
    script_path = Path(__file__).resolve()
    manifest = {
        'status': 'PILOT_NOT_CONVERGENCE_CERTIFIED',
        'design_status': spec['design_status'],
        'interpretation': 'conditional_exploratory_not_real_world_success_probability',
        'generator': 'numpy.random.Generator(PCG64)',
        'seed': seed, 'sample_size_per_context': n, 'contexts': len(contexts),
        'total_evaluations': len(results), 'invalid_count': 0,
        'dependency_mode': 'independent_diagnostic', 'marginal_design': 'exploratory_triangular',
        'python_version': platform.python_version(), 'numpy_version': np.__version__,
        'pandas_version': pd.__version__,
        'sha256_inputs': {name: sha256(ROOT / name) for name in INPUTS},
        'sha256_scripts': {
            'run_stage54_triangular.py': sha256(script_path),
            'lifecycle_cash_flow.py': sha256(ROOT/'src/lifecycle_cash_flow.py'),
            'engineering_generation.py': sha256(ROOT/'src/engineering_generation.py'),
        },
        'sha256_outputs': {sample_path.name:sha256(sample_path),summary_path.name:sha256(summary_path)},
    }
    manifest_path.write_text(json.dumps(manifest, indent=2)+'\n',encoding='utf-8')
    print('\nSaved:', sample_path.name, summary_path.name, manifest_path.name)
    print('This independent-triangular sensitivity experiment is NOT an empirical success probability or convergence certification.')
    return results, summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--n', type=int, default=128)
    parser.add_argument('--seed', type=int, default=20261105)
    parser.add_argument('--outdir', type=Path, default=None)
    args = parser.parse_args()
    run(args.n, args.seed, args.outdir)
