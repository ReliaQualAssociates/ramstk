PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;

-- Ordinal date 719163 = January 1, 1970

--
-- Create tables for storing program information.
--
DROP TABLE IF EXISTS "tbl_program_info";
CREATE TABLE "tbl_program_info" (
    "fld_program_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,    --
    "fld_revision_prefix" VARCHAR(16) NOT NULL DEFAULT('REVISION'), -- Default prefix to use for new revisions.
    "fld_revision_next_id" INTEGER NOT NULL DEFAULT(1),             -- Next revision ID.
    "fld_function_prefix" VARCHAR(16) NOT NULL DEFAULT('FUNCTION'), -- Default prefix to use for new function.
    "fld_function_next_id" INTEGER NOT NULL DEFAULT(1),             -- Next function ID.
    "fld_assembly_prefix" VARCHAR(16) NOT NULL DEFAULT('ASSEMBLY'), -- Default prefix to use for new hardware assembly.
    "fld_assembly_next_id" INTEGER NOT NULL DEFAULT(1),             -- Next hardware assembly ID.
    "fld_part_prefix" VARCHAR(16) NOT NULL DEFAULT('PART'),         -- Default prefix to use for new hardware part or component.
    "fld_part_next_id" INTEGER NOT NULL DEFAULT(1),
    "fld_fmeca_prefix" VARCHAR(16) NOT NULL DEFAULT('FMEA'),
    "fld_fmeca_next_id" INTEGER NOT NULL DEFAULT(1),
    "fld_mode_prefix" VARCHAR(16) NOT NULL DEFAULT('MODE'),
    "fld_mode_next_id" INTEGER NOT NULL DEFAULT(1),
    "fld_effect_prefix" VARCHAR(16) NOT NULL DEFAULT('EFFECT'),
    "fld_effect_next_id" INTEGER NOT NULL DEFAULT(1),
    "fld_cause_prefix" VARCHAR(16) NOT NULL DEFAULT('CAUSE'),
    "fld_cause_next_id" INTEGER NOT NULL DEFAULT(1),
    "fld_software_prefix" VARCHAR(16) NOT NULL DEFAULT('MODULE'),
    "fld_software_next_id" INTEGER NOT NULL DEFAULT(1),
    "fld_revision_active" TINYINT NOT NULL DEFAULT(1),
    "fld_requirement_active" TINYINT NOT NULL DEFAULT(1),
    "fld_function_active" TINYINT NOT NULL DEFAULT(1),
    "fld_hardware_active" TINYINT NOT NULL DEFAULT(1),
    "fld_software_active" TINYINT NOT NULL DEFAULT(1),
    "fld_vandv_active" TINYINT NOT NULL DEFAULT(1),
    "fld_testing_active" TINYINT NOT NULL DEFAULT(1),
    "fld_rcm_active" TINYINT NOT NULL DEFAULT(1),
    "fld_fraca_active" TINYINT NOT NULL DEFAULT(1),
    "fld_fmeca_active" TINYINT NOT NULL DEFAULT(1),
    "fld_survival_active" TINYINT NOT NULL DEFAULT(1),
    "fld_rbd_active" TINYINT NOT NULL DEFAULT(1),
    "fld_fta_active" TINYINT NOT NULL DEFAULT(1),
    "fld_created_on" datetime DEFAULT NULL,
    "fld_created_by" VARCHAR(45) DEFAULT(''),
    "fld_last_saved" datetime DEFAULT NULL,
    "fld_last_saved_by" VARCHAR(45) DEFAULT(''),
    "fld_method" VARCHAR(16) DEFAULT('STANDARD')
);
INSERT INTO "tbl_program_info" VALUES(0,'REVISION',1,'FUNCTION',1,'ASSEMBLY',1,'PART',1,'FMEA',1,'MODE',1,'EFFECT',1,'CAUSE',1,'MODULE',1,1,1,1,1,1,1,0,0,1,1,1,1,1,'0000-00-00 00:00:00','','0000-00-00 00:00:00','','STANDARD');

DROP TABLE IF EXISTS "tbl_missions";
CREATE TABLE "tbl_missions" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT(0),      -- Identifier for the revision.
    "fld_mission_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,    -- Identifier for the mission.
    "fld_mission_time" REAL DEFAULT(0),                 -- Total length of the mission.
    "fld_mission_units" INTEGER DEFAULT(0),             -- Unit of time measure for the mission.
    "fld_mission_description" BLOB                      -- Description of the mission.
);
INSERT INTO "tbl_missions" VALUES(0, 0, 100.0, 0, "Default mission");

DROP TABLE IF EXISTS "tbl_mission_phase";
CREATE TABLE "tbl_mission_phase" (
    "fld_mission_id" INTEGER NOT NULL DEFAULT(0),       -- Identifier for the mission.
    "fld_phase_id" INTEGER NOT NULL,                    -- Identifier for the mission phase.
    "fld_phase_start" REAL,                             -- Start time of mission phase.
    "fld_phase_end" REAL,                               -- End time of mission phase.
    "fld_phase_name" VARCHAR(64),                       -- Noun name of the mission phase.
    "fld_phase_description" BLOB,                       -- Description of the mission phase.
    FOREIGN KEY("fld_mission_id") REFERENCES "tbl_missions"("fld_mission_id") ON DELETE CASCADE
    PRIMARY KEY("fld_mission_id", "fld_phase_id")
);
INSERT INTO "tbl_mission_phase" VALUES(0, 1, 0.0, 0.5, 'Phase I', 'This is the first phase of the default mission.');
INSERT INTO "tbl_mission_phase" VALUES(0, 2, 0.5, 90.5, 'Phase II', 'This is the second phase of the default mission.');
INSERT INTO "tbl_mission_phase" VALUES(0, 3, 90.5, 100.0, 'Phase III', 'This is the third phase of the default mission.');

DROP TABLE IF EXISTS "tbl_environmental_profile";
CREATE TABLE "tbl_environmental_profile" (
    "fld_mission_id" INTEGER NOT NULL DEFAULT(0),       -- Identifier for the mission.
    "fld_phase_id" INTEGER NOT NULL DEFAULT(0),         -- Identifier for the mission phase.
    "fld_condition_id" INTEGER,                         -- Identifier for the environmental condition.
    "fld_condition_name" VARCHAR(128),                  -- Noun name of the environmental condition.
    "fld_units" VARCHAR(64),                            -- Units of measure for the environmental condition.
    "fld_minimum" REAL,                                 -- Minimum value of the environmental condition.
    "fld_maximum" REAL,                                 -- Maximum value of the environmental condition.
    "fld_mean" REAL,                                    -- Mean value of the environmental condition.
    "fld_variance" REAL,                                -- Variance of the environmental condition.
    FOREIGN KEY("fld_mission_id") REFERENCES "tbl_missions"("fld_mission_id") ON DELETE CASCADE
    FOREIGN KEY("fld_phase_id") REFERENCES "tbl_mission_phase"("fld_phase_id") ON DELETE CASCADE
    PRIMARY KEY("fld_mission_id", "fld_condition_id")
);

DROP TABLE IF EXISTS "tbl_failure_definitions";
CREATE TABLE "tbl_failure_definitions" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT(0),      -- Indentifier for the revision.
    "fld_definition_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, --Identifier for the failure definition.
    "fld_definition" BLOB,                              -- Definition of the failure.
    FOREIGN KEY("fld_revision_id") REFERENCES "tbl_revisions"("fld_revision_id") ON DELETE CASCADE
);

DROP TABLE IF EXISTS "tbl_revisions";
CREATE TABLE "tbl_revisions" (
    "fld_revision_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_availability" REAL NOT NULL DEFAULT(1),        -- Assessed availability of the revision.
    "fld_availability_mission" REAL NOT NULL DEFAULT(1),-- Assessed mission availability of the revision.
    "fld_cost" REAL NOT NULL DEFAULT(0),                -- Assessed cost of the revision.
    "fld_cost_failure" REAL NOT NULL DEFAULT(0),        -- Assessed cost per failure of the revision.
    "fld_cost_hour" REAL NOT NULL DEFAULT(0),           -- Assessed cost to operate the revision for one hour.
    "fld_failure_rate_active" REAL NOT NULL DEFAULT(0), -- Assessed active failure intensity of the revision.
    "fld_failure_rate_dormant" REAL NOT NULL DEFAULT(0),-- Assessed dormant failure intensity of the revision.
    "fld_failure_rate_mission" REAL NOT NULL DEFAULT(0),-- Assessed mission failure intensity of the revision.
    "fld_failure_rate_predicted" REAL NOT NULL DEFAULT(0),-- Assessed failure intensity of the revision (sum of active, dormant, and software failure intensities).
    "fld_failure_rate_software" REAL NOT NULL DEFAULT(0),-- Assessed software failure intensity of the revision.
    "fld_mmt" REAL NOT NULL DEFAULT(0),                 -- Mean maintenance time (MMT) of the revision.
    "fld_mcmt" REAL NOT NULL DEFAULT(0),                -- Mean corrective maintenance time (MCMT) of the revision.
    "fld_mpmt" REAL NOT NULL DEFAULT(0),                -- Mean preventive maintenance time (MPMT) of the revision.
    "fld_mtbf_mission" REAL NOT NULL DEFAULT(0),        -- Assessed mission MTBF of the revision.
    "fld_mtbf_predicted" REAL NOT NULL DEFAULT(0),      -- Assessed MTBF of the revision.
    "fld_mttr" REAL NOT NULL DEFAULT(0),                -- Assessed MTTR of the revision.
    "fld_name" VARCHAR(128) NOT NULL DEFAULT(''),       -- Noun name of the revision.
    "fld_reliability_mission" REAL NOT NULL DEFAULT(1), -- Assessed mission reliability of the revision.
    "fld_reliability_predicted" REAL NOT NULL DEFAULT(1),   -- Assessed reliability of the revision.
    "fld_remarks" BLOB NOT NULL,                        -- Remarks about the revision.
    "fld_total_part_quantity" INTEGER NOT NULL DEFAULT(1),  -- Total number of components comprising the revision.
    "fld_revision_code" VARCHAR(8) DEFAULT('')          -- Alphnumeric code for the revision.
);
INSERT INTO "tbl_revisions" VALUES(0,1.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,'Original',1.0,1.0,'This is the original revision of the system.',0,'');

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

--
-- Create tables for storing system function information.
--
DROP TABLE IF EXISTS "tbl_functions";
CREATE TABLE "tbl_functions" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT(0),
    "fld_function_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_availability" FLOAT NOT NULL DEFAULT(1),           -- Assessed availability of the function.
    "fld_availability_mission" FLOAT NOT NULL DEFAULT(1),   -- Assessed mission availability of the function.
    "fld_code" VARCHAR(16) NOT NULL DEFAULT('Function Code'),   -- Tracking code for the function.
    "fld_cost" FLOAT NOT NULL DEFAULT(0),                   -- Assessed cost of the function.
    "fld_failure_rate_mission" FLOAT NOT NULL DEFAULT(0),   -- Assessed mission failure intensity of the function.
    "fld_failure_rate_predicted" FLOAT NOT NULL DEFAULT(0), -- Assessed limiting failure intensity of the function.
    "fld_mmt" FLOAT NOT NULL DEFAULT(0),                    -- Assessed mean maintenance time of the function.
    "fld_mcmt" FLOAT NOT NULL DEFAULT(0),                   -- Assessed mean corrective maintenance time of the function.
    "fld_mpmt" FLOAT NOT NULL DEFAULT(0),                   -- Assessed mean preventive maintenance time of the function.
    "fld_mtbf_mission" FLOAT NOT NULL DEFAULT(0),           -- Assessed mission mean time between failures of the function.
    "fld_mtbf_predicted" FLOAT NOT NULL DEFAULT(0),         -- Assessed limiting mean time between failures of the function.
    "fld_mttr" FLOAT NOT NULL DEFAULT(0),                   -- Assessed mean time to repair of the function.
    "fld_name" VARCHAR(255) DEFAULT('Function Name'),       -- Noun name of the function.
    "fld_remarks" BLOB,                                     -- Remarks associated with the function.
    "fld_total_mode_quantity" INTEGER NOT NULL DEFAULT(0),  -- Total number of failure modes impacting the function.
    "fld_total_part_quantity" INTEGER NOT NULL DEFAULT(0),  -- Total number of components comprising the function.
    "fld_type" INTEGER NOT NULL DEFAULT(0),                 --
    "fld_parent_id" VARCHAR(16) NOT NULL DEFAULT('-'),      --
    "fld_level" INTEGER NOT NULL DEFAULT(0),                --
    "fld_safety_critical" INTEGER NOT NULL DEFAULT(0)       -- Indicates whether or not the function is safety critical.
);
INSERT INTO "tbl_functions" VALUES(0,0,1.0,1.0,'UF-01',0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,'Unassigned to Function','',0,0,0,'-',0,0);

CREATE TABLE "tbl_functional_matrix" (
    "fld_assembly_id" INTEGER NOT NULL DEFAULT (0),
    "fld_function_id" INTEGER NOT NULL DEFAULT (0),
    "fld_revision_id" INTEGER NOT NULL DEFAULT (0),
    PRIMARY KEY ("fld_assembly_id", "fld_function_id")
);
INSERT INTO "tbl_functional_matrix" VALUES(0,0,0);

--
-- Create the tables for storing program requirements information.
--
DROP TABLE IF EXISTS "tbl_stakeholder_input";
CREATE TABLE "tbl_stakeholder_input" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT(0),      -- Identifier for the associated revision.
    "fld_input_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,  -- Identifier for the stakeholder input.
    "fld_stakeholder" VARCHAR(128),                     -- The name of the stakeholder providing the input.
    "fld_description" BLOB,                             -- Description of the stakeholder input.
    "fld_group" VARCHAR(128),                           -- Name of the group this stakeholder input is assigned to.
    "fld_priority" INTEGER DEFAULT (5),                 -- stakeholder priority for the input.
    "fld_customer_rank" INTEGER DEFAULT (1),            -- stakeholder satisfaction rating of the existing product for the input.
    "fld_planned_rank" INTEGER DEFAULT (3),             -- Planned satisfaction rating of the new product for the input.
    "fld_improvement" FLOAT DEFAULT (1.0),              -- The improvement factor on the satisfaction rating.
    "fld_overall_weight" FLOAT DEFAULT (0),             -- Overall weighting factor for the need/desire.
    "fld_requirement_code" VARCHAR(16) DEFAULT (''),    -- The alphanumeric code of the requirement that satisfies this stakeholder input.
    "fld_user_float_1" FLOAT DEFAULT (0.0),             -- User defined float value.
    "fld_user_float_2" FLOAT DEFAULT (0.0),             -- User defined float value.
    "fld_user_float_3" FLOAT DEFAULT (0.0),             -- User defined float value.
    "fld_user_float_4" FLOAT DEFAULT (0.0),             -- User defined float value.
    "fld_user_float_5" FLOAT DEFAULT (0.0),             -- User defined float value.
    FOREIGN KEY("fld_revision_id") REFERENCES "tbl_revisions"("fld_revision_id") ON DELETE CASCADE
);

DROP TABLE IF EXISTS "tbl_requirements";
CREATE TABLE "tbl_requirements" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT(0),      -- Identifier for the associated revision.
    "fld_requirement_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,    -- Identifier for the requirement.
    "fld_assembly_id" INTEGER NOT NULL DEFAULT(0),      -- The ID of the hardware assembly associated with the requirement.
    "fld_requirement_desc" BLOB,                        -- Noun description of the requirement.
    "fld_requirement_type" VARCHAR(128) DEFAULT (''),   -- Type of requirement.
    "fld_requirement_code" VARCHAR(16) DEFAULT (''),    -- Alphanumeric code for the requirement.
    "fld_derived" TINYINT DEFAULT(0),                   -- Indicates whether or not the requirement is derived.
    "fld_parent_requirement" VARCHAR(45) NOT NULL DEFAULT('-'), -- If a derived requirement, the gtk.TreePath of the parent.
    "fld_validated" TINYINT DEFAULT(0),                 -- Indicates whether or not the requirement has been validated.
    "fld_validated_date" INTEGER DEFAULT (719163),      -- The ordinal date the requirement was validated.
    "fld_owner" VARCHAR(128) DEFAULT (''),              -- The responsible group or individual for the requirement.
    "fld_specification" VARCHAR(128) DEFAULT (''),      -- Any industry, company, etc. specification associated  with the requirement.
    "fld_page_number" VARCHAR(32) DEFAULT (''),         -- The page number in the associated specification.
    "fld_figure_number" VARCHAR(32) DEFAULT (''),       -- The figure number in the associated specification.
    "fld_parent_id" INTEGER DEFAULT(0),                 -- The ID of the parent requirement.
    "fld_software_id" INTEGER DEFAULT(0),               -- The ID of the software module associated with the requirement.
    "fld_clear_q1" TINYINT DEFAULT(0),
    "fld_clear_q2" TINYINT DEFAULT(0),
    "fld_clear_q3" TINYINT DEFAULT(0),
    "fld_clear_q4" TINYINT DEFAULT(0),
    "fld_clear_q5" TINYINT DEFAULT(0),
    "fld_clear_q6" TINYINT DEFAULT(0),
    "fld_clear_q7" TINYINT DEFAULT(0),
    "fld_clear_q8" TINYINT DEFAULT(0),
    "fld_clear_q9" TINYINT DEFAULT(0),
    "fld_clear_q10" TINYINT DEFAULT(0),
    "fld_complete_q1" TINYINT DEFAULT(0),
    "fld_complete_q2" TINYINT DEFAULT(0),
    "fld_complete_q3" TINYINT DEFAULT(0),
    "fld_complete_q4" TINYINT DEFAULT(0),
    "fld_complete_q5" TINYINT DEFAULT(0),
    "fld_complete_q6" TINYINT DEFAULT(0),
    "fld_complete_q7" TINYINT DEFAULT(0),
    "fld_complete_q8" TINYINT DEFAULT(0),
    "fld_complete_q9" TINYINT DEFAULT(0),
    "fld_complete_q10" TINYINT DEFAULT(0),
    "fld_consistent_q1" TINYINT DEFAULT(0),
    "fld_consistent_q2" TINYINT DEFAULT(0),
    "fld_consistent_q3" TINYINT DEFAULT(0),
    "fld_consistent_q4" TINYINT DEFAULT(0),
    "fld_consistent_q5" TINYINT DEFAULT(0),
    "fld_consistent_q6" TINYINT DEFAULT(0),
    "fld_consistent_q7" TINYINT DEFAULT(0),
    "fld_consistent_q8" TINYINT DEFAULT(0),
    "fld_consistent_q9" TINYINT DEFAULT(0),
    "fld_consistent_q10" TINYINT DEFAULT(0),
    "fld_verifiable_q1" TINYINT DEFAULT(0),
    "fld_verifiable_q2" TINYINT DEFAULT(0),
    "fld_verifiable_q3" TINYINT DEFAULT(0),
    "fld_verifiable_q4" TINYINT DEFAULT(0),
    "fld_verifiable_q5" TINYINT DEFAULT(0),
    "fld_verifiable_q6" TINYINT DEFAULT(0)
);


--
-- Create tables for storing system hardware and software
-- structure information.
--
DROP TABLE IF EXISTS "tbl_system";
CREATE TABLE "tbl_system" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT(0),                  -- Revision code.
    "fld_assembly_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,   -- Assembly code.
    "fld_add_adj_factor" REAL NOT NULL DEFAULT(0),                  -- Failure rate additive adjustment factor.
    "fld_allocation_type" INTEGER NOT NULL DEFAULT(0),              -- Allocation method to use.
    "fld_alt_part_number" VARCHAR(128) DEFAULT(''),                 -- Alternate part number.
    "fld_assembly_criticality" VARCHAR(256) DEFAULT(''),            -- MIL-STD-1629A criticality of the assembly.
    "fld_attachments" VARCHAR(256) DEFAULT(''),                     -- Hyperlinks to any attachments.
    "fld_availability" REAL NOT NULL DEFAULT(1),                    -- Inherent availability.
    "fld_availability_mission" REAL NOT NULL DEFAULT(1),            -- Estimated mission availability.
    "fld_cage_code" VARCHAR(64) DEFAULT(''),                        -- CAGE code for assembly or part.
    "fld_calculation_model" INTEGER NOT NULL DEFAULT(1),            -- Failure rate calculation model to use.
    "fld_category_id" INTEGER NOT NULL DEFAULT(0),                  -- Component category ID.
    "fld_comp_ref_des" VARCHAR(128) DEFAULT(''),                    -- Composite reference designator.
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
    "fld_failure_dist" INTEGER NOT NULL DEFAULT (0),                -- Failure distribution.
    "fld_failure_parameter_1" REAL NOT NULL DEFAULT (0),            -- Scale parameter.
    "fld_failure_parameter_2" REAL NOT NULL DEFAULT (0),            -- Shape parameter.
    "fld_failure_parameter_3" REAL NOT NULL DEFAULT (0),            -- Location parameter.
    "fld_failure_rate_active" REAL NOT NULL DEFAULT (0),
    "fld_failure_rate_dormant" REAL NOT NULL DEFAULT (0),
    "fld_failure_rate_mission" REAL NOT NULL DEFAULT (0),
    "fld_failure_rate_percent" REAL NOT NULL DEFAULT (0),
    "fld_failure_rate_predicted" REAL NOT NULL DEFAULT (0),
    "fld_failure_rate_software" REAL NOT NULL DEFAULT (0),          -- Software failure rate.
    "fld_failure_rate_specified" REAL NOT NULL DEFAULT (0),         -- Specified failure rate.
    "fld_failure_rate_type" INTEGER NOT NULL DEFAULT(1),            -- How the failure rate is determined (1=Assessed, 2=Specified, Failure Rate, 3=Specified, MTBF)
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
    "fld_reliability_goal" REAL NOT NULL DEFAULT (1),
    "fld_mtbf_lcl" REAL NOT NULL DEFAULT (0),
    "fld_mtbf_ucl" REAL NOT NULL DEFAULT (0),
    "fld_failure_rate_lcl" REAL NOT NULL DEFAULT (0),
    "fld_failure_rate_ucl" REAL NOT NULL DEFAULT (0)
);
INSERT INTO "tbl_system" VALUES(0,0,0.0,0,'',0.0,'',1.0,1.0,'',1,0,'',0.0,0.0,0.0,1,'System',0.0,100.0,100.0,'',0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1,'',0.0,'',0.0,0.0,'',0,-1,0.0,100.0,0.0,'',0.0,0.0,0.0,0.0,0.0,1.0,1.0,0.0,0,1.0,'System','',0,'','-',0,'',0.0,0.0,1,'',0.0,0.0,'',0,0.0,0.0,1,0.0,'',0,0,0.0,0.0,0,0.0,0.0,0,'',2002,'',0,1.0,0.0,0.0,0.0,0.0);

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
INSERT INTO "tbl_software" VALUES(0, 0, 0, "System Software", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "-", 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);

--
-- Create tables for storing hardware reliability information.
--
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

CREATE TABLE "tbl_risk_analysis" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT (0),
    "fld_assembly_id" INTEGER NOT NULL DEFAULT (0),
    "fld_risk_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_potential_hazard" VARCHAR(128) DEFAULT (''),
    "fld_potential_cause" VARCHAR(512) DEFAULT (''),
    "fld_assembly_effect" VARCHAR(512) DEFAULT (''),
    "fld_assembly_severity" VARCHAR(128) DEFAULT (''),
    "fld_assembly_probability" VARCHAR(128) DEFAULT (''),
    "fld_assembly_hri" INTEGER DEFAULT (0),
    "fld_assembly_mitigation" BLOB DEFAULT (''),
    "fld_assembly_severity_f" VARCHAR(128) DEFAULT (''),
    "fld_assembly_probability_f" VARCHAR(128) DEFAULT (''),
    "fld_assembly_hri_f" INTEGER DEFAULT (0),
    "fld_system_effect" VARCHAR(512) DEFAULT (''),
    "fld_system_severity" VARCHAR(128) DEFAULT (''),
    "fld_system_probability" VARCHAR(128) DEFAULT (''),
    "fld_system_hri" INTEGER DEFAULT (0),
    "fld_system_mitigation" BLOB DEFAULT (''),
    "fld_system_severity_f" VARCHAR(128) DEFAULT (''),
    "fld_system_probability_f" VARCHAR(128) DEFAULT (''),
    "fld_system_hri_f" INTEGER DEFAULT (0),
    "fld_remarks" BLOB DEFAULT (''),
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
    "fld_user_blob_1" BLOB DEFAULT (''),
    "fld_user_blob_2" BLOB DEFAULT (''),
    "fld_user_blob_3" BLOB DEFAULT (''),
    "fld_user_float_1" REAL DEFAULT (0),
    "fld_user_float_2" REAL DEFAULT (0),
    "fld_user_float_3" REAL DEFAULT (0),
    "fld_user_int_1" INTEGER DEFAULT (0),
    "fld_user_int_2" INTEGER DEFAULT (0),
    "fld_user_int_3" INTEGER DEFAULT (0)
);
INSERT INTO "tbl_risk_analysis" VALUES(0,0,0,'','','','','',0,'','','',0,'','','',0,'','','',0,'','','','','','',0.0,0.0,0.0,0.0,0.0,'','','',0.0,0.0,0.0,0,0,0);

CREATE TABLE "tbl_risk_matrix" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT (0),
    "fld_assembly_id" INTEGER NOT NULL DEFAULT (0),
    "fld_severity_id" INTEGER NOT NULL DEFAULT (0),
    "fld_probability_id" INTEGER NOT NULL DEFAULT (0),
    "fld_hazard_count" INTEGER DEFAULT (0),
    PRIMARY KEY ("fld_revision_id","fld_assembly_id", "fld_severity_id", "fld_probability_id")
);

CREATE TABLE "tbl_similar_item" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT (0),
    "fld_assembly_id" INTEGER NOT NULL DEFAULT (0),
    "fld_sia_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_change_desc_1" BLOB DEFAULT ('No changes'),
    "fld_change_factor_1" REAL DEFAULT (1),
    "fld_change_desc_2" BLOB DEFAULT ('No changes'),
    "fld_change_factor_2" REAL DEFAULT (1),
    "fld_change_desc_3" BLOB DEFAULT ('No changes'),
    "fld_change_factor_3" REAL DEFAULT (1),
    "fld_change_desc_4" BLOB DEFAULT ('No changes'),
    "fld_change_factor_4" REAL DEFAULT (1),
    "fld_change_desc_5" BLOB DEFAULT ('No changes'),
    "fld_change_factor_5" REAL DEFAULT (1),
    "fld_change_desc_6" BLOB DEFAULT ('No changes'),
    "fld_change_factor_6" REAL DEFAULT (1),
    "fld_change_desc_7" BLOB DEFAULT ('No changes'),
    "fld_change_factor_7" REAL DEFAULT (1),
    "fld_change_desc_8" BLOB DEFAULT ('No changes'),
    "fld_change_factor_8" REAL DEFAULT (1),
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
    "fld_user_int_3" INTEGER DEFAULT (0)
);
INSERT INTO "tbl_similar_item" VALUES(0,0,1,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'','','','','',0.0,0.0,0.0,0.0,0.0,NULL,NULL,NULL,0.0,0.0,0.0,0,0,0);

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

--
-- Create tables for storing software reliability information.
--
CREATE TABLE "tbl_software_development" (
    "fld_software_id" INTEGER NOT NULL DEFAULT (0),                 -- Software module ID.
    "fld_question_id" INTEGER NOT NULL DEFAULT (0),                 -- Question ID.
    "fld_y" TINYINT DEFAULT (0),                                    -- Value of Y/N question.
    FOREIGN KEY("fld_software_id") REFERENCES "tbl_software"("fld_software_id") ON DELETE CASCADE
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

CREATE TABLE "tbl_srr_ssr" (
    "fld_software_id" INTEGER NOT NULL DEFAULT (0),                 -- Software module ID.
    "fld_question_id" INTEGER NOT NULL DEFAULT (0),                 -- Question ID.
    "fld_y" TINYINT DEFAULT (0),                                    -- Value of Y/N question.
    "fld_value" INTEGER DEFAULT (0),                                -- Value of quantity question.
    FOREIGN KEY("fld_software_id") REFERENCES "tbl_software"("fld_software_id") ON DELETE CASCADE
    PRIMARY KEY("fld_software_id", "fld_question_id")
);
INSERT INTO "tbl_srr_ssr" VALUES(0, 0, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 1, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 2, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 3, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 4, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 5, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 6, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 7, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 8, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 9, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 10, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 11, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 12, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 13, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 14, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 15, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 16, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 17, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 18, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 19, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 20, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 21, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 22, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 23, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 24, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 25, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 26, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 27, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 28, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 29, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 30, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 31, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 32, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 33, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 34, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 35, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 36, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 37, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 38, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 39, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 40, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 41, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 42, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 43, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 44, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 45, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 46, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 47, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 48, 0, 0);
INSERT INTO "tbl_srr_ssr" VALUES(0, 49, 0, 0);

CREATE TABLE "tbl_pdr" (
    "fld_software_id" INTEGER NOT NULL DEFAULT (0),                 -- Software module ID.
    "fld_question_id" INTEGER NOT NULL DEFAULT (0),                 -- Question ID.
    "fld_y" TINYINT DEFAULT (0),                                    -- Value of Y/N question.
    "fld_value" INTEGER DEFAULT (0),                                -- Value of quantity question.
    FOREIGN KEY("fld_software_id") REFERENCES "tbl_software"("fld_software_id") ON DELETE CASCADE
    PRIMARY KEY("fld_software_id", "fld_question_id")
);
INSERT INTO "tbl_pdr" VALUES(0, 0, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 1, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 2, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 3, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 4, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 5, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 6, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 7, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 8, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 9, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 10, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 11, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 12, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 13, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 14, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 15, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 16, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 17, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 18, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 19, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 20, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 21, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 22, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 23, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 24, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 25, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 26, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 27, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 28, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 29, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 30, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 31, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 32, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 33, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 34, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 35, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 36, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 37, 0, 0);
INSERT INTO "tbl_pdr" VALUES(0, 38, 0, 0);

CREATE TABLE "tbl_cdr" (
    "fld_software_id" INTEGER NOT NULL DEFAULT (0),                 -- Software module ID.
    "fld_question_id" INTEGER NOT NULL DEFAULT (0),                 -- Question ID.
    "fld_y" TINYINT DEFAULT (0),                                    -- Value of Y/N question.
    "fld_value" INTEGER DEFAULT (0),                                -- Value of quantity question.
    FOREIGN KEY("fld_software_id") REFERENCES "tbl_software"("fld_software_id") ON DELETE CASCADE
    PRIMARY KEY("fld_software_id", "fld_question_id")
);
INSERT INTO "tbl_cdr" VALUES(0, 0, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 1, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 2, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 3, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 4, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 5, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 6, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 7, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 8, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 9, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 10, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 11, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 12, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 13, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 14, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 15, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 16, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 17, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 18, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 19, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 20, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 21, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 22, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 23, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 24, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 25, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 26, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 27, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 28, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 29, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 30, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 31, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 32, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 33, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 34, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 35, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 36, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 37, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 38, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 39, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 40, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 41, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 42, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 43, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 44, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 45, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 46, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 47, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 48, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 49, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 50, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 51, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 52, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 53, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 54, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 55, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 56, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 57, 0, 0);
INSERT INTO "tbl_cdr" VALUES(0, 58, 0, 0);

CREATE TABLE "tbl_trr" (
    "fld_software_id" INTEGER NOT NULL DEFAULT (0),                 -- Software module ID.
    "fld_question_id" INTEGER NOT NULL DEFAULT (0),                 -- Question ID.
    "fld_y" TINYINT DEFAULT (0),                                    -- Value of Y/N question.
    "fld_value" INTEGER DEFAULT (0),                                -- Value of quantity question.
    FOREIGN KEY("fld_software_id") REFERENCES "tbl_software"("fld_software_id") ON DELETE CASCADE
    PRIMARY KEY("fld_software_id", "fld_question_id")
);
INSERT INTO "tbl_trr" VALUES(0, 0, 0, 0);
INSERT INTO "tbl_trr" VALUES(0, 1, 0, 0);
INSERT INTO "tbl_trr" VALUES(0, 2, 0, 0);
INSERT INTO "tbl_trr" VALUES(0, 3, 0, 0);
INSERT INTO "tbl_trr" VALUES(0, 4, 0, 0);
INSERT INTO "tbl_trr" VALUES(0, 5, 0, 0);
INSERT INTO "tbl_trr" VALUES(0, 6, 0, 0);
INSERT INTO "tbl_trr" VALUES(0, 7, 0, 0);
INSERT INTO "tbl_trr" VALUES(0, 8, 0, 0);
INSERT INTO "tbl_trr" VALUES(0, 9, 0, 0);
INSERT INTO "tbl_trr" VALUES(0, 10, 0, 0);
INSERT INTO "tbl_trr" VALUES(0, 11, 0, 0);
INSERT INTO "tbl_trr" VALUES(0, 12, 0, 0);
INSERT INTO "tbl_trr" VALUES(0, 13, 0, 0);
INSERT INTO "tbl_trr" VALUES(0, 14, 0, 0);
INSERT INTO "tbl_trr" VALUES(0, 15, 0, 0);
INSERT INTO "tbl_trr" VALUES(0, 16, 0, 0);
INSERT INTO "tbl_trr" VALUES(0, 17, 0, 0);
INSERT INTO "tbl_trr" VALUES(0, 18, 0, 0);
INSERT INTO "tbl_trr" VALUES(0, 19, 0, 0);
INSERT INTO "tbl_trr" VALUES(0, 20, 0, 0);
INSERT INTO "tbl_trr" VALUES(0, 21, 0, 0);
INSERT INTO "tbl_trr" VALUES(0, 22, 0, 0);
INSERT INTO "tbl_trr" VALUES(0, 23, 0, 0);

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

--
-- Create tables for storing validation plan information.
--
CREATE TABLE "tbl_validation" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT(0),
    "fld_validation_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_task_desc" BLOB,
    "fld_task_type" VARCHAR(256) DEFAULT(''),
    "fld_task_specification" VARCHAR(128) NOT NULL DEFAULT(''),
    "fld_measurement_unit" INTEGER DEFAULT(0),
    "fld_min_acceptable" REAL DEFAULT(0),
    "fld_mean_acceptable" REAL DEFAULT(0),
    "fld_max_acceptable" REAL DEFAULT(0),
    "fld_variance_acceptable" REAL DEFAULT(0),
    "fld_start_date" INTEGER DEFAULT(719163),
    "fld_end_date" INTEGER DEFAULT(719163),
    "fld_status" REAL DEFAULT(0),
    "fld_minimum_time" REAL DEFAULT(0),
    "fld_average_time" REAL DEFAULT(0),
    "fld_maximum_time" REAL DEFAULT(0),
    "fld_mean_time" REAL DEFAULT(0),
    "fld_time_variance" REAL DEFAULT(0),
    "fld_minimum_cost" REAL DEFAULT(0),
    "fld_average_cost" REAL DEFAULT(0),
    "fld_maximum_cost" REAL DEFAULT(0),
    "fld_mean_cost" REAL DEFAULT(0),
    "fld_cost_variance" REAL DEFAULT(0)
);

CREATE TABLE "tbl_validation_matrix" (
    "fld_validation_id" INTEGER NOT NULL,
    "fld_requirement_id" INTEGER NOT NULL,
    "fld_revision_id" INTEGER DEFAULT(1),
    PRIMARY KEY ("fld_validation_id","fld_requirement_id")
);

CREATE TABLE "tbl_validation_status" (
    "fld_revision_id" INTEGER DEFAULT(0),
    "fld_update_date" INTEGER DEFAULT(719163) NOT NULL PRIMARY KEY,
    "fld_time_remaining" REAL DEFAULT(0),
    "fld_cost_remaining" REAL DEFAULT(0)
);

--
-- Create tables for storing program incident information.
--
CREATE TABLE "tbl_incident" (
    "fld_revision_id" INTEGER DEFAULT(0),
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
    "fld_request_by" INTEGER DEFAULT(0),
    "fld_request_date" INTEGER,
    "fld_reviewed" TINYINT DEFAULT(0),
    "fld_reviewed_by" INTEGER DEFAULT(0),
    "fld_reviewed_date" INTEGER,
    "fld_approved" TINYINT DEFAULT(0),
    "fld_approved_by" INTEGER DEFAULT(0),
    "fld_approved_date" INTEGER,
    "fld_complete" TINYINT DEFAULT(0),
    "fld_complete_by" INTEGER DEFAULT(0),
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
    "fld_mode_type" INTEGER DEFAULT(0),
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

--
-- Create tables for storing survival analysis datasets.
--
CREATE TABLE "tbl_dataset" (
    "fld_dataset_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_assembly_id" INTEGER DEFAULT(0),
    "fld_description" VARCHAR(512),
    "fld_source" INTEGER DEFAULT(0),
    "fld_distribution_id" INTEGER DEFAULT(0),
    "fld_confidence" FLOAT DEFAULT(50),
    "fld_confidence_type" INTEGER DEFAULT(0),
    "fld_confidence_method" INTEGER DEFAULT(0),
    "fld_fit_method" INTEGER DEFAULT(0),
    "fld_rel_time" FLOAT DEFAULT(0),            -- Maximum failure time for filtering survival data records.
    "fld_num_rel_points" INTEGER DEFAULT(0),
    "fld_num_suspension" INTEGER DEFAULT(0),
    "fld_num_failures" INTEGER DEFAULT(0),
    "fld_scale" FLOAT DEFAULT(0),
    "fld_scale_ll" FLOAT DEFAULT(0),
    "fld_scale_ul" FLOAT DEFAULT(0),
    "fld_shape" FLOAT DEFAULT(0),
    "fld_shape_ll" FLOAT DEFAULT(0),
    "fld_shape_ul" FLOAT DEFAULT(0),
    "fld_location" FLOAT DEFAULT(0),
    "fld_location_ll" FLOAT DEFAULT(0),
    "fld_location_ul" FLOAT DEFAULT(0),
    "fld_variance_1" FLOAT DEFAULT(0),
    "fld_variance_2" FLOAT DEFAULT(0),
    "fld_variance_3" FLOAT DEFAULT(0),
    "fld_covariance_1" FLOAT DEFAULT(0),
    "fld_covariance_2" FLOAT DEFAULT(0),
    "fld_covariance_3" FLOAT DEFAULT(0),
    "fld_mhb" FLOAT DEFAULT(0),
    "fld_lp" FLOAT DEFAULT(0),
    "fld_lr" FLOAT DEFAULT(0),
    "fld_aic" FLOAT DEFAULT(0),
    "fld_bic" FLOAT DEFAULT(0),
    "fld_mle" FLOAT DEFAULT(0),
    "fld_start_time" FLOAT DEFAULT(0),          -- Minimum failure time for filtering survival data records.
    "fld_start_date" INTEGER DEFAULT(719163),   -- Start date for filtering survival data records.
    "fld_end_date" INTEGER DEFAULT(719163),     -- End date for filtering survival data records.
    "fld_nevada_chart" INTEGER DEFAULT(0)       -- Whether or not the dataset includes a Nevada chart.
);

CREATE TABLE "tbl_survival_data" (
    "fld_record_id" INTEGER NOT NULL,
    "fld_dataset_id" INTEGER NOT NULL DEFAULT(0),
    "fld_left_interval" FLOAT DEFAULT(0),
    "fld_right_interval" FLOAT DEFAULT(0),
    "fld_status" VARCHAR(64) DEFAULT(''),
    "fld_quantity" INTEGER DEFAULT(1),
    "fld_unit" VARCHAR(256),
    "fld_part_num" VARCHAR(128),
    "fld_market" VARCHAR(32),
    "fld_model" VARCHAR(32),
    "fld_tbf" FLOAT DEFAULT(0),
    "fld_mode_type" INTEGER DEFAULT(1),
    "fld_assembly_id" INTEGER DEFAULT (0),
    "fld_request_date" INTEGER DEFAULT (719163),
    PRIMARY KEY ("fld_record_id", "fld_dataset_id")
);

CREATE TABLE "tbl_nevada_chart" (
    "fld_dataset_id" INTEGER NOT NULL DEFAULT(0),
    "fld_ship_date" INTEGER DEFAULT(719163),
    "fld_number_shipped" INTEGER DEFAULT(1),
    "fld_return_date" INTEGER DEFAULT(719163),
    "fld_number_returned" INTEGER DEFAULT(0)
);

--
-- Create tables for storing program test information.
--
DROP TABLE IF EXISTS "tbl_tests";
CREATE TABLE "tbl_tests" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT(0),      -- The ID of the revision the test is associated with.
    "fld_assembly_id" INTEGER NOT NULL DEFAULT(0),      -- The ID of the assembly the test is associated with.
    "fld_test_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_test_name" VARCHAR(512),                       -- Short name of the test.
    "fld_test_description" BLOB,                        -- Long description of the test.
    "fld_test_type" INTEGER NOT NULL DEFAULT(0),        -- Type of test.
    "fld_mi" REAL DEFAULT(0),                           --
    "fld_mg" REAL DEFAULT(0),                           --
    "fld_mgp" REAL DEFAULT(0),                          --
    "fld_tr" REAL DEFAULT(0),                           --
    "fld_consumer_risk" REAL DEFAULT(0),                --
    "fld_producer_risk" REAL DEFAULT(0),                --
    "fld_rg_plan_model" INTEGER DEFAULT(0),             --
    "fld_rg_assess_model" INTEGER DEFAULT(0),           --
    "fld_num_phases" INTEGER DEFAULT(1),                --
    "fld_attachment" VARCHAR(512),                      --
    "fld_ttt" REAL DEFAULT(0),                          --
    "fld_avg_growth" REAL DEFAULT(0.3),                 --
    "fld_avg_ms" REAL DEFAULT(0),                       -- Average management strategy for test.
    "fld_prob" REAL DEFAULT(0.75),                      -- Probability of observing a failure during test.
    "fld_ttff" REAL DEFAULT(0),                         -- Time to first failure.
    "fld_avg_fef" REAL DEFAULT(0.7),                    -- Average fix effectiveness factor for test.
    "fld_grouped" INTEGER DEFAULT(0),                   -- Indicates whether or not the observed failure times are exact (0) or grouped (1).
    "fld_group_interval" REAL DEFAULT(0.0),             -- The length of the grouping interval if failure times are grouped.
    "fld_cum_time" REAL DEFAULT(0.0),                   -- Cumulative test time.
    "fld_cum_failures" INTEGER DEFAULT(0.0),            -- Cumulative number of failures.
    "fld_confidence" REAL DEFAULT(0.75)                 -- Confidence level for GoF tests, MTBF bounds, etc.
);

CREATE TABLE "tbl_rel_growth" (
    "fld_test_id" INTEGER,
    "fld_phase_id" INTEGER,
    "fld_growth_rate" REAL DEFAULT(0),                  -- Average growth rate across entire reliability growth phase.
    "fld_ms" REAL DEFAULT(0),                           -- Management strategy (i.e., the percent of problems that will be fixed).
    "fld_fef_avg" REAL DEFAULT(0),                      -- Average fix effectiveness factor across entire reliability growth phase.
    "fld_mi" REAL DEFAULT(0),                           -- Initial MTBF for the test phase.
    "fld_mf" REAL DEFAULT(0),                           -- Final MTBF for the test phase.
    "fld_ma" REAL DEFAULT(0),                           -- Average MTBF over the test phase.
    "fld_ff_prob" REAL DEFAULT(0),                      -- Probability of observing a failure during test phase.
    "fld_ti" REAL DEFAULT(0),                           -- Time to first failure.
    "fld_test_time" REAL DEFAULT(0),                    -- Total test time for the test phase.
    "fld_num_fails" INTEGER DEFAULT(0),                 -- Number of failures expected during the test phase.
    "fld_start_date" INTEGER DEFAULT(719163),           -- Start date of test phase.
    "fld_end_date" INTEGER DEFAULT(719163),             -- End date of test phase.
    "fld_weeks" REAL DEFAULT(0),                        -- Length of test phase in weeks
    "fld_test_units" INTEGER DEFAULT(0),                -- Number of test units used in test phase.
    "fld_tpu" REAL DEFAULT(0),                          -- Average test time per test unit.
    "fld_tpupw" REAL DEFAULT(0),                        -- Average test time per test unit per week.
    PRIMARY KEY ("fld_test_id", "fld_phase_id")
);

CREATE TABLE "tbl_test_status" (
    "fld_test_id" INTEGER NOT NULL,                     -- ID of the test plan.
    "fld_update_date" INTEGER DEFAULT(719163),          -- Date the update was made.
    "fld_cum_hours" REAL DEFAULT(0.0),                  -- Cumulative number of test hours when updated.
    "fld_failure_rate" REAL DEFAULT(0.0),               -- Estimated failure rate.
    "fld_mtbf" REAL DEFAULT(0.0)                        -- Estimated MTBF.
);

--
-- Create tables for storing Failure Mode, Effects, and Criticality Analysis
-- (FMECA) information.
--
DROP TABLE IF EXISTS "tbl_fmeca";
CREATE TABLE "tbl_fmeca" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT(0),      -- ID of the associated system revision.
    "fld_assembly_id" INTEGER NOT NULL DEFAULT(0),      -- ID of the associated system assembly.
    "fld_function_id" INTEGER NOT NULL DEFAULT(0),      -- ID of the associated system function.
    "fld_mode_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_mode_description" VARCHAR(512),                -- Noun description of the failure mode.
    "fld_mission_phase" VARCHAR(64),                    -- Mission phase failure mode is of concern.
    "fld_local_effect" VARCHAR(512),                    -- Local effect of the failure mode.
    "fld_next_effect" VARCHAR(512),                     -- Next higher level effect of the failure mode.
    "fld_end_effect" VARCHAR(512),                      -- System level effect of the failure mode.
    "fld_detection_method" VARCHAR(512),                -- Description of method used to detect the failure mode.
    "fld_other_indications" VARCHAR(512),               -- Description of other indications of the failure mode.
    "fld_isolation_method" VARCHAR(512),                -- Description of method(s) used to isolate the failure mode.
    "fld_design_provisions" BLOB,                       -- Description of design provisions used to mitigate the failure mode.
    "fld_operator_actions" BLOB,                        -- Description of action(s) operator(s) can take to mitigate the failure mode.
    "fld_severity_class" VARCHAR(64),                   -- Severity classification of the failure mode.
    "fld_hazard_rate_source" VARCHAR(64),               -- Source of the hazard rate information for the item being analyzed.
    "fld_failure_probability" VARCHAR(64),              -- Qualitative probability of the failure mode.
    "fld_effect_probability" REAL DEFAULT(1),           -- Quantitative probability of the worse case end effect.
    "fld_mode_ratio" REAL DEFAULT(0),                   -- Ratio of the failure mode to all failure modes of the item being analyzed.
    "fld_mode_failure_rate" REAL DEFAULT(0),            -- Hazard rate of the failure mode.
    "fld_mode_op_time" REAL DEFAULT(0),                 -- Operating time during which the failure mode is a concern.
    "fld_mode_criticality" REAL DEFAULT(0),             -- MIL-STD-1629A, Task 102 criticality of the failure mode.
    "fld_rpn_severity" VARCHAR(64),                     -- RPN severity score of the failure mode.
    "fld_rpn_severity_new" VARCHAR(64),                 -- RPN severity score of the failure mode after taking action.
    "fld_critical_item" TINYINT DEFAULT(0),             -- Whether or not failure mode causes item under analysis to be critical.
    "fld_single_point" TINYINT DEFAULT(0),              -- Whether or not failure mode causes item under analysis to be a single point of vulnerability.
    "fld_remarks" BLOB                                  -- Remarks associated with the failure mode.
);

CREATE TABLE "tbl_fmeca_mechanisms" (
    "fld_assembly_id" INTEGER NOT NULL DEFAULT(0),
    "fld_mode_id" INTEGER NOT NULL DEFAULT(0),
    "fld_mechanism_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_mechanism_description" VARCHAR(512),           -- Noun description of the failure mechanism.
    "fld_rpn_occurrence" INTEGER DEFAULT(0),            -- RPN occurrence score for the failure mechanism.
    "fld_rpn_detection" INTEGER DEFAULT(0),             -- RPN detection score for the failure mechanism.
    "fld_rpn" INTEGER DEFAULT(0),                       -- RPN score for the failure mechanism.
    "fld_rpn_occurrence_new" INTEGER DEFAULT(0),        -- RPN occurrence score for the failure mechanism after taking action.
    "fld_rpn_detection_new" INTEGER DEFAULT(0),         -- RPN detection score for the failure mechanism after taking action.
    "fld_rpn_new" INTEGER DEFAULT(0),                   -- RPN score for the failure mechanism after taking action.
    "fld_parent" VARCHAR(16) NOT NULL DEFAULT('0')
);

CREATE TABLE "tbl_fmeca_controls" (
    "fld_assembly_id" INTEGER NOT NULL DEFAULT(0),
    "fld_mode_id" INTEGER NOT NULL DEFAULT(0),
    "fld_mechanism_id" INTEGER NOT NULL DEFAULT(0),
    "fld_control_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_control_description" VARCHAR(512),             -- Noun description of the control.
    "fld_control_type" INTEGER DEFAULT(0),              -- Type of control (prevention or detection).
    "fld_parent" VARCHAR(16) NOT NULL DEFAULT('0:0')
);

CREATE TABLE "tbl_fmeca_actions" (
    "fld_assembly_id" INTEGER NOT NULL DEFAULT(0),
    "fld_mode_id" INTEGER NOT NULL DEFAULT(0),
    "fld_mechanism_id" INTEGER NOT NULL DEFAULT(0),
    "fld_action_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_action_recommended" BLOB,                      -- Noun description of the recommended action.
    "fld_action_category" INTEGER DEFAULT(0),           -- Category of the action (Engineering, Manufacturing, V&V, etc.).
    "fld_action_owner" INTEGER DEFAULT(0),              -- Owner of the action.
    "fld_action_due_date" INTEGER DEFAULT(719163),      -- Due date of the action.
    "fld_action_status" INTEGER DEFAULT(0),             -- Status of the action.
    "fld_action_taken" BLOB,                            -- Description of action that was actually taken.
    "fld_action_approved" INTEGER DEFAULT(0),           -- Approver of the actual action.
    "fld_action_approve_date" INTEGER DEFAULT(719163),  -- Date actual action was approved.
    "fld_action_closed" INTEGER DEFAULT(0),             -- Closer of the actual action.
    "fld_action_close_date" INTEGER DEFAULT(719163),    -- Date actual action was closed.
    "fld_parent" VARCHAR(16) NOT NULL DEFAULT('0:0')
);


--
-- Create tables for storing maintenance planning analyses information.
--
CREATE TABLE "tbl_significant_item" (
    "fld_assembly_id" INTEGER NOT NULL DEFAULT(0),
    "fld_q1" INTEGER DEFAULT(1),                        -- Is item a major load carrying element?
    "fld_q2" INTEGER DEFAULT(1),                        -- Does failure have adverse effect on safety or result in mission failure?
    "fld_q3" INTEGER DEFAULT(0),                        -- Is the failure rate and consumption of resources high?
    "fld_q4" INTEGER DEFAULT(0),                        -- Does the item or a similar item have an existing scheduled maintenance requirement?
    "fld_ssi" INTEGER DEFAULT(0),                       -- Assembly is or is not a structurally significant item.
    "fld_fsi" INTEGER DEFAULT(1)                        -- Assembly is or is not a functionally significant item.
);

CREATE TABLE "tbl_failure_consequences" (
    "fld_assembly_id" INTEGER NOT NULL DEFAULT(0),
    "fld_mode_id" INTEGER NOT NULL DEFAULT(0),
    "fld_q1" INTEGER DEFAULT(0),                        -- Is failure evident to operator while performing normal duties?
    "fld_q1_justify" BLOB,                              -- Justification for the answer to question 1.
    "fld_q2" INTEGER DEFAULT(1),                        -- Does the failure cause functional loss of secondary damage that could have a direct impact on operating safety?
    "fld_q2_justify" BLOB,                              -- Justification for the answer to question 2.
    "fld_q3" INTEGER DEFAULT(1),                        -- Does the hidden failure itself or in combination with a second failure have an adverse affect on operating safety?
    "fld_q3_justify" BLOB,                              -- Justification for the answer to question 3.
    "fld_safety" INTEGER DEFAULT(0),                    -- Failure mode has apparent safety consequences.
    "fld_safety_hidden" INTEGER DEFAULT(1),             -- Failure mode has hidden safety consequences.
    "fld_operation_hidden" INTEGER DEFAULT(0)           -- Failure mode has hidden operational consequences.
);

CREATE TABLE "tbl_on_condition" (
    "tbl_assembly_id" INTEGER NOT NULL DEFAULT(0),
    "tbl_mode_id" INTEGER NOT NULL DEFAULT(0),
    "fld_q1" INTEGER DEFAULT(0),                        --
    "fld_q1_justify" BLOB,                              -- Justification for the answer to question 1.
    "fld_q2" INTEGER DEFAULT(0),                        --
    "fld_q2_justify" BLOB,                              -- Justification for the answer to question 2.
    "fld_q3" INTEGER DEFAULT(0),                        --
    "fld_q3_justify" BLOB,                              -- Justification for the answer to question 3.
    "fld_pot_act_interval" REAL,                        -- Interval between potential failure and actual failure.
    "fld_dmmh_inspection" REAL,                         -- Direct maintenance man-hours for one inspection.
    "fld_inspect_labor" REAL,                           -- Cost of labor per hour for one inspection.
    "fld_inspect_mat_cost" REAL,                        -- Material costs for one inspection.
    "fld_ci" REAL,                                      -- Cost of one inspection (fld_dmmh_inspection * fld_inspect_labor + fld_inspect_mat_cost).
    "fld_dmmh_repair" REAL,                             -- Direct maintenance man-hours for one repair.
    "fld_repair_labor" REAL,                            -- Cost of labor per hour for one repair.
    "fld_repair_mat_cost" REAL,                         -- Material costs for one repair.
    "fld_ccm" REAL,                                     -- Cost of one corrective maintenance task (fld_dmmh_repair * fld_repair_labor + fld_repair_mat_cost).
    "fld_op_cost" REAL,                                 -- Cost of one lost hour of operation.
    "fld_copc" REAL,                                    -- Cost of lost operation (fld_dmmh_repair * fld_op_cost).
    "fld_cnpm" REAL,                                    -- Cost of not performing preventive maintenance (fld_ccm + fld_copc).
    "fld_dmmh_correct" REAL,                            -- Direct maintenance man-hours to correct one potential failure.
    "fld_correct_labor" REAL,                           -- Cost of labor per hour to correct one potential failure.
    "fld_correct_mat_cost" REAL,                        -- Material costs to correct one potential failure.
    "fld_pf" REAL,                                      -- Cost of correcting one potential failure (fld_dmmh_correct * fld_correct_labor + fld_correct_mat_cost).
    "fld_cpm" REAL,                                     -- Cost of one preventive maintenance task (fld_ci + fld_cpf).
    "fld_num_insp" INTEGER DEFAULT(0)                   -- Number of inspections.
);

CREATE TABLE "tbl_hard_time" (
    "fld_assembly_id" INTEGER NOT NULL DEFAULT(0),
    "fld_mode_id" INTEGER NOT NULL DEFAULT(0),
    "fld_q1" INTEGER DEFAULT(0),                        --
    "fld_q1_justify" BLOB,                              -- Justification for the answer to question 1.
    "fld_wearout_age" REAL,                             -- Age when wearout begins to dominate.
    "fld_percent_survive" REAL,                         -- Percent of items that will survive to the wearout age.
    "fld_life_limit" REAL,                              -- Safety or economic life limit imposed on the item.
    "fld_cpm" REAL,                                     -- Cost of performing one preventive maintenance task.
    "fld_cnpm" REAL,                                    -- Cost of not performing preventive maintenance.
    "fld_cbr" REAL                                      -- Cost Benefit Ratio (fld_cpm / fld_cnpm).
);

CREATE TABLE "tbl_failure_finding" (
    "fld_assembly_id" INTEGER NOT NULL DEFAULT(0),
    "fld_mode_id" INTEGER NOT NULL DEFAULT(0),
    "fld_q1" INTEGER DEFAULT(0),                        --
    "fld_q1_justify" BLOB                               -- Justification for the answer to question 1.
);

CREATE TABLE "tbl_tasks" (
    "fld_assembly_id" INTEGER NOT NULL DEFAULT(0),
    "fld_mode_id" INTEGER NOT NULL DEFAULT(0),
    "fld_task_id" INTEGER NOT NULL DEFAULT(0),
    "fld_task_type" INTEGER DEFAULT(0),                 --
    "fld_task_description" BLOB,                        -- Description of the maintenance task.
    "fld_engineer_interval" REAL,                       -- Recommended engineering interval of the maintenance task.
    "fld_mnt_level" INTEGER DEFAULT(0),                 -- Level of maintenance that will perform the task.
    "fld_ac" INTEGER,                                   --
    "fld_sci" INTEGER,                                  --
    "fld_fm" INTEGER,                                   -- Total number of high risk failure modes the item is susceptible to.
    "fld_prob_acceptable" REAL,                         -- Acceptable probability of failure.
    "fld_prob_actual" REAL,                             -- Actual probability of failure.
    "fld_prob_mf" REAL,                                 -- Actual probability of multiple failures.
    "fld_applicable" INTEGER DEFAULT(0),                --
    "fld_effective" INTEGER DEFAULT(0),                 --
    "fld_approved" INTEGER DEFAULT(0)                   --
);

CREATE TABLE "tbl_age_exploration" (
    "fld_assembly_id" INTEGER NOT NULL DEFAULT(0),
    "fld_mode_id" INTEGER NOT NULL DEFAULT(0),
    "fld_task_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_required_info" BLOB,                           -- Information required to V&V the default decision.
    "fld_prelim_task" BLOB,                             -- Description of the preliminary age exploration task.
    "fld_sample_size" INTEGER,                          -- Required minimum sample size for the age exploration task.
    "fld_mnt_level" INTEGER DEFAULT(0),                 -- Level of maintenance that will collect the age exploration data.
    "fld_study_period" REAL,                            -- Length of the age exploration study period.
    "fld_task_type" INTEGER DEFAULT(0),                 -- Type of age exploration task (SAET or DAET).
    "fld_q1" INTEGER DEFAULT(0),                        --
    "fld_q2" INTEGER DEFAULT(0),                        --
    "fld_q2_justify" BLOB,                              -- Justification for the answer to question 2.
    "fld_q3" INTEGER DEFAULT(0),                        --
    "fld_q3_justify" BLOB,                              -- Justification for the answer to question 3.
    "fld_q4" INTEGER DEFAULT(0),                        --
    "fld_q4_justify" BLOB,                              -- Justification for the answer to question 4.
    "fld_applicable" INTEGER DEFAULT(0),                --
    "fld_effective" INTEGER DEFAULT(0),                 --
    "fld_approved" INTEGER DEFAULT(0)                   --
);

-- Test tables.  Currently not used by RTK.
CREATE TABLE "tbl_revision_format" (
    "fld_field_id" INTEGER NOT NULL PRIMARY KEY,
    "fld_default_title" VARCHAR(256),
    "fld_user_title" VARCHAR(256),
    "fld_datatype" VARCHAR(16),
    "fld_cell_type" VARCHAR(16),
    "fld_position" INTEGER,
    "fld_editable" INTEGER,
    "fld_visible" INTEGER
);
INSERT INTO "tbl_revision_format" VALUES (0, 'Revision ID', 'Revision ID', 'gint', 'text', 0, 0, 0);
INSERT INTO "tbl_revision_format" VALUES (1, 'Availability, Predicted', 'Availability, Predicted', 'gfloat', 'text', 1, 0, 0);
INSERT INTO "tbl_revision_format" VALUES (2, 'Availability, Mission', 'Availability, Mission', 'gfloat', 'text', 2, 0, 0);
INSERT INTO "tbl_revision_format" VALUES (3, 'Cost', 'Cost', 'gfloat', 'text', 3, 0, 0);
INSERT INTO "tbl_revision_format" VALUES (4, 'Cost/Failure', 'Cost/Failure', 'gfloat', 'text', 4, 0, 0);
INSERT INTO "tbl_revision_format" VALUES (5, 'Cost/Hour', 'Cost/Hour', 'gfloat', 'text', 5, 0, 0);
INSERT INTO "tbl_revision_format" VALUES (6, 'Failure Rate, Active', 'Failure Rate, Active', 'gfloat', 'text', 6, 0, 0);
INSERT INTO "tbl_revision_format" VALUES (7, 'Failure Rate, Dormant', 'Failure Rate, Dormant', 'gfloat', 'text', 7, 0, 0);
INSERT INTO "tbl_revision_format" VALUES (8, 'Failure Rate, Mission', 'Failure Rate, Mission', 'gfloat', 'text', 8, 0, 0);
INSERT INTO "tbl_revision_format" VALUES (9, 'Failure Rate, Predicted', 'Failure Rate, Predicted', 'gfloat', 'text', 9, 0, 1);
INSERT INTO "tbl_revision_format" VALUES (10, 'Failure Rate, Software', 'Failure Rate, Software', 'gfloat', 'text', 10, 0, 0);
INSERT INTO "tbl_revision_format" VALUES (11, 'Mean Maintenance Time (MMT)', 'Mean Maintenance Time (MMT)', 'gfloat', 'text', 11, 0, 0);
INSERT INTO "tbl_revision_format" VALUES (12, 'Mean Corrective Maintenance Time (MCMT)', 'Mean Corrective Maintenance Time (MCMT)', 'gfloat', 'text', 12, 0, 0);
INSERT INTO "tbl_revision_format" VALUES (13, 'Mean Preventive Maintenance Time (MPMT)', 'Mean Preventive Maintenance Time (MPMT)', 'gfloat', 'text', 13, 0, 0);
INSERT INTO "tbl_revision_format" VALUES (14, 'MTBF, Mission', 'MTBF, Mission', 'gfloat', 'text', 14, 0, 0);
INSERT INTO "tbl_revision_format" VALUES (15, 'MTBF, Predicted', 'MTBF, Predicted', 'gfloat', 'text', 15, 0, 1);
INSERT INTO "tbl_revision_format" VALUES (16, 'Mean Time to Repair (MTTR)', 'Mean Time to Repair (MTTR)', 'gfloat', 'text', 16, 0, 0);
INSERT INTO "tbl_revision_format" VALUES (17, 'Revision Name', 'Revision Name', 'gchararray', 'text', 17, 1, 1);
INSERT INTO "tbl_revision_format" VALUES (18, 'Reliability, Mission', 'Reliability, Mission', 'gfloat', 'text', 18, 0, 0);
INSERT INTO "tbl_revision_format" VALUES (19, 'Reliability, Predicted', 'Reliability, Predicted', 'gfloat', 'text', 19, 0, 1);
INSERT INTO "tbl_revision_format" VALUES (20, 'Remarks', 'Remarks', 'gchararray', 'text', 20, 1, 0);
INSERT INTO "tbl_revision_format" VALUES (21, 'Total Part Count', 'Total Part Count', 'gint', 'text', 21, 0, 0);
INSERT INTO "tbl_revision_format" VALUES (22, 'Revision', 'Revision', 'gchararray', 'text', 22, 1, 0);

DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('tbl_system', 0);
INSERT INTO "sqlite_sequence" VALUES('tbl_similar_item', 0);
INSERT INTO "sqlite_sequence" VALUES('tbl_program_info', 0);
INSERT INTO "sqlite_sequence" VALUES('tbl_functions', 0);
INSERT INTO "sqlite_sequence" VALUES('tbl_revisions', 0);
INSERT INTO "sqlite_sequence" VALUES('tbl_requirements', 0);
INSERT INTO "sqlite_sequence" VALUES('tbl_validation', 0);

END TRANSACTION;
