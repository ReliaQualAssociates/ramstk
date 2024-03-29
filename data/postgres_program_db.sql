CREATE TABLE ramstk_revision (
    fld_revision_id INTEGER NOT NULL,
    fld_availability_logistics FLOAT DEFAULT 1.0,
    fld_availability_mission FLOAT DEFAULT 1.0,
    fld_cost FLOAT DEFAULT 0.0,
    fld_cost_failure FLOAT DEFAULT 0.0,
    fld_cost_hour FLOAT DEFAULT 0.0,
    fld_hazard_rate_active FLOAT DEFAULT 0.0,
    fld_hazard_rate_dormant FLOAT DEFAULT 0.0,
    fld_hazard_rate_logistics FLOAT DEFAULT 0.0,
    fld_hazard_rate_mission FLOAT DEFAULT 0.0,
    fld_hazard_rate_software FLOAT DEFAULT 0.0,
    fld_mmt FLOAT DEFAULT 0.0,
    fld_mcmt FLOAT DEFAULT 0.0,
    fld_mpmt FLOAT DEFAULT 0.0,
    fld_mtbf_logistics FLOAT DEFAULT 0.0,
    fld_mtbf_mission FLOAT DEFAULT 0.0,
    fld_mttr FLOAT DEFAULT 0.0,
    fld_name VARCHAR(128) DEFAULT '',
    fld_reliability_logistics FLOAT DEFAULT 0.0,
    fld_reliability_mission FLOAT DEFAULT 0.0,
    fld_remarks VARCHAR DEFAULT 0.0,
    fld_total_part_count INTEGER DEFAULT 0,
    fld_revision_code VARCHAR(8) DEFAULT '',
    fld_program_time FLOAT DEFAULT 0.0,
    fld_program_time_sd FLOAT DEFAULT 0.0,
    fld_program_cost FLOAT DEFAULT 0.0,
    fld_program_cost_sd FLOAT DEFAULT 0.0,
    PRIMARY KEY (fld_revision_id)
);
INSERT INTO "ramstk_revision" VALUES(1,1.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,'Revision -',1.0,1.0,X'',1,'',0.0,0.0,0.0,0.0);
CREATE TABLE ramstk_mission (
    fld_revision_id INTEGER NOT NULL,
    fld_mission_id INTEGER NOT NULL,
    fld_description VARCHAR DEFAULT '',
    fld_mission_time FLOAT DEFAULT 0.0,
    fld_time_units VARCHAR(256) DEFAULT '',
    PRIMARY KEY (fld_mission_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_mission" VALUES(1,1,'Default Mission',0.0,'hours');
CREATE TABLE ramstk_mission_phase (
    fld_revision_id INTEGER NOT NULL,
    fld_mission_id INTEGER NOT NULL,
    fld_mission_phase_id INTEGER NOT NULL,
    fld_description VARCHAR DEFAULT '',
    fld_name VARCHAR(256) DEFAULT '',
    fld_phase_start FLOAT DEFAULT 0.0,
    fld_phase_end FLOAT DEFAULT 0.0,
    PRIMARY KEY (fld_mission_phase_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE,
    FOREIGN KEY(fld_mission_id) REFERENCES ramstk_mission (fld_mission_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_mission_phase" VALUES (1, 1,1,'Default Mission Phase 1','',0,0.0);
CREATE TABLE ramstk_environment (
    fld_revision_id INTEGER NOT NULL,
    fld_mission_id INTEGER NOT NULL,
    fld_mission_phase_id INTEGER NOT NULL,
    fld_environment_id INTEGER NOT NULL,
    fld_name VARCHAR(256) DEFAULT '',
    fld_units VARCHAR(128) DEFAULT '',
    fld_minimum FLOAT DEFAULT 0.0,
    fld_maximum FLOAT DEFAULT 0.0,
    fld_mean FLOAT DEFAULT 0.0,
    fld_variance FLOAT DEFAULT 0.0,
    fld_ramp_rate FLOAT DEFAULT 0.0,
    fld_low_dwell_time FLOAT DEFAULT 0.0,
    fld_high_dwell_time FLOAT DEFAULT 0.0,
    PRIMARY KEY (fld_environment_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE,
    FOREIGN KEY(fld_mission_id) REFERENCES ramstk_mission (fld_mission_id) ON DELETE CASCADE,
    FOREIGN KEY(fld_mission_phase_id) REFERENCES ramstk_mission_phase (fld_mission_phase_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_environment" VALUES (1,1,1,1,'Environment','',0.0,0.0,0.0,0.0,0.0,0.0,0.0);
CREATE TABLE ramstk_program_info (
    fld_revision_id INTEGER NOT NULL,
    fld_function_active INTEGER DEFAULT 0,
    fld_requirement_active INTEGER DEFAULT 0,
    fld_hardware_active INTEGER DEFAULT 0,
    fld_software_active INTEGER DEFAULT 0,
    fld_rcm_active INTEGER DEFAULT 0,
    fld_testing_active INTEGER DEFAULT 0,
    fld_incident_active INTEGER DEFAULT 0,
    fld_survival_active INTEGER DEFAULT 0,
    fld_vandv_active INTEGER DEFAULT 0,
    fld_hazard_active INTEGER DEFAULT 0,
    fld_stakeholder_active INTEGER DEFAULT 0,
    fld_allocation_active INTEGER DEFAULT 0,
    fld_similar_item_active INTEGER DEFAULT 0,
    fld_fmea_active INTEGER DEFAULT 0,
    fld_pof_active INTEGER DEFAULT 0,
    fld_rbd_active INTEGER DEFAULT 0,
    fld_fta_active INTEGER DEFAULT 0,
    fld_created_on DATE DEFAULT CURRENT_DATE,
    fld_created_by VARCHAR(512) DEFAULT '',
    fld_last_saved_on DATE DEFAULT CURRENT_DATE,
    fld_last_saved_by VARCHAR(512) DEFAULT '',
    PRIMARY KEY (fld_revision_id)
);
INSERT INTO "ramstk_program_info" VALUES(1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,0,0,CURRENT_DATE,'',CURRENT_DATE,'');
CREATE TABLE ramstk_program_status (
    fld_revision_id INTEGER NOT NULL,
    fld_status_id INTEGER NOT NULL,
    fld_cost_remaining FLOAT DEFAULT 0.0,
    fld_date_status DATE DEFAULt CURRENT_DATE,
    fld_time_remaining FLOAT DEFAULT 0.0,
    PRIMARY KEY (fld_status_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id),
    UNIQUE (fld_date_status)
);

CREATE TABLE ramstk_function (
    fld_revision_id INTEGER NOT NULL,
    fld_function_id INTEGER NOT NULL,
    fld_availability_logistics FLOAT DEFAULT 0.0,
    fld_availability_mission FLOAT DEFAULT 0.0,
    fld_cost FLOAT DEFAULT 0.0,
    fld_function_code VARCHAR(16) DEFAULT '',
    fld_hazard_rate_logistics FLOAT DEFAULT 0.0,
    fld_hazard_rate_mission FLOAT DEFAULT 0.0,
    fld_level INTEGER DEFAULT 0,
    fld_mmt FLOAT DEFAULT 0.0,
    fld_mcmt FLOAT DEFAULT 0.0,
    fld_mpmt FLOAT DEFAULT 0.0,
    fld_mtbf_logistics FLOAT DEFAULT 0.0,
    fld_mtbf_mission FLOAT DEFAULT 0.0,
    fld_mttr FLOAT DEFAULT 0.0,
    fld_name VARCHAR(256) DEFAULT '',
    fld_parent_id INTEGER DEFAULT 0,
    fld_remarks VARCHAR DEFAULT '',
    fld_safety_critical INTEGER DEFAULT 0,
    fld_total_mode_count INTEGER DEFAULT 0,
    fld_total_part_count INTEGER DEFAULT 0,
    fld_type_id INTEGER DEFAULT 0,
    PRIMARY KEY (fld_function_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE
);
CREATE TABLE ramstk_failure_definition (
    fld_revision_id INTEGER NOT NULL,
    fld_function_id INTEGER NOT NULL,
    fld_definition_id INTEGER NOT NULL,
    fld_definition VARCHAR(1024) DEFAULT '',
    PRIMARY KEY (fld_definition_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE,
    FOREIGN KEY(fld_function_id) REFERENCES ramstk_function (fld_function_id) ON DELETE CASCADE
);
CREATE TABLE ramstk_hazard_analysis (
    fld_revision_id INTEGER NOT NULL,
    fld_function_id INTEGER NOT NULL,
    fld_hazard_id INTEGER NOT NULL,
    fld_potential_hazard VARCHAR(256) DEFAULT '',
    fld_potential_cause VARCHAR(512) DEFAULT '',
    fld_assembly_effect VARCHAR(512) DEFAULT '',
    fld_assembly_severity VARCHAR(256) DEFAULT '',
    fld_assembly_probability VARCHAR(256) DEFAULT '',
    fld_assembly_hri INTEGER DEFAULT 0,
    fld_assembly_mitigation VARCHAR DEFAULT '',
    fld_assembly_severity_f VARCHAR(256) DEFAULT '',
    fld_assembly_probability_f VARCHAR(256) DEFAULT '',
    fld_assembly_hri_f INTEGER DEFAULT 0,
    fld_function_1 VARCHAR(128) DEFAULT '',
    fld_function_2 VARCHAR(128) DEFAULT '',
    fld_function_3 VARCHAR(128) DEFAULT '',
    fld_function_4 VARCHAR(128) DEFAULT '',
    fld_function_5 VARCHAR(128) DEFAULT '',
    fld_remarks VARCHAR DEFAULT '',
    fld_result_1 FLOAT DEFAULT 0.0,
    fld_result_2 FLOAT DEFAULT 0.0,
    fld_result_3 FLOAT DEFAULT 0.0,
    fld_result_4 FLOAT DEFAULT 0.0,
    fld_result_5 FLOAT DEFAULT 0.0,
    fld_system_effect VARCHAR(512) DEFAULT '',
    fld_system_severity VARCHAR(256) DEFAULT '',
    fld_system_probability VARCHAR(256) DEFAULT '',
    fld_system_hri INTEGER DEFAULT 0,
    fld_system_mitigation VARCHAR DEFAULT '',
    fld_system_severity_f VARCHAR(256) DEFAULT '',
    fld_system_probability_f VARCHAR(256) DEFAULT '',
    fld_system_hri_f INTEGER DEFAULT 0,
    fld_user_blob_1 VARCHAR DEFAULT '',
    fld_user_blob_2 VARCHAR DEFAULT '',
    fld_user_blob_3 VARCHAR DEFAULT '',
    fld_user_float_1 FLOAT DEFAULT 0.0,
    fld_user_float_2 FLOAT DEFAULT 0.0,
    fld_user_float_3 FLOAT DEFAULT 0.0,
    fld_user_int_1 INTEGER DEFAULT 0,
    fld_user_int_2 INTEGER DEFAULT 0,
    fld_user_int_3 INTEGER DEFAULT 0,
    PRIMARY KEY (fld_hazard_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE,
    FOREIGN KEY(fld_function_id) REFERENCES ramstk_function (fld_function_id) ON DELETE CASCADE
);

CREATE TABLE ramstk_requirement (
    fld_revision_id INTEGER NOT NULL,
    fld_requirement_id INTEGER NOT NULL,
    fld_derived INTEGER DEFAULT 0,
    fld_description VARCHAR DEFAULT '',
    fld_figure_number VARCHAR(256) DEFAULT '',
    fld_owner INTEGER DEFAULT 0,
    fld_page_number VARCHAR(256) DEFAULT '',
    fld_parent_id INTEGER DEFAULT 0,
    fld_priority INTEGER DEFAULT 0,
    fld_requirement_code VARCHAR(256) DEFAULT '',
    fld_specification VARCHAR(256) DEFAULT '',
    fld_requirement_type INTEGER DEFAULT 0,
    fld_validated INTEGER DEFAULT 0,
    fld_validated_date DATE,
    fld_clarity_0 INTEGER DEFAULT 0,
    fld_clarity_1 INTEGER DEFAULT 0,
    fld_clarity_2 INTEGER DEFAULT 0,
    fld_clarity_3 INTEGER DEFAULT 0,
    fld_clarity_4 INTEGER DEFAULT 0,
    fld_clarity_5 INTEGER DEFAULT 0,
    fld_clarity_6 INTEGER DEFAULT 0,
    fld_clarity_7 INTEGER DEFAULT 0,
    fld_clarity_8 INTEGER DEFAULT 0,
    fld_complete_0 INTEGER DEFAULT 0,
    fld_complete_1 INTEGER DEFAULT 0,
    fld_complete_2 INTEGER DEFAULT 0,
    fld_complete_3 INTEGER DEFAULT 0,
    fld_complete_4 INTEGER DEFAULT 0,
    fld_complete_5 INTEGER DEFAULT 0,
    fld_complete_6 INTEGER DEFAULT 0,
    fld_complete_7 INTEGER DEFAULT 0,
    fld_complete_8 INTEGER DEFAULT 0,
    fld_complete_9 INTEGER DEFAULT 0,
    fld_consistent_0 INTEGER DEFAULT 0,
    fld_consistent_1 INTEGER DEFAULT 0,
    fld_consistent_2 INTEGER DEFAULT 0,
    fld_consistent_3 INTEGER DEFAULT 0,
    fld_consistent_4 INTEGER DEFAULT 0,
    fld_consistent_5 INTEGER DEFAULT 0,
    fld_consistent_6 INTEGER DEFAULT 0,
    fld_consistent_7 INTEGER DEFAULT 0,
    fld_consistent_8 INTEGER DEFAULT 0,
    fld_verifiable_0 INTEGER DEFAULT 0,
    fld_verifiable_1 INTEGER DEFAULT 0,
    fld_verifiable_2 INTEGER DEFAULT 0,
    fld_verifiable_3 INTEGER DEFAULT 0,
    fld_verifiable_4 INTEGER DEFAULT 0,
    fld_verifiable_5 INTEGER DEFAULT 0,
    PRIMARY KEY (fld_requirement_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE
);
CREATE TABLE ramstk_stakeholder (
    fld_revision_id INTEGER NOT NULL,
    fld_stakeholder_id INTEGER NOT NULL,
    fld_customer_rank INTEGER DEFAULT 0,
    fld_description VARCHAR DEFAULT '',
    fld_group VARCHAR(128) DEFAULT '',
    fld_improvement FLOAT DEFAULT 0.0,
    fld_overall_weight FLOAT DEFAULT 0.0,
    fld_planned_rank INTEGER DEFAULT 0,
    fld_priority INTEGER DEFAULT 0,
    fld_requirement_id INTEGER DEFAULT 0,
    fld_stakeholder VARCHAR(128) DEFAULT '',
    fld_user_float_1 FLOAT DEFAULT 0.0,
    fld_user_float_2 FLOAT DEFAULT 0.0,
    fld_user_float_3 FLOAT DEFAULT 0.0,
    fld_user_float_4 FLOAT DEFAULT 0.0,
    fld_user_float_5 FLOAT DEFAULT 0.0,
    PRIMARY KEY (fld_stakeholder_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE
);

CREATE TABLE ramstk_hardware (
    fld_revision_id INTEGER NOT NULL,
    fld_hardware_id INTEGER NOT NULL,
    fld_alt_part_number VARCHAR(256) DEFAULT '',
    fld_attachments VARCHAR(512) DEFAULT '',
    fld_cage_code VARCHAR(256) DEFAULT '',
    fld_category_id INTEGER DEFAULT 0,
    fld_comp_ref_des VARCHAR(256) DEFAULT '',
    fld_cost FLOAT DEFAULT 0.0,
    fld_cost_failure FLOAT DEFAULT 0.0,
    fld_cost_hour FLOAT DEFAULT 0.0,
    fld_cost_type_id INTEGER DEFAULT 0,
    fld_description VARCHAR(512) DEFAULT '',
    fld_duty_cycle FLOAT DEFAULT 0.0,
    fld_figure_number VARCHAR(256) DEFAULT '',
    fld_lcn VARCHAR(256) DEFAULT '',
    fld_level INTEGER DEFAULT 0,
    fld_manufacturer_id INTEGER DEFAULT 0,
    fld_mission_time FLOAT DEFAULT 0.0,
    fld_name VARCHAR(256) DEFAULT '',
    fld_nsn VARCHAR(256) DEFAULT '',
    fld_page_number VARCHAR(256) DEFAULT '',
    fld_parent_id INTEGER DEFAULT 0,
    fld_part INTEGER DEFAULT 0,
    fld_part_number VARCHAR(256) DEFAULT '',
    fld_quantity INTEGER DEFAULT 0,
    fld_ref_des VARCHAR(256) DEFAULT '',
    fld_remarks VARCHAR DEFAULT '',
    fld_repairable INTEGER DEFAULT 0,
    fld_specification_number VARCHAR(256) DEFAULT '',
    fld_subcategory_id INTEGER DEFAULT 0,
    fld_tagged_part INTEGER DEFAULT 0,
    fld_total_cost FLOAT DEFAULT 0.0,
    fld_total_part_count INTEGER DEFAULT 0,
    fld_total_power_dissipation FLOAT DEFAULT 0.0,
    fld_year_of_manufacture INTEGER DEFAULT 0,
    PRIMARY KEY (fld_hardware_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_hardware" VALUES(1,1,'','','',0,'',0.0,0.0,0.0,0,'System',100.0,'','',0,0,0.0,'','','',0,0,'',1,'','',0,'',0,0,0.0,0,0.0,2019);
CREATE TABLE ramstk_allocation (
    fld_revision_id INTEGER NOT NULL,
    fld_hardware_id INTEGER NOT NULL,
    fld_availability_alloc FLOAT DEFAULT 0.0,
    fld_duty_cycle FLOAT DEFAULT 0.0,
    fld_env_factor INTEGER DEFAULT 0,
    fld_goal_measure_id INTEGER DEFAULT 0,
    fld_hazard_rate_alloc FLOAT DEFAULT 0.0,
    fld_hazard_rate_goal FLOAT DEFAULT 0.0,
    fld_included INTEGER DEFAULT 0,
    fld_int_factor INTEGER DEFAULT 0,
    fld_allocation_method_id INTEGER DEFAULT 0,
    fld_mission_time FLOAT DEFAULT 0.0,
    fld_mtbf_alloc FLOAT DEFAULT 0.0,
    fld_mtbf_goal FLOAT DEFAULT 0.0,
    fld_n_sub_systems INTEGER DEFAULT 0,
    fld_n_sub_elements INTEGER DEFAULT 0,
    fld_parent_id INTEGER DEFAULT 0,
    fld_percent_weight_factor FLOAT DEFAULT 0.0,
    fld_reliability_alloc FLOAT DEFAULT 0.0,
    fld_reliability_goal FLOAT DEFAULT 0.0,
    fld_op_time_factor INTEGER DEFAULT 0,
    fld_soa_factor INTEGER DEFAULT 0,
    fld_weight_factor INTEGER DEFAULT 0,
    PRIMARY KEY (fld_hardware_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE,
    FOREIGN KEY(fld_hardware_id) REFERENCES ramstk_hardware (fld_hardware_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_allocation" VALUES(1,1,0.0,100.0,1,0,0.0,0.0,1,1,1,1.0,0.0,0.0,0,0,0,0.0,0.0,0.0,1,1,0.0);
CREATE TABLE ramstk_design_electric (
    fld_revision_id INTEGER NOT NULL,
    fld_hardware_id INTEGER NOT NULL,
    fld_application_id INTEGER DEFAULT 0,
    fld_area FLOAT DEFAULT 0.0,
    fld_capacitance FLOAT DEFAULT 0.0,
    fld_configuration_id INTEGER DEFAULT 0,
    fld_construction_id INTEGER DEFAULT 0,
    fld_contact_form_id INTEGER DEFAULT 0,
    fld_contact_gauge INTEGER DEFAULT 0,
    fld_contact_rating_id INTEGER DEFAULT 0,
    fld_current_operating FLOAT DEFAULT 0.0,
    fld_current_rated FLOAT DEFAULT 0.0,
    fld_current_ratio FLOAT DEFAULT 0.0,
    fld_environment_active_id INTEGER DEFAULT 0,
    fld_environment_dormant_id INTEGER DEFAULT 0,
    fld_family_id INTEGER DEFAULT 0,
    fld_feature_size FLOAT DEFAULT 0.0,
    fld_frequency_operating FLOAT DEFAULT 0.0,
    fld_insert_id INTEGER DEFAULT 0,
    fld_insulation_id INTEGER DEFAULT 0,
    fld_manufacturing_id INTEGER DEFAULT 0,
    fld_matching_id INTEGER DEFAULT 0,
    fld_n_active_pins INTEGER DEFAULT 0,
    fld_n_circuit_planes INTEGER DEFAULT 0,
    fld_n_cycles FLOAT DEFAULT 0.0,
    fld_n_elements INTEGER DEFAULT 0,
    fld_n_hand_soldered INTEGER DEFAULT 0,
    fld_n_wave_soldered INTEGER DEFAULT 0,
    fld_operating_life FLOAT DEFAULT 0.0,
    fld_overstress INTEGER DEFAULT 0,
    fld_package_id INTEGER DEFAULT 0,
    fld_power_operating FLOAT DEFAULT 0.0,
    fld_power_rated FLOAT DEFAULT 0.0,
    fld_power_ratio FLOAT DEFAULT 0.0,
    fld_reason VARCHAR(1024) DEFAULT '',
    fld_resistance FLOAT DEFAULT 0.0,
    fld_specification_id INTEGER DEFAULT 0,
    fld_technology_id INTEGER DEFAULT 0,
    fld_temperature_active FLOAT DEFAULT 0.0,
    fld_temperature_case FLOAT DEFAULT 0.0,
    fld_temperature_dormant FLOAT DEFAULT 0.0,
    fld_temperature_hot_spot FLOAT DEFAULT 0.0,
    fld_temperature_junction FLOAT DEFAULT 0.0,
    fld_temperature_knee FLOAT DEFAULT 0.0,
    fld_temperature_rated_max FLOAT DEFAULT 0.0,
    fld_temperature_rated_min FLOAT DEFAULT 0.0,
    fld_temperature_rise FLOAT DEFAULT 0.0,
    fld_theta_jc FLOAT DEFAULT 0.0,
    fld_type_id INTEGER DEFAULT 0,
    fld_voltage_ac_operating FLOAT DEFAULT 0.0,
    fld_voltage_dc_operating FLOAT DEFAULT 0.0,
    fld_voltage_esd FLOAT DEFAULT 0.0,
    fld_voltage_rated FLOAT DEFAULT 0.0,
    fld_voltage_ratio FLOAT DEFAULT 0.0,
    fld_weight FLOAT DEFAULT 0.0,
    fld_years_in_production INTEGER DEFAULT 0,
    PRIMARY KEY (fld_hardware_id),
    FOREIGN KEY(fld_hardware_id) REFERENCES ramstk_hardware (fld_hardware_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_design_electric" VALUES(1,1,0,0.0,0.0,0,0,0,0,0,0.0,0.0,0.0,0,0,0,0.0,0.0,0,0,0,0,0,1,0,0,0,0,0.0,0,0,0.0,0.0,0.0,X'',0.0,0,0,35.0,0.0,25.0,0.0,0.0,25.0,0.0,0.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,1);
CREATE TABLE ramstk_design_mechanic (
    fld_revision_id INTEGER NOT NULL,
    fld_hardware_id INTEGER NOT NULL,
    fld_altitude_operating FLOAT DEFAULT 0.0,
    fld_application_id INTEGER DEFAULT 0,
    fld_balance_id INTEGER DEFAULT 0,
    fld_clearance FLOAT DEFAULT 0.0,
    fld_casing_id INTEGER DEFAULT 0,
    fld_contact_pressure FLOAT DEFAULT 0.0,
    fld_deflection FLOAT DEFAULT 0.0,
    fld_diameter_coil FLOAT DEFAULT 0.0,
    fld_diameter_inner FLOAT DEFAULT 0.0,
    fld_diameter_outer FLOAT DEFAULT 0.0,
    fld_diameter_wire FLOAT DEFAULT 0.0,
    fld_filter_size FLOAT DEFAULT 0.0,
    fld_flow_design FLOAT DEFAULT 0.0,
    fld_flow_operating FLOAT DEFAULT 0.0,
    fld_frequency_operating FLOAT DEFAULT 0.0,
    fld_friction FLOAT DEFAULT 0.0,
    fld_impact_id INTEGER DEFAULT 0,
    fld_leakage_allowable FLOAT DEFAULT 0.0,
    fld_length FLOAT DEFAULT 0.0,
    fld_length_compressed FLOAT DEFAULT 0.0,
    fld_length_relaxed FLOAT DEFAULT 0.0,
    fld_load_design FLOAT DEFAULT 0.0,
    fld_load_id INTEGER DEFAULT 0,
    fld_load_operating FLOAT DEFAULT 0.0,
    fld_lubrication_id INTEGER DEFAULT 0,
    fld_manufacturing_id INTEGER DEFAULT 0,
    fld_material_id INTEGER DEFAULT 0,
    fld_meyer_hardness FLOAT DEFAULT 0.0,
    fld_misalignment_angle FLOAT DEFAULT 0.0,
    fld_n_ten INTEGER DEFAULT 0,
    fld_n_cycles INTEGER DEFAULT 0,
    fld_n_elements INTEGER DEFAULT 0,
    fld_offset FLOAT DEFAULT 0.0,
    fld_particle_size FLOAT DEFAULT 0.0,
    fld_pressure_contact FLOAT DEFAULT 0.0,
    fld_pressure_delta FLOAT DEFAULT 0.0,
    fld_pressure_downstream FLOAT DEFAULT 0.0,
    fld_pressure_rated FLOAT DEFAULT 0.0,
    fld_pressure_upstream FLOAT DEFAULT 0.0,
    fld_rpm_design FLOAT DEFAULT 0.0,
    fld_rpm_operating FLOAT DEFAULT 0.0,
    fld_service_id INTEGER DEFAULT 0,
    fld_spring_index FLOAT DEFAULT 0.0,
    fld_surface_finish FLOAT DEFAULT 0.0,
    fld_technology_id INTEGER DEFAULT 0,
    fld_thickness FLOAT DEFAULT 0.0,
    fld_torque_id INTEGER DEFAULT 0,
    fld_type_id INTEGER DEFAULT 0,
    fld_viscosity_design FLOAT DEFAULT 0.0,
    fld_viscosity_dynamic FLOAT DEFAULT 0.0,
    fld_water_per_cent FLOAT DEFAULT 0.0,
    fld_width_minimum FLOAT DEFAULT 0.0,
    PRIMARY KEY (fld_hardware_id),
    FOREIGN KEY(fld_hardware_id) REFERENCES ramstk_hardware (fld_hardware_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_design_mechanic" VALUES(1,1,0.0,0,0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0,0.0,0,0,0,0.0,0.0,0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0.0,0.0,0,0.0,0,0,0.0,0.0,0.0,0.0);
CREATE TABLE ramstk_mil_hdbk_f (
    fld_revision_id INTEGER NOT NULL,
    fld_hardware_id INTEGER NOT NULL,
    fld_a_one FLOAT DEFAULT 0.0,
    fld_a_two FLOAT DEFAULT 0.0,
    fld_b_one FLOAT DEFAULT 0.0,
    fld_b_two FLOAT DEFAULT 0.0,
    fld_c_one FLOAT DEFAULT 0.0,
    fld_c_two FLOAT DEFAULT 0.0,
    fld_lambda_bd FLOAT DEFAULT 0.0,
    fld_lambda_bp FLOAT DEFAULT 0.0,
    fld_lambda_cyc FLOAT DEFAULT 0.0,
    fld_lambda_eos FLOAT DEFAULT 0.0,
    fld_pi_a FLOAT DEFAULT 0.0,
    fld_pi_c FLOAT DEFAULT 0.0,
    fld_pi_cd FLOAT DEFAULT 0.0,
    fld_pi_cf FLOAT DEFAULT 0.0,
    fld_pi_cr FLOAT DEFAULT 0.0,
    fld_pi_cv FLOAT DEFAULT 0.0,
    fld_pi_cyc FLOAT DEFAULT 0.0,
    fld_pi_e FLOAT DEFAULT 0.0,
    fld_pi_f FLOAT DEFAULT 0.0,
    fld_pi_i FLOAT DEFAULT 0.0,
    fld_pi_k FLOAT DEFAULT 0.0,
    fld_pi_l FLOAT DEFAULT 0.0,
    fld_pi_m FLOAT DEFAULT 0.0,
    fld_pi_mfg FLOAT DEFAULT 0.0,
    fld_pi_n FLOAT DEFAULT 0.0,
    fld_pi_nr FLOAT DEFAULT 0.0,
    fld_pi_p FLOAT DEFAULT 0.0,
    fld_pi_pt FLOAT DEFAULT 0.0,
    fld_pi_q FLOAT DEFAULT 0.0,
    fld_pi_r FLOAT DEFAULT 0.0,
    fld_pi_s FLOAT DEFAULT 0.0,
    fld_pi_t FLOAT DEFAULT 0.0,
    fld_pi_taps FLOAT DEFAULT 0.0,
    fld_pi_u FLOAT DEFAULT 0.0,
    fld_pi_v FLOAT DEFAULT 0.0,
    PRIMARY KEY (fld_hardware_id),
    FOREIGN KEY(fld_hardware_id) REFERENCES ramstk_hardware (fld_hardware_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_mil_hdbk_f" VALUES(1,1,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0);
CREATE TABLE ramstk_nswc (
    fld_revision_id INTEGER NOT NULL,
    fld_hardware_id INTEGER NOT NULL,
    fld_c_ac FLOAT DEFAULT 0.0,
    fld_c_alt FLOAT DEFAULT 0.0,
    fld_c_b FLOAT DEFAULT 0.0,
    fld_c_bl FLOAT DEFAULT 0.0,
    fld_c_bt FLOAT DEFAULT 0.0,
    fld_c_bv FLOAT DEFAULT 0.0,
    fld_c_c FLOAT DEFAULT 0.0,
    fld_c_cf FLOAT DEFAULT 0.0,
    fld_c_cp FLOAT DEFAULT 0.0,
    fld_c_cs FLOAT DEFAULT 0.0,
    fld_c_cv FLOAT DEFAULT 0.0,
    fld_c_cw FLOAT DEFAULT 0.0,
    fld_c_d FLOAT DEFAULT 0.0,
    fld_c_dc FLOAT DEFAULT 0.0,
    fld_c_dl FLOAT DEFAULT 0.0,
    fld_c_dp FLOAT DEFAULT 0.0,
    fld_c_ds FLOAT DEFAULT 0.0,
    fld_c_dt FLOAT DEFAULT 0.0,
    fld_c_dw FLOAT DEFAULT 0.0,
    fld_c_dy FLOAT DEFAULT 0.0,
    fld_c_e FLOAT DEFAULT 0.0,
    fld_c_f FLOAT DEFAULT 0.0,
    fld_c_g FLOAT DEFAULT 0.0,
    fld_c_ga FLOAT DEFAULT 0.0,
    fld_c_gl FLOAT DEFAULT 0.0,
    fld_c_gp FLOAT DEFAULT 0.0,
    fld_c_gs FLOAT DEFAULT 0.0,
    fld_c_gt FLOAT DEFAULT 0.0,
    fld_c_gv FLOAT DEFAULT 0.0,
    fld_c_h FLOAT DEFAULT 0.0,
    fld_c_i FLOAT DEFAULT 0.0,
    fld_c_k FLOAT DEFAULT 0.0,
    fld_c_l FLOAT DEFAULT 0.0,
    fld_c_lc FLOAT DEFAULT 0.0,
    fld_c_m FLOAT DEFAULT 0.0,
    fld_c_mu FLOAT DEFAULT 0.0,
    fld_c_n FLOAT DEFAULT 0.0,
    fld_c_np FLOAT DEFAULT 0.0,
    fld_c_nw FLOAT DEFAULT 0.0,
    fld_c_p FLOAT DEFAULT 0.0,
    fld_c_pd FLOAT DEFAULT 0.0,
    fld_c_pf FLOAT DEFAULT 0.0,
    fld_c_pv FLOAT DEFAULT 0.0,
    fld_c_q FLOAT DEFAULT 0.0,
    fld_c_r FLOAT DEFAULT 0.0,
    fld_c_rd FLOAT DEFAULT 0.0,
    fld_c_s FLOAT DEFAULT 0.0,
    fld_c_sc FLOAT DEFAULT 0.0,
    fld_c_sf FLOAT DEFAULT 0.0,
    fld_c_st FLOAT DEFAULT 0.0,
    fld_c_sv FLOAT DEFAULT 0.0,
    fld_c_sw FLOAT DEFAULT 0.0,
    fld_c_sz FLOAT DEFAULT 0.0,
    fld_c_t FLOAT DEFAULT 0.0,
    fld_c_v FLOAT DEFAULT 0.0,
    fld_c_w FLOAT DEFAULT 0.0,
    fld_c_y FLOAT DEFAULT 0.0,
    PRIMARY KEY (fld_hardware_id),
    FOREIGN KEY(fld_hardware_id) REFERENCES ramstk_hardware (fld_hardware_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_nswc" VALUES(1,1,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0);
CREATE TABLE ramstk_reliability (
    fld_revision_id INTEGER NOT NULL,
    fld_hardware_id INTEGER NOT NULL,
    fld_add_adj_factor FLOAT DEFAULT 0.0,
    fld_availability_logistics FLOAT DEFAULT 0.0,
    fld_availability_mission FLOAT DEFAULT 0.0,
    fld_avail_log_variance FLOAT DEFAULT 0.0,
    fld_avail_mis_variance FLOAT DEFAULT 0.0,
    fld_failure_distribution_id INTEGER DEFAULT 0,
    fld_hazard_rate_active FLOAT DEFAULT 0.0,
    fld_hazard_rate_dormant FLOAT DEFAULT 0.0,
    fld_hazard_rate_logistics FLOAT DEFAULT 0.0,
    fld_hazard_rate_method_id INTEGER DEFAULT 0,
    fld_hazard_rate_mission FLOAT DEFAULT 0.0,
    fld_hazard_rate_model VARCHAR(512) DEFAULT '',
    fld_hazard_rate_percent FLOAT DEFAULT 0.0,
    fld_hazard_rate_software FLOAT DEFAULT 0.0,
    fld_hazard_rate_specified FLOAT DEFAULT 0.0,
    fld_hazard_rate_type_id INTEGER DEFAULT 0,
    fld_hr_active_variance FLOAT DEFAULT 0.0,
    fld_hr_dormant_variance FLOAT DEFAULT 0.0,
    fld_hr_log_variance FLOAT DEFAULT 0.0,
    fld_hr_mis_variance FLOAT DEFAULT 0.0,
    fld_hr_spec_variance FLOAT DEFAULT 0.0,
    fld_lambda_b FLOAT DEFAULT 0.0,
    fld_location_parameter FLOAT DEFAULT 0.0,
    fld_mtbf_logistics FLOAT DEFAULT 0.0,
    fld_mtbf_mission FLOAT DEFAULT 0.0,
    fld_mtbf_specified FLOAT DEFAULT 0.0,
    fld_mtbf_log_variance FLOAT DEFAULT 0.0,
    fld_mtbf_mis_variance FLOAT DEFAULT 0.0,
    fld_mtbf_spec_variance FLOAT DEFAULT 0.0,
    fld_mult_adj_factor FLOAT DEFAULT 0.0,
    fld_quality_id INTEGER DEFAULT 0,
    fld_reliability_goal FLOAT DEFAULT 0.0,
    fld_reliability_goal_measure_id INTEGER DEFAULT 0,
    fld_reliability_logistics FLOAT DEFAULT 0.0,
    fld_reliability_mission FLOAT DEFAULT 0.0,
    fld_reliability_log_variance FLOAT DEFAULT 0.0,
    fld_reliability_mis_variance FLOAT DEFAULT 0.0,
    fld_scale_parameter FLOAT DEFAULT 0.0,
    fld_shape_parameter FLOAT DEFAULT 0.0,
    fld_survival_analysis_id INTEGER DEFAULT 0,
    PRIMARY KEY (fld_hardware_id),
    FOREIGN KEY(fld_hardware_id) REFERENCES ramstk_hardware (fld_hardware_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_reliability" VALUES(1,1,0.0,1.0,1.0,0.0,0.0,0,0.0,0.0,0.0,0,0.0,'',0.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0,0.0,0,1.0,1.0,0.0,0.0,0.0,0.0,0);
CREATE TABLE ramstk_similar_item (
    fld_revision_id INTEGER NOT NULL,
    fld_hardware_id INTEGER NOT NULL,
    fld_change_description_1 VARCHAR DEFAULT '',
    fld_change_description_2 VARCHAR DEFAULT '',
    fld_change_description_3 VARCHAR DEFAULT '',
    fld_change_description_4 VARCHAR DEFAULT '',
    fld_change_description_5 VARCHAR DEFAULT '',
    fld_change_description_6 VARCHAR DEFAULT '',
    fld_change_description_7 VARCHAR DEFAULT '',
    fld_change_description_8 VARCHAR DEFAULT '',
    fld_change_description_9 VARCHAR DEFAULT '',
    fld_change_description_10 VARCHAR DEFAULT '',
    fld_change_factor_1 FLOAT DEFAULT 0.0,
    fld_change_factor_2 FLOAT DEFAULT 0.0,
    fld_change_factor_3 FLOAT DEFAULT 0.0,
    fld_change_factor_4 FLOAT DEFAULT 0.0,
    fld_change_factor_5 FLOAT DEFAULT 0.0,
    fld_change_factor_6 FLOAT DEFAULT 0.0,
    fld_change_factor_7 FLOAT DEFAULT 0.0,
    fld_change_factor_8 FLOAT DEFAULT 0.0,
    fld_change_factor_9 FLOAT DEFAULT 0.0,
    fld_change_factor_10 FLOAT DEFAULT 0.0,
    fld_environment_from_id INTEGER DEFAULT 0,
    fld_environment_to_id INTEGER DEFAULT 0,
    fld_function_1 VARCHAR(128) DEFAULT '',
    fld_function_2 VARCHAR(128) DEFAULT '',
    fld_function_3 VARCHAR(128) DEFAULT '',
    fld_function_4 VARCHAR(128) DEFAULT '',
    fld_function_5 VARCHAR(128) DEFAULT '',
    fld_similar_item_method_id INTEGER DEFAULT 0,
    fld_parent_id INTEGER DEFAULT 0,
    fld_quality_from_id INTEGER DEFAULT 0,
    fld_quality_to_id INTEGER DEFAULT 0,
    fld_result_1 FLOAT DEFAULT 0.0,
    fld_result_2 FLOAT DEFAULT 0.0,
    fld_result_3 FLOAT DEFAULT 0.0,
    fld_result_4 FLOAT DEFAULT 0.0,
    fld_result_5 FLOAT DEFAULT 0.0,
    fld_temperature_from FLOAT DEFAULT 0.0,
    fld_temperature_to FLOAT DEFAULT 0.0,
    fld_user_blob_1 VARCHAR DEFAULT '',
    fld_user_blob_2 VARCHAR DEFAULT '',
    fld_user_blob_3 VARCHAR DEFAULT '',
    fld_user_blob_4 VARCHAR DEFAULT '',
    fld_user_blob_5 VARCHAR DEFAULT '',
    fld_user_float_1 FLOAT DEFAULT 0.0,
    fld_user_float_2 FLOAT DEFAULT 0.0,
    fld_user_float_3 FLOAT DEFAULT 0.0,
    fld_user_float_4 FLOAT DEFAULT 0.0,
    fld_user_float_5 FLOAT DEFAULT 0.0,
    fld_user_int_1 INTEGER DEFAULT 0,
    fld_user_int_2 INTEGER DEFAULT 0,
    fld_user_int_3 INTEGER DEFAULT 0,
    fld_user_int_4 INTEGER DEFAULT 0,
    fld_user_int_5 INTEGER DEFAULT 0,
    PRIMARY KEY (fld_hardware_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE,
    FOREIGN KEY(fld_hardware_id) REFERENCES ramstk_hardware (fld_hardware_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_similar_item" VALUES(1,1,'','','','','','','','','','',0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0,'','','','','',0,0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,'','','','','',0.0,0.0,0.0,0.0,0.0,0,0,0,0,0);
CREATE TABLE ramstk_mode (
    fld_revision_id INTEGER NOT NULL,
    fld_hardware_id INTEGER NOT NULL,
    fld_mode_id INTEGER NOT NULL,
    fld_critical_item INTEGER DEFAULT 0,
    fld_description VARCHAR(512) DEFAULT '',
    fld_design_provisions VARCHAR DEFAULT '',
    fld_detection_method VARCHAR(512) DEFAULT '',
    fld_effect_end VARCHAR(512) DEFAULT '',
    fld_effect_local VARCHAR(512) DEFAULT '',
    fld_effect_next VARCHAR(512) DEFAULT '',
    fld_effect_probability FLOAT DEFAULT 0.0,
    fld_hazard_rate_source VARCHAR(512) DEFAULT '',
    fld_isolation_method VARCHAR(512) DEFAULT '',
    fld_mission VARCHAR(64) DEFAULT '',
    fld_mission_phase VARCHAR(64) DEFAULT '',
    fld_mode_criticality FLOAT DEFAULT 0.0,
    fld_mode_hazard_rate FLOAT DEFAULT 0.0,
    fld_mode_op_time FLOAT DEFAULT 0.0,
    fld_mode_probability VARCHAR(64) DEFAULT '',
    fld_mode_ratio FLOAT DEFAULT 0.0,
    fld_operator_actions VARCHAR DEFAULT '',
    fld_other_indications VARCHAR(512) DEFAULT '',
    fld_remarks VARCHAR DEFAULT '',
    fld_rpn_severity INTEGER DEFAULT 0,
    fld_rpn_severity_new INTEGER DEFAULT 0,
    fld_severity_class VARCHAR(64) DEFAULT '',
    fld_single_point INTEGER DEFAULT 0,
    fld_type_id INTEGER DEFAULT 0,
    PRIMARY KEY (fld_mode_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE,
    FOREIGN KEY(fld_hardware_id) REFERENCES ramstk_hardware (fld_hardware_id) ON DELETE CASCADE
);
CREATE TABLE ramstk_mechanism (
    fld_revision_id INTEGER NOT NULL,
    fld_hardware_id INTEGER NOT NULL,
    fld_mode_id INTEGER NOT NULL,
    fld_mechanism_id INTEGER NOT NULL,
    fld_description VARCHAR(512) DEFAULT '',
    fld_pof_include INTEGER DEFAULT 0,
    fld_rpn INTEGER DEFAULT 0,
    fld_rpn_detection INTEGER DEFAULT 0,
    fld_rpn_detection_new INTEGER DEFAULT 0,
    fld_rpn_new INTEGER DEFAULT 0,
    fld_rpn_occurrence INTEGER DEFAULT 0,
    fld_rpn_occurrence_new INTEGER DEFAULT 0,
    PRIMARY KEY (fld_mechanism_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE,
    FOREIGN KEY(fld_mode_id) REFERENCES ramstk_mode (fld_mode_id) ON DELETE CASCADE
);
CREATE TABLE ramstk_cause (
    fld_revision_id INTEGER NOT NULL,
    fld_hardware_id INTEGER NOT NULL,
    fld_mode_id INTEGER NOT NULL,
    fld_mechanism_id INTEGER NOT NULL,
    fld_cause_id INTEGER NOT NULL,
    fld_description VARCHAR(512) DEFAULT '',
    fld_rpn INTEGER DEFAULT 0,
    fld_rpn_detection INTEGER DEFAULT 0,
    fld_rpn_detection_new INTEGER DEFAULT 0,
    fld_rpn_new INTEGER DEFAULT 0,
    fld_rpn_occurrence INTEGER DEFAULT 0,
    fld_rpn_occurrence_new INTEGER DEFAULT 0,
    PRIMARY KEY (fld_cause_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE,
    FOREIGN KEY(fld_mode_id) REFERENCES ramstk_mode (fld_mode_id) ON DELETE CASCADE,
    FOREIGN KEY(fld_mechanism_id) REFERENCES ramstk_mechanism (fld_mechanism_id) ON DELETE CASCADE
);
CREATE TABLE ramstk_control (
    fld_revision_id INTEGER NOT NULL,
    fld_hardware_id INTEGER NOT NULL,
    fld_mode_id INTEGER NOT NULL,
    fld_mechanism_id INTEGER NOT NULL,
    fld_cause_id INTEGER NOT NULL,
    fld_control_id INTEGER NOT NULL,
    fld_description VARCHAR(512) DEFAULT '',
    fld_type_id VARCHAR(512) DEFAULT '',
    PRIMARY KEY (fld_control_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE,
    FOREIGN KEY(fld_cause_id) REFERENCES ramstk_cause (fld_cause_id) ON DELETE CASCADE
);
CREATE TABLE ramstk_action (
    fld_revision_id INTEGER NOT NULL,
    fld_hardware_id INTEGER NOT NULL,
    fld_mode_id INTEGER NOT NULL,
    fld_mechanism_id INTEGER NOT NULL,
    fld_cause_id INTEGER NOT NULL,
    fld_action_id INTEGER NOT NULL,
    fld_description VARCHAR DEFAULT '',
    fld_action_category VARCHAR(512) DEFAULT '',
    fld_action_owner VARCHAR(512) DEFAULT '',
    fld_action_due_date DATE DEFAULT CURRENT_DATE + INTERVAL '30 day',
    fld_action_status VARCHAR(512) DEFAULT '',
    fld_action_taken VARCHAR DEFAULT '',
    fld_action_approved INTEGER DEFAULT 0,
    fld_action_approve_date DATE,
    fld_action_closed INTEGER DEFAULT 0,
    fld_action_close_date DATE,
    PRIMARY KEY (fld_action_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE,
    FOREIGN KEY(fld_cause_id) REFERENCES ramstk_cause (fld_cause_id) ON DELETE CASCADE
);

CREATE TABLE ramstk_op_load (
    fld_revision_id INTEGER NOT NULL,
    fld_hardware_id INTEGER NOT NULL,
    fld_mode_id INTEGER NOT NULL,
    fld_mechanism_id INTEGER NOT NULL,
    fld_opload_id INTEGER NOT NULL,
    fld_description VARCHAR(512) DEFAULT '',
    fld_damage_model VARCHAR(512) DEFAULT '',
    fld_priority_id INTEGER DEFAULT 0,
    PRIMARY KEY (fld_opload_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE,
    FOREIGN KEY(fld_mechanism_id) REFERENCES ramstk_mechanism (fld_mechanism_id) ON DELETE CASCADE
);
CREATE TABLE ramstk_op_stress (
    fld_revision_id INTEGER NOT NULL,
    fld_hardware_id INTEGER NOT NULL,
    fld_mode_id INTEGER NOT NULL,
    fld_mechanism_id INTEGER NOT NULL,
    fld_opload_id INTEGER NOT NULL,
    fld_opstress_id INTEGER NOT NULL,
    fld_description VARCHAR(512) DEFAULT '',
    fld_load_history VARCHAR(512) DEFAULT '',
    fld_measurable_parameter VARCHAR(512) DEFAULT '',
    fld_remarks VARCHAR DEFAULT '',
    PRIMARY KEY (fld_opstress_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE,
    FOREIGN KEY(fld_opload_id) REFERENCES ramstk_op_load (fld_opload_id) ON DELETE CASCADE
);
CREATE TABLE ramstk_load_history (
    fld_load_history_id INTEGER NOT NULL,
    fld_description VARCHAR(512) DEFAULT '',
    PRIMARY KEY (fld_load_history_id)
);
CREATE TABLE ramstk_test_method (
    fld_revision_id INTEGER NOT NULL,
    fld_hardware_id INTEGER NOT NULL,
    fld_mode_id INTEGER NOT NULL,
    fld_mechanism_id INTEGER NOT NULL,
    fld_opload_id INTEGER NOT NULL,
    fld_test_method_id INTEGER NOT NULL,
    fld_description VARCHAR(512) DEFAULT '',
    fld_boundary_conditions VARCHAR(512) DEFAULT '',
    fld_remarks VARCHAR DEFAULT '',
    PRIMARY KEY (fld_test_method_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE,
    FOREIGN KEY(fld_opload_id) REFERENCES ramstk_op_load (fld_opload_id) ON DELETE CASCADE
);

CREATE TABLE ramstk_validation (
    fld_revision_id INTEGER NOT NULL,
    fld_validation_id INTEGER NOT NULL,
    fld_acceptable_maximum FLOAT DEFAULT 0.0,
    fld_acceptable_mean FLOAT DEFAULT 0.0,
    fld_acceptable_minimum FLOAT DEFAULT 0.0,
    fld_acceptable_variance FLOAT DEFAULT 0.0,
    fld_confidence FLOAT DEFAULT 0.0,
    fld_cost_average FLOAT DEFAULT 0.0,
    fld_cost_ll FLOAT DEFAULT 0.0,
    fld_cost_maximum FLOAT DEFAULT 0.0,
    fld_cost_mean FLOAT DEFAULT 0.0,
    fld_cost_minimum FLOAT DEFAULT 0.0,
    fld_cost_ul FLOAT DEFAULT 0.0,
    fld_cost_variance FLOAT DEFAULT 0.0,
    fld_date_end DATE,
    fld_date_start DATE DEFAULT CURRENT_DATE,
    fld_description VARCHAR DEFAULT '',
    fld_measurement_unit INTEGER DEFAULT 0,
    fld_name VARCHAR(256) DEFAULT '',
    fld_status FLOAT DEFAULT 0.0,
    fld_type INTEGER DEFAULT 0,
    fld_task_specification VARCHAR(512) DEFAULT '',
    fld_time_average FLOAT DEFAULT 0.0,
    fld_time_ll FLOAT DEFAULT 0.0,
    fld_time_maximum FLOAT DEFAULT 0.0,
    fld_time_mean FLOAT DEFAULT 0.0,
    fld_time_minimum FLOAT DEFAULT 0.0,
    fld_time_ul FLOAT DEFAULT 0.0,
    fld_time_variance FLOAT DEFAULT 0.0,
    PRIMARY KEY (fld_validation_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE
);

CREATE TABLE ramstk_matrix (
    fld_revision_id INTEGER NOT NULL,
	fld_matrix_id INTEGER NOT NULL,
	fld_description VARCHAR NOT NULL DEFAULT '',
	fld_column_id INTEGER NULL DEFAULT 0,
	fld_row_id INTEGER NULL DEFAULT 0,
	fld_correlation INTEGER NULL DEFAULT 0,
	PRIMARY KEY (fld_matrix_id),
	FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE
);

-- Future tables
CREATE TABLE ramstk_test (
    fld_revision_id INTEGER NOT NULL,
    fld_test_id INTEGER NOT NULL,
    fld_assess_model_id INTEGER DEFAULT 0,
    fld_attachment VARCHAR(512),
    fld_avg_fef FLOAT DEFAULT 0.0,
    fld_avg_growth FLOAT DEFAULT 0.0,
    fld_avg_ms FLOAT DEFAULT 0.0,
    fld_chi_square FLOAT DEFAULT 0.0,
    fld_confidence FLOAT DEFAULT 0.0,
    fld_consumer_risk FLOAT DEFAULT 0.0,
    fld_cramer_vonmises FLOAT DEFAULT 0.0,
    fld_cum_failures INTEGER DEFAULT 0,
    fld_cum_mean FLOAT DEFAULT 0.0,
    fld_cum_mean_ll FLOAT DEFAULT 0.0,
    fld_cum_mean_se FLOAT DEFAULT 0.0,
    fld_cum_mean_ul FLOAT DEFAULT 0.0,
    fld_cum_time FLOAT DEFAULT 0.0,
    fld_description VARCHAR DEFAULT '',
    fld_grouped INTEGER DEFAULT 0,
    fld_group_interval FLOAT DEFAULT 0.0,
    fld_inst_mean FLOAT DEFAULT 0.0,
    fld_inst_mean_ll FLOAT DEFAULT 0.0,
    fld_inst_mean_se FLOAT DEFAULT 0.0,
    fld_inst_mean_ul FLOAT DEFAULT 0.0,
    fld_mg FLOAT DEFAULT 0.0,
    fld_mgp FLOAT DEFAULT 0.0,
    fld_n_phases INTEGER DEFAULT 0,
    fld_name VARCHAR(512),
    fld_plan_model_id INTEGER DEFAULT 0,
    fld_prob FLOAT DEFAULT 0.0,
    fld_producer_risk FLOAT DEFAULT 0.0,
    fld_scale FLOAT DEFAULT 0.0,
    fld_scale_ll FLOAT DEFAULT 0.0,
    fld_scale_se FLOAT DEFAULT 0.0,
    fld_scale_ul FLOAT DEFAULT 0.0,
    fld_shape FLOAT DEFAULT 0.0,
    fld_shape_ll FLOAT DEFAULT 0.0,
    fld_shape_se FLOAT DEFAULT 0.0,
    fld_shape_ul FLOAT DEFAULT 0.0,
    fld_tr FLOAT DEFAULT 0.0,
    fld_ttt FLOAT DEFAULT 0.0,
    fld_ttff FLOAT DEFAULT 0.0,
    fld_type_id INTEGER DEFAULT 0,
    PRIMARY KEY (fld_test_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id)
);
CREATE TABLE ramstk_growth_test (
    fld_test_id INTEGER NOT NULL,
    fld_phase_id INTEGER NOT NULL,
    fld_i_mi FLOAT DEFAULT 0.0,
    fld_i_mf FLOAT DEFAULT 0.0,
    fld_i_ma FLOAT DEFAULT 0.0,
    fld_i_num_fails INTEGER DEFAULT 0,
    fld_p_growth_rate FLOAT DEFAULT 0.0,
    fld_p_ms FLOAT DEFAULT 0.0,
    fld_p_fef_avg FLOAT DEFAULT 0.0,
    fld_p_prob FLOAT DEFAULT 0.0,
    fld_p_mi FLOAT DEFAULT 0.0,
    fld_p_mf FLOAT DEFAULT 0.0,
    fld_p_ma FLOAT DEFAULT 0.0,
    fld_test_time FLOAT DEFAULT 0.0,
    fld_p_num_fails INTEGER DEFAULT 0,
    fld_p_start_date DATE,
    fld_p_end_date DATE,
    fld_p_weeks FLOAT DEFAULT 0.0,
    fld_test_units INTEGER DEFAULT 0,
    fld_p_tpu FLOAT DEFAULT 0.0,
    fld_p_tpupw FLOAT DEFAULT 0.0,
    fld_o_growth_rate FLOAT DEFAULT 0.0,
    fld_o_ms FLOAT DEFAULT 0.0,
    fld_o_fef_avg FLOAT DEFAULT 0.0,
    fld_o_mi FLOAT DEFAULT 0.0,
    fld_o_mf FLOAT DEFAULT 0.0,
    fld_o_ma FLOAT DEFAULT 0.0,
    fld_o_test_time FLOAT DEFAULT 0.0,
    fld_o_num_fails INTEGER DEFAULT 0,
    fld_o_ttff FLOAT DEFAULT 0.0,
    PRIMARY KEY (fld_phase_id),
    FOREIGN KEY(fld_test_id) REFERENCES ramstk_test (fld_test_id)
);

CREATE TABLE ramstk_incident (
    fld_revision_id INTEGER NOT NULL,
    fld_incident_id INTEGER NOT NULL,
    fld_accepted INTEGER DEFAULT 0,
    fld_approved INTEGER DEFAULT 0,
    fld_approved_by INTEGER DEFAULT 0,
    fld_analysis VARCHAR DEFAULT '',
    fld_category_id INTEGER DEFAULT 0,
    fld_chargeable INTEGER DEFAULT 0,
    fld_chargeable_1 INTEGER DEFAULT 0,
    fld_chargeable_2 INTEGER DEFAULT 0,
    fld_chargeable_3 INTEGER DEFAULT 0,
    fld_chargeable_4 INTEGER DEFAULT 0,
    fld_chargeable_5 INTEGER DEFAULT 0,
    fld_chargeable_6 INTEGER DEFAULT 0,
    fld_chargeable_7 INTEGER DEFAULT 0,
    fld_chargeable_8 INTEGER DEFAULT 0,
    fld_chargeable_9 INTEGER DEFAULT 0,
    fld_chargeable_10 INTEGER DEFAULT 0,
    fld_complete INTEGER DEFAULT 0,
    fld_complete_by INTEGER DEFAULT 0,
    fld_cost FLOAT DEFAULT 0.0,
    fld_criticality_id INTEGER DEFAULT 0,
    fld_date_approved DATE,
    fld_date_complete DATE,
    fld_date_requested DATE,
    fld_date_reviewed DATE,
    fld_description_long VARCHAR DEFAULT '',
    fld_description_short VARCHAR(512),
    fld_detection_method_id INTEGER DEFAULT 0,
    fld_execution_time FLOAT DEFAULT 0.0,
    fld_hardware_id INTEGER DEFAULT 0,
    fld_incident_age INTEGER DEFAULT 0,
    fld_life_cycle_id INTEGER DEFAULT 0,
    fld_relevant INTEGER DEFAULT 0,
    fld_relevant_1 INTEGER DEFAULT 0,
    fld_relevant_2 INTEGER DEFAULT 0,
    fld_relevant_3 INTEGER DEFAULT 0,
    fld_relevant_4 INTEGER DEFAULT 0,
    fld_relevant_5 INTEGER DEFAULT 0,
    fld_relevant_6 INTEGER DEFAULT 0,
    fld_relevant_7 INTEGER DEFAULT 0,
    fld_relevant_8 INTEGER DEFAULT 0,
    fld_relevant_9 INTEGER DEFAULT 0,
    fld_relevant_10 INTEGER DEFAULT 0,
    fld_relevant_11 INTEGER DEFAULT 0,
    fld_relevant_12 INTEGER DEFAULT 0,
    fld_relevant_13 INTEGER DEFAULT 0,
    fld_relevant_14 INTEGER DEFAULT 0,
    fld_relevant_15 INTEGER DEFAULT 0,
    fld_relevant_16 INTEGER DEFAULT 0,
    fld_relevant_17 INTEGER DEFAULT 0,
    fld_relevant_18 INTEGER DEFAULT 0,
    fld_relevant_19 INTEGER DEFAULT 0,
    fld_relevant_20 INTEGER DEFAULT 0,
    fld_remarks VARCHAR DEFAULT '',
    fld_request_by INTEGER DEFAULT 0,
    fld_reviewed INTEGER DEFAULT 0,
    fld_reviewed_by INTEGER DEFAULT 0,
    fld_software_id INTEGER DEFAULT 0,
    fld_status INTEGER DEFAULT 0,
    fld_test_case VARCHAR(512),
    fld_test_found VARCHAR(512),
    fld_type_id INTEGER DEFAULT 0,
    fld_unit VARCHAR(256),
    PRIMARY KEY (fld_incident_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id)
);
CREATE TABLE ramstk_incident_action (
    fld_incident_id INTEGER NOT NULL,
    fld_action_id INTEGER NOT NULL,
    fld_action_owner INTEGER DEFAULT 0,
    fld_action_prescribed VARCHAR DEFAULT '',
    fld_action_taken VARCHAR DEFAULT '',
    fld_approved INTEGER DEFAULT 0,
    fld_approved_by INTEGER DEFAULT 0,
    fld_approved_date DATE,
    fld_closed INTEGER DEFAULT 0,
    fld_closed_by INTEGER DEFAULT 0,
    fld_closed_date DATE,
    fld_due_date DATE,
    fld_status_id INTEGER DEFAULT 0,
    PRIMARY KEY (fld_action_id),
    FOREIGN KEY(fld_incident_id) REFERENCES ramstk_incident (fld_incident_id)
);
CREATE TABLE ramstk_incident_detail (
    fld_incident_id INTEGER NOT NULL,
    fld_hardware_id INTEGER DEFAULT 0,
    fld_age_at_incident FLOAT DEFAULT 0.0,
    fld_cnd_nff INTEGER DEFAULT 0,
    fld_failure INTEGER DEFAULT 0,
    fld_initial_installation INTEGER DEFAULT 0,
    fld_interval_censored INTEGER DEFAULT 0,
    fld_mode_type_id INTEGER DEFAULT 0,
    fld_occ_fault INTEGER DEFAULT 0,
    fld_suspension INTEGER DEFAULT 0,
    fld_ttf FLOAT DEFAULT 0.0,
    fld_use_cal_time INTEGER DEFAULT 0,
    fld_use_op_time INTEGER DEFAULT 0,
    PRIMARY KEY (fld_incident_id),
    FOREIGN KEY(fld_incident_id) REFERENCES ramstk_incident (fld_incident_id)
);

CREATE TABLE ramstk_software (
    fld_revision_id INTEGER NOT NULL,
    fld_software_id INTEGER NOT NULL,
    fld_a FLOAT DEFAULT 0.0,
    fld_aloc INTEGER DEFAULT 0,
    fld_am FLOAT DEFAULT 0.0,
    fld_application_id INTEGER DEFAULT 0,
    fld_ax INTEGER DEFAULT 0,
    fld_budget_test FLOAT DEFAULT 0.0,
    fld_budget_dev FLOAT DEFAULT 0.0,
    fld_bx INTEGER DEFAULT 0,
    fld_category_id INTEGER DEFAULT 0,
    fld_cb INTEGER DEFAULT 0,
    fld_cx INTEGER DEFAULT 0,
    fld_d FLOAT DEFAULT 0.0,
    fld_dc FLOAT DEFAULT 0.0,
    fld_dd INTEGER DEFAULT 0,
    fld_description VARCHAR(512),
    fld_development_id INTEGER DEFAULT 0,
    fld_dev_assess_type_id INTEGER DEFAULT 0,
    fld_df FLOAT DEFAULT 0.0,
    fld_do FLOAT DEFAULT 0.0,
    fld_dr FLOAT DEFAULT 0.0,
    fld_dr_eot INTEGER DEFAULT 0,
    fld_dr_test INTEGER DEFAULT 0,
    fld_e FLOAT DEFAULT 0.0,
    fld_ec FLOAT DEFAULT 0.0,
    fld_et FLOAT DEFAULT 0.0,
    fld_ev FLOAT DEFAULT 0.0,
    fld_ew FLOAT DEFAULT 0.0,
    fld_f FLOAT DEFAULT 0.0,
    fld_ft1 FLOAT DEFAULT 0.0,
    fld_ft2 FLOAT DEFAULT 0.0,
    fld_hloc INTEGER DEFAULT 0,
    fld_hours_dev FLOAT DEFAULT 0.0,
    fld_hours_test FLOAT DEFAULT 0.0,
    fld_level INTEGER DEFAULT 0,
    fld_loc INTEGER DEFAULT 0,
    fld_n_branches INTEGER DEFAULT 0,
    fld_n_branches_test INTEGER DEFAULT 0,
    fld_n_inputs INTEGER DEFAULT 0,
    fld_n_inputs_test INTEGER DEFAULT 0,
    fld_n_interfaces INTEGER DEFAULT 0,
    fld_n_interfaces_test INTEGER DEFAULT 0,
    fld_ncb INTEGER DEFAULT 0,
    fld_nm INTEGER DEFAULT 0,
    fld_nm_test INTEGER DEFAULT 0,
    fld_os FLOAT DEFAULT 0.0,
    fld_parent_id INTEGER DEFAULT 0,
    fld_phase_id INTEGER DEFAULT 0,
    fld_ren_avg FLOAT DEFAULT 0.0,
    fld_ren_eot FLOAT DEFAULT 0.0,
    fld_rpfom FLOAT DEFAULT 0.0,
    fld_s1 FLOAT DEFAULT 0.0,
    fld_s2 FLOAT DEFAULT 0.0,
    fld_sa FLOAT DEFAULT 0.0,
    fld_schedule_dev FLOAT DEFAULT 0.0,
    fld_schedule_test FLOAT DEFAULT 0.0,
    fld_sl FLOAT DEFAULT 0.0,
    fld_sm FLOAT DEFAULT 0.0,
    fld_sq FLOAT DEFAULT 0.0,
    fld_sr FLOAT DEFAULT 0.0,
    fld_st FLOAT DEFAULT 0.0,
    fld_sx FLOAT DEFAULT 0.0,
    fld_t FLOAT DEFAULT 0.0,
    fld_tc FLOAT DEFAULT 0.0,
    fld_tcl INTEGER DEFAULT 0,
    fld_te FLOAT DEFAULT 0.0,
    fld_test_approach INTEGER DEFAULT 0,
    fld_test_effort INTEGER DEFAULT 0,
    fld_test_path INTEGER DEFAULT 0,
    fld_test_time FLOAT DEFAULT 0.0,
    fld_test_time_eot FLOAT DEFAULT 0.0,
    fld_tm FLOAT DEFAULT 0.0,
    fld_um INTEGER DEFAULT 0,
    fld_wm INTEGER DEFAULT 0,
    fld_xm INTEGER DEFAULT 0,
    PRIMARY KEY (fld_software_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id)
);
CREATE TABLE ramstk_software_development (
    fld_software_id INTEGER NOT NULL,
    fld_question_id INTEGER NOT NULL,
    fld_answer INTEGER DEFAULT 0,
    PRIMARY KEY (fld_question_id),
    FOREIGN KEY(fld_software_id) REFERENCES ramstk_software (fld_software_id)
);
CREATE TABLE ramstk_software_review (
    fld_software_id INTEGER NOT NULL,
    fld_question_id INTEGER NOT NULL,
    fld_answer INTEGER DEFAULT 0,
    fld_value INTEGER DEFAULT 0,
    fld_type VARCHAR(256),
    PRIMARY KEY (fld_question_id),
    FOREIGN KEY(fld_software_id) REFERENCES ramstk_software (fld_software_id)
);
CREATE TABLE ramstk_software_test (
    fld_software_id INTEGER NOT NULL,
    fld_technique_id INTEGER NOT NULL,
    fld_recommended INTEGER DEFAULT 0,
    fld_used INTEGER DEFAULT 0,
    PRIMARY KEY (fld_technique_id),
    FOREIGN KEY(fld_software_id) REFERENCES ramstk_software (fld_software_id)
);
CREATE TABLE ramstk_survival (
    fld_revision_id INTEGER NOT NULL,
    fld_survival_id INTEGER NOT NULL,
    fld_hardware_id INTEGER DEFAULT 0,
    fld_description VARCHAR(512),
    fld_source_id INTEGER DEFAULT 0,
    fld_distribution_id INTEGER DEFAULT 0,
    fld_confidence FLOAT DEFAULT 0.0,
    fld_confidence_type_id INTEGER DEFAULT 0,
    fld_confidence_method_id INTEGER DEFAULT 0,
    fld_fit_method_id INTEGER DEFAULT 0,
    fld_rel_time FLOAT DEFAULT 0.0,
    fld_n_rel_points INTEGER DEFAULT 0,
    fld_n_suspensions INTEGER DEFAULT 0,
    fld_n_failures INTEGER DEFAULT 0,
    fld_scale_ll FLOAT DEFAULT 0.0,
    fld_scale FLOAT DEFAULT 0.0,
    fld_scale_ul FLOAT DEFAULT 0.0,
    fld_shape_ll FLOAT DEFAULT 0.0,
    fld_shape FLOAT DEFAULT 0.0,
    fld_shape_ul FLOAT DEFAULT 0.0,
    fld_location_ll FLOAT DEFAULT 0.0,
    fld_location FLOAT DEFAULT 0.0,
    fld_location_ul FLOAT DEFAULT 0.0,
    fld_variance_1 FLOAT DEFAULT 0.0,
    fld_variance_2 FLOAT DEFAULT 0.0,
    fld_variance_3 FLOAT DEFAULT 0.0,
    fld_covariance_1 FLOAT DEFAULT 0.0,
    fld_covariance_2 FLOAT DEFAULT 0.0,
    fld_covariance_3 FLOAT DEFAULT 0.0,
    fld_mhb FLOAT DEFAULT 0.0,
    fld_lp FLOAT DEFAULT 0.0,
    fld_lr FLOAT DEFAULT 0.0,
    fld_aic FLOAT DEFAULT 0.0,
    fld_bic FLOAT DEFAULT 0.0,
    fld_mle FLOAT DEFAULT 0.0,
    fld_start_time FLOAT DEFAULT 0.0,
    fld_start_date DATE,
    fld_end_date DATE,
    fld_nevada_chart INTEGER DEFAULT 0,
    PRIMARY KEY (fld_survival_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id)
);
CREATE TABLE ramstk_survival_data (
    fld_survival_id INTEGER NOT NULL,
    fld_record_id INTEGER NOT NULL,
    fld_name VARCHAR(512),
    fld_source_id INTEGER DEFAULT 0,
    fld_failure_date DATE,
    fld_left_interval FLOAT DEFAULT 0.0,
    fld_right_interval FLOAT DEFAULT 0.0,
    fld_status_id INTEGER DEFAULT 0,
    fld_quantity INTEGER DEFAULT 0,
    fld_tbf FLOAT DEFAULT 0.0,
    fld_mode_type_id INTEGER DEFAULT 0,
    fld_nevada_chart INTEGER DEFAULT 0,
    fld_ship_date DATE,
    fld_number_shipped INTEGER DEFAULT 0,
    fld_return_date DATE,
    fld_number_returned INTEGER DEFAULT 0,
    fld_user_float_1 FLOAT DEFAULT 0.0,
    fld_user_float_2 FLOAT DEFAULT 0.0,
    fld_user_float_3 FLOAT DEFAULT 0.0,
    fld_user_integer_1 INTEGER DEFAULT 0,
    fld_user_integer_2 INTEGER DEFAULT 0,
    fld_user_integer_3 INTEGER DEFAULT 0,
    fld_user_string_1 VARCHAR(512),
    fld_user_string_2 VARCHAR(512),
    fld_user_string_3 VARCHAR(512),
    PRIMARY KEY (fld_record_id),
    FOREIGN KEY(fld_survival_id) REFERENCES ramstk_survival (fld_survival_id)
);
CREATE TABLE ramstk_unit (
    fld_unit_id INTEGER NOT NULL,
    fld_code VARCHAR(256),
    fld_description VARCHAR(512),
    fld_type VARCHAR(256),
    PRIMARY KEY (fld_unit_id)
);

-- Create views
CREATE OR REPLACE VIEW public.ramstk_fmeca
AS SELECT md.fld_revision_id,
    md.fld_hardware_id,
    md.fld_mode_id,
    mc.fld_mechanism_id,
    cs.fld_cause_id,
    ct.fld_control_id,
    ac.fld_action_id,
    md.fld_description AS md_description,
    mc.fld_description AS mc_description,
    cs.fld_description AS cs_description,
    ct.fld_description AS ct_description,
    ac.fld_description AS ac_description,
    md.fld_mission,
    md.fld_mission_phase,
    md.fld_effect_local,
    md.fld_effect_next,
    md.fld_effect_end,
    md.fld_detection_method,
    md.fld_other_indications,
    md.fld_isolation_method,
    md.fld_design_provisions,
    md.fld_operator_actions,
    md.fld_severity_class,
    md.fld_hazard_rate_source,
    md.fld_mode_probability,
    md.fld_effect_probability,
    rt.fld_hazard_rate_active,
    md.fld_mode_ratio,
    md.fld_mode_hazard_rate,
    md.fld_mode_op_time,
    md.fld_mode_criticality,
    md.fld_type_id,
    md.fld_rpn_severity,
    mc.fld_rpn_occurrence,
    mc.fld_rpn_detection,
    mc.fld_rpn,
    ac.fld_action_category,
    ac.fld_action_owner,
    ac.fld_action_due_date,
    ac.fld_action_status,
    ac.fld_action_taken,
    ac.fld_action_approved,
    ac.fld_action_approve_date,
    ac.fld_action_closed,
    ac.fld_action_close_date,
    md.fld_rpn_severity_new,
    mc.fld_rpn_occurrence_new,
    mc.fld_rpn_detection_new,
    mc.fld_rpn_new,
    md.fld_critical_item,
    md.fld_single_point,
    mc.fld_pof_include,
    md.fld_remarks,
    hw.fld_description AS hw_description
   FROM ramstk_hardware hw
     JOIN ramstk_mode md ON md.fld_hardware_id = hw.fld_hardware_id
     JOIN ramstk_reliability rt ON rt.fld_hardware_id = hw.fld_hardware_id
     JOIN ramstk_mechanism mc ON mc.fld_mode_id = md.fld_mode_id
     JOIN ramstk_cause cs ON cs.fld_mechanism_id = mc.fld_mechanism_id
     JOIN ramstk_control ct ON ct.fld_cause_id = cs.fld_cause_id
     JOIN ramstk_action ac ON ac.fld_cause_id = cs.fld_cause_id
  WHERE hw.fld_revision_id = 1;

-- Create functions.
CREATE OR REPLACE FUNCTION public.insertallocationrecord()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
    IF NEW.fld_part = 0 THEN
        INSERT INTO ramstk_allocation(fld_revision_id,fld_hardware_id,fld_parent_id)
        VALUES(NEW.fld_revision_id, NEW.fld_hardware_id, NEW.fld_parent_id);
    END IF;

    RETURN NEW;

END;
$function$
;

CREATE OR REPLACE FUNCTION public.insertsimilaritemrecord()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
    IF NEW.fld_part = 0 THEN
        INSERT INTO ramstk_similar_item(fld_revision_id,fld_hardware_id,fld_parent_id)
        VALUES(NEW.fld_revision_id, NEW.fld_hardware_id, NEW.fld_parent_id);
    END IF;

    RETURN NEW;

END;
$function$
;

CREATE OR REPLACE FUNCTION public.insertdesignelectricrecord()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
    IF NEW.fld_part = 1 THEN
        INSERT INTO ramstk_design_electric(fld_revision_id,fld_hardware_id)
        VALUES(NEW.fld_revision_id, NEW.fld_hardware_id);
    END IF;

    RETURN NEW;

END;
$function$
;

CREATE OR REPLACE FUNCTION public.insertdesignmechanicrecord()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
    IF NEW.fld_part = 1 THEN
        INSERT INTO ramstk_design_mechanic(fld_revision_id,fld_hardware_id)
        VALUES(NEW.fld_revision_id, NEW.fld_hardware_id);
    END IF;

    RETURN NEW;

END;
$function$
;

CREATE OR REPLACE FUNCTION public.insertmilhdbk217frecord()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
    IF NEW.fld_part = 1 THEN
        INSERT INTO ramstk_mil_hdbk_f(fld_revision_id,fld_hardware_id)
        VALUES(NEW.fld_revision_id, NEW.fld_hardware_id);
    END IF;

    RETURN NEW;

END;
$function$
;

CREATE OR REPLACE FUNCTION public.insertnswcrecord()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
    IF NEW.fld_part = 1 THEN
        INSERT INTO ramstk_nswc(fld_revision_id,fld_hardware_id)
        VALUES(NEW.fld_revision_id, NEW.fld_hardware_id);
    END IF;

    RETURN NEW;

END;
$function$
;

CREATE OR REPLACE FUNCTION public.insertreliabilityrecord()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
    INSERT INTO ramstk_reliability(fld_revision_id,fld_hardware_id)
    VALUES(NEW.fld_revision_id, NEW.fld_hardware_id);
    RETURN NEW;

END;
$function$
;

-- Create triggers
create trigger insertallocationrecord after
insert
    on
    public.ramstk_hardware for each row execute procedure insertallocationrecord();

create trigger insertsimilaritemrecord after
insert
    on
    public.ramstk_hardware for each row execute procedure insertsimilaritemrecord();

create trigger insertdesignelectricrecord after
insert
    on
    public.ramstk_hardware for each row execute procedure insertdesignelectricrecord();

create trigger insertdesignmechanicrecord after
insert
    on
    public.ramstk_hardware for each row execute procedure insertdesignmechanicrecord();

create trigger insertmilhdbk217frecord after
insert
    on
    public.ramstk_hardware for each row execute procedure insertmilhdbk217frecord();

create trigger insertnswcrecord after
insert
    on
    public.ramstk_hardware for each row execute procedure insertnswcrecord();

create trigger insertreliabilityrecord after
insert
    on
    public.ramstk_hardware for each row execute procedure insertreliabilityrecord();
