"""Stage 5.3: conditional convergence and within-context rank sensitivity.

Reads Stage 5.2 output, does NOT rerun the lifecycle model.
Run: python src/analyze_stage53.py
Option: --reports-dir reports
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT_COLUMNS = {
    'CAPEX': 'capex_eur_per_kwe',
    'FOM': 'fixed_opex_eur_million_per_year',
    'VOM': 'variable_opex_eur_per_mwh',
    'RATE': 'real_discount_rate',
    'PRICE': 'electricity_price_eur_per_mwh',
}
OUTPUT_COLUMNS = {
    'break_even': 'break_even_eur_2024_per_mwh',
    'NPV': 'npv_eur_2024',
}
REQUIRED = ['seed','draw_id','context_id','dependency_mode','marginal_design',
            'npv_positive', *INPUT_COLUMNS.values(), *OUTPUT_COLUMNS.values()]
QUANTILES = (.05, .5, .95)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def wilson_half_width(k, n, z=1.959963984540054):
    p = k / n
    return z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)


def load_largest_valid_seed(reports, seed, spec):
    candidates = sorted(reports.glob(f'stage52_draws_seed{seed}_n*.csv'))
    if not candidates:
        return None
    parsed = []
    for p in candidates:
        ntext = p.stem.split('_n')[-1]
        if ntext.isdigit():
            parsed.append((int(ntext), p))
    if not parsed:
        return None
    n, path = max(parsed)
    manifest_path = reports / f'stage52_manifest_seed{seed}_n{n}.json'
    if not manifest_path.exists():
        raise RuntimeError(f'Missing manifest: {manifest_path}')
    manifest = json.loads(manifest_path.read_text())
    if manifest['sha256_outputs'].get(path.name) != sha256(path):
        raise RuntimeError(f'Output hash mismatch: {path}')
    for rel, digest in manifest['sha256_inputs'].items():
        if sha256(ROOT / rel) != digest:
            raise RuntimeError(f'Stage 5.2 input changed since run: {rel}; rerun simulation')
    for rel, digest in manifest['sha256_scripts'].items():
        if sha256(ROOT / 'src' / rel) != digest:
            raise RuntimeError(f'Stage 5.2 script changed since run: {rel}; rerun simulation')
    df = pd.read_csv(path, usecols=lambda c: c in REQUIRED)
    if set(REQUIRED) - set(df.columns):
        raise RuntimeError(f'Missing output columns: {set(REQUIRED) - set(df.columns)}')
    if df['seed'].nunique() != 1 or df['seed'].iloc[0] != seed:
        raise RuntimeError('Seed mismatch')
    if df['dependency_mode'].nunique() != 1 or df['dependency_mode'].iloc[0] != 'independent_diagnostic':
        raise RuntimeError('Only independent-diagnostic design is supported here')
    if df['marginal_design'].nunique() != 1 or df['marginal_design'].iloc[0] != 'exploratory_uniform':
        raise RuntimeError('Only exploratory-uniform marginal design supported here')
    if len(df) != 12 * n or df['context_id'].nunique() != 12:
        raise RuntimeError(f'Wrong context coverage for seed {seed}')
    if df.duplicated(['context_id', 'draw_id']).any():
        raise RuntimeError('Duplicate draw/context pairs')
    if not df.groupby('context_id').size().eq(n).all():
        raise RuntimeError('Uneven context sample counts')
    if not np.isfinite(df.select_dtypes('number')).all().all():
        raise RuntimeError('Nonfinite output')
    for context, group in df.groupby('context_id'):
        if not np.array_equal(np.sort(group.draw_id.to_numpy()), np.arange(n)):
            raise RuntimeError(f'Missing draw ids: {context}')
    for col in INPUT_COLUMNS.values():
        if not df.groupby('draw_id')[col].nunique().eq(1).all():
            raise RuntimeError(f'Common random number mismatch in {col}')
    return df, n, path.name


def generate_reports(reports):
    spec = json.loads((ROOT / 'data/stage5_uncertainty_spec.json').read_text())
    seeds = spec['sampling_plan']['master_seeds']
    levels = spec['sampling_plan']['sample_sizes']
    acceptance = spec['acceptance']
    quantile_rows = []
    convergence_rows = []
    sensitivity_rows = []
    context_effect_rows = []
    loaded = []
    loaded_seeds = []
    baseline_context = 'GEN002_LC004_R05'

    for seed in seeds:
        item = load_largest_valid_seed(reports, seed, spec)
        if item is None:
            print(f'MISSING seed {seed}')
            continue
        df, n_max, filename = item
        loaded_seeds.append(seed)
        loaded.append({'seed': seed, 'max_n': n_max, 'source': filename})
        print(f'CHECKED seed={seed}, n={n_max}, file={filename}', flush=True)
        for context, group in df.groupby('context_id', sort=True):
            ordered = group.sort_values('draw_id').reset_index(drop=True)
            # Evaluate quantiles from nested prefixes of the same PCG64 sample stream.
            available_levels = [level for level in levels if level <= n_max]
            if n_max < levels[0]:
                available_levels = [n_max]  # exploratory smoke test, not convergence evidence
            for n in available_levels:
                part = ordered.iloc[:n]
                p_positive = float(part.npv_positive.mean())
                qrow = {'seed':seed, 'context_id':context, 'sample_size':n,
                        'conditional_fraction_npv_positive':p_positive,
                        'wilson_half_width_95':wilson_half_width(int(part.npv_positive.sum()), n)}
                for metric, col in OUTPUT_COLUMNS.items():
                    for p in QUANTILES:
                        qrow[f'{metric}_p{round(p*100):02d}'] = float(part[col].quantile(p, interpolation='linear'))
                quantile_rows.append(qrow)
            # Only rank associations within same context and at the largest available sample size.
            for outcome, out_col in OUTPUT_COLUMNS.items():
                for name, col in INPUT_COLUMNS.items():
                    rho = ordered[col].rank(method='average').corr(
                        ordered[out_col].rank(method='average'))
                    sensitivity_rows.append({'seed':seed,'context_id':context,'sample_size':n_max,
                                             'outcome':outcome,'input_parameter':name,
                                             'spearman_rho':float(rho), 'abs_rho':abs(float(rho)),
                                             'interpretation':'marginal_rank_association_not_causal'})
        # Matched common-random-number differences relative to baseline within this seed.
        baseline_rows = df.loc[df.context_id.eq(baseline_context), ['draw_id', *OUTPUT_COLUMNS.values()]]
        if len(baseline_rows) != n_max:
            raise RuntimeError('Baseline context missing')
        for context, group in df.groupby('context_id',sort=True):
            joined = group[['draw_id', *OUTPUT_COLUMNS.values()]].merge(
                baseline_rows,on='draw_id',suffixes=('_case','_baseline'),validate='one_to_one')
            for outcome, col in OUTPUT_COLUMNS.items():
                delta = joined[f'{col}_case'] - joined[f'{col}_baseline']
                context_effect_rows.append({'seed':seed,'context_id':context,
                                            'reference_context':baseline_context,'sample_size':n_max,
                                            'outcome':outcome, 'median_matched_delta':float(delta.median()),
                                            'p05_matched_delta':float(delta.quantile(.05)),
                                            'p95_matched_delta':float(delta.quantile(.95)),
                                            'interpretation':'matched_conditional_structural_difference_not_probability_weighted'})
        del df

    quant = pd.DataFrame(quantile_rows)
    if quant.empty:
        raise RuntimeError('No Stage 5.2 CSV files found; run pilot(s) first.')

    # Compare the successive 2048->8192 and 8192->32768 prefixes for every seed/context.
    for (seed, context), g in quant.groupby(['seed','context_id']):
        g = g.set_index('sample_size')
        for a,b in zip(levels[:-1], levels[1:]):
            if a not in g.index or b not in g.index:
                convergence_rows.append({'seed':seed,'context_id':context,'from_n':a,'to_n':b,
                    'metric':'all_required','status':'INCOMPLETE','absolute_change':np.nan,'tolerance':np.nan})
                continue
            for outcome in ('break_even', 'NPV'):
                abs_tol = acceptance['break_even_quantile_abs_tolerance_eur_per_mwh'] if outcome == 'break_even' else acceptance['npv_quantile_abs_tolerance_eur']
                rel_tol = acceptance['break_even_quantile_relative_tolerance'] if outcome == 'break_even' else acceptance['npv_quantile_relative_tolerance']
                for p in QUANTILES:
                    metric = f'{outcome}_p{round(p*100):02d}'
                    older, newer = float(g.loc[a,metric]), float(g.loc[b,metric])
                    difference = abs(newer - older)
                    tolerance = max(abs_tol, rel_tol * abs(older))
                    convergence_rows.append({'seed':seed,'context_id':context,'from_n':a,'to_n':b,
                                             'metric':metric,'status':'PASS' if difference <= tolerance else 'FAIL',
                                             'absolute_change':difference,'tolerance':tolerance})
            precision = float(g.loc[b,'wilson_half_width_95'])
            allowed = float(acceptance['fraction_MC_half_width_max'])
            convergence_rows.append({'seed':seed,'context_id':context,'from_n':a,'to_n':b,
                 'metric':'npv_positive_wilson_half_width','status':'PASS' if precision <= allowed else 'FAIL',
                 'absolute_change':precision,'tolerance':allowed})
    conv = pd.DataFrame(convergence_rows)
    complete = (len(loaded_seeds) == len(seeds) and
                all(x['max_n'] >= levels[-1] for x in loaded))
    failed = int(conv.status.eq('FAIL').sum())
    if not complete:
        status='INCOMPLETE'
    elif failed:
        status='NONCONVERGED'
    else:
        status='PASS_INDEPENDENT_UNIFORM_ONLY'

    # These files are separate and are not allowed to overwrite Stage 5.2 data.
    quant.to_csv(reports/'stage53_nested_quantiles.csv',index=False)
    conv.to_csv(reports/'stage53_convergence_checks.csv',index=False)
    pd.DataFrame(sensitivity_rows).to_csv(reports/'stage53_rank_sensitivity.csv',index=False)
    pd.DataFrame(context_effect_rows).to_csv(reports/'stage53_matched_context_effects.csv',index=False)
    audit={'stage':'5.3','status':status,'design':'independent_uniform_only',
           'canonical_sample_sizes':levels,'required_seeds':seeds,
           'processed':loaded,'failed_refinement_tests':failed,
           'consecutive_refinements_required':2,
           'notes':[
             'Convergence checks use nested prefixes within each independent seed.',
             'Results do not establish empirical probability of Proxima commercial success.',
             'Structural contexts are not probability weighted.',
             'Spearman associations are not causal effects or independent variance shares.',
             'Full Stage 5 convergence across distribution and dependence designs is not assessed here.',
             'Marginal and dependence stress designs are reserved for Stage 5.4.',
           ]}
    (reports/'stage53_audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    markdown=['# Stage 5.3 — Convergence and Sensitivity Audit','',f'**Status: {status}**','',
              'Design: exploratory-uniform, independent inputs, separate structural contexts.','',
              f'Loaded seeds: {len(loaded_seeds)}/{len(seeds)}.','',
              f'Failed completed refinement checks: {failed}.','',
              '## Available simulation files','']
    markdown += [f"- Seed {item['seed']}: n={item['max_n']} ({item['source']})" for item in loaded]
    markdown += ['', '## Interpretation','',
                 'A PASS applies **only to the independent-uniform diagnostic**; it does not establish empirical success probabilities, causality, calibration, or convergence of the dependence/marginal designs.','',
                 'Sensitivity figures are within-context Spearman rank associations; structural comparisons use matched draws.','',
                 'Review `stage53_convergence_checks.csv`, especially any FAIL/INCOMPLETE rows, before making claims.','']
    (reports/'stage53_audit.md').write_text('\n'.join(markdown))
    print('\nSTAGE 5.3:',status,'| loaded seeds:',len(loaded_seeds),'| failed refinement tests:',failed)
    print('Outputs: stage53_nested_quantiles.csv, stage53_convergence_checks.csv, stage53_rank_sensitivity.csv, stage53_matched_context_effects.csv, stage53_audit.json, stage53_audit.md')
    return status


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reports-dir',type=Path,default=ROOT/'reports')
    args=parser.parse_args()
    generate_reports(args.reports_dir)
