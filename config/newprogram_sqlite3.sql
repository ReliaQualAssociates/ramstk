PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;

-- Ordinal date 719163 = January 1, 1970

DROP TABLE IF EXISTS "tbl_revisions";
CREATE TABLE "tbl_revisions" (
    "fld_revision_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,   -- Indentifier for the revision.
    "fld_availability" REAL NOT NULL DEFAULT(1),                    -- Assessed availability of the revision.
    "fld_availability_mission" REAL NOT NULL DEFAULT(1),            -- Assessed mission availability of the revision.
    "fld_cost" REAL NOT NULL DEFAULT(0),                            -- Assessed cost of the revision.
    "fld_cost_failure" REAL NOT NULL DEFAULT(0),                    -- Assessed cost per failure of the revision.
    "fld_cost_hour" REAL NOT NULL DEFAULT(0),                       -- Assessed cost to operate the revision for one hour.
    "fld_failure_rate_active" REAL NOT NULL DEFAULT(0),             -- Assessed active failure intensity of the revision.
    "fld_failure_rate_dormant" REAL NOT NULL DEFAULT(0),            -- Assessed dormant failure intensity of the revision.
    "fld_failure_rate_mission" REAL NOT NULL DEFAULT(0),            -- Assessed mission failure intensity of the revision.
    "fld_failure_rate_predicted" REAL NOT NULL DEFAULT(0),          -- Assessed failure intensity of the revision (sum of active, dormant, and software failure intensities).
    "fld_failure_rate_sftwr" REAL NOT NULL DEFAULT(0),              -- Assessed software failure intensity of the revision.
    "fld_mmt" REAL NOT NULL DEFAULT(0),                             -- Mean maintenance time (MMT) of the revision.
    "fld_mcmt" REAL NOT NULL DEFAULT(0),                            -- Mean corrective maintenance time (MCMT) of the revision.
    "fld_mpmt" REAL NOT NULL DEFAULT(0),                            -- Mean preventive maintenance time (MPMT) of the revision.
    "fld_mtbf_mission" REAL NOT NULL DEFAULT(0),                    -- Assessed mission MTBF of the revision.
    "fld_mtbf_predicted" REAL NOT NULL DEFAULT(0),                  -- Assessed MTBF of the revision.
    "fld_mttr" REAL NOT NULL DEFAULT(0),                            -- Assessed MTTR of the revision.
    "fld_name" VARCHAR(128) NOT NULL DEFAULT(''),                   -- Noun name of the revision.
    "fld_reliability_mission" REAL NOT NULL DEFAULT(1),             -- Assessed mission reliability of the revision.
    "fld_reliability_predicted" REAL NOT NULL DEFAULT(1),           -- Assessed reliability of the revision.
    "fld_remarks" BLOB NOT NULL,                                    -- Remarks about the revision.
    "fld_total_part_quantity" INTEGER NOT NULL DEFAULT(1),          -- Total number of components comprising the revision.
    "fld_revision_code" VARCHAR(8) DEFAULT(''),                     -- Alphnumeric code for the revision.
    "fld_program_time" REAL DEFAULT(0),                             -- Total expected time for all tasks in the development program.
    "fld_program_time_sd" REAL DEFAULT(0),                          -- Standard error on the total expected program time.
    "fld_program_cost" REAL DEFAULT(0),                             -- Total expected cost for all tasks in the development program.
    "fld_program_cost_sd" REAL DEFAULT(0)                           -- Standard error on the total expected program cost.
);
INSERT INTO "tbl_revisions" VALUES(0,1.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,'Original',1.0,1.0,'This is the original revision of the system.',0,'', 0.0, 0.0, 0.0, 0.0);
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
    "fld_part_next_id" INTEGER NOT NULL DEFAULT(1),                 -- Next hardware component ID.
    "fld_fmeca_prefix" VARCHAR(16) NOT NULL DEFAULT('FMEA'),        -- Default prefix to use for new FMEA.
    "fld_fmeca_next_id" INTEGER NOT NULL DEFAULT(1),
    "fld_mode_prefix" VARCHAR(16) NOT NULL DEFAULT('MODE'),
    "fld_mode_next_id" INTEGER NOT NULL DEFAULT(1),
    "fld_effect_prefix" VARCHAR(16) NOT NULL DEFAULT('EFFECT'),
    "fld_effect_next_id" INTEGER NOT NULL DEFAULT(1),
    "fld_cause_prefix" VARCHAR(16) NOT NULL DEFAULT('CAUSE'),
    "fld_cause_next_id" INTEGER NOT NULL DEFAULT(1),
    "fld_sftwr_prefix" VARCHAR(16) NOT NULL DEFAULT('MODULE'),
    "fld_sftwr_next_id" INTEGER NOT NULL DEFAULT(1),
    "fld_revision_active" TINYINT NOT NULL DEFAULT(1),
    "fld_requirement_active" TINYINT NOT NULL DEFAULT(1),
    "fld_function_active" TINYINT NOT NULL DEFAULT(1),
    "fld_hardware_active" TINYINT NOT NULL DEFAULT(1),
    "fld_sftwr_active" TINYINT NOT NULL DEFAULT(1),
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
INSERT INTO "tbl_program_info" VALUES(0,'REVISION',1,'FUNCTION',1,'ASSEMBLY',1,'PART',1,'FMEA',1,'MODE',1,'EFFECT',1,'CAUSE',1,'MODULE',1,1,1,1,1,1,1,1,0,1,1,1,1,1,'0000-00-00 00:00:00','','0000-00-00 00:00:00','','STANDARD');


--
-- Create the tables used to store matrix information.
--
DROP TABLE IF EXISTS "rtk_matrix";
CREATE TABLE "rtk_matrix" (
    "fld_revision_id" INTEGER NOT NULL,                             -- Identifier for the Revision the Matrix belongs to.
    "fld_matrix_id" INTEGER NOT NULL,                               -- Identifier for the Matrix.
    "fld_matrix_type" INTEGER NOT NULL,                             -- Type of Matrix.  0 = Function/Hardware, 1 = Function/Software, 2 = Function/Testing, 3 = Requirement/Hardware, 4 = Requirement/Software, 5 = Requirement/Validation Task, 6 = Hardware/Testing, 7 = Hardware/Validation Task
    "fld_row_id" INTEGER NOT NULL DEFAULT(0),                       -- Identifier for the row the cell is in.
    "fld_col_id" INTEGER NOT NULL DEFAULT(0),                       -- Identifier for the column the cell is in.
    "fld_parent_id" INTEGER NOT NULL DEFAULT(-1),                   -- Identifier for the parent row.
    "fld_value" VARCHAR(512) DEFAULT('0'),                          -- The value to place in cell at row/column.
    "fld_row_item_id" INTEGER DEFAULT(0),                           -- Identifer for the item being displayed in the row (the row heading).
    "fld_col_item_id" INTEGER DEFAULT(0),                           -- Identifer for the item being displayed in the column (the column heading).
    PRIMARY KEY("fld_matrix_id", "fld_row_id", "fld_col_id"),
    FOREIGN KEY("fld_revision_id") REFERENCES "tbl_revisions"("fld_revision_id") ON DELETE CASCADE
);
INSERT INTO "rtk_matrix" VALUES(0, 0, 0, 0, 0, -1, '0', 0, 0);      -- Insert one row for the System hardware.
INSERT INTO "rtk_matrix" VALUES(0, 1, 1, 0, 0, -1, '0', 0, 0);      -- Insert one row for the System software.

DROP TABLE IF EXISTS "tbl_reviews";
CREATE TABLE "tbl_reviews" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT(0),                  -- Revision design review is associated with.
    "fld_gateway_id" INTEGER NOT NULL DEFAULT(1),                   -- Design revew gateway.
    "fld_concern_id" INTEGER NOT NULL,                              -- Criteria ID.
    "fld_satisfied" INTEGER NOT NULL DEFAULT(0),                    -- Whether criteria is satisfied or not.
    "fld_action" BLOB DEFAULT(''),                                  -- Any action(s) needing to be taken.
    "fld_due_date" INTEGER NOT NULL DEFAULT(719163),                -- The due date of any action(s).
    "fld_owner" VARCHAR(128) DEFAULT('')                            -- The responsible group or individual for the action(s).
);


--
-- Create the tables for olding Mission and Environmental profile information.
DROP TABLE IF EXISTS "tbl_missions";
CREATE TABLE "tbl_missions" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT(0),                  -- Identifier for the revision.
    "fld_mission_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,    -- Identifier for the mission.
    "fld_mission_time" REAL DEFAULT(0),                             -- Total length of the mission.
    "fld_mission_units" VARCHAR(128) DEFAULT(''),                   -- Unit of time measure for the mission.
    "fld_mission_description" BLOB,                                 -- Description of the mission.
    FOREIGN KEY("fld_revision_id") REFERENCES "tbl_revisions"("fld_revision_id") ON DELETE CASCADE
);
INSERT INTO "tbl_missions" VALUES(0, 0, 10.0, '', "Default mission");

DROP TABLE IF EXISTS "tbl_mission_phase";
CREATE TABLE "tbl_mission_phase" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT(0),                  -- Identifier for the revision.
    "fld_mission_id" INTEGER NOT NULL DEFAULT(0),                   -- Identifier for the mission.
    "fld_phase_id" INTEGER PRIMARY KEY AUTOINCREMENT,               -- Identifier for the mission phase.
    "fld_phase_start" REAL,                                         -- Start time of mission phase.
    "fld_phase_end" REAL,                                           -- End time of mission phase.
    "fld_phase_name" VARCHAR(64),                                   -- Noun name of the mission phase.
    "fld_phase_description" BLOB,                                   -- Description of the mission phase.
    FOREIGN KEY("fld_mission_id") REFERENCES "tbl_missions"("fld_mission_id") ON DELETE CASCADE
);
INSERT INTO "tbl_mission_phase" VALUES(0, 0, 1, 0.0, 0.5, 'Phase I', 'This is the first phase of the default mission.');
INSERT INTO "tbl_mission_phase" VALUES(0, 0, 2, 0.5, 9.5, 'Phase II', 'This is the second phase of the default mission.');
INSERT INTO "tbl_mission_phase" VALUES(0, 0, 3, 9.5, 10.0, 'Phase III', 'This is the third phase of the default mission.');

DROP TABLE IF EXISTS "tbl_environments";
CREATE TABLE "tbl_environments" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT(0),                  -- Identifier for the revision.
    "fld_mission_id" INTEGER NOT NULL DEFAULT(0),                   -- Identifier for the mission.
    "fld_phase_id" INTEGER NOT NULL DEFAULT(0),                     -- Identifier for the mission phase.
    "fld_test_id" INTEGER NOT NULL DEFAULT(0),                      -- Identifier for the ADT/ALT/ESS test.
    "fld_condition_id" INTEGER PRIMARY KEY AUTOINCREMENT,           -- Identifier for the environmental condition.
    "fld_condition_name" VARCHAR(128),                              -- Noun name of the environmental condition.
    "fld_units" VARCHAR(64),                                        -- Units of measure for the environmental condition.
    "fld_minimum" REAL,                                             -- Minimum value of the environmental condition.
    "fld_maximum" REAL,                                             -- Maximum value of the environmental condition.
    "fld_mean" REAL,                                                -- Mean value of the environmental condition.
    "fld_variance" REAL,                                            -- Variance of the environmental condition.
    "fld_ramp_rate" REAL,                                           -- Ramp rate of the condition in test (test only).
    "fld_low_dwell_time" REAL,                                      -- Dwell time at the minimum value (test only).
    "fld_high_dwell_time" REAL,                                     -- Dwell time at the maximum value (test only).
    FOREIGN KEY("fld_mission_id") REFERENCES "tbl_missions"("fld_mission_id") ON DELETE CASCADE
);

DROP TABLE IF EXISTS "tbl_failure_definitions";
CREATE TABLE "tbl_failure_definitions" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT(0),                  -- Indentifier for the revision.
    "fld_definition_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, -- Identifier for the failure definition.
    "fld_definition" BLOB,                                          -- Definition of the failure.
    FOREIGN KEY("fld_revision_id") REFERENCES "tbl_revisions"("fld_revision_id") ON DELETE CASCADE
);

DROP TABLE IF EXISTS "rtk_units";
CREATE TABLE "rtk_units" (
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
    "fld_revision_id" INTEGER NOT NULL DEFAULT(0),                  -- Indentifier for the revision.
    "fld_function_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,   -- Indentifier for the function.
    "fld_availability" FLOAT NOT NULL DEFAULT(1),                   -- Assessed availability of the function.
    "fld_availability_mission" FLOAT NOT NULL DEFAULT(1),           -- Assessed mission availability of the function.
    "fld_code" VARCHAR(16) NOT NULL DEFAULT('Function Code'),       -- Tracking code for the function.
    "fld_cost" FLOAT NOT NULL DEFAULT(0),                           -- Assessed cost of the Function.
    "fld_failure_rate_mission" FLOAT NOT NULL DEFAULT(0),           -- Assessed mission failure intensity of the Function.
    "fld_failure_rate_predicted" FLOAT NOT NULL DEFAULT(0),         -- Assessed limiting failure intensity of the Function.
    "fld_mmt" FLOAT NOT NULL DEFAULT(0),                            -- Assessed mean maintenance time of the Function.
    "fld_mcmt" FLOAT NOT NULL DEFAULT(0),                           -- Assessed mean corrective maintenance time of the Function.
    "fld_mpmt" FLOAT NOT NULL DEFAULT(0),                           -- Assessed mean preventive maintenance time of the Function.
    "fld_mtbf_mission" FLOAT NOT NULL DEFAULT(0),                   -- Assessed mission mean time between failures of the Function.
    "fld_mtbf_predicted" FLOAT NOT NULL DEFAULT(0),                 -- Assessed limiting mean time between failures of the Function.
    "fld_mttr" FLOAT NOT NULL DEFAULT(0),                           -- Assessed mean time to repair of the Function.
    "fld_name" VARCHAR(255) DEFAULT('Function Name'),               -- Noun name of the Function.
    "fld_remarks" BLOB,                                             -- Remarks associated with the Function.
    "fld_total_mode_quantity" INTEGER NOT NULL DEFAULT(0),          -- Total number of failure modes impacting the Function.
    "fld_total_part_quantity" INTEGER NOT NULL DEFAULT(0),          -- Total number of components comprising the Function.
    "fld_type" INTEGER NOT NULL DEFAULT(0),                         --
    "fld_parent_id" INTEGER NOT NULL DEFAULT(-1),                   -- Identifer of the parent Function.
    "fld_level" INTEGER NOT NULL DEFAULT(0),                        -- Level of the Function in the Function hierarchy beginning with 0.
    "fld_safety_critical" INTEGER NOT NULL DEFAULT(0),              -- Indicates whether or not the function is safety critical.
    FOREIGN KEY("fld_revision_id") REFERENCES "tbl_revisions"("fld_revision_id") ON DELETE CASCADE
);
INSERT INTO "tbl_functions" VALUES(0,0,1.0,1.0,'UF-01',0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,'Unassigned to Function','',0,0,0,-1,0,0);


--
-- Create the tables for storing program requirements information.
--
DROP TABLE IF EXISTS "tbl_stakeholder_input";
CREATE TABLE "tbl_stakeholder_input" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT(0),                  -- Identifier for the associated revision.
    "fld_input_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,      -- Identifier for the stakeholder input.
    "fld_stakeholder" VARCHAR(128),                                 -- The name of the stakeholder providing the input.
    "fld_description" BLOB,                                         -- Description of the stakeholder input.
    "fld_group" VARCHAR(128),                                       -- Name of the affinity group this stakeholder input is assigned to.
    "fld_priority" INTEGER DEFAULT(1),                              -- Stakeholder priority for the input.
    "fld_customer_rank" INTEGER DEFAULT(1),                         -- Stakeholder satisfaction rating of the existing product for the input.
    "fld_planned_rank" INTEGER DEFAULT(3),                          -- Planned satisfaction rating of the new product for the input.
    "fld_improvement" FLOAT DEFAULT(1.0),                           -- The improvement factor on the satisfaction rating.
    "fld_overall_weight" FLOAT DEFAULT(0.0),                        -- Overall weighting factor for the need/desire.
    "fld_requirement" VARCHAR(512) DEFAULT(''),                     -- Implementing requirement.
    "fld_user_float_1" FLOAT DEFAULT(0.0),                          -- User defined float value.
    "fld_user_float_2" FLOAT DEFAULT(0.0),                          -- User defined float value.
    "fld_user_float_3" FLOAT DEFAULT(0.0),                          -- User defined float value.
    "fld_user_float_4" FLOAT DEFAULT(0.0),                          -- User defined float value.
    "fld_user_float_5" FLOAT DEFAULT(0.0),                          -- User defined float value.
    FOREIGN KEY("fld_revision_id") REFERENCES "tbl_revisions"("fld_revision_id") ON DELETE CASCADE
);

DROP TABLE IF EXISTS "tbl_requirements";
CREATE TABLE "tbl_requirements" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT(0),                  -- Identifier for the associated revision.
    "fld_requirement_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,    -- Identifier for the requirement.
    "fld_description" BLOB,                                         -- Noun description of the requirement.
    "fld_code" VARCHAR(16) DEFAULT(''),                             -- Alphanumeric code for the requirement.
    "fld_requirement_type" VARCHAR(128) DEFAULT(''),                -- Type of requirement.
    "fld_priority" INTEGER DEFAULT(1),                              -- Priority of the requirement.
    "fld_specification" VARCHAR(128) DEFAULT(''),                   -- Any industry, company, etc. specification associated  with the requirement.
    "fld_page_number" VARCHAR(32) DEFAULT(''),                      -- The page number in the associated specification.
    "fld_figure_number" VARCHAR(32) DEFAULT(''),                    -- The figure number in the associated specification.
    "fld_derived" TINYINT DEFAULT(0),                               -- Indicates whether or not the requirement is derived.
    "fld_owner" VARCHAR(128) DEFAULT(''),                           -- The responsible group or individual for the requirement.
    "fld_validated" TINYINT DEFAULT(0),                             -- Indicates whether or not the requirement has been validated.
    "fld_validated_date" INTEGER DEFAULT(719163),                   -- The ordinal date the requirement was validated.
    "fld_parent_id" INTEGER NOT NULL DEFAULT(-1),                   -- The ID of the parent requirement.
    "fld_clear" VARCHAR(512) DEFAULT(''),                           -- Answers to the clarity analysis questions.
    "fld_complete" VARCHAR(512) DEFAULT(''),                        -- Answers to the completeness analysis questions.
    "fld_consistent" VARCHAR(512) DEFAULT(''),                      -- Answers to the consistency analysis questions.
    "fld_verifiable" VARCHAR(512) DEFAULT(''),                      -- Answers to the verifiability analysis questions.
    FOREIGN KEY("fld_revision_id") REFERENCES "tbl_revisions"("fld_revision_id") ON DELETE CASCADE
);

DROP TABLE IF EXISTS "rtk_requirement_analysis";
CREATE TABLE "rtk_requirement_analysis" (
    "fld_requirement_id" INTEGER NOT NULL DEFAULT(0),               -- The ID of the requirement.
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
    "fld_verifiable_q6" TINYINT DEFAULT(0),
    FOREIGN KEY("fld_requirement_id") REFERENCES "tbl_requirements"("fld_requirement_id") ON DELETE CASCADE
);

--
-- Create tables for storing system hardware structure information.
--
DROP TABLE IF EXISTS "rtk_hardware";
CREATE TABLE "rtk_hardware" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT(0),                  -- Revision ID.
    "fld_hardware_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,   -- Hardware ID.
    "fld_alt_part_number" VARCHAR(128) DEFAULT(''),                 -- Alternate part number.
    "fld_attachments" VARCHAR(256) DEFAULT(''),                     -- Hyperlinks to any attachments.
    "fld_cage_code" VARCHAR(64) DEFAULT(''),                        -- CAGE code for assembly or part.
    "fld_category_id" INTEGER DEFAULT(0),                           -- Component category ID.
    "fld_comp_ref_des" VARCHAR(128) DEFAULT(''),                    -- Composite reference designator.
    "fld_cost" REAL DEFAULT(0),                                     -- Cost each.
    "fld_cost_failure" REAL DEFAULT(0),                             -- Cost per failure.
    "fld_cost_hour" REAL DEFAULT(0),                                -- Cost per mission hour.
    "fld_cost_type" INTEGER DEFAULT(1),                             -- How to calculate the cost (1=Assessed, 2=Specified).
    "fld_description" VARCHAR(256) DEFAULT(''),                     -- Description of the hardware.
    "fld_duty_cycle" REAL DEFAULT(100),                             -- Duty cycle in the field.
    "fld_environment_active" INTEGER DEFAULT(0),                    -- Active environment of the hardware.
    "fld_environment_dormant" INTEGER DEFAULT(0),                   -- Dormant environment of the hardware.
    "fld_figure_number" VARCHAR(32) DEFAULT(''),                    -- Specification figure number fo the hardware item.
    "fld_humidity" REAL DEFAULT(50),                                -- Humidity of the operating environment.
    "fld_lcn" VARCHAR(128) DEFAULT(''),                             -- Logistics control number of the hardware item.
    "fld_level" INTEGER DEFAULT(1),                                 -- Level in the system structure.
    "fld_manufacturer" INTEGER DEFAULT(0),                          -- Manufacturer of the hardware item.
    "fld_mission_time" REAL DEFAULT(10),                            -- Mission time of the hardware item.
    "fld_name" VARCHAR(256) DEFAULT(''),                            -- Name of the hardware item.
    "fld_nsn" VARCHAR(32) DEFAULT(''),                              -- National stock number of the hardware item.
    "fld_overstress" TINYINT NOT NULL DEFAULT(0),                   -- Whether hardware item is overstressed.
    "fld_page_number" VARCHAR(32) DEFAULT(''),                      -- Specification page number for the hardware item.
    "fld_parent_id" INTEGER DEFAULT(0),                             -- Hardware ID of the parent assembly.
    "fld_part" INTEGER DEFAULT(0),                                  -- Whether the hardware item is an assembly or a component.
    "fld_part_number" VARCHAR(128) DEFAULT(''),                     -- Part number of the hardware item.
    "fld_quantity" INTEGER DEFAULT(1),                              -- Quantity of the hardware item used in the system.
    "fld_ref_des" VARCHAR(128) DEFAULT(''),                         -- Reference designator of the hardware item.
    "fld_reliability_goal" REAL DEFAULT(1),                         -- Numerical valure of the reliability goal.
    "fld_reliability_goal_measure" INTEGER DEFAULT(0),              -- Reliability goal measure (1=Reliability, 2=Hazard Rate, 3=MTBF)
    "fld_remarks" BLOB,                                             -- Remarks associated with the hardware item.
    "fld_repairable" TINYINT DEFAULT(0),                            -- Whether the hardware item is repairable.
    "fld_rpm" REAL DEFAULT(0),                                      -- Revolutions per minute of the hardware item.
    "fld_specification_number" VARCHAR(64) DEFAULT(''),             -- Governing specification of the hardware item.
    "fld_subcategory_id" INTEGER DEFAULT(0),                        -- Component sub-category ID.
    "fld_tagged_part" TINYINT DEFAULT (0),                          -- Indicates whether or not the Hardware item is tagged.
    "fld_temperature_active" REAL DEFAULT(30),                      -- Active operating temperature.
    "fld_temperature_dormant" REAL DEFAULT(30),                     -- Dormant (storage) temperature.
    "fld_total_part_quantity" INTEGER DEFAULT(0),                   -- Total number of components comprising the assembly.
    "fld_total_power_dissipation" REAL DEFAULT(0),                  -- Total power dissipation of the assembly.
    "fld_vibration" REAL DEFAULT(0),                                -- Vibration the hardware item is exposed to in the operating environment.
    "fld_year_of_manufacture" INTEGER DEFAULT(2014),                -- Year the hardware item was manufactured.
    FOREIGN KEY("fld_revision_id") REFERENCES "tbl_revisions"("fld_revision_id") ON DELETE CASCADE
);
INSERT INTO "rtk_hardware" VALUES(0, 0, '', '', '', 0, '', 0, 0, 0, 1, '', 100, 0, 0, '', 50, '', 1, 0, 10, '', '', 0, '', -1, 0, '', 1, '', 1, 0, '', 0, 0, '', 0, 0, 30, 30, 0, 0, 0, 2014);

DROP TABLE IF EXISTS "rtk_stress";
CREATE TABLE "rtk_stress" (
    "fld_hardware_id" INTEGER NOT NULL DEFAULT(0),                  -- Hardware ID.
    "fld_current_ratio" REAL DEFAULT(1),                            -- Ratio of operating to rated current.
    "fld_junction_temperature" REAL DEFAULT(30),                    -- Junction temperature of the hardware.
    "fld_knee_temperature" REAL DEFAULT(0),                         -- Derating knee temperature.
    "fld_max_rated_temperature" REAL DEFAULT(0),                    -- Derating maximum operating temperature.
    "fld_min_rated_temperature" REAL DEFAULT(0),                    -- Derating minumum operating temperature.
    "fld_operating_current" REAL DEFAULT(0),                        -- Operating current.
    "fld_operating_power" REAL DEFAULT(0),                          -- Operating power.
    "fld_operating_voltage" REAL DEFAULT(0),                        -- Operating voltage.
    "fld_power_ratio" REAL DEFAULT(1),                              -- Ratio of operating to rated power.
    "fld_rated_current" REAL DEFAULT(1),                            -- Rated current of the hardware item.
    "fld_rated_power" REAL DEFAULT(1),                              -- Rated power of the hardware item.
    "fld_rated_voltage" REAL DEFAULT(1),                            -- Rated voltage of the hardware item.
    "fld_temperature_rise" REAL DEFAULT(0),                         -- Temperature rise of the hardware item.
    "fld_thermal_resistance" REAL DEFAULT(0),                       -- Thermal resistance of the hardware item.
    "fld_tref" REAL DEFAULT(0),                                     -- Reference temperature of the hardware item.
    "fld_voltage_ratio" REAL DEFAULT(1),                            -- Ratio of operating to rated voltage.
    FOREIGN KEY("fld_hardware_id") REFERENCES "rtk_hardware"("fld_hardware_id") ON DELETE CASCADE
);
INSERT INTO "rtk_stress" VALUES(0, 1, 30, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1);

DROP TABLE IF EXISTS "rtk_reliability";
CREATE TABLE "rtk_reliability" (
    "fld_hardware_id" INTEGER NOT NULL DEFAULT(0),                  -- Hardware ID.
    "fld_add_adj_factor" REAL DEFAULT(0),                           -- Hazard rate additive adjustment factor.
    "fld_availability_logistics" REAL DEFAULT(1),                   -- Logistics availability.
    "fld_availability_mission" REAL DEFAULT(1),                     -- Mission availability.
    "fld_avail_log_variance" REAL DEFAULT(0),                       -- Variance of the logistics availability estimate.
    "fld_avail_mis_variance" REAL DEFAULT(0),                       -- Variance of the mission availability estimate.
    "fld_failure_dist" INTEGER DEFAULT(0),                          -- Failure distribution.
    "fld_failure_parameter_1" REAL DEFAULT(0),                      -- Scale parameter.
    "fld_failure_parameter_2" REAL DEFAULT(0),                      -- Shape parameter.
    "fld_failure_parameter_3" REAL DEFAULT(0),                      -- Location parameter.
    "fld_hazard_rate_active" REAL DEFAULT(0),                       -- Active hazard rate.
    "fld_hazard_rate_dormant" REAL DEFAULT(0),                      -- Dormant hazard rate.
    "fld_hazard_rate_logistics" REAL DEFAULT(0),                    -- Logistics hazard rate.
    "fld_hazard_rate_method" INTEGER DEFAULT(1),                    -- Hazard rate calculation method to use (1=217FN2 Parts Count, 2=217FN2 Parts Stress, 3=NSWC-07).
    "fld_hazard_rate_mission" REAL DEFAULT(0),                      -- Mission hazard rate.
    "fld_hazard_rate_model" VARCHAR(512) DEFAULT(''),               -- Hazard rate mathematical model.
    "fld_hazard_rate_percent" REAL DEFAULT(0),                      -- Percent of system hazard rate attributable to this hardware item.
    "fld_hazard_rate_software" REAL DEFAULT(0),                     -- Software hazard rate.
    "fld_hazard_rate_specified" REAL DEFAULT(0),                    -- Specified hazard rate.
    "fld_hazard_rate_type" INTEGER DEFAULT(1),                      -- How the hazard rate is determined (1=Assessed, 2=Specified, Failure Rate, 3=Specified, MTBF)
    "fld_hr_active_variance" REAL DEFAULT(0),                       -- Variance of the active hazard rate estimate.
    "fld_hr_dormant_variance" REAL DEFAULT(0),                      -- Variance of the dormant hazard rate estimate.
    "fld_hr_logistics_variance" REAL DEFAULT(0),                    -- Variance of the logistics hazard rate estimate.
    "fld_hr_mission_variance" REAL DEFAULT(0),                      -- Variance of the mission hazard rate estimate.
    "fld_hr_specified_variance" REAL DEFAULT(0),                    -- Variance of the specified hazard rate estimate.
    "fld_mtbf_logistics" REAL DEFAULT(0),                           -- Logistics MTBF.
    "fld_mtbf_mission" REAL DEFAULT(0),                             -- Mission MTBF.
    "fld_mtbf_specified" REAL DEFAULT(0),                           -- Specified MTBF.
    "fld_mtbf_log_variance" REAL DEFAULT(0),                        -- Variance of the logistics MTBF estimate.
    "fld_mtbf_miss_variance" REAL DEFAULT(0),                       -- Varianec of the mission MTBF estimate.
    "fld_mtbf_spec_variance" REAL DEFAULT(0),                       -- Variance of the specified MTBF estimate.
    "fld_mult_adj_factor" REAL DEFAULT(1),                          -- Hazard rate multiplicative adjustment factor.
    "fld_reliability_logistics" REAL DEFAULT(1),                    -- Logistics reliability of the hardware item.
    "fld_reliability_mission" REAL DEFAULT(1),                      -- Mission reliability of the hardware item.
    "fld_rel_log_variance" REAL DEFAULT(0),                         -- Variance of the logistics reliability estimate.
    "fld_rel_miss_variance" REAL DEFAULT(0),                        -- Variance of the mission reliability estiamte.
    "fld_survival_analysis" INTEGER DEFAULT(0),                     -- Survival data analysis to use.
    "fld_float1" REAL NOT NULL DEFAULT(0),                          -- Float value to use as input to R(t) predictions.
    "fld_float2" REAL NOT NULL DEFAULT(0),                          -- Float value to use as input to R(t) predictions.
    "fld_float3" REAL NOT NULL DEFAULT(0),                          -- Float value to use as input to R(t) predictions.
    "fld_float4" REAL NOT NULL DEFAULT(0),                          -- Float value to use as input to R(t) predictions.
    "fld_float5" REAL NOT NULL DEFAULT(0),                          -- Float value to use as input to R(t) predictions.
    "fld_float6" REAL NOT NULL DEFAULT(0),                          -- Float value to use as input to R(t) predictions.
    "fld_float7" REAL NOT NULL DEFAULT(0),                          -- Float value to use as input to R(t) predictions.
    "fld_float8" REAL NOT NULL DEFAULT(0),                          -- Float value to use as input to R(t) predictions.
    "fld_float9" REAL NOT NULL DEFAULT(0),                          -- Float value to use as input to R(t) predictions.
    "fld_float10" REAL NOT NULL DEFAULT(0),                         -- Float value to use as input to R(t) predictions.
    "fld_float11" REAL NOT NULL DEFAULT(0),                         -- Float value result from R(t) predictions.
    "fld_float12" REAL NOT NULL DEFAULT(0),                         -- Float value result from R(t) predictions.
    "fld_float13" REAL NOT NULL DEFAULT(0),                         -- Float value result from R(t) predictions.
    "fld_float14" REAL NOT NULL DEFAULT(0),                         -- Float value result from R(t) predictions.
    "fld_float15" REAL NOT NULL DEFAULT(1),                         -- Float value result from R(t) predictions.
    "fld_float16" REAL NOT NULL DEFAULT(0),                         -- Float value result from R(t) predictions.
    "fld_float17" REAL NOT NULL DEFAULT(0),                         -- Float value result from R(t) predictions.
    "fld_float18" REAL NOT NULL DEFAULT(0),                         -- Float value result from R(t) predictions.
    "fld_float19" REAL NOT NULL DEFAULT(0),                         -- Float value result from R(t) predictions.
    "fld_float20" REAL NOT NULL DEFAULT(0),                         -- Float value result from R(t) predictions.
    "fld_int1" INTEGER NOT NULL DEFAULT(0),                         -- Integer value to use as input to R(t) predictions.
    "fld_int2" INTEGER NOT NULL DEFAULT(0),                         -- Integer value to use as input to R(t) predictions.
    "fld_int3" INTEGER NOT NULL DEFAULT(0),                         -- Integer value to use as input to R(t) predictions.
    "fld_int4" INTEGER NOT NULL DEFAULT(0),                         -- Integer value to use as input to R(t) predictions.
    "fld_int5" INTEGER NOT NULL DEFAULT(0),                         -- Integer value to use as input to R(t) predictions.
    "fld_int6" INTEGER NOT NULL DEFAULT(0),                         -- Integer value result from R(t) predictions.
    "fld_int7" INTEGER NOT NULL DEFAULT(0),                         -- Integer value result from R(t) predictions.
    "fld_int8" INTEGER NOT NULL DEFAULT(0),                         -- Integer value result from R(t) predictions.
    "fld_int9" INTEGER NOT NULL DEFAULT(0),                         -- Integer value result from R(t) predictions.
    "fld_int10" INTEGER NOT NULL DEFAULT(0),                        -- Integer value result from R(t) predictions.
    "fld_varchar1" VARCHAR(512) NOT NULL DEFAULT(''),               -- String value to use as input to R(t) predictions.
    "fld_varchar2" VARCHAR(512) NOT NULL DEFAULT(''),               -- String value to use as input to R(t) predictions.
    "fld_varchar3" VARCHAR(512) NOT NULL DEFAULT(''),               -- String value to use as input to R(t) predictions.
    "fld_varchar4" VARCHAR(512) NOT NULL DEFAULT(''),               -- String value to use as input to R(t) predictions.
    "fld_varchar5" VARCHAR(512) NOT NULL DEFAULT(''),               -- String value to use as input to R(t) predictions.
    FOREIGN KEY("fld_hardware_id") REFERENCES "rtk_hardware"("fld_hardware_id") ON DELETE CASCADE
);
INSERT INTO "rtk_reliability" VALUES(0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, '', 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', '', '', '');

DROP TABLE IF EXISTS "rtk_allocation";
CREATE TABLE "rtk_allocation" (
    "fld_hardware_id" INTEGER NOT NULL DEFAULT(0),                  -- Hardware ID associated of this allocation.
    "fld_reliability_goal" REAL DEFAULT(1),                         -- Reliability goal for the hardware item.
    "fld_hazard_rate_goal" REAL DEFAULT(0),                         -- Hazard rate goal for the hardware item.
    "fld_mtbf_goal" REAL DEFAULT(0),                                -- MTBF goal for the hardware item.
    "fld_included" TINYINT DEFAULT(1),                              -- Whether to include hardware item in allocation.
    "fld_n_sub_systems" INTEGER DEFAULT(1),                         -- Number if sub-systems in allocation.
    "fld_n_sub_elements" INTEGER DEFAULT(1),                        -- Number of sub-elements in allocation.
    "fld_weight_factor" REAL DEFAULT(1),                            -- Allocation weighting factor.
    "fld_percent_wt_factor" REAL DEFAULT(1),                        -- Percent allocation weighting factor.
    "fld_int_factor" INTEGER DEFAULT(1),                            --
    "fld_soa_factor" INTEGER DEFAULT(1),                            -- State of the Art factor (FOO).
    "fld_op_time_factor" INTEGER DEFAULT(1),                        -- Operating Time factor (FOO).
    "fld_env_factor" INTEGER DEFAULT(1),                            -- Operating Environment factor (FOO).
    "fld_availability_alloc" REAL DEFAULT(0),                       -- Allocated availability.
    "fld_reliability_alloc" REAL DEFAULT(0),                        -- Allocated reliability.
    "fld_hazard_rate_alloc" REAL DEFAULT(0),                        -- Allocated hazard rate.
    "fld_mtbf_alloc" REAL DEFAULT(0),                               -- Allocated MTBF.
    "fld_parent_id" INTEGER DEFAULT(-1),                            -- Hardware ID of the parent hardware item.
    "fld_method" INTEGER DEFAULT(0),                                -- The allocation method to use.
    "fld_goal_measure" INTEGER DEFAULT(0),                          -- The goal measure to use (R(t), h(t), or MTBF).
    FOREIGN KEY("fld_hardware_id") REFERENCES "rtk_hardware"("fld_hardware_id") ON DELETE CASCADE
);
INSERT INTO "rtk_allocation" VALUES(0, 1, 0, 0, 1, 1, 1, 1.0, 1.0, 1, 1, 1, 1, 0.0, 0.0, 0.0, 0.0, -1, 0, 0);

DROP TABLE IF EXISTS "rtk_hazard";
CREATE TABLE "rtk_hazard" (
    "fld_hardware_id" INTEGER NOT NULL DEFAULT(0),                  -- Hardware ID.
    "fld_hazard_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,     -- Hazard ID.
    "fld_potential_hazard" VARCHAR(128) DEFAULT(''),                -- Name of potential hazard.
    "fld_potential_cause" VARCHAR(512) DEFAULT(''),                 -- User-defined cause of potential hazard.
    "fld_assembly_effect" VARCHAR(512) DEFAULT(''),                 -- User-defined assembly-level effect of potential hazard.
    "fld_assembly_severity" INTEGER DEFAULT(0),                     -- Severity index of assembly-level effect.
    "fld_assembly_probability" INTEGER DEFAULT(0),                  -- Probability index of hazard.
    "fld_assembly_hri" INTEGER DEFAULT(0),                          -- Assembly-level hazard risk index (Severity x Probability).
    "fld_assembly_mitigation" BLOB DEFAULT(''),                     -- Assembly-level mitigation actions for potential hazard.
    "fld_assembly_severity_f" INTEGER DEFAULT(0),                   -- Assembly-level severity index after mitigation actions.
    "fld_assembly_probability_f" INTEGER DEFAULT(0),                -- Assembly-level probability index after mitigation actions.
    "fld_assembly_hri_f" INTEGER DEFAULT(0),                        -- Assembly-level hazard risk index after mitigation actions.
    "fld_system_effect" VARCHAR(512) DEFAULT(''),                   -- System-level effect of potential hazard.
    "fld_system_severity" INTEGER DEFAULT(0),                       -- Severity index of system-level effect.
    "fld_system_probability" INTEGER DEFAULT(0),                    -- System-level probability index of potential hazard.
    "fld_system_hri" INTEGER DEFAULT(0),                            -- System-level hazard risk index.
    "fld_system_mitigation" BLOB DEFAULT(''),                       -- System-level mitigation actions.
    "fld_system_severity_f" INTEGER DEFAULT(0),                     -- System-level severity index after mitigation actions.
    "fld_system_probability_f" INTEGER DEFAULT(0),                  -- System-level probability index after mitigation actions.
    "fld_system_hri_f" INTEGER DEFAULT(0),                          -- System-level hazard risk index after mitigation actions.
    "fld_remarks" BLOB DEFAULT(''),                                 -- Remarks associated with the potential hazard.
    "fld_function_1" VARCHAR(128) NOT NULL DEFAULT(''),             -- User-defined mathematical function 1.
    "fld_function_2" VARCHAR(128) NOT NULL DEFAULT(''),             -- User-defined mathematical function 2.
    "fld_function_3" VARCHAR(128) NOT NULL DEFAULT(''),             -- User-defined mathematical function 3.
    "fld_function_4" VARCHAR(128) NOT NULL DEFAULT(''),             -- User-defined mathematical function 4.
    "fld_function_5" VARCHAR(128) NOT NULL DEFAULT(''),             -- User-defined mathematical function 5.
    "fld_result_1" REAL DEFAULT(0),                                 -- Result of user-defined mathematical function 1.
    "fld_result_2" REAL DEFAULT(0),                                 -- Result of user-defined mathematical function 2.
    "fld_result_3" REAL DEFAULT(0),                                 -- Result of user-defined mathematical function 3.
    "fld_result_4" REAL DEFAULT(0),                                 -- Result of user-defined mathematical function 4.
    "fld_result_5" REAL DEFAULT(0),                                 -- Result of user-defined mathematical function 5.
    "fld_user_blob_1" BLOB DEFAULT(''),                             -- User-defined blob (text field) 1.
    "fld_user_blob_2" BLOB DEFAULT(''),                             -- User-defined blob (text field) 2.
    "fld_user_blob_3" BLOB DEFAULT(''),                             -- User-defined blob (text field) 3.
    "fld_user_float_1" REAL DEFAULT(0),                             -- User-defined float value 1.
    "fld_user_float_2" REAL DEFAULT(0),                             -- User-defined float value 2.
    "fld_user_float_3" REAL DEFAULT(0),                             -- User-defined float value 3.
    "fld_user_int_1" INTEGER DEFAULT(0),                            -- User-defined integer value 1.
    "fld_user_int_2" INTEGER DEFAULT(0),                            -- User-defined integer value 2.
    "fld_user_int_3" INTEGER DEFAULT(0),                            -- User-defined integer value 3.
    FOREIGN KEY("fld_hardware_id") REFERENCES "rtk_hardware"("fld_hardware_id") ON DELETE CASCADE
);
INSERT INTO "rtk_hazard" VALUES(0, 0, '', '', '', 0, 0, 0, '', 0, 0, 0, '', 0, 0, 0, '', 0, 0, 0, '', '', '', '', '', '', 0.0, 0.0, 0.0, 0.0, 0.0, '', '', '', 0.0, 0.0, 0.0, 0, 0, 0);

DROP TABLE IF EXISTS "rtk_similar_item";
CREATE TABLE "rtk_similar_item" (
    "fld_hardware_id" INTEGER NOT NULL DEFAULT(0),                  -- Hardware ID.
    "fld_sia_id" INTEGER NOT NULL DEFAULT(0),                       -- Similar item analysis ID.
    "fld_method" INTEGER NOT NULL DEFAULT(0),                       -- Similar item analysis method.
    "fld_from_quality" INTEGER DEFAULT(0),                          -- Quality level of the surrogate Hardware item.
    "fld_to_quality" INTEGER DEFAULT(0),                            -- Quality level of the new Hardware item.
    "fld_from_environment" INTEGER DEFAULT(0),                      -- Operating environment of the surrogate Hardware item.
    "fld_to_environment" INTEGER DEFAULT(0),                        -- Operating environment of the new Hardware item.
    "fld_from_temperature" FLOAT DEFAULT(30),                       -- Operating ambient temperature of the surrogate Hardware item.
    "fld_to_temperature" FLOAT DEFAULT(30),                         -- Operating ambient temperature of the new Hardware item.
    "fld_change_desc_1" BLOB DEFAULT('No changes'),
    "fld_change_factor_1" REAL DEFAULT(1),
    "fld_change_desc_2" BLOB DEFAULT('No changes'),
    "fld_change_factor_2" REAL DEFAULT(1),
    "fld_change_desc_3" BLOB DEFAULT('No changes'),
    "fld_change_factor_3" REAL DEFAULT(1),
    "fld_change_desc_4" BLOB DEFAULT('No changes'),
    "fld_change_factor_4" REAL DEFAULT(1),
    "fld_change_desc_5" BLOB DEFAULT('No changes'),
    "fld_change_factor_5" REAL DEFAULT(1),
    "fld_change_desc_6" BLOB DEFAULT('No changes'),
    "fld_change_factor_6" REAL DEFAULT(1),
    "fld_change_desc_7" BLOB DEFAULT('No changes'),
    "fld_change_factor_7" REAL DEFAULT(1),
    "fld_change_desc_8" BLOB DEFAULT('No changes'),
    "fld_change_factor_8" REAL DEFAULT(1),
    "fld_change_desc_9" BLOB DEFAULT('No changes'),
    "fld_change_factor_9" REAL DEFAULT(1),
    "fld_change_desc_10" BLOB DEFAULT('No changes'),
    "fld_change_factor_10" REAL DEFAULT(1),
    "fld_function_1" VARCHAR(128) DEFAULT(''),
    "fld_function_2" VARCHAR(128) DEFAULT(''),
    "fld_function_3" VARCHAR(128) DEFAULT(''),
    "fld_function_4" VARCHAR(128) DEFAULT(''),
    "fld_function_5" VARCHAR(128) DEFAULT(''),
    "fld_result_1" REAL DEFAULT(0),
    "fld_result_2" REAL DEFAULT(0),
    "fld_result_3" REAL DEFAULT(0),
    "fld_result_4" REAL DEFAULT(0),
    "fld_result_5" REAL DEFAULT(0),
    "fld_user_blob_1" BLOB,
    "fld_user_blob_2" BLOB,
    "fld_user_blob_3" BLOB,
    "fld_user_blob_4" BLOB,
    "fld_user_blob_5" BLOB,
    "fld_user_float_1" REAL DEFAULT(0),
    "fld_user_float_2" REAL DEFAULT(0),
    "fld_user_float_3" REAL DEFAULT(0),
    "fld_user_float_4" REAL DEFAULT(0),
    "fld_user_float_5" REAL DEFAULT(0),
    "fld_user_int_1" INTEGER DEFAULT(0),
    "fld_user_int_2" INTEGER DEFAULT(0),
    "fld_user_int_3" INTEGER DEFAULT(0),
    "fld_user_int_4" INTEGER DEFAULT(0),
    "fld_user_int_5" INTEGER DEFAULT(0),
    "fld_parent_id" INTEGER DEFAULT(0),
    PRIMARY KEY("fld_hardware_id", "fld_sia_id"),
    FOREIGN KEY("fld_hardware_id") REFERENCES "rtk_hardware"("fld_hardware_id") ON DELETE CASCADE
);

DROP TABLE IF EXISTS "rtk_maintainability";
CREATE TABLE "rtk_maintainability" (
    "fld_hardware_id" INTEGER NOT NULL DEFAULT(0),                  -- Hardware ID.
    "fld_add_adj_factor" REAL DEFAULT(0),                           -- MTTR additive adjustment factor.
    "fld_detection_fr" REAL DEFAULT(0),                             --
    "fld_detection_percent" REAL DEFAULT(0),                        --
    "fld_isolation_fr" REAL DEFAULT(0),                             --
    "fld_isolation_percent" REAL DEFAULT(0),                        --
    "fld_mcmt" REAL DEFAULT(0),                                     --
    "fld_mcmt_variance" REAL DEFAULT(0),                            --
    "fld_mmt" REAL DEFAULT(0),                                      --
    "fld_mmt_variance" REAL DEFAULT(0),                             --
    "fld_mpmt" REAL DEFAULT(0),                                     --
    "fld_mpmt_variance" REAL DEFAULT(0),                            --
    "fld_mttr" REAL DEFAULT(0),                                     --
    "fld_mttr_variance" REAL DEFAULT(0),                            --
    "fld_mttr_specified" REAL DEFAULT(0),                           --
    "fld_mttr_spec_variance" REAL DEFAULT(0),                       --
    "fld_mttr_type" INTEGER DEFAULT(1),                             --
    "fld_mult_adj_factor" REAL DEFAULT(1),                          -- MTTR multiplicative adjustment factor.
    "fld_percent_isolation_group_ri" REAL DEFAULT(0),               --
    "fld_percent_isolation_single_ri" REAL DEFAULT(0),              --
    "fld_repair_dist" INTEGER DEFAULT(0),                           --
    "fld_repair_parameter_1" REAL DEFAULT(0),                       --
    "fld_repair_parameter_2" REAL DEFAULT(0),                       --
    FOREIGN KEY("fld_hardware_id") REFERENCES "rtk_hardware"("fld_hardware_id") ON DELETE CASCADE
);

--
-- Create tables for storing Failure Mode, Effects, and Criticality Analysis
-- (FMECA) information.
--
DROP TABLE IF EXISTS "rtk_modes";
CREATE TABLE "rtk_modes" (
    "fld_hardware_id" INTEGER NOT NULL DEFAULT(0),                  -- ID of the associated system assembly.
    "fld_function_id" INTEGER NOT NULL DEFAULT(0),                  -- ID of the associated system function.
    "fld_mode_id" INTEGER PRIMARY KEY AUTOINCREMENT,                -- ID of the failure mode.
    "fld_description" VARCHAR(512),                                 -- Noun description of the failure mode.
    "fld_mission" VARCHAR(64) DEFAULT('Default Mission'),           -- Mission during which the failure mode is of concern.
    "fld_mission_phase" VARCHAR(64),                                -- Mission phase during which the failure mode is of concern.
    "fld_local_effect" VARCHAR(512),                                -- Local effect of the failure mode.
    "fld_next_effect" VARCHAR(512),                                 -- Next higher level effect of the failure mode.
    "fld_end_effect" VARCHAR(512),                                  -- System level effect of the failure mode.
    "fld_detection_method" VARCHAR(512),                            -- Description of method used to detect the failure mode.
    "fld_other_indications" VARCHAR(512),                           -- Description of other indications of the failure mode.
    "fld_isolation_method" VARCHAR(512),                            -- Description of method(s) used to isolate the failure mode.
    "fld_design_provisions" BLOB,                                   -- Description of design provisions used to mitigate the failure mode.
    "fld_operator_actions" BLOB,                                    -- Description of action(s) operator(s) can take to mitigate the failure mode.
    "fld_severity_class" VARCHAR(64),                               -- Severity classification of the failure mode.
    "fld_hazard_rate_source" VARCHAR(64),                           -- Source of the hazard rate information for the item being analyzed.
    "fld_mode_probability" VARCHAR(64),                             -- Qualitative probability of the failure mode.
    "fld_effect_probability" REAL DEFAULT(1),                       -- Quantitative probability of the worse case end effect.
    "fld_mode_ratio" REAL DEFAULT(0),                               -- Ratio of the failure mode to all failure modes of the item being analyzed.
    "fld_mode_hazard_rate" REAL DEFAULT(0),                         -- Hazard rate of the failure mode.
    "fld_mode_op_time" REAL DEFAULT(0),                             -- Operating time during which the failure mode is a concern.
    "fld_mode_criticality" REAL DEFAULT(0),                         -- MIL-STD-1629A, Task 102 criticality of the failure mode.
    "fld_rpn_severity" VARCHAR(64) DEFAULT(''),                     -- RPN severity score of the failure mode.
    "fld_rpn_severity_new" VARCHAR(64) DEFAULT(''),                 -- RPN severity score of the failure mode after taking action.
    "fld_critical_item" TINYINT DEFAULT(0),                         -- Whether or not failure mode causes item under analysis to be critical.
    "fld_single_point" TINYINT DEFAULT(0),                          -- Whether or not failure mode causes item under analysis to be a single point of vulnerability.
    "fld_remarks" BLOB,                                             -- Remarks associated with the failure mode.
    "fld_type" INTEGER DEFAULT(0),                                  -- Type of failure mode (0=functional, 1=hardware)
    FOREIGN KEY("fld_hardware_id") REFERENCES "rtk_hardware"("fld_hardware_id") ON DELETE CASCADE,
    FOREIGN KEY("fld_function_id") REFERENCES "tbl_functions"("fld_function_id") ON DELETE CASCADE
);

DROP TABLE IF EXISTS "rtk_mechanisms";
CREATE TABLE "rtk_mechanisms" (
    "fld_assembly_id" INTEGER NOT NULL DEFAULT(0),                  -- ID of the associated assembly.
    "fld_function_id" INTEGER NOT NULL DEFAULT(0),                  -- ID of the associated function.
    "fld_mode_id" INTEGER NOT NULL DEFAULT(0),                      -- ID of the associated mode.
    "fld_mechanism_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,  -- ID of the mechanism.
    "fld_description" VARCHAR(512),                                 -- Noun description of the failure mechanism.
    "fld_rpn_occurrence" INTEGER DEFAULT(0),                        -- RPN occurrence score for the failure mechanism.
    "fld_rpn_detection" INTEGER DEFAULT(0),                         -- RPN detection score for the failure mechanism.
    "fld_rpn" INTEGER DEFAULT(0),                                   -- RPN score for the failure mechanism.
    "fld_rpn_occurrence_new" INTEGER DEFAULT(0),                    -- RPN occurrence score for the failure mechanism after taking action.
    "fld_rpn_detection_new" INTEGER DEFAULT(0),                     -- RPN detection score for the failure mechanism after taking action.
    "fld_rpn_new" INTEGER DEFAULT(0),                               -- RPN score for the failure mechanism after taking action.
    "fld_include_pof" INTEGER DEFAULT(0),                           -- Indicates whether or not to include the failure mechanism in the physics of failure analysis.
    FOREIGN KEY("fld_mode_id") REFERENCES "rtk_modes"("fld_mode_id") ON DELETE CASCADE
);

DROP TABLE IF EXISTS "rtk_causes";
CREATE TABLE "rtk_causes" (
    "fld_mode_id" INTEGER NOT NULL DEFAULT(0),                      -- ID of the associated failure mode.
    "fld_mechanism_id" INTEGER NOT NULL DEFAULT(0),                 -- ID of the associated failure mechanism.
    "fld_cause_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,      -- Failure cause ID.
    "fld_description" VARCHAR(512) DEFAULT(''),                     -- Description of the failure cause.
    "fld_rpn_occurrence" INTEGER DEFAULT(0),                        -- RPN occurrence score for the failure cause.
    "fld_rpn_detection" INTEGER DEFAULT(0),                         -- RPN detection score for the failure cause.
    "fld_rpn" INTEGER DEFAULT(0),                                   -- RPN score for the failure cause.
    "fld_rpn_occurrence_new" INTEGER DEFAULT(0),                    -- RPN occurrence score for the failure cause after taking action.
    "fld_rpn_detection_new" INTEGER DEFAULT(0),                     -- RPN detection score for the failure cause after taking action.
    "fld_rpn_new" INTEGER DEFAULT(0),                               -- RPN score for the failure cause after taking action.
    FOREIGN KEY("fld_mechanism_id") REFERENCES "rtk_mechanisms"("fld_mechanism_id") ON DELETE CASCADE
);

DROP TABLE IF EXISTS "rtk_controls";
CREATE TABLE "rtk_controls" (
    "fld_mode_id" INTEGER NOT NULL DEFAULT(0),                      -- ID of the associated failure mode.
    "fld_mechanism_id" INTEGER NOT NULL DEFAULT(0),                 -- ID of the associated failure mechanism.
    "fld_cause_id" INTEGER NOT NULL DEFAULT(0),                     -- ID of the associated failure cause.
    "fld_control_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,    -- Control ID.
    "fld_control_description" VARCHAR(512),                         -- Noun description of the control.
    "fld_control_type" INTEGER DEFAULT(0),                          -- Type of control (prevention or detection).
    FOREIGN KEY("fld_mechanism_id") REFERENCES "rtk_mechanisms"("fld_mechanism_id") ON DELETE CASCADE,
    FOREIGN KEY("fld_cause_id") REFERENCES "rtk_causes"("fld_cause_id") ON DELETE CASCADE
);

DROP TABLE IF EXISTS "rtk_actions";
CREATE TABLE "rtk_actions" (
    "fld_mode_id" INTEGER NOT NULL DEFAULT(0),                      -- ID of the associated failure mode.
    "fld_mechanism_id" INTEGER NOT NULL DEFAULT(0),                 -- ID of the associated failure mechanism.
    "fld_cause_id" INTEGER NOT NULL DEFAULT(0),                     -- ID of the associated failure cause.
    "fld_action_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,     -- Action ID.
    "fld_action_recommended" BLOB,                                  -- Noun description of the recommended action.
    "fld_action_category" INTEGER DEFAULT(0),                       -- Category of the action (Engineering, Manufacturing, V&V, etc.).
    "fld_action_owner" INTEGER DEFAULT(0),                          -- Owner of the action.
    "fld_action_due_date" INTEGER DEFAULT(719163),                  -- Due date of the action.
    "fld_action_status" INTEGER DEFAULT(0),                         -- Status of the action.
    "fld_action_taken" BLOB,                                        -- Description of action that was actually taken.
    "fld_action_approved" INTEGER DEFAULT(0),                       -- Approver of the actual action.
    "fld_action_approve_date" INTEGER DEFAULT(719163),              -- Date actual action was approved.
    "fld_action_closed" INTEGER DEFAULT(0),                         -- Closer of the actual action.
    "fld_action_close_date" INTEGER DEFAULT(719163),                -- Date actual action was closed.
    FOREIGN KEY("fld_mechanism_id") REFERENCES "rtk_mechanisms"("fld_mechanism_id") ON DELETE CASCADE,
    FOREIGN KEY("fld_cause_id") REFERENCES "rtk_causes"("fld_cause_id") ON DELETE CASCADE
);

--
-- Create tables for storing physics of failure analysis information.
--
DROP TABLE IF EXISTS "rtk_op_loads";
CREATE TABLE "rtk_op_loads" (
    "fld_mechanism_id" INTEGER DEFAULT(0),                          -- ID of the failure mechanism.
    "fld_load_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,       -- ID of the operating load condition.
    "fld_load_description" VARCHAR(512) DEFAULT(''),                -- Description of the operating load condition.
    "fld_damage_model" INTEGER DEFAULT(0),                          -- Damage model describing accumulation of damage.
    "fld_priority" INTEGER DEFAULT(0),                              -- Priority of the load.
    FOREIGN KEY("fld_mechanism_id") REFERENCES "rtk_mechanisms"("fld_mechanism_id") ON DELETE CASCADE
);

DROP TABLE IF EXISTS "rtk_op_stress";
CREATE TABLE "rtk_op_stress" (
    "fld_load_id" INTEGER DEFAULT(0),                               -- ID of the operating load condition.
    "fld_stress_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,     -- ID of the operational stress.
    "fld_stress_description" VARCHAR(512) DEFAULT(''),              -- Description of the operational stress.
    "fld_measurable_parameter" INTEGER DEFAULT(0),                  -- Description of the measurable parameter for the stress.
    "fld_load_history" INTEGER DEFAULT(0),                          -- Description of the method for quantifying the stress.
    "fld_remarks" BLOB,                                             -- User remarks/notes.
    FOREIGN KEY("fld_load_id") REFERENCES "rtk_op_loads"("fld_load_id") ON DELETE CASCADE
);

DROP TABLE IF EXISTS "rtk_test_methods";
CREATE TABLE "rtk_test_methods" (
    "fld_stress_id" INTEGER NOT NULL DEFAULT(0),                    -- ID of the operating stress associated with the test.
    "fld_method_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,     -- ID of the test method.
    "fld_method_description" VARCHAR(512) DEFAULT(''),              -- Applicable test method(s) to simulate the stress.
    "fld_boundary_conditions" VARCHAR(256) DEFAULT(''),             -- Applicable boundary conditions for the test method.
    "fld_remarks" BLOB,                                             -- User remarks/notes.
    FOREIGN KEY("fld_stress_id") REFERENCES "rtk_op_stress"("fld_stress_id") ON DELETE CASCADE
);


--
-- Create tables for storing system software structure information.
--
DROP TABLE IF EXISTS "rtk_software";
CREATE TABLE "rtk_software" (
    "fld_revision_id" INTEGER DEFAULT (0),
    "fld_software_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_level_id" INTEGER DEFAULT (1),
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
    "fld_parent_id" INTEGER DEFAULT (0),
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
    "fld_f" REAL DEFAULT (0),
    "fld_cb" INTEGER DEFAULT (0),
    "fld_ncb" INTEGER DEFAULT (0),
    "fld_dr_test" INTEGER DEFAULT (0),
    "fld_test_time" FLOAT DEFAULT (0),
    "fld_dr_eot" INTEGER DEFAULT (0),
    "fld_test_time_eot" FLOAT DEFAULT (0),
    FOREIGN KEY("fld_revision_id") REFERENCES "tbl_revisions"("fld_revision_id") ON DELETE CASCADE
);
INSERT INTO "rtk_software" VALUES(0, 0, 1, "System Software", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);

--
-- Create tables for storing software reliability information.
--
DROP TABLE IF EXISTS "rtk_software_development";
CREATE TABLE "rtk_software_development" (
    "fld_software_id" INTEGER NOT NULL DEFAULT (0),                 -- Software module ID.
    "fld_question_id" INTEGER NOT NULL DEFAULT (0),                 -- Question ID.
    "fld_y" TINYINT DEFAULT (0),                                    -- Value of Y/N question.
    FOREIGN KEY("fld_software_id") REFERENCES "rtk_software"("fld_software_id") ON DELETE CASCADE
);
INSERT INTO "rtk_software_development" VALUES(0, 0, 0);
INSERT INTO "rtk_software_development" VALUES(0, 1, 0);
INSERT INTO "rtk_software_development" VALUES(0, 2, 0);
INSERT INTO "rtk_software_development" VALUES(0, 3, 0);
INSERT INTO "rtk_software_development" VALUES(0, 4, 0);
INSERT INTO "rtk_software_development" VALUES(0, 5, 0);
INSERT INTO "rtk_software_development" VALUES(0, 6, 0);
INSERT INTO "rtk_software_development" VALUES(0, 7, 0);
INSERT INTO "rtk_software_development" VALUES(0, 8, 0);
INSERT INTO "rtk_software_development" VALUES(0, 9, 0);
INSERT INTO "rtk_software_development" VALUES(0, 10, 0);
INSERT INTO "rtk_software_development" VALUES(0, 11, 0);
INSERT INTO "rtk_software_development" VALUES(0, 12, 0);
INSERT INTO "rtk_software_development" VALUES(0, 13, 0);
INSERT INTO "rtk_software_development" VALUES(0, 14, 0);
INSERT INTO "rtk_software_development" VALUES(0, 15, 0);
INSERT INTO "rtk_software_development" VALUES(0, 16, 0);
INSERT INTO "rtk_software_development" VALUES(0, 17, 0);
INSERT INTO "rtk_software_development" VALUES(0, 18, 0);
INSERT INTO "rtk_software_development" VALUES(0, 19, 0);
INSERT INTO "rtk_software_development" VALUES(0, 20, 0);
INSERT INTO "rtk_software_development" VALUES(0, 21, 0);
INSERT INTO "rtk_software_development" VALUES(0, 22, 0);
INSERT INTO "rtk_software_development" VALUES(0, 23, 0);
INSERT INTO "rtk_software_development" VALUES(0, 24, 0);
INSERT INTO "rtk_software_development" VALUES(0, 25, 0);
INSERT INTO "rtk_software_development" VALUES(0, 26, 0);
INSERT INTO "rtk_software_development" VALUES(0, 27, 0);
INSERT INTO "rtk_software_development" VALUES(0, 28, 0);
INSERT INTO "rtk_software_development" VALUES(0, 29, 0);
INSERT INTO "rtk_software_development" VALUES(0, 30, 0);
INSERT INTO "rtk_software_development" VALUES(0, 31, 0);
INSERT INTO "rtk_software_development" VALUES(0, 32, 0);
INSERT INTO "rtk_software_development" VALUES(0, 33, 0);
INSERT INTO "rtk_software_development" VALUES(0, 34, 0);
INSERT INTO "rtk_software_development" VALUES(0, 35, 0);
INSERT INTO "rtk_software_development" VALUES(0, 36, 0);
INSERT INTO "rtk_software_development" VALUES(0, 37, 0);
INSERT INTO "rtk_software_development" VALUES(0, 38, 0);
INSERT INTO "rtk_software_development" VALUES(0, 39, 0);
INSERT INTO "rtk_software_development" VALUES(0, 40, 0);
INSERT INTO "rtk_software_development" VALUES(0, 41, 0);
INSERT INTO "rtk_software_development" VALUES(0, 42, 0);

DROP TABLE IF EXISTS "rtk_srr_ssr";
CREATE TABLE "rtk_srr_ssr" (
    "fld_software_id" INTEGER NOT NULL DEFAULT (0),                 -- Software module ID.
    "fld_question_id" INTEGER NOT NULL DEFAULT (0),                 -- Question ID.
    "fld_y" TINYINT DEFAULT (0),                                    -- Value of Y/N question.
    "fld_value" INTEGER DEFAULT (0),                                -- Value of quantity question.
    FOREIGN KEY("fld_software_id") REFERENCES "rtk_software"("fld_software_id") ON DELETE CASCADE
);
INSERT INTO "rtk_srr_ssr" VALUES(0, 0, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 1, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 2, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 3, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 4, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 5, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 6, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 7, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 8, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 9, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 10, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 11, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 12, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 13, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 14, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 15, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 16, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 17, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 18, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 19, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 20, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 21, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 22, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 23, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 24, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 25, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 26, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 27, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 28, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 29, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 30, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 31, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 32, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 33, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 34, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 35, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 36, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 37, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 38, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 39, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 40, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 41, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 42, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 43, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 44, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 45, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 46, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 47, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 48, 0, 0);
INSERT INTO "rtk_srr_ssr" VALUES(0, 49, 0, 0);

DROP TABLE IF EXISTS "rtk_pdr";
CREATE TABLE "rtk_pdr" (
    "fld_software_id" INTEGER NOT NULL DEFAULT (0),                 -- Software module ID.
    "fld_question_id" INTEGER NOT NULL DEFAULT (0),                 -- Question ID.
    "fld_y" TINYINT DEFAULT (0),                                    -- Value of Y/N question.
    "fld_value" INTEGER DEFAULT (0),                                -- Value of quantity question.
    FOREIGN KEY("fld_software_id") REFERENCES "rtk_software"("fld_software_id") ON DELETE CASCADE
);
INSERT INTO "rtk_pdr" VALUES(0, 0, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 1, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 2, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 3, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 4, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 5, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 6, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 7, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 8, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 9, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 10, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 11, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 12, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 13, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 14, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 15, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 16, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 17, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 18, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 19, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 20, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 21, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 22, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 23, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 24, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 25, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 26, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 27, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 28, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 29, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 30, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 31, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 32, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 33, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 34, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 35, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 36, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 37, 0, 0);
INSERT INTO "rtk_pdr" VALUES(0, 38, 0, 0);

DROP TABLE IF EXISTS "rtk_cdr";
CREATE TABLE "rtk_cdr" (
    "fld_software_id" INTEGER NOT NULL DEFAULT (0),                 -- Software module ID.
    "fld_question_id" INTEGER NOT NULL DEFAULT (0),                 -- Question ID.
    "fld_y" TINYINT DEFAULT (0),                                    -- Value of Y/N question.
    "fld_value" INTEGER DEFAULT (0),                                -- Value of quantity question.
    FOREIGN KEY("fld_software_id") REFERENCES "rtk_software"("fld_software_id") ON DELETE CASCADE
);
INSERT INTO "rtk_cdr" VALUES(0, 0, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 1, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 2, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 3, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 4, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 5, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 6, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 7, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 8, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 9, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 10, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 11, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 12, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 13, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 14, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 15, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 16, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 17, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 18, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 19, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 20, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 21, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 22, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 23, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 24, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 25, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 26, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 27, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 28, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 29, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 30, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 31, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 32, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 33, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 34, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 35, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 36, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 37, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 38, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 39, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 40, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 41, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 42, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 43, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 44, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 45, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 46, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 47, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 48, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 49, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 50, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 51, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 52, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 53, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 54, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 55, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 56, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 57, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 58, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 59, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 60, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 61, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 62, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 63, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 64, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 65, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 66, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 67, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 68, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 69, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 70, 0, 0);
INSERT INTO "rtk_cdr" VALUES(0, 71, 0, 0);

DROP TABLE IF EXISTS "rtk_trr";
CREATE TABLE "rtk_trr" (
    "fld_software_id" INTEGER NOT NULL DEFAULT (0),                 -- Software module ID.
    "fld_question_id" INTEGER NOT NULL DEFAULT (0),                 -- Question ID.
    "fld_y" TINYINT DEFAULT (0),                                    -- Value of Y/N question.
    "fld_value" INTEGER DEFAULT (0),                                -- Value of quantity question.
    FOREIGN KEY("fld_software_id") REFERENCES "rtk_software"("fld_software_id") ON DELETE CASCADE
);
INSERT INTO "rtk_trr" VALUES(0, 0, 0, 0);
INSERT INTO "rtk_trr" VALUES(0, 1, 0, 0);
INSERT INTO "rtk_trr" VALUES(0, 2, 0, 0);
INSERT INTO "rtk_trr" VALUES(0, 3, 0, 0);
INSERT INTO "rtk_trr" VALUES(0, 4, 0, 0);
INSERT INTO "rtk_trr" VALUES(0, 5, 0, 0);
INSERT INTO "rtk_trr" VALUES(0, 6, 0, 0);
INSERT INTO "rtk_trr" VALUES(0, 7, 0, 0);
INSERT INTO "rtk_trr" VALUES(0, 8, 0, 0);
INSERT INTO "rtk_trr" VALUES(0, 9, 0, 0);
INSERT INTO "rtk_trr" VALUES(0, 10, 0, 0);
INSERT INTO "rtk_trr" VALUES(0, 11, 0, 0);
INSERT INTO "rtk_trr" VALUES(0, 12, 0, 0);
INSERT INTO "rtk_trr" VALUES(0, 13, 0, 0);
INSERT INTO "rtk_trr" VALUES(0, 14, 0, 0);
INSERT INTO "rtk_trr" VALUES(0, 15, 0, 0);
INSERT INTO "rtk_trr" VALUES(0, 16, 0, 0);
INSERT INTO "rtk_trr" VALUES(0, 17, 0, 0);
INSERT INTO "rtk_trr" VALUES(0, 18, 0, 0);
INSERT INTO "rtk_trr" VALUES(0, 19, 0, 0);
INSERT INTO "rtk_trr" VALUES(0, 20, 0, 0);
INSERT INTO "rtk_trr" VALUES(0, 21, 0, 0);
INSERT INTO "rtk_trr" VALUES(0, 22, 0, 0);
INSERT INTO "rtk_trr" VALUES(0, 23, 0, 0);

DROP TABLE IF EXISTS "rtk_software_tests";
CREATE TABLE "rtk_software_tests" (
    "fld_software_id" INTEGER NOT NULL DEFAULT (0),
    "fld_technique_id" INTEGER NOT NULL DEFAULT (0),
    "fld_recommended" TINYINT DEFAULT (0),
    "fld_used" TINYINT DEFAULT (0),
    FOREIGN KEY("fld_software_id") REFERENCES "rtk_software"("fld_software_id") ON DELETE CASCADE
);
INSERT INTO "rtk_software_tests" VALUES(0, 0, 0, 0);
INSERT INTO "rtk_software_tests" VALUES(0, 1, 0, 0);
INSERT INTO "rtk_software_tests" VALUES(0, 2, 0, 0);
INSERT INTO "rtk_software_tests" VALUES(0, 3, 0, 0);
INSERT INTO "rtk_software_tests" VALUES(0, 4, 0, 0);
INSERT INTO "rtk_software_tests" VALUES(0, 5, 0, 0);
INSERT INTO "rtk_software_tests" VALUES(0, 6, 0, 0);
INSERT INTO "rtk_software_tests" VALUES(0, 7, 0, 0);
INSERT INTO "rtk_software_tests" VALUES(0, 8, 0, 0);
INSERT INTO "rtk_software_tests" VALUES(0, 9, 0, 0);
INSERT INTO "rtk_software_tests" VALUES(0, 10, 0, 0);
INSERT INTO "rtk_software_tests" VALUES(0, 11, 0, 0);
INSERT INTO "rtk_software_tests" VALUES(0, 12, 0, 0);
INSERT INTO "rtk_software_tests" VALUES(0, 13, 0, 0);
INSERT INTO "rtk_software_tests" VALUES(0, 14, 0, 0);
INSERT INTO "rtk_software_tests" VALUES(0, 15, 0, 0);
INSERT INTO "rtk_software_tests" VALUES(0, 16, 0, 0);
INSERT INTO "rtk_software_tests" VALUES(0, 17, 0, 0);
INSERT INTO "rtk_software_tests" VALUES(0, 18, 0, 0);
INSERT INTO "rtk_software_tests" VALUES(0, 19, 0, 0);
INSERT INTO "rtk_software_tests" VALUES(0, 20, 0, 0);


--
-- Create tables for storing program test information.
--
DROP TABLE IF EXISTS "rtk_tests";
CREATE TABLE "rtk_tests" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT(0),                  -- The ID of the revision the test is associated with.
    "fld_assembly_id" INTEGER NOT NULL DEFAULT(0),                  -- The ID of the assembly the test is associated with.
    "fld_test_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,       -- The ID of the test.
    "fld_name" VARCHAR(512),                                        -- Short name of the test.
    "fld_description" BLOB,                                         -- Long description of the test.
    "fld_test_type" INTEGER NOT NULL DEFAULT(0),                    -- Type of test.
    "fld_attachment" VARCHAR(512),                                  -- URL to any attachments associated with the test.
    "fld_cum_time" REAL DEFAULT(0.0),                               -- Cumulative test time.
    "fld_cum_failures" INTEGER DEFAULT(0),                          -- Cumulative number of failures.
    "fld_confidence" REAL DEFAULT(0.75),                            -- Confidence level for GoF tests, MTBF bounds, etc.
    "fld_consumer_risk" REAL DEFAULT(0.0),                          -- The probability of the consumer accepting an item that fails to meet it's reliability requirement.
    "fld_producer_risk" REAL DEFAULT(0.0),                          -- The probability of the producer rejecting an item that actually meets it's reliability requirement.
    "fld_plan_model" INTEGER DEFAULT(0),                            -- The growth planning model to use (1=Duane, 2=Crow-AMSAA, 3=SPLAN, 4=SSPLAN).
    "fld_assess_model" INTEGER DEFAULT(0),                          -- The growth assessment model to use (1=Duane, 2=Crow-AMSAA, 3=Crow Extended)
    "fld_tr" REAL DEFAULT(0.0),                                     -- Technical requirement for the program MTBF.
    "fld_mg" REAL DEFAULT(0.0),                                     -- Goal MTBF for the entire test.
    "fld_mgp" REAL DEFAULT(0.0),                                    -- Growth potential MTBF for the entire test.
    "fld_num_phases" INTEGER DEFAULT(1),                            -- Number of growth test phases.
    "fld_ttt" REAL DEFAULT(0.0),                                    -- Total time on test over all phases.
    "fld_avg_growth" REAL DEFAULT(0.3),                             -- Average growth rate over all phases.
    "fld_avg_ms" REAL DEFAULT(0.0),                                 -- Average management strategy over all phases.
    "fld_avg_fef" REAL DEFAULT(0.7),                                -- Average fix effectiveness factor over all phases..
    "fld_prob" REAL DEFAULT(0.75),                                  -- Probability of observing a failure over all phases.
    "fld_ttff" REAL DEFAULT(0.0),                                     -- Time to first fix.
    "fld_grouped" INTEGER DEFAULT(0),                               -- Indicates whether or not the observed failure times are exact (0) or grouped (1).
    "fld_group_interval" REAL DEFAULT(0.0),                         -- The length of the grouping interval if failure times are grouped.
    "fld_se_scale" REAL DEFAULT(0.0),                               -- The standard error of the scale paramter.
    "fld_se_shape" REAL DEFAULT(0.0),                               -- The standard error of the shape parameter.
    "fld_se_cum_mean" REAL DEFAULT(0.0),                            -- The standard error of the cumulative MTBF.
    "fld_se_inst_mean" REAL DEFAULT(0.0),                           -- The standard error of the instantaneous MTBF.
    "fld_cramer_vonmises" REAL DEFAULT(0.0),                        -- The Cramer-von Mises GoF test statistic.
    "fld_chi_square" REAL DEFAULT(0.0),                             -- The chi-square GoF test statistic.
    "fld_scale_ll" REAL DEFAULT(0.0),                               -- The lower bound estimate of the scale parameter of the growth model.
    "fld_scale" REAL DEFAULT(0.0),                                  -- The point estimate of the scale parameter of the growth model.
    "fld_scale_ul" REAL DEFAULT(0.0),                               -- The upper bound estimate of the scale parameter of the growth model.
    "fld_shape_ll" REAL DEFAULT(0.0),                               -- The lower bound estimate of the shape parameter of the growth model.
    "fld_shape" REAL DEFAULT(0.0),                                  -- The point estimate of the shape parameter of the growth model.
    "fld_shape_ul" REAL DEFAULT(0.0),                               -- The upper bound estimate of the shape parameter of the growth model.
    "fld_cum_mean_ll" REAL DEFAULT(0.0),                            -- The lower bound estimate of the cumulative MTBF.
    "fld_cum_mean" REAL DEFAULT(0.0),                               -- The point estimate of the cumulative MTBF.
    "fld_cum_mean_ul" REAL DEFAULT(0.0),                            -- The upper bound estimate of the cumulative MTBF.
    "fld_inst_mean_ll" REAL DEFAULT(0.0),                           -- The lower bound estimate of the instantaneous MTBF.
    "fld_inst_mean" REAL DEFAULT(0.0),                              -- The point estimate of the instantaneous MTBF.
    "fld_inst_mean_ul" REAL DEFAULT(0.0)                            -- The upper bound estimate of the instantaneous MTBF.
);

DROP TABLE IF EXISTS "rtk_growth_testing";
CREATE TABLE "rtk_growth_testing" (
    "fld_test_id" INTEGER,                                          -- The ID of the test.
    "fld_phase_id" INTEGER,                                         -- The ID of the test phase.
    "fld_p_growth_rate" REAL DEFAULT(0),                            -- Planned average growth rate for the test phase.
    "fld_p_ms" REAL DEFAULT(0),                                     -- Planned management strategy (i.e., the percent of problems that will be fixed) for the test phase.
    "fld_p_fef_avg" REAL DEFAULT(0),                                -- Planned average fix effectiveness factor for the test phase.
    "fld_p_prob" REAL DEFAULT(0),                                   -- Planned probability of observing a failure during the test phase.
    "fld_p_mi" REAL DEFAULT(0),                                     -- Planned initial MTBF for the test phase.
    "fld_p_mf" REAL DEFAULT(0),                                     -- Planned final MTBF for the test phase.
    "fld_p_ma" REAL DEFAULT(0),                                     -- Planned average MTBF over the test phase.
    "fld_p_test_time" REAL DEFAULT(0),                              -- Planned total test time for the test phase.
    "fld_p_num_fails" INTEGER DEFAULT(0),                           -- Planned number of failures expected during the test phase.
    "fld_p_start_date" INTEGER DEFAULT(719163),                     -- Planned start date of test phase.
    "fld_p_end_date" INTEGER DEFAULT(719163),                       -- Planned end date of test phase.
    "fld_p_weeks" REAL DEFAULT(0),                                  -- Planned length of test phase in weeks.
    "fld_p_test_units" INTEGER DEFAULT(0),                          -- Planned number of test units used in test phase.
    "fld_p_tpu" REAL DEFAULT(0),                                    -- Planned average test time per test unit.
    "fld_p_tpupw" REAL DEFAULT(0),                                  -- Planned average test time per test unit per week.
    "fld_o_growth_rate" REAL DEFAULT(0),                            -- Observed average growth rate across entire reliability growth phase.
    "fld_o_ms" REAL DEFAULT(0),                                     -- Observed management strategy for the test phase.
    "fld_o_fef_avg" REAL DEFAULT(0),                                -- Observed average fix effectiveness factor for the test phase.
    "fld_o_mi" REAL DEFAULT(0),                                     -- Observed initial MTBF for the test phase.
    "fld_o_mf" REAL DEFAULT(0),                                     -- Observed final MTBF for the test phase.
    "fld_o_ma" REAL DEFAULT(0),                                     -- Observed average MTBF over the test phase.
    "fld_o_test_time" REAL DEFAULT(0),                              -- Observed total test time for the test phase.
    "fld_o_num_fails" INTEGER DEFAULT(0),                           -- Observed number of failures during the test phase.
    "fld_o_ttff" REAL DEFAULT(0),                                   -- Observed time to first fix.
    "fld_o_cum_mean_ll" REAL DEFAULT(0),                            -- Observed lower limit on the cumulative mean.
    "fld_o_cum_mean" REAL DEFAULT(0),                               -- Observed point estimate of the cumulative mean.
    "fld_o_cum_mean_ul" REAL DEFAULT(0),                            -- Observed upper limit on the cumulative mean.
    "fld_o_inst_mean_ll" REAL DEFAULT(0),                           -- Observed lower limit on the instantaneous mean.
    "fld_o_inst_mean" REAL DEFAULT(0),                              -- Observed point estimate for the instantaneous mean.
    "fld_o_inst_mean_ul" REAL DEFAULT(0),                           -- Observed upper limit on the instantaneous mean.
    PRIMARY KEY ("fld_test_id", "fld_phase_id")
);


--
-- Create tables for storing accelerated test planning information.
--
DROP TABLE IF EXISTS "tbl_pof";
CREATE TABLE "tbl_pof" (
    "fld_assembly_id" INTEGER DEFAULT(0),                           -- ID of the hardware assembly.
    "fld_mode_id" INTEGER DEFAULT(0),                               -- ID of the failure mode.
    "fld_mechanism_id" INTEGER DEFAULT(0),                          -- ID of the failure mechanism.
    "fld_load_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,       -- ID of the operating load condition.
    "fld_load_description" VARCHAR(512) DEFAULT(''),                -- Description of the operating load condition.
    "fld_primary_stress" VARCHAR(256) DEFAULT(''),                  -- Description of the primary operational stress.
    "fld_secondary_stress" VARCHAR(256) DEFAULT(''),                -- Description of the secondary operational stress.
    "fld_tertiary_stress" VARCHAR(256) DEFAULT(''),                 -- Description of the tertiary operational stress.
    "fld_priority" VARCHAR(256) DEFAULT(''),                        -- Priority of the failure mechanism.
    "fld_primary_measurable" VARCHAR(256) DEFAULT(''),              -- Description of the measurable parameter for the primary stress.
    "fld_primary_load_history" VARCHAR(256) DEFAULT(''),            -- Description of the method for quantifying the primary stress.
    "fld_secondary_measureable" VARCHAR(256) DEFAULT(''),           -- Description of the measurable parameter for the secondary stress.
    "fld_secondary_load_history" VARCHAR(256) DEFAULT(''),          -- Description of the method for quantifying the secondary stress.
    "fld_tertiary_measurable" VARCHAR(256) DEFAULT(''),             -- Description of the measurable parameter for the tertiary stress.
    "fld_tertiary_load_history" VARCHAR(256) DEFAULT(''),           -- Description of the method for quantifying the tertiary stress.
    "fld_remarks" BLOB,                                             -- User remarks/notes.
    "fld_parent" VARCHAR(16) NOT NULL DEFAULT('0')                  -- Path of the parent failure mode or failure mechanism.
);


--
-- Create tables for storing validation plan information.
--
DROP TABLE IF EXISTS "rtk_validation";
CREATE TABLE "rtk_validation" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT(0),
    "fld_validation_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_task_desc" BLOB,
    "fld_task_type" INTEGER DEFAULT(0),
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
    "fld_cost_variance" REAL DEFAULT(0),
    "fld_confidence" REAL DEFAULT(95.0)
);

DROP TABLE IF EXISTS "rtk_validation_status";
CREATE TABLE "rtk_validation_status" (
    "fld_revision_id" INTEGER DEFAULT(0),
    "fld_update_date" INTEGER DEFAULT CURRENT_TIMESTAMP NOT NULL PRIMARY KEY,
    "fld_time_remaining" REAL DEFAULT(0),
    "fld_cost_remaining" REAL DEFAULT(0)
);

DROP TABLE IF EXISTS "rtk_validation_matrix";
CREATE TABLE "rtk_validation_matrix" (
    "fld_validation_id" INTEGER NOT NULL,
    "fld_requirement_id" INTEGER NOT NULL,
    "fld_revision_id" INTEGER DEFAULT(1),
    PRIMARY KEY ("fld_validation_id", "fld_requirement_id")
);

--
-- Create tables for storing program incident information.
--
DROP TABLE IF EXISTS "rtk_incident";
CREATE TABLE "rtk_incident" (
    "fld_revision_id" INTEGER DEFAULT(0),
    "fld_incident_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_incident_category" INTEGER DEFAULT(0),
    "fld_incident_type" INTEGER DEFAULT(0),
    "fld_short_description" VARCHAR(512),
    "fld_long_description" BLOB,
    "fld_criticality" INTEGER DEFAULT(0),
    "fld_detection_method" INTEGER DEFAULT(0),
    "fld_remarks" BLOB,
    "fld_status" INTEGER DEFAULT(0),
    "fld_test_found" VARCHAR(512),
    "fld_test_case" VARCHAR(512),
    "fld_execution_time" FLOAT DEFAULT(0),
    "fld_unit" VARCHAR(256) DEFAULT(''),
    "fld_cost" FLOAT DEFAULT(0),
    "fld_incident_age" INTEGER DEFAULT(0),
    "fld_hardware_id" INTEGER DEFAULT(0),
    "fld_sftwr_id" INTEGER DEFAULT(0),
    "fld_request_by" INTEGER DEFAULT(0),
    "fld_request_date" INTEGER DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "fld_reviewed" TINYINT DEFAULT(0),
    "fld_reviewed_by" INTEGER DEFAULT(0),
    "fld_reviewed_date" INTEGER DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "fld_approved" TINYINT DEFAULT(0),
    "fld_approved_by" INTEGER DEFAULT(0),
    "fld_approved_date" INTEGER DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "fld_complete" TINYINT DEFAULT(0),
    "fld_complete_by" INTEGER DEFAULT(0),
    "fld_complete_date" INTEGER DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "fld_life_cycle" INTEGER DEFAULT(0),
    "fld_analysis" BLOB,
    "fld_accepted" TINYINT DEFAULT(0)
);

DROP TABLE IF EXISTS "rtk_incident_detail";
CREATE TABLE "rtk_incident_detail" (
    "fld_incident_id" INTEGER NOT NULL,
    "fld_component_id" INTEGER NOT NULL,
    "fld_age_at_incident" REAL DEFAULT (0),
    "fld_failure" TINYINT DEFAULT (0),
    "fld_suspension" TINYINT DEFAULT (0),
    "fld_cnd_nff" TINYINT DEFAULT (0),
    "fld_occ_fault" TINYINT DEFAULT (0),
    "fld_initial_installation" TINYINT DEFAULT (0),
    "fld_interval_censored" TINYINT DEFAULT (0),
    "fld_use_op_time" TINYINT DEFAULT (0),
    "fld_use_cal_time" TINYINT DEFAULT (0),
    "fld_ttf" REAL DEFAULT (0),
    "fld_mode_type" INTEGER DEFAULT(0),
    "fld_relevant_1" TINYINT DEFAULT (-1),
    "fld_relevant_2" TINYINT DEFAULT (-1),
    "fld_relevant_3" TINYINT DEFAULT (-1),
    "fld_relevant_4" TINYINT DEFAULT (-1),
    "fld_relevant_5" TINYINT DEFAULT (-1),
    "fld_relevant_6" TINYINT DEFAULT (-1),
    "fld_relevant_7" TINYINT DEFAULT (-1),
    "fld_relevant_8" TINYINT DEFAULT (-1),
    "fld_relevant_9" TINYINT DEFAULT (-1),
    "fld_relevant_1-1" TINYINT DEFAULT (-1),
    "fld_relevant_11" TINYINT DEFAULT (-1),
    "fld_relevant_12" TINYINT DEFAULT (-1),
    "fld_relevant_13" TINYINT DEFAULT (-1),
    "fld_relevant_14" TINYINT DEFAULT (-1),
    "fld_relevant_15" TINYINT DEFAULT (-1),
    "fld_relevant_16" TINYINT DEFAULT (-1),
    "fld_relevant_17" TINYINT DEFAULT (-1),
    "fld_relevant_18" TINYINT DEFAULT (-1),
    "fld_relevant_19" TINYINT DEFAULT (-1),
    "fld_relevant_2-1" TINYINT DEFAULT (-1),
    "fld_relevant" TINYINT DEFAULT (-1),
    "fld_chargeable_1" TINYINT DEFAULT (-1),
    "fld_chargeable_2" TINYINT DEFAULT (-1),
    "fld_chargeable_3" TINYINT DEFAULT (-1),
    "fld_chargeable_4" TINYINT DEFAULT (-1),
    "fld_chargeable_5" TINYINT DEFAULT (-1),
    "fld_chargeable_6" TINYINT DEFAULT (-1),
    "fld_chargeable_7" TINYINT DEFAULT (-1),
    "fld_chargeable_8" TINYINT DEFAULT (-1),
    "fld_chargeable_9" TINYINT DEFAULT (-1),
    "fld_chargeable_1-1" TINYINT DEFAULT (-1),
    "fld_chargeable" TINYINT DEFAULT (-1),
    PRIMARY KEY ("fld_incident_id", "fld_component_id")
);

DROP TABLE IF EXISTS "rtk_incident_actions";
CREATE TABLE "rtk_incident_actions" (
    "fld_incident_id" INTEGER NOT NULL,
    "fld_action_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_prescribed_action" BLOB DEFAULT(''),
    "fld_action_taken" BLOB DEFAULT(''),
    "fld_action_owner" INTEGER DEFAULT(0),
    "fld_due_date" INTEGER DEFAULT (datetime(CURRENT_TIMESTAMP, '30 days')),
    "fld_status" INTEGER NOT NULL DEFAULT (0),
    "fld_approved_by" INTEGER DEFAULT(0),
    "fld_approved_date" INTEGER DEFAULT(0),
    "fld_approved" INTEGER DEFAULT(0),
    "fld_closed_by" INTEGER DEFAULT(0),
    "fld_closed_date" INTEGER DEFAULT(0),
    "fld_closed" INTEGER DEFAULT(0)
);

--
-- Create tables for storing survival analysis datasets.
--
DROP TABLE IF EXISTS "rtk_survival";
CREATE TABLE "rtk_survival" (
    "fld_revision_id" INTEGER DEFAULT(0),
    "fld_survival_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_assembly_id" INTEGER DEFAULT(0),
    "fld_description" VARCHAR(512),
    "fld_source" INTEGER DEFAULT(0),                -- Source of failure data: 0=field, 1=growth test
    "fld_distribution_id" INTEGER DEFAULT(0),
    "fld_confidence" FLOAT DEFAULT(50),
    "fld_confidence_type" INTEGER DEFAULT(0),
    "fld_confidence_method" INTEGER DEFAULT(0),
    "fld_fit_method" INTEGER DEFAULT(0),
    "fld_rel_time" FLOAT DEFAULT(0),                -- Maximum failure time for filtering survival data records.
    "fld_num_rel_points" INTEGER DEFAULT(0),
    "fld_num_suspension" INTEGER DEFAULT(0),
    "fld_num_failures" INTEGER DEFAULT(0),
    "fld_scale_ll" FLOAT DEFAULT(0),
    "fld_scale" FLOAT DEFAULT(0),
    "fld_scale_ul" FLOAT DEFAULT(0),
    "fld_shape_ll" FLOAT DEFAULT(0),
    "fld_shape" FLOAT DEFAULT(0),
    "fld_shape_ul" FLOAT DEFAULT(0),
    "fld_location_ll" FLOAT DEFAULT(0),
    "fld_location" FLOAT DEFAULT(0),
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
    "fld_start_time" FLOAT DEFAULT(0),              -- Minimum failure time for filtering survival data records.
    "fld_start_date" INTEGER DEFAULT(719163),       -- Start date for filtering survival data records.
    "fld_end_date" INTEGER DEFAULT(719163),         -- End date for filtering survival data records.
    "fld_nevada_chart" INTEGER DEFAULT(0)           -- Whether or not the dataset includes a Nevada chart.
);

DROP TABLE IF EXISTS "rtk_survival_data";
CREATE TABLE "rtk_survival_data" (
    "fld_survival_id" INTEGER NOT NULL DEFAULT(0),
    "fld_dataset_id" INTEGER NOT NULL DEFAULT(0),
    "fld_record_id" INTEGER NOT NULL DEFAULT(0),
    "fld_name" VARCHAR(256) DEFAULT(0),             -- The name of the failed assembly.
    "fld_source" INTEGER DEFAULT(0),                -- Source of failure data: 0=field, 1=growth test
    "fld_failure_date" INTEGER DEFAULT(719163),     -- Date the failure occurred or was discovered.
    "fld_left_interval" FLOAT DEFAULT(0),           -- Beginning time of the failure interval (same as right for exact failure times).
    "fld_right_interval" FLOAT DEFAULT(0),          -- Ending time of the failure interval (same as left for exact failure times).
    "fld_status" INTEGER DEFAULT(0),                -- Indicates whether the record is an event (0), right-censored (1), left-censored (2), or interval censored (3).
    "fld_quantity" INTEGER DEFAULT(1),              -- The number of failures occuring at the failure time.
    "fld_tbf" FLOAT DEFAULT(0),                     -- Time between failures for the assembly ID.
    "fld_mode_type" INTEGER DEFAULT(1),             -- The failure mode type.
    "fld_nevada_chart" INTEGER DEFAULT(0),          -- Indicates data set is in a Nevada chart format.
    "fld_ship_date" INTEGER DEFAULT(719163),        -- Date shipped (used with Nevada charts).
    "fld_number_shipped" INTEGER DEFAULT(1),        -- Number of items shipped  (used with Nevada charts).
    "fld_return_date" INTEGER DEFAULT(719163),      -- Date of return (used with Nevada charts).
    "fld_number_returned" INTEGER DEFAULT(0),       -- Number returned (used with Nevada charts).
    "fld_user_float_1" FLOAT DEFAULT(0),
    "fld_user_float_2" FLOAT DEFAULT(0),
    "fld_user_float_3" FLOAT DEFAULT(0),
    "fld_user_integer_1" INTEGER DEFAULT(0),
    "fld_user_integer_2" INTEGER DEFAULT(0),
    "fld_user_integer_3" INTEGER DEFAULT(0),
    "fld_user_string_1" VARCHAR(256),
    "fld_user_string_2" VARCHAR(256),
    "fld_user_string_3" VARCHAR(256),
    PRIMARY KEY("fld_survival_id", "fld_dataset_id", "fld_record_id"),
    FOREIGN KEY("fld_survival_id") REFERENCES "rtk_survival"("fld_survival_id") ON DELETE CASCADE
);

--
-- Create tables for storing maintenance planning analysis information.
--
DROP TABLE IF EXISTS "rtk_significant_item";
CREATE TABLE "rtk_significant_item" (
    "fld_assembly_id" INTEGER NOT NULL DEFAULT(0),
    "fld_q1" INTEGER DEFAULT(1),                                    -- Is item a major load carrying element?
    "fld_q2" INTEGER DEFAULT(1),                                    -- Does failure have adverse effect on safety or result in mission failure?
    "fld_q3" INTEGER DEFAULT(0),                                    -- Is the failure rate and consumption of resources high?
    "fld_q4" INTEGER DEFAULT(0),                                    -- Does the item or a similar item have an existing scheduled maintenance requirement?
    "fld_ssi" INTEGER DEFAULT(0),                                   -- Assembly is or is not a structurally significant item.
    "fld_fsi" INTEGER DEFAULT(1)                                    -- Assembly is or is not a functionally significant item.
);

DROP TABLE IF EXISTS "rtk_failure_consequences";
CREATE TABLE "rtk_failure_consequences" (
    "fld_assembly_id" INTEGER NOT NULL DEFAULT(0),
    "fld_mode_id" INTEGER NOT NULL DEFAULT(0),
    "fld_q1" INTEGER DEFAULT(0),                                    -- Is failure evident to operator while performing normal duties?
    "fld_q1_justify" BLOB,                                          -- Justification for the answer to question 1.
    "fld_q2" INTEGER DEFAULT(1),                                    -- Does the failure cause functional loss of secondary damage that could have a direct impact on operating safety?
    "fld_q2_justify" BLOB,                                          -- Justification for the answer to question 2.
    "fld_q3" INTEGER DEFAULT(1),                                    -- Does the hidden failure itself or in combination with a second failure have an adverse affect on operating safety?
    "fld_q3_justify" BLOB,                                          -- Justification for the answer to question 3.
    "fld_safety" INTEGER DEFAULT(0),                                -- Failure mode has apparent safety consequences.
    "fld_safety_hidden" INTEGER DEFAULT(1),                         -- Failure mode has hidden safety consequences.
    "fld_operation_hidden" INTEGER DEFAULT(0)                       -- Failure mode has hidden operational consequences.
);

DROP TABLE IF EXISTS "rtk_on_condition";
CREATE TABLE "rtk_on_condition" (
    "tbl_assembly_id" INTEGER NOT NULL DEFAULT(0),
    "tbl_mode_id" INTEGER NOT NULL DEFAULT(0),
    "fld_q1" INTEGER DEFAULT(0),                                    --
    "fld_q1_justify" BLOB,                                          -- Justification for the answer to question 1.
    "fld_q2" INTEGER DEFAULT(0),                                    --
    "fld_q2_justify" BLOB,                                          -- Justification for the answer to question 2.
    "fld_q3" INTEGER DEFAULT(0),                                    --
    "fld_q3_justify" BLOB,                                          -- Justification for the answer to question 3.
    "fld_pot_act_interval" REAL,                                    -- Interval between potential failure and actual failure.
    "fld_dmmh_inspection" REAL,                                     -- Direct maintenance man-hours for one inspection.
    "fld_inspect_labor" REAL,                                       -- Cost of labor per hour for one inspection.
    "fld_inspect_mat_cost" REAL,                                    -- Material costs for one inspection.
    "fld_ci" REAL,                                                  -- Cost of one inspection (fld_dmmh_inspection * fld_inspect_labor + fld_inspect_mat_cost).
    "fld_dmmh_repair" REAL,                                         -- Direct maintenance man-hours for one repair.
    "fld_repair_labor" REAL,                                        -- Cost of labor per hour for one repair.
    "fld_repair_mat_cost" REAL,                                     -- Material costs for one repair.
    "fld_ccm" REAL,                                                 -- Cost of one corrective maintenance task (fld_dmmh_repair * fld_repair_labor + fld_repair_mat_cost).
    "fld_op_cost" REAL,                                             -- Cost of one lost hour of operation.
    "fld_copc" REAL,                                                -- Cost of lost operation (fld_dmmh_repair * fld_op_cost).
    "fld_cnpm" REAL,                                                -- Cost of not performing preventive maintenance (fld_ccm + fld_copc).
    "fld_dmmh_correct" REAL,                                        -- Direct maintenance man-hours to correct one potential failure.
    "fld_correct_labor" REAL,                                       -- Cost of labor per hour to correct one potential failure.
    "fld_correct_mat_cost" REAL,                                    -- Material costs to correct one potential failure.
    "fld_pf" REAL,                                                  -- Cost of correcting one potential failure (fld_dmmh_correct * fld_correct_labor + fld_correct_mat_cost).
    "fld_cpm" REAL,                                                 -- Cost of one preventive maintenance task (fld_ci + fld_cpf).
    "fld_num_insp" INTEGER DEFAULT(0)                               -- Number of inspections.
);

DROP TABLE IF EXISTS "rtk_hard_time";
CREATE TABLE "rtk_hard_time" (
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

DROP TABLE IF EXISTS "rtk_failure_finding";
CREATE TABLE "rtk_failure_finding" (
    "fld_assembly_id" INTEGER NOT NULL DEFAULT(0),
    "fld_mode_id" INTEGER NOT NULL DEFAULT(0),
    "fld_q1" INTEGER DEFAULT(0),                        --
    "fld_q1_justify" BLOB                               -- Justification for the answer to question 1.
);

DROP TABLE IF EXISTS "rtk_tasks";
CREATE TABLE "rtk_tasks" (
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

DROP TABLE IF EXISTS "rtk_age_exploration";
CREATE TABLE "rtk_age_exploration" (
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

--DELETE FROM "sqlite_sequence";
--INSERT INTO "sqlite_sequence" VALUES('tbl_system', 0);
--INSERT INTO "sqlite_sequence" VALUES('tbl_similar_item', 0);
--INSERT INTO "sqlite_sequence" VALUES('tbl_program_info', 0);
--INSERT INTO "sqlite_sequence" VALUES('tbl_functions', 0);
--INSERT INTO "sqlite_sequence" VALUES('tbl_revisions', 0);
--INSERT INTO "sqlite_sequence" VALUES('tbl_requirements', 0);
--INSERT INTO "sqlite_sequence" VALUES('tbl_validation', 0);

--END TRANSACTION;
