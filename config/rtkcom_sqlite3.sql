PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

--
-- Create tables for site-wide information.
--
DROP TABLE IF EXISTS "tbl_site_info";
CREATE TABLE "tbl_site_info" (
    "fld_product_key" VARCHAR(64) NOT NULL,
    "fld_expire_date" INTEGER NOT NULL DEFAULT(719163)
);

--
-- Table to store responsible department information.
--
DROP TABLE IF EXISTS "tbl_departments";
CREATE TABLE "tbl_departments" (
    "fld_department_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT  -- Identifier for the department.
    "fld_department_name" VARCHAR(512) NOT NULL DEFAULT('') -- Noun name of the department.
);

--
-- Table to store customer need affinity groups.
--
DROP TABLE IF EXISTS "tbl_need_groups";
CREATE TABLE "tbl_need_groups" (
    "fld_group_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT   -- Identifier for the need group.
    "fld_group_name" VARCHAR(256) NOT NULL DEFAULT('')  -- Name of the need group.
);

--
-- Create tables for general program information.
--
DROP TABLE IF EXISTS "tbl_distributions";
CREATE TABLE "tbl_distributions" (
  "fld_distribution_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_distribution_noun" VARCHAR(64) NOT NULL
);
INSERT INTO "tbl_distributions" VALUES (1,'Constant Probability');
INSERT INTO "tbl_distributions" VALUES (2,'Exponential');
INSERT INTO "tbl_distributions" VALUES (3,'LogNormal');
INSERT INTO "tbl_distributions" VALUES (4,'Uniform');
INSERT INTO "tbl_distributions" VALUES (5,'Weibull');

DROP TABLE IF EXISTS "tbl_lifecycles";
CREATE TABLE "tbl_lifecycles" (
  "fld_lifecycle_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_lifecycle_name" VARCHAR(128)
);
INSERT INTO "tbl_lifecycles" VALUES (1, "Design");
INSERT INTO "tbl_lifecycles" VALUES (2, "Reliability Growth");
INSERT INTO "tbl_lifecycles" VALUES (3, "Reliability Qualification");
INSERT INTO "tbl_lifecycles" VALUES (4, "Production");
INSERT INTO "tbl_lifecycles" VALUES (5, "Storage");
INSERT INTO "tbl_lifecycles" VALUES (6, "Operation");
INSERT INTO "tbl_lifecycles" VALUES (7, "Disposal");

DROP TABLE IF EXISTS "tbl_manufacturers";
CREATE TABLE "tbl_manufacturers" (
  "fld_manufacturers_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_manufacturers_noun" VARCHAR(128) DEFAULT '',
  "fld_location" VARCHAR(45) DEFAULT '',
  "fld_cage_code" VARCHAR(45) DEFAULT ''
);
INSERT INTO "tbl_manufacturers" VALUES (1,'Sprague','New Hampshire','13606');
INSERT INTO "tbl_manufacturers" VALUES (2,'Xilinx','','');
INSERT INTO "tbl_manufacturers" VALUES (3,'National Semiconductor','California','27014');

DROP TABLE IF EXISTS "tbl_measurement_units";
CREATE TABLE "tbl_measurement_units" (
  "fld_measurement_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_measurement_code" VARCHAR(64) DEFAULT NULL
);
INSERT INTO "tbl_measurement_units" VALUES (1,'lbf');
INSERT INTO "tbl_measurement_units" VALUES (2,'hours');

DROP TABLE IF EXISTS "tbl_mttr_type";
CREATE TABLE "tbl_mttr_type" (
  "fld_mttr_type_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_mttr_type_noun" VARCHAR(64) NOT NULL
);
INSERT INTO "tbl_mttr_type" VALUES (1,'Assessed');
INSERT INTO "tbl_mttr_type" VALUES (2,'Specified');

DROP TABLE IF EXISTS "tbl_requirement_type";
CREATE TABLE "tbl_requirement_type" (
  "fld_requirement_type_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_requirement_type_desc" VARCHAR(32) DEFAULT NULL,
  "fld_requirement_type_code" VARCHAR(4) DEFAULT NULL
);
INSERT INTO "tbl_requirement_type" ("fld_requirement_type_desc", "fld_requirement_type_code") VALUES ('Functional','FUN');
INSERT INTO "tbl_requirement_type" ("fld_requirement_type_desc", "fld_requirement_type_code") VALUES ('Performance','PRF');
INSERT INTO "tbl_requirement_type" ("fld_requirement_type_desc", "fld_requirement_type_code") VALUES ('Regulatory','REG');
INSERT INTO "tbl_requirement_type" ("fld_requirement_type_desc", "fld_requirement_type_code") VALUES ('Reliability','REL');
INSERT INTO "tbl_requirement_type" ("fld_requirement_type_desc", "fld_requirement_type_code") VALUES ('Safety','SAF');
INSERT INTO "tbl_requirement_type" ("fld_requirement_type_desc", "fld_requirement_type_code") VALUES ('Serviceability','SVC');
INSERT INTO "tbl_requirement_type" ("fld_requirement_type_desc", "fld_requirement_type_code") VALUES ('Usability','USE');

DROP TABLE IF EXISTS "tbl_stakeholders";
CREATE TABLE "tbl_stakeholders" (
    "fld_stakeholder_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_stakeholder" VARCHAR(128)
);

DROP TABLE IF EXISTS "tbl_status";
CREATE TABLE "tbl_status" (
  "fld_status_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_status_name" VARCHAR(256),
  "fld_status_description" BLOB
);
INSERT INTO "tbl_status" ("fld_status_name", "fld_status_description") VALUES ('Initiated', 'Incident or action has been initiated.');
INSERT INTO "tbl_status" ("fld_status_name", "fld_status_description") VALUES ('Reviewed', 'Incident or action has been reviewed.');
INSERT INTO "tbl_status" ("fld_status_name", "fld_status_description") VALUES ('Analysis', 'Incident or action has been assigned and is being analyzed.');
INSERT INTO "tbl_status" ("fld_status_name", "fld_status_description") VALUES ('Solution Identified', 'A solution to the reported problem has been identified.');
INSERT INTO "tbl_status" ("fld_status_name", "fld_status_description") VALUES ('Solution Implemented', 'A solution to the reported problem has been implemented.');
INSERT INTO "tbl_status" ("fld_status_name", "fld_status_description") VALUES ('Solution Verified', 'A solution to the reported problem has been verified.');
INSERT INTO "tbl_status" ("fld_status_name", "fld_status_description") VALUES ('Ready for Approval', 'Incident analysis or action is ready to be approved.');
INSERT INTO "tbl_status" ("fld_status_name", "fld_status_description") VALUES ('Approved', 'Incident or action has been approved.');
INSERT INTO "tbl_status" ("fld_status_name", "fld_status_description") VALUES ('Ready for Closure', 'Incident or action is ready to be closed.');
INSERT INTO "tbl_status" ("fld_status_name", "fld_status_description") VALUES ('Closed', 'Incident or action has been closed.');

DROP TABLE IF EXISTS "tbl_groups";
CREATE TABLE "tbl_groups" (
    "fld_group_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,  -- Identifier for the group.
    "fld_group_name" VARCHAR (256)                      -- Name of the group.
);
INSERT INTO "tbl_groups" ("fld_group_name") VALUES ('Engineering, Design');
INSERT INTO "tbl_groups" ("fld_group_name") VALUES ('Engineering, Logistics Support');
INSERT INTO "tbl_groups" ("fld_group_name") VALUES ('Engineering, Maintainability');
INSERT INTO "tbl_groups" ("fld_group_name") VALUES ('Engineering, Reliability');
INSERT INTO "tbl_groups" ("fld_group_name") VALUES ('Engineering, Safety');
INSERT INTO "tbl_groups" ("fld_group_name") VALUES ('Engineering, Software');

DROP TABLE IF EXISTS "tbl_users";
CREATE TABLE "tbl_users" (
    "fld_user_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,   -- Identifier for the user.
    "fld_group_id" VARCHAR (256),                 -- Group ID user belongs too.
    "fld_user_lname" VARCHAR (256),                     -- User's last name.
    "fld_user_fname" VARCHAR (256),                     -- User's first name.
    "fld_user_email" VARCHAR (256),                     -- User's email address.
    "fld_user_phone" VARCHAR (256),                     -- User's phone number.
    "fld_is_admin" TINYINT DEFAULT (0)                  -- Indicates whether or not the user has admin privileges.
);

--
-- Create tables for storing component information.
--
DROP TABLE IF EXISTS "tbl_category";
CREATE TABLE "tbl_category" (
  "fld_category_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_category_noun" VARCHAR(64) DEFAULT NULL
);
INSERT INTO "tbl_category" VALUES (1,'Integrated Circuit');
INSERT INTO "tbl_category" VALUES (2,'Semiconductor');
INSERT INTO "tbl_category" VALUES (3,'Resistor');
INSERT INTO "tbl_category" VALUES (4,'Capacitor');
INSERT INTO "tbl_category" VALUES (5,'Inductive Device');
INSERT INTO "tbl_category" VALUES (6,'Relay');
INSERT INTO "tbl_category" VALUES (7,'Switching Device');
INSERT INTO "tbl_category" VALUES (8,'Connection');
INSERT INTO "tbl_category" VALUES (9,'Meter');
INSERT INTO "tbl_category" VALUES (10,'Miscellaneous');
INSERT INTO "tbl_category" VALUES (1000,'Function');

DROP TABLE IF EXISTS "tbl_subcategory";
CREATE TABLE "tbl_subcategory" (
  "fld_category_id" INTEGER NOT NULL,
  "fld_subcategory_id" INTEGER NOT NULL,
  "fld_subcategory_noun" VARCHAR(64) DEFAULT NULL,
  PRIMARY KEY ("fld_category_id","fld_subcategory_id"),
  CONSTRAINT "tbl_subcategory_ibfk_1" FOREIGN KEY ("fld_category_id") REFERENCES "tbl_category" ("fld_category_id") ON DELETE CASCADE ON UPDATE CASCADE
);
INSERT INTO "tbl_subcategory" VALUES (1,1,'Linear');
INSERT INTO "tbl_subcategory" VALUES (1,2,'Logic');
INSERT INTO "tbl_subcategory" VALUES (1,3,'PAL, PLA');
INSERT INTO "tbl_subcategory" VALUES (1,4,'Microprocessor, Microcontroller');
INSERT INTO "tbl_subcategory" VALUES (1,5,'Memory, ROM');
INSERT INTO "tbl_subcategory" VALUES (1,6,'Memory, EEPROM');
INSERT INTO "tbl_subcategory" VALUES (1,7,'Memory, DRAM');
INSERT INTO "tbl_subcategory" VALUES (1,8,'Memory, SRAM');
INSERT INTO "tbl_subcategory" VALUES (1,9,'GaAs Digital');
INSERT INTO "tbl_subcategory" VALUES (1,10,'GaAs MMIC');
INSERT INTO "tbl_subcategory" VALUES (1,11,'VHSIC, VLSI');
INSERT INTO "tbl_subcategory" VALUES (2,12,'Diode, Low Frequency');
INSERT INTO "tbl_subcategory" VALUES (2,13,'Diode, High Frequency');
INSERT INTO "tbl_subcategory" VALUES (2,14,'Transistor, Low Frequency, Bipolar');
INSERT INTO "tbl_subcategory" VALUES (2,15,'Transistor, Low Frequency, Si FET');
INSERT INTO "tbl_subcategory" VALUES (2,16,'Transistor, Unijunction');
INSERT INTO "tbl_subcategory" VALUES (2,17,'Transistor, High Frequency, Low Noise, Bipolar');
INSERT INTO "tbl_subcategory" VALUES (2,18,'Transistor, High Frequency, High Power, Bipolar');
INSERT INTO "tbl_subcategory" VALUES (2,19,'Transistor, High Frequency, GaAs FET');
INSERT INTO "tbl_subcategory" VALUES (2,20,'Transistor, High Frequency, Si FET');
INSERT INTO "tbl_subcategory" VALUES (2,21,'Thyristor, SCR');
INSERT INTO "tbl_subcategory" VALUES (2,22,'Optoelectronic, Detector, Isolator, Emitter');
INSERT INTO "tbl_subcategory" VALUES (2,23,'Optoelectronic, Alphanumeric Display');
INSERT INTO "tbl_subcategory" VALUES (2,24,'Optoelectronic, Laser Diode');
INSERT INTO "tbl_subcategory" VALUES (3,25,'Fixed, Composition (RC, RCR)');
INSERT INTO "tbl_subcategory" VALUES (3,26,'Fixed, Film (RL, RLR, RN, RNC, RNN, RNR)');
INSERT INTO "tbl_subcategory" VALUES (3,27,'Fixed, Film, Power (RD)');
INSERT INTO "tbl_subcategory" VALUES (3,28,'Fixed, Film, Network (RZ)');
INSERT INTO "tbl_subcategory" VALUES (3,29,'Fixed, Wirewound (RB, RBR)');
INSERT INTO "tbl_subcategory" VALUES (3,30,'Fixed, Wirewound, Power (RW, RWR)');
INSERT INTO "tbl_subcategory" VALUES (3,31,'Fixed, Wirewound, Power, Chassis-Mounted (RE, RER)');
INSERT INTO "tbl_subcategory" VALUES (3,32,'Thermistor (RTH)');
INSERT INTO "tbl_subcategory" VALUES (3,33,'Variable, Wirewound (RT, RTR)');
INSERT INTO "tbl_subcategory" VALUES (3,34,'Variable, Wirewound, Precision (RR)');
INSERT INTO "tbl_subcategory" VALUES (3,35,'Variable, Wirewound, Semiprecision (RA, RK)');
INSERT INTO "tbl_subcategory" VALUES (3,36,'Variable, Wirewound, Power (RP)');
INSERT INTO "tbl_subcategory" VALUES (3,37,'Variable, Non-Wirewound (RJ, RJR)');
INSERT INTO "tbl_subcategory" VALUES (3,38,'Variable, Composition (RV)');
INSERT INTO "tbl_subcategory" VALUES (3,39,'Variable, Non-Wirewound, Film and Precision (RQ, RVC)');
INSERT INTO "tbl_subcategory" VALUES (4,40,'Fixed, Paper, Bypass (CA, CP)');
INSERT INTO "tbl_subcategory" VALUES (4,41,'Fixed, Feed-Through (CZ, CZR)');
INSERT INTO "tbl_subcategory" VALUES (4,42,'Fixed, Paper and Plastic Film (CPV, CQ, CQR)');
INSERT INTO "tbl_subcategory" VALUES (4,43,'Fixed, Metallized Paper, Paper-Plastic and Plastic (CH, CHR)');
INSERT INTO "tbl_subcategory" VALUES (4,44,'Fixed, Plastic and Metallized Plastic');
INSERT INTO "tbl_subcategory" VALUES (4,45,'Fixed, Super-Metallized Plastic (CRH)');
INSERT INTO "tbl_subcategory" VALUES (4,46,'Fixed, Mica (CM, CMR)');
INSERT INTO "tbl_subcategory" VALUES (4,47,'Fixed, Mica, Button (CB)');
INSERT INTO "tbl_subcategory" VALUES (4,48,'Fixed, Glass (CY, CYR)');
INSERT INTO "tbl_subcategory" VALUES (4,49,'Fixed, Ceramic, General Purpose (CK, CKR)');
INSERT INTO "tbl_subcategory" VALUES (4,50,'Fixed, Ceramic, Temperature Compensating and Chip (CC, CCR, CDR)');
INSERT INTO "tbl_subcategory" VALUES (4,51,'Fixed, Electrolytic, Tantalum, Solid (CSR)');
INSERT INTO "tbl_subcategory" VALUES (4,52,'Fixed, Electrolytic, Tantalum, Non-Solid (CL, CLR)');
INSERT INTO "tbl_subcategory" VALUES (4,53,'Fixed, Electrolytic, Aluminum (CU, CUR)');
INSERT INTO "tbl_subcategory" VALUES (4,54,'Fixed, Electrolytic (Dry), Aluminum (CE)');
INSERT INTO "tbl_subcategory" VALUES (4,55,'Variable, Ceramic (CV)');
INSERT INTO "tbl_subcategory" VALUES (4,56,'Variable, Piston Type (PC)');
INSERT INTO "tbl_subcategory" VALUES (4,57,'Variable, Air Trimmer (CT)');
INSERT INTO "tbl_subcategory" VALUES (4,58,'Variable and Fixed, Gas or Vacuum (CG)');
INSERT INTO "tbl_subcategory" VALUES (5,59,'Transformer, Pulse');
INSERT INTO "tbl_subcategory" VALUES (5,60,'Transformer, Audio');
INSERT INTO "tbl_subcategory" VALUES (5,61,'Transformer, Power');
INSERT INTO "tbl_subcategory" VALUES (5,62,'Transformer, RF');
INSERT INTO "tbl_subcategory" VALUES (5,63,'Coil');
INSERT INTO "tbl_subcategory" VALUES (6,64,'Mechanical');
INSERT INTO "tbl_subcategory" VALUES (6,65,'Solid State');
INSERT INTO "tbl_subcategory" VALUES (7,67,'Toggle or Pushbutton');
INSERT INTO "tbl_subcategory" VALUES (7,68,'Sensitive');
INSERT INTO "tbl_subcategory" VALUES (7,69,'Rotary');
INSERT INTO "tbl_subcategory" VALUES (7,70,'Thumbwheel');
INSERT INTO "tbl_subcategory" VALUES (7,71,'Circuit Breaker');
INSERT INTO "tbl_subcategory" VALUES (8,72,'Multi-Pin');
INSERT INTO "tbl_subcategory" VALUES (8,73,'PCB Edge');
INSERT INTO "tbl_subcategory" VALUES (8,74,'IC Socket');
INSERT INTO "tbl_subcategory" VALUES (8,75,'Plated Through Hole');
INSERT INTO "tbl_subcategory" VALUES (8,76,'Clip');
INSERT INTO "tbl_subcategory" VALUES (8,83,'Crimp');
INSERT INTO "tbl_subcategory" VALUES (8,84,'Hand Solder');
INSERT INTO "tbl_subcategory" VALUES (8,85,'Reflow Solder');
INSERT INTO "tbl_subcategory" VALUES (8,86,'Weld');
INSERT INTO "tbl_subcategory" VALUES (8,87,'Wrap');
INSERT INTO "tbl_subcategory" VALUES (9,77,'Elapsed Time');
INSERT INTO "tbl_subcategory" VALUES (9,78,'Panel');
INSERT INTO "tbl_subcategory" VALUES (10,80,'Crystal');
INSERT INTO "tbl_subcategory" VALUES (10,81,'Lamp');
INSERT INTO "tbl_subcategory" VALUES (10,82,'Fuse');
INSERT INTO "tbl_subcategory" VALUES (10,83,'Filter, Non-Tunable Electronic');
INSERT INTO "tbl_subcategory" VALUES (1000,1,'All');

--
-- Create tables for storing environmental information.
--
DROP TABLE IF EXISTS "tbl_active_environs";
CREATE TABLE "tbl_active_environs" (
  "fld_subcategory_id" INTEGER NOT NULL,
  "fld_calculation_model_id" INTEGER NOT NULL,
  "fld_active_environ_id" INTEGER NOT NULL,
  "fld_active_environ_code" VARCHAR(4) NOT NULL,
  "fld_active_environ_noun" VARCHAR(64) NOT NULL,
  "fld_pi_e" FLOAT NOT NULL DEFAULT (1),
  PRIMARY KEY ("fld_subcategory_id","fld_calculation_model_id","fld_active_environ_id"),
  CONSTRAINT "tbl_active_environs_ibfk_1" FOREIGN KEY ("fld_calculation_model_id") REFERENCES "tbl_calculation_model" ("fld_model_id") ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT "tbl_active_environs_ibfk_2" FOREIGN KEY ("fld_subcategory_id") REFERENCES "tbl_subcategory" ("fld_subcategory_id") ON DELETE CASCADE ON UPDATE CASCADE
);
INSERT INTO "tbl_active_environs" VALUES (1,1,1,'GB','Ground, Benign',0.5);
INSERT INTO "tbl_active_environs" VALUES (1,1,2,'GF','Ground, Fixed',2);
INSERT INTO "tbl_active_environs" VALUES (1,1,3,'GM','Ground, Mobile',4);
INSERT INTO "tbl_active_environs" VALUES (1,1,4,'NS','Naval, Sheltered',4);
INSERT INTO "tbl_active_environs" VALUES (1,1,5,'NU','Naval, Unsheltered',6);
INSERT INTO "tbl_active_environs" VALUES (1,1,6,'AIC','Airborne, Inhabited, Cargo',4);
INSERT INTO "tbl_active_environs" VALUES (1,1,7,'AIF','Airborne, Inhabited, Fighter',5);
INSERT INTO "tbl_active_environs" VALUES (1,1,8,'AUC','Airborne, Uninhabited, Cargo',5);
INSERT INTO "tbl_active_environs" VALUES (1,1,9,'AUF','Airborne, Uninhabited, Fighter',8);
INSERT INTO "tbl_active_environs" VALUES (1,1,10,'ARW','Airborne, Rotary Wing',8);
INSERT INTO "tbl_active_environs" VALUES (1,1,11,'SF','Space, Flight',0.5);
INSERT INTO "tbl_active_environs" VALUES (1,1,12,'MF','Missile, Flight',5);
INSERT INTO "tbl_active_environs" VALUES (1,1,13,'ML','Missile, Launch',12);
INSERT INTO "tbl_active_environs" VALUES (1,1,14,'CL','Cannon, Launch',220);

DROP TABLE IF EXISTS "tbl_dormant_environs";
CREATE TABLE "tbl_dormant_environs" (
  "fld_model_id" INTEGER NOT NULL,
  "fld_dormant_environ_id" INTEGER NOT NULL,
  "fld_dormant_environ_noun" VARCHAR(64) NOT NULL,
  PRIMARY KEY ("fld_model_id","fld_dormant_environ_id"),
  CONSTRAINT "tbl_dormant_environs_ibfk_1" FOREIGN KEY ("fld_model_id") REFERENCES "tbl_calculation_model" ("fld_model_id") ON DELETE CASCADE ON UPDATE CASCADE
);
INSERT INTO "tbl_dormant_environs" VALUES (1,1,'Ground');
INSERT INTO "tbl_dormant_environs" VALUES (1,2,'Naval');
INSERT INTO "tbl_dormant_environs" VALUES (1,3,'Airborne');

DROP TABLE IF EXISTS "tbl_environmental_conditions";
CREATE TABLE "tbl_environmental_conditions" (
    "fld_condition_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_condition_name" VARCHAR(128)
);
INSERT INTO "tbl_environmental_conditions" VALUES(0, "Abrasion");
INSERT INTO "tbl_environmental_conditions" VALUES(1, "Acceleration");
INSERT INTO "tbl_environmental_conditions" VALUES(2, "Corona");
INSERT INTO "tbl_environmental_conditions" VALUES(3, "Contamination, Chemicals");
INSERT INTO "tbl_environmental_conditions" VALUES(4, "Contamination, Dirt/Dust");
INSERT INTO "tbl_environmental_conditions" VALUES(5, "Contamination, Salt Spray");
INSERT INTO "tbl_environmental_conditions" VALUES(6, "Electrostatic Discharge");
INSERT INTO "tbl_environmental_conditions" VALUES(7, "Fungus");
INSERT INTO "tbl_environmental_conditions" VALUES(8, "Gas, Ionized");
INSERT INTO "tbl_environmental_conditions" VALUES(9, "Geomagnetics");
INSERT INTO "tbl_environmental_conditions" VALUES(10, "Humidity");
INSERT INTO "tbl_environmental_conditions" VALUES(11, "Ozone");
INSERT INTO "tbl_environmental_conditions" VALUES(12, "Pressure, Atmospheric");
INSERT INTO "tbl_environmental_conditions" VALUES(13, "Pressure");
INSERT INTO "tbl_environmental_conditions" VALUES(14, "Radiation, Alpha");
INSERT INTO "tbl_environmental_conditions" VALUES(15, "Radiation, Electromagnetic");
INSERT INTO "tbl_environmental_conditions" VALUES(16, "Radiation, Gamma");
INSERT INTO "tbl_environmental_conditions" VALUES(17, "Radiation, Neutron");
INSERT INTO "tbl_environmental_conditions" VALUES(18, "Radiation, Solar");
INSERT INTO "tbl_environmental_conditions" VALUES(19, "Shock, Mechanical");
INSERT INTO "tbl_environmental_conditions" VALUES(20, "Shock, Thermal");
INSERT INTO "tbl_environmental_conditions" VALUES(21, "Temperature");
INSERT INTO "tbl_environmental_conditions" VALUES(22, "Thermal Cycles");
INSERT INTO "tbl_environmental_conditions" VALUES(23, "Vibration, Acoustic");
INSERT INTO "tbl_environmental_conditions" VALUES(24, "Vibration, Mechanical");
INSERT INTO "tbl_environmental_conditions" VALUES(25, "Weather, Fog");
INSERT INTO "tbl_environmental_conditions" VALUES(26, "Weather, Freezing Rain");
INSERT INTO "tbl_environmental_conditions" VALUES(27, "Weather, Frost");
INSERT INTO "tbl_environmental_conditions" VALUES(28, "Weather, Hail");
INSERT INTO "tbl_environmental_conditions" VALUES(29, "Weather, Ice");
INSERT INTO "tbl_environmental_conditions" VALUES(30, "Weather, Rain");
INSERT INTO "tbl_environmental_conditions" VALUES(31, "Weather, Sleet");
INSERT INTO "tbl_environmental_conditions" VALUES(32, "Weather, Snow");
INSERT INTO "tbl_environmental_conditions" VALUES(33, "Weather, Wind");

--
-- Create tables for system reliability assessments.
--
DROP TABLE IF EXISTS "tbl_allocation_models";
CREATE TABLE "tbl_allocation_models" (
  "fld_allocation_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_allocation_noun" VARCHAR(64) NOT NULL
);
INSERT INTO "tbl_allocation_models" VALUES (1,'Equal Apportionment');
INSERT INTO "tbl_allocation_models" VALUES (2,'AGREE Apportionment');
INSERT INTO "tbl_allocation_models" VALUES (3,'ARINC Apportionment');
INSERT INTO "tbl_allocation_models" VALUES (4,'Feasibility of Objectives');
INSERT INTO "tbl_allocation_models" VALUES (5,'Repairable Systems Apportionment');

DROP TABLE IF EXISTS "tbl_calculation_model";
CREATE TABLE "tbl_calculation_model" (
  "fld_model_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_model_noun" VARCHAR(50) DEFAULT NULL
);
INSERT INTO "tbl_calculation_model" VALUES (1,'MIL-HDBK-217F Stress');
INSERT INTO "tbl_calculation_model" VALUES (2,'MIL-HDBK-217F Parts Count');
INSERT INTO "tbl_calculation_model" VALUES (3,'MIL-HDBK-217FN1 Stress');
INSERT INTO "tbl_calculation_model" VALUES (4,'MIL-HDBK-217FN1 Parts Count');
INSERT INTO "tbl_calculation_model" VALUES (5,'MIL-HDBK-217FN2 Stress');
INSERT INTO "tbl_calculation_model" VALUES (6,'MIL-HDBK-217FN2 Parts Count');
INSERT INTO "tbl_calculation_model" VALUES (7,'Mechanical');

DROP TABLE IF EXISTS "tbl_cost_type";
CREATE TABLE "tbl_cost_type" (
  "fld_cost_type_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_cost_type_noun" VARCHAR(64) NOT NULL
);
INSERT INTO "tbl_cost_type" VALUES (1,'Calculated');
INSERT INTO "tbl_cost_type" VALUES (2,'Specified');

DROP TABLE IF EXISTS "tbl_hr_type";
CREATE TABLE "tbl_hr_type" (
  "fld_hr_type_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_hr_type_noun" VARCHAR(64) NOT NULL
);
INSERT INTO "tbl_hr_type" VALUES (1,'Assessed');
INSERT INTO "tbl_hr_type" VALUES (2,'Specified, Hazard Rate');
INSERT INTO "tbl_hr_type" VALUES (3,'Specified, MTBF');

--
-- Create tables for storing failure probability and failure criticality
-- category information.
--
DROP TABLE IF EXISTS "tbl_failure_probability";
CREATE TABLE "tbl_failure_probability" (
    "fld_probability_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_probability_name" VARCHAR(256),
    "fld_probability_values" INTEGER
);
INSERT INTO "tbl_failure_probability" VALUES(0, "Level A - Frequent", 1);
INSERT INTO "tbl_failure_probability" VALUES(1, "Level B - Reasonably Probable", 2);
INSERT INTO "tbl_failure_probability" VALUES(2, "Level C - Occasional", 3);
INSERT INTO "tbl_failure_probability" VALUES(3, "Level D - Remote", 4);
INSERT INTO "tbl_failure_probability" VALUES(4, "Level E - Extremely Unlikely", 5);

DROP TABLE IF EXISTS "tbl_criticality";
CREATE TABLE "tbl_criticality" (
  "fld_criticality_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_criticality_name" VARCHAR(256),
  "fld_criticality_cat" VARCHAR(218),
  "fld_criticality_description" BLOB,
  "fld_criticality_value" INTEGER
);
INSERT INTO "tbl_criticality" VALUES (1,"Catastrophic","I","Could result in death, permanent total disability, loss exceeding $1M, or irreversible severe environmental damage that violates law or regulation.", 4);
INSERT INTO "tbl_criticality" VALUES (2,"Critical","II","Could result in permanent partial disability, injuries or occupational illness that may result in hospitalization of at least three personnel, loss exceeding $200K but less than $1M, or reversible environmental damage causing a violation of law or regulation.", 3);
INSERT INTO "tbl_criticality" VALUES (3,"Marginal","III","Could result in injury or occupational illness resulting in one or more lost work days(s), loss exceeding $10K but less than $200K, or mitigatible environmental damage without violation of law or regulation where restoration activities can be accomplished.", 2);
INSERT INTO "tbl_criticality" VALUES (4,"Negligble","IV","Could result in injury or illness not resulting in a lost work day, loss exceeding $2K but less than $10K, or minimal environmental damage not violating law or regulation.", 1);

DROP TABLE IF EXISTS "tbl_hazards";
CREATE TABLE "tbl_hazards" (
    "fld_hazard_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_category" VARCHAR(256),
    "fld_subcategory" VARCHAR(256)
);
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Acceleration/Gravity", "Falls");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Acceleration/Gravity", "Falling Objects");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Acceleration/Gravity", "Fragments/Missiles");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Acceleration/Gravity", "Impacts");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Acceleration/Gravity", "Inadvertent Motion");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Acceleration/Gravity", "Loose Object Translation");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Acceleration/Gravity", "Slip/Trip");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Acceleration/Gravity", "Sloshing Liquids");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Chemical/Water Contamination", "Backflow/Siphon Effect");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Chemical/Water Contamination", "Leaks/Spills");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Chemical/Water Contamination", "System-Cross Connection");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Chemical/Water Contamination", "Vessel/Pipe/Conduit Rupture");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Common Causes", "Dust/Dirt");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Common Causes", "Faulty Calibration");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Common Causes", "Fire");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Common Causes", "Flooding");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Common Causes", "Location");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Common Causes", "Maintenance Error");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Common Causes", "Moisture/Humidity");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Common Causes", "Radiation");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Common Causes", "Seismic Disturbance/Impact");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Common Causes", "Single-Operator Coupling");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Common Causes", "Temperature Extremes");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Common Causes", "Utility Outages");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Common Causes", "Vibration");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Common Causes", "Wear-Out");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Common Causes", "Vermin/Insects");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Contingencies", "Earthquake");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Contingencies", "Fire");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Contingencies", "Flooding");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Contingencies", "Freezing");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Contingencies", "Hailstorm");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Contingencies", "Shutdowns/Failures");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Contingencies", "Snow/Ice Load");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Contingencies", "Utility Outages");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Contingencies", "Windstorm");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Control Systems", "Grounding Failure");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Control Systems", "Inadvertent Activation");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Control Systems", "Interferences (EMI/ESI)");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Control Systems", "Lightning Strike");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Control Systems", "Moisture");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Control Systems", "Power Outage");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Control Systems", "Sneak Circuit");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Control Systems", "Sneak Software");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Electrical", "Burns");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Electrical", "Distribution Feedback");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Electrical", "Explosion (Arc)");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Electrical", "Explosion (Electrostatic)");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Electrical", "Overheating");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Electrical", "Power Outage");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Electrical", "Shock");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Ergonomics", "Fatigue");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Ergonomics", "Faulty/Inadequate Control/Readout Labeling");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Ergonomics", "Faulty Work Station Design");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Ergonomics", "Glare");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Ergonomics", "Inaccessibility");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Ergonomics", "Inadequate Control/Readout Differentiation");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Ergonomics", "Inadequate/Improper Illumination");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Ergonomics", "Inappropriate Control/Readout Location");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Ergonomics", "Nonexistent/Inadequate 'Kill' Switches");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Explosive Conditions", "Explosive Dust Present");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Explosive Conditions", "Explosive Gas Present");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Explosive Conditions", "Explosive Liquid Present");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Explosive Conditions", "Explosive Propellant Present");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Explosive Conditions", "Explosive Vapor Present");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Explosive Effects", "Blast Overpressure");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Explosive Effects", "Mass Fire");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Explosive Effects", "Seismic Ground Wave");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Explosive Effects", "Thrown Fragments");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Explosive Initiator", "Chemical Contamination");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Explosive Initiator", "Electrostatic Discharge");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Explosive Initiator", "Friction");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Explosive Initiator", "Heat");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Explosive Initiator", "Impact/Shock");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Explosive Initiator", "Lightning");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Explosive Initiator", "Vibration");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Explosive Initiator", "Welding (Stray Current/Sparks)");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Fire/Flammability", "Fuel");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Fire/Flammability", "Ignition Source");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Fire/Flammability", "Oxidizer");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Fire/Flammability", "Propellant");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Human Factors", "Failure to Operate");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Human Factors", "Inadvertent Operation");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Human Factors", "Operated Too Long");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Human Factors", "Operated Too Briefly");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Human Factors", "Operation Early/Late");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Human Factors", "Operation Out of Sequence");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Human Factors", "Operator Error");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Human Factors", "Right Operation/Wrong Control");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Ionizing Radiation", "Alpha");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Ionizing Radiation", "Beta");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Ionizing Radiation", "Gamma");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Ionizing Radiation", "Neutron");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Ionizing Radiation", "X-Ray");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Leaks/Spills", "Asphyxiating");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Leaks/Spills", "Corrosive");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Leaks/Spills", "Flammable");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Leaks/Spills", "Flooding");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Leaks/Spills", "Gases/Vapors");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Leaks/Spills", "Irritating Dusts");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Leaks/Spills", "Liquids/Cryogens");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Leaks/Spills", "Odorous");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Leaks/Spills", "Pathogenic");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Leaks/Spills", "Radiation Sources");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Leaks/Spills", "Reactive");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Leaks/Spills", "Run Off");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Leaks/Spills", "Slippery");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Leaks/Spills", "Toxic");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Leaks/Spills", "Vapor Propagation");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Mechanical", "Crushing Surfaces");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Mechanical", "Ejected Parts/Fragments");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Mechanical", "Lifting Weights");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Mechanical", "Pinch Points");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Mechanical", "Reciprocating Equipment");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Mechanical", "Rotating Equipment");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Mechanical", "Sharp Edges/Points");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Mechanical", "Stability/Topping Potential");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Mission Phasing", "Activation");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Mission Phasing", "Calibration");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Mission Phasing", "Checkout");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Mission Phasing", "Coupling/Uncoupling");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Mission Phasing", "Delivery");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Mission Phasing", "Diagnosis/Trouble Shooting");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Mission Phasing", "Emergency Start");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Mission Phasing", "Installation");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Mission Phasing", "Load Change");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Mission Phasing", "Maintenance");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Mission Phasing", "Normal Operation");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Mission Phasing", "Shake Down");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Mission Phasing", "Shutdown Emergency");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Mission Phasing", "Standard Shutdown");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Mission Phasing", "Standard Start");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Mission Phasing", "Stressed Operation");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Mission Phasing", "Transport");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Nonionizing Radiation", "Infrared");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Nonionizing Radiation", "Laser");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Nonionizing Radiation", "Microwave");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Nonionizing Radiation", "Ultraviolet");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Physiological", "Allergens");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Physiological", "Asphyxiants");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Physiological", "Baropressure Extremes");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Physiological", "Carcinogens");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Physiological", "Cryogens");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Physiological", "Fatigue");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Physiological", "Irritants");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Physiological", "Lifted Weights");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Physiological", "Mutagens");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Physiological", "Noise");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Physiological", "Nuisance Dust/Odors");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Physiological", "Pathogens");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Physiological", "Temperature Extremes");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Physiological", "Teratogens");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Physiological", "Toxins");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Physiological", "Vibration (Raynaud’s Syndrome)");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Pneumatic/Hydraulic", "Backflow");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Pneumatic/Hydraulic", "Blown Objects");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Pneumatic/Hydraulic", "Crossflow");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Pneumatic/Hydraulic", "Dynamic Pressure Loading");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Pneumatic/Hydraulic", "Hydraulic Ram");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Pneumatic/Hydraulic", "Implosion");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Pneumatic/Hydraulic", "Inadvertent Release");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Pneumatic/Hydraulic", "Miscalibrated Relief Device");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Pneumatic/Hydraulic", "Mislocated Relief Device");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Pneumatic/Hydraulic", "Overpressurization");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Pneumatic/Hydraulic", "Pipe/Hose Whip");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Pneumatic/Hydraulic", "Pipe/Vessel/Duct Rupture");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Pneumatic/Hydraulic", "Relief Pressure Improperly Set");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Thermal", "Altered Structural Properties (e.g., Embrittlement)");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Thermal", "Confined Gas/Liquid");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Thermal", "Elevated Flammability");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Thermal", "Elevated Reactivity");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Thermal", "Elevated Volatility");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Thermal", "Freezing");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Thermal", "Heat Source/Sink");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Thermal", "Hot/Cold Surface Burns");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Thermal", "Humidity/Moisture");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Thermal", "Pressure Evaluation");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Unannunciated Utility Outages", "Air Conditioning");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Unannunciated Utility Outages", "Compressed Air/Gas");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Unannunciated Utility Outages", "Electricity");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Unannunciated Utility Outages", "Exhaust");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Unannunciated Utility Outages", "Fuel");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Unannunciated Utility Outages", "Heating/Cooling");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Unannunciated Utility Outages", "Lubrication Drains/Sumps");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Unannunciated Utility Outages", "Steam");
INSERT INTO "tbl_hazards" ("fld_category", "fld_subcategory") VALUES ("Unannunciated Utility Outages", "Ventilation");

--
-- Create tables used to store information for software reliability
-- predictions.
--
DROP TABLE IF EXISTS "tbl_development_environment";
CREATE TABLE "tbl_development_environment" (
  "fld_development_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_development_desc" VARCHAR(32) DEFAULT NULL,
  "fld_do" FLOAT DEFAULT NULL
);
INSERT INTO "tbl_development_environment" VALUES (1,'Organic',0.76);
INSERT INTO "tbl_development_environment" VALUES (2,'Semi-Detached',1);
INSERT INTO "tbl_development_environment" VALUES (3,'Embedded',1.3);

DROP TABLE IF EXISTS "tbl_development_phase";
CREATE TABLE "tbl_development_phase" (
  "fld_phase_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_phase_desc" VARCHAR(64) DEFAULT NULL
);
INSERT INTO "tbl_development_phase" VALUES (1,'Requirements Review (SRR)');
INSERT INTO "tbl_development_phase" VALUES (2,'Requirements Analysis (SSR)');
INSERT INTO "tbl_development_phase" VALUES (3,'Preliminary Design Review (PDR)');
INSERT INTO "tbl_development_phase" VALUES (4,'Critical Design Review (CDR)');
INSERT INTO "tbl_development_phase" VALUES (5,'Test Readiness Review (TRR)');
INSERT INTO "tbl_development_phase" VALUES (6,'Released');

DROP TABLE IF EXISTS "tbl_software_application";
CREATE TABLE "tbl_software_application" (
  "fld_application_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_application_desc" VARCHAR(32) DEFAULT NULL,
  "fld_fault_density" FLOAT DEFAULT NULL,
  "fld_transformation_ratio" FLOAT DEFAULT NULL
);
INSERT INTO "tbl_software_application" VALUES (0,'Airborne',0.0128,6.28);
INSERT INTO "tbl_software_application" VALUES (1,'Strategic',0.0092,1.2);
INSERT INTO "tbl_software_application" VALUES (2,'Tactical',0.0078,13.8);
INSERT INTO "tbl_software_application" VALUES (3,'Process Control',0.0018,3.8);
INSERT INTO "tbl_software_application" VALUES (4,'Production Center',0.0085,23);
INSERT INTO "tbl_software_application" VALUES (5,'Developmental',0.0123,132.6);

DROP TABLE IF EXISTS "tbl_software_category";
CREATE TABLE "tbl_software_category"(
    "fld_category_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_category_name" VARCHAR(128),
    "fld_category_description" BLOB
);
INSERT INTO "tbl_software_category" VALUES (0, "Batch (General)", "Can be run as a normal batch job and makes no unusual hardware or input-output actions (e.g., payroll program and wind tunnel data analysis program). Small, throwaway programs for preliminary analysis also fit in this category.");
INSERT INTO "tbl_software_category" VALUES (1, "Event Control", "Does realtime processing of data resulting from external events. An example might be a computer program that processes telemetry data.");
INSERT INTO "tbl_software_category" VALUES (2, "Process Control", "Receives data from an external source and issues commands to that source to control its actions based on the received data.");
INSERT INTO "tbl_software_category" VALUES (3, "Procedure Control", "Controls other software; for example, an operrting system that controls execution of time-shared and batch computer programs.");
INSERT INTO "tbl_software_category" VALUES (4, "Navigation", "Does computation and modeling to computer information required to guide an airplane from point of origin to destination.");
INSERT INTO "tbl_software_category" VALUES (5, "Flight Dynamics", "Uses the functions computed by naviga-ion software and augmented by control theory to control the entire flight of an aircraft.");
INSERT INTO "tbl_software_category" VALUES (6, "Orbital Dynamics", "Resembles navigation and flight dynamics software,-but has the additional complexity required by orbital navigation, such as a more complex reference system and the inclusion of gravitational effects of other heavenly bodies.");
INSERT INTO "tbl_software_category" VALUES (7, "Message Processing", "Handles input and output mnessages. processing the text or information contained therein.");
INSERT INTO "tbl_software_category" VALUES (8, "Diagnostic Software", "Used to detect and isolate hardware errors in the computer in which it resides or in other hardware that can communicate with the computer.");
INSERT INTO "tbl_software_category" VALUES (9, "Sensor and Signal Processing", "Similar to that of message processing, except that it required greater processing, analyzing, and transforming the input into a usable data processing format.");
INSERT INTO "tbl_software_category" VALUES (10, "Simulation", "Used to simulate and environmentmr ieseion situation. other heavradlwuaatrieo,n aonfd a icnopmutps uftreo mpr otghreasme nt o enable a more realistic or a piece of hardware.");
INSERT INTO "tbl_software_category" VALUES (11, "Database Management", "Manages the storage and access of (typically large) groups of data. Such software can also often prepare reports in user-defined formats, based on the contents of the database.");
INSERT INTO "tbl_software_category" VALUES (12, "Data Acquisition", "Receives information in real-time and stores 'it in some form suitable for later processing, for example, software that receives data from a space probe ,and files.");
INSERT INTO "tbl_software_category" VALUES (13, "Data Presentation", "Formats and transforms data, as necessary, for convenienit and understandable displays for humans. Typically, such _displays would bi- for some screen presentation.");
INSERT INTO "tbl_software_category" VALUES (14, "Decision and Planning Aids", "Uses arcial intelligence techniques to provide an expert system to evaluate data and provide additional information and consideration for decision and policy makers.");
INSERT INTO "tbl_software_category" VALUES (15, "Pattern and Image Processing", "Used for computer image generation and processing. Such software may analyze terrain data and generate images based on stored data.");
INSERT INTO "tbl_software_category" VALUES (16, "Computer System Software", "Provides services to operational computer programs (i.e., problem oriented).");
INSERT INTO "tbl_software_category" VALUES (17, "Software Development Tools", "Provides services to aid in the development of software (e.g., compilers, assemblers, static and dynamic analyzers).");

DROP TABLE IF EXISTS "tbl_software_level";
CREATE TABLE "tbl_software_level" (
  "fld_level_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_level_desc" VARCHAR(64) DEFAULT NULL
);
INSERT INTO "tbl_software_level" VALUES (0,'Software System');
INSERT INTO "tbl_software_level" VALUES (1,'Software Module');
INSERT INTO "tbl_software_level" VALUES (2,'Software Unit');

DROP TABLE IF EXISTS "tbl_test_techniques";
CREATE TABLE "tbl_test_techniques" (
    "fld_technique_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_technique_name" VARCHAR(64),
    "fld_technique_type" INTEGER,
    "fld_technique_description" BLOB
);
INSERT INTO "tbl_test_techniques" VALUES (0, "Code Reviews", 0, "Code review is a systematic examination (often known as peer review) of computer source code.");
INSERT INTO "tbl_test_techniques" VALUES (1, "Error/Anomaly Detection", 0, "");
INSERT INTO "tbl_test_techniques" VALUES (2, "Structure Analysis", 0, "");
INSERT INTO "tbl_test_techniques" VALUES (3, "Random Testing", 0, "");
INSERT INTO "tbl_test_techniques" VALUES (4, "Functional Testing", 0, "");
INSERT INTO "tbl_test_techniques" VALUES (5, "Branch Testing", 0, "");

--
-- Create tables for FMEA/FMECA work.
--
DROP TABLE IF EXISTS "tbl_failure_modes";
CREATE TABLE "tbl_failure_modes" (
    "fld_category_id" INTEGER NOT NULL DEFAULT(0),
    "fld_subcategory_id" INTEGER NOT NULL DEFAULT(0),
    "fld_mode_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_mode_description" VARCHAR(256),
    "fld_mode_ratio" FLOAT
);
INSERT INTO "tbl_failure_modes" VALUES (4,40,1,"Shorted",0.6);
INSERT INTO "tbl_failure_modes" VALUES (4,40,2,"Opened",0.35);
INSERT INTO "tbl_failure_modes" VALUES (4,40,3,"Parametric Drift",0.05);
INSERT INTO "tbl_failure_modes" VALUES (4,41,4,"",0.0);
INSERT INTO "tbl_failure_modes" VALUES (1000,1,1,"Function fails to occur when required",0.0);
INSERT INTO "tbl_failure_modes" VALUES (1000,1,2,"Function occurs when not required",0.0);
INSERT INTO "tbl_failure_modes" VALUES (1000,1,3,"Function occurs when required, but under performs (i.e., too little function)",0.0);
INSERT INTO "tbl_failure_modes" VALUES (1000,1,4,"Function occurs when required, but over performs (i.e., too much function)",0.0);
INSERT INTO "tbl_failure_modes" VALUES (1000,1,5,"Function occurs when required, but is erratic/intermittent",0.0);

DROP TABLE IF EXISTS "tbl_failure_mechanisms";
CREATE TABLE "tbl_failure_mechanisms" (
    "fld_mode_id" INTEGER NOT NULL DEFAULT(0),
    "fld_mechanism_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_meschanism_description" VARCHAR(256)
);
INSERT INTO "tbl_failure_mechanisms" VALUES (1,1,"Corrosion");
INSERT INTO "tbl_failure_mechanisms" VALUES (1,2,"Seal Leakage");
INSERT INTO "tbl_failure_mechanisms" VALUES (2,3,"Corrosion");

DROP TABLE IF EXISTS "tbl_rpn_severity";
CREATE TABLE "tbl_rpn_severity" (
    "fld_severity_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_severity_name" VARCHAR(512),
    "fld_severity_description" VARCHAR(512),
    "fld_fmeca_type" INTEGER DEFAULT (0)
);
INSERT INTO "tbl_rpn_severity" VALUES(1,"None","No effect.",0);
INSERT INTO "tbl_rpn_severity" VALUES(2,"Very Minor","System operable with minimal interference.",0);
INSERT INTO "tbl_rpn_severity" VALUES(3,"Minor","System operable with some degradation of performance.",0);
INSERT INTO "tbl_rpn_severity" VALUES(4,"Very Low","System operable with significant degradation of performance.",0);
INSERT INTO "tbl_rpn_severity" VALUES(5,"Low","System inoperable without damage.",0);
INSERT INTO "tbl_rpn_severity" VALUES(6,"Moderate","System inoperable with minor damage.",0);
INSERT INTO "tbl_rpn_severity" VALUES(7,"High","System inoperable with system damage.",0);
INSERT INTO "tbl_rpn_severity" VALUES(8,"Very High","System inoperable with destructive failure without compromising safety.",0);
INSERT INTO "tbl_rpn_severity" VALUES(9,"Hazardous, with warning","Failure effects safe system operation with warning.",0);
INSERT INTO "tbl_rpn_severity" VALUES(10,"Hazardous, without warning","Failure effects safe system operation without warning.",0);

DROP TABLE IF EXISTS "tbl_rpn_occurrence";
CREATE TABLE "tbl_rpn_occurrence" (
    "fld_occurrence_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_occurrence_name" VARCHAR(512),
    "fld_occurrence_description" VARCHAR(512),
    "fld_fmeca_type" INTEGER DEFAULT (0)
);
INSERT INTO "tbl_rpn_occurrence" VALUES(1,"Remote","Failure rate is 1 in 1,500,000.",0);
INSERT INTO "tbl_rpn_occurrence" VALUES(2,"Very Low","Failure rate is 1 in 150,000.",0);
INSERT INTO "tbl_rpn_occurrence" VALUES(3,"Low","Failure rate is 1 in 15,000",0);
INSERT INTO "tbl_rpn_occurrence" VALUES(4,"Moderately Low","Failure rate is 1 in 2000.",0);
INSERT INTO "tbl_rpn_occurrence" VALUES(5,"Moderate","Failure rate is 1 in 400.",0);
INSERT INTO "tbl_rpn_occurrence" VALUES(6,"Moderately High","Failure rate is 1 in 80.",0);
INSERT INTO "tbl_rpn_occurrence" VALUES(7,"High","Failure rate is 1 in 20.",0);
INSERT INTO "tbl_rpn_occurrence" VALUES(8,"Very High","Failure rate is 1 in 8.",0);
INSERT INTO "tbl_rpn_occurrence" VALUES(9,"Extremely High","Failure rate is 1 in 3.",0);
INSERT INTO "tbl_rpn_occurrence" VALUES(10,"Dangerously High","Failure rate is > 1 in 2.",0);

DROP TABLE IF EXISTS "tbl_rpn_detection";
CREATE TABLE "tbl_rpn_detection" (
    "fld_detection_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_detection_name" VARCHAR(512),
    "fld_detection_description" VARCHAR(512),
    "fld_fmeca_type" INTEGER DEFAULT (0)
);
INSERT INTO "tbl_rpn_detection" VALUES(1,"Almost Certain","Design control will almost certainly detect a potential mechanism/cause and subsequent failure mode.",0);
INSERT INTO "tbl_rpn_detection" VALUES(2,"Very High","Very high chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.",0);
INSERT INTO "tbl_rpn_detection" VALUES(3,"High","High chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.",0);
INSERT INTO "tbl_rpn_detection" VALUES(4,"Moderately High","Moderately high chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.",0);
INSERT INTO "tbl_rpn_detection" VALUES(5,"Moderate","Moderate chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.",0);
INSERT INTO "tbl_rpn_detection" VALUES(6,"Low","Low chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.",0);
INSERT INTO "tbl_rpn_detection" VALUES(7,"Very Low","Very low chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.",0);
INSERT INTO "tbl_rpn_detection" VALUES(8,"Remote","Remote chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.",0);
INSERT INTO "tbl_rpn_detection" VALUES(9,"Very Remote","Very remote chance the existing design controls will or can detect a potential mechanism/cause and subsequent failure mode.",0);
INSERT INTO "tbl_rpn_detection" VALUES(10,"Absolute Uncertainty","Existing design controls will not or cannot detect a potential mechanism/cause and subsequent failure mode; there is no design control.",0);

DROP TABLE IF EXISTS "tbl_risk_category";
CREATE TABLE "tbl_risk_category" (
  "fld_category_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_category_noun" VARCHAR(64) NOT NULL,
  "fld_category_value" INTEGER DEFAULT (0)
);
INSERT INTO "tbl_risk_category" VALUES (0,'Category I',0);
INSERT INTO "tbl_risk_category" VALUES (1,'Category II',1);
INSERT INTO "tbl_risk_category" VALUES (2,'Category III',2);
INSERT INTO "tbl_risk_category" VALUES (3,'Category IV',3);

DROP TABLE IF EXISTS "tbl_action_category";
CREATE TABLE "tbl_action_category" (
    "fld_action_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "fld_action_name" VARCHAR(128)
);
INSERT INTO "tbl_action_category" VALUES(0,"Engineering, Design");
INSERT INTO "tbl_action_category" VALUES(1,"Engineering, Reliability");
INSERT INTO "tbl_action_category" VALUES(2,"Engineering, Systems");
INSERT INTO "tbl_action_category" VALUES(3,"Manufacturing");
INSERT INTO "tbl_action_category" VALUES(4,"Test");
INSERT INTO "tbl_action_category" VALUES(5,"Verification & Validation");

--
-- Create tables for use with program incidents.
--
DROP TABLE IF EXISTS "tbl_incident_category";
CREATE TABLE "tbl_incident_category" (
  "fld_incident_cat_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_incident_cat_name" VARCHAR(256)
);
INSERT INTO "tbl_incident_category" VALUES (1, "Hardware");
INSERT INTO "tbl_incident_category" VALUES (2, "Software");
INSERT INTO "tbl_incident_category" VALUES (3, "Process");

DROP TABLE IF EXISTS "tbl_incident_type";
CREATE TABLE "tbl_incident_type" (
  "fld_incident_type_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_incident_type_name" VARCHAR(256)
);
INSERT INTO "tbl_incident_type" VALUES (1, "Planning");
INSERT INTO "tbl_incident_type" VALUES (2, "Concept");
INSERT INTO "tbl_incident_type" VALUES (3, "Requirement");
INSERT INTO "tbl_incident_type" VALUES (4, "Design");
INSERT INTO "tbl_incident_type" VALUES (5, "Coding");
INSERT INTO "tbl_incident_type" VALUES (6, "Database");
INSERT INTO "tbl_incident_type" VALUES (7, "Test Information");
INSERT INTO "tbl_incident_type" VALUES (8, "Manuals");
INSERT INTO "tbl_incident_type" VALUES (9, "Other");

DROP TABLE IF EXISTS "tbl_incident_relevency";
CREATE TABLE "tbl_incident_relevency" (
  "fld_relevency_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_relevency_q" VARCHAR(512),
  "fld_y_status" INTEGER DEFAULT (1)
);
INSERT INTO "tbl_incident_relevency" VALUES (1, "This failure occurred on equipment or a component part that is production intent.", -1);
INSERT INTO "tbl_incident_relevency" VALUES (2, "This failure is independent of any other failure.", -1);
INSERT INTO "tbl_incident_relevency" VALUES (3, "This failure is due to design deficiencies or poor workmanship of the equipment or component part.", 1);
INSERT INTO "tbl_incident_relevency" VALUES (4, "This failure is due to a defective component part.", 1);
INSERT INTO "tbl_incident_relevency" VALUES (5, "This failure is due to a component part that wore out prior to it's stipulated life.", 1);
INSERT INTO "tbl_incident_relevency" VALUES (6, "This failure is the first occurrence of an intermittent failure on this equipment.", 1);
INSERT INTO "tbl_incident_relevency" VALUES (7, "This failure is a malfunction (including false alarm) of the built-in test features.", 1);
INSERT INTO "tbl_incident_relevency" VALUES (8, "This failure is due to misadjustment of operator controls AND the information necessary to properly adjust these controls is not available from indicators which are integral to the equipment under test.", 1);
INSERT INTO "tbl_incident_relevency" VALUES (9, "This failure is dependent on another, relevent, failure.", 0);
INSERT INTO "tbl_incident_relevency" VALUES (10, "This failure is directly attributable to improper test setup.", 0);
INSERT INTO "tbl_incident_relevency" VALUES (11, "This failure is the failure of test insrumentation or monitoring equipment (other than built-in test equipment).", 0);
INSERT INTO "tbl_incident_relevency" VALUES (12, "This failure is the result of test operator error.", 0);
INSERT INTO "tbl_incident_relevency" VALUES (13, "This failure is attributable to an error in the test procedure.", 0);
INSERT INTO "tbl_incident_relevency" VALUES (14, "This failure is the second or subsequent intermittent failure on this equipment.", 0);
INSERT INTO "tbl_incident_relevency" VALUES (15, "This failure occurred during burn-in, troubleshooting, repair verification, or setup.", 0);
INSERT INTO "tbl_incident_relevency" VALUES (16, "This failure is clearly attributable to an overstress condition in excess of the design requirements.", 0);

DROP TABLE IF EXISTS "tbl_chargeability";
CREATE TABLE "tbl_chargeability" (
  "fld_chargeability_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_chargeability_q" VARCHAR(512) DEFAULT NULL,
  "fld_order" INTEGER NOT NULL DEFAULT(0),
  "fld_y_next" INTEGER NOT NULL DEFAULT(82),
  "fld_n_next" INTEGER NOT NULL DEFAULT(82)
);

--
-- Creae tables to use with verification and validation tasks.
--
DROP TABLE IF EXISTS "tbl_validation_type";
CREATE TABLE "tbl_validation_type" (
  "fld_validation_type_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fld_validation_type_desc" VARCHAR(128) DEFAULT NULL,
  "fld_validation_type_code" VARCHAR(16) DEFAULT NULL
);
INSERT INTO "tbl_validation_type" VALUES (1,'System Engineering','SYS');
INSERT INTO "tbl_validation_type" VALUES (2,'Reliability Analysis','REL');
INSERT INTO "tbl_validation_type" VALUES (3,'Design for X','DFX');
INSERT INTO "tbl_validation_type" VALUES (4,'SubSystem Reliability Testing','SRT');

END TRANSACTION;
