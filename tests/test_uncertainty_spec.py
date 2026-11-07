"""Uncertainty design contracts; no stochastic simulation is executed."""
import csv
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

PROJECT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PROJECT/'src'))
from validate_uncertainty_spec import REVIEWED_INPUTS,validate,dry_run


class UncertaintySpecTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        for name in (*REVIEWED_INPUTS,'data/stage5_uncertainty_spec.json'):
            p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(PROJECT/name,p)

    def edit(self,fn):
        p=self.root/'data/stage5_uncertainty_spec.json';spec=json.loads(p.read_text());fn(spec);p.write_text(json.dumps(spec))

    def rejected(self,fn,message):
        self.edit(fn)
        with self.assertRaisesRegex(ValueError,message):validate(self.root)

    def test_current_spec(self):
        spec,*_=validate(self.root)
        self.assertEqual(spec['design_status'],'specified_not_simulated')

    def test_stale_source_rejected_without_repinning(self):
        p=self.root/'data/engineering_generation_cases.csv';p.write_text(p.read_text()+'\n')
        source=self.root/'data/stage5_uncertainty_spec.json';before=source.read_bytes()
        with self.assertRaisesRegex(ValueError,'Reviewed source changed'):validate(self.root)
        self.assertEqual(source.read_bytes(),before)

    def test_removed_source_hash_rejected(self):
        self.rejected(lambda s:s['reviewed_input_hashes'].pop(REVIEWED_INPUTS[0]),'file set')

    def test_range_cannot_silently_expand(self):
        self.rejected(lambda s:s['parameters'][0].update(upper=25000),'range/reference')

    def test_nonfinite_range_rejected(self):
        self.rejected(lambda s:s['parameters'][0].update(lower=float('nan')),'finite')

    def test_boolean_range_rejected(self):
        self.rejected(lambda s:s['parameters'][0].update(reference=True),'boolean|numeric|number')

    def test_duplicate_parameter_rejected(self):
        self.rejected(lambda s:s['parameters'].append(s['parameters'][0]),'duplicate')

    def test_empirical_distribution_claim_rejected(self):
        self.rejected(lambda s:s['parameters'][0].update(evidence_class='empirically_calibrated'),'Evidence')

    def test_normal_distribution_without_bounds_not_accepted(self):
        self.rejected(lambda s:s['parameters'][0].update(distribution='normal'),'distribution')

    def test_CF_cannot_be_independently_sampled(self):
        self.rejected(lambda s:s['pilot']['sampled_ids'].append('CF'),'independently sampled')

    def test_context_probabilities_rejected(self):
        self.rejected(lambda s:s['pilot'].update(context_weights=[1/12]*12),'mixture probabilities')

    def test_stretch_case_cannot_enter_pilot(self):
        self.rejected(lambda s:s['pilot']['engineering_case_ids'].append('GEN006'),'context set')

    def test_nominal_levered_boundary_rejected(self):
        self.rejected(lambda s:s['model_basis'].update(discount_basis='nominal_levered'),'boundary')

    def test_extra_IDC_not_silently_included(self):
        self.rejected(lambda s:s['model_basis'].update(extra_IDC=True),'boundary')

    def test_silent_resampling_rejected(self):
        self.rejected(lambda s:s['dependencies'].update(rejection_policy='resample'),'clipping/resampling')

    def test_missing_dependence_mapping_rejected(self):
        self.rejected(lambda s:s['dependencies']['modes'][1]['signs'].pop('PRICE'),'mapping')

    def test_double_learning_on_replacement_rejected(self):
        self.rejected(lambda s:s['learning_extension'].update(replacement_rule='apply_magnet_learning_again'),'double counting')

    def test_duplicate_seeds_rejected(self):
        self.rejected(lambda s:s['sampling_plan'].update(master_seeds=[1,1,2,3]),'distinct seeds')

    def test_unordered_convergence_sizes_rejected(self):
        self.rejected(lambda s:s['sampling_plan'].update(sample_sizes=[8192,2048,32768]),'increasing')

    def test_single_refinement_not_accepted(self):
        self.rejected(lambda s:s['acceptance'].update(consecutive_refinements_required=1),'Two consecutive')

    def test_probability_truth_claim_rejected(self):
        self.rejected(lambda s:s.update(probability_interpretation='real_success_probability'),'interpretation')

    def test_simulation_cannot_be_marked_implemented(self):
        self.rejected(lambda s:s['gates'].update(main_stage5_simulation='complete'),'cannot certify')

    def test_dry_run_covers_corners_and_preserves_legacy_extension_reference(self):
        result,rows=dry_run(self.root)
        self.assertEqual(len(rows),396)
        self.assertFalse(result['simulation_executed'])
        contexts={(r['engineering_case_id'],r['construction_case_id'],r['replacement_fraction']) for r in rows}
        self.assertEqual(len(contexts),12)
        for context in contexts:
            self.assertEqual(sum((r['engineering_case_id'],r['construction_case_id'],r['replacement_fraction'])==context for r in rows),33)
        ref=next(r for r in rows if r['engineering_case_id']=='GEN002' and r['construction_case_id']=='LC004' and r['replacement_fraction']==0.05 and r['point']=='reference')
        with (PROJECT/'reports/lifecycle_summary.csv').open() as f:
            old=next(r for r in csv.DictReader(f) if r['scenario_id']=='LC004')
        self.assertAlmostEqual(ref['break_even_eur_2024_per_mwh'],float(old['break_even_eur_2024_per_mwh']),places=9)
        self.assertAlmostEqual(ref['npv_eur'],float(old['npv_eur'])-30*float(old['pv_generation_mwh']),places=4)
        aux=next(r for r in rows if r['engineering_case_id']=='GEN007' and r['construction_case_id']=='LC004' and r['replacement_fraction']==0.05 and r['point']=='reference')
        self.assertEqual(aux['net_rated_mwe'],875)
        self.assertEqual(aux['capex_eur_million'],ref['capex_eur_million'])
        self.assertTrue(all(0<r['finite_life_capacity_factor']<=1 for r in rows))
        self.assertTrue(all(r['replacement_cost_eur_million']==r['capex_eur_million']*r['replacement_fraction'] for r in rows))


if __name__=='__main__':unittest.main(verbosity=2)
