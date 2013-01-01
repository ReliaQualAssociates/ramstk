PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

CREATE TABLE "tbl_actions" (
    "fld_incident_id" INTEGER NOT NULL,
    "fld_action_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_prescribed_action" BLOB,
    "fld_action_taken" BLOB,
    "fld_owner" INTEGER NOT NULL DEFAULT (0),
    "fld_due_date" datetime,
    "fld_status" INTEGER NOT NULL DEFAULT (0),
    "fld_approved_by" INTEGER NOT NULL DEFAULT (0),
    "fld_approved_date" datetime,
    "fld_approved" TINYINT,
    "fld_closed_by" INTEGER NOT NULL DEFAULT (0),
    "fld_closed_date" datetime,
    "fld_closed" TINYINT
);

CREATE TABLE "tbl_allocation" (
    "fld_revision_id" INTEGER NOT NULL,
    "fld_assembly_id" INTEGER NOT NULL,
    "fld_included" TINYINT(4) NOT NULL DEFAULT (1),
    "fld_n_sub_systems" INTEGER NOT NULL DEFAULT (1),
    "fld_n_sub_elements" INTEGER NOT NULL DEFAULT (1),
    "fld_weight_factor" REAL NOT NULL DEFAULT (1),
    "fld_percent_wt_factor" REAL NOT NULL DEFAULT (1),
    "fld_int_factor" INTEGER NOT NULL DEFAULT (1),
    "fld_soa_factor" INTEGER NOT NULL DEFAULT (1),
    "fld_op_time_factor" INTEGER NOT NULL DEFAULT (1),
    "fld_env_factor" INTEGER NOT NULL DEFAULT (1),
    "fld_availability_alloc" REAL NOT NULL DEFAULT (0),
    "fld_reliability_alloc" REAL NOT NULL DEFAULT (0),
    "fld_failure_rate_alloc" REAL NOT NULL DEFAULT (0),
    "fld_mtbf_alloc" REAL NOT NULL DEFAULT (0),
    PRIMARY KEY ("fld_revision_id","fld_assembly_id")
);

INSERT INTO "tbl_allocation" VALUES(0,0,1,1,1,1.0,1.0,1,1,1,1,0.0,0.0,0.0,0.0);

CREATE TABLE "tbl_anomaly_management" (
    "fld_software_id" INTEGER NOT NULL DEFAULT (0),
    "fld_phase_id" INTEGER NOT NULL DEFAULT (0),
    "fld_question_id" INTEGER NOT NULL DEFAULT (0),
    "fld_value" INTEGER DEFAULT (0),
    "fld_ratio" REAL DEFAULT (0),
    "fld_y" TINYINT DEFAULT (0),
    "fld_n" TINYINT DEFAULT (0),
    "fld_na" TINYINT DEFAULT (0),
    "fld_unk" TINYINT DEFAULT (0),
     PRIMARY KEY("fld_software_id", "fld_phase_id", "fld_question_id")
);

CREATE TABLE "tbl_dataset" (
    "fld_dataset_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_assembly_id" INTEGER DEFAULT(0),
    "fld_description" VARCHAR(512),
    "fld_type" INTEGER DEFAULT(0),
    "fld_distribution_id" INTEGER DEFAULT(0),
    "fld_scale" FLOAT DEFAULT(0),
    "fld_shape" FLOAT DEFAULT(0),
    "fld_location" FLOAT DEFAULT(0),
    "fld_variance_1" FLOAT DEFAULT(0),
    "fld_variance_2" FLOAT DEFAULT(0),
    "fld_variance_3" FLOAT DEFAULT(0),
    "fld_covariance_1" FLOAT DEFAULT(0),
    "fld_covariance_2" FLOAT DEFAULT(0),
    "fld_covariance_3" FLOAT DEFAULT(0),
    "fld_confidence" FLOAT DEFAULT(50),
    "fld_confidence_type" INTEGER DEFAULT(0)
);

CREATE TABLE "tbl_survival_data" (
    "fld_dataset_id" INTEGER NOT NULL DEFAULT(0),
    "fld_left_interval" FLOAT DEFAULT(0),
    "fld_right_interval" FLOAT DEFAULT(0),
    "fld_status" INTEGER DEFAULT(0),
    "fld_quantity" INTEGER DEFAULT(1),
    "fld_unit" VARCHAR(256),
    "fld_part_num" VARCHAR(128),
    "fld_market" VARCHAR(32),
    "fld_model" VARCHAR(32),
    "fld_tbf" FLOAT DEFAULT(0)
);

CREATE TABLE "tbl_fmeca" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT (0),
    "fld_assembly_id" INTEGER NOT NULL DEFAULT (0),
    "fld_mode_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_mode_description" VARCHAR(512),
    "fld_mission_phase" VARCHAR(64),
    "fld_local_effect" VARCHAR(512),
    "fld_next_effect" VARCHAR(512),
    "fld_end_effect" VARCHAR(512),
    "fld_detection_method" VARCHAR(512),
    "fld_other_indications" VARCHAR(512),
    "fld_isolation_method" VARCHAR(512),
    "fld_design_provisions" BLOB,
    "fld_operator_provisions" BLOB,
    "fld_severity_class" VARCHAR(64),
    "fld_hazard_rate_source" VARCHAR(64),
    "fld_effect_probability" REAL DEFAULT (1),
    "fld_mode_ratio" REAL DEFAULT (0),
    "fld_mode_failure_rate" REAL DEFAULT (0),
    "fld_mode_op_time" REAL DEFAULT (0),
    "fld_mode_criticality" REAL DEFAULT (0),
    "fld_rpn_severity" INTEGER,
    "fld_immediate_cause" VARCHAR(512),
    "fld_root_cause" VARCHAR(512),
    "fld_rpn_occurence" INTEGER,
    "fld_detection_control" BLOB,
    "fld_prevention_control" BLOB,
    "fld_rpn_detectability" INTEGER,
    "fld_rpn" INTEGER,
    "fld_recommended_action" BLOB,
    "fld_action_taken" BLOB,
    "fld_rpn_severity_new" INTEGER,
    "fld_rpn_occurrence_new" INTEGER,
    "fld_rpn_detectability_new" INTEGER,
    "fld_rpn_new" INTEGER,
    "fld_critical_item" TINYINT,
    "fld_single_point" TINYINT,
    "fld_remarks" BLOB
);

CREATE TABLE "tbl_functional_matrix" (
    "fld_assembly_id" INTEGER NOT NULL DEFAULT (0),
    "fld_function_id" INTEGER NOT NULL DEFAULT (0),
    "fld_revision_id" INTEGER NOT NULL DEFAULT (0),
    PRIMARY KEY ("fld_function_id","fld_assembly_id")
);

INSERT INTO "tbl_functional_matrix" VALUES(0,0,0);

CREATE TABLE "tbl_functions" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT (0),
    "fld_function_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_availability" FLOAT NOT NULL DEFAULT (1),
    "fld_availability_mission" FLOAT NOT NULL DEFAULT (1),
    "fld_code" VARCHAR(16) NOT NULL DEFAULT ('Function Code'),
    "fld_cost" FLOAT NOT NULL DEFAULT (0),
    "fld_failure_rate_mission" FLOAT NOT NULL DEFAULT (0),
    "fld_failure_rate_predicted" FLOAT NOT NULL DEFAULT (0),
    "fld_mmt" FLOAT NOT NULL DEFAULT (0),
    "fld_mcmt" FLOAT NOT NULL DEFAULT (0),
    "fld_mpmt" FLOAT NOT NULL DEFAULT (0),
    "fld_mtbf_mission" FLOAT NOT NULL DEFAULT (0),
    "fld_mtbf_predicted" FLOAT NOT NULL DEFAULT (0),
    "fld_mttr" FLOAT NOT NULL DEFAULT (0),
    "fld_name" VARCHAR(255) DEFAULT ('Function Name'),
    "fld_remarks" BLOB,
    "fld_total_mode_quantity" INTEGER NOT NULL DEFAULT (0),
    "fld_total_part_quantity" INTEGER NOT NULL DEFAULT (0),
    "fld_type" INTEGER NOT NULL DEFAULT (0),
    "fld_parent_id" VARCHAR(16) NOT NULL DEFAULT ('-'),
    "fld_level" INTEGER NOT NULL DEFAULT (0)
);
INSERT INTO "tbl_functions" VALUES(0,0,1.0,1.0,'UF-01',0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,'Unassigned to Function','',0,0,0,'-',0);

CREATE TABLE "tbl_incident" (
    "fld_revision_id" INTEGER DEFAULT (0),
    "fld_incident_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_incident_category" INTEGER NOT NULL DEFAULT(0),
    "fld_incident_type" INTEGER NOT NULL DEFAULT(0),
    "fld_short_description" VARCHAR(512),
    "fld_long_description" BLOB,
    "fld_criticality" INTEGER NOT NULL DEFAULT(1),
    "fld_detection_method" VARCHAR(256),
    "fld_remarks" BLOB,
    "fld_status" INTEGER NOT NULL DEFAULT(0),
    "fld_test_found" VARCHAR(512),
    "fld_test_case" VARCHAR(512),
    "fld_execution_time" FLOAT DEFAULT(0),
    "fld_unit" VARCHAR(256),
    "fld_cost" FLOAT DEFAULT(0),
    "fld_incident_age" INTEGER DEFAULT(0),
    "fld_hardware_id" INTEGER DEFAULT(-1),
    "fld_software_id" INTEGER DEFAULT(-1),
    "fld_request_by" VARCHAR(256),
    "fld_request_date" INTEGER,
    "fld_reviewed" TINYINT DEFAULT(0),
    "fld_reviewed_by" VARCHAR(256),
    "fld_reviewed_date" INTEGER,
    "fld_approved" TINYINT DEFAULT(0),
    "fld_approved_by" VARCHAR(256),
    "fld_approved_date" INTEGER,
    "fld_complete" TINYINT DEFAULT(0),
    "fld_complete_by" VARCHAR(256),
    "fld_complete_date" INTEGER,
    "fld_life_cycle" INTEGER DEFAULT(0),
    "fld_analysis" BLOB,
    "fld_accepted" TINYINT DEFAULT(0)
);

CREATE TABLE "tbl_incident_detail" (
    "fld_incident_id" VARCHAR(32) NOT NULL,
    "fld_part_num" VARCHAR(128) DEFAULT(''),
    "fld_age_at_incident" REAL DEFAULT (0),
    "fld_failure" INTEGER DEFAULT (0),
    "fld_suspension" INTEGER DEFAULT (0),
    "fld_cnd_nff" INTEGER DEFAULT (0),
    "fld_occ_fault" INTEGER DEFAULT (0),
    "fld_initial_installation" INTEGER DEFAULT (0),
    "fld_interval_censored" INTEGER DEFAULT (0),
    "fld_use_op_time" INTEGER DEFAULT (0),
    "fld_use_cal_time" INTEGER DEFAULT (0),
    "fld_ttf" REAL DEFAULT (0),
    "fld_relevant_1" TINYINT DEFAULT (0),
    "fld_relevant_2" TINYINT DEFAULT (0),
    "fld_relevant_3" TINYINT DEFAULT (0),
    "fld_relevant_4" TINYINT DEFAULT (0),
    "fld_relevant_5" TINYINT DEFAULT (0),
    "fld_relevant_6" TINYINT DEFAULT (0),
    "fld_relevant_7" TINYINT DEFAULT (0),
    "fld_relevant_8" TINYINT DEFAULT (0),
    "fld_relevant_9" TINYINT DEFAULT (0),
    "fld_relevant_10" TINYINT DEFAULT (0),
    "fld_relevant_11" TINYINT DEFAULT (0),
    "fld_relevant_12" TINYINT DEFAULT (0),
    "fld_relevant_13" TINYINT DEFAULT (0),
    "fld_relevant_14" TINYINT DEFAULT (0),
    "fld_relevant_15" TINYINT DEFAULT (0),
    "fld_relevant_16" TINYINT DEFAULT (0),
    "fld_relevant_17" TINYINT DEFAULT (0),
    "fld_relevant_18" TINYINT DEFAULT (0),
    "fld_relevant_19" TINYINT DEFAULT (0),
    "fld_relevant_20" TINYINT DEFAULT (0),
    "fld_relevant" TINYINT DEFAULT (0),
    "fld_chargeable_1" TINYINT DEFAULT (0),
    "fld_chargeable_2" TINYINT DEFAULT (0),
    "fld_chargeable_3" TINYINT DEFAULT (0),
    "fld_chargeable_4" TINYINT DEFAULT (0),
    "fld_chargeable_5" TINYINT DEFAULT (0),
    "fld_chargeable_6" TINYINT DEFAULT (0),
    "fld_chargeable_7" TINYINT DEFAULT (0),
    "fld_chargeable_8" TINYINT DEFAULT (0),
    "fld_chargeable_9" TINYINT DEFAULT (0),
    "fld_chargeable_10" TINYINT DEFAULT (0),
    "fld_chargeable" TINYINT DEFAULT (0),
    PRIMARY KEY ("fld_incident_id", "fld_part_num")
);

CREATE TABLE "tbl_mechanisms" (
    "fld_mode_id" INTEGER NOT NULL DEFAULT (0),
    "fld_mechanism_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_mechanism_description" VARCHAR(512),
    "fld_damaging_conditions" BLOB,
    "fld_damage_model" VARCHAR(256),
    "fld_primary_parameter" VARCHAR(256),
    "fld_secondary_parameter" VARCHAR(256),
    "fld_tertiary_parameter" VARCHAR(256),
    "fld_mean_load_history" VARCHAR(256),
    "fld_boundary_conditions" BLOB
);

CREATE TABLE "tbl_prediction" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT (0),
    "fld_assembly_id" INTEGER NOT NULL DEFAULT (0),
    "fld_function_id" INTEGER NOT NULL DEFAULT (0),
    "fld_a1" REAL NOT NULL DEFAULT (0),
    "fld_a2" REAL NOT NULL DEFAULT (0),
    "fld_application_id" INTEGER NOT NULL DEFAULT (0),
    "fld_burnin_temperature" REAL NOT NULL DEFAULT (30),
    "fld_burnin_time" REAL NOT NULL DEFAULT (0),
    "fld_c1" REAL NOT NULL DEFAULT (0),
    "fld_c2" REAL NOT NULL DEFAULT (0),
    "fld_c3" REAL NOT NULL DEFAULT (0),
    "fld_c4" REAL NOT NULL DEFAULT (0),
    "fld_c5" REAL NOT NULL DEFAULT (0),
    "fld_c6" REAL NOT NULL DEFAULT (0),
    "fld_c7" REAL NOT NULL DEFAULT (0),
    "fld_capacitance" REAL NOT NULL DEFAULT (0),
    "fld_construction_id" INTEGER NOT NULL DEFAULT (0),
    "fld_current_ratio" REAL NOT NULL DEFAULT (1),
    "fld_cycles_id" INTEGER NOT NULL DEFAULT (0),
    "fld_cycling_rate" REAL NOT NULL DEFAULT (0),
    "fld_devices_lab" INTEGER NOT NULL DEFAULT (0),
    "fld_die_area" REAL NOT NULL DEFAULT (0),
    "fld_ea" REAL NOT NULL DEFAULT (0),
    "fld_ecc_id" INTEGER NOT NULL DEFAULT (0),
    "fld_element_id" INTEGER NOT NULL DEFAULT (0),
    "fld_esd_voltage" REAL NOT NULL DEFAULT (0),
    "fld_failures_field" INTEGER NOT NULL DEFAULT (0),
    "fld_failures_lab" INTEGER NOT NULL DEFAULT (0),
    "fld_family_id" INTEGER NOT NULL DEFAULT (0),
    "fld_feature_size" REAL NOT NULL DEFAULT (1),
    "fld_func_id" INTEGER NOT NULL DEFAULT (0),
    "fld_i1" REAL NOT NULL DEFAULT (0),
    "fld_i2" REAL NOT NULL DEFAULT (0),
    "fld_i3" REAL NOT NULL DEFAULT (0),
    "fld_i4" REAL NOT NULL DEFAULT (0),
    "fld_i5" REAL NOT NULL DEFAULT (0),
    "fld_i6" REAL NOT NULL DEFAULT (0),
    "fld_initial_temperature" REAL NOT NULL DEFAULT (30),
    "fld_insulation_id" INTEGER NOT NULL DEFAULT (0),
    "fld_junction_temperature" REAL NOT NULL DEFAULT (30),
    "fld_k1" REAL NOT NULL DEFAULT (0),
    "fld_k2" REAL NOT NULL DEFAULT (0),
    "fld_k3" REAL NOT NULL DEFAULT (0),
    "fld_knee_temperature" REAL NOT NULL DEFAULT (0),
    "fld_l1" REAL NOT NULL DEFAULT (0),
    "fld_l2" REAL NOT NULL DEFAULT (0),
    "fld_lambda_b" REAL NOT NULL DEFAULT (0),
    "fld_lambda_b0" REAL NOT NULL DEFAULT (0),
    "fld_lambda_b1" REAL NOT NULL DEFAULT (0),
    "fld_lambda_b2" REAL NOT NULL DEFAULT (0),
    "fld_lambda_bd" REAL NOT NULL DEFAULT (0),
    "fld_lambda_eos" REAL NOT NULL DEFAULT (0),
    "fld_lambda_g" REAL NOT NULL DEFAULT (0),
    "fld_lambda_o" REAL NOT NULL DEFAULT (0),
    "fld_manufacturing_id" INTEGER NOT NULL DEFAULT (0),
    "fld_max_rated_temperature" REAL NOT NULL DEFAULT (0),
    "fld_min_rated_temperature" REAL NOT NULL DEFAULT (0),
    "fld_number_contacts" INTEGER NOT NULL DEFAULT (0),
    "fld_number_elements" INTEGER NOT NULL DEFAULT (0),
    "fld_number_hand" INTEGER NOT NULL DEFAULT (0),
    "fld_number_pins" INTEGER NOT NULL DEFAULT (0),
    "fld_number_wave" INTEGER NOT NULL DEFAULT (0),
    "fld_operating_current" REAL NOT NULL DEFAULT (0),
    "fld_operating_freq" REAL NOT NULL DEFAULT (0),
    "fld_operating_power" REAL NOT NULL DEFAULT (0),
    "fld_operating_time_field" REAL NOT NULL DEFAULT (0),
    "fld_operating_voltage" REAL NOT NULL DEFAULT (0),
    "fld_package_id" INTEGER NOT NULL DEFAULT (0),
    "fld_pi_a" REAL NOT NULL DEFAULT (1),
    "fld_pi_c" REAL NOT NULL DEFAULT (1),
    "fld_pi_cf" REAL NOT NULL DEFAULT (1),
    "fld_pi_cyc" REAL NOT NULL DEFAULT (1),
    "fld_pi_e" REAL NOT NULL DEFAULT (1),
    "fld_pi_ecc" REAL NOT NULL DEFAULT (1),
    "fld_pi_f" REAL NOT NULL DEFAULT (1),
    "fld_pi_k" REAL NOT NULL DEFAULT (1),
    "fld_pi_m" REAL NOT NULL DEFAULT (1),
    "fld_pi_mfg" REAL NOT NULL DEFAULT (1),
    "fld_pi_pt" REAL NOT NULL DEFAULT (1),
    "fld_pi_q" REAL NOT NULL DEFAULT (1),
    "fld_pi_r" REAL NOT NULL DEFAULT (1),
    "fld_pi_sr" REAL NOT NULL DEFAULT (1),
    "fld_pi_u" REAL NOT NULL DEFAULT (1),
    "fld_pi_v" REAL NOT NULL DEFAULT (1),
    "fld_power_ratio" REAL NOT NULL DEFAULT (1),
    "fld_quality_id" INTEGER NOT NULL DEFAULT (0),
    "fld_r1" REAL NOT NULL DEFAULT (0),
    "fld_r2" REAL NOT NULL DEFAULT (0),
    "fld_r3" REAL NOT NULL DEFAULT (0),
    "fld_r4" REAL NOT NULL DEFAULT (0),
    "fld_r5" REAL NOT NULL DEFAULT (0),
    "fld_r6" REAL NOT NULL DEFAULT (0),
    "fld_rated_current" REAL NOT NULL DEFAULT (1),
    "fld_rated_power" REAL NOT NULL DEFAULT (1),
    "fld_rated_voltage" REAL NOT NULL DEFAULT (1),
    "fld_resistance" REAL NOT NULL DEFAULT (1),
    "fld_resistance_id" INTEGER NOT NULL DEFAULT (0),
    "fld_s1" REAL NOT NULL DEFAULT (0),
    "fld_s2" REAL NOT NULL DEFAULT (0),
    "fld_s3" REAL NOT NULL DEFAULT (0),
    "fld_s4" REAL NOT NULL DEFAULT (0),
    "fld_specification_id" INTEGER NOT NULL DEFAULT (0),
    "fld_specsheet_id" INTEGER NOT NULL DEFAULT (0),
    "fld_tbase" REAL NOT NULL DEFAULT (0),
    "fld_technology_id" INTEGER NOT NULL DEFAULT (0),
    "fld_temperature" REAL NOT NULL DEFAULT (30),
    "fld_temperature_lab" REAL NOT NULL DEFAULT (30),
    "fld_temperature_rise" REAL NOT NULL DEFAULT (0),
    "fld_test_time_lab" REAL NOT NULL DEFAULT (0),
    "fld_thermal_resistance" REAL NOT NULL DEFAULT (0),
    "fld_tref" REAL NOT NULL DEFAULT (0),
    "fld_voltage_ratio" REAL NOT NULL DEFAULT (1),
    "fld_years" REAL NOT NULL DEFAULT (1),
    PRIMARY KEY ("fld_revision_id","fld_assembly_id"),
    CONSTRAINT "tbl_prediction_ibfk_2" FOREIGN KEY ("fld_assembly_id") REFERENCES "tbl_system" ("fld_assembly_id") ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE "tbl_program_info" (
    "fld_program_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_revision_prefix" VARCHAR(16) NOT NULL DEFAULT ('REVISION'),
    "fld_revision_next_id" INTEGER NOT NULL DEFAULT (1),
    "fld_function_prefix" VARCHAR(16) NOT NULL DEFAULT ('FUNCTION'),
    "fld_function_next_id" INTEGER NOT NULL DEFAULT (1),
    "fld_assembly_prefix" VARCHAR(16) NOT NULL DEFAULT ('ASSEMBLY'),
    "fld_assembly_next_id" INTEGER NOT NULL DEFAULT (1),
    "fld_part_prefix" VARCHAR(16) NOT NULL DEFAULT ('PART'),
    "fld_part_next_id" INTEGER NOT NULL DEFAULT (1),
    "fld_fmeca_prefix" VARCHAR(16) NOT NULL DEFAULT ('FMEA'),
    "fld_fmeca_next_id" INTEGER NOT NULL DEFAULT (1),
    "fld_mode_prefix" VARCHAR(16) NOT NULL DEFAULT ('MODE'),
    "fld_mode_next_id" INTEGER NOT NULL DEFAULT (1),
    "fld_effect_prefix" VARCHAR(16) NOT NULL DEFAULT ('EFFECT'),
    "fld_effect_next_id" INTEGER NOT NULL DEFAULT (1),
    "fld_cause_prefix" VARCHAR(16) NOT NULL DEFAULT ('CAUSE'),
    "fld_cause_next_id" INTEGER NOT NULL DEFAULT (1),
    "fld_software_prefix" VARCHAR(16) NOT NULL DEFAULT ('MODULE'),
    "fld_software_next_id" INTEGER NOT NULL DEFAULT (1),
    "fld_revision_active" TINYINT NOT NULL DEFAULT (1),
    "fld_requirement_active" TINYINT NOT NULL DEFAULT (1),
    "fld_function_active" TINYINT NOT NULL DEFAULT (1),
    "fld_hardware_active" TINYINT NOT NULL DEFAULT (1),
    "fld_software_active" TINYINT NOT NULL DEFAULT (1),
    "fld_vandv_active" TINYINT NOT NULL DEFAULT (1),
    "fld_testing_active" TINYINT NOT NULL DEFAULT (1),
    "fld_rcm_active" TINYINT NOT NULL DEFAULT (1),
    "fld_fraca_active" TINYINT NOT NULL DEFAULT (1),
    "fld_fmeca_active" TINYINT NOT NULL DEFAULT (1),
    "fld_maintainability_active" TINYINT NOT NULL DEFAULT (1),
    "fld_rbd_active" TINYINT NOT NULL DEFAULT (1),
    "fld_fta_active" TINYINT NOT NULL DEFAULT (1),
    "fld_created_on" datetime DEFAULT NULL,
    "fld_created_by" VARCHAR(45) DEFAULT (''),
    "fld_last_saved" datetime DEFAULT NULL,
    "fld_last_saved_by" VARCHAR(45) DEFAULT ('')
);
INSERT INTO "tbl_program_info" VALUES(0,'REVISION',1,'FUNCTION',1,'ASSEMBLY',1,'PART',1,'FMEA',1,'MODE',1,'EFFECT',1,'CAUSE',1,'MODULE',1,1,1,1,1,1,1,0,0,1,1,1,1,1,'0000-00-00 00:00:00','',NULL,NULL);

CREATE TABLE "tbl_requirements" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT (0),
    "fld_requirement_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_assembly_id" INTEGER NOT NULL DEFAULT (0),
    "fld_requirement_desc" BLOB,
    "fld_requirement_type" INTEGER NOT NULL DEFAULT (0),
    "fld_requirement_code" VARCHAR(16) DEFAULT NULL,
    "fld_derived" TINYINT DEFAULT (0),
    "fld_parent_requirement" VARCHAR(45) NOT NULL DEFAULT ('-'),
    "fld_validated" TINYINT DEFAULT (0),
    "fld_validated_date" VARCHAR(45) DEFAULT NULL,
    "fld_owner" VARCHAR(64) DEFAULT NULL,
    "fld_specification" VARCHAR(128) DEFAULT NULL,
    "fld_page_number" VARCHAR(32) DEFAULT NULL,
    "fld_figure_number" VARCHAR(32) DEFAULT NULL,
    "fld_parent_id" INTEGER DEFAULT (0),
    "fld_software_id" INTEGER DEFAULT (0)
);

CREATE TABLE "tbl_revisions" (
    "fld_revision_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_availability" REAL NOT NULL DEFAULT (1),
    "fld_availability_mission" REAL NOT NULL DEFAULT (1),
    "fld_cost" REAL NOT NULL DEFAULT (0),
    "fld_cost_failure" REAL NOT NULL DEFAULT (0),
    "fld_cost_hour" REAL NOT NULL DEFAULT (0),
    "fld_failure_rate_active" REAL NOT NULL DEFAULT (0),
    "fld_failure_rate_dormant" REAL NOT NULL DEFAULT (0),
    "fld_failure_rate_mission" REAL NOT NULL DEFAULT (0),
    "fld_failure_rate_predicted" REAL NOT NULL DEFAULT (0),
    "fld_failure_rate_software" REAL NOT NULL DEFAULT (0),
    "fld_mmt" REAL NOT NULL DEFAULT (0),
    "fld_mcmt" REAL NOT NULL DEFAULT (0),
    "fld_mpmt" REAL NOT NULL DEFAULT (0),
    "fld_mtbf_mission" REAL NOT NULL DEFAULT (0),
    "fld_mtbf_predicted" REAL NOT NULL DEFAULT (0),
    "fld_mttr" REAL NOT NULL DEFAULT (0),
    "fld_name" VARCHAR(128) NOT NULL DEFAULT (''),
    "fld_reliability_mission" REAL NOT NULL DEFAULT (1),
    "fld_reliability_predicted" REAL NOT NULL DEFAULT (1),
    "fld_remarks" BLOB NOT NULL,
    "fld_total_part_quantity" INTEGER NOT NULL DEFAULT (1),
    "fld_revision_code" VARCHAR(8) DEFAULT ('')
);

INSERT INTO "tbl_revisions" VALUES(0,1.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,'Original',1.0,1.0,'This is the original revision the system.',0,'');

CREATE TABLE "tbl_similar_item" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT (0),
    "fld_assembly_id" INTEGER NOT NULL DEFAULT (0),
    "fld_sia_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_change_desc_1" BLOB DEFAULT ('No changes'),
    "fld_change_category_1" VARCHAR(32) NOT NULL DEFAULT ('None'),
    "fld_change_factor_1" REAL DEFAULT (1),
    "fld_change_effort_1" INTEGER DEFAULT (0),
    "fld_change_cost_1" REAL DEFAULT (0),
    "fld_change_desc_2" BLOB DEFAULT ('No changes'),
    "fld_change_category_2" VARCHAR(32) NOT NULL DEFAULT ('None'),
    "fld_change_factor_2" REAL DEFAULT (1),
    "fld_change_effort_2" INTEGER DEFAULT (0),
    "fld_change_cost_2" REAL DEFAULT (0),
    "fld_change_desc_3" BLOB DEFAULT ('No changes'),
    "fld_change_category_3" VARCHAR(32) NOT NULL DEFAULT ('None'),
    "fld_change_factor_3" REAL DEFAULT (1),
    "fld_change_effort_3" INTEGER DEFAULT (0),
    "fld_change_cost_3" REAL DEFAULT (0),
    "fld_change_desc_4" BLOB DEFAULT ('No changes'),
    "fld_change_category_4" VARCHAR(32) NOT NULL DEFAULT ('None'),
    "fld_change_factor_4" REAL DEFAULT (1),
    "fld_change_effort_4" INTEGER DEFAULT (0),
    "fld_change_cost_4" REAL DEFAULT (0),
    "fld_change_desc_5" BLOB DEFAULT ('No changes'),
    "fld_change_category_5" VARCHAR(32) NOT NULL DEFAULT ('None'),
    "fld_change_factor_5" REAL DEFAULT (1),
    "fld_change_effort_5" INTEGER DEFAULT (0),
    "fld_change_cost_5" REAL DEFAULT (0),
    "fld_change_desc_6" BLOB DEFAULT ('No changes'),
    "fld_change_category_6" VARCHAR(32) NOT NULL DEFAULT ('None'),
    "fld_change_factor_6" REAL DEFAULT (1),
    "fld_change_effort_6" INTEGER DEFAULT (0),
    "fld_change_cost_6" REAL DEFAULT (0),
    "fld_change_desc_7" BLOB DEFAULT ('No changes'),
    "fld_change_category_7" VARCHAR(32) NOT NULL DEFAULT ('None'),
    "fld_change_factor_7" REAL DEFAULT (1),
    "fld_change_effort_7" INTEGER DEFAULT (0),
    "fld_change_cost_7" REAL DEFAULT (0),
    "fld_change_desc_8" BLOB DEFAULT ('No changes'),
    "fld_change_category_8" VARCHAR(32) NOT NULL DEFAULT ('None'),
    "fld_change_factor_8" REAL DEFAULT (1),
    "fld_change_effort_8" INTEGER DEFAULT (0),
    "fld_change_cost_8" REAL DEFAULT (0),
    "fld_function_1" VARCHAR(128) NOT NULL DEFAULT (''),
    "fld_function_2" VARCHAR(128) NOT NULL DEFAULT (''),
    "fld_function_3" VARCHAR(128) NOT NULL DEFAULT (''),
    "fld_function_4" VARCHAR(128) NOT NULL DEFAULT (''),
    "fld_function_5" VARCHAR(128) NOT NULL DEFAULT (''),
    "fld_result_1" REAL DEFAULT (0),
    "fld_result_2" REAL DEFAULT (0),
    "fld_result_3" REAL DEFAULT (0),
    "fld_result_4" REAL DEFAULT (0),
    "fld_result_5" REAL DEFAULT (0),
    "fld_user_blob_1" BLOB,
    "fld_user_blob_2" BLOB,
    "fld_user_blob_3" BLOB,
    "fld_user_float_1" REAL DEFAULT (0),
    "fld_user_float_2" REAL DEFAULT (0),
    "fld_user_float_3" REAL DEFAULT (0),
    "fld_user_int_1" INTEGER DEFAULT (0),
    "fld_user_int_2" INTEGER DEFAULT (0),
    "fld_user_int_3" INTEGER DEFAULT (0),
    "fld_category_value_1" INTEGER DEFAULT (0),
    "fld_category_value_2" INTEGER DEFAULT (0),
    "fld_category_value_3" INTEGER DEFAULT (0),
    "fld_category_value_4" INTEGER DEFAULT (0),
    "fld_category_value_5" INTEGER DEFAULT (0),
    "fld_category_value_6" INTEGER DEFAULT (0),
    "fld_category_value_7" INTEGER DEFAULT (0),
    "fld_category_value_8" INTEGER DEFAULT (0)
);

INSERT INTO "tbl_similar_item" VALUES(0,0,1,'No changes','None',1.0,0,0.0,'No changes','None',1.0,0,0.0,'No changes','None',1.0,0,0.0,'No changes','None',1.0,0,0.0,'No changes','None',1.0,0,0.0,'No changes','None',1.0,0,0.0,'No changes','None',1.0,0,0.0,'No changes','None',1.0,0,0.0,'','','','','',0.0,0.0,0.0,0.0,0.0,NULL,NULL,NULL,0.0,0.0,0.0,0,0,0,0,0,0,0,0,0,0,0);

CREATE TABLE "tbl_software" (
    "fld_revision_id" INTEGER DEFAULT (0),
    "fld_software_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_level_id" INTEGER DEFAULT (0),
    "fld_description" VARCHAR(128),
    "fld_application_id" INTEGER DEFAULT (0),
    "fld_development_id" INTEGER DEFAULT (0),
    "fld_a" REAL DEFAULT (0),
    "fld_do" REAL DEFAULT (0),
    "fld_dd" INTEGER DEFAULT (0),
    "fld_dc" REAL DEFAULT (0),
    "fld_d" REAL DEFAULT (0),
    "fld_am" REAL DEFAULT (0),
    "fld_sa" REAL DEFAULT (0),
    "fld_st" REAL DEFAULT (0),
    "fld_dr" REAL DEFAULT (0),
    "fld_sq" REAL DEFAULT (0),
    "fld_s1" REAL DEFAULT (0),
    "fld_hloc" INTEGER DEFAULT (0),
    "fld_aloc" INTEGER DEFAULT (0),
    "fld_loc" INTEGER DEFAULT (0),
    "fld_sl" REAL DEFAULT (0),
    "fld_ax" INTEGER DEFAULT (0),
    "fld_bx" INTEGER DEFAULT (0),
    "fld_cx" INTEGER DEFAULT (0),
    "fld_nm" INTEGER DEFAULT (0),
    "fld_sx" REAL DEFAULT (0),
    "fld_um" INTEGER DEFAULT (0),
    "fld_wm" INTEGER DEFAULT (0),
    "fld_xm" INTEGER DEFAULT (0),
    "fld_sm" REAL DEFAULT (0),
    "fld_df" REAL DEFAULT (0),
    "fld_sr" REAL DEFAULT (0),
    "fld_s2" REAL DEFAULT (0),
    "fld_rpfom" REAL DEFAULT (0),
    "fld_parent_module" VARCHAR(16) NOT NULL DEFAULT (0),
    "fld_dev_assess_type" TINYINT DEFAULT (1),
    "fld_phase_id" TINYINT DEFAULT (1),
    "fld_tcl" INTEGER DEFAULT (0),
    "fld_test_path" INTEGER DEFAULT (0),
    "fld_category" INTEGER DEFAULT (0),
    "fld_test_effort" INTEGER DEFAULT (0),
    "fld_test_approach" INTEGER DEFAULT (0),
    "fld_labor_hours_test" REAL DEFAULT (0),
    "fld_labor_hours_dev" REAL DEFAULT (0),
    "fld_budget_test" REAL DEFAULT (0),
    "fld_budget_dev" REAL DEFAULT (0),
    "fld_schedule_test" REAL DEFAULT (0),
    "fld_schedule_dev" REAL DEFAULT (0),
    "fld_branches" INTEGER DEFAULT (0),
    "fld_branches_test" INTEGER DEFAULT (0),
    "fld_inputs" INTEGER DEFAULT (0),
    "fld_inputs_test" INTEGER DEFAULT (0),
    "fld_nm_test" INTEGER DEFAULT (0),
    "fld_interfaces" INTEGER DEFAULT (0),
    "fld_interfaces_test" INTEGER DEFAULT (0),
    "fld_te" REAL DEFAULT (0),
    "fld_tm" REAL DEFAULT (0),
    "fld_tc" REAL DEFAULT (0),
    "fld_t" REAL DEFAULT (0),
    "fld_ft1" REAL DEFAULT (0),
    "fld_ft2" REAL DEFAULT (0),
    "fld_ren_avg" REAL DEFAULT (0),
    "fld_ren_eot" REAL DEFAULT (0),
    "fld_ec" REAL DEFAULT (0),
    "fld_ev" REAL DEFAULT (0),
    "fld_et" REAL DEFAULT (0),
    "fld_os" REAL DEFAULT (0),
    "fld_ew" REAL DEFAULT (0),
    "fld_e" REAL DEFAULT (0),
    "fld_f" REAL DEFAULT (0)
);
INSERT INTO "tbl_software" VALUES(0, 0, 0, "System Software", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "-", 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);

CREATE TABLE "tbl_software_development" (
    "fld_software_id" INTEGER NOT NULL DEFAULT (0),
    "fld_question_id" INTEGER NOT NULL DEFAULT (0),
    "fld_y" TINYINT DEFAULT (0),
    PRIMARY KEY("fld_software_id", "fld_question_id")
);
INSERT INTO "tbl_software_development" VALUES(0, 0, 0);
INSERT INTO "tbl_software_development" VALUES(0, 1, 0);
INSERT INTO "tbl_software_development" VALUES(0, 2, 0);
INSERT INTO "tbl_software_development" VALUES(0, 3, 0);
INSERT INTO "tbl_software_development" VALUES(0, 4, 0);
INSERT INTO "tbl_software_development" VALUES(0, 5, 0);
INSERT INTO "tbl_software_development" VALUES(0, 6, 0);
INSERT INTO "tbl_software_development" VALUES(0, 7, 0);
INSERT INTO "tbl_software_development" VALUES(0, 8, 0);
INSERT INTO "tbl_software_development" VALUES(0, 9, 0);
INSERT INTO "tbl_software_development" VALUES(0, 10, 0);
INSERT INTO "tbl_software_development" VALUES(0, 11, 0);
INSERT INTO "tbl_software_development" VALUES(0, 12, 0);
INSERT INTO "tbl_software_development" VALUES(0, 13, 0);
INSERT INTO "tbl_software_development" VALUES(0, 14, 0);
INSERT INTO "tbl_software_development" VALUES(0, 15, 0);
INSERT INTO "tbl_software_development" VALUES(0, 16, 0);
INSERT INTO "tbl_software_development" VALUES(0, 17, 0);
INSERT INTO "tbl_software_development" VALUES(0, 18, 0);
INSERT INTO "tbl_software_development" VALUES(0, 19, 0);
INSERT INTO "tbl_software_development" VALUES(0, 20, 0);
INSERT INTO "tbl_software_development" VALUES(0, 21, 0);
INSERT INTO "tbl_software_development" VALUES(0, 22, 0);
INSERT INTO "tbl_software_development" VALUES(0, 23, 0);
INSERT INTO "tbl_software_development" VALUES(0, 24, 0);
INSERT INTO "tbl_software_development" VALUES(0, 25, 0);
INSERT INTO "tbl_software_development" VALUES(0, 26, 0);
INSERT INTO "tbl_software_development" VALUES(0, 27, 0);
INSERT INTO "tbl_software_development" VALUES(0, 28, 0);
INSERT INTO "tbl_software_development" VALUES(0, 29, 0);
INSERT INTO "tbl_software_development" VALUES(0, 30, 0);
INSERT INTO "tbl_software_development" VALUES(0, 31, 0);
INSERT INTO "tbl_software_development" VALUES(0, 32, 0);
INSERT INTO "tbl_software_development" VALUES(0, 33, 0);
INSERT INTO "tbl_software_development" VALUES(0, 34, 0);
INSERT INTO "tbl_software_development" VALUES(0, 35, 0);
INSERT INTO "tbl_software_development" VALUES(0, 36, 0);
INSERT INTO "tbl_software_development" VALUES(0, 37, 0);
INSERT INTO "tbl_software_development" VALUES(0, 38, 0);
INSERT INTO "tbl_software_development" VALUES(0, 39, 0);
INSERT INTO "tbl_software_development" VALUES(0, 40, 0);
INSERT INTO "tbl_software_development" VALUES(0, 41, 0);
INSERT INTO "tbl_software_development" VALUES(0, 42, 0);

CREATE TABLE "tbl_software_quality" (
    "fld_software_id" INTEGER NOT NULL DEFAULT (0),
    "fld_phase_id" INTEGER NOT NULL DEFAULT (0),
    "fld_question_id" INTEGER NOT NULL DEFAULT (0),
    "fld_value" INTEGER DEFAULT (0),
    "fld_ratio" REAL DEFAULT (0),
    "fld_y" TINYINT DEFAULT (0),
    "fld_n" TINYINT DEFAULT (0),
    "fld_na" TINYINT DEFAULT (0),
    "fld_unk" TINYINT DEFAULT (0),
    PRIMARY KEY("fld_software_id", "fld_phase_id", "fld_question_id")
);

CREATE TABLE "tbl_software_standards" (
    "fld_software_id" INTEGER NOT NULL DEFAULT (0),
    "fld_phase_id" INTEGER NOT NULL DEFAULT (0),
    "fld_question_id" INTEGER NOT NULL DEFAULT (0),
    "fld_value" INTEGER DEFAULT (0),
    "fld_ratio" REAL DEFAULT (0),
    "fld_y" TINYINT DEFAULT (0),
    "fld_n" TINYINT DEFAULT (0),
    "fld_na" TINYINT DEFAULT (0),
    "fld_unk" TINYINT DEFAULT (0),
    PRIMARY KEY("fld_software_id", "fld_phase_id", "fld_question_id")
);

CREATE TABLE "tbl_software_tests" (
    "fld_software_id" INTEGER NOT NULL DEFAULT (0),
    "fld_technique_id" INTEGER NOT NULL DEFAULT (0),
    "fld_tcl" VARCHAR(4) DEFAULT ('L'),
    "fld_effectiveness_single" TINYINT DEFAULT (0),
    "fld_effectiveness_paired" TINYINT DEFAULT (0),
    "fld_coverage_single" TINYINT DEFAULT (0),
    "fld_coverage_paired" TINYINT DEFAULT (0),
    "fld_error_cat" TINYINT DEFAULT (0),
    "fld_remarks" BLOB,
    "fld_used" TINYINT DEFAULT (0),
    PRIMARY KEY("fld_software_id", "fld_technique_id")
);

CREATE TABLE "tbl_software_traceability" (
    "fld_software_id" INTEGER NOT NULL DEFAULT (0),
    "fld_phase_id" INTEGER NOT NULL DEFAULT (0),
    "fld_tc11" INTEGER NOT NULL DEFAULT (0),
    "fld_tc12" INTEGER NOT NULL DEFAULT (0),
    PRIMARY KEY("fld_software_id", "fld_phase_id")
);

CREATE TABLE "tbl_system" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT (0),
    "fld_assembly_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_add_adj_factor" REAL NOT NULL DEFAULT (0),
    "fld_allocation_type" INTEGER NOT NULL DEFAULT (0),
    "fld_alt_part_number" VARCHAR(128) DEFAULT (''),
    "fld_assembly_criticality" REAL NOT NULL DEFAULT (0),
    "fld_attachments" VARCHAR(256) DEFAULT (''),
    "fld_availability" REAL NOT NULL DEFAULT (1),
    "fld_availability_mission" REAL NOT NULL DEFAULT (1),
    "fld_cage_code" VARCHAR(64) DEFAULT (''),
    "fld_calculation_model" INTEGER NOT NULL DEFAULT (1),
    "fld_category_id" INTEGER NOT NULL DEFAULT (0),
    "fld_comp_ref_des" VARCHAR(128) DEFAULT (''),
    "fld_cost" REAL NOT NULL DEFAULT (0),
    "fld_cost_failure" REAL NOT NULL DEFAULT (0),
    "fld_cost_hour" REAL NOT NULL DEFAULT (0),
    "fld_cost_type" INTEGER NOT NULL DEFAULT (1),
    "fld_description" VARCHAR(256) DEFAULT (''),
    "fld_detection_fr" REAL NOT NULL DEFAULT (0),
    "fld_detection_percent" REAL NOT NULL DEFAULT (100),
    "fld_duty_cycle" REAL NOT NULL DEFAULT (100),
    "fld_entered_by" VARCHAR(64) DEFAULT (''),
    "fld_environment_active" INTEGER NOT NULL DEFAULT (0),
    "fld_environment_dormant" INTEGER NOT NULL DEFAULT (0),
    "fld_failure_dist" INTEGER NOT NULL DEFAULT (0),
    "fld_failure_parameter_1" REAL NOT NULL DEFAULT (0),
    "fld_failure_parameter_2" REAL NOT NULL DEFAULT (0),
    "fld_failure_parameter_3" REAL NOT NULL DEFAULT (0),
    "fld_failure_rate_active" REAL NOT NULL DEFAULT (0),
    "fld_failure_rate_dormant" REAL NOT NULL DEFAULT (0),
    "fld_failure_rate_mission" REAL NOT NULL DEFAULT (0),
    "fld_failure_rate_percent" REAL NOT NULL DEFAULT (0),
    "fld_failure_rate_predicted" REAL NOT NULL DEFAULT (0),
    "fld_failure_rate_software" REAL NOT NULL DEFAULT (0),
    "fld_failure_rate_specified" REAL NOT NULL DEFAULT (0),
    "fld_failure_rate_type" INTEGER NOT NULL DEFAULT (2),
    "fld_figure_number" VARCHAR(32) DEFAULT (''),
    "fld_humidity" REAL NOT NULL DEFAULT (50),
    "fld_image_file" VARCHAR(128) DEFAULT (''),
    "fld_isolation_fr" REAL NOT NULL DEFAULT (0),
    "fld_isolation_percent" REAL NOT NULL DEFAULT (0),
    "fld_lcn" VARCHAR(128) DEFAULT (''),
    "fld_level" INTEGER NOT NULL DEFAULT (1),
    "fld_manufacturer" INTEGER NOT NULL DEFAULT (0),
    "fld_mcmt" REAL NOT NULL DEFAULT (0),
    "fld_mission_time" REAL NOT NULL DEFAULT (100),
    "fld_mmt" REAL NOT NULL DEFAULT (0),
    "fld_modified_by" VARCHAR(64) DEFAULT (''),
    "fld_mpmt" REAL NOT NULL DEFAULT (0),
    "fld_mtbf_mission" REAL NOT NULL DEFAULT (0),
    "fld_mtbf_predicted" REAL NOT NULL DEFAULT (0),
    "fld_mtbf_specified" REAL NOT NULL DEFAULT (0),
    "fld_mttr" REAL NOT NULL DEFAULT (0),
    "fld_mttr_add_adj_factor" REAL NOT NULL DEFAULT (1),
    "fld_mttr_mult_adj_factor" REAL NOT NULL DEFAULT (0),
    "fld_mttr_specified" REAL NOT NULL DEFAULT (0),
    "fld_mttr_type" INTEGER NOT NULL DEFAULT (1),
    "fld_mult_adj_factor" REAL NOT NULL DEFAULT (1),
    "fld_name" VARCHAR(256) DEFAULT (''),
    "fld_nsn" VARCHAR(32) DEFAULT (''),
    "fld_overstress" TINYINT NOT NULL DEFAULT (0),
    "fld_page_number" VARCHAR(32) DEFAULT (''),
    "fld_parent_assembly" VARCHAR(16) NOT NULL DEFAULT (0),
    "fld_part" TINYINT NOT NULL DEFAULT (0),
    "fld_part_number" VARCHAR(128) DEFAULT (''),
    "fld_percent_isolation_group_ri" REAL NOT NULL DEFAULT (0),
    "fld_percent_isolation_single_ri" REAL NOT NULL DEFAULT (0),
    "fld_quantity" INTEGER NOT NULL DEFAULT (1),
    "fld_ref_des" VARCHAR(128) DEFAULT (''),
    "fld_reliability_mission" REAL NOT NULL DEFAULT (1),
    "fld_reliability_predicted" REAL NOT NULL DEFAULT (1),
    "fld_remarks" BLOB,
    "fld_repair_dist" INTEGER NOT NULL DEFAULT (0),
    "fld_repair_parameter_1" REAL NOT NULL DEFAULT (0),
    "fld_repair_parameter_2" REAL NOT NULL DEFAULT (0),
    "fld_repairable" TINYINT NOT NULL DEFAULT (0),
    "fld_rpm" REAL NOT NULL DEFAULT (0),
    "fld_specification_number" VARCHAR(64) DEFAULT (''),
    "fld_subcategory_id" INTEGER NOT NULL DEFAULT (0),
    "fld_tagged_part" TINYINT NOT NULL DEFAULT (0),
    "fld_temperature_active" REAL NOT NULL DEFAULT (30),
    "fld_temperature_dormant" REAL NOT NULL DEFAULT (30),
    "fld_total_part_quantity" INTEGER NOT NULL DEFAULT (0),
    "fld_total_power_dissipation" REAL NOT NULL DEFAULT (0),
    "fld_vibration" REAL NOT NULL DEFAULT (0),
    "fld_weibull_data_set" INTEGER NOT NULL DEFAULT (1),
    "fld_weibull_file" VARCHAR(128) DEFAULT (''),
    "fld_year_of_manufacture" INTEGER NOT NULL DEFAULT (2002),
    "fld_ht_model" VARCHAR(512) DEFAULT (''),
    "fld_reliability_goal_measure" INTEGER NOT NULL DEFAULT (0),
    "fld_reliability_goal" REAL NOT NULL DEFAULT (1)
);

INSERT INTO "tbl_system" VALUES(0,0,0.0,0,'',0.0,'',1.0,1.0,'',1,0,'',0.0,0.0,0.0,1,'System',0.0,100.0,100.0,'',0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,'',0.0,'',0.0,0.0,'',0,-1,0.0,100.0,0.0,'',0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0,0.0,'','',0,'','-',0,'',0.0,0.0,1,'',0.0,0.0,'',0,0.0,0.0,1,0.0,'',0,0,0.0,0.0,0,0.0,0.0,0,'',2002,'',0,1.0);

CREATE TABLE "tbl_software_traceability" (
    "fld_software_id" INTEGER NOT NULL DEFAULT(0),
    "fld_phase_id" INTEGER NOT NULL DEFAULT(0),
    "fld_tc11" INTEGER NOT NULL DEFAULT(0),
    "fld_tc12" INTEGER NOT NULL DEFAULT(0)
);

CREATE TABLE "tbl_units" (
    "fld_serial_no" VARCHAR(128) NOT NULL PRIMARY KEY,
    "fld_model" VARCHAR(64),
    "fld_market" VARCHAR(16),
    "fld_build_date" VARCHAR(16),
    "fld_delivery_date" VARCHAR(16),
    "fld_warranty_date" VARCHAR(16),
    "fld_warranty_period" INTEGER,
    "fld_warranty_type" VARCHAR(8)
);

CREATE TABLE "tbl_validation" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT (0),
    "fld_validation_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_task_desc" BLOB,
    "fld_task_type" INTEGER DEFAULT (0),
    "fld_task_specification" VARCHAR(128) NOT NULL DEFAULT (''),
    "fld_measurement_unit" INTEGER DEFAULT (0),
    "fld_min_acceptable" REAL DEFAULT (0),
    "fld_mean_acceptable" REAL DEFAULT (0),
    "fld_max_acceptable" REAL DEFAULT (0),
    "fld_variance_acceptable" REAL DEFAULT (0),
    "fld_start_date" VARCHAR(45) DEFAULT (''),
    "fld_end_date" VARCHAR(45) DEFAULT (''),
    "fld_status" REAL DEFAULT (0),
    "fld_effectiveness" REAL DEFAULT (0)
);

CREATE TABLE "tbl_validation_matrix" (
    "fld_validation_id" INTEGER NOT NULL,
    "fld_requirement_id" INTEGER NOT NULL,
    "fld_revision_id" INTEGER DEFAULT (1),
    PRIMARY KEY ("fld_validation_id","fld_requirement_id")
);

DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('tbl_system', 0);
INSERT INTO "sqlite_sequence" VALUES('tbl_similar_item', 0);
INSERT INTO "sqlite_sequence" VALUES('tbl_program_info', 0);
INSERT INTO "sqlite_sequence" VALUES('tbl_functions', 0);
INSERT INTO "sqlite_sequence" VALUES('tbl_revisions', 0);
INSERT INTO "sqlite_sequence" VALUES('tbl_requirements', 0);
INSERT INTO "sqlite_sequence" VALUES('tbl_validation', 0);

END TRANSACTION;
