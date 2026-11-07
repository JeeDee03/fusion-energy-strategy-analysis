"""Stage 5.5: preliminary cross-seed, cross-experiment research summary.

Requires 8192-draw Stage 5.4 marginal/dependence/learning outputs for four seeds.
Does not certify convergence or empirical probabilities.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / 'reports'
SEEDS = [20261105, 20261106, 20261107, 20261108]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def collect(pattern, audit_pattern, n):
    frames, inputs = [], []
    for seed in SEEDS:
        p = REPORTS / pattern.format(seed=seed, n=n)
        audit_path = REPORTS / audit_pattern.format(seed=seed, n=n)
        if not p.is_file() or not audit_path.is_file():
            raise FileNotFoundError(f'Missing output or audit for seed {seed}: {p.name}, {audit_path.name}')
        audit = json.loads(audit_path.read_text())
        if not str(audit.get('status', '')).startswith('PASS'):
            raise RuntimeError(f'Comparison audit not PASS: {audit_path.name}')
        df = pd.read_csv(p)
        if 'seed' not in df.columns or set(df['seed']) != {seed}:
            raise ValueError(f'Seed mismatch in {p.name}')
        frames.append(df)
        inputs.extend([{'file': p.name, 'sha256': sha256(p)},
                       {'file': audit_path.name, 'sha256': sha256(audit_path)}])
    return pd.concat(frames, ignore_index=True), inputs


def main(n):
    marginal, input_hashes = collect(
        'stage54_marginal_comparison_seed{seed}_n{n}.csv',
        'stage54_marginal_comparison_audit_seed{seed}_n{n}.json', n)
    dependency, hashes = collect(
        'stage54_dependency_comparison_seed{seed}_n{n}.csv',
        'stage54_dependency_audit_seed{seed}_n{n}.json', n)
    input_hashes += hashes
    learning_frames = []
    for seed in SEEDS:
        summary = REPORTS / f'stage543_learning_summary_seed{seed}_n{n}.csv'
        manifest = REPORTS / f'stage543_learning_manifest_seed{seed}_n{n}.json'
        if not summary.is_file() or not manifest.is_file():
            raise FileNotFoundError(f'Missing H3 summary/manifest: {summary.name} or {manifest.name}')
        m = json.loads(manifest.read_text())
        if m.get('seed') != seed or m.get('n_per_level') != n:
            raise ValueError(f'Manifest seed/sample mismatch: {manifest.name}')
        if m.get('sha256_outputs', {}).get(summary.name) != sha256(summary):
            raise ValueError(f'H3 summary hash mismatch: {summary.name}')
        df = pd.read_csv(summary)
        if set(df['seed']) != {seed} or set(df['cumulative_equivalent_units']) != {1, 2, 4, 8, 16}:
            raise ValueError(f'H3 missing levels or seed mismatch: {summary.name}')
        learning_frames.append(df)
        input_hashes.extend([{'file': summary.name, 'sha256': sha256(summary)},
                             {'file': manifest.name, 'sha256': sha256(manifest)}])
    learning = pd.concat(learning_frames, ignore_index=True)

    contexts = set(marginal.context_id)
    if len(contexts) != 12 or set(dependency.context_id) != contexts:
        raise ValueError('Expected identical coverage of 12 structural contexts')
    for seed in SEEDS:
        if len(marginal[marginal.seed == seed]) != 12:
            raise ValueError('Expected one marginal row per context per seed')
        dg = dependency[dependency.seed == seed]
        if len(dg) != 24 or set(dg['mode']) != {'aligned_burden_stress', 'offsetting_burden_stress'}:
            raise ValueError('Expected two modes x 12 dependency contexts per seed')
    if len(learning) != 20:
        raise ValueError('Expected five learning levels per seed')

    outputs = []
    def describe(df, method, group_keys, metrics):
        for keys, sub in df.groupby(group_keys, sort=True):
            if not isinstance(keys, tuple): keys = (keys,)
            if len(sub) != 4 or set(sub.seed) != set(SEEDS):
                raise ValueError(f'Incomplete seed coverage {method}: {keys}')
            row = {'experiment': method, **dict(zip(group_keys, keys)), 'sample_size_per_seed': n}
            for metric in metrics:
                values = sub[metric].astype(float)
                if not np.isfinite(values).all(): raise ValueError(f'Nonfinite {metric}: {keys}')
                row[f'{metric}_seed_mean'] = float(values.mean())
                row[f'{metric}_seed_min'] = float(values.min())
                row[f'{metric}_seed_max'] = float(values.max())
            outputs.append(row)
    describe(marginal, 'triangular_vs_uniform', ['context_id'],
             ['break_even_delta_p50', 'NPV_delta_p50', 'positive_fraction_delta'])
    describe(dependency, 'dependence_vs_independent', ['mode', 'context_id'],
             ['break_even_delta_p50', 'NPV_delta_p50', 'positive_fraction_delta'])
    describe(learning, 'H3_manufacturing_learning', ['cumulative_equivalent_units'],
             ['mean_capex_reduction_fraction', 'break_even_p50', 'npv_p50_eur', 'positive_fraction'])
    out = pd.DataFrame(outputs)
    REPORTS.mkdir(exist_ok=True)
    path = REPORTS / 'stage55_cross_seed_summary.csv'
    out.to_csv(path, index=False)
    audit = {
        'status': 'COMPLETE_EXPLORATORY_CROSS_SEED_SUMMARY_NOT_CONVERGENCE_CERTIFIED',
        'n_per_seed': n, 'seeds': SEEDS, 'contexts': len(contexts),
        'marginal_rows': len(marginal), 'dependency_rows': len(dependency), 'learning_rows': len(learning),
        'input_hashes': input_hashes, 'output_sha256': sha256(path),
        'limits': ['four-seed summary does not certify convergence',
                   'distribution and dependence assumptions are exploratory',
                   'H3 learning analysis uses one structural context',
                   'historical Stage 5.3 strict status remains NONCONVERGED',
                   'seed means are descriptive, not real-world probabilities']
    }
    auditpath = REPORTS / 'stage55_integration_audit.json'
    auditpath.write_text(json.dumps(audit, indent=2) + '\n')
    text = [
        '# Stage 5.5 — Preliminary Cross-Seed Integration', '',
        f'**Status:** {audit["status"]}', '',
        f'Four seeds; {n:,} draws per seed; 12 structural contexts for marginal and dependency tests.', '',
        'This file summarizes validated experiment comparison outputs. It is not convergence certification.', '',
        '## Reference-context marginal comparison', ''
    ]
    ref = out[(out.experiment=='triangular_vs_uniform') & (out.context_id=='GEN002_LC004_R05')].iloc[0]
    text += [f'- NPV P50 delta (mean across seeds): EUR {ref.NPV_delta_p50_seed_mean/1e9:+.3f} billion',
             f'- Break-even P50 delta: {ref.break_even_delta_p50_seed_mean:+.3f} EUR/MWh',
             f'- Positive-fraction delta: {ref.positive_fraction_delta_seed_mean:+.3%}', '',
             '## Reference-context dependence stresses', '']
    for mode in ['aligned_burden_stress','offsetting_burden_stress']:
        row = out[(out.experiment=='dependence_vs_independent') & (out.context_id=='GEN002_LC004_R05') & (out['mode']==mode)].iloc[0]
        text.append(f'- **{mode}:** NPV P50 delta EUR {row.NPV_delta_p50_seed_mean/1e9:+.3f} bn; '
                    f'break-even P50 delta {row.break_even_delta_p50_seed_mean:+.3f} EUR/MWh; '
                    f'positive fraction delta {row.positive_fraction_delta_seed_mean:+.3%}')
    text += ['', '## H3 learning illustration (same structural context)', '']
    h3 = out[(out.experiment=='H3_manufacturing_learning') & (out.cumulative_equivalent_units==16)].iloc[0]
    text += [f'- Mean CAPEX reduction at 16 units: {h3.mean_capex_reduction_fraction_seed_mean:.2%}',
             f'- Median break-even price, seed mean: {h3.break_even_p50_seed_mean:.2f} EUR/MWh',
             f'- Median NPV, seed mean: EUR {h3.npv_p50_eur_seed_mean/1e9:.3f} billion',
             '', '## Research interpretation constraints', '',
             '- These outcomes depend on exploratory distribution specifications and structural assumptions.',
             '- The strict Stage 5.3 two-refinement convergence requirement remains unmet.',
             '- The H3 study does not include manufacturing-facility investments or prove repeat-unit cost feasibility.',
             '- Do not average structural contexts as if they had empirically estimated probabilities.',
             '- Consult the CSV for all contexts and across-seed minimum/maximum variation.', '']
    mdpath = REPORTS / 'stage55_integration_summary.md'
    mdpath.write_text('\n'.join(text))
    print('Stage 5.5 integration: exploratory cross-seed coverage COMPLETE')
    print('Wrote:',path.name,auditpath.name,mdpath.name)
    print('\n'.join(text[8:23]))

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--n', type=int, default=8192)
    main(p.parse_args().n)
