"""Verify that a 131072-draw Stage 5.2 file preserves the existing 32768-draw prefix.

Run: python src/check_stage53_nested_extension.py --seed 20261105
Note: the analysis script independently verifies SHA256 input, script, output provenance.
"""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ['seed', 'draw_id', 'context_id', 'capex_eur_per_kwe',
          'fixed_opex_eur_million_per_year', 'variable_opex_eur_per_mwh',
          'real_discount_rate', 'electricity_price_eur_per_mwh',
          'break_even_eur_2024_per_mwh', 'npv_eur_2024', 'npv_positive']


def check(seed, reports):
    old_path = reports / f'stage52_draws_seed{seed}_n32768.csv'
    new_path = reports / f'stage52_draws_seed{seed}_n131072.csv'
    if not old_path.exists() or not new_path.exists():
        raise FileNotFoundError(f'Expected files: {old_path.name}, {new_path.name}')
    prior = pd.read_csv(old_path, usecols=FIELDS)
    prefix_parts = []
    total = 0
    for chunk in pd.read_csv(new_path, usecols=FIELDS, chunksize=100_000):
        total += len(chunk)
        prefix_parts.append(chunk.loc[chunk['draw_id'] < 32768])
    prefix = pd.concat(prefix_parts, ignore_index=True)
    expected_old, expected_prefix = 32768 * 12, 32768 * 12
    if len(prior) != expected_old or len(prefix) != expected_prefix or total != 131072 * 12:
        raise AssertionError(f'Invalid row counts: old={len(prior)} prefix={len(prefix)} extension={total}')
    keys = ['context_id', 'draw_id']
    for frame in (prior, prefix):
        if frame.duplicated(keys).any():
            raise AssertionError('Duplicate context/draw key')
    a = prior.sort_values(keys).reset_index(drop=True)
    b = prefix.sort_values(keys).reset_index(drop=True)
    if not a[keys].equals(b[keys]):
        raise AssertionError('Context/draw IDs do not match')
    if not (a['seed'].eq(seed).all() and b['seed'].eq(seed).all()):
        raise AssertionError('Seed mismatch')
    numeric = [c for c in FIELDS if c not in keys and c != 'seed']
    for c in numeric:
        if not np.allclose(a[c].to_numpy(), b[c].to_numpy(), rtol=1e-12, atol=1e-8, equal_nan=False):
            maximum = float(np.max(np.abs(a[c].to_numpy() - b[c].to_numpy())))
            raise AssertionError(f'Nested prefix mismatch in {c}; max absolute deviation={maximum}')
    print(f'PASS: seed={seed}, existing 32768-draw results match the extension prefix in all 12 contexts')
    print('This verifies nested numeric outputs, not scientific calibration or convergence.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed', type=int, required=True)
    parser.add_argument('--reports-dir', type=Path, default=ROOT / 'reports')
    args = parser.parse_args()
    check(args.seed, args.reports_dir)
