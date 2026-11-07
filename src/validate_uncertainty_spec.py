"""Validate the Stage 5 design and deterministic corners. No random sampling."""
import copy
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys

from economic_validation import finite_number, positive_integer
from engineering_generation import calculate_generation_case
from lifecycle_cash_flow import calculate_lifecycle, normalize_config
from stage34_provenance import write_json

ROOT = Path(__file__).resolve().parents[1]
REVIEWED_INPUTS = ('data/economic_assumptions.csv','data/economic_reference_notes.csv',
                   'data/economic_model_basis.json','data/lcoe_scenarios_stage42.csv',
                   'data/engineering_generation_cases.csv','data/lifecycle_cash_flow_cases.json')
PILOT_IDS = ['CAPEX','FOM','VOM','RATE','PRICE']
ROLES = {'CAPEX':'pilot_sample','FOM':'pilot_sample','VOM':'pilot_sample','RATE':'pilot_sample',
         'PRICE':'pilot_sample','LIFE':'fixed_pilot','POWER':'derived_engineering',
         'CF':'derived_engineering','SHARE':'learning_extension','LEARNING':'learning_extension'}


def read_rows(root, name, key):
    with (root/name).open(newline='',encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    result = {r[key]:r for r in rows}
    if len(result)!=len(rows) or '' in result:
        raise ValueError('Duplicate/blank IDs: '+name)
    return result


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(root=ROOT):
    root=Path(root)
    spec=json.loads((root/'data/stage5_uncertainty_spec.json').read_text())
    require(spec['schema_version']==1 and spec['design_status']=='specified_not_simulated', 'Unsupported specification/status')
    require(spec['probability_interpretation']=='conditional_on_exploratory_design_not_real_world_success_probability', 'Exploratory probability interpretation required')
    saved=spec['reviewed_input_hashes']
    require(set(saved)==set(REVIEWED_INPUTS),'Reviewed source file set differs')
    for name in REVIEWED_INPUTS:
        require(saved[name]==hashlib.sha256((root/name).read_bytes()).hexdigest(), 'Reviewed source changed: '+name)
    basis=spec['model_basis']
    require(basis=={'currency':'EUR','price_year':2024,'discount_basis':'real_pre_tax_unlevered_no_extra_IDC',
                   'reference_case':'CAL002','capex_mapping':'intensity_times_fixed_reference_1000_MWe_divided_by_1000_to_EUR_million',
                   'capex_context_rule':'same_total_CAPEX_across_auxiliary_contexts_not_scaled_with_derived_net_power',
                   'opex_boundary':'routine_excludes_major_replacements','years_after_COD':35}, 'Unsupported money/timing/power boundary')
    assumptions=read_rows(root,'data/economic_assumptions.csv','parameter_id')
    params={p['parameter_id']:p for p in spec['parameters']}
    require(len(params)==len(spec['parameters']) and set(params)==set(ROLES),'Missing/duplicate uncertainty parameters')
    for key,p in params.items():
        original=assumptions[key]
        require(p['role']==ROLES[key],'Unsupported sampling role: '+key)
        require(p['model_field']==original['model_field'] and p['unit']==original['unit'], 'Field/unit mismatch: '+key)
        require(p['evidence_class']=='analyst_assumption' and p['range_class']==original['range_role'], 'Evidence/range class mismatch: '+key)
        for a,b in [('lower','lower'),('reference','reference_value'),('upper','upper')]:
            require(finite_number(p[a],key)==float(original[b]), 'Reviewed range/reference differs: '+key)
        require(p['lower']<=p['reference']<=p['upper'],'Invalid range order: '+key)
        require(p['distribution']==('exploratory_uniform' if p['role'] in {'pilot_sample','learning_extension'} else 'not_sampled'), 'Unsupported distribution: '+key)
        require(bool(p['rationale'].strip()) and bool(p['next_evidence'].strip()), 'Missing range rationale/evidence gap: '+key)
    pilot=spec['pilot']
    require(pilot['sampled_ids']==PILOT_IDS and pilot['fixed_ids']==['LIFE'] and pilot['derived_ids']==['POWER','CF'], 'Derived generation/lifetime must not be independently sampled')
    require(pilot['engineering_case_ids']==['GEN002','GEN003','GEN007'] and pilot['construction_case_ids']==['LC004','LC006'],'Unreviewed context set')
    require(pilot['replacement_fractions_of_sampled_initial_CAPEX']==[0.05,0.10], 'Unreviewed replacement-cost context')
    require(pilot['context_weights'] is None and pilot['context_interpretation']=='separate_structural_stress_cases_no_mixture_probabilities','Do not assign context mixture probabilities')
    require(set(pilot['excluded_engineering_cases'])=={'GEN001','GEN004','GEN005','GEN006'} and all(pilot['excluded_engineering_cases'].values()),'Diagnostic/stretch exclusions must remain explicit')
    deps=spec['dependencies']
    require(deps['rejection_policy']=='fail_and_report_invalid_configuration_never_silently_resample_or_clip','Silent clipping/resampling prohibited')
    require(deps['feasibility_scope']=='mathematical_and_boundary_consistency_not_demonstrated_engineering_feasibility','Feasibility interpretation changed')
    require(len(deps['derived_rules'])==6 and all(deps['derived_rules']),'Missing derivation rules')
    modes=deps['modes']
    require([m['id'] for m in modes]==['independent_diagnostic','aligned_burden_stress','offsetting_burden_stress'], 'Missing dependence sensitivity')
    require(modes[0]['rule']=='independent_uniform_ranks','Unsupported independence mode')
    for mode in modes[1:]:
        require(mode['rule']=='common_rank' and set(mode['signs'])==set(PILOT_IDS),'Incomplete dependence mapping')
        require(all(type(s) is int and s in (-1,1) for s in mode['signs'].values()),'Rank signs must be +/-1')
    require(modes[1]['signs']=={'CAPEX':1,'FOM':1,'VOM':1,'RATE':1,'PRICE':-1},'Aligned burden mapping changed')
    require(modes[2]['signs']=={'CAPEX':1,'FOM':-1,'VOM':-1,'RATE':-1,'PRICE':1},'Offsetting burden mapping changed')
    learning=spec['learning_extension']
    require(learning['status']=='specified_not_simulated' and learning['sampled_ids']==['SHARE','LEARNING'],'Learning must remain a separate specified extension')
    require(learning['cumulative_units']==[1,2,4,8,16] and learning['context_engineering_case']=='GEN002' and learning['construction_case']=='LC004' and learning['replacement_fraction']==0.05,'Unreviewed learning family')
    require(learning['capex_factor']=='1-share+share*N**log2(1-learning_rate)' and learning['replacement_rule']=='fraction_of_unlearned_sampled_initial_CAPEX_no_automatic_learning_on_replacements','Learning cost double counting/boundary mismatch')
    require(learning['cost_boundary']=='magnet_only_initial_CAPEX_learning_nonmagnet_costs_constant_industrial_investment_omitted','Industrial investment limitation missing')
    sampling=spec['sampling_plan']
    seeds=sampling['master_seeds'];sizes=sampling['sample_sizes']
    require(len(seeds)>=4 and len(set(seeds))==len(seeds),'At least four distinct seeds required')
    for seed in seeds: positive_integer(seed,'seed')
    for n in sizes: positive_integer(n,'sample size')
    require(len(sizes)>=3 and sizes==sorted(set(sizes)), 'At least three increasing sample sizes required')
    require(positive_integer(sampling['extension_size_if_needed'],'extension size')>max(sizes),'Extension must increase sample size')
    require(sampling['generator']=='numpy.random.Generator_PCG64' and sampling['common_random_numbers_across_contexts'] is True,'Generator/common-random-number design missing')
    require(sampling['design']=='independent_replicates_with_nested_prefixes_within_each_seed','Unsupported replication design')
    require(sampling['quantile_convention']=='linear_interpolation_at_(n-1)*p' and sampling['alternative_marginal']=='triangular_same_bounds_mode_at_reference_exploratory_density_sensitivity','Density/quantile sensitivity missing')
    require(sampling['invalid_draw_policy']=='halt_report_input_and_context_no_replacement_draws','Invalid draws must halt')
    require(set(sampling['archive'])=={'design_hash','input_and_script_hashes','python_and_package_versions','seed','generator','context','dependency_mode','sample_size','invalid_count','output_hashes'}, 'Incomplete future reproducibility record')
    acceptance=spec['acceptance']
    require(acceptance['quantiles']==[0.05,0.5,0.95] and acceptance['consecutive_refinements_required']==2,'Two consecutive convergence refinements required')
    require(acceptance['metrics']==['lifecycle_break_even_price','project_NPV','conditional_sample_fraction_NPV_above_zero'],'Missing uncertainty metrics')
    for key in ('break_even_quantile_abs_tolerance_eur_per_mwh','break_even_quantile_relative_tolerance','npv_quantile_abs_tolerance_eur','npv_quantile_relative_tolerance','fraction_MC_half_width_max'):
        finite_number(acceptance[key],key,minimum=0,minimum_inclusive=False)
    require(acceptance['fraction_MC_half_width_max']<=0.01,'MC fraction precision weakened without design review')
    require(acceptance['fraction_MC_interval_method']=='Wilson_95_percent_under_chosen_iid_design' and acceptance['interpretation']=='Monte_Carlo_error_is_not_epistemic_confidence_or_empirical_probability','MC error must not become empirical confidence')
    require(all(acceptance[k].strip() for k in ('rule','sensitivity')),'Convergence/failure and sensitivity plans required')
    require(spec['gates']=={'empirical_calibration':'open','human_editorial_and_source_review':'required','H1_H2_H3':'open','main_stage5_simulation':'not_implemented','main_stage6_strategy':'planned','main_stage7_final_deliverables':'planned'},'Specification cannot certify simulation, calibration or hypotheses')
    engineering=read_rows(root,'data/engineering_generation_cases.csv','scenario_id')
    configs=json.loads((root/'data/lifecycle_cash_flow_cases.json').read_text())['cases']
    configs={c['scenario_id']:normalize_config(c) for c in configs}
    for name in pilot['engineering_case_ids']:
        metrics=calculate_generation_case(engineering[name])
        require(0<metrics['derived_capacity_factor']<=1 and metrics['net_rated_mwe']>0,'Invalid engineering generation')
    for name in pilot['construction_case_ids']:
        require(configs[name]['generation_mode']=='engineering_events' and configs[name]['opex_boundary']==basis['opex_boundary'],'Incompatible lifecycle context')
    reference=read_rows(root,'data/lcoe_scenarios_stage42.csv','scenario_id')['CAL002']
    require(float(reference['net_power_mwe'])==1000 and float(reference['plant_lifetime_years'])==35,'Reference power/lifetime mapping changed')
    return spec,params,engineering,configs,reference


def dry_run(root=ROOT):
    """396 deterministic center/corner evaluations; no RNG or inferred frequency."""
    spec,params,engineering,configs,reference=validate(root)
    pilot=spec['pilot']; rows=[]
    corners=list(itertools.product((0,1),repeat=len(PILOT_IDS)))
    points=[('reference',{k:params[k]['reference'] for k in PILOT_IDS})]
    points += [('corner_'+''.join(map(str,choice)), {k:params[k]['upper' if bit else 'lower'] for k,bit in zip(PILOT_IDS,choice)}) for choice in corners]
    for eng_id,config_id,fraction in itertools.product(pilot['engineering_case_ids'],pilot['construction_case_ids'],pilot['replacement_fractions_of_sampled_initial_CAPEX']):
        eng=engineering[eng_id];generation=calculate_generation_case(eng)
        for point,values in points:
            case=copy.deepcopy(reference)
            # Intensity support is mapped at the fixed 1000-MWe reference. Total
            # CAPEX stays equal across auxiliary contexts; no scaling is inferred.
            capex=values['CAPEX']*float(reference['net_power_mwe'])/1000
            case.update(capex_eur_million=capex,net_power_mwe=generation['net_rated_mwe'],
                        capacity_factor=generation['derived_capacity_factor'],
                        fixed_opex_eur_million_per_year=values['FOM'],variable_opex_eur_per_mwh=values['VOM'],real_discount_rate=values['RATE'])
            config=copy.deepcopy(configs[config_id]);config['engineering_case_id']=eng_id
            config['replacement_cost_eur_million']=fraction*capex
            _,_,result=calculate_lifecycle(case,values['PRICE'],config,eng)
            require(all(math.isfinite(float(result[k])) for k in ('npv_eur','break_even_eur_2024_per_mwh','total_generation_mwh')),'Nonfinite deterministic model result')
            require(result['total_generation_mwh']>0 and 0<result['finite_life_capacity_factor']<=1,'Nonpositive generation or impossible CF')
            rows.append({'engineering_case_id':eng_id,'construction_case_id':config_id,'replacement_fraction':fraction,
                         'point':point,'run_class':'deterministic_design_check_not_Monte_Carlo',
                         **{k:values[k] for k in PILOT_IDS},'capex_eur_million':capex,
                         'replacement_cost_eur_million':fraction*capex,
                         'net_rated_mwe':result['net_rated_mwe'],'finite_life_capacity_factor':result['finite_life_capacity_factor'],
                         'npv_eur':result['npv_eur'],'break_even_eur_2024_per_mwh':result['break_even_eur_2024_per_mwh']})
    return {'status':'SPECIFICATION_CHECKS_CLEAR_WITH_RESEARCH_GAPS','simulation_executed':False,
            'contexts':12,'deterministic_evaluations':len(rows),'errors':[],
            'limitations':['No random samples or probability estimates produced.',
                           'Uniform/triangular densities and dependence modes are exploratory designs, not empirically calibrated probabilities.',
                           'Corner checks establish numerical/boundary admissibility at evaluated points, not technical feasibility or all interior interactions.',
                           'Human source/editorial review and empirical economic calibration remain required.']},rows


def main():
    try:
        audit,rows=dry_run()
    except (OSError,ValueError,KeyError,TypeError,AttributeError) as exc:
        audit={'status':'FAIL','simulation_executed':False,'errors':[str(exc)]};rows=[]
    reports=ROOT/'reports';reports.mkdir(exist_ok=True)
    write_json(reports/'stage5_spec_audit.json',audit)
    if rows:
        with (reports/'stage5_design_dry_run.csv').open('w',newline='',encoding='utf-8') as handle:
            writer=csv.DictWriter(handle,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    lines=['# Stage 5 Uncertainty Specification Preflight','', 'Status: '+audit['status'],'',
           'Simulation executed: **no**. Deterministic checks are not a probability distribution.','',
           f"Contexts: {audit.get('contexts',0)}; deterministic reference/corner evaluations: {audit.get('deterministic_evaluations',0)}.",'']
    lines += ['- '+e for e in audit.get('errors',[])]+['- '+e for e in audit.get('limitations',[])]
    lines += ['', 'Design: `data/stage5_uncertainty_spec.json`; explanation: `research/32_stage5_uncertainty_specification.md`.']
    (reports/'stage5_spec_audit.md').write_text('\n'.join(lines)+'\n')
    print('Stage 5 specification: '+audit['status'])
    print(f"Deterministic evaluations: {len(rows)}; Monte Carlo executed: no")
    for error in audit['errors']:print('REVIEW: '+error)
    return int(bool(audit['errors']))


if __name__=='__main__':
    sys.exit(main())
