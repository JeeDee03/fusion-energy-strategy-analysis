# Stage 7.2.3 — Results Evidence Inventory

Generated from local research artifacts.
This is a file inventory, not scientific validation.

## engineering_generation_scenarios.csv
- SHA256: `4bed94ae8d59c19d7b10b899e422a98cb13c58010f031d527262c7461718c040`
- Bytes: 4001
- Rows: 7
- Columns: scenario_id, scenario_name, maintenance_basis, interval_years, major_outage_months, other_outage_fraction, operating_load_fraction, gross_electric_mwe, auxiliary_fraction, target_capacity_factor, assumption_class, source_id, notes, operating_window_years, cycle_years, major_outage_availability, online_availability, derived_capacity_factor, net_rated_mwe, annual_net_energy_mwh, target_met, cf_target_gap, evidence_relation, capex_eur_million, effective_capex_eur_per_kwe, lcoe_eur_2024_per_mwh, cost_basis
- Sample: `{"scenario_id": "GEN001", "scenario_name": "Seven-month major-outage upper limit", "maintenance_basis": "full_power_exposure", "interval_years": "4.0", "major_outage_months": "7.0", "other_outage_fraction": "0.0", "operating_load_fraction": "1.0", "gross_electric_mwe": "1250.0", "auxiliary_fraction": "0.2", "target_capacity_factor": "0.85", "assumption_class": "analyst_scenario", "source_id": "S3_006", "notes": "No non-major losses: a mathematical upper limit under conceptual maintenance inputs; not a plant forecast.", "operating_window_years": "4.0", "cycle_years": "4.583333333333333", "major_outage_availability": "0.8727272727272728", "online_availability": "0.8727272727272728", "derived_c`
- Sample: `{"scenario_id": "GEN002", "scenario_name": "Seven-month cycle with other losses", "maintenance_basis": "full_power_exposure", "interval_years": "4.0", "major_outage_months": "7.0", "other_outage_fraction": "0.01", "operating_load_fraction": "0.99", "gross_electric_mwe": "1250.0", "auxiliary_fraction": "0.2", "target_capacity_factor": "0.85", "assumption_class": "analyst_scenario", "source_id": "S3_006", "notes": "Analyst 1% other downtime and 99% online load; 1250 gross MWe and 20% proportional online auxiliary use are constructed assumptions, not published gross power.", "operating_window_years": "4.081216202428323", "cycle_years": "4.664549535761656", "major_outage_availability": "0.874943`

## lifecycle_summary.csv
- SHA256: `e8146904b42a2a2f4217f032554f86dda71e13d7af7c36f26c76fc958b476faa`
- Bytes: 3667
- Rows: 6
- Columns: scenario_id, scenario_name, generation_mode, engineering_case_id, price_scenario_id, construction_years, replacement_cost_eur_million, opex_boundary, assumption_class, notes, spend_shares_json, electricity_price_eur_2024_per_mwh, price_input_class, engineering_evidence_relation, first_revenue_model_year, last_operating_model_year, replacement_count, net_rated_mwe, total_generation_mwh, finite_life_capacity_factor, undiscounted_construction_capex_eur, pv_construction_capex_eur, pv_routine_opex_eur, pv_replacement_cost_eur, pv_generation_mwh, npv_eur, break_even_eur_2024_per_mwh
- Sample: `{"scenario_id": "LC001", "scenario_name": "Legacy special-case reconciliation", "generation_mode": "legacy_constant_cf", "engineering_case_id": "not_applicable", "price_scenario_id": "REV004", "construction_years": "0", "replacement_cost_eur_million": "0.0", "opex_boundary": "legacy_aggregate", "assumption_class": "analyst_scenario", "notes": "Validation control: upfront investment, constant CF and no explicit replacements reproduce the prior simplified DCF.", "spend_shares_json": "[1.0]", "electricity_price_eur_2024_per_mwh": "200.0", "price_input_class": "analyst_scenario", "engineering_evidence_relation": "legacy_constant_CF_diagnostic", "first_revenue_model_year": "1", "last_operating_mo`
- Sample: `{"scenario_id": "LC002", "scenario_name": "Five-year construction, constant-CF diagnostic", "generation_mode": "legacy_constant_cf", "engineering_case_id": "not_applicable", "price_scenario_id": "REV004", "construction_years": "5", "replacement_cost_eur_million": "0.0", "opex_boundary": "legacy_aggregate", "assumption_class": "analyst_scenario", "notes": "Analyst five-year schedule isolates construction spending and receipt timing; no commercial construction-duration evidence is claimed.", "spend_shares_json": "[0.1,0.2,0.3,0.25,0.15]", "electricity_price_eur_2024_per_mwh": "200.0", "price_input_class": "analyst_scenario", "engineering_evidence_relation": "legacy_constant_CF_diagnostic", "fi`

## stage44_learning_results.csv
- SHA256: `485c42f97a8c87ae5128065bb1ca1c4a96885cece6accd148eada0ef05def41e`
- Bytes: 1400
- Rows: 15
- Columns: scenario_id, scenario_name, cumulative_equivalent_units, magnet_capex_share, magnet_learning_rate, magnet_cost_factor, total_capex_eur_million, capex_eur_per_kwe, lcoe_eur_per_mwh
- Sample: `{"scenario_id": "LR000", "scenario_name": "No magnet learning", "cumulative_equivalent_units": "1", "magnet_capex_share": "0.25", "magnet_learning_rate": "0.0", "magnet_cost_factor": "1.0", "total_capex_eur_million": "12000.0", "capex_eur_per_kwe": "12000.0", "lcoe_eur_per_mwh": "170.14090447598144"}`
- Sample: `{"scenario_id": "LR000", "scenario_name": "No magnet learning", "cumulative_equivalent_units": "2", "magnet_capex_share": "0.25", "magnet_learning_rate": "0.0", "magnet_cost_factor": "1.0", "total_capex_eur_million": "12000.0", "capex_eur_per_kwe": "12000.0", "lcoe_eur_per_mwh": "170.14090447598144"}`

## stage45_npv_summary.csv
- SHA256: `76a6e1ffe14984e6a436fe1bbbec07a4fd6acb7260edd8790b03040471c81185`
- Bytes: 912
- Rows: 4
- Columns: scenario_id, scenario_name, pricing_basis, assumption_class, electricity_price_eur_per_mwh, annual_energy_mwh, annual_revenue_eur, annual_operating_cash_flow_eur, lcoe_eur_per_mwh, break_even_price_eur_per_mwh, npv_eur
- Sample: `{"scenario_id": "REV001", "scenario_name": "2024 German day-ahead average", "pricing_basis": "historical_average_stress_test", "assumption_class": "historical_observation", "electricity_price_eur_per_mwh": "78.51", "annual_energy_mwh": "7446000.0", "annual_revenue_eur": "584585460.0", "annual_operating_cash_flow_eur": "347355460.0", "lcoe_eur_per_mwh": "170.14090447598144", "break_even_price_eur_per_mwh": "170.14090447598144", "npv_eur": "-7951722096.14063"}`
- Sample: `{"scenario_id": "REV002", "scenario_name": "Low fixed-price case", "pricing_basis": "hypothetical_fixed_price", "assumption_class": "analyst_scenario", "electricity_price_eur_per_mwh": "120.0", "annual_energy_mwh": "7446000.0", "annual_revenue_eur": "893520000.0", "annual_operating_cash_flow_eur": "656290000.0", "lcoe_eur_per_mwh": "170.14090447598144", "break_even_price_eur_per_mwh": "170.14090447598144", "npv_eur": "-4351223425.3526125"}`

## stage4_integrated_summary.csv
- SHA256: `6bb7e01bae4d784d19ec9879de63e468686a3a5669c1ac02f874698446850806`
- Bytes: 766
- Rows: 10
- Columns: stage, metric, value, unit, classification
- Sample: `{"stage": "4.2", "metric": "Reference CAPEX", "value": "12000.0", "unit": "EUR million", "classification": "analyst_scenario"}`
- Sample: `{"stage": "4.2", "metric": "Reference LCOE", "value": "170.14090447598144", "unit": "EUR/MWh", "classification": "conditional_model_output"}`

## stage52_summary_seed20261105_n128.csv
- SHA256: `5da4bebb02d507db2badc57b71360e7a8f3103e07641d69a8a86b937d6dd65b8`
- Bytes: 2721
- Rows: 12
- Columns: seed, context_id, sample_size, lifecycle_break_even_p05, lifecycle_break_even_p50, lifecycle_break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, conditional_fraction_npv_positive, interpretation
- Sample: `{"seed": "20261105", "context_id": "GEN002_LC004_R05", "sample_size": "128", "lifecycle_break_even_p05": "136.72459073663433", "lifecycle_break_even_p50": "219.64423915504722", "lifecycle_break_even_p95": "388.2907655221354", "npv_p05_eur": "-11326659913.415897", "npv_p50_eur": "-4811152994.180506", "npv_p95_eur": "1700180651.1798623", "conditional_fraction_npv_positive": "0.09375", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`
- Sample: `{"seed": "20261105", "context_id": "GEN002_LC004_R10", "sample_size": "128", "lifecycle_break_even_p05": "149.4797472525918", "lifecycle_break_even_p50": "234.67958995091487", "lifecycle_break_even_p95": "408.55145288997335", "npv_p05_eur": "-12256808528.773859", "npv_p50_eur": "-5730646257.040941", "npv_p95_eur": "150529886.89247358", "conditional_fraction_npv_positive": "0.0625", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`

## stage52_summary_seed20261105_n131072.csv
- SHA256: `29f481b658fc3d0919b66271bf0112a172cf467f1aa07ce95f3d2bcacf883796`
- Bytes: 2870
- Rows: 12
- Columns: seed, context_id, sample_size, lifecycle_break_even_p05, lifecycle_break_even_p50, lifecycle_break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, conditional_fraction_npv_positive, interpretation
- Sample: `{"seed": "20261105", "context_id": "GEN002_LC004_R05", "sample_size": "131072", "lifecycle_break_even_p05": "133.54946595751588", "lifecycle_break_even_p50": "221.5839587343117", "lifecycle_break_even_p95": "366.9956883434185", "npv_p05_eur": "-11120489528.45372", "npv_p50_eur": "-5256051264.439345", "npv_p95_eur": "2190608194.0854964", "conditional_fraction_npv_positive": "0.11031341552734375", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`
- Sample: `{"seed": "20261105", "context_id": "GEN002_LC004_R10", "sample_size": "131072", "lifecycle_break_even_p05": "145.75615695553338", "lifecycle_break_even_p50": "237.80035858520148", "lifecycle_break_even_p95": "386.3697693285715", "npv_p05_eur": "-12376764663.207186", "npv_p50_eur": "-6255711829.87733", "npv_p95_eur": "999459540.1205747", "conditional_fraction_npv_positive": "0.07364654541015625", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`

## stage52_summary_seed20261105_n2048.csv
- SHA256: `eb258cdfb689971f0053ed2c57df0084f81f090792183b06eff7644fcfd53a9a`
- Bytes: 2776
- Rows: 12
- Columns: seed, context_id, sample_size, lifecycle_break_even_p05, lifecycle_break_even_p50, lifecycle_break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, conditional_fraction_npv_positive, interpretation
- Sample: `{"seed": "20261105", "context_id": "GEN002_LC004_R05", "sample_size": "2048", "lifecycle_break_even_p05": "132.65691745720068", "lifecycle_break_even_p50": "217.77035300149902", "lifecycle_break_even_p95": "365.4688315833115", "npv_p05_eur": "-10980700945.152624", "npv_p50_eur": "-5090623226.47911", "npv_p95_eur": "2277212003.1085668", "conditional_fraction_npv_positive": "0.12255859375", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`
- Sample: `{"seed": "20261105", "context_id": "GEN002_LC004_R10", "sample_size": "2048", "lifecycle_break_even_p05": "144.75175606387126", "lifecycle_break_even_p50": "234.60448595015583", "lifecycle_break_even_p95": "384.7930903049549", "npv_p05_eur": "-12301369694.466145", "npv_p50_eur": "-6098779751.968857", "npv_p95_eur": "1033116798.8055512", "conditional_fraction_npv_positive": "0.07763671875", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`

## stage52_summary_seed20261105_n32768.csv
- SHA256: `e5ebd7255eda39ecaebb3a07859362fe9608fa52a0670a512f8cbd7aa867c6ca`
- Bytes: 2844
- Rows: 12
- Columns: seed, context_id, sample_size, lifecycle_break_even_p05, lifecycle_break_even_p50, lifecycle_break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, conditional_fraction_npv_positive, interpretation
- Sample: `{"seed": "20261105", "context_id": "GEN002_LC004_R05", "sample_size": "32768", "lifecycle_break_even_p05": "133.14529089261103", "lifecycle_break_even_p50": "220.58801336594706", "lifecycle_break_even_p95": "366.1125278751123", "npv_p05_eur": "-11086402925.059162", "npv_p50_eur": "-5253263909.956694", "npv_p95_eur": "2216927318.8221807", "conditional_fraction_npv_positive": "0.1104736328125", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`
- Sample: `{"seed": "20261105", "context_id": "GEN002_LC004_R10", "sample_size": "32768", "lifecycle_break_even_p05": "145.52416230967904", "lifecycle_break_even_p50": "236.92972330602305", "lifecycle_break_even_p95": "385.7623950647968", "npv_p05_eur": "-12346838147.574884", "npv_p50_eur": "-6241337035.121938", "npv_p95_eur": "1018457314.012962", "conditional_fraction_npv_positive": "0.073577880859375", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`

## stage52_summary_seed20261105_n8192.csv
- SHA256: `425b07a1db5375f4362028a513c8f98a6e48dcaccfdc72c9bc5d9e3391ee4785`
- Bytes: 2817
- Rows: 12
- Columns: seed, context_id, sample_size, lifecycle_break_even_p05, lifecycle_break_even_p50, lifecycle_break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, conditional_fraction_npv_positive, interpretation
- Sample: `{"seed": "20261105", "context_id": "GEN002_LC004_R05", "sample_size": "8192", "lifecycle_break_even_p05": "132.68561578392362", "lifecycle_break_even_p50": "218.84149676056646", "lifecycle_break_even_p95": "362.7161982567364", "npv_p05_eur": "-11066938158.967888", "npv_p50_eur": "-5173353384.438463", "npv_p95_eur": "2129650614.6595783", "conditional_fraction_npv_positive": "0.1126708984375", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`
- Sample: `{"seed": "20261105", "context_id": "GEN002_LC004_R10", "sample_size": "8192", "lifecycle_break_even_p05": "145.0676145177421", "lifecycle_break_even_p50": "235.3200728609146", "lifecycle_break_even_p95": "382.13431201801683", "npv_p05_eur": "-12355774484.948868", "npv_p50_eur": "-6142399388.00144", "npv_p95_eur": "953001006.3045151", "conditional_fraction_npv_positive": "0.073486328125", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`

## stage52_summary_seed20261106_n131072.csv
- SHA256: `3431bfca3f678da31f7e32ade3e9906656ec76e7ad3b8377556daf23b2d7a018`
- Bytes: 2868
- Rows: 12
- Columns: seed, context_id, sample_size, lifecycle_break_even_p05, lifecycle_break_even_p50, lifecycle_break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, conditional_fraction_npv_positive, interpretation
- Sample: `{"seed": "20261106", "context_id": "GEN002_LC004_R05", "sample_size": "131072", "lifecycle_break_even_p05": "133.83884729936293", "lifecycle_break_even_p50": "221.65055928014823", "lifecycle_break_even_p95": "367.20539960510746", "npv_p05_eur": "-11138274902.488268", "npv_p50_eur": "-5271112637.368307", "npv_p95_eur": "2128493424.998522", "conditional_fraction_npv_positive": "0.11065673828125", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`
- Sample: `{"seed": "20261106", "context_id": "GEN002_LC004_R10", "sample_size": "131072", "lifecycle_break_even_p05": "146.14067121240763", "lifecycle_break_even_p50": "237.9909433508977", "lifecycle_break_even_p95": "386.7484608728805", "npv_p05_eur": "-12381699487.36287", "npv_p50_eur": "-6273764495.8392725", "npv_p95_eur": "939677816.0662597", "conditional_fraction_npv_positive": "0.073638916015625", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`

## stage52_summary_seed20261106_n32768.csv
- SHA256: `a568ad868e0ddc134765483b4e1a73cb347b8e83094fb4d6f8fbed2a1a79cb86`
- Bytes: 2835
- Rows: 12
- Columns: seed, context_id, sample_size, lifecycle_break_even_p05, lifecycle_break_even_p50, lifecycle_break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, conditional_fraction_npv_positive, interpretation
- Sample: `{"seed": "20261106", "context_id": "GEN002_LC004_R05", "sample_size": "32768", "lifecycle_break_even_p05": "134.0613290497489", "lifecycle_break_even_p50": "221.8779079921773", "lifecycle_break_even_p95": "367.7265722611355", "npv_p05_eur": "-11126049439.181406", "npv_p50_eur": "-5283018996.055289", "npv_p95_eur": "2105522748.5098128", "conditional_fraction_npv_positive": "0.109710693359375", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`
- Sample: `{"seed": "20261106", "context_id": "GEN002_LC004_R10", "sample_size": "32768", "lifecycle_break_even_p05": "146.4946022800619", "lifecycle_break_even_p50": "238.07068275050486", "lifecycle_break_even_p95": "387.1032914499805", "npv_p05_eur": "-12367407898.892523", "npv_p50_eur": "-6291379573.057513", "npv_p95_eur": "911395636.5507584", "conditional_fraction_npv_positive": "0.073486328125", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`

## stage52_summary_seed20261106_n8192.csv
- SHA256: `0868d76ada551e2a76c24107df51feacfd4820f54d1bcb09dd1ab3c120a34196`
- Bytes: 2800
- Rows: 12
- Columns: seed, context_id, sample_size, lifecycle_break_even_p05, lifecycle_break_even_p50, lifecycle_break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, conditional_fraction_npv_positive, interpretation
- Sample: `{"seed": "20261106", "context_id": "GEN002_LC004_R05", "sample_size": "8192", "lifecycle_break_even_p05": "133.5872758864629", "lifecycle_break_even_p50": "221.43662120590687", "lifecycle_break_even_p95": "367.5083483800788", "npv_p05_eur": "-11121132074.329699", "npv_p50_eur": "-5225338356.257486", "npv_p95_eur": "2095307899.2290223", "conditional_fraction_npv_positive": "0.1107177734375", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`
- Sample: `{"seed": "20261106", "context_id": "GEN002_LC004_R10", "sample_size": "8192", "lifecycle_break_even_p05": "145.8532351472363", "lifecycle_break_even_p50": "237.21774808498162", "lifecycle_break_even_p95": "386.5476376189836", "npv_p05_eur": "-12313788823.818", "npv_p50_eur": "-6210453916.09767", "npv_p95_eur": "852753791.8037597", "conditional_fraction_npv_positive": "0.07470703125", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`

## stage52_summary_seed20261107_n131072.csv
- SHA256: `74342b1432dcb2309b0d5bd8287cd7f973ce39404eb48321c6a6408bb317f4bb`
- Bytes: 2878
- Rows: 12
- Columns: seed, context_id, sample_size, lifecycle_break_even_p05, lifecycle_break_even_p50, lifecycle_break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, conditional_fraction_npv_positive, interpretation
- Sample: `{"seed": "20261107", "context_id": "GEN002_LC004_R05", "sample_size": "131072", "lifecycle_break_even_p05": "133.8580963188316", "lifecycle_break_even_p50": "221.66964188760906", "lifecycle_break_even_p95": "366.9151746345818", "npv_p05_eur": "-11118310479.011957", "npv_p50_eur": "-5257925739.378733", "npv_p95_eur": "2127237689.7408667", "conditional_fraction_npv_positive": "0.1102142333984375", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`
- Sample: `{"seed": "20261107", "context_id": "GEN002_LC004_R10", "sample_size": "131072", "lifecycle_break_even_p05": "146.1777629223412", "lifecycle_break_even_p50": "237.83578648402218", "lifecycle_break_even_p95": "386.4265706254194", "npv_p05_eur": "-12343392697.802465", "npv_p50_eur": "-6254662498.524147", "npv_p95_eur": "948247245.5999742", "conditional_fraction_npv_positive": "0.073089599609375", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`

## stage52_summary_seed20261107_n32768.csv
- SHA256: `93c0404218c2d1bc7fd655fb2aa2fd27d61aa31d83e3adb144b2fb7ab664f767`
- Bytes: 2839
- Rows: 12
- Columns: seed, context_id, sample_size, lifecycle_break_even_p05, lifecycle_break_even_p50, lifecycle_break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, conditional_fraction_npv_positive, interpretation
- Sample: `{"seed": "20261107", "context_id": "GEN002_LC004_R05", "sample_size": "32768", "lifecycle_break_even_p05": "134.10382529387329", "lifecycle_break_even_p50": "221.44571775936294", "lifecycle_break_even_p95": "366.26028609644175", "npv_p05_eur": "-11108319749.698719", "npv_p50_eur": "-5233328655.291726", "npv_p95_eur": "2142903687.442731", "conditional_fraction_npv_positive": "0.111297607421875", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`
- Sample: `{"seed": "20261107", "context_id": "GEN002_LC004_R10", "sample_size": "32768", "lifecycle_break_even_p05": "146.5277625448594", "lifecycle_break_even_p50": "237.58742803983876", "lifecycle_break_even_p95": "385.86895668135753", "npv_p05_eur": "-12333314753.43122", "npv_p50_eur": "-6215332555.383571", "npv_p95_eur": "936849994.5298753", "conditional_fraction_npv_positive": "0.07305908203125", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`

## stage52_summary_seed20261107_n8192.csv
- SHA256: `347157ef02713d0ce0226f8b07271871b3940fa8e624b83fec2b092c6848d8c0`
- Bytes: 2808
- Rows: 12
- Columns: seed, context_id, sample_size, lifecycle_break_even_p05, lifecycle_break_even_p50, lifecycle_break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, conditional_fraction_npv_positive, interpretation
- Sample: `{"seed": "20261107", "context_id": "GEN002_LC004_R05", "sample_size": "8192", "lifecycle_break_even_p05": "135.53201934152764", "lifecycle_break_even_p50": "222.3846788513922", "lifecycle_break_even_p95": "363.9125502045286", "npv_p05_eur": "-11135158432.727226", "npv_p50_eur": "-5332374242.742248", "npv_p95_eur": "1871429889.2727246", "conditional_fraction_npv_positive": "0.102783203125", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`
- Sample: `{"seed": "20261107", "context_id": "GEN002_LC004_R10", "sample_size": "8192", "lifecycle_break_even_p05": "147.97402718594464", "lifecycle_break_even_p50": "238.15769212411323", "lifecycle_break_even_p95": "383.10600570754525", "npv_p05_eur": "-12332545200.026941", "npv_p50_eur": "-6310133944.864283", "npv_p95_eur": "658424415.9707156", "conditional_fraction_npv_positive": "0.066162109375", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`

## stage52_summary_seed20261108_n131072.csv
- SHA256: `3fcae89a027c0d4bf7269b735cf9e8603bb175f4a1220da950fe9da67e316dc5`
- Bytes: 2877
- Rows: 12
- Columns: seed, context_id, sample_size, lifecycle_break_even_p05, lifecycle_break_even_p50, lifecycle_break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, conditional_fraction_npv_positive, interpretation
- Sample: `{"seed": "20261108", "context_id": "GEN002_LC004_R05", "sample_size": "131072", "lifecycle_break_even_p05": "133.56710715962475", "lifecycle_break_even_p50": "221.555859790803", "lifecycle_break_even_p95": "366.77881706895636", "npv_p05_eur": "-11136138430.251225", "npv_p50_eur": "-5246807522.042931", "npv_p95_eur": "2178779810.375727", "conditional_fraction_npv_positive": "0.1112213134765625", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`
- Sample: `{"seed": "20261108", "context_id": "GEN002_LC004_R10", "sample_size": "131072", "lifecycle_break_even_p05": "145.8502244600978", "lifecycle_break_even_p50": "237.66724125275016", "lifecycle_break_even_p95": "386.318280493385", "npv_p05_eur": "-12376220058.15169", "npv_p50_eur": "-6244455188.18358", "npv_p95_eur": "995832466.207938", "conditional_fraction_npv_positive": "0.07399749755859375", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`

## stage52_summary_seed20261108_n32768.csv
- SHA256: `19449b23d4d0fc05c1b06435dadaa2462dd6eafb1c0560a5a77ed659e0fb2054`
- Bytes: 2845
- Rows: 12
- Columns: seed, context_id, sample_size, lifecycle_break_even_p05, lifecycle_break_even_p50, lifecycle_break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, conditional_fraction_npv_positive, interpretation
- Sample: `{"seed": "20261108", "context_id": "GEN002_LC004_R05", "sample_size": "32768", "lifecycle_break_even_p05": "133.46666969318122", "lifecycle_break_even_p50": "221.70955559528045", "lifecycle_break_even_p95": "367.2559367020077", "npv_p05_eur": "-11109975706.991444", "npv_p50_eur": "-5264053338.029192", "npv_p95_eur": "2141492206.1018138", "conditional_fraction_npv_positive": "0.11138916015625", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`
- Sample: `{"seed": "20261108", "context_id": "GEN002_LC004_R10", "sample_size": "32768", "lifecycle_break_even_p05": "145.69333014792997", "lifecycle_break_even_p50": "237.90214945592152", "lifecycle_break_even_p95": "386.6725452062219", "npv_p05_eur": "-12345105081.9535", "npv_p50_eur": "-6269254421.581294", "npv_p95_eur": "977574438.4806718", "conditional_fraction_npv_positive": "0.07232666015625", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`

## stage52_summary_seed20261108_n8192.csv
- SHA256: `21490ea0c2dab67b9083cb651ac17b767b298aca299c218e3043ef72c53fb747`
- Bytes: 2801
- Rows: 12
- Columns: seed, context_id, sample_size, lifecycle_break_even_p05, lifecycle_break_even_p50, lifecycle_break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, conditional_fraction_npv_positive, interpretation
- Sample: `{"seed": "20261108", "context_id": "GEN002_LC004_R05", "sample_size": "8192", "lifecycle_break_even_p05": "132.4485642528128", "lifecycle_break_even_p50": "221.0473536964781", "lifecycle_break_even_p95": "367.40397434907413", "npv_p05_eur": "-11187933400.563044", "npv_p50_eur": "-5254557560.427105", "npv_p95_eur": "2194504837.4004674", "conditional_fraction_npv_positive": "0.111083984375", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`
- Sample: `{"seed": "20261108", "context_id": "GEN002_LC004_R10", "sample_size": "8192", "lifecycle_break_even_p05": "144.4120463327577", "lifecycle_break_even_p50": "237.12988193185745", "lifecycle_break_even_p95": "386.63630499993803", "npv_p05_eur": "-12424428908.953768", "npv_p50_eur": "-6263321839.29294", "npv_p95_eur": "1056237726.4292247", "conditional_fraction_npv_positive": "0.072265625", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`

## stage53_audit.json
- SHA256: `61633d2efe2642135804f0039a5bca847777ff3290c390690295464c7687a822`
- Bytes: 1281
- Top-level keys: stage, status, design, canonical_sample_sizes, required_seeds, processed, failed_refinement_tests, consecutive_refinements_required, notes

## stage53_extension_audit.json
- SHA256: `b7e01cc5bddc2aa45a595f35b398a9a78c8f6a45e55ffacd74a618512de5419d`
- Bytes: 1357
- Top-level keys: stage, status, design, extension_sample_sizes, required_seeds, processed, failed_refinement_tests, consecutive_refinements_required, notes

## stage543_learning_summary_seed20261105_n2048.csv
- SHA256: `8707d83dd85f2379476de5d6547e8da45d722acff5f5991512c297dad0f5f717`
- Bytes: 1067
- Rows: 5
- Columns: seed, sample_size, context_id, cumulative_equivalent_units, break_even_p05, break_even_p50, break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, positive_fraction, mean_capex_reduction_fraction
- Sample: `{"seed": "20261105", "sample_size": "2048", "context_id": "GEN002_LC004_R05", "cumulative_equivalent_units": "1", "break_even_p05": "132.65691745720068", "break_even_p50": "217.77035300149902", "break_even_p95": "365.4688315833115", "npv_p05_eur": "-10980700945.152624", "npv_p50_eur": "-5090623226.47911", "npv_p95_eur": "2277212003.1085668", "positive_fraction": "0.12255859375", "mean_capex_reduction_fraction": "0.0"}`
- Sample: `{"seed": "20261105", "sample_size": "2048", "context_id": "GEN002_LC004_R05", "cumulative_equivalent_units": "2", "break_even_p05": "130.47002905627795", "break_even_p50": "213.12687993836641", "break_even_p95": "357.8486520211894", "npv_p05_eur": "-10614698750.928534", "npv_p50_eur": "-4840309040.817728", "npv_p95_eur": "2552637926.603374", "positive_fraction": "0.1376953125", "mean_capex_reduction_fraction": "0.024374618590163988"}`

## stage543_learning_summary_seed20261105_n8192.csv
- SHA256: `9ff9f55d8abf774afb3ef53cad7dde470d5d0d10f2e15d629ed23758fc237cfc`
- Bytes: 1078
- Rows: 5
- Columns: seed, sample_size, context_id, cumulative_equivalent_units, break_even_p05, break_even_p50, break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, positive_fraction, mean_capex_reduction_fraction
- Sample: `{"seed": "20261105", "sample_size": "8192", "context_id": "GEN002_LC004_R05", "cumulative_equivalent_units": "1", "break_even_p05": "132.68561578392362", "break_even_p50": "218.84149676056646", "break_even_p95": "362.7161982567364", "npv_p05_eur": "-11066938158.967888", "npv_p50_eur": "-5173353384.438463", "npv_p95_eur": "2129650614.6595783", "positive_fraction": "0.1126708984375", "mean_capex_reduction_fraction": "0.0"}`
- Sample: `{"seed": "20261105", "sample_size": "8192", "context_id": "GEN002_LC004_R05", "cumulative_equivalent_units": "2", "break_even_p05": "130.47097655451898", "break_even_p50": "214.45844159830227", "break_even_p95": "354.89546497171233", "npv_p05_eur": "-10720613816.29229", "npv_p50_eur": "-4921317336.208149", "npv_p95_eur": "2401420460.825609", "positive_fraction": "0.12353515625", "mean_capex_reduction_fraction": "0.024723144989544088"}`

## stage543_learning_summary_seed20261106_n8192.csv
- SHA256: `9c839dcd974bf08c58a3b78ed745d63593597e451ab6b21777dbbf3eea1c099d`
- Bytes: 1078
- Rows: 5
- Columns: seed, sample_size, context_id, cumulative_equivalent_units, break_even_p05, break_even_p50, break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, positive_fraction, mean_capex_reduction_fraction
- Sample: `{"seed": "20261106", "sample_size": "8192", "context_id": "GEN002_LC004_R05", "cumulative_equivalent_units": "1", "break_even_p05": "133.5872758864629", "break_even_p50": "221.43662120590687", "break_even_p95": "367.5083483800788", "npv_p05_eur": "-11121132074.329699", "npv_p50_eur": "-5225338356.257486", "npv_p95_eur": "2095307899.2290223", "positive_fraction": "0.1107177734375", "mean_capex_reduction_fraction": "0.0"}`
- Sample: `{"seed": "20261106", "sample_size": "8192", "context_id": "GEN002_LC004_R05", "cumulative_equivalent_units": "2", "break_even_p05": "131.4324128133084", "break_even_p50": "216.62475001357376", "break_even_p95": "358.4779845900052", "npv_p05_eur": "-10758466782.54154", "npv_p50_eur": "-4953479268.027357", "npv_p95_eur": "2260255745.162068", "positive_fraction": "0.121826171875", "mean_capex_reduction_fraction": "0.025177782485124922"}`

## stage543_learning_summary_seed20261107_n8192.csv
- SHA256: `39fb4b0d86747bed6c9476925a7dae5a26f1221d2be0a25bde0de73a730b4ee0`
- Bytes: 1068
- Rows: 5
- Columns: seed, sample_size, context_id, cumulative_equivalent_units, break_even_p05, break_even_p50, break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, positive_fraction, mean_capex_reduction_fraction
- Sample: `{"seed": "20261107", "sample_size": "8192", "context_id": "GEN002_LC004_R05", "cumulative_equivalent_units": "1", "break_even_p05": "135.53201934152764", "break_even_p50": "222.3846788513922", "break_even_p95": "363.9125502045286", "npv_p05_eur": "-11135158432.727226", "npv_p50_eur": "-5332374242.742248", "npv_p95_eur": "1871429889.2727246", "positive_fraction": "0.102783203125", "mean_capex_reduction_fraction": "0.0"}`
- Sample: `{"seed": "20261107", "sample_size": "8192", "context_id": "GEN002_LC004_R05", "cumulative_equivalent_units": "2", "break_even_p05": "133.5409741913395", "break_even_p50": "217.79544750473923", "break_even_p95": "357.3504158243463", "npv_p05_eur": "-10803043602.36512", "npv_p50_eur": "-5057693161.499514", "npv_p95_eur": "2116677840.3770583", "positive_fraction": "0.112060546875", "mean_capex_reduction_fraction": "0.02508510133164421"}`

## stage543_learning_summary_seed20261108_n8192.csv
- SHA256: `2ba4043e450eb607a4650fc16cddb44c91183da63bca4742cc19236c1537a6a5`
- Bytes: 1079
- Rows: 5
- Columns: seed, sample_size, context_id, cumulative_equivalent_units, break_even_p05, break_even_p50, break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, positive_fraction, mean_capex_reduction_fraction
- Sample: `{"seed": "20261108", "sample_size": "8192", "context_id": "GEN002_LC004_R05", "cumulative_equivalent_units": "1", "break_even_p05": "132.4485642528128", "break_even_p50": "221.0473536964781", "break_even_p95": "367.40397434907413", "npv_p05_eur": "-11187933400.563044", "npv_p50_eur": "-5254557560.427105", "npv_p95_eur": "2194504837.4004674", "positive_fraction": "0.111083984375", "mean_capex_reduction_fraction": "0.0"}`
- Sample: `{"seed": "20261108", "sample_size": "8192", "context_id": "GEN002_LC004_R05", "cumulative_equivalent_units": "2", "break_even_p05": "130.18784814619335", "break_even_p50": "216.5258538460709", "break_even_p95": "359.47799442526787", "npv_p05_eur": "-10873149717.295902", "npv_p50_eur": "-4980933070.813482", "npv_p95_eur": "2413289758.5980577", "positive_fraction": "0.1187744140625", "mean_capex_reduction_fraction": "0.024999375539167423"}`

## stage54_dependency_aligned_burden_stress_summary_seed20261105_n2048.csv
- SHA256: `4b878b75b878828a4ce2e29258914246824bc61922ee9423ad0372a216927ed5`
- Bytes: 2764
- Rows: 12
- Columns: seed, context_id, sample_size, lifecycle_break_even_p05, lifecycle_break_even_p50, lifecycle_break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, conditional_fraction_npv_positive, interpretation
- Sample: `{"seed": "20261105", "context_id": "GEN002_LC004_R05", "sample_size": "2048", "lifecycle_break_even_p05": "94.76727070203341", "lifecycle_break_even_p50": "226.79201461806804", "lifecycle_break_even_p95": "433.19228023989996", "npv_p05_eur": "-13214507317.685472", "npv_p50_eur": "-5331720625.071793", "npv_p95_eur": "11105326026.35288", "conditional_fraction_npv_positive": "0.3095703125", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`
- Sample: `{"seed": "20261105", "context_id": "GEN002_LC004_R10", "sample_size": "2048", "lifecycle_break_even_p05": "105.58826420691264", "lifecycle_break_even_p50": "242.8842748614442", "lifecycle_break_even_p95": "453.89005243298186", "npv_p05_eur": "-14000997103.609495", "npv_p50_eur": "-6318635205.759832", "npv_p95_eur": "9908947325.547293", "conditional_fraction_npv_positive": "0.2783203125", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`

## stage54_dependency_aligned_burden_stress_summary_seed20261105_n8192.csv
- SHA256: `473aedfec3766d4587d5a620bf10ac2fe21038d3a3681b1f528f75b7d8e306f9`
- Bytes: 2801
- Rows: 12
- Columns: seed, context_id, sample_size, lifecycle_break_even_p05, lifecycle_break_even_p50, lifecycle_break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, conditional_fraction_npv_positive, interpretation
- Sample: `{"seed": "20261105", "context_id": "GEN002_LC004_R05", "sample_size": "8192", "lifecycle_break_even_p05": "96.15332927786078", "lifecycle_break_even_p50": "225.3008591294557", "lifecycle_break_even_p95": "434.56021688758227", "npv_p05_eur": "-13246105366.35581", "npv_p50_eur": "-5234821352.172436", "npv_p95_eur": "10770032250.906542", "conditional_fraction_npv_positive": "0.3133544921875", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`
- Sample: `{"seed": "20261105", "context_id": "GEN002_LC004_R10", "sample_size": "8192", "lifecycle_break_even_p05": "107.05103218935665", "lifecycle_break_even_p50": "241.34877510114498", "lifecycle_break_even_p95": "455.2814964227575", "npv_p05_eur": "-14031612303.865364", "npv_p50_eur": "-6223696354.633077", "npv_p95_eur": "9575971100.64138", "conditional_fraction_npv_positive": "0.2806396484375", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`

## stage54_dependency_aligned_burden_stress_summary_seed20261106_n8192.csv
- SHA256: `e3449cbe19d8e0137f297695b62192d852a374a416244fc0b8c4d8f6172b07dc`
- Bytes: 2800
- Rows: 12
- Columns: seed, context_id, sample_size, lifecycle_break_even_p05, lifecycle_break_even_p50, lifecycle_break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, conditional_fraction_npv_positive, interpretation
- Sample: `{"seed": "20261106", "context_id": "GEN002_LC004_R05", "sample_size": "8192", "lifecycle_break_even_p05": "97.36406179107674", "lifecycle_break_even_p50": "228.2923843508853", "lifecycle_break_even_p95": "435.3400260945893", "npv_p05_eur": "-13264048706.666325", "npv_p50_eur": "-5428201391.850367", "npv_p95_eur": "10482699054.22887", "conditional_fraction_npv_positive": "0.3084716796875", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`
- Sample: `{"seed": "20261106", "context_id": "GEN002_LC004_R10", "sample_size": "8192", "lifecycle_break_even_p05": "108.32819966684264", "lifecycle_break_even_p50": "244.42902904474488", "lifecycle_break_even_p95": "456.07467706041905", "npv_p05_eur": "-14048996836.835363", "npv_p50_eur": "-6413153181.084488", "npv_p95_eur": "9290675264.872276", "conditional_fraction_npv_positive": "0.2720947265625", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`

## stage54_dependency_aligned_burden_stress_summary_seed20261107_n8192.csv
- SHA256: `e5951b898fc66b1661e548aadf712429fc92e6e053871b5aad54272440660968`
- Bytes: 2800
- Rows: 12
- Columns: seed, context_id, sample_size, lifecycle_break_even_p05, lifecycle_break_even_p50, lifecycle_break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, conditional_fraction_npv_positive, interpretation
- Sample: `{"seed": "20261107", "context_id": "GEN002_LC004_R05", "sample_size": "8192", "lifecycle_break_even_p05": "97.39182692954081", "lifecycle_break_even_p50": "228.26755348687772", "lifecycle_break_even_p95": "437.31092570867844", "npv_p05_eur": "-13309176124.31749", "npv_p50_eur": "-5426613080.565541", "npv_p95_eur": "10476169214.823553", "conditional_fraction_npv_positive": "0.2999267578125", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`
- Sample: `{"seed": "20261107", "context_id": "GEN002_LC004_R10", "sample_size": "8192", "lifecycle_break_even_p05": "108.3574821566438", "lifecycle_break_even_p50": "244.40346557131454", "lifecycle_break_even_p95": "458.07927788089773", "npv_p05_eur": "-14092716666.65898", "npv_p50_eur": "-6411597272.309594", "npv_p95_eur": "9284192280.072737", "conditional_fraction_npv_positive": "0.2637939453125", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`

## stage54_dependency_aligned_burden_stress_summary_seed20261108_n8192.csv
- SHA256: `d130f6db2cc8f6e547dca5da504706d4c42e2e80e8a771370e65851b2a8cde5b`
- Bytes: 2801
- Rows: 12
- Columns: seed, context_id, sample_size, lifecycle_break_even_p05, lifecycle_break_even_p50, lifecycle_break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, conditional_fraction_npv_positive, interpretation
- Sample: `{"seed": "20261108", "context_id": "GEN002_LC004_R05", "sample_size": "8192", "lifecycle_break_even_p05": "96.9631801282074", "lifecycle_break_even_p50": "226.63086059867237", "lifecycle_break_even_p95": "437.1957532273159", "npv_p05_eur": "-13306547771.315218", "npv_p50_eur": "-5321297995.718286", "npv_p95_eur": "10577273806.297316", "conditional_fraction_npv_positive": "0.3143310546875", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`
- Sample: `{"seed": "20261108", "context_id": "GEN002_LC004_R10", "sample_size": "8192", "lifecycle_break_even_p05": "107.90537932651661", "lifecycle_break_even_p50": "242.7183397855126", "lifecycle_break_even_p95": "457.96213970761715", "npv_p05_eur": "-14090170381.646868", "npv_p50_eur": "-6308423972.510752", "npv_p95_eur": "9384574165.359558", "conditional_fraction_npv_positive": "0.282958984375", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`

## stage54_dependency_audit_seed20261105_n2048.json
- SHA256: `840afae47533cceae2403463ea52d6d19dfd793c62ac5200831e19a36c156b9f`
- Bytes: 1218
- Top-level keys: status, seed, n, contexts, modes, baseline_file, baseline_sha256, stress_inputs, comparison_sha256, method, warning

## stage54_dependency_audit_seed20261105_n8192.json
- SHA256: `89b9f06a4e0c01f96e6d80b4caad291d7a65e7d048e8feaef4af98e6174885cb`
- Bytes: 1218
- Top-level keys: status, seed, n, contexts, modes, baseline_file, baseline_sha256, stress_inputs, comparison_sha256, method, warning

## stage54_dependency_audit_seed20261106_n8192.json
- SHA256: `387aefe4f50b720960b953bd97a3696175b1c4f71487639b1b8bf650d49219c5`
- Bytes: 1218
- Top-level keys: status, seed, n, contexts, modes, baseline_file, baseline_sha256, stress_inputs, comparison_sha256, method, warning

## stage54_dependency_audit_seed20261107_n8192.json
- SHA256: `28b03ceeed22b110645af8e2a0c22f684dc4f9e2aae80d005b05a6da48d546d5`
- Bytes: 1218
- Top-level keys: status, seed, n, contexts, modes, baseline_file, baseline_sha256, stress_inputs, comparison_sha256, method, warning

## stage54_dependency_audit_seed20261108_n8192.json
- SHA256: `c930087c6507ac8947474c8045c03c876feffa0d8f97adf851c79cc34e7a63ce`
- Bytes: 1218
- Top-level keys: status, seed, n, contexts, modes, baseline_file, baseline_sha256, stress_inputs, comparison_sha256, method, warning

## stage54_dependency_offsetting_burden_stress_summary_seed20261105_n2048.csv
- SHA256: `cdb94ca2daf231936a904313d7fd1e99685f29f319b79c02830b277333db94c7`
- Bytes: 2723
- Rows: 12
- Columns: seed, context_id, sample_size, lifecycle_break_even_p05, lifecycle_break_even_p50, lifecycle_break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, conditional_fraction_npv_positive, interpretation
- Sample: `{"seed": "20261105", "context_id": "GEN002_LC004_R05", "sample_size": "2048", "lifecycle_break_even_p05": "184.98944432602153", "lifecycle_break_even_p50": "228.94073812052716", "lifecycle_break_even_p95": "239.1716791321619", "npv_p05_eur": "-6005040859.467515", "npv_p50_eur": "-5473686030.354402", "npv_p95_eur": "872310858.6159935", "conditional_fraction_npv_positive": "0.07958984375", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`
- Sample: `{"seed": "20261105", "context_id": "GEN002_LC004_R10", "sample_size": "2048", "lifecycle_break_even_p05": "207.43315508397026", "lifecycle_break_even_p50": "244.29063621262162", "lifecycle_break_even_p95": "251.54209883157677", "npv_p05_eur": "-6656614852.5574875", "npv_p50_eur": "-6167405188.713419", "npv_p95_eur": "-1547768567.1815689", "conditional_fraction_npv_positive": "0.0", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`

## stage54_dependency_offsetting_burden_stress_summary_seed20261105_n8192.csv
- SHA256: `f2f7f60f0f51e37102d3fe075665e81582490941dff493a8c1ed99c3b99268cd`
- Bytes: 2726
- Rows: 12
- Columns: seed, context_id, sample_size, lifecycle_break_even_p05, lifecycle_break_even_p50, lifecycle_break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, conditional_fraction_npv_positive, interpretation
- Sample: `{"seed": "20261105", "context_id": "GEN002_LC004_R05", "sample_size": "8192", "lifecycle_break_even_p05": "184.69021863389767", "lifecycle_break_even_p50": "229.20432228016386", "lifecycle_break_even_p95": "239.18247920448846", "npv_p05_eur": "-6004709377.474704", "npv_p50_eur": "-5493574669.17407", "npv_p95_eur": "939761823.3179805", "conditional_fraction_npv_positive": "0.0845947265625", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`
- Sample: `{"seed": "20261105", "context_id": "GEN002_LC004_R10", "sample_size": "8192", "lifecycle_break_even_p05": "207.16899242867711", "lifecycle_break_even_p50": "244.4074128460398", "lifecycle_break_even_p95": "251.53136352333894", "npv_p05_eur": "-6656386777.211199", "npv_p50_eur": "-6174790723.017708", "npv_p95_eur": "-1492503932.962297", "conditional_fraction_npv_positive": "0.0", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`

## stage54_dependency_offsetting_burden_stress_summary_seed20261106_n8192.csv
- SHA256: `5ec606a56a76de89856128435c29046b8cf85e9cded8935002a453c85bab782e`
- Bytes: 2722
- Rows: 12
- Columns: seed, context_id, sample_size, lifecycle_break_even_p05, lifecycle_break_even_p50, lifecycle_break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, conditional_fraction_npv_positive, interpretation
- Sample: `{"seed": "20261106", "context_id": "GEN002_LC004_R05", "sample_size": "8192", "lifecycle_break_even_p05": "184.5197275340157", "lifecycle_break_even_p50": "228.67361755285185", "lifecycle_break_even_p95": "239.17138802611322", "npv_p05_eur": "-6005056151.534997", "npv_p50_eur": "-5453307028.860454", "npv_p95_eur": "978377084.4491109", "conditional_fraction_npv_positive": "0.089111328125", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`
- Sample: `{"seed": "20261106", "context_id": "GEN002_LC004_R10", "sample_size": "8192", "lifecycle_break_even_p05": "207.01845716999637", "lifecycle_break_even_p50": "244.30879229921243", "lifecycle_break_even_p95": "251.53136450267087", "npv_p05_eur": "-6657033211.649003", "npv_p50_eur": "-6171512432.385544", "npv_p95_eur": "-1460853313.3436425", "conditional_fraction_npv_positive": "0.0", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`

## stage54_dependency_offsetting_burden_stress_summary_seed20261107_n8192.csv
- SHA256: `6d8fe841d40ff3b4869e549879d2937b8e107e4964914fc35c3df5405e0d7aab`
- Bytes: 2722
- Rows: 12
- Columns: seed, context_id, sample_size, lifecycle_break_even_p05, lifecycle_break_even_p50, lifecycle_break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, conditional_fraction_npv_positive, interpretation
- Sample: `{"seed": "20261107", "context_id": "GEN002_LC004_R05", "sample_size": "8192", "lifecycle_break_even_p05": "184.08910913897336", "lifecycle_break_even_p50": "228.67805410058222", "lifecycle_break_even_p95": "239.16719561867743", "npv_p05_eur": "-6005586350.809249", "npv_p50_eur": "-5453647375.44359", "npv_p95_eur": "1076504977.19298", "conditional_fraction_npv_positive": "0.089111328125", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`
- Sample: `{"seed": "20261107", "context_id": "GEN002_LC004_R10", "sample_size": "8192", "lifecycle_break_even_p05": "206.63817153829996", "lifecycle_break_even_p50": "244.3078729734421", "lifecycle_break_even_p95": "251.54594551070127", "npv_p05_eur": "-6656417122.571086", "npv_p50_eur": "-6178440164.089608", "npv_p95_eur": "-1380385218.5292623", "conditional_fraction_npv_positive": "0.0", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`

## stage54_dependency_offsetting_burden_stress_summary_seed20261108_n8192.csv
- SHA256: `aa3eea867f00e2504aab884b55fc0089bb37c0e5f8f00b9a35fd59003f0abca2`
- Bytes: 2725
- Rows: 12
- Columns: seed, context_id, sample_size, lifecycle_break_even_p05, lifecycle_break_even_p50, lifecycle_break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, conditional_fraction_npv_positive, interpretation
- Sample: `{"seed": "20261108", "context_id": "GEN002_LC004_R05", "sample_size": "8192", "lifecycle_break_even_p05": "184.1142617107456", "lifecycle_break_even_p50": "228.96931769833037", "lifecycle_break_even_p95": "239.18026426439414", "npv_p05_eur": "-6004750928.051382", "npv_p50_eur": "-5475853268.995472", "npv_p95_eur": "1070749759.6127243", "conditional_fraction_npv_positive": "0.08935546875", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`
- Sample: `{"seed": "20261108", "context_id": "GEN002_LC004_R10", "sample_size": "8192", "lifecycle_break_even_p05": "206.66038692310966", "lifecycle_break_even_p50": "244.33451885435278", "lifecycle_break_even_p95": "251.5328523294612", "npv_p05_eur": "-6655441444.216213", "npv_p50_eur": "-6169746398.488663", "npv_p95_eur": "-1385106197.7349777", "conditional_fraction_npv_positive": "0.0", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`

## stage54_marginal_comparison_audit_seed20261105_n2048.json
- SHA256: `afb003a8ef478dc2ebaa678ad8f6302464f22c8a2e70d823806b491e182c0125`
- Bytes: 676
- Top-level keys: status, seed, sample_size_per_context, contexts, total_paired_evaluations, uniform_input_sha256, triangular_input_sha256, comparison_sha256, methods, interpretation

## stage54_marginal_comparison_audit_seed20261105_n8192.json
- SHA256: `287dd863e3becb91ea670805933c1829c9d637e448cec435203b5ade141b81ad`
- Bytes: 676
- Top-level keys: status, seed, sample_size_per_context, contexts, total_paired_evaluations, uniform_input_sha256, triangular_input_sha256, comparison_sha256, methods, interpretation

## stage54_marginal_comparison_audit_seed20261106_n8192.json
- SHA256: `7d2793cb4216eaf8f62c0c88d09c99bb5812f19dd94cbee3f7d5c620d8295806`
- Bytes: 676
- Top-level keys: status, seed, sample_size_per_context, contexts, total_paired_evaluations, uniform_input_sha256, triangular_input_sha256, comparison_sha256, methods, interpretation

## stage54_marginal_comparison_audit_seed20261107_n8192.json
- SHA256: `83351770085cbe699d97ad74a120f8a6ec16666ec0c458176161f2ed96f547fb`
- Bytes: 676
- Top-level keys: status, seed, sample_size_per_context, contexts, total_paired_evaluations, uniform_input_sha256, triangular_input_sha256, comparison_sha256, methods, interpretation

## stage54_marginal_comparison_audit_seed20261108_n8192.json
- SHA256: `c35e1b9debbc7624ad276aadff05e12fef8278ec0fab91208a0cec57d4269548`
- Bytes: 676
- Top-level keys: status, seed, sample_size_per_context, contexts, total_paired_evaluations, uniform_input_sha256, triangular_input_sha256, comparison_sha256, methods, interpretation

## stage54_triangular_summary_seed20261105_n2048.csv
- SHA256: `0e1d2613ca3f5c1e568909359e79a3a04d1703ea12e88fb2222b80b59502a1be`
- Bytes: 2772
- Rows: 12
- Columns: seed, context_id, sample_size, lifecycle_break_even_p05, lifecycle_break_even_p50, lifecycle_break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, conditional_fraction_npv_positive, interpretation
- Sample: `{"seed": "20261105", "context_id": "GEN002_LC004_R05", "sample_size": "2048", "lifecycle_break_even_p05": "153.34439074869388", "lifecycle_break_even_p50": "217.8043040388556", "lifecycle_break_even_p95": "312.35749831451625", "npv_p05_eur": "-8742131809.113438", "npv_p50_eur": "-4253456864.540021", "npv_p95_eur": "676549478.1510231", "conditional_fraction_npv_positive": "0.08056640625", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`
- Sample: `{"seed": "20261105", "context_id": "GEN002_LC004_R10", "sample_size": "2048", "lifecycle_break_even_p05": "166.22354781505476", "lifecycle_break_even_p50": "233.67922577784566", "lifecycle_break_even_p95": "330.2992664012134", "npv_p05_eur": "-9834923116.462452", "npv_p50_eur": "-5189099443.550177", "npv_p95_eur": "-387080709.44950175", "conditional_fraction_npv_positive": "0.03759765625", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`

## stage54_triangular_summary_seed20261105_n8192.csv
- SHA256: `371252e8888d634dc5bb1c4ed34622657a8e6573d0c9b8b4fe93f17511543b69`
- Bytes: 2820
- Rows: 12
- Columns: seed, context_id, sample_size, lifecycle_break_even_p05, lifecycle_break_even_p50, lifecycle_break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, conditional_fraction_npv_positive, interpretation
- Sample: `{"seed": "20261105", "context_id": "GEN002_LC004_R05", "sample_size": "8192", "lifecycle_break_even_p05": "154.03555866500363", "lifecycle_break_even_p50": "218.58337744233995", "lifecycle_break_even_p95": "310.6021689004267", "npv_p05_eur": "-8755783050.484083", "npv_p50_eur": "-4305723501.786383", "npv_p95_eur": "602623515.5324025", "conditional_fraction_npv_positive": "0.0738525390625", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`
- Sample: `{"seed": "20261105", "context_id": "GEN002_LC004_R10", "sample_size": "8192", "lifecycle_break_even_p05": "166.92813396770083", "lifecycle_break_even_p50": "234.3479841036181", "lifecycle_break_even_p95": "328.54342855674446", "npv_p05_eur": "-9846994520.63435", "npv_p50_eur": "-5265527717.3490925", "npv_p95_eur": "-460398896.31634814", "conditional_fraction_npv_positive": "0.035888671875", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`

## stage54_triangular_summary_seed20261106_n8192.csv
- SHA256: `7c5326e7db2c1fac8cf39d6e1a558ab8f696666b36edecd71990c6fd99f3e673`
- Bytes: 2810
- Rows: 12
- Columns: seed, context_id, sample_size, lifecycle_break_even_p05, lifecycle_break_even_p50, lifecycle_break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, conditional_fraction_npv_positive, interpretation
- Sample: `{"seed": "20261106", "context_id": "GEN002_LC004_R05", "sample_size": "8192", "lifecycle_break_even_p05": "154.25972279691945", "lifecycle_break_even_p50": "220.24278228317135", "lifecycle_break_even_p95": "315.9509478055476", "npv_p05_eur": "-8838089292.883982", "npv_p50_eur": "-4354009592.882257", "npv_p95_eur": "538281904.7153542", "conditional_fraction_npv_positive": "0.07080078125", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`
- Sample: `{"seed": "20261106", "context_id": "GEN002_LC004_R10", "sample_size": "8192", "lifecycle_break_even_p05": "167.73957681211942", "lifecycle_break_even_p50": "235.64216183160988", "lifecycle_break_even_p95": "333.86329067061934", "npv_p05_eur": "-9921512898.364765", "npv_p50_eur": "-5298227631.835823", "npv_p95_eur": "-532316443.0263614", "conditional_fraction_npv_positive": "0.032958984375", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`

## stage54_triangular_summary_seed20261107_n8192.csv
- SHA256: `5a67db861c651374cc39841379500a3e93f3aa6efa51404c167390fafa73cd55`
- Bytes: 2805
- Rows: 12
- Columns: seed, context_id, sample_size, lifecycle_break_even_p05, lifecycle_break_even_p50, lifecycle_break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, conditional_fraction_npv_positive, interpretation
- Sample: `{"seed": "20261107", "context_id": "GEN002_LC004_R05", "sample_size": "8192", "lifecycle_break_even_p05": "155.32478200851338", "lifecycle_break_even_p50": "220.50450279031702", "lifecycle_break_even_p95": "312.4460186748621", "npv_p05_eur": "-8864997010.069801", "npv_p50_eur": "-4394765273.885855", "npv_p95_eur": "472115140.73976165", "conditional_fraction_npv_positive": "0.066162109375", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`
- Sample: `{"seed": "20261107", "context_id": "GEN002_LC004_R10", "sample_size": "8192", "lifecycle_break_even_p05": "169.06265154955025", "lifecycle_break_even_p50": "236.22448169690205", "lifecycle_break_even_p95": "330.3874288510696", "npv_p05_eur": "-9973849705.495878", "npv_p50_eur": "-5362728757.260307", "npv_p95_eur": "-589952119.5102956", "conditional_fraction_npv_positive": "0.031982421875", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`

## stage54_triangular_summary_seed20261108_n8192.csv
- SHA256: `e80d7861667c52390acd2e843160c76bcab8bdd421714fd24b544c4f9a4b2e4e`
- Bytes: 2810
- Rows: 12
- Columns: seed, context_id, sample_size, lifecycle_break_even_p05, lifecycle_break_even_p50, lifecycle_break_even_p95, npv_p05_eur, npv_p50_eur, npv_p95_eur, conditional_fraction_npv_positive, interpretation
- Sample: `{"seed": "20261108", "context_id": "GEN002_LC004_R05", "sample_size": "8192", "lifecycle_break_even_p05": "153.2510725971144", "lifecycle_break_even_p50": "220.0974607010853", "lifecycle_break_even_p95": "314.2968253770697", "npv_p05_eur": "-8955135066.661129", "npv_p50_eur": "-4347677103.595069", "npv_p95_eur": "649461983.934888", "conditional_fraction_npv_positive": "0.0728759765625", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`
- Sample: `{"seed": "20261108", "context_id": "GEN002_LC004_R10", "sample_size": "8192", "lifecycle_break_even_p05": "166.80297713661815", "lifecycle_break_even_p50": "236.033865057835", "lifecycle_break_even_p95": "332.26448661300293", "npv_p05_eur": "-10008703876.979132", "npv_p50_eur": "-5312263795.823075", "npv_p95_eur": "-451009116.29736", "conditional_fraction_npv_positive": "0.037841796875", "interpretation": "conditional_exploratory_not_real_world_success_probability"}`

## stage55_cross_seed_summary.csv
- SHA256: `ba68235e0d2e40a739859f4565d06b8ac15915629d793af69a47e48b9c3392c9`
- Bytes: 10486
- Rows: 41
- Columns: experiment, context_id, sample_size_per_seed, break_even_delta_p50_seed_mean, break_even_delta_p50_seed_min, break_even_delta_p50_seed_max, NPV_delta_p50_seed_mean, NPV_delta_p50_seed_min, NPV_delta_p50_seed_max, positive_fraction_delta_seed_mean, positive_fraction_delta_seed_min, positive_fraction_delta_seed_max, mode, cumulative_equivalent_units, mean_capex_reduction_fraction_seed_mean, mean_capex_reduction_fraction_seed_min, mean_capex_reduction_fraction_seed_max, break_even_p50_seed_mean, break_even_p50_seed_min, break_even_p50_seed_max, npv_p50_eur_seed_mean, npv_p50_eur_seed_min, npv_p50_eur_seed_max, positive_fraction_seed_mean, positive_fraction_seed_min, positive_fraction_seed_max
- Sample: `{"experiment": "triangular_vs_uniform", "context_id": "GEN002_LC004_R05", "sample_size_per_seed": "8192", "break_even_delta_p50_seed_mean": "-1.0705068243575013", "break_even_delta_p50_seed_min": "-1.8801760610751899", "break_even_delta_p50_seed_max": "-0.25811931822650536", "NPV_delta_p50_seed_mean": "895862017.9289346", "NPV_delta_p50_seed_min": "867629882.6520805", "NPV_delta_p50_seed_max": "937608968.8563929", "positive_fraction_delta_seed_mean": "-0.03839111328125", "positive_fraction_delta_seed_min": "-0.0399169921875", "positive_fraction_delta_seed_max": "-0.03662109375", "mode": "", "cumulative_equivalent_units": "", "mean_capex_reduction_fraction_seed_mean": "", "mean_capex_reductio`
- Sample: `{"experiment": "triangular_vs_uniform", "context_id": "GEN002_LC004_R10", "sample_size_per_seed": "8192", "break_even_delta_p50_seed_mean": "-1.3942255779754689", "break_even_delta_p50_seed_min": "-1.9332104272111792", "break_even_delta_p50_seed_max": "-0.9720887572964898", "NPV_delta_p50_seed_mean": "921890296.4970086", "NPV_delta_p50_seed_min": "876871670.6523476", "NPV_delta_p50_seed_max": "951058043.4698648", "positive_fraction_delta_seed_mean": "-0.0369873046875", "positive_fraction_delta_seed_min": "-0.041748046875", "positive_fraction_delta_seed_max": "-0.0341796875", "mode": "", "cumulative_equivalent_units": "", "mean_capex_reduction_fraction_seed_mean": "", "mean_capex_reduction_fr`

## stage55_integration_audit.json
- SHA256: `9ac2fe6afbe232a61f97097763c309fa2d889a0744828ba4057a095e68d5d2b3`
- Bytes: 4653
- Top-level keys: status, n_per_seed, seeds, contexts, marginal_rows, dependency_rows, learning_rows, input_hashes, output_sha256, limits

## stage5_spec_audit.json
- SHA256: `6c87310668547b8b6739e81fadb68450f8656ad653fd1147783bd78d0fc62592`
- Bytes: 603
- Top-level keys: status, simulation_executed, contexts, deterministic_evaluations, errors, limitations

## stage62_value_capture_audit.json
- SHA256: `dbbaa5cb299460cfa3bd0fb1dfd76ee2d979e14a2a235fa21f55c7dff7956ec9`
- Bytes: 1531
- Top-level keys: status, strategy_count, price_scenarios, result_rows, cash_flow_rows, validation, source_sha256, limitations

## stage63_risk_allocation_audit.json
- SHA256: `2f5f5c858bbb27ea37dc8130a0ae60403b26f272c9ae91873a6d863a4e9502cf`
- Bytes: 1848
- Top-level keys: status, result_rows, strategies, price_cases, stress_cases, reconciliation, source_sha256, limitations

## stage64_partial_mcda_audit.json
- SHA256: `d215e3377d6b93436f7db5dbf03607ce166c7b5bb3d2798caa2023db294263de`
- Bytes: 1679
- Top-level keys: status, scored_criteria, excluded_or_pending, scenarios, weight_sets, score_rows, scenarios_with_different_leaders_across_weight_sets, source_sha256, limitations

## stage65_context_gate_summary.csv
- SHA256: `47dc102be3f802d4bfecfbdf5fb48e76be5873fb43b15981f2b3175ee6a5dd2c`
- Bytes: 1288
- Rows: 15
- Columns: price_case, stress_id, feasible_strategy_count, provisional_mcda_leaders, eligible_strategy_ids, provisional_leader_viable, interpretation
- Sample: `{"price_case": "P120", "stress_id": "RS00", "feasible_strategy_count": "0", "provisional_mcda_leaders": "STR03", "eligible_strategy_ids": "", "provisional_leader_viable": "False", "interpretation": "NO_ECONOMICALLY_ELIGIBLE_STRATEGY_NO_RECOMMENDATION"}`
- Sample: `{"price_case": "P120", "stress_id": "RS01", "feasible_strategy_count": "0", "provisional_mcda_leaders": "STR03", "eligible_strategy_ids": "", "provisional_leader_viable": "False", "interpretation": "NO_ECONOMICALLY_ELIGIBLE_STRATEGY_NO_RECOMMENDATION"}`

## stage65_feasibility_audit.json
- SHA256: `9b88dc3132e1c11fef936860614488e4de1b8e27cf46a73a6ce1c26ae1d355d9`
- Bytes: 893
- Top-level keys: status, risk_rows, context_rows, threshold_rows, eligible_rows, contexts_with_eligible_strategy, inputs_sha256, limits

## stage65_feasibility_screen.csv
- SHA256: `f6d98ea7a35803c76c708cf827e952dd14ac0f57032cb8a351ffae2fc495dce3`
- Bytes: 21459
- Rows: 60
- Columns: strategy_id, price_case, stress_id, electricity_price_eur_per_mwh, baseline_project_npv_eur, stressed_project_npv_eur, project_npv_change_eur, company_baseline_npv_eur, company_stressed_npv_eur, company_npv_change_eur, external_baseline_npv_eur, external_stressed_npv_eur, external_npv_change_eur, incremental_company_cost_pv_eur, capex_contribution_to_project_npv_eur, delay_contribution_to_project_npv_eur, price_contribution_to_project_npv_eur, capex_risk_company_share, delay_risk_company_share, price_risk_company_share, first_revenue_model_year, model_status, company_gate, external_gate, project_gate, stakeholder_joint_gate, all_economic_gates, policy_status
- Sample: `{"strategy_id": "STR01", "price_case": "P120", "stress_id": "RS00", "electricity_price_eur_per_mwh": "120.0", "baseline_project_npv_eur": "-5696126975.714134", "stressed_project_npv_eur": "-5696126975.714134", "project_npv_change_eur": "0.0", "company_baseline_npv_eur": "-5965105525.164159", "company_stressed_npv_eur": "-5965105525.164159", "company_npv_change_eur": "0.0", "external_baseline_npv_eur": "0.0", "external_stressed_npv_eur": "0.0", "external_npv_change_eur": "0.0", "incremental_company_cost_pv_eur": "268978549.4500235", "capex_contribution_to_project_npv_eur": "0.0", "delay_contribution_to_project_npv_eur": "0.0", "price_contribution_to_project_npv_eur": "0.0", "capex_risk_compan`
- Sample: `{"strategy_id": "STR01", "price_case": "P120", "stress_id": "RS01", "electricity_price_eur_per_mwh": "120.0", "baseline_project_npv_eur": "-5696126975.714134", "stressed_project_npv_eur": "-7738765462.394687", "project_npv_change_eur": "-2042638486.6805525", "company_baseline_npv_eur": "-5965105525.164159", "company_stressed_npv_eur": "-8007744011.844711", "company_npv_change_eur": "-2042638486.6805525", "external_baseline_npv_eur": "0.0", "external_stressed_npv_eur": "0.0", "external_npv_change_eur": "0.0", "incremental_company_cost_pv_eur": "268978549.4500235", "capex_contribution_to_project_npv_eur": "-2042638486.6805525", "delay_contribution_to_project_npv_eur": "0.0", "price_contributio`

## stage65_price_thresholds.csv
- SHA256: `efa736d18c8d398243c6bc0c5e437afdd764e1f076cfb0deccc99f831c9c146b`
- Bytes: 4874
- Rows: 20
- Columns: strategy_id, stress_id, company_npv_slope_eur_per_eur_mwh, company_break_even_price_eur_mwh, external_npv_slope_eur_per_eur_mwh, external_break_even_price_eur_mwh, project_npv_slope_eur_per_eur_mwh, project_break_even_price_eur_mwh, joint_economic_threshold_price_eur_mwh, threshold_location, max_linearity_residual_eur, interpretation
- Sample: `{"strategy_id": "STR01", "stress_id": "RS00", "company_npv_slope_eur_per_eur_mwh": "60976026.27581875", "company_break_even_price_eur_mwh": "217.82706236352004", "external_npv_slope_eur_per_eur_mwh": "0.0", "external_break_even_price_eur_mwh": "", "project_npv_slope_eur_per_eur_mwh": "60976026.27581874", "project_break_even_price_eur_mwh": "213.4158442852326", "joint_economic_threshold_price_eur_mwh": "217.82706236352004", "threshold_location": "EXTRAPOLATED_ABOVE_200", "max_linearity_residual_eur": "9.5367431640625e-07", "interpretation": "ZERO_NPV_GATES_NO_CUSTOMER_FINANCING_OR_CONTRACT_FEASIBILITY"}`
- Sample: `{"strategy_id": "STR01", "stress_id": "RS01", "company_npv_slope_eur_per_eur_mwh": "60976026.27581875", "company_break_even_price_eur_mwh": "251.32610471568793", "external_npv_slope_eur_per_eur_mwh": "0.0", "external_break_even_price_eur_mwh": "", "project_npv_slope_eur_per_eur_mwh": "60976026.27581874", "project_break_even_price_eur_mwh": "246.91488663740046", "joint_economic_threshold_price_eur_mwh": "251.32610471568793", "threshold_location": "EXTRAPOLATED_ABOVE_200", "max_linearity_residual_eur": "9.5367431640625e-07", "interpretation": "ZERO_NPV_GATES_NO_CUSTOMER_FINANCING_OR_CONTRACT_FEASIBILITY"}`

## stage66_context_synthesis.csv
- SHA256: `ddaa7320c867ac3b716d73a4f61cde5f6abfab91f9d7f662ff09a93467dbb63e`
- Bytes: 1386
- Rows: 15
- Columns: price_case, stress_id, feasible_strategy_count, provisional_mcda_leaders, eligible_strategy_ids, provisional_leader_viable, interpretation, leaders
- Sample: `{"price_case": "P120", "stress_id": "RS00", "feasible_strategy_count": "0", "provisional_mcda_leaders": "STR03", "eligible_strategy_ids": "", "provisional_leader_viable": "False", "interpretation": "NO_ECONOMICALLY_ELIGIBLE_STRATEGY_NO_RECOMMENDATION", "leaders": "STR03"}`
- Sample: `{"price_case": "P120", "stress_id": "RS01", "feasible_strategy_count": "0", "provisional_mcda_leaders": "STR03", "eligible_strategy_ids": "", "provisional_leader_viable": "False", "interpretation": "NO_ECONOMICALLY_ELIGIBLE_STRATEGY_NO_RECOMMENDATION", "leaders": "STR03"}`

## stage66_strategy_evidence_matrix.csv
- SHA256: `6faab4525da68b819ce4e271b5d65948770853e46d04bace9dfde197bdaf6788`
- Bytes: 393
- Rows: 4
- Columns: strategy_id, screened_cases, company_pass_count, external_pass_count, project_pass_count, joint_pass_count, mcda_first_place_records, assessment
- Sample: `{"strategy_id": "STR01", "screened_cases": "15", "company_pass_count": "0", "external_pass_count": "15", "project_pass_count": "0", "joint_pass_count": "0", "mcda_first_place_records": "0", "assessment": "NO_ECONOMICALLY_ELIGIBLE_CASE_IN_TESTED_SET"}`
- Sample: `{"strategy_id": "STR02", "screened_cases": "15", "company_pass_count": "0", "external_pass_count": "0", "project_pass_count": "0", "joint_pass_count": "0", "mcda_first_place_records": "0", "assessment": "NO_ECONOMICALLY_ELIGIBLE_CASE_IN_TESTED_SET"}`

## stage66_synthesis_audit.json
- SHA256: `c1a0c18dc80b46207dffa6866b4da4f5fe12aafc218f845628848601df6498bd`
- Bytes: 2292
- Top-level keys: status, source_hashes_sha256, derived_summary
