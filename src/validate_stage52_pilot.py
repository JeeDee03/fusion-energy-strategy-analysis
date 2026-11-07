"""Validate Stage 5.2 pilot outputs; place in repository src/.

Usage: python src/validate_stage52_pilot.py --n 128 --seed 20261105
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(n, seed, outdir):
    outdir = Path(outdir) if outdir else ROOT / 'reports'
    suffix = f'seed{seed}_n{n}'
    data_file = outdir / f'stage52_draws_{suffix}.csv'
    summary_file = outdir / f'stage52_summary_{suffix}.csv'
    manifest_file = outdir / f'stage52_manifest_{suffix}.json'
    df = pd.read_csv(data_file)
    summary = pd.read_csv(summary_file)
    manifest = json.loads(manifest_file.read_text())
    spec = json.loads((ROOT / 'data/stage5_uncertainty_spec.json').read_text())

    assert manifest['status'] == 'PILOT_NOT_CONVERGENCE_CERTIFIED'
    assert manifest['seed'] == seed and manifest['sample_size_per_context'] == n
    assert manifest['total_evaluations'] == 12 * n and manifest['invalid_count'] == 0
    assert len(df) == n * 12
    assert len(summary) == 12
    assert df['context_id'].nunique() == 12
    assert not df.duplicated(['context_id', 'seed', 'draw_id']).any()
    assert df['dependency_mode'].eq('independent_diagnostic').all()
    assert df['marginal_design'].eq('exploratory_uniform').all()
    assert df.groupby('context_id').size().eq(n).all()
    assert df.groupby('context_id')['draw_id'].nunique().eq(n).all()
    assert np.isfinite(df.select_dtypes(include='number').to_numpy()).all()
    assert (df['break_even_eur_2024_per_mwh'] > 0).all()
    assert df['finite_life_capacity_factor'].between(0,1,inclusive='right').all()
    assert df['net_rated_mwe'].gt(0).all()
    assert (df['npv_positive'] == (df['npv_eur_2024'] > 0).astype(int)).all()

    param_specs = {p['parameter_id']:p for p in spec['parameters']}
    columns = {
        'CAPEX':'capex_eur_per_kwe',
        'FOM':'fixed_opex_eur_million_per_year',
        'VOM':'variable_opex_eur_per_mwh',
        'RATE':'real_discount_rate',
        'PRICE':'electricity_price_eur_per_mwh',
    }
    # Common random numbers: each draw has the same five sampled inputs in all 12 contexts.
    for param_id,col in columns.items():
        p = param_specs[param_id]
        assert df[col].between(p['lower'],p['upper']).all(), col
        assert df.groupby('draw_id')[col].nunique().eq(1).all(), col

    # Reconcile NPV sign with sale price relative to lifecycle break-even price.
    price_minus_break_even = df['electricity_price_eur_per_mwh'] - df['break_even_eur_2024_per_mwh']
    assert ((df['npv_eur_2024'] > 0) == (price_minus_break_even > 0)).all()
    assert manifest['sha256_outputs'][data_file.name] == digest(data_file)
    assert manifest['sha256_outputs'][summary_file.name] == digest(summary_file)
    for rel,expected_hash in manifest['sha256_inputs'].items():
        assert digest(ROOT/rel) == expected_hash, f'Input changed: {rel}'
    for rel,expected_hash in manifest['sha256_scripts'].items():
        assert digest(ROOT/'src'/rel) == expected_hash, f'Script changed: {rel}'

    for _,row in summary.iterrows():
        g = df.loc[df['context_id'].eq(row['context_id'])]
        assert len(g) == n
        for label,q in [('p05', .05),('p50', .5),('p95', .95)]:
            assert np.isclose(row[f'lifecycle_break_even_{label}'],g['break_even_eur_2024_per_mwh'].quantile(q))
            assert np.isclose(row[f'npv_{label}_eur'],g['npv_eur_2024'].quantile(q))
        assert np.isclose(row['conditional_fraction_npv_positive'],g['npv_positive'].mean())

    print(f'PASS — {len(df)} draws across 12 structural contexts; seed={seed}, n={n}')
    print('PASS — Sampling bounds, common random numbers, NPV identities, quantiles, provenance hashes')
    print('WARNING — No convergence certification or empirical success probability')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--n', type=int, default=128)
    parser.add_argument('--seed', type=int, default=20261105)
    parser.add_argument('--outdir', type=Path, default=None)
    args = parser.parse_args()
    main(args.n,args.seed,args.outdir)
