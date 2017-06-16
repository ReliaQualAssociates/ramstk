PRAGMA foreign_keys=ON;
-- BEGIN TRANSACTION;

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
    "fld_failure_rate_software" REAL NOT NULL DEFAULT(0),           -- Assessed software failure intensity of the revision.
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
INSERT INTO "tbl_revisions" VALUES(0,1.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,'Original',1.0,1.0,'This is the original revision of the system.',0,'-',0.0,0.0,0.0,0.0);

DROP TABLE IF EXISTS "tbl_missions";
CREATE TABLE "tbl_missions" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT(0),                  -- Identifier for the revision.
    "fld_mission_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,    -- Identifier for the mission.
    "fld_mission_time" REAL DEFAULT(0),                             -- Total length of the mission.
    "fld_mission_units" VARCHAR(128) DEFAULT(''),                   -- Unit of time measure for the mission.
    "fld_mission_description" BLOB,                                 -- Description of the mission.
    FOREIGN KEY("fld_revision_id") REFERENCES "tbl_revisions"("fld_revision_id") ON DELETE CASCADE
);
INSERT INTO "tbl_missions" VALUES(0,0,10.0,'','Default mission');

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
INSERT INTO "tbl_mission_phase" VALUES(0,0,1,0.0,0.5,'Phase I','This is the first phase of the default mission.');
INSERT INTO "tbl_mission_phase" VALUES(0,0,2,0.5,9.5,'Phase II','This is the second phase of the default mission.');
INSERT INTO "tbl_mission_phase" VALUES(0,0,3,9.5,10.0,'Phase III','This is the third phase of the default mission.');

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
INSERT INTO "tbl_environments" VALUES(0,0,1,0,1,'Temperature, Ambient','',0.0,0.0,0.0,0.0,NULL,NULL,NULL);

DROP TABLE IF EXISTS "tbl_failure_definitions";
CREATE TABLE "tbl_failure_definitions" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT(0),                  -- Indentifier for the revision.
    "fld_definition_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, -- Identifier for the failure definition.
    "fld_definition" BLOB,                                          -- Definition of the failure.
    FOREIGN KEY("fld_revision_id") REFERENCES "tbl_revisions"("fld_revision_id") ON DELETE CASCADE
);
INSERT INTO "tbl_failure_definitions" VALUES(0,1,'This is the first definition added.');
INSERT INTO "tbl_failure_definitions" VALUES(0,2,'This is the second definition added.');
INSERT INTO "tbl_failure_definitions" VALUES(0,3,'This is the third definition added.');
INSERT INTO "tbl_failure_definitions" VALUES(0,4,'This is the fourth definition added.');

DROP TABLE IF EXISTS "tbl_functions";
CREATE TABLE "tbl_functions" (
    "fld_revision_id" INTEGER NOT NULL DEFAULT(0),                  -- Indentifier for the revision.
    "fld_function_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,   -- Indentifier for the function.
    "fld_availability" FLOAT NOT NULL DEFAULT(1),                   -- Assessed availability of the function.
    "fld_availability_mission" FLOAT NOT NULL DEFAULT(1),           -- Assessed mission availability of the function.
    "fld_code" VARCHAR(16) NOT NULL DEFAULT('Function Code'),       -- Tracking code for the function.
    "fld_cost" FLOAT NOT NULL DEFAULT(0),                           -- Assessed cost of the function.
    "fld_failure_rate_mission" FLOAT NOT NULL DEFAULT(0),           -- Assessed mission failure intensity of the function.
    "fld_failure_rate_predicted" FLOAT NOT NULL DEFAULT(0),         -- Assessed limiting failure intensity of the function.
    "fld_mmt" FLOAT NOT NULL DEFAULT(0),                            -- Assessed mean maintenance time of the function.
    "fld_mcmt" FLOAT NOT NULL DEFAULT(0),                           -- Assessed mean corrective maintenance time of the function.
    "fld_mpmt" FLOAT NOT NULL DEFAULT(0),                           -- Assessed mean preventive maintenance time of the function.
    "fld_mtbf_mission" FLOAT NOT NULL DEFAULT(0),                   -- Assessed mission mean time between failures of the function.
    "fld_mtbf_predicted" FLOAT NOT NULL DEFAULT(0),                 -- Assessed limiting mean time between failures of the function.
    "fld_mttr" FLOAT NOT NULL DEFAULT(0),                           -- Assessed mean time to repair of the function.
    "fld_name" VARCHAR(255) DEFAULT('Function Name'),               -- Noun name of the function.
    "fld_remarks" BLOB,                                             -- Remarks associated with the function.
    "fld_total_mode_quantity" INTEGER NOT NULL DEFAULT(0),          -- Total number of failure modes impacting the function.
    "fld_total_part_quantity" INTEGER NOT NULL DEFAULT(0),          -- Total number of components comprising the function.
    "fld_type" INTEGER NOT NULL DEFAULT(0),                         --
    "fld_parent_id" INTEGER NOT NULL DEFAULT(0),                    -- Identifer of the parent function.
    "fld_level" INTEGER NOT NULL DEFAULT(0),                        --
    "fld_safety_critical" INTEGER NOT NULL DEFAULT(0),              -- Indicates whether or not the function is safety critical.
    FOREIGN KEY("fld_revision_id") REFERENCES "tbl_revisions"("fld_revision_id") ON DELETE CASCADE
);
INSERT INTO "tbl_functions" VALUES(0,0,1.0,1.0,'PRESS-01',0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,'Provide sufficient pressure.','Air pressure needs to be raised in stages from atmospheric to final pressure.',0,0,0,-1,0,0);
INSERT INTO "tbl_functions" VALUES(0,1,1.0,1.0,'PRESS-11',0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,'Increase incoming air to 40 bar','',0,0,0,9738,0,0);
INSERT INTO "tbl_functions" VALUES(0,2,1.0,1.0,'PRESS-12',0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,'Increase 40 bar compressed air to 100 bar','',0,0,0,9738,0,0);
INSERT INTO "tbl_functions" VALUES(0,3,1.0,1.0,'FLOW-1',0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,'Provide sufficient air flow','',0,0,0,-1,0,0);
INSERT INTO "tbl_functions" VALUES(0,4,1.0,1.0,'TEMP-1',0.0,0.0,0.00102,0.0,0.0,0.0,0.0,980.796014,0.0,'Maintain air temperature at safe level.','',0,0,0,-1,0,0);
INSERT INTO "tbl_functions" VALUES(0,5,1.0,1.0,'VOL-1',0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,'Provide at least 100 scf of air reserve','',0,0,0,-1,0,0);
INSERT INTO "tbl_functions" VALUES(0,6,1.0,1.0,'QUAL-1',0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,'Dry air to less than 5% moisture','This is the system-level air quality function.',0,0,0,-1,0,0);
INSERT INTO "tbl_functions" VALUES(0,7,1.0,1.0,'QUAL-2',0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,'Dry air to less than 25% moisture','Drying the air to less than 5% moisture will require multiple stages.',0,0,0,9750,0,0);
INSERT INTO "tbl_functions" VALUES(0,8,1.0,1.0,'TEMP-11',0.0,0.0,0.00062,0.0,0.0,0.0,0.0,1613.999183,0.0,'Cool compressed air.','',0,0,0,9748,0,0);
INSERT INTO "tbl_functions" VALUES(0,9,1.0,1.0,'TEMP-12',0.0,0.0,0.0004,0.0,0.0,0.0,0.0,2500.0,0.0,'Heat compressed air.','',0,0,0,9748,0,0);
INSERT INTO "tbl_functions" VALUES(0,10,1.0,1.0,'PRESS-13',0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,'Prevent overpressure conditions','This is a safety function',0,0,0,9738,0,0);

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
INSERT INTO "tbl_requirements" VALUES(0,1,'The Widgi-Digi-Tator 2000 shall respond to a 10% over-pressure condition within 500 milliseconds.','PRF-0001','Performance',2,'That Spec','55','55.1',0,'Engineering, Design',1,736006,-1,'111011111','1000000000','000000000','000000');
INSERT INTO "tbl_requirements" VALUES(0,2,'The Widgi-Digi-Tator 2000 shall have a reliability at 100 hours of 0.95 at 90% confidence.','REL-0003','Reliability',1,'','','',0,'Engineering, Reliability',0,736009,-1,'111010111','1111101111','101111111','101100');
INSERT INTO "tbl_requirements" VALUES(0,3,'The Widgi-Digi-Tator 2000 shall provide means for preventing pressure from exceeding 110 lbf per in square.','SAF-0006','Safety',1,'','','',0,'Engineering, Safety',0,719163,-1,'000000000','0000000000','000000000','000000');
INSERT INTO "tbl_requirements" VALUES(0,4,'The Widgi-Digi-Tator 2000 shall begin reducing pressure when sensed pressure reaches 108 ldf per in square.','SAF-0011','Safety',1,'','','',0,'Engineering, Safety',0,719163,6,'000000000','0000000000','000000000','000000');
INSERT INTO "tbl_requirements" VALUES(0,5,'The Widgi-Digi-Tator 2000 shall provide compressed air at 100 lbf per in square.','FUN-0473','Functional',1,'','','',0,'Engineering, Design',0,736011,-1,'000000000','0000000000','000000000','000000');

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
INSERT INTO "tbl_stakeholder_input" VALUES(0,1,'Customer','The Widgi-Digi-Tator 2000 should be reliable','Reliability',1,2,1,0.8,0.8,'REL-0003-The Widgi-Digi-Tator 2000 shall have a reliability at 100 hours of 0.95 at 90% confidence.',1.0,1.0,1.0,1.0,1.0);
INSERT INTO "tbl_stakeholder_input" VALUES(0,111,'Customer','The Widgi-Digi-Tator 2000 should last a long time.','Durability',3,1,3,1.4,4.2,'',1.0,1.0,1.0,1.0,1.0);
INSERT INTO "tbl_stakeholder_input" VALUES(0,113,'Marketing','','',1,5,3,1.0,0.0,'',1.0,1.0,1.0,1.0,1.0);
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
INSERT INTO "rtk_matrix" VALUES(0,0,0,1,0,0,'1',1,0);
INSERT INTO "rtk_matrix" VALUES(0,0,0,1,9,0,'0',1,115);
INSERT INTO "rtk_matrix" VALUES(0,0,0,1,8,0,'0',1,105);
INSERT INTO "rtk_matrix" VALUES(0,0,0,1,7,0,'0',1,102);
INSERT INTO "rtk_matrix" VALUES(0,0,0,1,6,0,'0',1,88);
INSERT INTO "rtk_matrix" VALUES(0,0,0,1,5,0,'0',1,8);
INSERT INTO "rtk_matrix" VALUES(0,0,0,1,4,0,'0',1,7);
INSERT INTO "rtk_matrix" VALUES(0,0,0,1,3,0,'0',1,5);
INSERT INTO "rtk_matrix" VALUES(0,0,0,1,2,0,'0',1,3);
INSERT INTO "rtk_matrix" VALUES(0,0,0,1,1,0,'1',1,2);
INSERT INTO "rtk_matrix" VALUES(0,1,1,0,0,-1,'0',0,0);
INSERT INTO "rtk_matrix" VALUES(0,1,1,0,1,-1,'0',0,5);
INSERT INTO "rtk_matrix" VALUES(0,1,1,0,2,-1,'0',0,6);
INSERT INTO "rtk_matrix" VALUES(0,0,0,3,0,-1,'0',3,0);
INSERT INTO "rtk_matrix" VALUES(0,0,0,3,1,-1,'0',3,2);
INSERT INTO "rtk_matrix" VALUES(0,0,0,3,2,-1,'0',3,3);
INSERT INTO "rtk_matrix" VALUES(0,0,0,3,3,-1,'0',3,5);
INSERT INTO "rtk_matrix" VALUES(0,0,0,3,4,-1,'0',3,7);
INSERT INTO "rtk_matrix" VALUES(0,0,0,3,5,-1,'0',3,8);
INSERT INTO "rtk_matrix" VALUES(0,0,0,3,6,-1,'0',3,88);
INSERT INTO "rtk_matrix" VALUES(0,0,0,3,7,-1,'0',3,102);
INSERT INTO "rtk_matrix" VALUES(0,0,0,3,8,-1,'0',3,105);
INSERT INTO "rtk_matrix" VALUES(0,0,0,3,9,-1,'0',3,115);
INSERT INTO "rtk_matrix" VALUES(0,1,1,2,0,0,'0',2,0);
INSERT INTO "rtk_matrix" VALUES(0,1,1,2,1,0,'0',2,5);
INSERT INTO "rtk_matrix" VALUES(0,1,1,2,2,0,'1',2,6);
INSERT INTO "rtk_matrix" VALUES(0,0,0,4,0,-1,'0',4,0);
INSERT INTO "rtk_matrix" VALUES(0,0,0,4,1,-1,'0',4,2);
INSERT INTO "rtk_matrix" VALUES(0,0,0,4,2,-1,'0',4,3);
INSERT INTO "rtk_matrix" VALUES(0,0,0,4,3,-1,'0',4,5);
INSERT INTO "rtk_matrix" VALUES(0,0,0,4,4,-1,'0',4,7);
INSERT INTO "rtk_matrix" VALUES(0,0,0,4,5,-1,'2',4,8);
INSERT INTO "rtk_matrix" VALUES(0,0,0,4,6,-1,'0',4,88);
INSERT INTO "rtk_matrix" VALUES(0,0,0,4,7,-1,'1',4,102);
INSERT INTO "rtk_matrix" VALUES(0,0,0,4,8,-1,'0',4,105);
INSERT INTO "rtk_matrix" VALUES(0,0,0,4,9,-1,'1',4,115);
INSERT INTO "rtk_matrix" VALUES(0,1,1,3,0,-1,'0',3,0);
INSERT INTO "rtk_matrix" VALUES(0,1,1,3,1,-1,'2',3,5);
INSERT INTO "rtk_matrix" VALUES(0,1,1,3,2,-1,'0',3,6);
INSERT INTO "rtk_matrix" VALUES(0,0,0,5,0,-1,'0',5,0);
INSERT INTO "rtk_matrix" VALUES(0,0,0,5,1,-1,'0',5,2);
INSERT INTO "rtk_matrix" VALUES(0,0,0,5,2,-1,'0',5,3);
INSERT INTO "rtk_matrix" VALUES(0,0,0,5,3,-1,'0',5,5);
INSERT INTO "rtk_matrix" VALUES(0,0,0,5,4,-1,'0',5,7);
INSERT INTO "rtk_matrix" VALUES(0,0,0,5,5,-1,'0',5,8);
INSERT INTO "rtk_matrix" VALUES(0,0,0,5,6,-1,'1',5,88);
INSERT INTO "rtk_matrix" VALUES(0,0,0,5,7,-1,'0',5,102);
INSERT INTO "rtk_matrix" VALUES(0,0,0,5,8,-1,'0',5,105);
INSERT INTO "rtk_matrix" VALUES(0,0,0,5,9,-1,'0',5,115);
INSERT INTO "rtk_matrix" VALUES(0,1,1,4,0,-1,'0',4,0);
INSERT INTO "rtk_matrix" VALUES(0,1,1,4,1,-1,'0',4,5);
INSERT INTO "rtk_matrix" VALUES(0,1,1,4,2,-1,'0',4,6);
INSERT INTO "rtk_matrix" VALUES(0,0,0,6,0,-1,'0',6,0);
INSERT INTO "rtk_matrix" VALUES(0,0,0,6,1,-1,'0',6,2);
INSERT INTO "rtk_matrix" VALUES(0,0,0,6,2,-1,'0',6,3);
INSERT INTO "rtk_matrix" VALUES(0,0,0,6,3,-1,'0',6,5);
INSERT INTO "rtk_matrix" VALUES(0,0,0,6,4,-1,'0',6,7);
INSERT INTO "rtk_matrix" VALUES(0,0,0,6,5,-1,'0',6,8);
INSERT INTO "rtk_matrix" VALUES(0,0,0,6,6,-1,'0',6,88);
INSERT INTO "rtk_matrix" VALUES(0,0,0,6,7,-1,'0',6,102);
INSERT INTO "rtk_matrix" VALUES(0,0,0,6,8,-1,'0',6,105);
INSERT INTO "rtk_matrix" VALUES(0,0,0,6,9,-1,'0',6,115);
INSERT INTO "rtk_matrix" VALUES(0,1,1,5,0,-1,'0',5,0);
INSERT INTO "rtk_matrix" VALUES(0,1,1,5,1,-1,'0',5,5);
INSERT INTO "rtk_matrix" VALUES(0,1,1,5,2,-1,'0',5,6);
INSERT INTO "rtk_matrix" VALUES(0,0,0,7,0,6,'0',7,0);
INSERT INTO "rtk_matrix" VALUES(0,0,0,7,1,6,'0',7,2);
INSERT INTO "rtk_matrix" VALUES(0,0,0,7,2,6,'0',7,3);
INSERT INTO "rtk_matrix" VALUES(0,0,0,7,3,6,'0',7,5);
INSERT INTO "rtk_matrix" VALUES(0,0,0,7,4,6,'0',7,7);
INSERT INTO "rtk_matrix" VALUES(0,0,0,7,5,6,'0',7,8);
INSERT INTO "rtk_matrix" VALUES(0,0,0,7,6,6,'0',7,88);
INSERT INTO "rtk_matrix" VALUES(0,0,0,7,7,6,'0',7,102);
INSERT INTO "rtk_matrix" VALUES(0,0,0,7,8,6,'0',7,105);
INSERT INTO "rtk_matrix" VALUES(0,0,0,7,9,6,'0',7,115);
INSERT INTO "rtk_matrix" VALUES(0,1,1,6,0,-1,'0',6,0);
INSERT INTO "rtk_matrix" VALUES(0,1,1,6,1,-1,'0',6,5);
INSERT INTO "rtk_matrix" VALUES(0,1,1,6,2,-1,'0',6,6);
INSERT INTO "rtk_matrix" VALUES(0,3,3,0,0,-1,'0',1,0);
INSERT INTO "rtk_matrix" VALUES(0,3,3,0,1,-1,'2',1,2);
INSERT INTO "rtk_matrix" VALUES(0,0,0,8,0,4,'0',8,0);
INSERT INTO "rtk_matrix" VALUES(0,0,0,8,1,4,'0',8,2);
INSERT INTO "rtk_matrix" VALUES(0,0,0,8,2,4,'0',8,3);
INSERT INTO "rtk_matrix" VALUES(0,0,0,8,3,4,'0',8,5);
INSERT INTO "rtk_matrix" VALUES(0,0,0,8,4,4,'0',8,7);
INSERT INTO "rtk_matrix" VALUES(0,0,0,8,5,4,'0',8,8);
INSERT INTO "rtk_matrix" VALUES(0,0,0,8,6,4,'0',8,88);
INSERT INTO "rtk_matrix" VALUES(0,0,0,8,7,4,'2',8,102);
INSERT INTO "rtk_matrix" VALUES(0,0,0,8,8,4,'0',8,105);
INSERT INTO "rtk_matrix" VALUES(0,0,0,8,9,4,'0',8,115);
INSERT INTO "rtk_matrix" VALUES(0,1,1,7,0,6,'0',7,0);
INSERT INTO "rtk_matrix" VALUES(0,1,1,7,1,6,'0',7,5);
INSERT INTO "rtk_matrix" VALUES(0,1,1,7,2,6,'1',7,6);
INSERT INTO "rtk_matrix" VALUES(0,0,0,9,0,4,'0',9,0);
INSERT INTO "rtk_matrix" VALUES(0,0,0,9,1,4,'0',9,2);
INSERT INTO "rtk_matrix" VALUES(0,0,0,9,2,4,'0',9,3);
INSERT INTO "rtk_matrix" VALUES(0,0,0,9,3,4,'0',9,5);
INSERT INTO "rtk_matrix" VALUES(0,0,0,9,4,4,'0',9,7);
INSERT INTO "rtk_matrix" VALUES(0,0,0,9,5,4,'0',9,8);
INSERT INTO "rtk_matrix" VALUES(0,0,0,9,6,4,'0',9,88);
INSERT INTO "rtk_matrix" VALUES(0,0,0,9,7,4,'0',9,102);
INSERT INTO "rtk_matrix" VALUES(0,0,0,9,8,4,'0',9,105);
INSERT INTO "rtk_matrix" VALUES(0,0,0,9,9,4,'2',9,115);
INSERT INTO "rtk_matrix" VALUES(0,1,1,8,0,4,'0',8,0);
INSERT INTO "rtk_matrix" VALUES(0,1,1,8,1,4,'0',8,5);
INSERT INTO "rtk_matrix" VALUES(0,1,1,8,2,4,'1',8,6);
INSERT INTO "rtk_matrix" VALUES(0,0,0,10,0,0,'0',10,0);
INSERT INTO "rtk_matrix" VALUES(0,0,0,10,1,0,'0',10,2);
INSERT INTO "rtk_matrix" VALUES(0,0,0,10,2,0,'0',10,3);
INSERT INTO "rtk_matrix" VALUES(0,0,0,10,3,0,'0',10,5);
INSERT INTO "rtk_matrix" VALUES(0,0,0,10,4,0,'0',10,7);
INSERT INTO "rtk_matrix" VALUES(0,0,0,10,5,0,'0',10,8);
INSERT INTO "rtk_matrix" VALUES(0,0,0,10,6,0,'0',10,88);
INSERT INTO "rtk_matrix" VALUES(0,0,0,10,7,0,'0',10,102);
INSERT INTO "rtk_matrix" VALUES(0,0,0,10,8,0,'0',10,105);
INSERT INTO "rtk_matrix" VALUES(0,0,0,10,9,0,'0',10,115);
INSERT INTO "rtk_matrix" VALUES(0,1,1,9,0,4,'',9,0);
INSERT INTO "rtk_matrix" VALUES(0,1,1,9,1,4,'',9,5);
INSERT INTO "rtk_matrix" VALUES(0,1,1,9,2,4,'',9,6);
INSERT INTO "rtk_matrix" VALUES(0,0,0,0,0,-1,'0',0,0);
INSERT INTO "rtk_matrix" VALUES(0,0,0,0,1,-1,'0',0,2);
INSERT INTO "rtk_matrix" VALUES(0,0,0,0,2,-1,'0',0,3);
INSERT INTO "rtk_matrix" VALUES(0,0,0,0,3,-1,'0',0,5);
INSERT INTO "rtk_matrix" VALUES(0,0,0,0,4,-1,'0',0,7);
INSERT INTO "rtk_matrix" VALUES(0,0,0,0,5,-1,'0',0,8);
INSERT INTO "rtk_matrix" VALUES(0,0,0,0,6,-1,'0',0,88);
INSERT INTO "rtk_matrix" VALUES(0,0,0,0,7,-1,'0',0,102);
INSERT INTO "rtk_matrix" VALUES(0,0,0,0,8,-1,'0',0,105);
INSERT INTO "rtk_matrix" VALUES(0,0,0,0,9,-1,'0',0,115);
INSERT INTO "rtk_matrix" VALUES(0,0,0,2,0,0,'0',2,0);
INSERT INTO "rtk_matrix" VALUES(0,0,0,2,1,0,'0',2,2);
INSERT INTO "rtk_matrix" VALUES(0,0,0,2,2,0,'0',2,3);
INSERT INTO "rtk_matrix" VALUES(0,0,0,2,3,0,'0',2,5);
INSERT INTO "rtk_matrix" VALUES(0,0,0,2,4,0,'0',2,7);
INSERT INTO "rtk_matrix" VALUES(0,0,0,2,5,0,'0',2,8);
INSERT INTO "rtk_matrix" VALUES(0,0,0,2,6,0,'0',2,88);
INSERT INTO "rtk_matrix" VALUES(0,0,0,2,7,0,'0',2,102);
INSERT INTO "rtk_matrix" VALUES(0,0,0,2,8,0,'0',2,105);
INSERT INTO "rtk_matrix" VALUES(0,0,0,2,9,0,'0',2,115);
INSERT INTO "rtk_matrix" VALUES(0,1,1,1,0,0,'0',1,0);
INSERT INTO "rtk_matrix" VALUES(0,1,1,1,1,0,'0',1,5);
INSERT INTO "rtk_matrix" VALUES(0,1,1,1,2,0,'0',1,6);
INSERT INTO "rtk_matrix" VALUES(0,3,3,0,9,-1,'0',1,115);
INSERT INTO "rtk_matrix" VALUES(0,3,3,0,2,-1,'0',1,3);
INSERT INTO "rtk_matrix" VALUES(0,3,3,0,8,-1,'0',1,105);
INSERT INTO "rtk_matrix" VALUES(0,3,3,0,3,-1,'0',1,5);
INSERT INTO "rtk_matrix" VALUES(0,3,3,0,4,-1,'0',1,7);
INSERT INTO "rtk_matrix" VALUES(0,3,3,0,5,-1,'0',1,8);
INSERT INTO "rtk_matrix" VALUES(0,3,3,0,6,-1,'0',1,88);
INSERT INTO "rtk_matrix" VALUES(0,3,3,0,7,-1,'0',1,102);
INSERT INTO "rtk_matrix" VALUES(0,3,3,1,0,-1,'0',3,0);
INSERT INTO "rtk_matrix" VALUES(0,3,3,1,1,-1,'0',3,2);
INSERT INTO "rtk_matrix" VALUES(0,3,3,1,2,-1,'0',3,3);
INSERT INTO "rtk_matrix" VALUES(0,3,3,1,3,-1,'0',3,5);
INSERT INTO "rtk_matrix" VALUES(0,3,3,1,4,-1,'0',3,7);
INSERT INTO "rtk_matrix" VALUES(0,3,3,1,5,-1,'0',3,8);
INSERT INTO "rtk_matrix" VALUES(0,3,3,1,6,-1,'0',3,88);
INSERT INTO "rtk_matrix" VALUES(0,3,3,1,7,-1,'0',3,102);
INSERT INTO "rtk_matrix" VALUES(0,3,3,1,8,-1,'0',3,105);
INSERT INTO "rtk_matrix" VALUES(0,3,3,1,9,-1,'0',3,115);
INSERT INTO "rtk_matrix" VALUES(0,3,3,2,0,-1,'0',6,0);
INSERT INTO "rtk_matrix" VALUES(0,3,3,2,1,-1,'0',6,2);
INSERT INTO "rtk_matrix" VALUES(0,3,3,2,2,-1,'2',6,3);
INSERT INTO "rtk_matrix" VALUES(0,3,3,2,3,-1,'0',6,5);
INSERT INTO "rtk_matrix" VALUES(0,3,3,2,4,-1,'0',6,7);
INSERT INTO "rtk_matrix" VALUES(0,3,3,2,5,-1,'0',6,8);
INSERT INTO "rtk_matrix" VALUES(0,3,3,2,6,-1,'0',6,88);
INSERT INTO "rtk_matrix" VALUES(0,3,3,2,7,-1,'1',6,102);
INSERT INTO "rtk_matrix" VALUES(0,3,3,2,8,-1,'0',6,105);
INSERT INTO "rtk_matrix" VALUES(0,3,3,2,9,-1,'1',6,115);
INSERT INTO "rtk_matrix" VALUES(0,3,3,3,0,6,'0',11,0);
INSERT INTO "rtk_matrix" VALUES(0,3,3,3,1,6,'0',11,2);
INSERT INTO "rtk_matrix" VALUES(0,3,3,3,2,6,'0',11,3);
INSERT INTO "rtk_matrix" VALUES(0,3,3,3,3,6,'0',11,5);
INSERT INTO "rtk_matrix" VALUES(0,3,3,3,4,6,'0',11,7);
INSERT INTO "rtk_matrix" VALUES(0,3,3,3,5,6,'0',11,8);
INSERT INTO "rtk_matrix" VALUES(0,3,3,3,6,6,'0',11,88);
INSERT INTO "rtk_matrix" VALUES(0,3,3,3,7,6,'1',11,102);
INSERT INTO "rtk_matrix" VALUES(0,3,3,3,8,6,'0',11,105);
INSERT INTO "rtk_matrix" VALUES(0,3,3,3,9,6,'1',11,115);
INSERT INTO "rtk_matrix" VALUES(0,3,3,4,0,-1,'0',473,0);
INSERT INTO "rtk_matrix" VALUES(0,3,3,4,1,-1,'0',473,2);
INSERT INTO "rtk_matrix" VALUES(0,3,3,4,2,-1,'0',473,3);
INSERT INTO "rtk_matrix" VALUES(0,3,3,4,3,-1,'0',473,5);
INSERT INTO "rtk_matrix" VALUES(0,3,3,4,4,-1,'0',473,7);
INSERT INTO "rtk_matrix" VALUES(0,3,3,4,5,-1,'0',473,8);
INSERT INTO "rtk_matrix" VALUES(0,3,3,4,6,-1,'0',473,88);
INSERT INTO "rtk_matrix" VALUES(0,3,3,4,7,-1,'0',473,102);
INSERT INTO "rtk_matrix" VALUES(0,3,3,4,8,-1,'0',473,105);
INSERT INTO "rtk_matrix" VALUES(0,3,3,4,9,-1,'0',473,115);
INSERT INTO "rtk_matrix" VALUES(0,4,4,0,0,-1,'0',1,0);
INSERT INTO "rtk_matrix" VALUES(0,4,4,0,1,-1,'1',1,5);
INSERT INTO "rtk_matrix" VALUES(0,4,4,0,2,-1,'0',1,6);
INSERT INTO "rtk_matrix" VALUES(0,4,4,1,0,-1,'0',3,0);
INSERT INTO "rtk_matrix" VALUES(0,4,4,1,1,-1,'0',3,5);
INSERT INTO "rtk_matrix" VALUES(0,4,4,1,2,-1,'1',3,6);
INSERT INTO "rtk_matrix" VALUES(0,4,4,2,0,-1,'0',6,0);
INSERT INTO "rtk_matrix" VALUES(0,4,4,2,1,-1,'0',6,5);
INSERT INTO "rtk_matrix" VALUES(0,4,4,2,2,-1,'0',6,6);
INSERT INTO "rtk_matrix" VALUES(0,4,4,3,0,6,'0',11,0);
INSERT INTO "rtk_matrix" VALUES(0,4,4,3,1,6,'0',11,5);
INSERT INTO "rtk_matrix" VALUES(0,4,4,3,2,6,'0',11,6);
INSERT INTO "rtk_matrix" VALUES(0,4,4,4,0,-1,'0',473,0);
INSERT INTO "rtk_matrix" VALUES(0,4,4,4,1,-1,'0',473,5);
INSERT INTO "rtk_matrix" VALUES(0,4,4,4,2,-1,'0',473,6);
INSERT INTO "rtk_matrix" VALUES(0,5,5,0,0,-1,'0',1,8);
INSERT INTO "rtk_matrix" VALUES(0,5,5,0,1,-1,'0',1,9);
INSERT INTO "rtk_matrix" VALUES(0,5,5,0,2,-1,'0',1,10);
INSERT INTO "rtk_matrix" VALUES(0,5,5,0,3,-1,'0',1,13);
INSERT INTO "rtk_matrix" VALUES(0,5,5,1,0,-1,'0',3,8);
INSERT INTO "rtk_matrix" VALUES(0,5,5,1,1,-1,'0',3,9);
INSERT INTO "rtk_matrix" VALUES(0,5,5,1,2,-1,'0',3,10);
INSERT INTO "rtk_matrix" VALUES(0,5,5,1,3,-1,'1',3,13);
INSERT INTO "rtk_matrix" VALUES(0,5,5,2,0,-1,'0',6,8);
INSERT INTO "rtk_matrix" VALUES(0,5,5,2,1,-1,'0',6,9);
INSERT INTO "rtk_matrix" VALUES(0,5,5,2,2,-1,'0',6,10);
INSERT INTO "rtk_matrix" VALUES(0,5,5,2,3,-1,'0',6,13);
INSERT INTO "rtk_matrix" VALUES(0,5,5,3,0,6,'0',11,8);
INSERT INTO "rtk_matrix" VALUES(0,5,5,3,1,6,'0',11,9);
INSERT INTO "rtk_matrix" VALUES(0,5,5,3,2,6,'0',11,10);
INSERT INTO "rtk_matrix" VALUES(0,5,5,3,3,6,'0',11,13);
INSERT INTO "rtk_matrix" VALUES(0,5,5,4,0,-1,'0',473,8);
INSERT INTO "rtk_matrix" VALUES(0,5,5,4,1,-1,'0',473,9);
INSERT INTO "rtk_matrix" VALUES(0,5,5,4,2,-1,'0',473,10);
INSERT INTO "rtk_matrix" VALUES(0,5,5,4,3,-1,'0',473,13);
INSERT INTO "rtk_matrix" VALUES(0,2,2,0,0,-1,'0',0,1);
INSERT INTO "rtk_matrix" VALUES(0,2,2,0,1,-1,'0',0,2);
INSERT INTO "rtk_matrix" VALUES(0,2,2,0,2,-1,'0',0,3);
INSERT INTO "rtk_matrix" VALUES(0,2,2,1,0,0,'0',1,1);
INSERT INTO "rtk_matrix" VALUES(0,2,2,1,1,0,'0',1,2);
INSERT INTO "rtk_matrix" VALUES(0,2,2,1,2,0,'0',1,3);
INSERT INTO "rtk_matrix" VALUES(0,2,2,2,0,0,'0',2,1);
INSERT INTO "rtk_matrix" VALUES(0,2,2,2,1,0,'0',2,2);
INSERT INTO "rtk_matrix" VALUES(0,2,2,2,2,0,'0',2,3);
INSERT INTO "rtk_matrix" VALUES(0,2,2,3,0,-1,'0',3,1);
INSERT INTO "rtk_matrix" VALUES(0,2,2,3,1,-1,'0',3,2);
INSERT INTO "rtk_matrix" VALUES(0,2,2,3,2,-1,'0',3,3);
INSERT INTO "rtk_matrix" VALUES(0,2,2,4,0,-1,'0',4,1);
INSERT INTO "rtk_matrix" VALUES(0,2,2,4,1,-1,'0',4,2);
INSERT INTO "rtk_matrix" VALUES(0,2,2,4,2,-1,'0',4,3);
INSERT INTO "rtk_matrix" VALUES(0,2,2,5,0,-1,'0',5,1);
INSERT INTO "rtk_matrix" VALUES(0,2,2,5,1,-1,'0',5,2);
INSERT INTO "rtk_matrix" VALUES(0,2,2,5,2,-1,'0',5,3);
INSERT INTO "rtk_matrix" VALUES(0,2,2,6,0,-1,'0',6,1);
INSERT INTO "rtk_matrix" VALUES(0,2,2,6,1,-1,'0',6,2);
INSERT INTO "rtk_matrix" VALUES(0,2,2,6,2,-1,'0',6,3);
INSERT INTO "rtk_matrix" VALUES(0,2,2,7,0,6,'0',7,1);
INSERT INTO "rtk_matrix" VALUES(0,2,2,7,1,6,'0',7,2);
INSERT INTO "rtk_matrix" VALUES(0,2,2,7,2,6,'0',7,3);
INSERT INTO "rtk_matrix" VALUES(0,2,2,8,0,4,'0',8,1);
INSERT INTO "rtk_matrix" VALUES(0,2,2,8,1,4,'0',8,2);
INSERT INTO "rtk_matrix" VALUES(0,2,2,8,2,4,'0',8,3);
INSERT INTO "rtk_matrix" VALUES(0,2,2,9,0,4,'0',9,1);
INSERT INTO "rtk_matrix" VALUES(0,2,2,9,1,4,'0',9,2);
INSERT INTO "rtk_matrix" VALUES(0,2,2,9,2,4,'0',9,3);
INSERT INTO "rtk_matrix" VALUES(0,2,2,10,0,0,'0',10,1);
INSERT INTO "rtk_matrix" VALUES(0,2,2,10,1,0,'0',10,2);
INSERT INTO "rtk_matrix" VALUES(0,2,2,10,2,0,'0',10,3);
INSERT INTO "rtk_matrix" VALUES(0,1,1,10,0,0,'0',10,0);
INSERT INTO "rtk_matrix" VALUES(0,1,1,10,1,0,'0',10,5);
INSERT INTO "rtk_matrix" VALUES(0,1,1,10,2,0,'0',10,6);

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
    "fld_cost_type_id" INTEGER DEFAULT(1),                          -- How to calculate the cost (1=Assessed, 2=Specified).
    "fld_description" VARCHAR(256) DEFAULT(''),                     -- Description of the hardware.
    "fld_duty_cycle" REAL DEFAULT(100),                             -- Duty cycle in the field.
    "fld_figure_number" VARCHAR(32) DEFAULT(''),                    -- Specification figure number fo the hardware item.
    "fld_lcn" VARCHAR(128) DEFAULT(''),                             -- Logistics control number of the hardware item.
    "fld_level" INTEGER DEFAULT(1),                                 -- Level in the system structure.
    "fld_manufacturer_id" INTEGER DEFAULT(0),                       -- Manufacturer of the hardware item.
    "fld_mission_time" REAL DEFAULT(100),                           -- Mission time of the hardware item.
    "fld_name" VARCHAR(256) DEFAULT(''),                            -- Name of the hardware item.
    "fld_nsn" VARCHAR(32) DEFAULT(''),                              -- National stock number of the hardware item.
    "fld_page_number" VARCHAR(32) DEFAULT(''),                      -- Specification page number for the hardware item.
    "fld_parent_id" INTEGER DEFAULT(0),                             -- Hardware ID of the parent assembly.
    "fld_part" INTEGER DEFAULT(0),                                  -- Whether the hardware item is an assembly or a component.
    "fld_part_number" VARCHAR(128) DEFAULT(''),                     -- Part number of the hardware item.
    "fld_quantity" INTEGER DEFAULT(1),                              -- Quantity of the hardware item used in the system.
    "fld_ref_des" VARCHAR(128) DEFAULT(''),                         -- Reference designator of the hardware item.
    "fld_remarks" BLOB,                                             -- Remarks associated with the hardware item.
    "fld_repairable" TINYINT DEFAULT(0),                            -- Whether the hardware item is repairable.
    "fld_specification_number" VARCHAR(64) DEFAULT(''),             -- Governing specification of the hardware item.
    "fld_subcategory_id" INTEGER DEFAULT(0),                        -- Component sub-category ID.
    "fld_tagged_part" TINYINT DEFAULT (0),                          --
    "fld_total_part_count" INTEGER DEFAULT(0),                      -- Total number of components comprising the assembly.
    "fld_total_power_dissipation" REAL DEFAULT(0),                  -- Total power dissipation of the assembly.
    "fld_year_of_manufacture" INTEGER DEFAULT(2014),                -- Year the hardware item was manufactured.
    FOREIGN KEY("fld_revision_id") REFERENCES "tbl_revisions"("fld_revision_id") ON DELETE CASCADE
);
INSERT INTO "rtk_hardware" VALUES(0,1,'','','',0,'S1',1.68,86.860837,0.168,1,'',100.0,'','',1,0,10.0,'System','NSN','Page Number',0,0,'',1,'S1','Remarks',0,'Specification',0,0,3,0.75,2014);
INSERT INTO "rtk_hardware" VALUES(0,2,'','','',0,'',0.0,0.0,0.0,2,'',100.0,'','',1,0,10.0,'Sub-System 1','','',1,0,'',1,'SS1','None',0,'Specification',0,0,0,0.0,2014);
INSERT INTO "rtk_hardware" VALUES(0,3,'','','',0,'',0.0,0.0,0.0,1,'',100.0,'','',1,0,10.0,'Sub-System 2','','',1,0,'',1,'SS2','None',0,'Specification',0,0,0,0.0,2014);
INSERT INTO "rtk_hardware" VALUES(0,5,'','','',0,'',0.0,0.0,0.0,1,'',100.0,'','',1,0,10.0,'Sub-System 3','','',1,0,'',1,'SS3','None',0,'Specification',0,0,0,0.0,2014);
INSERT INTO "rtk_hardware" VALUES(0,6,'','','',0,'',1.68,9848098.205226,0.168,1,'',100.0,'','',1,0,10.0,'Switch','','',3,1,'',3,'SW1','',0,'Specification',0,0,0,0.0,2014);
INSERT INTO "rtk_hardware" VALUES(0,7,'','','',0,'',0.0,0.0,0.0,2,'',100.0,'','',1,0,10.0,'Assembly 11','','',2,0,'',1,'A11','None',0,'Specification',0,0,0,0.0,2014);
INSERT INTO "rtk_hardware" VALUES(0,8,'','','',0,'',0.0,0.0,0.0,1,'',100.0,'','',1,0,10.0,'Assembly 12','','',2,0,'',1,'A12','None',0,'Specification',0,0,0,0.0,2014);
INSERT INTO "rtk_hardware" VALUES(0,88,'','','',0,'',0.0,0.0,0.0,1,'',100.0,'','',1,0,100.0,'Sub-System 4','','',1,0,'',1,'SS4','None',0,'Specification',0,0,0,0.0,2014);
INSERT INTO "rtk_hardware" VALUES(0,102,'','','',0,'',0.0,0.0,0.0,1,'',100.0,'','',1,0,100.0,'Sub-Assembly 121','','',8,0,'',1,'SA121','None',0,'Specification',0,0,0,0.0,2014);
INSERT INTO "rtk_hardware" VALUES(0,105,'','','',0,'',0.0,0.0,0.0,1,'',85.0,'','',1,0,100.0,'Sub-Assembly 111','','',7,0,'',1,'SA111','None',0,'Specification',0,0,0,0.0,2014);
INSERT INTO "rtk_hardware" VALUES(0,115,'','','',0,'',0.0,0.0,0.0,1,'',100.0,'','',1,0,100.0,'Sub-Assembly 122','','',8,0,'XA4320195J6',1,'SA122','None',0,'Specification',0,0,0,0.0,2014);

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
INSERT INTO "rtk_allocation" VALUES(1,0.975,0.002532,394.978902,1,1,1,1960.0,1.0,1,1,1,1,0.0,0.0,0.0,0.0,-1,4,1);
INSERT INTO "rtk_allocation" VALUES(2,0.99228,0.000775,1290.330329,1,1,1,600.0,0.306122,3,5,10,4,0.0,0.99228,0.000775,1290.264413,0,4,1);
INSERT INTO "rtk_allocation" VALUES(3,0.989592,0.0,0.0,1,1,1,810.0,0.413265,5,3,9,6,0.0,0.989592,0.001046,955.751417,0,0,0);
INSERT INTO "rtk_allocation" VALUES(5,0.99639,0.000362,2764.852314,1,1,1,280.0,0.142857,2,2,10,7,0.0,0.99639,0.000362,2764.852314,0,4,1);
INSERT INTO "rtk_allocation" VALUES(6,0.998064,0.0,0.0,1,1,1,150.0,0.076531,5,1,6,5,0.0,0.998064,0.000194,5161.057653,0,0,0);
INSERT INTO "rtk_allocation" VALUES(7,1.0,0.0,0.0,1,1,1,0.0,1.0,3,2,10,4,0.0,0.997471,0.0,39497.890205,2,4,1);
INSERT INTO "rtk_allocation" VALUES(8,1.0,0.0,0.0,1,1,1,0.0,1.0,3,1,9,4,0.0,0.997471,0.0,39497.890205,2,0,0);
INSERT INTO "rtk_allocation" VALUES(88,1.0,0.0,0.0,1,1,1,1.0,1.0,1,1,1,1,0.0,0.0,0.0,0.0,0,0,0);
INSERT INTO "rtk_allocation" VALUES(102,1.0,0.0,0.0,1,1,1,1.0,1.0,6,4,9,4,0.0,0.0,0.0,0.0,8,0,0);
INSERT INTO "rtk_allocation" VALUES(105,1.0,0.0,0.0,1,1,1,1.0,1.0,1,1,1,1,0.0,0.0,0.0,0.0,7,4,1);
INSERT INTO "rtk_allocation" VALUES(115,1.0,0.0,0.0,1,1,1,1.0,1.0,4,5,9,4,0.0,0.0,0.0,0.0,8,4,1);

DROP TABLE IF EXISTS "rtk_hazard";
CREATE TABLE "rtk_hazard" (
    "fld_hardware_id" INTEGER NOT NULL DEFAULT(0),                  -- Hardware ID.
    "fld_hazard_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,     -- Hazard ID.
    "fld_potential_hazard" VARCHAR(128) DEFAULT(''),                -- Name of potential hazard.
    "fld_potential_cause" VARCHAR(512) DEFAULT(''),                 -- User-defined cause of potential hazard.
    "fld_assembly_effect" VARCHAR(512) DEFAULT(''),                 -- User-defined assembly-level effect of potential hazard.
    "fld_assembly_severity" INTEGER DEFAULT(4),                     -- Severity index of assembly-level effect.
    "fld_assembly_probability" INTEGER DEFAULT(5),                  -- Probability index of hazard.
    "fld_assembly_hri" INTEGER DEFAULT(20),                         -- Assembly-level hazard risk index (Severity x Probability).
    "fld_assembly_mitigation" BLOB DEFAULT(''),                     -- Assembly-level mitigation actions for potential hazard.
    "fld_assembly_severity_f" INTEGER DEFAULT(4),                   -- Assembly-level severity index after mitigation actions.
    "fld_assembly_probability_f" INTEGER DEFAULT(5),                -- Assembly-level probability index after mitigation actions.
    "fld_assembly_hri_f" INTEGER DEFAULT(20),                       -- Assembly-level hazard risk index after mitigation actions.
    "fld_system_effect" VARCHAR(512) DEFAULT(''),                   -- System-level effect of potential hazard.
    "fld_system_severity" INTEGER DEFAULT(4),                       -- Severity index of system-level effect.
    "fld_system_probability" INTEGER DEFAULT(5),                    -- System-level probability index of potential hazard.
    "fld_system_hri" INTEGER DEFAULT(20),                           -- System-level hazard risk index.
    "fld_system_mitigation" BLOB DEFAULT(''),                       -- System-level mitigation actions.
    "fld_system_severity_f" INTEGER DEFAULT(4),                     -- System-level severity index after mitigation actions.
    "fld_system_probability_f" INTEGER DEFAULT(5),                  -- System-level probability index after mitigation actions.
    "fld_system_hri_f" INTEGER DEFAULT(20),                         -- System-level hazard risk index after mitigation actions.
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
INSERT INTO "rtk_hazard" VALUES(1,0,'Electrical, Burns','','',3,2,6,'',4,5,20,'',4,5,20,'',4,5,20,'','','','','','',0.0,0.0,0.0,0.0,0.0,'','','',0.0,0.0,0.0,0,0,0);
INSERT INTO "rtk_hazard" VALUES(1,1,'','','',4,5,20,'',4,5,20,'',4,5,20,'',4,5,20,'','','','','','',0.0,0.0,0.0,0.0,0.0,'','','',0.0,0.0,0.0,0,0,0);
INSERT INTO "rtk_hazard" VALUES(1,2,'','','',4,5,20,'',4,5,20,'',4,5,20,'',4,5,20,'','','','','','',0.0,0.0,0.0,0.0,0.0,'','','',0.0,0.0,0.0,0,0,0);

DROP TABLE IF EXISTS "rtk_similar_item";
CREATE TABLE "rtk_similar_item" (
    "fld_hardware_id" INTEGER NOT NULL DEFAULT(0),                  -- Hardware ID.
    "fld_sia_id" INTEGER NOT NULL DEFAULT(0),                    -- Similar item analysis ID.
    "fld_method" INTEGER NOT NULL DEFAULT(0),
    "fld_from_quality" INTEGER DEFAULT(0),
    "fld_to_quality" INTEGER DEFAULT(0),
    "fld_from_environment" INTEGER DEFAULT(0),
    "fld_to_environment" INTEGER DEFAULT(0),
    "fld_from_temperature" FLOAT DEFAULT(30),
    "fld_to_temperature" FLOAT DEFAULT(30),
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
    CONSTRAINT "rtk_similar_item_fk" FOREIGN KEY("fld_hardware_id") REFERENCES "rtk_hardware"("fld_hardware_id") ON DELETE CASCADE
);
INSERT INTO "rtk_similar_item" VALUES(2,0,0,0,0,0,0,30.0,30.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'','','','','',0.0,0.0,0.0,0.0,0.0,'None','None','None','None','None',0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0);
INSERT INTO "rtk_similar_item" VALUES(88,0,0,4,2,1,2,30.0,30.0,'No changes',3.3,'No changes',0.2,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'','','','','',0.0,0.0,0.0,0.0,0.0,'None','None','None','None','None',0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0);
INSERT INTO "rtk_similar_item" VALUES(102,0,8,0,0,0,0,30.0,30.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'','','','','',0.0,0.0,0.0,0.0,0.0,'None','None','None','None','None',0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0);
INSERT INTO "rtk_similar_item" VALUES(105,0,7,0,0,3,0,30.0,30.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'','','','','',0.000648,0.0,0.0,0.0,0.0,'None','None','None','None','None',0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0);
INSERT INTO "rtk_similar_item" VALUES(115,0,8,0,0,0,0,30.0,30.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'No changes',1.0,'','','','','',0.0,0.0,0.0,0.0,0.0,'None','None','None','None','None',0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0);

DROP TABLE IF EXISTS "rtk_stress";
CREATE TABLE "rtk_stress" (
    "fld_hardware_id" INTEGER NOT NULL DEFAULT(0),                  -- Hardware ID.
    "fld_current_ratio" REAL DEFAULT(1),                            -- Ratio of operating to rated current.
    "fld_environment_active_id" INTEGER DEFAULT(0),                 -- ID of the operating environment.
    "fld_environment_dormant_id" INTEGER DEFAULT(0),                -- ID of the storage environment.
    "fld_humidity" REAL DEFAULT(50),                                -- Humidity of the operating environment.
    "fld_junction_temperature" REAL DEFAULT(30),                    -- Junction temperature of the hardware.
    "fld_knee_temperature" REAL DEFAULT(0),                         -- Derating knee temperature.
    "fld_max_rated_temperature" REAL DEFAULT(0),                    -- Derating maximum operating temperature.
    "fld_min_rated_temperature" REAL DEFAULT(0),                    -- Derating minumum operating temperature.
    "fld_operating_current" REAL DEFAULT(0),                        -- Operating current.
    "fld_operating_power" REAL DEFAULT(0),                          -- Operating power.
    "fld_operating_voltage" REAL DEFAULT(0),                        -- Operating voltage.
    "fld_overstress" TINYINT NOT NULL DEFAULT(0),                   -- Whether hardware item is overstressed.
    "fld_power_ratio" REAL DEFAULT(1),                              -- Ratio of operating to rated power.
    "fld_rated_current" REAL DEFAULT(1),                            -- Rated current of the hardware item.
    "fld_rated_power" REAL DEFAULT(1),                              -- Rated power of the hardware item.
    "fld_rated_voltage" REAL DEFAULT(1),                            -- Rated voltage of the hardware item.
    "fld_rpm" REAL DEFAULT(0),                                      -- Revolutions per minute of the hardware item.
    "fld_temperature_active" REAL DEFAULT(30.0),                    -- Operating temperature in Centigrade.
    "fld_temperature_dormant" REAL DEFAULT(25.0),                   -- Storage temperature in Centigrade.
    "fld_temperature_rise" REAL DEFAULT(0),                         -- Temperature rise of the hardware item.
    "fld_reason" BLOB,                                              -- The reason(s) the component is over-stressed.
    "fld_thermal_resistance" REAL DEFAULT(0),                       -- Thermal resistance of the hardware item.
    "fld_tref" REAL DEFAULT(0),                                     -- Reference temperature of the hardware item.
    "fld_vibration" REAL DEFAULT(0),                                -- Vibration the hardware item is exposed to in the operating environment.
    "fld_voltage_ratio" REAL DEFAULT(1),                            -- Ratio of operating to rated voltage.
    FOREIGN KEY("fld_hardware_id") REFERENCES "rtk_hardware"("fld_hardware_id") ON DELETE CASCADE
);
INSERT INTO "rtk_stress" VALUES(1,1.0,0,0,50.0,30.0,0.0,0.0,0.0,0.0,0.0,0.0,0,1.0,1.0,1.0,1.0,0.0,30.0,25.0,0.0,'Reason',0.0,0.0,0.0,1.0);
INSERT INTO "rtk_stress" VALUES(2,1.0,0,0,50.0,30.0,0.0,0.0,0.0,0.0,0.0,0.0,0,1.0,1.0,1.0,1.0,0.0,30.0,25.0,0.0,'Reason',0.0,0.0,0.0,1.0);
INSERT INTO "rtk_stress" VALUES(3,1.0,0,0,50.0,30.0,0.0,0.0,0.0,0.0,0.0,0.0,0,1.0,1.0,1.0,1.0,0.0,30.0,25.0,0.0,'Reason',0.0,0.0,0.0,1.0);
INSERT INTO "rtk_stress" VALUES(5,1.0,0,0,50.0,30.0,0.0,0.0,0.0,0.0,0.0,0.0,0,1.0,1.0,1.0,1.0,0.0,30.0,25.0,0.0,'Reason',0.0,0.0,0.0,1.0);

DROP TABLE IF EXISTS "rtk_reliability";
CREATE TABLE "rtk_reliability" (
    "fld_hardware_id" INTEGER NOT NULL DEFAULT(0),                  -- Hardware ID.
    "fld_add_adj_factor" REAL DEFAULT(0),                           -- Hazard rate additive adjustment factor.
    "fld_availability_logistics" REAL DEFAULT(1),                   -- Logistics availability.
    "fld_availability_mission" REAL DEFAULT(1),                     -- Mission availability.
    "fld_avail_log_variance" REAL DEFAULT(0),                       -- Variance of the logistics availability estimate.
    "fld_avail_mis_variance" REAL DEFAULT(0),                       -- Variance of the mission availability estimate.
    "fld_failure_distribution_id" INTEGER DEFAULT(0),               -- Failure distribution.
    "fld_scale_parameter" REAL DEFAULT(0),                          -- Scale parameter.
    "fld_shape_parameter" REAL DEFAULT(0),                          -- Shape parameter.
    "fld_location_parameter" REAL DEFAULT(0),                       -- Location parameter.
    "fld_hazard_rate_active" REAL DEFAULT(0),                       -- Active hazard rate.
    "fld_hazard_rate_dormant" REAL DEFAULT(0),                      -- Dormant hazard rate.
    "fld_hazard_rate_logistics" REAL DEFAULT(0),                    -- Logistics hazard rate.
    "fld_hazard_rate_method_id" INTEGER DEFAULT(1),                 -- Hazard rate calculation method to use (1=217FN2 Parts Count, 2=217FN2 Parts Stress, 3=NSWC-07).
    "fld_hazard_rate_mission" REAL DEFAULT(0),                      -- Mission hazard rate.
    "fld_hazard_rate_model" VARCHAR(512) DEFAULT(''),               -- Hazard rate mathematical model.
    "fld_hazard_rate_percent" REAL DEFAULT(0),                      -- Percent of system hazard rate attributable to this hardware item.
    "fld_hazard_rate_software" REAL DEFAULT(0),                     -- Software hazard rate.
    "fld_hazard_rate_specified" REAL DEFAULT(0),                    -- Specified hazard rate.
    "fld_hazard_rate_type_id" INTEGER DEFAULT(1),                   -- How the hazard rate is determined (1=Assessed, 2=Specified, Failure Rate, 3=Specified, MTBF)
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
    "fld_quality_id" INTEGER DEFAULT(0),                            -- ID of the quality level.
    "fld_reliability_goal" REAL DEFAULT(1.0),                       -- Reliability goal.
    "fld_reliability_goal_measure_id" INTEGER DEFAULT(0),           -- ID of the reliability goal measurement.
    "fld_reliability_logistics" REAL DEFAULT(1),                    -- Logistics reliability of the hardware item.
    "fld_reliability_mission" REAL DEFAULT(1),                      -- Mission reliability of the hardware item.
    "fld_rel_log_variance" REAL DEFAULT(0),                         -- Variance of the logistics reliability estimate.
    "fld_rel_miss_variance" REAL DEFAULT(0),                        -- Variance of the mission reliability estiamte.
    "fld_survival_analysis_id" INTEGER DEFAULT(0),                  -- ID of the survival data analysis to use.
    "fld_lambda_b" REAL DEFAULT(0.0),                               -- Base hazard rate of hardware item.
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
INSERT INTO "rtk_reliability" VALUES(1,0.0,1.0,1.0,0.0,0.0,0,0.0,0.0,0.0,0.00193413,2.84319e-09,0.00193413,1,0.0,'',0.0,0.0,0.0,2,0.0,0.0,0.0,0.0,0.0,517.028792,0.0,0.0,0.0,0.0,0.0,1.0,0,1.0,0,0.980845,1.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,0,0,0,0,'','','','','');
INSERT INTO "rtk_reliability" VALUES(2,0.0,1.0,1.0,0.0,0.0,0,0.0,0.0,0.0,0.00193411,0.0,0.00193411,1,0.0,'',0.0,0.0,0.0,1,0.0,0.0,0.0,0.0,0.0,517.033352,0.0,0.0,0.0,0.0,0.0,1.0,0,1.0,0,0.980845,1.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,0,0,0,0,'','','','','');
INSERT INTO "rtk_reliability" VALUES(3,0.0,1.0,1.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,1,0.0,'',0.0,0.0,0.0,1,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0,0.0,1.0,0,1.0,1.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,0,0,0,0,'','','','','');
INSERT INTO "rtk_reliability" VALUES(5,0.0,1.0,1.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,1,0.0,'',0.0,0.0,0.0,1,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0,0.0,1.0,0,1.0,1.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,0,0,0,0,'','','','','');


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
INSERT INTO "rtk_modes" VALUES(1,0,1,NULL,'Default Mission',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1.0,0.0,0.0,0.0,0.0,'','',0,0,NULL,1);
INSERT INTO "rtk_modes" VALUES(1,0,2,NULL,'Default Mission',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1.0,0.0,0.0,0.0,0.0,'','',0,0,NULL,1);
INSERT INTO "rtk_modes" VALUES(1,0,3,'Pressure is too high.','Default mission','Phase I','Bad things happen','More bad things happen','The worst things happen','','','','Not much we can do, just deal with it.','Scream and yell','II - Critical','','',1.0,0.0,0.0,0.0,0.0,'10','10',0,0,'This shit is bad.',0);
INSERT INTO "rtk_modes" VALUES(1,0,4,'Pressure is too low.','','','','','','','','','','','','','',1.0,0.0,0.0,0.0,0.0,'10','10',0,0,'',0);
INSERT INTO "rtk_modes" VALUES(1,0,5,'Pressure is erratic.','','','','','','','','','','','','','',1.0,0.0,0.0,0.0,0.0,'10','10',0,0,'',0);

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
INSERT INTO "rtk_mechanisms" VALUES(1,0,1,1,NULL,0,0,0,0,0,0,1);
INSERT INTO "rtk_mechanisms" VALUES(1,0,1,2,NULL,0,0,0,0,0,0,1);
INSERT INTO "rtk_mechanisms" VALUES(1,0,2,3,NULL,0,0,0,0,0,0,1);
INSERT INTO "rtk_mechanisms" VALUES(1,0,2,4,NULL,0,0,0,0,0,0,1);

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
INSERT INTO "rtk_causes" VALUES(1,1,1,'',0,0,0,0,0,0);
INSERT INTO "rtk_causes" VALUES(1,1,2,'',0,0,0,0,0,0);
INSERT INTO "rtk_causes" VALUES(1,2,3,'',0,0,0,0,0,0);
INSERT INTO "rtk_causes" VALUES(1,2,4,'',0,0,0,0,0,0);
INSERT INTO "rtk_causes" VALUES(2,3,5,'',0,0,0,0,0,0);
INSERT INTO "rtk_causes" VALUES(2,3,6,'',0,0,0,0,0,0);
INSERT INTO "rtk_causes" VALUES(2,4,7,'',0,0,0,0,0,0);
INSERT INTO "rtk_causes" VALUES(2,4,8,'',0,0,0,0,0,0);

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
INSERT INTO "rtk_controls" VALUES(1,1,1,1,NULL,0);
INSERT INTO "rtk_controls" VALUES(1,1,2,2,NULL,0);
INSERT INTO "rtk_controls" VALUES(1,2,3,3,NULL,0);
INSERT INTO "rtk_controls" VALUES(1,2,4,4,NULL,0);
INSERT INTO "rtk_controls" VALUES(2,3,5,5,NULL,0);
INSERT INTO "rtk_controls" VALUES(2,3,6,6,NULL,0);
INSERT INTO "rtk_controls" VALUES(2,4,7,7,NULL,0);
INSERT INTO "rtk_controls" VALUES(2,4,8,8,NULL,0);

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

DROP TABLE IF EXISTS "rtk_op_loads";
CREATE TABLE "rtk_op_loads" (
    "fld_mechanism_id" INTEGER DEFAULT(0),                          -- ID of the failure mechanism.
    "fld_load_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,       -- ID of the operating load condition.
    "fld_load_description" VARCHAR(512) DEFAULT(''),                -- Description of the operating load condition.
    "fld_damage_model" INTEGER DEFAULT(0),                          -- Damage model describing accumulation of damage.
    "fld_priority" INTEGER DEFAULT(0),                              -- Priority of the load.
    FOREIGN KEY("fld_mechanism_id") REFERENCES "rtk_mechanisms"("fld_mechanism_id") ON DELETE CASCADE
);
INSERT INTO "rtk_op_loads" VALUES(1,0,'',3,3);
INSERT INTO "rtk_op_loads" VALUES(1,1,'',0,0);
INSERT INTO "rtk_op_loads" VALUES(2,2,'',0,0);
INSERT INTO "rtk_op_loads" VALUES(2,3,'',0,0);
INSERT INTO "rtk_op_loads" VALUES(3,4,'',0,0);
INSERT INTO "rtk_op_loads" VALUES(4,5,'',0,0);

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
INSERT INTO "rtk_op_stress" VALUES(0,0,'',1,8,'');
INSERT INTO "rtk_op_stress" VALUES(0,1,'Stress Description',17,2,'');
INSERT INTO "rtk_op_stress" VALUES(1,2,'',0,0,'None');
INSERT INTO "rtk_op_stress" VALUES(1,3,'Stress Description',2,3,'Remarks');
INSERT INTO "rtk_op_stress" VALUES(2,4,'',0,0,'None');
INSERT INTO "rtk_op_stress" VALUES(2,5,'Stress Description',2,3,'Remarks');
INSERT INTO "rtk_op_stress" VALUES(3,6,'',0,0,'None');
INSERT INTO "rtk_op_stress" VALUES(3,7,'Stress Description',2,3,'Remarks');
INSERT INTO "rtk_op_stress" VALUES(4,8,'',0,0,'None');
INSERT INTO "rtk_op_stress" VALUES(4,9,'Stress Description',2,3,'Remarks');
INSERT INTO "rtk_op_stress" VALUES(5,10,'',0,0,'None');
INSERT INTO "rtk_op_stress" VALUES(5,11,'Stress Description',2,3,'Remarks');

DROP TABLE IF EXISTS "rtk_test_methods";
CREATE TABLE "rtk_test_methods" (
    "fld_stress_id" INTEGER NOT NULL DEFAULT(0),                    -- ID of the operating stress associated with the test.
    "fld_method_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,     -- ID of the test method.
    "fld_method_description" VARCHAR(512) DEFAULT(''),              -- Applicable test method(s) to simulate the stress.
    "fld_boundary_conditions" VARCHAR(256) DEFAULT(''),             -- Applicable boundary conditions for the test method.
    "fld_remarks" BLOB,                                             -- User remarks/notes.
    FOREIGN KEY("fld_stress_id") REFERENCES "rtk_op_stress"("fld_stress_id") ON DELETE CASCADE
);
INSERT INTO "rtk_test_methods" VALUES(3,0,'Test Description','Test Boundary Conditions','Test Remarks');

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
INSERT INTO "rtk_software" VALUES(0,0,1,'System Software',0,0,0.0,0.0,0,0.767442,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0.0,0,0,0,0,0.0,0,0,0,0.0,0.0,0.0,0.0,0.0,-1,1,1,0,0,0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,0,0.9,1.0,1.0,0.9,0.0,0.0,0.0,0.0,0.0,0.1,0.0,0.0,0.0,0.0,0.0,0,0,0,0.0,0,0.0);
INSERT INTO "rtk_software" VALUES(0,1,2,'CSCI',0,0,0.0,0.0,0,0.0,2.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0.0,0,0,0,0,1.5,0,0,0,2.0,0.0,0.0,0.0,0.0,0,1,1,0,0,0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,0,0.9,1.0,1.0,0.9,0.0,0.0,0.0,0.0,0.0,0.1,0.0,0.0,0.0,0.0,0.0,0,0,0,0.0,0,0.0);
INSERT INTO "rtk_software" VALUES(0,2,3,'Unit',0,0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0.0,0,0,0,0,0.0,0,0,0,0.0,0.0,0.0,0.0,0.0,1,1,1,0,0,0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0.0,0,0.0);
INSERT INTO "rtk_software" VALUES(0,3,2,'CSCI',0,0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0.0,0,0,0,0,0.0,0,0,0,0.0,0.0,0.0,0.0,0.0,0,1,1,0,0,0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0.0,0,0.0);
INSERT INTO "rtk_software" VALUES(0,4,3,'Unit',0,0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0.0,0,0,0,0,0.0,0,0,0,0.0,0.0,0.0,0.0,0.0,3,1,1,0,0,0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0,0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0,0,0.0,0,0.0);

DROP TABLE IF EXISTS "rtk_software_development";
CREATE TABLE "rtk_software_development" (
    "fld_software_id" INTEGER NOT NULL DEFAULT (0),                 -- Software module ID.
    "fld_question_id" INTEGER NOT NULL DEFAULT (0),                 -- Question ID.
    "fld_y" TINYINT DEFAULT (0),                                    -- Value of Y/N question.
    FOREIGN KEY("fld_software_id") REFERENCES "rtk_software"("fld_software_id") ON DELETE CASCADE
);
INSERT INTO "rtk_software_development" VALUES(0,0,1);
INSERT INTO "rtk_software_development" VALUES(0,1,1);
INSERT INTO "rtk_software_development" VALUES(0,2,1);
INSERT INTO "rtk_software_development" VALUES(0,3,1);
INSERT INTO "rtk_software_development" VALUES(0,4,1);
INSERT INTO "rtk_software_development" VALUES(0,5,1);
INSERT INTO "rtk_software_development" VALUES(0,6,1);
INSERT INTO "rtk_software_development" VALUES(0,7,1);
INSERT INTO "rtk_software_development" VALUES(0,8,1);
INSERT INTO "rtk_software_development" VALUES(0,9,1);
INSERT INTO "rtk_software_development" VALUES(0,10,1);
INSERT INTO "rtk_software_development" VALUES(0,11,1);
INSERT INTO "rtk_software_development" VALUES(0,12,1);
INSERT INTO "rtk_software_development" VALUES(0,13,0);
INSERT INTO "rtk_software_development" VALUES(0,14,1);
INSERT INTO "rtk_software_development" VALUES(0,15,1);
INSERT INTO "rtk_software_development" VALUES(0,16,1);
INSERT INTO "rtk_software_development" VALUES(0,17,1);
INSERT INTO "rtk_software_development" VALUES(0,18,1);
INSERT INTO "rtk_software_development" VALUES(0,19,1);
INSERT INTO "rtk_software_development" VALUES(0,20,0);
INSERT INTO "rtk_software_development" VALUES(0,21,1);
INSERT INTO "rtk_software_development" VALUES(0,22,1);
INSERT INTO "rtk_software_development" VALUES(0,23,1);
INSERT INTO "rtk_software_development" VALUES(0,24,0);
INSERT INTO "rtk_software_development" VALUES(0,25,1);
INSERT INTO "rtk_software_development" VALUES(0,26,0);
INSERT INTO "rtk_software_development" VALUES(0,27,1);
INSERT INTO "rtk_software_development" VALUES(0,28,0);
INSERT INTO "rtk_software_development" VALUES(0,29,1);
INSERT INTO "rtk_software_development" VALUES(0,30,1);
INSERT INTO "rtk_software_development" VALUES(0,31,1);
INSERT INTO "rtk_software_development" VALUES(0,32,1);
INSERT INTO "rtk_software_development" VALUES(0,33,1);
INSERT INTO "rtk_software_development" VALUES(0,34,0);
INSERT INTO "rtk_software_development" VALUES(0,35,1);
INSERT INTO "rtk_software_development" VALUES(0,36,0);
INSERT INTO "rtk_software_development" VALUES(0,37,1);
INSERT INTO "rtk_software_development" VALUES(0,38,0);
INSERT INTO "rtk_software_development" VALUES(0,39,0);
INSERT INTO "rtk_software_development" VALUES(0,40,1);
INSERT INTO "rtk_software_development" VALUES(0,41,1);
INSERT INTO "rtk_software_development" VALUES(0,42,0);
INSERT INTO "rtk_software_development" VALUES(1,0,0);
INSERT INTO "rtk_software_development" VALUES(1,1,0);
INSERT INTO "rtk_software_development" VALUES(1,2,0);
INSERT INTO "rtk_software_development" VALUES(1,3,0);
INSERT INTO "rtk_software_development" VALUES(1,4,0);
INSERT INTO "rtk_software_development" VALUES(1,5,0);
INSERT INTO "rtk_software_development" VALUES(1,6,0);
INSERT INTO "rtk_software_development" VALUES(1,7,0);
INSERT INTO "rtk_software_development" VALUES(1,8,0);
INSERT INTO "rtk_software_development" VALUES(1,9,0);
INSERT INTO "rtk_software_development" VALUES(1,10,0);
INSERT INTO "rtk_software_development" VALUES(1,11,0);
INSERT INTO "rtk_software_development" VALUES(1,12,0);
INSERT INTO "rtk_software_development" VALUES(1,13,0);
INSERT INTO "rtk_software_development" VALUES(1,14,0);
INSERT INTO "rtk_software_development" VALUES(1,15,0);
INSERT INTO "rtk_software_development" VALUES(1,16,0);
INSERT INTO "rtk_software_development" VALUES(1,17,0);
INSERT INTO "rtk_software_development" VALUES(1,18,0);
INSERT INTO "rtk_software_development" VALUES(1,19,0);
INSERT INTO "rtk_software_development" VALUES(1,20,0);
INSERT INTO "rtk_software_development" VALUES(1,21,0);
INSERT INTO "rtk_software_development" VALUES(1,22,0);
INSERT INTO "rtk_software_development" VALUES(1,23,0);
INSERT INTO "rtk_software_development" VALUES(1,24,0);
INSERT INTO "rtk_software_development" VALUES(1,25,0);
INSERT INTO "rtk_software_development" VALUES(1,26,0);
INSERT INTO "rtk_software_development" VALUES(1,27,0);
INSERT INTO "rtk_software_development" VALUES(1,28,0);
INSERT INTO "rtk_software_development" VALUES(1,29,0);
INSERT INTO "rtk_software_development" VALUES(1,30,0);
INSERT INTO "rtk_software_development" VALUES(1,31,0);
INSERT INTO "rtk_software_development" VALUES(1,32,0);
INSERT INTO "rtk_software_development" VALUES(1,33,0);
INSERT INTO "rtk_software_development" VALUES(1,34,0);
INSERT INTO "rtk_software_development" VALUES(1,35,0);
INSERT INTO "rtk_software_development" VALUES(1,36,0);
INSERT INTO "rtk_software_development" VALUES(1,37,0);
INSERT INTO "rtk_software_development" VALUES(1,38,0);
INSERT INTO "rtk_software_development" VALUES(1,39,0);
INSERT INTO "rtk_software_development" VALUES(1,40,0);
INSERT INTO "rtk_software_development" VALUES(1,41,0);
INSERT INTO "rtk_software_development" VALUES(1,42,0);
INSERT INTO "rtk_software_development" VALUES(2,0,0);
INSERT INTO "rtk_software_development" VALUES(2,1,0);
INSERT INTO "rtk_software_development" VALUES(2,2,0);
INSERT INTO "rtk_software_development" VALUES(2,3,0);
INSERT INTO "rtk_software_development" VALUES(2,4,0);
INSERT INTO "rtk_software_development" VALUES(2,5,0);
INSERT INTO "rtk_software_development" VALUES(2,6,0);
INSERT INTO "rtk_software_development" VALUES(2,7,0);
INSERT INTO "rtk_software_development" VALUES(2,8,0);
INSERT INTO "rtk_software_development" VALUES(2,9,0);
INSERT INTO "rtk_software_development" VALUES(2,10,0);
INSERT INTO "rtk_software_development" VALUES(2,11,0);
INSERT INTO "rtk_software_development" VALUES(2,12,0);
INSERT INTO "rtk_software_development" VALUES(2,13,0);
INSERT INTO "rtk_software_development" VALUES(2,14,0);
INSERT INTO "rtk_software_development" VALUES(2,15,0);
INSERT INTO "rtk_software_development" VALUES(2,16,0);
INSERT INTO "rtk_software_development" VALUES(2,17,0);
INSERT INTO "rtk_software_development" VALUES(2,18,0);
INSERT INTO "rtk_software_development" VALUES(2,19,0);
INSERT INTO "rtk_software_development" VALUES(2,20,0);
INSERT INTO "rtk_software_development" VALUES(2,21,0);
INSERT INTO "rtk_software_development" VALUES(2,22,0);
INSERT INTO "rtk_software_development" VALUES(2,23,0);
INSERT INTO "rtk_software_development" VALUES(2,24,0);
INSERT INTO "rtk_software_development" VALUES(2,25,0);
INSERT INTO "rtk_software_development" VALUES(2,26,0);
INSERT INTO "rtk_software_development" VALUES(2,27,0);
INSERT INTO "rtk_software_development" VALUES(2,28,0);
INSERT INTO "rtk_software_development" VALUES(2,29,0);
INSERT INTO "rtk_software_development" VALUES(2,30,0);
INSERT INTO "rtk_software_development" VALUES(2,31,0);
INSERT INTO "rtk_software_development" VALUES(2,32,0);
INSERT INTO "rtk_software_development" VALUES(2,33,0);
INSERT INTO "rtk_software_development" VALUES(2,34,0);
INSERT INTO "rtk_software_development" VALUES(2,35,0);
INSERT INTO "rtk_software_development" VALUES(2,36,0);
INSERT INTO "rtk_software_development" VALUES(2,37,0);
INSERT INTO "rtk_software_development" VALUES(2,38,0);
INSERT INTO "rtk_software_development" VALUES(2,39,0);
INSERT INTO "rtk_software_development" VALUES(2,40,0);
INSERT INTO "rtk_software_development" VALUES(2,41,0);
INSERT INTO "rtk_software_development" VALUES(2,42,0);
INSERT INTO "rtk_software_development" VALUES(3,0,0);
INSERT INTO "rtk_software_development" VALUES(3,1,0);
INSERT INTO "rtk_software_development" VALUES(3,2,0);
INSERT INTO "rtk_software_development" VALUES(3,3,0);
INSERT INTO "rtk_software_development" VALUES(3,4,0);
INSERT INTO "rtk_software_development" VALUES(3,5,0);
INSERT INTO "rtk_software_development" VALUES(3,6,0);
INSERT INTO "rtk_software_development" VALUES(3,7,0);
INSERT INTO "rtk_software_development" VALUES(3,8,0);
INSERT INTO "rtk_software_development" VALUES(3,9,0);
INSERT INTO "rtk_software_development" VALUES(3,10,0);
INSERT INTO "rtk_software_development" VALUES(3,11,0);
INSERT INTO "rtk_software_development" VALUES(3,12,0);
INSERT INTO "rtk_software_development" VALUES(3,13,0);
INSERT INTO "rtk_software_development" VALUES(3,14,0);
INSERT INTO "rtk_software_development" VALUES(3,15,0);
INSERT INTO "rtk_software_development" VALUES(3,16,0);
INSERT INTO "rtk_software_development" VALUES(3,17,0);
INSERT INTO "rtk_software_development" VALUES(3,18,0);
INSERT INTO "rtk_software_development" VALUES(3,19,0);
INSERT INTO "rtk_software_development" VALUES(3,20,0);
INSERT INTO "rtk_software_development" VALUES(3,21,0);
INSERT INTO "rtk_software_development" VALUES(3,22,0);
INSERT INTO "rtk_software_development" VALUES(3,23,0);
INSERT INTO "rtk_software_development" VALUES(3,24,0);
INSERT INTO "rtk_software_development" VALUES(3,25,0);
INSERT INTO "rtk_software_development" VALUES(3,26,0);
INSERT INTO "rtk_software_development" VALUES(3,27,0);
INSERT INTO "rtk_software_development" VALUES(3,28,0);
INSERT INTO "rtk_software_development" VALUES(3,29,0);
INSERT INTO "rtk_software_development" VALUES(3,30,0);
INSERT INTO "rtk_software_development" VALUES(3,31,0);
INSERT INTO "rtk_software_development" VALUES(3,32,0);
INSERT INTO "rtk_software_development" VALUES(3,33,0);
INSERT INTO "rtk_software_development" VALUES(3,34,0);
INSERT INTO "rtk_software_development" VALUES(3,35,0);
INSERT INTO "rtk_software_development" VALUES(3,36,0);
INSERT INTO "rtk_software_development" VALUES(3,37,0);
INSERT INTO "rtk_software_development" VALUES(3,38,0);
INSERT INTO "rtk_software_development" VALUES(3,39,0);
INSERT INTO "rtk_software_development" VALUES(3,40,0);
INSERT INTO "rtk_software_development" VALUES(3,41,0);
INSERT INTO "rtk_software_development" VALUES(3,42,0);
INSERT INTO "rtk_software_development" VALUES(4,0,0);
INSERT INTO "rtk_software_development" VALUES(4,1,0);
INSERT INTO "rtk_software_development" VALUES(4,2,0);
INSERT INTO "rtk_software_development" VALUES(4,3,0);
INSERT INTO "rtk_software_development" VALUES(4,4,0);
INSERT INTO "rtk_software_development" VALUES(4,5,0);
INSERT INTO "rtk_software_development" VALUES(4,6,0);
INSERT INTO "rtk_software_development" VALUES(4,7,0);
INSERT INTO "rtk_software_development" VALUES(4,8,0);
INSERT INTO "rtk_software_development" VALUES(4,9,0);
INSERT INTO "rtk_software_development" VALUES(4,10,0);
INSERT INTO "rtk_software_development" VALUES(4,11,0);
INSERT INTO "rtk_software_development" VALUES(4,12,0);
INSERT INTO "rtk_software_development" VALUES(4,13,0);
INSERT INTO "rtk_software_development" VALUES(4,14,0);
INSERT INTO "rtk_software_development" VALUES(4,15,0);
INSERT INTO "rtk_software_development" VALUES(4,16,0);
INSERT INTO "rtk_software_development" VALUES(4,17,0);
INSERT INTO "rtk_software_development" VALUES(4,18,0);
INSERT INTO "rtk_software_development" VALUES(4,19,0);
INSERT INTO "rtk_software_development" VALUES(4,20,0);
INSERT INTO "rtk_software_development" VALUES(4,21,0);
INSERT INTO "rtk_software_development" VALUES(4,22,0);
INSERT INTO "rtk_software_development" VALUES(4,23,0);
INSERT INTO "rtk_software_development" VALUES(4,24,0);
INSERT INTO "rtk_software_development" VALUES(4,25,0);
INSERT INTO "rtk_software_development" VALUES(4,26,0);
INSERT INTO "rtk_software_development" VALUES(4,27,0);
INSERT INTO "rtk_software_development" VALUES(4,28,0);
INSERT INTO "rtk_software_development" VALUES(4,29,0);
INSERT INTO "rtk_software_development" VALUES(4,30,0);
INSERT INTO "rtk_software_development" VALUES(4,31,0);
INSERT INTO "rtk_software_development" VALUES(4,32,0);
INSERT INTO "rtk_software_development" VALUES(4,33,0);
INSERT INTO "rtk_software_development" VALUES(4,34,0);
INSERT INTO "rtk_software_development" VALUES(4,35,0);
INSERT INTO "rtk_software_development" VALUES(4,36,0);
INSERT INTO "rtk_software_development" VALUES(4,37,0);
INSERT INTO "rtk_software_development" VALUES(4,38,0);
INSERT INTO "rtk_software_development" VALUES(4,39,0);
INSERT INTO "rtk_software_development" VALUES(4,40,0);
INSERT INTO "rtk_software_development" VALUES(4,41,0);
INSERT INTO "rtk_software_development" VALUES(4,42,0);

DROP TABLE IF EXISTS "rtk_srr_ssr";
CREATE TABLE "rtk_srr_ssr" (
    "fld_software_id" INTEGER NOT NULL DEFAULT (0),                 -- Software module ID.
    "fld_question_id" INTEGER NOT NULL DEFAULT (0),                 -- Question ID.
    "fld_y" TINYINT DEFAULT (0),                                    -- Value of Y/N question.
    "fld_value" INTEGER DEFAULT (0),                                -- Value of quantity question.
    FOREIGN KEY("fld_software_id") REFERENCES "rtk_software"("fld_software_id") ON DELETE CASCADE
);
INSERT INTO "rtk_srr_ssr" VALUES(0,0,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,1,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,2,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,3,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,4,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,5,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,6,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,7,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,8,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,9,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,10,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,11,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,12,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,13,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,14,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,15,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,16,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,17,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,18,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,19,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,20,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,21,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,22,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,23,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,24,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,25,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,26,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,27,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,28,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,29,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,30,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,31,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,32,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,33,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,34,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,35,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,36,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,37,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,38,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,39,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,40,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,41,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,42,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,43,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,44,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,45,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,46,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,47,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,48,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(0,49,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,0,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,1,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,2,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,3,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,4,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,5,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,6,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,7,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,8,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,9,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,10,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,11,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,12,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,13,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,14,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,15,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,16,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,17,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,18,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,19,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,20,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,21,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,22,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,23,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,24,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,25,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,26,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,27,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,28,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,29,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,30,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,31,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,32,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,33,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,34,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,35,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,36,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,37,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,38,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,39,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,40,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,41,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,42,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,43,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,44,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,45,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,46,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,47,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,48,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(1,49,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,0,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,1,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,2,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,3,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,4,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,5,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,6,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,7,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,8,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,9,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,10,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,11,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,12,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,13,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,14,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,15,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,16,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,17,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,18,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,19,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,20,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,21,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,22,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,23,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,24,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,25,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,26,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,27,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,28,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,29,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,30,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,31,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,32,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,33,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,34,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,35,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,36,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,37,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,38,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,39,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,40,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,41,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,42,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,43,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,44,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,45,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,46,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,47,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,48,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(2,49,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,0,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,1,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,2,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,3,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,4,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,5,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,6,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,7,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,8,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,9,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,10,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,11,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,12,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,13,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,14,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,15,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,16,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,17,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,18,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,19,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,20,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,21,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,22,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,23,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,24,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,25,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,26,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,27,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,28,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,29,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,30,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,31,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,32,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,33,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,34,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,35,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,36,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,37,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,38,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,39,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,40,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,41,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,42,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,43,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,44,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,45,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,46,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,47,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,48,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(3,49,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,0,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,1,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,2,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,3,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,4,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,5,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,6,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,7,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,8,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,9,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,10,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,11,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,12,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,13,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,14,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,15,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,16,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,17,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,18,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,19,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,20,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,21,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,22,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,23,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,24,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,25,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,26,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,27,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,28,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,29,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,30,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,31,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,32,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,33,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,34,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,35,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,36,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,37,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,38,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,39,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,40,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,41,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,42,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,43,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,44,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,45,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,46,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,47,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,48,0,0);
INSERT INTO "rtk_srr_ssr" VALUES(4,49,0,0);

DROP TABLE IF EXISTS "rtk_pdr";
CREATE TABLE "rtk_pdr" (
    "fld_software_id" INTEGER NOT NULL DEFAULT (0),                 -- Software module ID.
    "fld_question_id" INTEGER NOT NULL DEFAULT (0),                 -- Question ID.
    "fld_y" TINYINT DEFAULT (0),                                    -- Value of Y/N question.
    "fld_value" INTEGER DEFAULT (0),                                -- Value of quantity question.
    FOREIGN KEY("fld_software_id") REFERENCES "rtk_software"("fld_software_id") ON DELETE CASCADE
);
INSERT INTO "rtk_pdr" VALUES(0,0,0,0);
INSERT INTO "rtk_pdr" VALUES(0,1,0,0);
INSERT INTO "rtk_pdr" VALUES(0,2,0,0);
INSERT INTO "rtk_pdr" VALUES(0,3,0,0);
INSERT INTO "rtk_pdr" VALUES(0,4,0,0);
INSERT INTO "rtk_pdr" VALUES(0,5,0,0);
INSERT INTO "rtk_pdr" VALUES(0,6,0,0);
INSERT INTO "rtk_pdr" VALUES(0,7,0,0);
INSERT INTO "rtk_pdr" VALUES(0,8,0,0);
INSERT INTO "rtk_pdr" VALUES(0,9,0,0);
INSERT INTO "rtk_pdr" VALUES(0,10,0,0);
INSERT INTO "rtk_pdr" VALUES(0,11,0,0);
INSERT INTO "rtk_pdr" VALUES(0,12,0,0);
INSERT INTO "rtk_pdr" VALUES(0,13,0,0);
INSERT INTO "rtk_pdr" VALUES(0,14,0,0);
INSERT INTO "rtk_pdr" VALUES(0,15,0,0);
INSERT INTO "rtk_pdr" VALUES(0,16,0,0);
INSERT INTO "rtk_pdr" VALUES(0,17,0,0);
INSERT INTO "rtk_pdr" VALUES(0,18,0,0);
INSERT INTO "rtk_pdr" VALUES(0,19,0,0);
INSERT INTO "rtk_pdr" VALUES(0,20,0,0);
INSERT INTO "rtk_pdr" VALUES(0,21,0,0);
INSERT INTO "rtk_pdr" VALUES(0,22,0,0);
INSERT INTO "rtk_pdr" VALUES(0,23,0,0);
INSERT INTO "rtk_pdr" VALUES(0,24,0,0);
INSERT INTO "rtk_pdr" VALUES(0,25,0,0);
INSERT INTO "rtk_pdr" VALUES(0,26,0,0);
INSERT INTO "rtk_pdr" VALUES(0,27,0,0);
INSERT INTO "rtk_pdr" VALUES(0,28,0,0);
INSERT INTO "rtk_pdr" VALUES(0,29,0,0);
INSERT INTO "rtk_pdr" VALUES(0,30,0,0);
INSERT INTO "rtk_pdr" VALUES(0,31,0,0);
INSERT INTO "rtk_pdr" VALUES(0,32,0,0);
INSERT INTO "rtk_pdr" VALUES(0,33,0,0);
INSERT INTO "rtk_pdr" VALUES(0,34,0,0);
INSERT INTO "rtk_pdr" VALUES(0,35,0,0);
INSERT INTO "rtk_pdr" VALUES(0,36,0,0);
INSERT INTO "rtk_pdr" VALUES(0,37,0,0);
INSERT INTO "rtk_pdr" VALUES(0,38,0,0);
INSERT INTO "rtk_pdr" VALUES(1,0,0,0);
INSERT INTO "rtk_pdr" VALUES(1,1,0,0);
INSERT INTO "rtk_pdr" VALUES(1,2,0,0);
INSERT INTO "rtk_pdr" VALUES(1,3,0,0);
INSERT INTO "rtk_pdr" VALUES(1,4,0,0);
INSERT INTO "rtk_pdr" VALUES(1,5,0,0);
INSERT INTO "rtk_pdr" VALUES(1,6,0,0);
INSERT INTO "rtk_pdr" VALUES(1,7,0,0);
INSERT INTO "rtk_pdr" VALUES(1,8,0,0);
INSERT INTO "rtk_pdr" VALUES(1,9,0,0);
INSERT INTO "rtk_pdr" VALUES(1,10,0,0);
INSERT INTO "rtk_pdr" VALUES(1,11,0,0);
INSERT INTO "rtk_pdr" VALUES(1,12,0,0);
INSERT INTO "rtk_pdr" VALUES(1,13,0,0);
INSERT INTO "rtk_pdr" VALUES(1,14,0,0);
INSERT INTO "rtk_pdr" VALUES(1,15,0,0);
INSERT INTO "rtk_pdr" VALUES(1,16,0,0);
INSERT INTO "rtk_pdr" VALUES(1,17,0,0);
INSERT INTO "rtk_pdr" VALUES(1,18,0,0);
INSERT INTO "rtk_pdr" VALUES(1,19,0,0);
INSERT INTO "rtk_pdr" VALUES(1,20,0,0);
INSERT INTO "rtk_pdr" VALUES(1,21,0,0);
INSERT INTO "rtk_pdr" VALUES(1,22,0,0);
INSERT INTO "rtk_pdr" VALUES(1,23,0,0);
INSERT INTO "rtk_pdr" VALUES(1,24,0,0);
INSERT INTO "rtk_pdr" VALUES(1,25,0,0);
INSERT INTO "rtk_pdr" VALUES(1,26,0,0);
INSERT INTO "rtk_pdr" VALUES(1,27,0,0);
INSERT INTO "rtk_pdr" VALUES(1,28,0,0);
INSERT INTO "rtk_pdr" VALUES(1,29,0,0);
INSERT INTO "rtk_pdr" VALUES(1,30,0,0);
INSERT INTO "rtk_pdr" VALUES(1,31,0,0);
INSERT INTO "rtk_pdr" VALUES(1,32,0,0);
INSERT INTO "rtk_pdr" VALUES(1,33,0,0);
INSERT INTO "rtk_pdr" VALUES(1,34,0,0);
INSERT INTO "rtk_pdr" VALUES(1,35,0,0);
INSERT INTO "rtk_pdr" VALUES(1,36,0,0);
INSERT INTO "rtk_pdr" VALUES(1,37,0,0);
INSERT INTO "rtk_pdr" VALUES(1,38,0,0);
INSERT INTO "rtk_pdr" VALUES(2,0,0,0);
INSERT INTO "rtk_pdr" VALUES(2,1,0,0);
INSERT INTO "rtk_pdr" VALUES(2,2,0,0);
INSERT INTO "rtk_pdr" VALUES(2,3,0,0);
INSERT INTO "rtk_pdr" VALUES(2,4,0,0);
INSERT INTO "rtk_pdr" VALUES(2,5,0,0);
INSERT INTO "rtk_pdr" VALUES(2,6,0,0);
INSERT INTO "rtk_pdr" VALUES(2,7,0,0);
INSERT INTO "rtk_pdr" VALUES(2,8,0,0);
INSERT INTO "rtk_pdr" VALUES(2,9,0,0);
INSERT INTO "rtk_pdr" VALUES(2,10,0,0);
INSERT INTO "rtk_pdr" VALUES(2,11,0,0);
INSERT INTO "rtk_pdr" VALUES(2,12,0,0);
INSERT INTO "rtk_pdr" VALUES(2,13,0,0);
INSERT INTO "rtk_pdr" VALUES(2,14,0,0);
INSERT INTO "rtk_pdr" VALUES(2,15,0,0);
INSERT INTO "rtk_pdr" VALUES(2,16,0,0);
INSERT INTO "rtk_pdr" VALUES(2,17,0,0);
INSERT INTO "rtk_pdr" VALUES(2,18,0,0);
INSERT INTO "rtk_pdr" VALUES(2,19,0,0);
INSERT INTO "rtk_pdr" VALUES(2,20,0,0);
INSERT INTO "rtk_pdr" VALUES(2,21,0,0);
INSERT INTO "rtk_pdr" VALUES(2,22,0,0);
INSERT INTO "rtk_pdr" VALUES(2,23,0,0);
INSERT INTO "rtk_pdr" VALUES(2,24,0,0);
INSERT INTO "rtk_pdr" VALUES(2,25,0,0);
INSERT INTO "rtk_pdr" VALUES(2,26,0,0);
INSERT INTO "rtk_pdr" VALUES(2,27,0,0);
INSERT INTO "rtk_pdr" VALUES(2,28,0,0);
INSERT INTO "rtk_pdr" VALUES(2,29,0,0);
INSERT INTO "rtk_pdr" VALUES(2,30,0,0);
INSERT INTO "rtk_pdr" VALUES(2,31,0,0);
INSERT INTO "rtk_pdr" VALUES(2,32,0,0);
INSERT INTO "rtk_pdr" VALUES(2,33,0,0);
INSERT INTO "rtk_pdr" VALUES(2,34,0,0);
INSERT INTO "rtk_pdr" VALUES(2,35,0,0);
INSERT INTO "rtk_pdr" VALUES(2,36,0,0);
INSERT INTO "rtk_pdr" VALUES(2,37,0,0);
INSERT INTO "rtk_pdr" VALUES(2,38,0,0);
INSERT INTO "rtk_pdr" VALUES(3,0,0,0);
INSERT INTO "rtk_pdr" VALUES(3,1,0,0);
INSERT INTO "rtk_pdr" VALUES(3,2,0,0);
INSERT INTO "rtk_pdr" VALUES(3,3,0,0);
INSERT INTO "rtk_pdr" VALUES(3,4,0,0);
INSERT INTO "rtk_pdr" VALUES(3,5,0,0);
INSERT INTO "rtk_pdr" VALUES(3,6,0,0);
INSERT INTO "rtk_pdr" VALUES(3,7,0,0);
INSERT INTO "rtk_pdr" VALUES(3,8,0,0);
INSERT INTO "rtk_pdr" VALUES(3,9,0,0);
INSERT INTO "rtk_pdr" VALUES(3,10,0,0);
INSERT INTO "rtk_pdr" VALUES(3,11,0,0);
INSERT INTO "rtk_pdr" VALUES(3,12,0,0);
INSERT INTO "rtk_pdr" VALUES(3,13,0,0);
INSERT INTO "rtk_pdr" VALUES(3,14,0,0);
INSERT INTO "rtk_pdr" VALUES(3,15,0,0);
INSERT INTO "rtk_pdr" VALUES(3,16,0,0);
INSERT INTO "rtk_pdr" VALUES(3,17,0,0);
INSERT INTO "rtk_pdr" VALUES(3,18,0,0);
INSERT INTO "rtk_pdr" VALUES(3,19,0,0);
INSERT INTO "rtk_pdr" VALUES(3,20,0,0);
INSERT INTO "rtk_pdr" VALUES(3,21,0,0);
INSERT INTO "rtk_pdr" VALUES(3,22,0,0);
INSERT INTO "rtk_pdr" VALUES(3,23,0,0);
INSERT INTO "rtk_pdr" VALUES(3,24,0,0);
INSERT INTO "rtk_pdr" VALUES(3,25,0,0);
INSERT INTO "rtk_pdr" VALUES(3,26,0,0);
INSERT INTO "rtk_pdr" VALUES(3,27,0,0);
INSERT INTO "rtk_pdr" VALUES(3,28,0,0);
INSERT INTO "rtk_pdr" VALUES(3,29,0,0);
INSERT INTO "rtk_pdr" VALUES(3,30,0,0);
INSERT INTO "rtk_pdr" VALUES(3,31,0,0);
INSERT INTO "rtk_pdr" VALUES(3,32,0,0);
INSERT INTO "rtk_pdr" VALUES(3,33,0,0);
INSERT INTO "rtk_pdr" VALUES(3,34,0,0);
INSERT INTO "rtk_pdr" VALUES(3,35,0,0);
INSERT INTO "rtk_pdr" VALUES(3,36,0,0);
INSERT INTO "rtk_pdr" VALUES(3,37,0,0);
INSERT INTO "rtk_pdr" VALUES(3,38,0,0);
INSERT INTO "rtk_pdr" VALUES(4,0,0,0);
INSERT INTO "rtk_pdr" VALUES(4,1,0,0);
INSERT INTO "rtk_pdr" VALUES(4,2,0,0);
INSERT INTO "rtk_pdr" VALUES(4,3,0,0);
INSERT INTO "rtk_pdr" VALUES(4,4,0,0);
INSERT INTO "rtk_pdr" VALUES(4,5,0,0);
INSERT INTO "rtk_pdr" VALUES(4,6,0,0);
INSERT INTO "rtk_pdr" VALUES(4,7,0,0);
INSERT INTO "rtk_pdr" VALUES(4,8,0,0);
INSERT INTO "rtk_pdr" VALUES(4,9,0,0);
INSERT INTO "rtk_pdr" VALUES(4,10,0,0);
INSERT INTO "rtk_pdr" VALUES(4,11,0,0);
INSERT INTO "rtk_pdr" VALUES(4,12,0,0);
INSERT INTO "rtk_pdr" VALUES(4,13,0,0);
INSERT INTO "rtk_pdr" VALUES(4,14,0,0);
INSERT INTO "rtk_pdr" VALUES(4,15,0,0);
INSERT INTO "rtk_pdr" VALUES(4,16,0,0);
INSERT INTO "rtk_pdr" VALUES(4,17,0,0);
INSERT INTO "rtk_pdr" VALUES(4,18,0,0);
INSERT INTO "rtk_pdr" VALUES(4,19,0,0);
INSERT INTO "rtk_pdr" VALUES(4,20,0,0);
INSERT INTO "rtk_pdr" VALUES(4,21,0,0);
INSERT INTO "rtk_pdr" VALUES(4,22,0,0);
INSERT INTO "rtk_pdr" VALUES(4,23,0,0);
INSERT INTO "rtk_pdr" VALUES(4,24,0,0);
INSERT INTO "rtk_pdr" VALUES(4,25,0,0);
INSERT INTO "rtk_pdr" VALUES(4,26,0,0);
INSERT INTO "rtk_pdr" VALUES(4,27,0,0);
INSERT INTO "rtk_pdr" VALUES(4,28,0,0);
INSERT INTO "rtk_pdr" VALUES(4,29,0,0);
INSERT INTO "rtk_pdr" VALUES(4,30,0,0);
INSERT INTO "rtk_pdr" VALUES(4,31,0,0);
INSERT INTO "rtk_pdr" VALUES(4,32,0,0);
INSERT INTO "rtk_pdr" VALUES(4,33,0,0);
INSERT INTO "rtk_pdr" VALUES(4,34,0,0);
INSERT INTO "rtk_pdr" VALUES(4,35,0,0);
INSERT INTO "rtk_pdr" VALUES(4,36,0,0);
INSERT INTO "rtk_pdr" VALUES(4,37,0,0);
INSERT INTO "rtk_pdr" VALUES(4,38,0,0);

DROP TABLE IF EXISTS "rtk_cdr";
CREATE TABLE "rtk_cdr" (
    "fld_software_id" INTEGER NOT NULL DEFAULT (0),                 -- Software module ID.
    "fld_question_id" INTEGER NOT NULL DEFAULT (0),                 -- Question ID.
    "fld_y" TINYINT DEFAULT (0),                                    -- Value of Y/N question.
    "fld_value" INTEGER DEFAULT (0),                                -- Value of quantity question.
    FOREIGN KEY("fld_software_id") REFERENCES "rtk_software"("fld_software_id") ON DELETE CASCADE
);
INSERT INTO "rtk_cdr" VALUES(0,0,0,0);
INSERT INTO "rtk_cdr" VALUES(0,1,0,0);
INSERT INTO "rtk_cdr" VALUES(0,2,0,0);
INSERT INTO "rtk_cdr" VALUES(0,3,0,0);
INSERT INTO "rtk_cdr" VALUES(0,4,0,0);
INSERT INTO "rtk_cdr" VALUES(0,5,0,0);
INSERT INTO "rtk_cdr" VALUES(0,6,0,0);
INSERT INTO "rtk_cdr" VALUES(0,7,0,0);
INSERT INTO "rtk_cdr" VALUES(0,8,0,0);
INSERT INTO "rtk_cdr" VALUES(0,9,0,0);
INSERT INTO "rtk_cdr" VALUES(0,10,0,0);
INSERT INTO "rtk_cdr" VALUES(0,11,0,0);
INSERT INTO "rtk_cdr" VALUES(0,12,0,0);
INSERT INTO "rtk_cdr" VALUES(0,13,0,0);
INSERT INTO "rtk_cdr" VALUES(0,14,0,0);
INSERT INTO "rtk_cdr" VALUES(0,15,0,0);
INSERT INTO "rtk_cdr" VALUES(0,16,0,0);
INSERT INTO "rtk_cdr" VALUES(0,17,0,0);
INSERT INTO "rtk_cdr" VALUES(0,18,0,0);
INSERT INTO "rtk_cdr" VALUES(0,19,0,0);
INSERT INTO "rtk_cdr" VALUES(0,20,0,0);
INSERT INTO "rtk_cdr" VALUES(0,21,0,0);
INSERT INTO "rtk_cdr" VALUES(0,22,0,0);
INSERT INTO "rtk_cdr" VALUES(0,23,0,0);
INSERT INTO "rtk_cdr" VALUES(0,24,0,0);
INSERT INTO "rtk_cdr" VALUES(0,25,0,0);
INSERT INTO "rtk_cdr" VALUES(0,26,0,0);
INSERT INTO "rtk_cdr" VALUES(0,27,0,0);
INSERT INTO "rtk_cdr" VALUES(0,28,0,0);
INSERT INTO "rtk_cdr" VALUES(0,29,0,0);
INSERT INTO "rtk_cdr" VALUES(0,30,0,0);
INSERT INTO "rtk_cdr" VALUES(0,31,0,0);
INSERT INTO "rtk_cdr" VALUES(0,32,0,0);
INSERT INTO "rtk_cdr" VALUES(0,33,0,0);
INSERT INTO "rtk_cdr" VALUES(0,34,0,0);
INSERT INTO "rtk_cdr" VALUES(0,35,0,0);
INSERT INTO "rtk_cdr" VALUES(0,36,0,0);
INSERT INTO "rtk_cdr" VALUES(0,37,0,0);
INSERT INTO "rtk_cdr" VALUES(0,38,0,0);
INSERT INTO "rtk_cdr" VALUES(0,39,0,0);
INSERT INTO "rtk_cdr" VALUES(0,40,0,0);
INSERT INTO "rtk_cdr" VALUES(0,41,0,0);
INSERT INTO "rtk_cdr" VALUES(0,42,0,0);
INSERT INTO "rtk_cdr" VALUES(0,43,0,0);
INSERT INTO "rtk_cdr" VALUES(0,44,0,0);
INSERT INTO "rtk_cdr" VALUES(0,45,0,0);
INSERT INTO "rtk_cdr" VALUES(0,46,0,0);
INSERT INTO "rtk_cdr" VALUES(0,47,0,0);
INSERT INTO "rtk_cdr" VALUES(0,48,0,0);
INSERT INTO "rtk_cdr" VALUES(0,49,0,0);
INSERT INTO "rtk_cdr" VALUES(0,50,0,0);
INSERT INTO "rtk_cdr" VALUES(0,51,0,0);
INSERT INTO "rtk_cdr" VALUES(0,52,0,0);
INSERT INTO "rtk_cdr" VALUES(0,53,0,0);
INSERT INTO "rtk_cdr" VALUES(0,54,0,0);
INSERT INTO "rtk_cdr" VALUES(0,55,0,0);
INSERT INTO "rtk_cdr" VALUES(0,56,0,0);
INSERT INTO "rtk_cdr" VALUES(0,57,0,0);
INSERT INTO "rtk_cdr" VALUES(0,58,0,0);
INSERT INTO "rtk_cdr" VALUES(0,59,0,0);
INSERT INTO "rtk_cdr" VALUES(0,60,0,0);
INSERT INTO "rtk_cdr" VALUES(0,61,0,0);
INSERT INTO "rtk_cdr" VALUES(0,62,0,0);
INSERT INTO "rtk_cdr" VALUES(0,63,0,0);
INSERT INTO "rtk_cdr" VALUES(0,64,0,0);
INSERT INTO "rtk_cdr" VALUES(0,65,0,0);
INSERT INTO "rtk_cdr" VALUES(0,66,0,0);
INSERT INTO "rtk_cdr" VALUES(0,67,0,0);
INSERT INTO "rtk_cdr" VALUES(0,68,0,0);
INSERT INTO "rtk_cdr" VALUES(0,69,0,0);
INSERT INTO "rtk_cdr" VALUES(0,70,0,0);
INSERT INTO "rtk_cdr" VALUES(0,71,0,0);
INSERT INTO "rtk_cdr" VALUES(1,0,0,0);
INSERT INTO "rtk_cdr" VALUES(1,1,0,0);
INSERT INTO "rtk_cdr" VALUES(1,2,0,0);
INSERT INTO "rtk_cdr" VALUES(1,3,0,0);
INSERT INTO "rtk_cdr" VALUES(1,4,0,0);
INSERT INTO "rtk_cdr" VALUES(1,5,0,0);
INSERT INTO "rtk_cdr" VALUES(1,6,0,0);
INSERT INTO "rtk_cdr" VALUES(1,7,0,0);
INSERT INTO "rtk_cdr" VALUES(1,8,0,0);
INSERT INTO "rtk_cdr" VALUES(1,9,0,0);
INSERT INTO "rtk_cdr" VALUES(1,10,0,0);
INSERT INTO "rtk_cdr" VALUES(1,11,0,0);
INSERT INTO "rtk_cdr" VALUES(1,12,0,0);
INSERT INTO "rtk_cdr" VALUES(1,13,0,0);
INSERT INTO "rtk_cdr" VALUES(1,14,0,0);
INSERT INTO "rtk_cdr" VALUES(1,15,0,0);
INSERT INTO "rtk_cdr" VALUES(1,16,0,0);
INSERT INTO "rtk_cdr" VALUES(1,17,0,0);
INSERT INTO "rtk_cdr" VALUES(1,18,0,0);
INSERT INTO "rtk_cdr" VALUES(1,19,0,0);
INSERT INTO "rtk_cdr" VALUES(1,20,0,0);
INSERT INTO "rtk_cdr" VALUES(1,21,0,0);
INSERT INTO "rtk_cdr" VALUES(1,22,0,0);
INSERT INTO "rtk_cdr" VALUES(1,23,0,0);
INSERT INTO "rtk_cdr" VALUES(1,24,0,0);
INSERT INTO "rtk_cdr" VALUES(1,25,0,0);
INSERT INTO "rtk_cdr" VALUES(1,26,0,0);
INSERT INTO "rtk_cdr" VALUES(1,27,0,0);
INSERT INTO "rtk_cdr" VALUES(1,28,0,0);
INSERT INTO "rtk_cdr" VALUES(1,29,0,0);
INSERT INTO "rtk_cdr" VALUES(1,30,0,0);
INSERT INTO "rtk_cdr" VALUES(1,31,0,0);
INSERT INTO "rtk_cdr" VALUES(1,32,0,0);
INSERT INTO "rtk_cdr" VALUES(1,33,0,0);
INSERT INTO "rtk_cdr" VALUES(1,34,0,0);
INSERT INTO "rtk_cdr" VALUES(1,35,0,0);
INSERT INTO "rtk_cdr" VALUES(1,36,0,0);
INSERT INTO "rtk_cdr" VALUES(1,37,0,0);
INSERT INTO "rtk_cdr" VALUES(1,38,0,0);
INSERT INTO "rtk_cdr" VALUES(1,39,0,0);
INSERT INTO "rtk_cdr" VALUES(1,40,0,0);
INSERT INTO "rtk_cdr" VALUES(1,41,0,0);
INSERT INTO "rtk_cdr" VALUES(1,42,0,0);
INSERT INTO "rtk_cdr" VALUES(1,43,0,0);
INSERT INTO "rtk_cdr" VALUES(1,44,0,0);
INSERT INTO "rtk_cdr" VALUES(1,45,0,0);
INSERT INTO "rtk_cdr" VALUES(1,46,0,0);
INSERT INTO "rtk_cdr" VALUES(1,47,0,0);
INSERT INTO "rtk_cdr" VALUES(1,48,0,0);
INSERT INTO "rtk_cdr" VALUES(1,49,0,0);
INSERT INTO "rtk_cdr" VALUES(1,50,0,0);
INSERT INTO "rtk_cdr" VALUES(1,51,0,0);
INSERT INTO "rtk_cdr" VALUES(1,52,0,0);
INSERT INTO "rtk_cdr" VALUES(1,53,0,0);
INSERT INTO "rtk_cdr" VALUES(1,54,0,0);
INSERT INTO "rtk_cdr" VALUES(1,55,0,0);
INSERT INTO "rtk_cdr" VALUES(1,56,0,0);
INSERT INTO "rtk_cdr" VALUES(1,57,0,0);
INSERT INTO "rtk_cdr" VALUES(1,58,0,0);
INSERT INTO "rtk_cdr" VALUES(1,59,0,0);
INSERT INTO "rtk_cdr" VALUES(1,60,0,0);
INSERT INTO "rtk_cdr" VALUES(1,61,0,0);
INSERT INTO "rtk_cdr" VALUES(1,62,0,0);
INSERT INTO "rtk_cdr" VALUES(1,63,0,0);
INSERT INTO "rtk_cdr" VALUES(1,64,0,0);
INSERT INTO "rtk_cdr" VALUES(1,65,0,0);
INSERT INTO "rtk_cdr" VALUES(1,66,0,0);
INSERT INTO "rtk_cdr" VALUES(1,67,0,0);
INSERT INTO "rtk_cdr" VALUES(1,68,0,0);
INSERT INTO "rtk_cdr" VALUES(1,69,0,0);
INSERT INTO "rtk_cdr" VALUES(1,70,0,0);
INSERT INTO "rtk_cdr" VALUES(1,71,0,0);
INSERT INTO "rtk_cdr" VALUES(2,0,0,0);
INSERT INTO "rtk_cdr" VALUES(2,1,0,0);
INSERT INTO "rtk_cdr" VALUES(2,2,0,0);
INSERT INTO "rtk_cdr" VALUES(2,3,0,0);
INSERT INTO "rtk_cdr" VALUES(2,4,0,0);
INSERT INTO "rtk_cdr" VALUES(2,5,0,0);
INSERT INTO "rtk_cdr" VALUES(2,6,0,0);
INSERT INTO "rtk_cdr" VALUES(2,7,0,0);
INSERT INTO "rtk_cdr" VALUES(2,8,0,0);
INSERT INTO "rtk_cdr" VALUES(2,9,0,0);
INSERT INTO "rtk_cdr" VALUES(2,10,0,0);
INSERT INTO "rtk_cdr" VALUES(2,11,0,0);
INSERT INTO "rtk_cdr" VALUES(2,12,0,0);
INSERT INTO "rtk_cdr" VALUES(2,13,0,0);
INSERT INTO "rtk_cdr" VALUES(2,14,0,0);
INSERT INTO "rtk_cdr" VALUES(2,15,0,0);
INSERT INTO "rtk_cdr" VALUES(2,16,0,0);
INSERT INTO "rtk_cdr" VALUES(2,17,0,0);
INSERT INTO "rtk_cdr" VALUES(2,18,0,0);
INSERT INTO "rtk_cdr" VALUES(2,19,0,0);
INSERT INTO "rtk_cdr" VALUES(2,20,0,0);
INSERT INTO "rtk_cdr" VALUES(2,21,0,0);
INSERT INTO "rtk_cdr" VALUES(2,22,0,0);
INSERT INTO "rtk_cdr" VALUES(2,23,0,0);
INSERT INTO "rtk_cdr" VALUES(2,24,0,0);
INSERT INTO "rtk_cdr" VALUES(2,25,0,0);
INSERT INTO "rtk_cdr" VALUES(2,26,0,0);
INSERT INTO "rtk_cdr" VALUES(2,27,0,0);
INSERT INTO "rtk_cdr" VALUES(2,28,0,0);
INSERT INTO "rtk_cdr" VALUES(2,29,0,0);
INSERT INTO "rtk_cdr" VALUES(2,30,0,0);
INSERT INTO "rtk_cdr" VALUES(2,31,0,0);
INSERT INTO "rtk_cdr" VALUES(2,32,0,0);
INSERT INTO "rtk_cdr" VALUES(2,33,0,0);
INSERT INTO "rtk_cdr" VALUES(2,34,0,0);
INSERT INTO "rtk_cdr" VALUES(2,35,0,0);
INSERT INTO "rtk_cdr" VALUES(2,36,0,0);
INSERT INTO "rtk_cdr" VALUES(2,37,0,0);
INSERT INTO "rtk_cdr" VALUES(2,38,0,0);
INSERT INTO "rtk_cdr" VALUES(2,39,0,0);
INSERT INTO "rtk_cdr" VALUES(2,40,0,0);
INSERT INTO "rtk_cdr" VALUES(2,41,0,0);
INSERT INTO "rtk_cdr" VALUES(2,42,0,0);
INSERT INTO "rtk_cdr" VALUES(2,43,0,0);
INSERT INTO "rtk_cdr" VALUES(2,44,0,0);
INSERT INTO "rtk_cdr" VALUES(2,45,0,0);
INSERT INTO "rtk_cdr" VALUES(2,46,0,0);
INSERT INTO "rtk_cdr" VALUES(2,47,0,0);
INSERT INTO "rtk_cdr" VALUES(2,48,0,0);
INSERT INTO "rtk_cdr" VALUES(2,49,0,0);
INSERT INTO "rtk_cdr" VALUES(2,50,0,0);
INSERT INTO "rtk_cdr" VALUES(2,51,0,0);
INSERT INTO "rtk_cdr" VALUES(2,52,0,0);
INSERT INTO "rtk_cdr" VALUES(2,53,0,0);
INSERT INTO "rtk_cdr" VALUES(2,54,0,0);
INSERT INTO "rtk_cdr" VALUES(2,55,0,0);
INSERT INTO "rtk_cdr" VALUES(2,56,0,0);
INSERT INTO "rtk_cdr" VALUES(2,57,0,0);
INSERT INTO "rtk_cdr" VALUES(2,58,0,0);
INSERT INTO "rtk_cdr" VALUES(2,59,0,0);
INSERT INTO "rtk_cdr" VALUES(2,60,0,0);
INSERT INTO "rtk_cdr" VALUES(2,61,0,0);
INSERT INTO "rtk_cdr" VALUES(2,62,0,0);
INSERT INTO "rtk_cdr" VALUES(2,63,0,0);
INSERT INTO "rtk_cdr" VALUES(2,64,0,0);
INSERT INTO "rtk_cdr" VALUES(2,65,0,0);
INSERT INTO "rtk_cdr" VALUES(2,66,0,0);
INSERT INTO "rtk_cdr" VALUES(2,67,0,0);
INSERT INTO "rtk_cdr" VALUES(2,68,0,0);
INSERT INTO "rtk_cdr" VALUES(2,69,0,0);
INSERT INTO "rtk_cdr" VALUES(2,70,0,0);
INSERT INTO "rtk_cdr" VALUES(2,71,0,0);
INSERT INTO "rtk_cdr" VALUES(3,0,0,0);
INSERT INTO "rtk_cdr" VALUES(3,1,0,0);
INSERT INTO "rtk_cdr" VALUES(3,2,0,0);
INSERT INTO "rtk_cdr" VALUES(3,3,0,0);
INSERT INTO "rtk_cdr" VALUES(3,4,0,0);
INSERT INTO "rtk_cdr" VALUES(3,5,0,0);
INSERT INTO "rtk_cdr" VALUES(3,6,0,0);
INSERT INTO "rtk_cdr" VALUES(3,7,0,0);
INSERT INTO "rtk_cdr" VALUES(3,8,0,0);
INSERT INTO "rtk_cdr" VALUES(3,9,0,0);
INSERT INTO "rtk_cdr" VALUES(3,10,0,0);
INSERT INTO "rtk_cdr" VALUES(3,11,0,0);
INSERT INTO "rtk_cdr" VALUES(3,12,0,0);
INSERT INTO "rtk_cdr" VALUES(3,13,0,0);
INSERT INTO "rtk_cdr" VALUES(3,14,0,0);
INSERT INTO "rtk_cdr" VALUES(3,15,0,0);
INSERT INTO "rtk_cdr" VALUES(3,16,0,0);
INSERT INTO "rtk_cdr" VALUES(3,17,0,0);
INSERT INTO "rtk_cdr" VALUES(3,18,0,0);
INSERT INTO "rtk_cdr" VALUES(3,19,0,0);
INSERT INTO "rtk_cdr" VALUES(3,20,0,0);
INSERT INTO "rtk_cdr" VALUES(3,21,0,0);
INSERT INTO "rtk_cdr" VALUES(3,22,0,0);
INSERT INTO "rtk_cdr" VALUES(3,23,0,0);
INSERT INTO "rtk_cdr" VALUES(3,24,0,0);
INSERT INTO "rtk_cdr" VALUES(3,25,0,0);
INSERT INTO "rtk_cdr" VALUES(3,26,0,0);
INSERT INTO "rtk_cdr" VALUES(3,27,0,0);
INSERT INTO "rtk_cdr" VALUES(3,28,0,0);
INSERT INTO "rtk_cdr" VALUES(3,29,0,0);
INSERT INTO "rtk_cdr" VALUES(3,30,0,0);
INSERT INTO "rtk_cdr" VALUES(3,31,0,0);
INSERT INTO "rtk_cdr" VALUES(3,32,0,0);
INSERT INTO "rtk_cdr" VALUES(3,33,0,0);
INSERT INTO "rtk_cdr" VALUES(3,34,0,0);
INSERT INTO "rtk_cdr" VALUES(3,35,0,0);
INSERT INTO "rtk_cdr" VALUES(3,36,0,0);
INSERT INTO "rtk_cdr" VALUES(3,37,0,0);
INSERT INTO "rtk_cdr" VALUES(3,38,0,0);
INSERT INTO "rtk_cdr" VALUES(3,39,0,0);
INSERT INTO "rtk_cdr" VALUES(3,40,0,0);
INSERT INTO "rtk_cdr" VALUES(3,41,0,0);
INSERT INTO "rtk_cdr" VALUES(3,42,0,0);
INSERT INTO "rtk_cdr" VALUES(3,43,0,0);
INSERT INTO "rtk_cdr" VALUES(3,44,0,0);
INSERT INTO "rtk_cdr" VALUES(3,45,0,0);
INSERT INTO "rtk_cdr" VALUES(3,46,0,0);
INSERT INTO "rtk_cdr" VALUES(3,47,0,0);
INSERT INTO "rtk_cdr" VALUES(3,48,0,0);
INSERT INTO "rtk_cdr" VALUES(3,49,0,0);
INSERT INTO "rtk_cdr" VALUES(3,50,0,0);
INSERT INTO "rtk_cdr" VALUES(3,51,0,0);
INSERT INTO "rtk_cdr" VALUES(3,52,0,0);
INSERT INTO "rtk_cdr" VALUES(3,53,0,0);
INSERT INTO "rtk_cdr" VALUES(3,54,0,0);
INSERT INTO "rtk_cdr" VALUES(3,55,0,0);
INSERT INTO "rtk_cdr" VALUES(3,56,0,0);
INSERT INTO "rtk_cdr" VALUES(3,57,0,0);
INSERT INTO "rtk_cdr" VALUES(3,58,0,0);
INSERT INTO "rtk_cdr" VALUES(3,59,0,0);
INSERT INTO "rtk_cdr" VALUES(3,60,0,0);
INSERT INTO "rtk_cdr" VALUES(3,61,0,0);
INSERT INTO "rtk_cdr" VALUES(3,62,0,0);
INSERT INTO "rtk_cdr" VALUES(3,63,0,0);
INSERT INTO "rtk_cdr" VALUES(3,64,0,0);
INSERT INTO "rtk_cdr" VALUES(3,65,0,0);
INSERT INTO "rtk_cdr" VALUES(3,66,0,0);
INSERT INTO "rtk_cdr" VALUES(3,67,0,0);
INSERT INTO "rtk_cdr" VALUES(3,68,0,0);
INSERT INTO "rtk_cdr" VALUES(3,69,0,0);
INSERT INTO "rtk_cdr" VALUES(3,70,0,0);
INSERT INTO "rtk_cdr" VALUES(3,71,0,0);
INSERT INTO "rtk_cdr" VALUES(4,0,0,0);
INSERT INTO "rtk_cdr" VALUES(4,1,0,0);
INSERT INTO "rtk_cdr" VALUES(4,2,0,0);
INSERT INTO "rtk_cdr" VALUES(4,3,0,0);
INSERT INTO "rtk_cdr" VALUES(4,4,0,0);
INSERT INTO "rtk_cdr" VALUES(4,5,0,0);
INSERT INTO "rtk_cdr" VALUES(4,6,0,0);
INSERT INTO "rtk_cdr" VALUES(4,7,0,0);
INSERT INTO "rtk_cdr" VALUES(4,8,0,0);
INSERT INTO "rtk_cdr" VALUES(4,9,0,0);
INSERT INTO "rtk_cdr" VALUES(4,10,0,0);
INSERT INTO "rtk_cdr" VALUES(4,11,0,0);
INSERT INTO "rtk_cdr" VALUES(4,12,0,0);
INSERT INTO "rtk_cdr" VALUES(4,13,0,0);
INSERT INTO "rtk_cdr" VALUES(4,14,0,0);
INSERT INTO "rtk_cdr" VALUES(4,15,0,0);
INSERT INTO "rtk_cdr" VALUES(4,16,0,0);
INSERT INTO "rtk_cdr" VALUES(4,17,0,0);
INSERT INTO "rtk_cdr" VALUES(4,18,0,0);
INSERT INTO "rtk_cdr" VALUES(4,19,0,0);
INSERT INTO "rtk_cdr" VALUES(4,20,0,0);
INSERT INTO "rtk_cdr" VALUES(4,21,0,0);
INSERT INTO "rtk_cdr" VALUES(4,22,0,0);
INSERT INTO "rtk_cdr" VALUES(4,23,0,0);
INSERT INTO "rtk_cdr" VALUES(4,24,0,0);
INSERT INTO "rtk_cdr" VALUES(4,25,0,0);
INSERT INTO "rtk_cdr" VALUES(4,26,0,0);
INSERT INTO "rtk_cdr" VALUES(4,27,0,0);
INSERT INTO "rtk_cdr" VALUES(4,28,0,0);
INSERT INTO "rtk_cdr" VALUES(4,29,0,0);
INSERT INTO "rtk_cdr" VALUES(4,30,0,0);
INSERT INTO "rtk_cdr" VALUES(4,31,0,0);
INSERT INTO "rtk_cdr" VALUES(4,32,0,0);
INSERT INTO "rtk_cdr" VALUES(4,33,0,0);
INSERT INTO "rtk_cdr" VALUES(4,34,0,0);
INSERT INTO "rtk_cdr" VALUES(4,35,0,0);
INSERT INTO "rtk_cdr" VALUES(4,36,0,0);
INSERT INTO "rtk_cdr" VALUES(4,37,0,0);
INSERT INTO "rtk_cdr" VALUES(4,38,0,0);
INSERT INTO "rtk_cdr" VALUES(4,39,0,0);
INSERT INTO "rtk_cdr" VALUES(4,40,0,0);
INSERT INTO "rtk_cdr" VALUES(4,41,0,0);
INSERT INTO "rtk_cdr" VALUES(4,42,0,0);
INSERT INTO "rtk_cdr" VALUES(4,43,0,0);
INSERT INTO "rtk_cdr" VALUES(4,44,0,0);
INSERT INTO "rtk_cdr" VALUES(4,45,0,0);
INSERT INTO "rtk_cdr" VALUES(4,46,0,0);
INSERT INTO "rtk_cdr" VALUES(4,47,0,0);
INSERT INTO "rtk_cdr" VALUES(4,48,0,0);
INSERT INTO "rtk_cdr" VALUES(4,49,0,0);
INSERT INTO "rtk_cdr" VALUES(4,50,0,0);
INSERT INTO "rtk_cdr" VALUES(4,51,0,0);
INSERT INTO "rtk_cdr" VALUES(4,52,0,0);
INSERT INTO "rtk_cdr" VALUES(4,53,0,0);
INSERT INTO "rtk_cdr" VALUES(4,54,0,0);
INSERT INTO "rtk_cdr" VALUES(4,55,0,0);
INSERT INTO "rtk_cdr" VALUES(4,56,0,0);
INSERT INTO "rtk_cdr" VALUES(4,57,0,0);
INSERT INTO "rtk_cdr" VALUES(4,58,0,0);
INSERT INTO "rtk_cdr" VALUES(4,59,0,0);
INSERT INTO "rtk_cdr" VALUES(4,60,0,0);
INSERT INTO "rtk_cdr" VALUES(4,61,0,0);
INSERT INTO "rtk_cdr" VALUES(4,62,0,0);
INSERT INTO "rtk_cdr" VALUES(4,63,0,0);
INSERT INTO "rtk_cdr" VALUES(4,64,0,0);
INSERT INTO "rtk_cdr" VALUES(4,65,0,0);
INSERT INTO "rtk_cdr" VALUES(4,66,0,0);
INSERT INTO "rtk_cdr" VALUES(4,67,0,0);
INSERT INTO "rtk_cdr" VALUES(4,68,0,0);
INSERT INTO "rtk_cdr" VALUES(4,69,0,0);
INSERT INTO "rtk_cdr" VALUES(4,70,0,0);
INSERT INTO "rtk_cdr" VALUES(4,71,0,0);

DROP TABLE IF EXISTS "rtk_trr";
CREATE TABLE "rtk_trr" (
    "fld_software_id" INTEGER NOT NULL DEFAULT (0),                 -- Software module ID.
    "fld_question_id" INTEGER NOT NULL DEFAULT (0),                 -- Question ID.
    "fld_y" TINYINT DEFAULT (0),                                    -- Value of Y/N question.
    "fld_value" INTEGER DEFAULT (0),                                -- Value of quantity question.
    FOREIGN KEY("fld_software_id") REFERENCES "rtk_software"("fld_software_id") ON DELETE CASCADE
);
INSERT INTO "rtk_trr" VALUES(0,0,0,0);
INSERT INTO "rtk_trr" VALUES(0,1,0,0);
INSERT INTO "rtk_trr" VALUES(0,2,0,0);
INSERT INTO "rtk_trr" VALUES(0,3,0,0);
INSERT INTO "rtk_trr" VALUES(0,4,0,0);
INSERT INTO "rtk_trr" VALUES(0,5,0,0);
INSERT INTO "rtk_trr" VALUES(0,6,0,0);
INSERT INTO "rtk_trr" VALUES(0,7,0,0);
INSERT INTO "rtk_trr" VALUES(0,8,0,0);
INSERT INTO "rtk_trr" VALUES(0,9,0,0);
INSERT INTO "rtk_trr" VALUES(0,10,0,0);
INSERT INTO "rtk_trr" VALUES(0,11,0,0);
INSERT INTO "rtk_trr" VALUES(0,12,0,0);
INSERT INTO "rtk_trr" VALUES(0,13,0,0);
INSERT INTO "rtk_trr" VALUES(0,14,0,0);
INSERT INTO "rtk_trr" VALUES(0,15,0,0);
INSERT INTO "rtk_trr" VALUES(0,16,0,0);
INSERT INTO "rtk_trr" VALUES(0,17,0,0);
INSERT INTO "rtk_trr" VALUES(0,18,0,0);
INSERT INTO "rtk_trr" VALUES(0,19,0,0);
INSERT INTO "rtk_trr" VALUES(0,20,0,0);
INSERT INTO "rtk_trr" VALUES(0,21,0,0);
INSERT INTO "rtk_trr" VALUES(0,22,0,0);
INSERT INTO "rtk_trr" VALUES(0,23,0,0);
INSERT INTO "rtk_trr" VALUES(1,0,0,0);
INSERT INTO "rtk_trr" VALUES(1,1,0,0);
INSERT INTO "rtk_trr" VALUES(1,2,0,0);
INSERT INTO "rtk_trr" VALUES(1,3,0,0);
INSERT INTO "rtk_trr" VALUES(1,4,0,0);
INSERT INTO "rtk_trr" VALUES(1,5,0,0);
INSERT INTO "rtk_trr" VALUES(1,6,0,0);
INSERT INTO "rtk_trr" VALUES(1,7,0,0);
INSERT INTO "rtk_trr" VALUES(1,8,0,0);
INSERT INTO "rtk_trr" VALUES(1,9,0,0);
INSERT INTO "rtk_trr" VALUES(1,10,0,0);
INSERT INTO "rtk_trr" VALUES(1,11,0,0);
INSERT INTO "rtk_trr" VALUES(1,12,0,0);
INSERT INTO "rtk_trr" VALUES(1,13,0,0);
INSERT INTO "rtk_trr" VALUES(1,14,0,0);
INSERT INTO "rtk_trr" VALUES(1,15,0,0);
INSERT INTO "rtk_trr" VALUES(1,16,0,0);
INSERT INTO "rtk_trr" VALUES(1,17,0,0);
INSERT INTO "rtk_trr" VALUES(1,18,0,0);
INSERT INTO "rtk_trr" VALUES(1,19,0,0);
INSERT INTO "rtk_trr" VALUES(1,20,0,0);
INSERT INTO "rtk_trr" VALUES(1,21,0,0);
INSERT INTO "rtk_trr" VALUES(1,22,0,0);
INSERT INTO "rtk_trr" VALUES(1,23,0,0);
INSERT INTO "rtk_trr" VALUES(2,0,0,0);
INSERT INTO "rtk_trr" VALUES(2,1,0,0);
INSERT INTO "rtk_trr" VALUES(2,2,0,0);
INSERT INTO "rtk_trr" VALUES(2,3,0,0);
INSERT INTO "rtk_trr" VALUES(2,4,0,0);
INSERT INTO "rtk_trr" VALUES(2,5,0,0);
INSERT INTO "rtk_trr" VALUES(2,6,0,0);
INSERT INTO "rtk_trr" VALUES(2,7,0,0);
INSERT INTO "rtk_trr" VALUES(2,8,0,0);
INSERT INTO "rtk_trr" VALUES(2,9,0,0);
INSERT INTO "rtk_trr" VALUES(2,10,0,0);
INSERT INTO "rtk_trr" VALUES(2,11,0,0);
INSERT INTO "rtk_trr" VALUES(2,12,0,0);
INSERT INTO "rtk_trr" VALUES(2,13,0,0);
INSERT INTO "rtk_trr" VALUES(2,14,0,0);
INSERT INTO "rtk_trr" VALUES(2,15,0,0);
INSERT INTO "rtk_trr" VALUES(2,16,0,0);
INSERT INTO "rtk_trr" VALUES(2,17,0,0);
INSERT INTO "rtk_trr" VALUES(2,18,0,0);
INSERT INTO "rtk_trr" VALUES(2,19,0,0);
INSERT INTO "rtk_trr" VALUES(2,20,0,0);
INSERT INTO "rtk_trr" VALUES(2,21,0,0);
INSERT INTO "rtk_trr" VALUES(2,22,0,0);
INSERT INTO "rtk_trr" VALUES(2,23,0,0);
INSERT INTO "rtk_trr" VALUES(3,0,0,0);
INSERT INTO "rtk_trr" VALUES(3,1,0,0);
INSERT INTO "rtk_trr" VALUES(3,2,0,0);
INSERT INTO "rtk_trr" VALUES(3,3,0,0);
INSERT INTO "rtk_trr" VALUES(3,4,0,0);
INSERT INTO "rtk_trr" VALUES(3,5,0,0);
INSERT INTO "rtk_trr" VALUES(3,6,0,0);
INSERT INTO "rtk_trr" VALUES(3,7,0,0);
INSERT INTO "rtk_trr" VALUES(3,8,0,0);
INSERT INTO "rtk_trr" VALUES(3,9,0,0);
INSERT INTO "rtk_trr" VALUES(3,10,0,0);
INSERT INTO "rtk_trr" VALUES(3,11,0,0);
INSERT INTO "rtk_trr" VALUES(3,12,0,0);
INSERT INTO "rtk_trr" VALUES(3,13,0,0);
INSERT INTO "rtk_trr" VALUES(3,14,0,0);
INSERT INTO "rtk_trr" VALUES(3,15,0,0);
INSERT INTO "rtk_trr" VALUES(3,16,0,0);
INSERT INTO "rtk_trr" VALUES(3,17,0,0);
INSERT INTO "rtk_trr" VALUES(3,18,0,0);
INSERT INTO "rtk_trr" VALUES(3,19,0,0);
INSERT INTO "rtk_trr" VALUES(3,20,0,0);
INSERT INTO "rtk_trr" VALUES(3,21,0,0);
INSERT INTO "rtk_trr" VALUES(3,22,0,0);
INSERT INTO "rtk_trr" VALUES(3,23,0,0);
INSERT INTO "rtk_trr" VALUES(4,0,0,0);
INSERT INTO "rtk_trr" VALUES(4,1,0,0);
INSERT INTO "rtk_trr" VALUES(4,2,0,0);
INSERT INTO "rtk_trr" VALUES(4,3,0,0);
INSERT INTO "rtk_trr" VALUES(4,4,0,0);
INSERT INTO "rtk_trr" VALUES(4,5,0,0);
INSERT INTO "rtk_trr" VALUES(4,6,0,0);
INSERT INTO "rtk_trr" VALUES(4,7,0,0);
INSERT INTO "rtk_trr" VALUES(4,8,0,0);
INSERT INTO "rtk_trr" VALUES(4,9,0,0);
INSERT INTO "rtk_trr" VALUES(4,10,0,0);
INSERT INTO "rtk_trr" VALUES(4,11,0,0);
INSERT INTO "rtk_trr" VALUES(4,12,0,0);
INSERT INTO "rtk_trr" VALUES(4,13,0,0);
INSERT INTO "rtk_trr" VALUES(4,14,0,0);
INSERT INTO "rtk_trr" VALUES(4,15,0,0);
INSERT INTO "rtk_trr" VALUES(4,16,0,0);
INSERT INTO "rtk_trr" VALUES(4,17,0,0);
INSERT INTO "rtk_trr" VALUES(4,18,0,0);
INSERT INTO "rtk_trr" VALUES(4,19,0,0);
INSERT INTO "rtk_trr" VALUES(4,20,0,0);
INSERT INTO "rtk_trr" VALUES(4,21,0,0);
INSERT INTO "rtk_trr" VALUES(4,22,0,0);
INSERT INTO "rtk_trr" VALUES(4,23,0,0);

DROP TABLE IF EXISTS "rtk_software_tests";
CREATE TABLE "rtk_software_tests" (
    "fld_software_id" INTEGER NOT NULL DEFAULT (0),
    "fld_technique_id" INTEGER NOT NULL DEFAULT (0),
    "fld_recommended" TINYINT DEFAULT (0),
    "fld_used" TINYINT DEFAULT (0),
    FOREIGN KEY("fld_software_id") REFERENCES "rtk_software"("fld_software_id") ON DELETE CASCADE
);
INSERT INTO "rtk_software_tests" VALUES(0,0,0,0);
INSERT INTO "rtk_software_tests" VALUES(0,1,0,0);
INSERT INTO "rtk_software_tests" VALUES(0,2,0,0);
INSERT INTO "rtk_software_tests" VALUES(0,3,0,0);
INSERT INTO "rtk_software_tests" VALUES(0,4,0,0);
INSERT INTO "rtk_software_tests" VALUES(0,5,0,0);
INSERT INTO "rtk_software_tests" VALUES(0,6,0,0);
INSERT INTO "rtk_software_tests" VALUES(0,7,0,0);
INSERT INTO "rtk_software_tests" VALUES(0,8,0,0);
INSERT INTO "rtk_software_tests" VALUES(0,9,0,0);
INSERT INTO "rtk_software_tests" VALUES(0,10,0,0);
INSERT INTO "rtk_software_tests" VALUES(0,11,0,0);
INSERT INTO "rtk_software_tests" VALUES(0,12,0,0);
INSERT INTO "rtk_software_tests" VALUES(0,13,0,0);
INSERT INTO "rtk_software_tests" VALUES(0,14,0,0);
INSERT INTO "rtk_software_tests" VALUES(0,15,0,0);
INSERT INTO "rtk_software_tests" VALUES(0,16,0,0);
INSERT INTO "rtk_software_tests" VALUES(0,17,0,0);
INSERT INTO "rtk_software_tests" VALUES(0,18,0,0);
INSERT INTO "rtk_software_tests" VALUES(0,19,0,0);
INSERT INTO "rtk_software_tests" VALUES(0,20,0,0);
INSERT INTO "rtk_software_tests" VALUES(1,0,0,0);
INSERT INTO "rtk_software_tests" VALUES(1,1,0,0);
INSERT INTO "rtk_software_tests" VALUES(1,2,0,0);
INSERT INTO "rtk_software_tests" VALUES(1,3,0,0);
INSERT INTO "rtk_software_tests" VALUES(1,4,0,0);
INSERT INTO "rtk_software_tests" VALUES(1,5,0,0);
INSERT INTO "rtk_software_tests" VALUES(1,6,0,0);
INSERT INTO "rtk_software_tests" VALUES(1,7,0,0);
INSERT INTO "rtk_software_tests" VALUES(1,8,0,0);
INSERT INTO "rtk_software_tests" VALUES(1,9,0,0);
INSERT INTO "rtk_software_tests" VALUES(1,10,0,0);
INSERT INTO "rtk_software_tests" VALUES(1,11,0,0);
INSERT INTO "rtk_software_tests" VALUES(1,12,0,0);
INSERT INTO "rtk_software_tests" VALUES(1,13,0,0);
INSERT INTO "rtk_software_tests" VALUES(1,14,0,0);
INSERT INTO "rtk_software_tests" VALUES(1,15,0,0);
INSERT INTO "rtk_software_tests" VALUES(1,16,0,0);
INSERT INTO "rtk_software_tests" VALUES(1,17,0,0);
INSERT INTO "rtk_software_tests" VALUES(1,18,0,0);
INSERT INTO "rtk_software_tests" VALUES(1,19,0,0);
INSERT INTO "rtk_software_tests" VALUES(1,20,0,0);
INSERT INTO "rtk_software_tests" VALUES(2,0,0,0);
INSERT INTO "rtk_software_tests" VALUES(2,1,0,0);
INSERT INTO "rtk_software_tests" VALUES(2,2,0,0);
INSERT INTO "rtk_software_tests" VALUES(2,3,0,0);
INSERT INTO "rtk_software_tests" VALUES(2,4,0,0);
INSERT INTO "rtk_software_tests" VALUES(2,5,0,0);
INSERT INTO "rtk_software_tests" VALUES(2,6,0,0);
INSERT INTO "rtk_software_tests" VALUES(2,7,0,0);
INSERT INTO "rtk_software_tests" VALUES(2,8,0,0);
INSERT INTO "rtk_software_tests" VALUES(2,9,0,0);
INSERT INTO "rtk_software_tests" VALUES(2,10,0,0);
INSERT INTO "rtk_software_tests" VALUES(2,11,0,0);
INSERT INTO "rtk_software_tests" VALUES(2,12,0,0);
INSERT INTO "rtk_software_tests" VALUES(2,13,0,0);
INSERT INTO "rtk_software_tests" VALUES(2,14,0,0);
INSERT INTO "rtk_software_tests" VALUES(2,15,0,0);
INSERT INTO "rtk_software_tests" VALUES(2,16,0,0);
INSERT INTO "rtk_software_tests" VALUES(2,17,0,0);
INSERT INTO "rtk_software_tests" VALUES(2,18,0,0);
INSERT INTO "rtk_software_tests" VALUES(2,19,0,0);
INSERT INTO "rtk_software_tests" VALUES(2,20,0,0);
INSERT INTO "rtk_software_tests" VALUES(3,0,0,0);
INSERT INTO "rtk_software_tests" VALUES(3,1,0,0);
INSERT INTO "rtk_software_tests" VALUES(3,2,0,0);
INSERT INTO "rtk_software_tests" VALUES(3,3,0,0);
INSERT INTO "rtk_software_tests" VALUES(3,4,0,0);
INSERT INTO "rtk_software_tests" VALUES(3,5,0,0);
INSERT INTO "rtk_software_tests" VALUES(3,6,0,0);
INSERT INTO "rtk_software_tests" VALUES(3,7,0,0);
INSERT INTO "rtk_software_tests" VALUES(3,8,0,0);
INSERT INTO "rtk_software_tests" VALUES(3,9,0,0);
INSERT INTO "rtk_software_tests" VALUES(3,10,0,0);
INSERT INTO "rtk_software_tests" VALUES(3,11,0,0);
INSERT INTO "rtk_software_tests" VALUES(3,12,0,0);
INSERT INTO "rtk_software_tests" VALUES(3,13,0,0);
INSERT INTO "rtk_software_tests" VALUES(3,14,0,0);
INSERT INTO "rtk_software_tests" VALUES(3,15,0,0);
INSERT INTO "rtk_software_tests" VALUES(3,16,0,0);
INSERT INTO "rtk_software_tests" VALUES(3,17,0,0);
INSERT INTO "rtk_software_tests" VALUES(3,18,0,0);
INSERT INTO "rtk_software_tests" VALUES(3,19,0,0);
INSERT INTO "rtk_software_tests" VALUES(3,20,0,0);
INSERT INTO "rtk_software_tests" VALUES(4,0,0,0);
INSERT INTO "rtk_software_tests" VALUES(4,1,0,0);
INSERT INTO "rtk_software_tests" VALUES(4,2,0,0);
INSERT INTO "rtk_software_tests" VALUES(4,3,0,0);
INSERT INTO "rtk_software_tests" VALUES(4,4,0,0);
INSERT INTO "rtk_software_tests" VALUES(4,5,0,0);
INSERT INTO "rtk_software_tests" VALUES(4,6,0,0);
INSERT INTO "rtk_software_tests" VALUES(4,7,0,0);
INSERT INTO "rtk_software_tests" VALUES(4,8,0,0);
INSERT INTO "rtk_software_tests" VALUES(4,9,0,0);
INSERT INTO "rtk_software_tests" VALUES(4,10,0,0);
INSERT INTO "rtk_software_tests" VALUES(4,11,0,0);
INSERT INTO "rtk_software_tests" VALUES(4,12,0,0);
INSERT INTO "rtk_software_tests" VALUES(4,13,0,0);
INSERT INTO "rtk_software_tests" VALUES(4,14,0,0);
INSERT INTO "rtk_software_tests" VALUES(4,15,0,0);
INSERT INTO "rtk_software_tests" VALUES(4,16,0,0);
INSERT INTO "rtk_software_tests" VALUES(4,17,0,0);
INSERT INTO "rtk_software_tests" VALUES(4,18,0,0);
INSERT INTO "rtk_software_tests" VALUES(4,19,0,0);
INSERT INTO "rtk_software_tests" VALUES(4,20,0,0);

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
INSERT INTO "rtk_validation" VALUES(0,8,'Perform a hazards analysis for the Example System.',16,'',0,0.0,0.0,0.0,0.0,735848,735907,85.0,15.0,25.0,40.0,25.833333,17.361111,0.0,0.0,0.0,0.0,0.0,95.0);
INSERT INTO "rtk_validation" VALUES(0,9,'Perform FEA on Example System',18,'',0,0.0,0.0,0.0,0.0,735825,735872,100.0,40.0,60.0,90.0,61.666667,69.444444,0.0,0.0,0.0,0.0,0.0,95.0);
INSERT INTO "rtk_validation" VALUES(0,10,'Perform accelerated life test on Example System.',11,'',2,0.0,0.0,0.0,0.0,735856,735866,100.0,10.0,18.5,25.0,18.166667,6.25,0.0,0.0,0.0,0.0,0.0,95.0);
INSERT INTO "rtk_validation" VALUES(0,13,'PDR Reliability Assessment',5,'',0,25.0,0.0,0.0,0.0,735824,735936,55.0,80.0,120.0,160.0,120.0,177.777778,0.0,0.0,0.0,0.0,0.0,95.0);

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
    "fld_accepted" TINYINT DEFAULT(0),
    "fld_relevant_1" TINYINT DEFAULT(-1),
    "fld_relevant_2" TINYINT DEFAULT(-1),
    "fld_relevant_3" TINYINT DEFAULT(-1),
    "fld_relevant_4" TINYINT DEFAULT(-1),
    "fld_relevant_5" TINYINT DEFAULT(-1),
    "fld_relevant_6" TINYINT DEFAULT(-1),
    "fld_relevant_7" TINYINT DEFAULT(-1),
    "fld_relevant_8" TINYINT DEFAULT(-1),
    "fld_relevant_9" TINYINT DEFAULT(-1),
    "fld_relevant_10" TINYINT DEFAULT(-1),
    "fld_relevant_11" TINYINT DEFAULT(-1),
    "fld_relevant_12" TINYINT DEFAULT(-1),
    "fld_relevant_13" TINYINT DEFAULT(-1),
    "fld_relevant_14" TINYINT DEFAULT(-1),
    "fld_relevant_15" TINYINT DEFAULT(-1),
    "fld_relevant_16" TINYINT DEFAULT(-1),
    "fld_relevant_17" TINYINT DEFAULT(-1),
    "fld_relevant_18" TINYINT DEFAULT(-1),
    "fld_relevant_19" TINYINT DEFAULT(-1),
    "fld_relevant_20" TINYINT DEFAULT(-1),
    "fld_relevant" TINYINT DEFAULT(-1),
    "fld_chargeable_1" TINYINT DEFAULT(-1),
    "fld_chargeable_2" TINYINT DEFAULT(-1),
    "fld_chargeable_3" TINYINT DEFAULT(-1),
    "fld_chargeable_4" TINYINT DEFAULT(-1),
    "fld_chargeable_5" TINYINT DEFAULT(-1),
    "fld_chargeable_6" TINYINT DEFAULT(-1),
    "fld_chargeable_7" TINYINT DEFAULT(-1),
    "fld_chargeable_8" TINYINT DEFAULT(-1),
    "fld_chargeable_9" TINYINT DEFAULT(-1),
    "fld_chargeable_10" TINYINT DEFAULT(-1),
    "fld_chargeable" TINYINT DEFAULT(-1)
);
INSERT INTO "rtk_incident" VALUES(0,1,2,3,'Short Description','Detailed Description',4,5,'Remarks',6,'Test','Test Case',7.0,'8',9.0,10,11,12,1,719163,1,1,719163,0,1,719164,0,1,719163,3,'Analysis',1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1);
INSERT INTO "rtk_incident" VALUES(0,2,1,2,'New Incident 2','None',3,0,'',1,'None','None',0.0,'0',0.0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,1,'',1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1);
INSERT INTO "rtk_incident" VALUES(0,3,1,1,'New Incident 3','None',1,0,'None',1,'None','None',0.0,'0',0.0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,1,'',1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1);
INSERT INTO "rtk_incident" VALUES(0,4,0,0,'New Incident 4','None',0,0,'None',1,'None','None',0.0,'0',0.0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,'',0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1);
INSERT INTO "rtk_incident" VALUES(0,5,1,3,'Switch SW1 is mis-specified.','Switch SW1 as currently specified has a contact current rating of 0.1 amperes.  This switch may carry up to 0.5 amperes per contact.  The specified switch for SW1 is under rated.',2,0,'',4,'','',0.0,'0',0.0,0,0,0,1,0,1,1,0,0,0,0,0,0,0,1,'',1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1);

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
    PRIMARY KEY ("fld_incident_id", "fld_component_id")
);
INSERT INTO "rtk_incident_detail" VALUES(1,6,95.0,1,0,0,0,0,0,0,0,0.0,0);
INSERT INTO "rtk_incident_detail" VALUES(2,6,95.0,1,0,0,0,0,0,0,0,0.0,0);
INSERT INTO "rtk_incident_detail" VALUES(3,6,95.0,1,0,0,0,0,0,0,0,0.0,0);
INSERT INTO "rtk_incident_detail" VALUES(4,6,95.0,1,0,0,0,0,0,0,0,0.0,0);
INSERT INTO "rtk_incident_detail" VALUES(5,6,95.0,1,0,0,0,0,0,0,0,0.0,0);

DROP TABLE IF EXISTS "rtk_incident_actions";
CREATE TABLE "rtk_incident_actions" (
    "fld_incident_id" INTEGER NOT NULL,
    "fld_action_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_prescribed_action" BLOB DEFAULT(''),
    "fld_action_taken" BLOB DEFAULT(''),
    "fld_action_owner" INTEGER DEFAULT(0),
    "fld_due_date" DATE DEFAULT (datetime(CURRENT_TIMESTAMP, '30 days')),
    "fld_status" INTEGER NOT NULL DEFAULT (0),
    "fld_approved_by" INTEGER DEFAULT(0),
    "fld_approved_date" INTEGER DEFAULT(0),
    "fld_approved" INTEGER DEFAULT(0),
    "fld_closed_by" INTEGER DEFAULT(0),
    "fld_closed_date" INTEGER DEFAULT(0),
    "fld_closed" INTEGER DEFAULT(0)
);
INSERT INTO "rtk_incident_actions" VALUES(1,1,'','',1,'2015-11-21 16:04:26',0,0,719163,0,0,719163,0);
INSERT INTO "rtk_incident_actions" VALUES(1,2,'','',1,'2015-11-21 16:04:26',0,0,719163,0,0,719163,0);
INSERT INTO "rtk_incident_actions" VALUES(1,3,'','',1,0,0,0,0,0,0,0,0);
INSERT INTO "rtk_incident_actions" VALUES(1,4,'','',1,0,0,0,0,0,0,0,0);
INSERT INTO "rtk_incident_actions" VALUES(5,5,'Identify a switch with contact ratings >0.5 amperes.','',1,'2015-11-21 16:04:26',2,0,0,0,0,735893,0);
INSERT INTO "rtk_incident_actions" VALUES(2,6,'','',0,'2015-11-21 16:04:26',0,0,0,0,0,0,0);
INSERT INTO "rtk_incident_actions" VALUES(5,7,'Revise electrical standard ELE-SW-001 to require specifying switch contact ratings based on maximum expected current rather than nominal expected current.','',2,'2015-11-21 16:04:26',2,0,0,0,0,0,0);

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
    "fld_cum_failures" INTEGER DEFAULT(0.0),                        -- Cumulative number of failures.
    "fld_confidence" REAL DEFAULT(0.75),                            -- Confidence level for GoF tests, MTBF bounds, etc.
    "fld_consumer_risk" REAL DEFAULT(0),                            -- The probability of the consumer accepting an item that fails to meet it's reliability requirement.
    "fld_producer_risk" REAL DEFAULT(0),                            -- The probability of the producer rejecting an item that actually meets it's reliability requirement.
    "fld_plan_model" INTEGER DEFAULT(0),                            -- The growth planning model to use (1=Duane, 2=Crow-AMSAA, 3=SPLAN, 4=SSPLAN).
    "fld_assess_model" INTEGER DEFAULT(0),                          -- The growth assessment model to use (1=Duane, 2=Crow-AMSAA, 3=Crow Extended)
    "fld_tr" REAL DEFAULT(0),                                       -- Technical requirement for the program MTBF.
    "fld_mg" REAL DEFAULT(0),                                       -- Goal MTBF for the entire test.
    "fld_mgp" REAL DEFAULT(0),                                      -- Growth potential MTBF for the entire test.
    "fld_num_phases" INTEGER DEFAULT(1),                            -- Number of growth test phases.
    "fld_ttt" REAL DEFAULT(0),                                      -- Total time on test over all phases.
    "fld_avg_growth" REAL DEFAULT(0.3),                             -- Average growth rate over all phases.
    "fld_avg_ms" REAL DEFAULT(0),                                   -- Average management strategy over all phases.
    "fld_avg_fef" REAL DEFAULT(0.7),                                -- Average fix effectiveness factor over all phases..
    "fld_prob" REAL DEFAULT(0.75),                                  -- Probability of observing a failure over all phases.
    "fld_ttff" REAL DEFAULT(0),                                     -- Time to first fix.
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
INSERT INTO "rtk_tests" VALUES(0,1,1,'Test Plan','Description',4,'Attachment',0.0,0,0.75,0.0,0.0,0,0,0.0,0.0,0.0,1,0.0,0.3,0.0,0.7,0.75,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0);
INSERT INTO "rtk_tests" VALUES(0,1,2,'Test Plan','None',4,'None',0.0,0,0.75,0.0,0.0,0,0,0.0,0.0,0.0,1,0.0,0.3,0.0,0.7,0.75,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0);
INSERT INTO "rtk_tests" VALUES(0,1,3,'Test Plan','None',4,'None',0.0,0,0.75,0.0,0.0,0,0,0.0,0.0,0.0,1,0.0,0.3,0.0,0.7,0.75,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0);

DROP TABLE IF EXISTS "rtk_growth_testing";
CREATE TABLE "rtk_growth_testing" (
    "fld_test_id" INTEGER,                                          -- The ID of the test.
    "fld_phase_id" INTEGER,                                         -- The ID of the test phase.
    "fld_i_mi" REAL DEFAULT(0),                                     -- Ideal initial MTBF for the test phase.
    "fld_i_mf" REAL DEFAULT(0),                                     -- Ideal final MTBF for the test phase.
    "fld_i_ma" REAL DEFAULT(0),                                     -- Ideal average MTBF for the test phase.
    "fld_i_num_fails" INTEGER DEFAULT(0),                           -- Expected number of failures predicted by the Ideal model for the test phase.
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
    PRIMARY KEY ("fld_test_id", "fld_phase_id"),
    FOREIGN KEY("fld_test_id") REFERENCES "rtk_tests"("fld_test_id") ON DELETE CASCADE
);
INSERT INTO "rtk_growth_testing" VALUES(1,0,0.0,0.0,0.0,0,0.47,1.214286,0.7,1.0,30.0,56.603775,43.301888,5000.0,166,735599,735886,0.0,5,1000.0,24.390244,0.06499,0.0,0.0,0.0,0.0,0.0,0.0,1,0.0);
INSERT INTO "rtk_growth_testing" VALUES(2,0,0.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,719163,719163,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0.0);
INSERT INTO "rtk_growth_testing" VALUES(3,0,0.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,719163,719163,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0.0);
INSERT INTO "rtk_growth_testing" VALUES(1,1,0.0,0.0,0.0,0,0.3,1.024259,0.7,0.0,56.603773,59.588109,59.295348,10000.0,168,735913,736279,0.0,4,2500.0,47.814208,0.38579,0.0,0.0,0.0,0.0,0.0,0.0,1,500.0);
INSERT INTO "rtk_growth_testing" VALUES(1,2,0.0,0.0,0.0,0,0.3,1.002942,0.7,0.0,59.588109,73.361568,80.694955,15000.0,185,736279,736644,0.0,4,3750.0,71.917808,0.547262,0.0,0.0,0.0,0.0,0.0,0.0,1,500.0);
INSERT INTO "rtk_growth_testing" VALUES(1,3,0.0,0.0,0.0,0,0.47,-0.368394,0.7,0.0,18.018224,21.306686,19.668313,150.0,7,735856,735917,0.0,6,25.0,2.868852,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1,25.3);
INSERT INTO "rtk_growth_testing" VALUES(1,4,0.0,0.0,0.0,0,0.47,-0.696354,0.7,0.0,21.306686,24.102899,22.708458,150.0,6,735964,736084,0.0,6,25.0,1.458333,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,25.3);

DROP TABLE IF EXISTS "rtk_survival";
CREATE TABLE "rtk_survival" (
    "fld_revision_id" INTEGER DEFAULT(0),
    "fld_survival_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
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
    "fld_start_time" FLOAT DEFAULT(0),          -- Minimum failure time for filtering survival data records.
    "fld_start_date" INTEGER DEFAULT(719163),   -- Start date for filtering survival data records.
    "fld_end_date" INTEGER DEFAULT(719163),     -- End date for filtering survival data records.
    "fld_nevada_chart" INTEGER DEFAULT(0)       -- Whether or not the dataset includes a Nevada chart.
);
INSERT INTO "rtk_survival" VALUES(0,1,1,'System Survival Analyses',4,3,0.75,3,3,2,500.0,50,0,14,0.004339,0.004582,0.004838,1.287071,1.298257,1.309442,0.0,0.0,0.0,9.708521,0.226665,0.0,0.005292,0.0,0.0,16.152813,0.685057,2.276464,1726.626548,1726.120875,-862.313274,0.0,735599,735920,0);
INSERT INTO "rtk_survival" VALUES(0,2,1,'Exponential Data Set',4,5,0.95,3,3,2,150.0,10,0,6,0.02466,0.05,0.10138,43.827727,43.827727,43.827727,0.0,0.0,0.0,0.000462,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,-1.151213,-2.504183,1.575606,0.0,735924,735924,0);
INSERT INTO "rtk_survival" VALUES(0,3,1,'Duane Data Set',4,3,0.9,3,3,2,22000.0,100,0,23,0.400464,0.513964,0.627463,0.377783,0.386766,0.39562,0.0,0.0,0.0,0.0,0.0,0.0,719163.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,735940,735940,0);

DROP TABLE IF EXISTS "rtk_survival_data";
CREATE TABLE "rtk_survival_data" (
    "fld_survival_id" INTEGER NOT NULL DEFAULT (0),
    "fld_dataset_id" INTEGER NOT NULL DEFAULT (0),
    "fld_record_id" INTEGER NOT NULL DEFAULT (0),
    "fld_name" VARCHAR(256) DEFAULT (''),
    "fld_source" INTEGER DEFAULT (0),
    "fld_failure_date" INTEGER DEFAULT (719163),
    "fld_left_interval" FLOAT DEFAULT (0),
    "fld_right_interval" FLOAT DEFAULT (0),
    "fld_status" INTEGER DEFAULT (0),
    "fld_quantity" INTEGER DEFAULT (1),
    "fld_tbf" FLOAT DEFAULT (0),
    "fld_mode_type" INTEGER DEFAULT (1),
    "fld_nevada_chart" INTEGER DEFAULT (0),
    "fld_ship_date" INTEGER DEFAULT (719163),
    "fld_number_shipped" INTEGER DEFAULT (1),
    "fld_return_date" INTEGER DEFAULT (719163),
    "fld_number_returned" INTEGER DEFAULT (0),
    "fld_user_float_1" FLOAT DEFAULT (0),
    "fld_user_float_2" FLOAT DEFAULT (0),
    "fld_user_float_3" FLOAT DEFAULT (0),
    "fld_user_integer_1" INTEGER DEFAULT (0),
    "fld_user_integer_2" INTEGER DEFAULT (0),
    "fld_user_integer_3" INTEGER DEFAULT (0),
    "fld_user_string_1" VARCHAR(256),
    "fld_user_string_2" VARCHAR(256),
    "fld_user_string_3" VARCHAR(256)
);
INSERT INTO "rtk_survival_data" VALUES(1,1,1,'Sub-System 1',0,735572,116.4,116.4,0,1,59.7,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(1,1,2,'Sub-System 1',0,735613,152.1,152.1,0,1,35.7,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(1,1,3,'Sub-System 1',0,735623,198.4,198.4,0,1,46.3,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(1,1,4,'Sub-System 1',0,735675,233.3,233.3,0,1,34.9,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(1,1,5,'Sub-System 1',0,735682,286.1,286.1,0,2,52.8,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(1,1,6,'Sub-System 1',0,735698,322.9,322.9,0,1,36.8,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(1,1,7,'Sub-System 1',0,735710,343.6,343.6,0,1,20.7,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(1,1,8,'Sub-System 1',0,735734,389.7,389.7,0,3,46.1,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(1,1,9,'Sub-System 1',0,735749,421.0,421.0,0,1,31.3,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(1,1,10,'Sub-System 1',0,735812,488.8,488.8,0,1,67.8,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(1,0,11,'Sub-System 1',0,735835,56.7,56.7,0,1,56.7,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(2,0,1,'',0,719163,16.0,16.0,0,1,16.0,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(2,0,2,'',0,719163,34.0,34.0,0,1,18.0,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(2,0,3,'',0,719163,53.0,53.0,0,1,19.0,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(2,0,4,'',0,719163,75.0,75.0,0,1,22.0,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(2,0,5,'',0,719163,93.0,93.0,0,1,18.0,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(2,0,6,'',0,719163,120.0,120.0,0,1,27.0,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(3,1,1,'System',1,719163,0.0,2.7,0,1,0.0,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(3,1,2,'System',1,719163,0.0,10.3,0,1,0.0,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(3,1,3,'System',1,719163,0.0,30.6,0,1,0.0,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(3,1,4,'System',1,719163,0.0,57.0,0,1,0.0,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(3,1,5,'System',1,719163,0.0,61.3,0,1,0.0,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(3,1,6,'System',1,719163,0.0,80.0,0,1,0.0,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(3,1,7,'System',1,719163,0.0,109.5,0,1,0.0,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(3,1,8,'System',1,719163,0.0,125.0,0,1,0.0,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(3,1,9,'System',1,719163,0.0,128.6,0,1,0.0,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(3,1,10,'System',1,719163,0.0,143.8,0,1,0.0,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(3,1,11,'System',1,719163,0.0,167.9,0,1,0.0,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(3,1,12,'System',1,719163,0.0,229.2,0,1,0.0,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(3,1,13,'System',1,719163,0.0,269.7,0,1,0.0,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(3,1,14,'System',1,719163,0.0,320.6,0,1,0.0,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(3,1,15,'System',1,719163,0.0,328.2,0,1,0.0,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(3,1,16,'System',1,719163,0.0,366.2,0,1,0.0,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(3,1,17,'System',1,719163,0.0,396.7,0,1,0.0,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(3,1,18,'System',1,719163,0.0,421.1,0,1,0.0,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(3,1,19,'System',1,719163,0.0,438.2,0,1,0.0,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(3,1,20,'System',1,719163,0.0,501.2,0,1,0.0,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');
INSERT INTO "rtk_survival_data" VALUES(3,1,21,'System',1,719163,0.0,620.0,0,1,0.0,1,0,719163,1,719163,0,0.0,0.0,0.0,0,0,0,'None','None','None');

-- COMMIT;
